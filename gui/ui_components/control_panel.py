from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import qtawesome as qta

def create_control_panel(app_instance):
    widget = QWidget()
    widget.setObjectName("control-panel")
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(16)

    header = create_panel_header()
    layout.addWidget(header)

    # Stacked widget for filter‑specific descriptions (no controls now)
    stacked_widget = QStackedWidget()
    stacked_widget.setObjectName("filter-stack")



    layout.addWidget(stacked_widget)

    # Store reference to stacked widget
    app_instance.filter_stack = stacked_widget

    # Return only the stacked widget (no threshold controls here)
    return widget, (stacked_widget,)

def create_panel_header():
    header = QWidget()
    header_layout = QVBoxLayout(header)
    header_layout.setContentsMargins(0, 0, 0, 0)
    header_layout.setSpacing(8)

    title = QLabel("Processing Controls")
    title.setObjectName("panel-title")

    subtitle = QLabel("Select a filter tab above to see its description")
    subtitle.setObjectName("panel-subtitle")

    header_layout.addWidget(title)
    header_layout.addWidget(subtitle)

    return header