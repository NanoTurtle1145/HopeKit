from hopekit.registry import ModuleRegistry
from hopekit.qt_compat import QMainWindow, QTextEdit, QPushButton


@ModuleRegistry.register("copyright", icon="©", title="版权声明", category="tools")
def copyright_factory(main_window):
    win = QMainWindow()
    win.setWindowTitle('版权声明')
    text_edit = QTextEdit(win)
    text_edit.setPlainText(
        "版权声明\n"
        "感谢您对希望工作室的关注和支持。在使用我们的产品、服务和内容之前，"
        "请务必仔细阅读并理解本版权声明。\n\n"
        "1. 版权所有：除非另有明确说明，希望工作室拥有所有产品、服务和内容"
        "（包括但不限于文字、图像、音频、视频、软件、标志、商标等）的版权。\n\n"
        "2. 保护知识产权：未经希望工作室明确授权，禁止任何人使用、复制、修改、"
        "发布、传播、展示或运用希望工作室的知识产权内容。\n\n"
        "3. 授权使用：若您希望使用希望工作室的产品、服务或内容，"
        "请您与我们联系，获取书面授权。\n\n"
        "4. 用户提交内容：对于您在产品、服务或平台上提交的内容，"
        "您同意授予希望工作室非独占的、永久的、全球范围内的、免费的使用权许可。\n\n"
        "5. 第三方内容和链接：对于这些内容和链接，希望工作室不能保证"
        "其准确性、合法性、安全性或完整性。\n\n"
        "6. 免责声明：在法律允许的范围内，希望工作室不对因使用其产品、服务和内容"
        "而导致的任何直接或间接损失承担责任。\n\n"
        "7. 法律适用和争议解决：本版权声明受中华人民共和国法律的约束。\n\n"
        "本版权声明的解释权归希望工作室所有。\n\n"
        "希望工作室 版权所有"
    )
    text_edit.setReadOnly(True)
    win.setCentralWidget(text_edit)

    button = QPushButton('关闭', win)
    button.move(375, 465)
    button.clicked.connect(win.close)
    win.setFixedSize(500, 500)
    return win
