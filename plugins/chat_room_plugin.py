from hopekit.registry import ModuleRegistry
from hopekit.qt_compat import QMainWindow


@ModuleRegistry.register("chat_room", icon="💬", title="聊天室", category="tools")
def chat_room_factory(main_window):
    from examples.chat_room.chat_room import MainWin
    return MainWin()


@ModuleRegistry.register("ai_bot", icon="🤖", title="AI机器人（余额用尽）", category="tools", enabled=False)
def ai_bot_factory(main_window):
    return QMainWindow()


@ModuleRegistry.register("ticket", icon="🎫", title="查火车票（暂未开放）", category="tools", enabled=False)
def ticket_factory(main_window):
    return QMainWindow()


@ModuleRegistry.register("tool_ex", icon="🧰", title="牛逼の外部工具", category="tools", enabled=False)
def tool_ex_factory(main_window):
    return QMainWindow()
