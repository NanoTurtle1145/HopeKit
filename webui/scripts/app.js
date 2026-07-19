/* ============================================================
   app.js — 应用状态 + 渲染 + 事件绑定
   职责：
   - 持有 categories / plugins / theme 状态
   - 渲染左侧 nav（含 settings 折叠组）
   - 渲染右侧各分类页（含 module 卡片网格）
   - 处理交互：分类切换 / 模块打开 / 开关 / 主题切换
   - 应用 Apple 设计原则：即时反馈 / 可中断弹簧 / 空间一致性
   ============================================================ */

(function (global) {
  'use strict';

  const state = {
    version: '',
    categories: [],
    plugins: [],
    theme: null,
    aboutInfo: null,
    currentPage: null,    // category key
    settingsExpanded: false,
    settingsSub: null,     // 'theme' | 'about'
    sidebarCollapsed: false,
    _drawerAnim: null,
  };

  // ---- DOM 缓存 ----
  const $ = (sel) => document.querySelector(sel);
  const dom = {};

  function cacheDom() {
    dom.sidebar = $('#sidebar');
    dom.collapseBtn = $('#collapseBtn');
    dom.navList = $('#navList');
    dom.exitBtn = $('#exitBtn');
    dom.content = $('#content');
    dom.pageStack = $('#pageStack');
    dom.contentTitle = $('#contentTitle');
    dom.contentTip = $('#contentTip');
    dom.logoImg = $('#logoImg');
  }

  // ============================================================
  //  RENDER — NAV SIDEBAR
  // ============================================================
  function renderNav() {
    dom.navList.innerHTML = '';

    // 普通分类按钮
    state.categories.forEach((cat) => {
      const li = document.createElement('li');
      const btn = document.createElement('button');
      btn.className = 'nav-item';
      btn.dataset.category = cat;
      btn.setAttribute('aria-current', 'false');
      btn.innerHTML = `
        <span class="nav-icon">${categoryIcon(cat)}</span>
        <span class="nav-label">${cat}</span>
      `;
      btn.addEventListener('click', () => switchCategory(cat));
      // pointerdown 即时反馈（CSS :active 已处理，这里仅记录意图）
      btn.addEventListener('pointerdown', () => {
        btn.dataset.pressTime = String(performance.now());
      });
      li.appendChild(btn);
      dom.navList.appendChild(li);
    });

    // 设置（可折叠二级菜单，放底部）
    const group = document.createElement('li');
    group.className = 'nav-group';
    group.dataset.expanded = String(state.settingsExpanded);

    const header = document.createElement('button');
    header.className = 'nav-group-header nav-item';
    header.innerHTML = `
      <svg class="chevron" viewBox="0 0 12 12" aria-hidden="true">
        <path d="M4 2 8 6 4 10" fill="none" stroke="currentColor"
              stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <span class="nav-icon">⚙</span>
      <span class="nav-label">设置</span>
    `;
    header.addEventListener('click', () => toggleSettingsGroup());

    const childrenWrap = document.createElement('div');
    childrenWrap.className = 'nav-group-children';
    const childrenInner = document.createElement('div');
    const subItems = [
      { key: 'theme', label: '主题', icon: '🎨' },
      { key: 'about', label: '关于', icon: 'ℹ' },
    ];
    subItems.forEach((it) => {
      const b = document.createElement('button');
      b.className = 'nav-item';
      b.dataset.settingsSub = it.key;
      b.setAttribute('aria-current', 'false');
      b.innerHTML = `<span class="nav-icon">${it.icon}</span><span class="nav-label">${it.label}</span>`;
      b.addEventListener('click', () => switchSettingsSub(it.key));
      childrenInner.appendChild(b);
    });
    childrenWrap.appendChild(childrenInner);

    group.appendChild(header);
    group.appendChild(childrenWrap);
    dom.navList.appendChild(group);
  }

  function categoryIcon(cat) {
    const map = { tools: '🧰', calendar: '📅', links: '🔗' };
    return map[cat] || '📦';
  }

  /** 设置 logo 图片，加载失败时隐藏而不是显示 broken image 图标 */
  function setLogo(url) {
    if (!url) {
      dom.logoImg.style.display = 'none';
      const aboutLogo = document.querySelector('#aboutLogo');
      if (aboutLogo) aboutLogo.style.display = 'none';
      return;
    }
    dom.logoImg.style.display = '';
    dom.logoImg.onerror = () => { dom.logoImg.style.display = 'none'; };
    dom.logoImg.src = url;
    const aboutLogo = document.querySelector('#aboutLogo');
    if (aboutLogo) {
      aboutLogo.style.display = '';
      aboutLogo.onerror = () => { aboutLogo.style.display = 'none'; };
      aboutLogo.src = url;
    }
  }

  // ============================================================
  //  RENDER — PAGES
  // ============================================================
  function renderPages() {
    dom.pageStack.innerHTML = '';

    // 每个分类一页
    state.categories.forEach((cat) => {
      const page = document.createElement('section');
      page.className = 'page';
      page.dataset.category = cat;
      page.setAttribute('aria-current', 'false');

      const title = document.createElement('h2');
      title.className = 'page-title';
      title.textContent = cat;
      page.appendChild(title);

      const pluginsInCat = state.plugins.filter((p) => p.category === cat);
      const pagePlugins = pluginsInCat.filter((p) => p.kind === 'page');
      const windowPlugins = pluginsInCat.filter((p) => p.kind !== 'page');

      // page 型：内嵌容器（暂时仅显示提示，因为 PySide6 不支持把 QWidget 嵌入 HTML）
      pagePlugins.forEach((p) => {
        const note = document.createElement('div');
        note.className = 'card';
        note.dataset.disabled = 'true';
        note.innerHTML = `
          <div class="card-icon">${p.icon || '📦'}</div>
          <div class="card-body">
            <div class="card-title">${p.title}</div>
            <div class="card-desc">${p.description || '（嵌入式页面）'}</div>
          </div>
        `;
        page.appendChild(note);
      });

      // window 型：卡片网格
      if (windowPlugins.length > 0) {
        const grid = document.createElement('div');
        grid.className = 'module-grid';
        windowPlugins.forEach((p) => grid.appendChild(makeCard(p, cat)));
        page.appendChild(grid);
      }

      dom.pageStack.appendChild(page);
    });

    // 设置页
    const settingsPage = buildSettingsPage();
    dom.pageStack.appendChild(settingsPage);
  }

  function makeCard(p, category) {
    const card = document.createElement('div');
    card.className = 'card';
    card.dataset.module = p.name;
    card.dataset.disabled = String(!p.enabled);

    card.innerHTML = `
      <div class="card-icon">${p.icon || '📦'}</div>
      <div class="card-body">
        <div class="card-title">${p.title}</div>
        <div class="card-desc">${p.description || ''}</div>
      </div>
      <div class="card-action"></div>
    `;

    const action = card.querySelector('.card-action');

    if (category === 'links') {
      const btn = document.createElement('button');
      btn.className = 'view-btn';
      btn.textContent = '查看';
      btn.dataset.disabled = String(!p.enabled);
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (p.enabled) openModule(p.name);
      });
      action.appendChild(btn);
    } else {
      const toggle = document.createElement('button');
      toggle.className = 'toggle-switch';
      toggle.setAttribute('role', 'switch');
      toggle.setAttribute('aria-checked', String(p.enabled));
      toggle.dataset.module = p.name;
      toggle.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleModule(p.name, !p.enabled);
      });
      action.appendChild(toggle);
    }

    if (p.enabled) {
      card.addEventListener('click', () => openModule(p.name));
    }

    return card;
  }

  // ============================================================
  //  SETTINGS PAGE
  // ============================================================
  function buildSettingsPage() {
    const page = document.createElement('section');
    page.className = 'page';
    page.dataset.category = '__settings';
    page.setAttribute('aria-current', 'false');

    const title = document.createElement('h2');
    title.className = 'page-title';
    title.textContent = '设置';
    page.appendChild(title);

    // ---- 主题 ----
    const themeSection = document.createElement('div');
    themeSection.className = 'settings-section';
    themeSection.innerHTML = `<h3>主题</h3>`;

    const styleGrid = document.createElement('div');
    styleGrid.className = 'theme-grid';
    styleGrid.id = 'themeStyleGrid';
    themeSection.appendChild(styleGrid);

    const modeRow = document.createElement('div');
    modeRow.className = 'settings-row';
    modeRow.innerHTML = `
      <div class="settings-row-label">
        <span class="primary">外观</span>
        <span class="secondary">跟随系统 / 浅色 / 深色</span>
      </div>
    `;
    const seg = document.createElement('div');
    seg.className = 'segmented';
    seg.id = 'themeModeSegmented';
    [['auto', '自动'], ['light', '浅色'], ['dark', '深色']].forEach(([k, l]) => {
      const b = document.createElement('button');
      b.dataset.mode = k;
      b.textContent = l;
      b.setAttribute('aria-checked', 'false');
      b.addEventListener('click', () => setThemeMode(k));
      seg.appendChild(b);
    });
    modeRow.appendChild(seg);
    themeSection.appendChild(modeRow);

    // 颜色样本（仅供视觉示范）
    const previewRow = document.createElement('div');
    previewRow.className = 'settings-row';
    previewRow.innerHTML = `
      <div class="settings-row-label">
        <span class="primary">强调色</span>
        <span class="secondary">由系统强调色决定</span>
      </div>
      <div id="accentSwatch" style="width:32px;height:32px;border-radius:8px;background:var(--color-primary);box-shadow:var(--shadow-1);"></div>
    `;
    themeSection.appendChild(previewRow);

    page.appendChild(themeSection);

    // ---- 关于 ----
    const aboutSection = document.createElement('div');
    aboutSection.className = 'settings-section about-page';
    aboutSection.innerHTML = `
      <h3>关于</h3>
      <img class="about-logo" id="aboutLogo" alt="Logo">
      <div class="about-name" id="aboutName"></div>
      <div class="about-version">版本 <span id="aboutVersion">—</span></div>
      <div class="about-desc" id="aboutDesc"></div>
      <div class="about-copyright" id="aboutCopyright"></div>
    `;
    page.appendChild(aboutSection);

    return page;
  }

  function renderThemeStyleGrid() {
    const grid = $('#themeStyleGrid');
    if (!grid || !state.theme) return;
    grid.innerHTML = '';
    const labels = {
      md3: 'MD3', md2: 'MD2', qt: 'Qt 原生',
      winui3: 'WinUI 3', win10fluent: 'Win10 Fluent',
      gnome: 'GNOME', kde: 'KDE',
      cupertino: 'Cupertino', chromeos: 'ChromeOS',
    };
    state.theme.availableStyles.forEach((s) => {
      const card = document.createElement('button');
      card.className = 'theme-card';
      card.dataset.style = s;
      card.setAttribute('aria-checked', String(s === state.theme.style));
      card.innerHTML = `
        <div class="swatch">
          <span style="background:var(--color-primary)"></span>
          <span style="background:var(--color-surface)"></span>
          <span style="background:var(--color-background)"></span>
        </div>
        <span class="name">${labels[s] || s}</span>
        <span class="check">
          <svg viewBox="0 0 12 12" width="11" height="11" aria-hidden="true">
            <path d="M2 6.5 4.5 9 10 3" fill="none" stroke="currentColor"
                  stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
      `;
      card.addEventListener('click', () => setThemeStyle(s));
      grid.appendChild(card);
    });
  }

  function renderThemeModeSegmented() {
    const seg = $('#themeModeSegmented');
    if (!seg || !state.theme) return;
    Array.from(seg.children).forEach((b) => {
      b.setAttribute('aria-checked', String(b.dataset.mode === state.theme.mode));
    });
  }

  function renderAboutInfo() {
    if (!state.aboutInfo) return;
    const nameEl = document.querySelector('#aboutName');
    const verEl = document.querySelector('#aboutVersion');
    const descEl = document.querySelector('#aboutDesc');
    const copyrightEl = document.querySelector('#aboutCopyright');
    if (nameEl) nameEl.textContent = state.aboutInfo.name;
    if (verEl) verEl.textContent = state.aboutInfo.version;
    if (descEl) descEl.textContent = state.aboutInfo.description;
    if (copyrightEl) copyrightEl.textContent = state.aboutInfo.copyright;
  }

  // ============================================================
  //  NAVIGATION
  // ============================================================
  /** 统一清理所有 nav-item 的 aria-current，再按传入的过滤器勾选 */
  function setNavCurrent(predicate) {
    document.querySelectorAll('.nav-item').forEach((b) => {
      b.setAttribute('aria-current', String(!!predicate(b)));
    });
  }

  function switchCategory(cat) {
    if (state.currentPage === cat) return;
    state.currentPage = cat;
    state.settingsSub = null;

    // 互斥选中态：分类按钮之间、分类 vs 设置子项之间
    setNavCurrent((b) => b.dataset.category === cat);

    // 切换 page（crossfade + 微弱 scale，可中断）
    showPage(`.page[data-category="${cat}"]`);
  }

  function switchSettingsSub(sub) {
    state.settingsSub = sub;
    state.currentPage = '__settings';

    // 自动展开 settings 组
    if (!state.settingsExpanded) toggleSettingsGroup(true);

    setNavCurrent((b) => b.dataset.settingsSub === sub);

    showPage(`.page[data-category="__settings"]`);

    // 滚动到对应子区
    const section = sub === 'theme'
      ? document.querySelector('.settings-section')
      : document.querySelector('.about-page');
    if (section) section.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function toggleSettingsGroup(forceExpand) {
    const shouldExpand = forceExpand ?? !state.settingsExpanded;
    state.settingsExpanded = shouldExpand;
    const group = document.querySelector('.nav-group');
    if (group) group.dataset.expanded = String(shouldExpand);
  }

  let _currentPageEl = null;
  function showPage(selector) {
    const target = document.querySelector(selector);
    if (!target || target === _currentPageEl) return;

    const prev = _currentPageEl;
    _currentPageEl = target;

    // crossfade（Apple 风格的页面切换，crossfade 即可，避免方向性滑动造成迷失）
    if (prev) {
      prev.style.opacity = '0';
      prev.setAttribute('aria-current', 'false');
      setTimeout(() => { prev.style.opacity = ''; }, 200);
    }
    target.setAttribute('aria-current', 'true');
    target.style.opacity = '0';
    requestAnimationFrame(() => {
      target.style.transition = 'opacity 200ms cubic-bezier(0.16,1,0.3,1)';
      target.style.opacity = '1';
      setTimeout(() => { target.style.transition = ''; }, 220);
    });

    // 同步顶部标题
    const cat = target.dataset.category;
    const catLabel = (cat === '__settings') ? '设置' : cat;
    if (cat !== '__settings' && cat) {
      dom.contentTitle.textContent = `HopeKit ${state.version}`;
      dom.contentTip.textContent = categoryTip(cat);
    } else {
      dom.contentTitle.textContent = `HopeKit ${state.version}`;
      dom.contentTip.textContent = '自定义外观与版本信息';
    }
  }

  function categoryTip(cat) {
    const map = {
      tools: '你今天看起来很聪明！',
      calendar: '今天也是充实的一天',
      links: '从这里出发',
    };
    return map[cat] || '';
  }

  // ============================================================
  //  SIDEBAR DRAWER (Spring Animation)
  // ============================================================
  function toggleSidebar() {
    state.sidebarCollapsed = !state.sidebarCollapsed;
    dom.sidebar.dataset.collapsed = String(state.sidebarCollapsed);

    const from = dom.sidebar.offsetWidth;
    const to = state.sidebarCollapsed
      ? parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-collapsed'))
      : parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-width'));

    // 停止之前的弹簧
    if (state._drawerAnim) state._drawerAnim.stop();

    state._drawerAnim = HopeMotion.springDrawer(dom.sidebar, from, to, {
      damping: 0.8,    // sheet 风格，轻微 overshoot
      response: 0.3,
      velocity: 0,
    });
  }

  // ============================================================
  //  BRIDGE ACTIONS
  // ============================================================
  async function openModule(name) {
    try {
      const ok = await HopeBridge.openModule(name);
      if (!ok) showToast('模块暂时无法打开');
    } catch (e) {
      console.error(e);
      showToast('调用失败');
    }
  }

  /**
   * 乐观更新 + 失败回滚：
   * 先立即切换 UI（让用户感知到 0 延迟反馈，符合 Apple Response §1），
   * 再异步通知 Python；若 Python 失败则回滚到之前状态。
   */
  function toggleModule(name, enabled) {
    const p = state.plugins.find((x) => x.name === name);
    if (!p) return;
    const prevEnabled = p.enabled;
    if (prevEnabled === enabled) return;

    // 立即更新本地状态 + UI
    p.enabled = enabled;
    updateCardVisual(name, p);

    // 异步通知 Python，失败回滚
    HopeBridge.toggleModule(name, enabled)
      .then((ok) => {
        if (!ok) {
          p.enabled = prevEnabled;
          updateCardVisual(name, p);
          showToast('无法切换');
        }
      })
      .catch((e) => {
        console.error(e);
        p.enabled = prevEnabled;
        updateCardVisual(name, p);
        showToast('切换失败');
      });
  }

  /** 根据 plugin 状态刷新单张卡片的视觉 */
  function updateCardVisual(name, p) {
    const card = document.querySelector(`.card[data-module="${name}"]`);
    if (!card) return;
    card.dataset.disabled = String(!p.enabled);
    const toggle = card.querySelector('.toggle-switch');
    if (toggle) toggle.setAttribute('aria-checked', String(p.enabled));
    // links 分类的 view-btn 同步 disabled
    const viewBtn = card.querySelector('.view-btn');
    if (viewBtn) viewBtn.dataset.disabled = String(!p.enabled);
  }

  /**
   * 主题风格切换：乐观更新选中态，失败回滚。
   * 调用 bridge 拿到最新 colors，再应用到 CSS 变量。
   */
  async function setThemeStyle(style) {
    if (!state.theme || style === state.theme.style) return;
    const prevStyle = state.theme.style;
    state.theme.style = style;

    // 立即更新选中态视觉
    document.querySelectorAll('.theme-card[data-style]').forEach((c) => {
      c.setAttribute('aria-checked', String(c.dataset.style === style));
    });
    document.documentElement.dataset.themeTransitioning = 'true';

    try {
      const colorsJson = await HopeBridge.setTheme(style, state.theme.mode);
      applyThemeColors(colorsJson);
    } catch (e) {
      console.error(e);
      // 回滚选中态
      state.theme.style = prevStyle;
      document.querySelectorAll('.theme-card[data-style]').forEach((c) => {
        c.setAttribute('aria-checked', String(c.dataset.style === prevStyle));
      });
      showToast('主题切换失败');
    } finally {
      setTimeout(() => {
        delete document.documentElement.dataset.themeTransitioning;
      }, 320);
    }
  }

  /**
   * 主题模式（auto/light/dark）切换：同样乐观更新。
   */
  async function setThemeMode(mode) {
    if (!state.theme || mode === state.theme.mode) return;
    const prevMode = state.theme.mode;
    state.theme.mode = mode;
    const prevIsDark = state.theme.isDark;
    const isDark = (mode === 'dark')
      || (mode === 'auto' && window.matchMedia?.('(prefers-color-scheme: dark)').matches);
    state.theme.isDark = isDark;

    // 立即更新视觉
    document.documentElement.dataset.theme = isDark ? 'dark' : 'light';
    document.querySelectorAll('#themeModeSegmented button').forEach((b) => {
      b.setAttribute('aria-checked', String(b.dataset.mode === mode));
    });
    document.documentElement.dataset.themeTransitioning = 'true';

    try {
      const colorsJson = await HopeBridge.setTheme(state.theme.style, mode);
      applyThemeColors(colorsJson);
    } catch (e) {
      console.error(e);
      // 回滚
      state.theme.mode = prevMode;
      state.theme.isDark = prevIsDark;
      document.documentElement.dataset.theme = prevIsDark ? 'dark' : 'light';
      document.querySelectorAll('#themeModeSegmented button').forEach((b) => {
        b.setAttribute('aria-checked', String(b.dataset.mode === prevMode));
      });
      showToast('模式切换失败');
    } finally {
      setTimeout(() => {
        delete document.documentElement.dataset.themeTransitioning;
      }, 320);
    }
  }

  function applyThemeColors(colorsJson) {
    let colors = {};
    try { colors = JSON.parse(colorsJson); } catch (e) { return; }
    const root = document.documentElement;
    const mapping = {
      primary: '--color-primary', on_primary: '--color-on-primary',
      primary_container: '--color-primary-container',
      on_primary_container: '--color-on-primary-container',
      secondary: '--color-secondary', on_secondary: '--color-on-secondary',
      secondary_container: '--color-secondary-container',
      on_secondary_container: '--color-on-secondary-container',
      surface: '--color-surface', on_surface: '--color-on-surface',
      surface_variant: '--color-surface-variant',
      on_surface_variant: '--color-on-surface-variant',
      background: '--color-background', on_background: '--color-on-background',
      outline: '--color-outline', outline_variant: '--color-outline-variant',
      error: '--color-error', on_error: '--color-on-error',
      sidebar_bg: '--color-sidebar-bg', sidebar_text: '--color-sidebar-text',
      sidebar_hover: '--color-sidebar-hover', sidebar_active: '--color-sidebar-active',
      sidebar_active_text: '--color-sidebar-active-text',
      exit_btn_bg: '--color-exit-btn-bg', exit_btn_hover: '--color-exit-btn-hover',
    };
    Object.entries(mapping).forEach(([k, cssVar]) => {
      if (colors[k]) root.style.setProperty(cssVar, colors[k]);
    });

    // 圆角
    if (colors.card_radius) root.style.setProperty('--radius-card', colors.card_radius);
    if (colors.btn_radius) root.style.setProperty('--radius-control', colors.btn_radius);
    if (colors.nav_radius) root.style.setProperty('--radius-nav', colors.nav_radius);

    // material 透明
    const transparentStyles = ['winui3', 'win10fluent'];
    if (state.theme && transparentStyles.includes(state.theme.style)) {
      document.documentElement.dataset.material = 'transparent';
    } else {
      delete document.documentElement.dataset.material;
    }
  }

  // ============================================================
  //  TOAST
  // ============================================================
  let _toastTimer = null;
  function showToast(msg) {
    let toast = document.querySelector('.toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'toast';
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.dataset.visible = 'true';
    clearTimeout(_toastTimer);
    _toastTimer = setTimeout(() => {
      toast.dataset.visible = 'false';
    }, 1800);
  }

  // ============================================================
  //  EVENTS
  // ============================================================
  function bindEvents() {
    dom.collapseBtn.addEventListener('click', toggleSidebar);
    dom.exitBtn.addEventListener('click', () => HopeBridge.exitApp());

    // 内容滚动检测：用于 content::before 的 fade-in
    const stack = dom.pageStack;
    stack.addEventListener('scroll', () => {
      dom.content.dataset.scrolled = String(stack.scrollTop > 4);
    }, { passive: true });
  }

  // ============================================================
  //  INIT
  // ============================================================
  async function init() {
    cacheDom();

    const initialStateStr = await HopeBridge.getInitialState();
    const initial = JSON.parse(initialStateStr);
    state.version = initial.version || '';
    state.categories = initial.categories || [];
    state.plugins = initial.plugins || [];
    state.theme = initial.theme || null;

    const aboutInfoStr = await HopeBridge.getAboutInfo();
    try {
      state.aboutInfo = JSON.parse(aboutInfoStr);
    } catch (e) {
      console.error('Failed to parse about info:', e);
      state.aboutInfo = null;
    }

    // logo
    if (initial.logoUrl) {
      setLogo(initial.logoUrl);
    } else {
      // 无 logo 时隐藏 img，避免 broken image 图标
      dom.logoImg.style.display = 'none';
    }
    renderAboutInfo();

    // 初始 theme 颜色
    if (state.theme && state.theme.colors) {
      applyThemeColors(JSON.stringify(state.theme.colors));
    }
    if (state.theme) {
      const isDark = state.theme.isDark
        || (state.theme.mode === 'dark')
        || (state.theme.mode === 'auto' && window.matchMedia?.('(prefers-color-scheme: dark)').matches);
      document.documentElement.dataset.theme = isDark ? 'dark' : 'light';
      if (['winui3','win10fluent'].includes(state.theme.style)) {
        document.documentElement.dataset.material = 'transparent';
      }
    }

    renderNav();
    renderPages();
    renderThemeStyleGrid();
    renderThemeModeSegmented();
    bindEvents();

    // 默认进入第一个分类
    if (state.categories.length > 0) {
      switchCategory(state.categories[0]);
    }

    // 监听外部主题变化
    HopeBridge.on('themeChanged', (data) => {
      state.theme = data;
      if (data.colors) applyThemeColors(JSON.stringify(data.colors));
      const isDark = data.isDark
        || (data.mode === 'dark')
        || (data.mode === 'auto' && window.matchMedia?.('(prefers-color-scheme: dark)').matches);
      document.documentElement.dataset.theme = isDark ? 'dark' : 'light';
      renderThemeStyleGrid();
      renderThemeModeSegmented();
    });

    HopeBridge.on('pluginsChanged', (plugins) => {
      state.plugins = plugins;
      renderPages();
      // renderPages 重建了设置页 DOM，主题选中态和关于信息丢失，需要重渲
      renderThemeStyleGrid();
      renderThemeModeSegmented();
      renderAboutInfo();
      // 重新选中当前页
      if (state.currentPage) {
        if (state.currentPage === '__settings') {
          switchSettingsSub(state.settingsSub || 'theme');
        } else {
          showPage(`.page[data-category="${state.currentPage}"]`);
        }
      }
    });
  }

  global.HopeApp = { init, state };
})(window);
