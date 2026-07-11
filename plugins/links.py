from hopekit.registry import ModuleRegistry
from hopekit.qt_compat import QDesktopServices, QUrl


def _open_url(url: str):
    QDesktopServices.openUrl(QUrl(url))


@ModuleRegistry.register("website", icon="🌐", title="我们的网站", category="links")
def website_factory(main_window):
    _open_url("https://hopestudio.top/")
    return None


@ModuleRegistry.register("copyright_link", icon="©", title="版权声明", category="links")
def copyright_link_factory(main_window):
    from plugins.copyright import copyright_factory
    return copyright_factory(main_window)


@ModuleRegistry.register("qq_group", icon="🐧", title="加入QQ交流群", category="links")
def qq_group_factory(main_window):
    _open_url(
        "http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=ZWK9Hjr85usU530C3rt0X_3a3ELG0o9e"
        "&authKey=g5Q5ELTce3ChemOo76dqWRxgCbJOHRJ6cRWiEJGFL95vR+JE4tyB2yqgTj5V22xf"
        "&noverify=0&group_code=876244203"
    )
    return None


@ModuleRegistry.register("sports", icon="🏅", title="在线看亚运", category="links")
def sports_factory(main_window):
    _open_url("https://sports.cctv.com/")
    return None


@ModuleRegistry.register("bilibili", icon="📺", title="哔哩哔哩", category="links")
def bilibili_factory(main_window):
    _open_url("https://space.bilibili.com/1711131229")
    return None


@ModuleRegistry.register("blog", icon="📝", title="博客", category="links")
def blog_factory(main_window):
    _open_url("https://blog.nanoturtle.cn")
    return None


@ModuleRegistry.register("github", icon="🐙", title="GitHub", category="links")
def github_factory(main_window):
    _open_url("https://github.com/NanoTurtle1145")
    return None
