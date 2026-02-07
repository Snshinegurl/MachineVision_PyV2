from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import qtawesome as qta

def create_image_processing_section(app_instance):
    widget = QWidget()
    layout = QHBoxLayout(widget)
    layout.setSpacing(24)
    layout.setContentsMargins(0, 0, 0, 0)
    
    original_card, original_placeholder, original_image_label = create_image_card(
        "Original Image", "file-upload", True, app_instance
    )
    processed_card, processed_placeholder, processed_image_label, processed_status, save_btn = create_image_card(
        "Processed Image", "magic", False, app_instance
    )
    
    layout.addWidget(original_card)
    layout.addWidget(processed_card)
    
    components = (
        original_placeholder, original_image_label,
        processed_placeholder, processed_image_label,
        processed_status, save_btn
    )
    return widget, components

def create_image_card(title, icon, is_original, app_instance):
    widget = QWidget()
    widget.setObjectName("processing-card")
    widget.setMinimumHeight(500)
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    if is_original:
        header = create_card_header(title, icon, is_original, app_instance)
        layout.addWidget(header)
        
        display_area, placeholder, image_label = create_image_display_area(is_original, app_instance)
        layout.addWidget(display_area)
        return widget, placeholder, image_label
    else:
        header, processed_status, save_btn = create_card_header(title, icon, is_original, app_instance)
        layout.addWidget(header)
        
        display_area, placeholder, image_label = create_image_display_area(is_original, app_instance)
        layout.addWidget(display_area)
        return widget, placeholder, image_label, processed_status, save_btn

def create_card_header(title, icon, is_original, app_instance):
    header = QWidget()
    header.setObjectName("card-header")
    header_layout = QHBoxLayout(header)
    header_layout.setContentsMargins(20, 20, 20, 20)
    
    title_widget = create_card_title(title, icon)
    
    if is_original:
        upload_btn = create_upload_button(app_instance)
        header_layout.addWidget(title_widget)
        header_layout.addWidget(upload_btn)
        return header
    else:
        right_widget, processed_status, save_btn = create_processed_header_right(app_instance)
        header_layout.addWidget(title_widget)
        header_layout.addWidget(right_widget)
        return header, processed_status, save_btn

def create_card_title(title, icon):
    title_widget = QWidget()
    title_layout = QHBoxLayout(title_widget)
    title_layout.setContentsMargins(0, 0, 0, 0)
    title_layout.setSpacing(10)
    
    icon_label = QLabel()
    icon_label.setFixedSize(20, 20)
    icon_label.setAlignment(Qt.AlignCenter)
    
    if icon == "file-upload":
        try:
            icon_fa = qta.icon('fa5s.file-upload', color='#4F46E5')
            icon_pixmap = icon_fa.pixmap(16, 16)
            icon_label.setPixmap(icon_pixmap)
        except:
            icon_label.setText("📤")
    else:  # magic
        try:
            icon_fa = qta.icon('fa5s.magic', color='#4F46E5')
            icon_pixmap = icon_fa.pixmap(16, 16)
            icon_label.setPixmap(icon_pixmap)
        except:
            icon_label.setText("✨")
    
    title_label = QLabel(title)
    title_label.setObjectName("card-title")
    
    title_layout.addWidget(icon_label)
    title_layout.addWidget(title_label)
    title_layout.addStretch()
    
    return title_widget

def create_upload_button(app_instance):
    upload_btn = QPushButton(" Upload Image")
    upload_btn.setObjectName("upload-btn")
    upload_btn.setCursor(Qt.PointingHandCursor)
    
    try:
        upload_icon = qta.icon('fa5s.upload', color='white')
        upload_btn.setIcon(upload_icon)
        upload_btn.setIconSize(QSize(16, 16))
    except:
        upload_btn.setText("📤 Upload Image")
        
    upload_btn.clicked.connect(app_instance.upload_image)
    return upload_btn

def create_processed_header_right(app_instance):
    right_widget = QWidget()
    right_layout = QHBoxLayout(right_widget)
    right_layout.setContentsMargins(0, 0, 0, 0)
    right_layout.setSpacing(12)
    
    processed_status = QLabel("Waiting")
    processed_status.setObjectName("status-badge-pending")
    
    save_btn = QPushButton(" Save")
    save_btn.setObjectName("save-btn")
    save_btn.setCursor(Qt.PointingHandCursor)
    save_btn.setEnabled(False)
    
    try:
        save_icon = qta.icon('fa5s.save', color='white')
        save_btn.setIcon(save_icon)
        save_btn.setIconSize(QSize(14, 14))
    except:
        save_btn.setText("💾 Save")
        
    save_btn.clicked.connect(app_instance.save_processed_image)
    
    right_layout.addWidget(processed_status)
    right_layout.addWidget(save_btn)
    
    return right_widget, processed_status, save_btn

def create_image_display_area(is_original, app_instance):
    display_area = QWidget()
    display_area.setObjectName("image-display-area")
    display_area.setMinimumHeight(400)
    display_layout = QVBoxLayout(display_area)
    display_layout.setContentsMargins(30, 30, 30, 30)
    display_layout.setAlignment(Qt.AlignCenter)
    
    if is_original:
        placeholder = create_image_placeholder("Upload Original Image", "Drag & drop or click to browse", "cloud-upload-alt")
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.hide()
        
        display_layout.addWidget(placeholder)
        display_layout.addWidget(image_label)
        return display_area, placeholder, image_label
    else:
        placeholder = create_image_placeholder("Processing Image", "Will appear here after processing", "cogs")
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.hide()
        
        display_layout.addWidget(placeholder)
        display_layout.addWidget(image_label)
        return display_area, placeholder, image_label

def create_image_placeholder(text, subtext, icon):
    widget = QWidget()
    widget.setObjectName("image-placeholder")
    widget.setMinimumHeight(300)
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignCenter)
    layout.setSpacing(20)
    
    icon_label = QLabel()
    icon_label.setObjectName("placeholder-icon")
    icon_label.setAlignment(Qt.AlignCenter)
    icon_label.setFixedSize(64, 64)
    
    icon_map = {
        'cloud-upload-alt': 'fa5s.cloud-upload-alt',
        'cogs': 'fa5s.cogs'
    }
    
    if icon in icon_map:
        try:
            icon_fa = qta.icon(icon_map[icon], color='#9CA3AF')
            icon_pixmap = icon_fa.pixmap(48, 48)
            icon_label.setPixmap(icon_pixmap)
        except:
            icon_label.setText("📁")
    else:
        icon_label.setText("📁")
    
    text_label = QLabel(text)
    text_label.setObjectName("placeholder-text")
    text_label.setAlignment(Qt.AlignCenter)
    
    subtext_label = QLabel(subtext)
    subtext_label.setObjectName("placeholder-subtext")
    subtext_label.setAlignment(Qt.AlignCenter)
    
    layout.addWidget(icon_label)
    layout.addWidget(text_label)
    layout.addWidget(subtext_label)
    
    return widget