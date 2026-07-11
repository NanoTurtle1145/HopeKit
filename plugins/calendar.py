from hopekit.registry import ModuleRegistry
from hopekit.qt_compat import QWidget, QVBoxLayout, QCalendarWidget, QGroupBox


@ModuleRegistry.register("calendar", icon="📅", title="日历", category="calendar", kind="page")
def calendar_factory(main_window):
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setSpacing(12)

    cal_box = QGroupBox("日历")
    cal_layout = QVBoxLayout(cal_box)
    cal_layout.addWidget(QCalendarWidget())
    layout.addWidget(cal_box)
    layout.addStretch(1)
    return page
