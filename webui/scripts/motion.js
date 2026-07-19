/* ============================================================
   motion.js — 弹簧动画引擎
   Apple Designing Fluid Interfaces (WWDC 2018) 原则：
   - 阻尼 + 响应（不是 mass/stiffness/damping）
   - 可中断：re-target 时从当前展示值 + 当前速度衔接
   - 速度追踪：每次 RAF 记录位移历史
   - 临界阻尼默认（damping 1.0）；动量交互才用 0.8
   ============================================================ */

(function (global) {
  'use strict';

  const reducedMotion = global.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;

  // ---- Spring 物理 ----
  // 参考 Apple公式：a = -k*(x - target) - c*v
  // k 由 response 推导：k = (2π / response)^2
  // c 由 damping 推导：c = 2 * damping * sqrt(k) （1.0 = 临界）
  function springCoeffs(damping, response) {
    const k = Math.pow(2 * Math.PI / response, 2);
    const c = 2 * damping * Math.sqrt(k);
    return { k, c };
  }

  /**
   * SpringAnimator — 单轴弹簧动画
   * - 从 currentValue 起跳，带初始 velocity
   * - 调用 .target(t, v) 可随时改目标（保留当前速度）
   * - 调用 .stop() 立即停止
   */
  class SpringAnimator {
    constructor(opts = {}) {
      this.damping = opts.damping ?? 1.0;       // 1.0 = 临界阻尼
      this.response = opts.response ?? 0.32;    // s
      this.from = opts.from ?? 0;
      this.to = opts.to ?? 0;
      this.initialVelocity = opts.velocity ?? 0;
      this.onUpdate = opts.onUpdate ?? (() => {});
      this.onComplete = opts.onComplete ?? (() => {});

      this._raf = null;
      this._startTime = 0;
      this._lastTime = 0;
      this._position = this.from;
      this._velocity = this.initialVelocity;
      this._running = false;
      this._settled = false;
    }

    /** 改变目标：保留当前位置与速度 */
    target(newTo, newVelocity) {
      this.to = newTo;
      if (typeof newVelocity === 'number') {
        this._velocity = newVelocity;
      }
      if (this._settled) {
        // 已落定，重新启动
        this._settled = false;
        this._running = false;
        this._start();
      }
    }

    start() {
      this._position = this.from;
      this._velocity = this.initialVelocity;
      this._settled = false;
      this._start();
    }

    _start() {
      if (this._running || reducedMotion) {
        // reduced-motion：直接到目标，无动画
        if (reducedMotion) {
          this._position = this.to;
          this._velocity = 0;
          this.onUpdate(this._position);
          this._settled = true;
          this.onComplete(this._position, true);
          return;
        }
        return;
      }
      this._running = true;
      this._startTime = performance.now();
      this._lastTime = this._startTime;
      this._raf = requestAnimationFrame(this._tick);
    }

    _tick = (now) => {
      const dt = Math.min((now - this._lastTime) / 1000, 1 / 30); // 防止 tab 切换的大 dt
      this._lastTime = now;

      const { k, c } = springCoeffs(this.damping, this.response);
      const x = this._position - this.to;
      const a = -k * x - c * this._velocity;

      // 半隐式 Euler：先更新速度，再用新速度更新位置（更稳定）
      this._velocity += a * dt;
      this._position += this._velocity * dt;

      this.onUpdate(this._position);

      // 落定判定：位移足够小 + 速度足够小
      const settled = Math.abs(this.to - this._position) < 0.4
                   && Math.abs(this._velocity) < 0.4;
      if (settled) {
        this._position = this.to;
        this._velocity = 0;
        this.onUpdate(this._position);
        this._running = false;
        this._settled = true;
        this._raf = null;
        this.onComplete(this._position, true);
        return;
      }
      this._raf = requestAnimationFrame(this._tick);
    };

    stop() {
      if (this._raf) {
        cancelAnimationFrame(this._raf);
        this._raf = null;
      }
      this._running = false;
    }

    get currentValue() { return this._position; }
    get currentVelocity() { return this._velocity; }
    get isRunning() { return this._running; }
  }

  /**
   * animateSpring — 便捷单次动画
   * @returns {SpringAnimator}
   */
  function animateSpring(opts) {
    const a = new SpringAnimator(opts);
    a.start();
    return a;
  }

  /**
   * projectMomentum — Apple 投影函数（指数衰减）
   * 用于 swipe 释放时预测静止点
   *   v (px/s), decelerationRate ≈ 0.998
   */
  function projectMomentum(initialVelocity, decelerationRate = 0.998) {
    return (initialVelocity / 1000) * decelerationRate / (1 - decelerationRate);
  }

  /**
   * nearestSnap — 在投影点附近找最近的吸附点
   */
  function nearestSnap(position, snapPoints) {
    let best = snapPoints[0];
    let bestDist = Math.abs(position - best);
    for (let i = 1; i < snapPoints.length; i++) {
      const d = Math.abs(position - snapPoints[i]);
      if (d < bestDist) {
        best = snapPoints[i];
        bestDist = d;
      }
    }
    return best;
  }

  /**
   * rubberband — Apple 边界阻尼
   * overshoot 越大，跟随越少
   */
  function rubberband(overshoot, dimension, constant = 0.55) {
    return (overshoot * dimension * constant) / (dimension + constant * Math.abs(overshoot));
  }

  /**
   * crossfade — 两元素之间的纯淡入淡出（用于 reduced-motion 或非手势切换）
   */
  function crossfade(fromEl, toEl, duration = 200) {
    if (reducedMotion) duration = 1;
    fromEl.style.transition = `opacity ${duration}ms var(--ease-out, ease-out)`;
    toEl.style.transition = `opacity ${duration}ms var(--ease-out, ease-out)`;
    fromEl.style.opacity = '0';
    toEl.style.opacity = '0';
    requestAnimationFrame(() => {
      toEl.style.opacity = '1';
    });
    setTimeout(() => {
      fromEl.style.transition = '';
      toEl.style.transition = '';
    }, duration + 16);
  }

  /**
   * springDrawer — 用于 sidebar 折叠/展开：
   * 在 minimumWidth 与 maximumWidth 上同时跑弹簧
   * 阻尼 0.8 / 响应 0.3（Apple sheet 风格）
   */
  function springDrawer(element, fromWidth, toWidth, opts = {}) {
    const damping = opts.damping ?? 0.8;
    const response = opts.response ?? 0.3;
    const velocity = opts.velocity ?? 0;

    // 同时动画 min/max width（避免布局抖动）
    const animMin = new SpringAnimator({
      damping, response, from: fromWidth, to: toWidth, velocity,
      onUpdate: (v) => { element.style.minWidth = `${v}px`; },
    });
    const animMax = new SpringAnimator({
      damping, response, from: fromWidth, to: toWidth, velocity,
      onUpdate: (v) => { element.style.maxWidth = `${v}px`; },
    });
    animMin.start();
    animMax.start();
    return {
      stop: () => { animMin.stop(); animMax.stop(); },
      retarget: (newTo, newV) => {
        animMin.target(newTo, newV);
        animMax.target(newTo, newV);
      },
    };
  }

  global.HopeMotion = {
    SpringAnimator,
    animateSpring,
    projectMomentum,
    nearestSnap,
    rubberband,
    crossfade,
    springDrawer,
    reducedMotion,
  };
})(window);
