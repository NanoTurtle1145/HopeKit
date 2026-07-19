/* ============================================================
   main.js — 入口
   等待 DOMContentLoaded，先初始化 bridge（异步 QWebChannel），
   然后调用 app.init() 完成首次渲染。
   ============================================================ */

(function () {
  'use strict';

  function boot() {
    HopeBridge.init()
      .then(() => HopeApp.init())
      .catch((err) => {
        console.error('[boot] 初始化失败', err);
        // 显示致命错误
        document.body.innerHTML = `
          <div style="display:flex;align-items:center;justify-content:center;
                      height:100vh;flex-direction:column;gap:8px;
                      font-family:system-ui;color:#1D1D1F;background:#F5F5F7;">
            <h2 style="margin:0;font-size:22px;font-weight:600;">HopeKit UI 初始化失败</h2>
            <p style="margin:0;color:#6D6D72;font-size:13px;">${String(err.message || err)}</p>
          </div>`;
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
