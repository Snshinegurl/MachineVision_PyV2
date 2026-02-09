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
    
    content_container, components = create_panel_content(app_instance)
    layout.addWidget(content_container)
    
    return widget, components

def create_panel_header():
    header = QWidget()
    header_layout = QVBoxLayout(header)
    header_layout.setContentsMargins(0, 0, 0, 0)
    header_layout.setSpacing(8)
    
    title = QLabel("Processing Controls") 
    title.setObjectName("panel-title")
    
    subtitle = QLabel("Select filters and adjust parameters for image processing")
    subtitle.setObjectName("panel-subtitle")
    
    header_layout.addWidget(title)
    header_layout.addWidget(subtitle)
    
    return header

def create_panel_content(app_instance):
    content_container = QWidget()
    content_layout = QVBoxLayout(content_container)
    content_layout.setSpacing(20)
    content_layout.setContentsMargins(0, 0, 0, 0)
    
    main_horizontal = QHBoxLayout()
    main_horizontal.setSpacing(24)
    main_horizontal.setContentsMargins(0, 0, 0, 0)
    
    filters_widget, filter_group, threshold_widget, threshold_value_label, threshold_slider, bw_radio = create_filters_section(app_instance)
    main_horizontal.addWidget(filters_widget, 6)
    
    process_section, process_btn = create_process_section(app_instance)
    main_horizontal.addWidget(process_section, 4)
    
    content_layout.addLayout(main_horizontal)
    
    components = (filter_group, threshold_widget, threshold_value_label, threshold_slider, process_btn, bw_radio)
    return content_container, components

def create_filters_section(app_instance):
    filters_widget = QWidget()
    filters_layout = QVBoxLayout(filters_widget)
    filters_layout.setContentsMargins(0, 0, 0, 0)
    filters_layout.setSpacing(16)
    
    filter_grid, filter_group, threshold_widget, threshold_value_label, threshold_slider, bw_radio = create_filter_grid(app_instance)
    filters_layout.addWidget(filter_grid)
    filters_layout.addStretch()
    
    return filters_widget, filter_group, threshold_widget, threshold_value_label, threshold_slider, bw_radio

def create_filter_grid(app_instance):
    widget = QWidget()
    layout = QGridLayout(widget)
    layout.setHorizontalSpacing(20)
    layout.setVerticalSpacing(16)
    layout.setContentsMargins(0, 0, 0, 0)
    
    filter_group = QButtonGroup()
    filters = [
        ("Grayscale", "custom_grayscale", "moon", "Manual grayscale conversion using luminosity method", None),
        ("Black & White", "custom_bw", "adjust", "Using the grayscale conversion and then applying a threshold to create a binary black and white image", create_threshold_widget(app_instance)),
        ("Background Removal", "background_removal", "eraser", "Remove image background using color detection algorithm. Creates transparent background.", None),
    ]
    
    threshold_widget = None
    threshold_value_label = None
    threshold_slider = None
    bw_radio = None
    
    for i, (name, value, icon, description, twidget) in enumerate(filters):
        row = i // 2
        col = i % 2
        
        filter_widget, radio = create_filter_option(name, value, icon, description, twidget, app_instance)
        layout.addWidget(filter_widget, row, col)
        filter_group.addButton(radio)
        
        if value == "custom_bw":
            threshold_widget = twidget
            threshold_value_label = app_instance.threshold_value_label
            threshold_slider = app_instance.threshold_slider
            bw_radio = radio
    
    if filter_group.buttons():
        filter_group.buttons()[0].setChecked(True)
    
    return widget, filter_group, threshold_widget, threshold_value_label, threshold_slider, bw_radio

def create_filter_option(name, value, icon, description, threshold_widget, app_instance):
    widget = QWidget()
    widget.setObjectName("filter-option")
    widget.setMinimumHeight(200)
    widget.setMinimumWidth(280)
    widget.setCursor(Qt.PointingHandCursor)
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    
    container = QWidget()
    container_layout = QVBoxLayout(container)
    container_layout.setContentsMargins(0, 0, 0, 0)
    container_layout.setSpacing(0)
    
    radio = QRadioButton()
    radio.setObjectName(f"filter-{value}")
    radio.setText("")
    radio.setCursor(Qt.PointingHandCursor)
    radio.toggled.connect(lambda checked, val=value: app_instance.on_filter_changed(val, checked))
    
    label = create_filter_label(name, icon, description, threshold_widget)
    container_layout.addWidget(radio)
    container_layout.addWidget(label)
    
    layout.addWidget(container)
    
    label.mousePressEvent = lambda e, rb=radio: rb.setChecked(True)
    
    return widget, radio

