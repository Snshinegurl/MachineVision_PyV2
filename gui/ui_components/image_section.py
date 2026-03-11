from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import qtawesome as qta

def create_image_processing_section(app_instance):
    widget = QWidget()
    layout = QHBoxLayout(widget)
    layout.setSpacing(24)
    layout.setContentsMargins(0, 0, 0, 0)

    original_card, original_placeholder, original_image_label, crop_btn, threshold_widget = create_image_card(
        "Original Image", "file-upload", True, app_instance
    )
    processed_card, processed_placeholder, processed_image_label, processed_status, save_btn, process_btn = create_image_card(
        "Processed Image", "magic", False, app_instance
    )

    layout.addWidget(original_card)
    layout.addWidget(processed_card)

    components = (
        original_placeholder, original_image_label,
        processed_placeholder, processed_image_label,
        processed_status, save_btn, crop_btn, process_btn, threshold_widget
    )
    return widget, components

def create_image_card(title, icon, is_original, app_instance):
    widget = QWidget()
    widget.setObjectName("processing-card")
    widget.setMinimumHeight(500)
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)

    if is_original:
        header, crop_btn, threshold_widget = create_card_header(title, icon, is_original, app_instance)
        layout.addWidget(header)

        display_area, placeholder, image_label = create_image_display_area(is_original, app_instance)
        layout.addWidget(display_area)
        return widget, placeholder, image_label, crop_btn, threshold_widget
    else:
        header, processed_status, save_btn, process_btn = create_card_header(title, icon, is_original, app_instance)
        layout.addWidget(header)

        display_area, placeholder, image_label = create_image_display_area(is_original, app_instance)
        layout.addWidget(display_area)
        return widget, placeholder, image_label, processed_status, save_btn, process_btn

def create_card_header(title, icon, is_original, app_instance):
    header = QWidget()
    header.setObjectName("card-header")
    header_layout = QVBoxLayout(header)   # Changed to vertical to accommodate threshold slider below
    header_layout.setContentsMargins(20, 20, 20, 10)
    header_layout.setSpacing(8)

    # Top row: title and buttons
    top_row = QWidget()
    top_layout = QHBoxLayout(top_row)
    top_layout.setContentsMargins(0, 0, 0, 0)

    title_widget = create_card_title(title, icon)
    top_layout.addWidget(title_widget)
    top_layout.addStretch()

    if is_original:
        crop_btn = create_crop_button(app_instance)
        upload_btn = create_upload_button(app_instance)
        top_layout.addWidget(crop_btn)
        top_layout.addWidget(upload_btn)

        # Threshold slider (initially hidden)
        threshold_widget = create_threshold_widget(app_instance)
        threshold_widget.setVisible(False)  # Hidden by default
        app_instance.bw_threshold_widget = threshold_widget  # Store reference

        header_layout.addWidget(top_row)
        header_layout.addWidget(threshold_widget)

        return header, crop_btn, threshold_widget
    else:
        right_widget, processed_status, save_btn, process_btn = create_processed_header_right(app_instance)
        top_layout.addWidget(right_widget)

        header_layout.addWidget(top_row)
        return header, processed_status, save_btn, process_btn

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

def create_crop_button(app_instance):
    crop_btn = QPushButton(" Crop")
    crop_btn.setObjectName("crop-btn")
    crop_btn.setCursor(Qt.PointingHandCursor)
    crop_btn.clicked.connect(app_instance.start_cropping)
    crop_btn.setEnabled(False)

    try:
        crop_icon = qta.icon('fa5s.crop', color='white')
        crop_btn.setIcon(crop_icon)
        crop_btn.setIconSize(QSize(14, 14))
    except:
        crop_btn.setText("✂️ Crop")

    return crop_btn

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
    right_layout.setSpacing(8)

    # Status badge with fixed size (like a button)
    processed_status = QLabel("Waiting")
    processed_status.setObjectName("status-badge-pending")
    processed_status.setFixedSize(70, 28)
    processed_status.setAlignment(Qt.AlignCenter)

    process_btn = QPushButton(" Process")
    process_btn.setObjectName("process-btn")
    process_btn.setCursor(Qt.PointingHandCursor)
    process_btn.setEnabled(False)
    try:
        bolt_icon = qta.icon('fa5s.bolt', color='white')
        process_btn.setIcon(bolt_icon)
        process_btn.setIconSize(QSize(14, 14))
    except:
        process_btn.setText("⚡ Process")
    process_btn.clicked.connect(app_instance.process_image)

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
    right_layout.addWidget(process_btn)
    right_layout.addWidget(save_btn)

    return right_widget, processed_status, save_btn, process_btn

def create_threshold_widget(app_instance):
    """Create the threshold slider for Black & White filter."""
    widget = QWidget()
    widget.setObjectName("threshold-widget")
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 8, 0, 0)
    layout.setSpacing(8)

    threshold_header = QWidget()
    threshold_header_layout = QHBoxLayout(threshold_header)
    threshold_header_layout.setContentsMargins(0, 0, 0, 0)

    threshold_label = QLabel("Threshold:")
    threshold_label.setObjectName("threshold-label")

    threshold_value_label = QLabel("128")
    threshold_value_label.setObjectName("threshold-value-label")

    threshold_header_layout.addWidget(threshold_label)
    threshold_header_layout.addStretch()
    threshold_header_layout.addWidget(threshold_value_label)

    threshold_slider = QSlider(Qt.Horizontal)
    threshold_slider.setObjectName("threshold-slider")
    threshold_slider.setMinimum(0)
    threshold_slider.setMaximum(255)
    threshold_slider.setValue(128)
    threshold_slider.setSingleStep(1)
    threshold_slider.setPageStep(10)
    threshold_slider.valueChanged.connect(app_instance.on_threshold_changed)

    layout.addWidget(threshold_header)
    layout.addWidget(threshold_slider)

    # Store references in the main app instance for later access
    app_instance.bw_threshold_slider = threshold_slider
    app_instance.bw_threshold_value_label = threshold_value_label

    return widget

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