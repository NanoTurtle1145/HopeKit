from hopekit.registry import ModuleRegistry
from hopekit.qt_compat import QDialog, QLineEdit, QPushButton, QGridLayout


@ModuleRegistry.register("calculator", icon="🔢", title="简易计算器", category="tools")
def calculator_factory(main_window):
    dlg = QDialog()
    dlg.setWindowTitle("计算器")

    input_line = QLineEdit()
    result_line = QLineEdit()
    result_line.setReadOnly(True)

    buttons = [
        ['7', '8', '9', '/'],
        ['4', '5', '6', '*'],
        ['1', '2', '3', '-'],
        ['0', '.', '=', '+'],
        ['C'],
    ]

    layout = QGridLayout(dlg)
    layout.addWidget(input_line, 0, 0, 1, 4)
    layout.addWidget(result_line, 1, 0, 1, 4)

    def on_click(label):
        if label == "=":
            try:
                result = eval(input_line.text())
                result_line.setText(str(result))
            except Exception:
                result_line.setText("Error")
        elif label == "C":
            input_line.clear()
            result_line.clear()
        else:
            input_line.insert(label)

    for row_idx, button_row in enumerate(buttons, start=2):
        for col_idx, label in enumerate(button_row):
            btn = QPushButton(label)
            btn.clicked.connect(lambda _=False, l=label: on_click(l))
            layout.addWidget(btn, row_idx, col_idx)

    return dlg