def create_filter_label(name, icon, description, threshold_widget):
    label = QLabel()
    label.setObjectName("filter-label")
    label_layout = QVBoxLayout(label)
    label_layout.setContentsMargins(20, 20, 20, 20)
    label_layout.setSpacing(16)
    
    top_widget = create_filter_top_row(name, icon)
    label_layout.addWidget(top_widget)
    
    desc_label = QLabel(description)
    desc_label.setObjectName("filter-description")
    desc_label.setWordWrap(True)
    desc_label.setMinimumHeight(60)
    desc_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
    label_layout.addWidget(desc_label)
    
    if threshold_widget:
        threshold_widget.setVisible(False)
        label_layout.addWidget(threshold_widget)
    
    return label

def create_filter_top_row(name, icon):
    top_widget = QWidget()
    top_layout = QHBoxLayout(top_widget)
    top_layout.setContentsMargins(0, 0, 0, 0)
    top_layout.setSpacing(12)
    
    icon_widget = QLabel()
    icon_widget.setObjectName("filter-icon")
    icon_widget.setFixedSize(44, 44)
    icon_widget.setAlignment(Qt.AlignCenter)
    
    icon_map = {
        'moon': 'fa5s.moon',
        'adjust': 'fa5s.adjust',
        'eraser': 'fa5s.eraser'
    }
    
    if icon in icon_map:
        try:
            icon_fa = qta.icon(icon_map[icon], color='#4F46E5')
            icon_pixmap = icon_fa.pixmap(24, 24)
            icon_widget.setPixmap(icon_pixmap)
        except:
            icon_widget.setText("⚫")
    else:
        icon_widget.setText("⚫")
    
    name_label = QLabel(name)
    name_label.setObjectName("filter-name")
    
    top_layout.addWidget(icon_widget)
    top_layout.addWidget(name_label)
    top_layout.addStretch()
    
    return top_widget

def create_threshold_widget(app_instance):
    widget = QWidget()
    widget.setObjectName("threshold-widget")
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 12, 0, 0)
    layout.setSpacing(12)
    
    threshold_header = QWidget()
    threshold_header_layout = QHBoxLayout(threshold_header)
    threshold_header_layout.setContentsMargins(0, 0, 0, 0)
    
    threshold_label = QLabel("Threshold:")
    threshold_label.setObjectName("threshold-label")
    
    threshold_value_label = QLabel("128")
    threshold_value_label.setObjectName("threshold-value-label")
    
    app_instance.threshold_value_label = threshold_value_label
    
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
    
    app_instance.threshold_slider = threshold_slider
    
    threshold_explanation = QLabel("Lower = more black, Higher = more white")
    threshold_explanation.setObjectName("threshold-explanation")
    threshold_explanation.setWordWrap(True)
    threshold_explanation.setAlignment(Qt.AlignCenter)
    
    layout.addWidget(threshold_header)
    layout.addWidget(threshold_slider)
    layout.addWidget(threshold_explanation)
    
    return widget

def create_process_section(app_instance):
    widget = QWidget()
    widget.setObjectName("process-section")
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    
    centered_container = QWidget()
    centered_container.setObjectName("centered-container")
    centered_layout = QVBoxLayout(centered_container)
    centered_layout.setContentsMargins(20, 20, 20, 20)
    centered_layout.setSpacing(20)
    centered_layout.setAlignment(Qt.AlignCenter)
    
    centered_layout.addStretch(1)
    
    process_btn = create_process_button(app_instance)
    centered_layout.addWidget(process_btn, 0, Qt.AlignHCenter)
    
    description = create_process_description()
    centered_layout.addWidget(description, 0, Qt.AlignHCenter)
    
    centered_layout.addStretch(1)
    
    layout.addWidget(centered_container)
    
    return widget, process_btn

def create_process_button(app_instance):
    process_btn = QPushButton(" Process Image")
    process_btn.setObjectName("process-btn")
    process_btn.setCursor(Qt.PointingHandCursor)
    process_btn.clicked.connect(app_instance.process_image)
    process_btn.setEnabled(False)
    process_btn.setMinimumHeight(65)
    process_btn.setMinimumWidth(220)
    
    try:
        bolt_icon = qta.icon('fa5s.bolt', color='white')
        process_btn.setIcon(bolt_icon)
        process_btn.setIconSize(QSize(24, 24))
    except:
        process_btn.setText("⚡ Process Image")
    
    return process_btn

def create_process_description():
    description = QLabel("Select a filter above and click to apply it to your image. The processed result will appear in the right panel.")
    description.setObjectName("button-description")
    description.setWordWrap(True)
    description.setAlignment(Qt.AlignCenter)
    description.setMinimumWidth(250)
    description.setMaximumWidth(300)
    
    return description