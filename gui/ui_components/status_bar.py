from PySide6.QtWidgets import *

def create_status_bar():
    widget = QWidget()
    widget.setObjectName("status-bar")
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(24, 16, 24, 16)
    
    status_widget = QWidget()
    status_layout = QVBoxLayout(status_widget)
    status_layout.setContentsMargins(0, 0, 0, 0)
    status_layout.setSpacing(4)
    
    status_label = QLabel("Current Status")
    status_label.setObjectName("status-label")
    
    status_value = QLabel("Ready for Upload")
    status_value.setObjectName("status-value-ready")
    
    status_layout.addWidget(status_label)
    status_layout.addWidget(status_value)
    
    layout.addWidget(status_widget)
    layout.addStretch()
    
    return widget, status_value