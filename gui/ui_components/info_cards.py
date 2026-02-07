from PySide6.QtWidgets import *
from PySide6.QtCore import *
import qtawesome as qta

def create_file_info_cards():
    widget = QWidget()
    layout = QGridLayout(widget)
    layout.setSpacing(16)
    layout.setContentsMargins(0, 0, 0, 0)
    
    file_name_card = create_info_card("File Name", "No file", "blue", "file")
    file_size_card = create_info_card("File Size", "-", "green", "weight-hanging")
    dimensions_card = create_info_card("Dimensions", "-", "purple", "expand-alt")
    pixels_card = create_info_card("Total Pixels", "-", "orange", "th-large")
    format_card = create_info_card("Format", "-", "red", "file-image")
    
    layout.addWidget(file_name_card, 0, 0)
    layout.addWidget(file_size_card, 0, 1)
    layout.addWidget(dimensions_card, 0, 2)
    layout.addWidget(pixels_card, 0, 3)
    layout.addWidget(format_card, 0, 4)
    
    cards = (file_name_card, file_size_card, dimensions_card, pixels_card, format_card)
    return widget, cards

def create_info_card(label, value, color, icon_name):
    widget = QWidget()
    widget.setObjectName("info-card")
    widget.setMinimumHeight(120)
    widget.setCursor(Qt.PointingHandCursor)
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(12)
    
    icon_label = QLabel()
    icon_label.setObjectName(f"card-icon-{color}")
    icon_label.setFixedSize(40, 40)
    icon_label.setAlignment(Qt.AlignCenter)
    
    icon_map = {
        'file': 'fa5s.file',
        'weight-hanging': 'fa5s.weight-hanging',
        'expand-alt': 'fa5s.expand-alt',
        'th-large': 'fa5s.th-large',
        'file-image': 'fa5s.file-image'
    }
    
    if icon_name in icon_map:
        icon_color = get_color_for_icon(color)
        try:
            icon = qta.icon(icon_map[icon_name], color=icon_color)
            icon_pixmap = icon.pixmap(24, 24)
            icon_label.setPixmap(icon_pixmap)
        except Exception as e:
            icon_label.setText("📄")
    else:
        icon_label.setText("📄")
    
    label_widget = QLabel(label)
    label_widget.setObjectName("card-label")
    
    value_widget = QLabel(value)
    value_widget.setObjectName("card-value")
    value_widget.setWordWrap(True)
    
    layout.addWidget(icon_label)
    layout.addWidget(label_widget)
    layout.addWidget(value_widget)
    layout.addStretch()
    
    return widget

def get_color_for_icon(color):
    colors = {
        'blue': '#4F46E5',
        'green': '#10B981',
        'purple': '#A855F7',
        'orange': '#F59E0B',
        'red': '#EF4444'
    }
    return colors.get(color, '#4F46E5')

def update_info_cards(image_info, file_name_card, file_size_card, dimensions_card, pixels_card, format_card):
    file_name = image_info['name']
    if len(file_name) > 10:
        file_name = file_name[:7] + '...' + file_name.split('.')[-1]
    file_name_card.findChild(QLabel, "card-value").setText(file_name)
    
    file_size_kb = image_info['file_size'] / 1024
    file_size_card.findChild(QLabel, "card-value").setText(f"{file_size_kb:.1f} KB")
    
    dimensions = f"{image_info['width']} × {image_info['height']}"
    dimensions_card.findChild(QLabel, "card-value").setText(dimensions)
    
    pixels = image_info['total_pixels']
    pixels_card.findChild(QLabel, "card-value").setText(f"{pixels:,}")
    
    format_name = image_info['format'] if image_info['format'] else "Unknown"
    format_card.findChild(QLabel, "card-value").setText(format_name)