from hopekit.registry import ModuleRegistry
from hopekit.qt_compat import QMainWindow, QTextEdit, QPushButton


@ModuleRegistry.register("caidan", icon="🥚", title="彩蛋", category="tools")
def caidan_factory(main_window):
    win = QMainWindow()
    win.setWindowTitle('彩蛋')
    text_edit = QTextEdit(win)
    text_edit.setPlainText(
        '只要功夫深，bug如井喷。\n'
        '一测三千年，测完成荒坟。\n'
        '熟识与非门，交谈非真人。\n'
        '谁解其中味，颈雄已沉沉!\n'
        '    ——致敬程序开发者\n'
        '    ——GXBF(NanoTurtle1145)\n'
        '    ——shengrui11(BusySheng)'
    )
    text_edit.setReadOnly(True)
    win.setCentralWidget(text_edit)

    button = QPushButton('关闭', win)
    button.move(100, 220)
    button.clicked.connect(win.close)
    win.setFixedSize(200, 250)
    return win
