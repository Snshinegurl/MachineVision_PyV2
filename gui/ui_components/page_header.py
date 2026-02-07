from PySide6.QtWidgets import *

def create_page_header():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    
    title = QLabel("Image Processing Dashboard")
    title.setObjectName("page-title")
    title.setWordWrap(True)
    
    subtitle = QLabel("Upload images and apply various filters including custom grayscale conversion")
    subtitle.setObjectName("page-subtitle")
    subtitle.setWordWrap(True)
    
    layout.addWidget(title)
    layout.addWidget(subtitle)
    
    return widget