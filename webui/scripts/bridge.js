/* ============================================================
   bridge.js — QWebChannel 桥接层
   - 等待 qt.webChannelTransport 就绪
   - 把 PythonBridge 的 slot 包成 Promise 风格的 JS API
   - 提供 onChanged 订阅（接收 Python 推送的信号）
   ============================================================ */

(function (global) {
  'use strict';

  // PythonBridge 实例（由 QWebChannel 注入）
  let _bridge = null;
  let _ready = false;
  const _readyCallbacks = [];
  const _subscribers = {
    themeChanged: [],
    pluginsChanged: [],
  };

  /**
   * 初始化 QWebChannel，拿到 PythonBridge。
   * 在 PySide6 中通过 setWebChannel 注册后，window.qt.webChannelTransport 会出现。
   */
  function init() {
    return new Promise((resolve) => {
      if (typeof qt === 'undefined' || !qt.webChannelTransport) {
        // 不在 WebEngine 环境中（例如浏览器预览），用一个 mock 供调试
        console.warn('[bridge] 不在 QWebEngine 环境中，使用 mock bridge');
        _bridge = makeMockBridge();
        _ready = true;
        _readyCallbacks.forEach((cb) => cb(_bridge));
        _readyCallbacks.length = 0;
        resolve(_bridge);
        return;
      }

      new QWebChannel(qt.webChannelTransport, (channel) => {
        _bridge = channel.objects.bridge;
        if (!_bridge) {
          console.error('[bridge] channel.objects.bridge 不存在');
          return;
        }

        // 订阅 Python 信号
        if (_bridge.themeChanged) {
          _bridge.themeChanged.connect((jsonStr) => {
            try {
              const data = JSON.parse(jsonStr);
              _subscribers.themeChanged.forEach((cb) => cb(data));
            } catch (e) {
              console.error('[bridge] themeChanged parse error', e);
            }
          });
        }
        if (_bridge.pluginsChanged) {
          _bridge.pluginsChanged.connect((jsonStr) => {
            try {
              const data = JSON.parse(jsonStr);
              _subscribers.pluginsChanged.forEach((cb) => cb(data));
            } catch (e) {
              console.error('[bridge] pluginsChanged parse error', e);
            }
          });
        }

        _ready = true;
        _readyCallbacks.forEach((cb) => cb(_bridge));
        _readyCallbacks.length = 0;
        resolve(_bridge);
      });
    });
  }

  function onReady(cb) {
    if (_ready) cb(_bridge);
    else _readyCallbacks.push(cb);
  }

  function on(signal, cb) {
    if (!_subscribers[signal]) _subscribers[signal] = [];
    _subscribers[signal].push(cb);
  }

  // ---- 异步 API（QWebChannel slot 返回值通过 callback 获取） ----
  // PySide6: @Slot(result=str) 配合调用方 bridge.getInitialState()
  // 但 QWebChannel 异步语义是 .getInitialState(callback)

  function call(method, ...args) {
    return new Promise((resolve, reject) => {
      if (!_bridge || typeof _bridge[method] !== 'function') {
        reject(new Error(`bridge.${method} not available`));
        return;
      }
      try {
        _bridge[method](...args, (result) => resolve(result));
      } catch (e) {
        // 同步 slot（无 callback）
        try {
          const r = _bridge[method](...args);
          resolve(r);
        } catch (e2) {
          reject(e2);
        }
      }
    });
  }

  // ---- 高层 API ----
  const API = {
    init,
    onReady,
    on,

    getInitialState: () => call('getInitialState'),
    getPlugins:      () => call('getPlugins'),
    getTheme:        () => call('getTheme'),
    openModule:      (name) => call('openModule', name),
    toggleModule:    (name, enabled) => call('toggleModule', name, enabled),
    setTheme:        (style, mode) => call('setTheme', style, mode),
    importTheme:     () => call('importTheme'),
    exitApp:         () => call('exitApp'),
    getLogoUrl:      () => call('getLogoUrl'),
    getAboutInfo:    () => call('getAboutInfo'),
  };

  // ---- Mock bridge（浏览器预览 / 调试用） ----
  function makeMockBridge() {
    const cats = ['tools', 'calendar', 'links'];
    const plugins = [
      { name: 'caidan', icon: '🥚', title: '彩蛋', description: '神秘彩蛋', category: 'tools', kind: 'window', enabled: true },
      { name: 'calculator', icon: '🔢', title: '简易计算器', description: '基础四则运算', category: 'tools', kind: 'window', enabled: true },
      { name: 'chat_room', icon: '💬', title: '聊天室', description: '在线聊天', category: 'tools', kind: 'window', enabled: true },
      { name: 'ai_bot', icon: '🤖', title: 'AI机器人', description: '余额用尽', category: 'tools', kind: 'window', enabled: false },
      { name: 'ticket', icon: '🎫', title: '查火车票', description: '暂未开放', category: 'tools', kind: 'window', enabled: false },
      { name: 'copyright', icon: '©', title: '版权声明', description: '希望工作室版权', category: 'tools', kind: 'window', enabled: true },
      { name: 'shit', icon: '💩', title: '探索系统屎山', description: '关机命令与官网', category: 'tools', kind: 'window', enabled: true },
      { name: 'shutdown', icon: '⏻', title: '关机命令集', description: '调起系统关机', category: 'tools', kind: 'window', enabled: true },
      { name: 'calendar', icon: '📅', title: '日历', description: '月历视图', category: 'calendar', kind: 'page', enabled: true },
      { name: 'website', icon: '🌐', title: '我们的网站', description: 'hopestudio.top', category: 'links', kind: 'window', enabled: true },
      { name: 'bilibili', icon: '📺', title: '哔哩哔哩', description: '主站空间', category: 'links', kind: 'window', enabled: true },
      { name: 'github', icon: '🐙', title: 'GitHub', description: '项目仓库', category: 'links', kind: 'window', enabled: true },
    ];
    return {
      getInitialState: (cb) => cb(JSON.stringify({
        version: '2.1.0-mock',
        categories: cats,
        plugins,
        theme: { style: 'cupertino', mode: 'light', availableStyles: ['md3','md2','qt','winui3','win10fluent','gnome','kde','cupertino','chromeos'], isDark: false, colors: {} },
      })),
      getPlugins: (cb) => cb(JSON.stringify(plugins)),
      getTheme: (cb) => cb(JSON.stringify({ style: 'cupertino', mode: 'light', availableStyles: ['cupertino','md3'], isDark: false, colors: {} })),
      openModule: (n, cb) => { console.log('openModule', n); cb(true); },
      toggleModule: (n, e, cb) => { console.log('toggleModule', n, e); cb(true); },
      setTheme: (s, m, cb) => { console.log('setTheme', s, m); cb('{}'); },
      importTheme: (cb) => cb(false),
      exitApp: () => console.log('exitApp'),
      getLogoUrl: (cb) => cb(''),
      getAboutInfo: (cb) => cb(JSON.stringify({
        name: 'HopeKit (Mock)',
        version: '2.2.0-mock',
        description: 'Mock 环境预览。',
        copyright: '© 2026 HopeKit. All rights reserved.',
      })),
    };
  }

  global.HopeBridge = API;
})(window);
