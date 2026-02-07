import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import io
import qtawesome as qta

# Import our custom modules
# Go up one level from gui to project root, then to modules/utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.image_processor import ImageProcessor
from modules.grayscale_converter import GrayscaleConverter
from modules.black_white_converter import BlackWhiteConverter

class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.processed_image = None
        self.image_processor = ImageProcessor()
        self.grayscale_converter = GrayscaleConverter()
        self.black_white_converter = BlackWhiteConverter()
        self.current_filter = "custom_grayscale"
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        self.setWindowTitle("VisionPro AI - Image Processing Dashboard")
        self.setMinimumSize(1400, 900)
        
        # Create central widget with scroll area
        central_widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Style the scrollbar
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #111827;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #1F2937;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #4F46E5;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #4338CA;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QLabel {
            padding: 2px 4px;
            border-radius: 5px;
            }                      
        """)
        
        self.setCentralWidget(scroll_area)
        
        # Main layout for central widget
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header (fixed at top)
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Main content area (scrollable)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)
        
        # Page header
        page_header = self.create_page_header()
        content_layout.addWidget(page_header)
        
        # Status bar
        status_bar = self.create_status_bar()
        content_layout.addWidget(status_bar)
        
        # File info cards
        file_info_cards = self.create_file_info_cards()
        content_layout.addWidget(file_info_cards)
        
        # Image processing section
        image_section = self.create_image_processing_section()
        content_layout.addWidget(image_section)
        
        # Control panel
        control_panel = self.create_control_panel()
        content_layout.addWidget(control_panel)
        
        # Add stretch to push everything up
        content_layout.addStretch()
        
        main_layout.addWidget(content_widget)
        
    def create_header(self):
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(70)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 4, 24, 4)
        
        # Left side: Logo and navigation
        left_widget = QWidget()
        left_layout = QHBoxLayout(left_widget)
        left_layout.setSpacing(40)
        
        # Logo with eye icon
        logo_widget = QWidget()
        logo_layout = QHBoxLayout(logo_widget)
        logo_layout.setSpacing(12)
        
        logo_icon = QLabel()
        logo_icon.setFixedSize(36, 36)
        logo_icon.setObjectName("logo-icon")
        logo_icon.setAlignment(Qt.AlignCenter)
        
        # Create eye icon using qtawesome - FIXED: use fa5.eye instead of fa.eye
        try:
            eye_icon = qta.icon('fa5s.eye', color='white')
            eye_pixmap = eye_icon.pixmap(24, 24)
            logo_icon.setPixmap(eye_pixmap)
        except:
            # Fallback if icon fails
            logo_icon.setText("👁️")
        
        logo_text = QLabel("VisionPro AI")
        logo_text.setObjectName("logo-text")
        
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        left_layout.addWidget(logo_widget)
        
        # Navigation menu
        nav_menu = QWidget()
        nav_layout = QHBoxLayout(nav_menu)
        nav_layout.setSpacing(8)
        
        dashboard_btn = QPushButton("Dashboard")
        dashboard_btn.setObjectName("nav-item-active")
        dashboard_btn.setCursor(Qt.PointingHandCursor)
        nav_layout.addWidget(dashboard_btn)
        
        left_layout.addWidget(nav_menu)
        left_layout.addStretch()
        
        # Right side: User profile
        right_widget = QWidget()
        right_layout = QHBoxLayout(right_widget)
        right_layout.setSpacing(16)
        
        user_profile = QWidget()
        user_profile.setObjectName("user-profile")
        user_profile.setCursor(Qt.PointingHandCursor)
        user_layout = QHBoxLayout(user_profile)
        user_layout.setSpacing(12)
        user_layout.setContentsMargins(8, 8, 8, 8)
        
        user_avatar = QLabel("AI")
        user_avatar.setObjectName("user-avatar")
        user_avatar.setAlignment(Qt.AlignCenter)
        user_avatar.setFixedSize(32, 32)
        
        user_info = QWidget()
        user_info_layout = QVBoxLayout(user_info)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setSpacing(2)
        
        user_name = QLabel("Image Processor")
        user_name.setObjectName("user-name")
        
        user_role = QLabel("AI Assistant")
        user_role.setObjectName("user-role")
        
        user_info_layout.addWidget(user_name)
        user_info_layout.addWidget(user_role)
        
        user_layout.addWidget(user_avatar)
        user_layout.addWidget(user_info)
        right_layout.addWidget(user_profile)
        
        layout.addWidget(left_widget)
        layout.addStretch()
        layout.addWidget(right_widget)
        
        return header
    
    def create_page_header(self):
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
    
    def create_status_bar(self):
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
        
        self.status_value = QLabel("Ready for Upload")
        self.status_value.setObjectName("status-value-ready")
        
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_value)
        
        layout.addWidget(status_widget)
        layout.addStretch()
        
        return widget
    
    def create_file_info_cards(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # File name card
        self.file_name_card = self.create_info_card("File Name", "No file", "blue", "file")
        layout.addWidget(self.file_name_card, 0, 0)
        
        # File size card
        self.file_size_card = self.create_info_card("File Size", "-", "green", "weight-hanging")
        layout.addWidget(self.file_size_card, 0, 1)
        
        # Dimensions card
        self.dimensions_card = self.create_info_card("Dimensions", "-", "purple", "expand-alt")
        layout.addWidget(self.dimensions_card, 0, 2)
        
        # Pixels card
        self.pixels_card = self.create_info_card("Total Pixels", "-", "orange", "th-large")
        layout.addWidget(self.pixels_card, 0, 3)
        
        # Format card
        self.format_card = self.create_info_card("Format", "-", "red", "file-image")
        layout.addWidget(self.format_card, 0, 4)
        
        return widget
    
    def create_info_card(self, label, value, color, icon_name):
        widget = QWidget()
        widget.setObjectName("info-card")
        widget.setMinimumHeight(120)
        widget.setCursor(Qt.PointingHandCursor)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Icon with Font Awesome
        icon_label = QLabel()
        icon_label.setObjectName(f"card-icon-{color}")
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Map icon names to Font Awesome - FIXED: use fa5s instead of fa
        icon_map = {
            'file': 'fa5s.file',
            'weight-hanging': 'fa5s.weight-hanging',
            'expand-alt': 'fa5s.expand-alt',
            'th-large': 'fa5s.th-large',
            'file-image': 'fa5s.file-image'
        }
        
        if icon_name in icon_map:
            icon_color = self.get_color_for_icon(color)
            try:
                icon = qta.icon(icon_map[icon_name], color=icon_color)
                icon_pixmap = icon.pixmap(24, 24)
                icon_label.setPixmap(icon_pixmap)
            except Exception as e:
                # Fallback to text if icon fails
                print(f"Icon error for {icon_name}: {e}")
                icon_label.setText("📄")
        else:
            icon_label.setText("📄")
        
        # Label
        label_widget = QLabel(label)
        label_widget.setObjectName("card-label")
        
        # Value
        value_widget = QLabel(value)
        value_widget.setObjectName("card-value")
        value_widget.setWordWrap(True)
        
        layout.addWidget(icon_label)
        layout.addWidget(label_widget)
        layout.addWidget(value_widget)
        layout.addStretch()
        
        return widget
    
    def get_color_for_icon(self, color):
        """Get hex color for different icon types"""
        colors = {
            'blue': '#4F46E5',
            'green': '#10B981',
            'purple': '#A855F7',
            'orange': '#F59E0B',
            'red': '#EF4444'
        }
        return colors.get(color, '#4F46E5')
    
    def create_image_processing_section(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Original image card
        original_card = self.create_image_card("Original Image", "file-upload", True)
        layout.addWidget(original_card)
        
        # Processed image card
        processed_card = self.create_image_card("Processed Image", "magic", False)
        layout.addWidget(processed_card)
        
        return widget
    
    def create_image_card(self, title, icon, is_original):
        widget = QWidget()
        widget.setObjectName("processing-card")
        widget.setMinimumHeight(500)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Card header
        header = QWidget()
        header.setObjectName("card-header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title with icon
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)
        
        # Add icon to title
        icon_label = QLabel()
        icon_label.setFixedSize(20, 20)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Set icon based on type - FIXED: use fa5s instead of fa
        if is_original:
            try:
                icon_fa = qta.icon('fa5s.file-upload', color='#4F46E5')
                icon_pixmap = icon_fa.pixmap(16, 16)
                icon_label.setPixmap(icon_pixmap)
            except:
                icon_label.setText("📤")
        else:
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
        
        # Buttons or status badge
        if is_original:
            upload_btn = QPushButton(" Upload Image")
            upload_btn.setObjectName("upload-btn")
            upload_btn.setCursor(Qt.PointingHandCursor)
            
            # Add upload icon to button - FIXED: use fa5s instead of fa
            try:
                upload_icon = qta.icon('fa5s.upload', color='white')
                upload_btn.setIcon(upload_icon)
                upload_btn.setIconSize(QSize(16, 16))
            except:
                upload_btn.setText("📤 Upload Image")
                
            upload_btn.clicked.connect(self.upload_image)
            header_layout.addWidget(title_widget)
            header_layout.addWidget(upload_btn)
        else:
            # Create a container for status and save button
            right_widget = QWidget()
            right_layout = QHBoxLayout(right_widget)
            right_layout.setContentsMargins(0, 0, 0, 0)
            right_layout.setSpacing(12)
            
            self.processed_status = QLabel("Waiting")
            self.processed_status.setObjectName("status-badge-pending")
            
            # Create save button
            self.save_btn = QPushButton(" Save")
            self.save_btn.setObjectName("save-btn")
            self.save_btn.setCursor(Qt.PointingHandCursor)
            self.save_btn.setEnabled(False)  # Disabled until an image is processed
            
            # Add save icon to button
            try:
                save_icon = qta.icon('fa5s.save', color='white')
                self.save_btn.setIcon(save_icon)
                self.save_btn.setIconSize(QSize(14, 14))
            except:
                self.save_btn.setText("💾 Save")
                
            self.save_btn.clicked.connect(self.save_processed_image)
            
            right_layout.addWidget(self.processed_status)
            right_layout.addWidget(self.save_btn)
            
            header_layout.addWidget(title_widget)
            header_layout.addWidget(right_widget)
        
        layout.addWidget(header)
        
        # Image display area
        display_area = QWidget()
        display_area.setObjectName("image-display-area")
        display_area.setMinimumHeight(400)
        display_layout = QVBoxLayout(display_area)
        display_layout.setContentsMargins(30, 30, 30, 30)
        display_layout.setAlignment(Qt.AlignCenter)
        
        if is_original:
            self.original_placeholder = self.create_image_placeholder("Upload Original Image", "Drag & drop or click to browse", "cloud-upload-alt")
            self.original_image_label = QLabel()
            self.original_image_label.setAlignment(Qt.AlignCenter)
            self.original_image_label.hide()
            
            display_layout.addWidget(self.original_placeholder)
            display_layout.addWidget(self.original_image_label)
        else:
            self.processed_placeholder = self.create_image_placeholder("Processing Image", "Will appear here after processing", "cogs")
            self.processed_image_label = QLabel()
            self.processed_image_label.setAlignment(Qt.AlignCenter)
            self.processed_image_label.hide()
            
            display_layout.addWidget(self.processed_placeholder)
            display_layout.addWidget(self.processed_image_label)
        
        layout.addWidget(display_area)
        
        return widget
    
    def create_image_placeholder(self, text, subtext, icon):
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
        
        # Set Font Awesome icon - FIXED: use fa5s instead of fa
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
    
    def create_control_panel(self):
        widget = QWidget()
        widget.setObjectName("control-panel")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)  # Increased spacing
        
        # Panel header
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
        layout.addWidget(header)
        
        # Create a container to evenly distribute the content
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setSpacing(32)  # Increased spacing between sections
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a widget for filter cards
        filters_widget = QWidget()
        filters_layout = QVBoxLayout(filters_widget)
        filters_layout.setContentsMargins(0, 0, 0, 0)
        filters_layout.setSpacing(16)  # Added spacing
        
        # Filter cards grid
        filter_grid = self.create_filter_grid()
        filters_layout.addWidget(filter_grid)
        
        # Add stretch to push filter grid to top
        filters_layout.addStretch()
        
        # Process button section
        process_section = self.create_process_section()
        
        # Add widgets to content layout with stretch factors
        content_layout.addWidget(filters_widget, 3)  # 3/4 of space for filters
        content_layout.addWidget(process_section, 1)  # 1/4 of space for process button
        
        layout.addWidget(content_container)
        
        return widget
    
    def create_filter_grid(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setHorizontalSpacing(24)  # Increased horizontal spacing
        layout.setVerticalSpacing(16)    # Increased vertical spacing
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.filter_group = QButtonGroup()
        filters = [
            ("Grayscale", "custom_grayscale", "moon", "Manual grayscale conversion using luminosity method", None),
            ("Black & White", "custom_bw", "adjust", "Using the grayscale conversion and then applying a threshold to create a binary black and white image", self.create_threshold_widget()),
        ]
        
        for i, (name, value, icon, description, threshold_widget) in enumerate(filters):
            row = i // 2
            col = i % 2
            
            filter_widget = self.create_filter_option(name, value, icon, description, threshold_widget)
            layout.addWidget(filter_widget, row, col)
        
        # Check the first filter by default
        if self.filter_group.buttons():
            self.filter_group.buttons()[0].setChecked(True)
        
        return widget
    
    def create_filter_option(self, name, value, icon, description, threshold_widget=None):
        widget = QWidget()
        widget.setObjectName("filter-option")
        widget.setMinimumHeight(200)  # Increased height for better spacing
        widget.setMinimumWidth(350)   # Minimum width for better layout
        widget.setCursor(Qt.PointingHandCursor)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create a container for the radio button and label
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        radio = QRadioButton()
        radio.setObjectName(f"filter-{value}")
        radio.setText("")  # Hide text
        radio.setCursor(Qt.PointingHandCursor)
        radio.toggled.connect(lambda checked, val=value: self.on_filter_changed(val, checked))
        
        label = QLabel()
        label.setObjectName("filter-label")
        label_layout = QVBoxLayout(label)
        label_layout.setContentsMargins(24, 24, 24, 24)  # Increased padding
        label_layout.setSpacing(16)  # Increased spacing
        
        # Top row: Icon and name
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(16)  # Increased spacing
        
        # Icon with Font Awesome - FIXED: use fa5s instead of fa
        icon_widget = QLabel()
        icon_widget.setObjectName("filter-icon")
        icon_widget.setFixedSize(48, 48)  # Slightly larger icon
        icon_widget.setAlignment(Qt.AlignCenter)
        
        # Map icon names to Font Awesome
        icon_map = {
            'moon': 'fa5s.moon',
            'exchange-alt': 'fa5s.exchange-alt',
            'umbrella-beach': 'fa5s.umbrella-beach',
            'sun': 'fa5s.sun',
            'adjust': 'fa5s.adjust'
        }
        
        if icon in icon_map:
            try:
                icon_fa = qta.icon(icon_map[icon], color='#4F46E5')
                icon_pixmap = icon_fa.pixmap(28, 28)
                icon_widget.setPixmap(icon_pixmap)
            except:
                icon_widget.setText("⚫")
        else:
            icon_widget.setText("⚫")
        
        # Name
        name_label = QLabel(name)
        name_label.setObjectName("filter-name")
        
        top_layout.addWidget(icon_widget)
        top_layout.addWidget(name_label)
        top_layout.addStretch()
        
        label_layout.addWidget(top_widget)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setObjectName("filter-description")
        desc_label.setWordWrap(True)
        desc_label.setMinimumHeight(60)  # Minimum height for description
        desc_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        label_layout.addWidget(desc_label)
        
        # Add threshold widget if provided
        if threshold_widget:
            threshold_widget.setVisible(False)  # Hidden by default
            label_layout.addWidget(threshold_widget)
        
        container_layout.addWidget(radio)
        container_layout.addWidget(label)
        
        layout.addWidget(container)
        
        self.filter_group.addButton(radio)
        
        # Connect label click to radio button
        label.mousePressEvent = lambda e, rb=radio: rb.setChecked(True)
        
        # Store threshold widget reference if this is the B&W filter
        if value == "custom_bw":
            self.threshold_widget = threshold_widget
            self.bw_radio = radio
        
        return widget
    
    def create_threshold_widget(self):
        """Create threshold slider widget for Black & White filter"""
        widget = QWidget()
        widget.setObjectName("threshold-widget")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 12, 0, 0)  # Increased top margin
        layout.setSpacing(12)  # Increased spacing
        
        # Threshold label and value
        threshold_header = QWidget()
        threshold_header_layout = QHBoxLayout(threshold_header)
        threshold_header_layout.setContentsMargins(0, 0, 0, 0)
        
        threshold_label = QLabel("Threshold:")
        threshold_label.setObjectName("threshold-label")
        
        self.threshold_value_label = QLabel("128")
        self.threshold_value_label.setObjectName("threshold-value-label")
        
        threshold_header_layout.addWidget(threshold_label)
        threshold_header_layout.addStretch()
        threshold_header_layout.addWidget(self.threshold_value_label)
        
        # Threshold slider
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setObjectName("threshold-slider")
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255)
        self.threshold_slider.setValue(128)
        self.threshold_slider.setSingleStep(1)
        self.threshold_slider.setPageStep(10)
        self.threshold_slider.valueChanged.connect(self.on_threshold_changed)
        
        # Threshold explanation
        threshold_explanation = QLabel("Lower = more black, Higher = more white")
        threshold_explanation.setObjectName("threshold-explanation")
        threshold_explanation.setWordWrap(True)
        threshold_explanation.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(threshold_header)
        layout.addWidget(self.threshold_slider)
        layout.addWidget(threshold_explanation)
        
        return widget
    
    def create_process_section(self):
        """Create the process button section (right side)"""
        widget = QWidget()
        widget.setObjectName("process-section")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)  # Added padding
        layout.setSpacing(24)  # Increased spacing
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        # Process button container for better centering
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)
        
        # Process button
        self.process_btn = QPushButton(" Process Image")
        self.process_btn.setObjectName("process-btn")
        self.process_btn.setCursor(Qt.PointingHandCursor)
        self.process_btn.clicked.connect(self.process_image)
        self.process_btn.setEnabled(False)
        self.process_btn.setMinimumHeight(70)  # Taller button
        self.process_btn.setMinimumWidth(250)
        
        # Add bolt icon to button - FIXED: use fa5s instead of fa
        try:
            bolt_icon = qta.icon('fa5s.bolt', color='white')
            self.process_btn.setIcon(bolt_icon)
            self.process_btn.setIconSize(QSize(28, 28))  # Larger icon
        except:
            self.process_btn.setText("⚡ Process Image")
        
        # Description
        description = QLabel("Select a filter above and click to apply it to your image. The processed result will appear in the right panel.")
        description.setObjectName("button-description")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        description.setMinimumWidth(280)  # Minimum width
        description.setMaximumWidth(320)  # Maximum width
        
        button_layout.addWidget(self.process_btn, 0, Qt.AlignHCenter)
        button_layout.addWidget(description, 0, Qt.AlignHCenter)
        
        layout.addWidget(button_container)
        layout.addStretch()
        
        return widget
    
    def on_filter_changed(self, filter_name, checked):
        """Handle filter selection change"""
        if checked:
            self.current_filter = filter_name
            # Show/hide threshold widget based on filter
            if hasattr(self, 'threshold_widget'):
                if filter_name == "custom_bw":
                    self.threshold_widget.setVisible(True)
                else:
                    self.threshold_widget.setVisible(False)
    
    def on_threshold_changed(self, value):
        """Handle threshold slider change"""
        self.threshold_value_label.setText(str(value))
        # Update threshold in black and white converter
        self.black_white_converter.threshold = value
    
    def upload_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select Image", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp)"
        )
        
        if file_path:
            try:
                # Load image using ImageProcessor
                image_info = self.image_processor.load_image(file_path)
                self.original_image = self.image_processor.pil_image
                
                # Display original image
                pixmap = QPixmap(file_path)
                scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.original_image_label.setPixmap(scaled_pixmap)
                self.original_placeholder.hide()
                self.original_image_label.show()
                
                # Update file info cards
                self.update_info_cards(image_info)
                
                # Update status
                self.status_value.setText("Image Uploaded")
                self.status_value.setObjectName("status-value-uploaded")
                self.apply_styles()
                
                # Enable process button
                self.process_btn.setEnabled(True)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")
    
    def update_info_cards(self, image_info):
        """Update all information cards with image data"""
        # File name
        file_name = image_info['name']
        if len(file_name) > 10:
            file_name = file_name[:7] + '...' + file_name.split('.')[-1]
        self.file_name_card.findChild(QLabel, "card-value").setText(file_name)
        
        # File size
        file_size_kb = image_info['file_size'] / 1024
        self.file_size_card.findChild(QLabel, "card-value").setText(f"{file_size_kb:.1f} KB")
        
        # Dimensions
        dimensions = f"{image_info['width']} × {image_info['height']}"
        self.dimensions_card.findChild(QLabel, "card-value").setText(dimensions)
        
        # Total pixels
        pixels = image_info['total_pixels']
        self.pixels_card.findChild(QLabel, "card-value").setText(f"{pixels:,}")
        
        # Format
        format_name = image_info['format'] if image_info['format'] else "Unknown"
        self.format_card.findChild(QLabel, "card-value").setText(format_name)
    
    def process_image(self):
        if not self.original_image:
            QMessageBox.warning(self, "Warning", "Please upload an image first!")
            return
        
        # Get selected filter
        selected_filter = self.current_filter
        
        if not selected_filter:
            selected_filter = "custom_grayscale"
        
        # Update status
        self.status_value.setText("Processing...")
        self.status_value.setObjectName("status-value-processing")
        self.processed_status.setText("Processing")
        self.processed_status.setObjectName("status-badge-processing")
        self.process_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.apply_styles()
        
        QApplication.processEvents()  # Update UI
        
        try:
            # Process image based on selected filter
            processed = self.apply_filter(self.original_image, selected_filter)
            self.processed_image = processed
            
            # Convert PIL image to QPixmap
            byte_arr = io.BytesIO()
            processed.save(byte_arr, format='PNG')
            pixmap = QPixmap()
            pixmap.loadFromData(byte_arr.getvalue())
            
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.processed_image_label.setPixmap(scaled_pixmap)
            self.processed_placeholder.hide()
            self.processed_image_label.show()
            
            # Update status
            self.status_value.setText("Processing Complete")
            self.status_value.setObjectName("status-value-complete")
            self.processed_status.setText("Complete")
            self.processed_status.setObjectName("status-badge-ready")
            
            # Enable save button
            self.save_btn.setEnabled(True)
            
            # Show success message with threshold info if applicable
            if selected_filter == "custom_bw":
                threshold = self.threshold_slider.value()
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Image processed successfully using Black & White filter!\nThreshold: {threshold}"
                )
            else:
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Image processed successfully using {selected_filter.replace('_', ' ').title()} filter!"
                )
            
        except Exception as e:
            # Update status to error
            self.status_value.setText("Processing Failed")
            self.status_value.setObjectName("status-value-ready")
            self.processed_status.setText("Failed")
            self.processed_status.setObjectName("status-badge-pending")
            self.save_btn.setEnabled(False)
            QMessageBox.critical(self, "Error", f"Failed to process image: {str(e)}")
        
        self.process_btn.setEnabled(True)
        self.apply_styles()
    
    def save_processed_image(self):
        """Save the processed image to a file"""
        if not self.processed_image:
            QMessageBox.warning(self, "Warning", "No processed image to save!")
            return
        
        # Get save file path
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Save Processed Image", "",
            "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;BMP Image (*.bmp);;TIFF Image (*.tiff);;All Files (*)"
        )
        
        if file_path:
            try:
                # Determine format from file extension
                if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                    format = 'JPEG'
                elif file_path.lower().endswith('.png'):
                    format = 'PNG'
                elif file_path.lower().endswith('.bmp'):
                    format = 'BMP'
                elif file_path.lower().endswith('.tiff'):
                    format = 'TIFF'
                else:
                    # Default to PNG
                    file_path += '.png'
                    format = 'PNG'
                
                # Save the image
                self.processed_image.save(file_path, format=format)
                
                # Show success message
                QMessageBox.information(self, "Success", f"Image saved successfully to:\n{file_path}")
                
                # Update status
                self.status_value.setText("Image Saved")
                self.status_value.setObjectName("status-value-complete")
                self.apply_styles()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")
    
    def apply_filter(self, image, filter_name):
        """Apply selected filter to image"""
        if filter_name == "custom_grayscale":
            # Use our custom grayscale converter with manual loop method
            return self.grayscale_converter.convert_manual_loop(image)
        
        elif filter_name == "custom_bw":
            # Use black and white converter with current threshold
            threshold = self.threshold_slider.value()
            return self.black_white_converter.convert_to_black_white(image, threshold=threshold)
        
        else:
            # Default to custom grayscale
            return self.grayscale_converter.convert_manual_loop(image)
    
    def apply_styles(self):
        style = """
        /* Global Styles */
        QWidget {
            background-color: #111827;
            color: #F9FAFB;
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
        }
        
        /* Header - Fixed at top */
        #header {
            background-color: #1F2937;
            border-bottom: 1px solid #374151;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        #logo-icon {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #4F46E5, stop:1 #10B981);
            border-radius: 8px;
            font-weight: bold;
            font-size: 18px;
        }
        
        #logo-text {
            font-size: 22px;
            font-weight: 700;
            color: #F9FAFB;
        }
        
        #nav-item-active {
            padding: 5px 20px;
            border-radius: 8px;
            background-color: #4F46E5;
            color: white;
            font-weight: 500;
            font-size: 15px;
            border: none;
        }
        
        #nav-item-active:hover {
            background-color: #4338CA;
        }
        
        #user-profile {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }
        
        #user-profile:hover {
            background-color: rgba(255, 255, 255, 0.08);
        }
        
        #user-avatar {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #4F46E5, stop:1 #10B981);
            border-radius: 16px;
            font-weight: 600;
            font-size: 14px;
            color: white;
        }
        
        #user-name {
            font-size: 14px;
            font-weight: 600;
        }
        
        #user-role {
            font-size: 12px;
            color: #9CA3AF;
        }
        
        /* Page Header */
        #page-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        #page-subtitle {
            color: #9CA3AF;
            font-size: 15px;
        }
        
        /* Status Bar */
        #status-bar {
            background-color: #1F2937;
            border-radius: 12px;
            border: 1px solid #374151;
        }
        
        #status-label {
            font-size: 14px;
            color: #9CA3AF;
        }
        
        #status-value-ready {
            font-size: 16px;
            font-weight: 600;
            color: #10B981;
        }
        
        #status-value-uploaded {
            font-size: 16px;
            font-weight: 600;
            color: #F59E0B;
        }
        
        #status-value-processing {
            font-size: 16px;
            font-weight: 600;
            color: #4F46E5;
        }
        
        #status-value-complete {
            font-size: 16px;
            font-weight: 600;
            color: #10B981;
        }
        
        /* Info Cards */
        #info-card {
            background-color: #1F2937;
            border-radius: 12px;
            border: 1px solid #374151;
        }
        
        #info-card:hover {
            border-color: #4F46E5;
            transform: translateY(-2px);
        }
        
        #card-icon-blue {
            background-color: rgba(79, 70, 229, 0.2);
            color: #4F46E5;
            border-radius: 8px;
            font-size: 18px;
        }
        
        #card-icon-green {
            background-color: rgba(16, 185, 129, 0.2);
            color: #10B981;
            border-radius: 8px;
            font-size: 18px;
        }
        
        #card-icon-purple {
            background-color: rgba(168, 85, 247, 0.2);
            color: #A855F7;
            border-radius: 8px;
            font-size: 18px;
        }
        
        #card-icon-orange {
            background-color: rgba(245, 158, 11, 0.2);
            color: #F59E0B;
            border-radius: 8px;
            font-size: 18px;
        }
        
        #card-icon-red {
            background-color: rgba(239, 68, 68, 0.2);
            color: #EF4444;
            border-radius: 8px;
            font-size: 18px;
        }
        
        #card-label {
            color: #9CA3AF;
            font-size: 13px;
        }
        
        #card-value {
            font-size: 18px;
            font-weight: 600;
        }
        
        /* Processing Cards */
        #processing-card {
            background-color: #1F2937;
            border-radius: 12px;
            border: 1px solid #374151;
        }
        
        #card-header {
            border-bottom: 1px solid #374151;
        }
        
        #card-title {
            font-size: 18px;
            font-weight: 600;
        }
        
        #upload-btn {
            background-color: #4F46E5;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 14px;
        }
        
        #upload-btn:hover {
            background-color: #4338CA;
        }
        
        /* Save Button */
        #save-btn {
            background-color: #10B981;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 13px;
        }
        
        #save-btn:hover:enabled {
            background-color: #0DA271;
            transform: translateY(-2px);
        }
        
        #save-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        #status-badge-pending {
            background-color: rgba(245, 158, 11, 0.2);
            color: #F59E0B;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        #status-badge-processing {
            background-color: rgba(79, 70, 229, 0.2);
            color: #4F46E5;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        #status-badge-ready {
            background-color: rgba(16, 185, 129, 0.2);
            color: #10B981;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        #image-display-area {
            background-color: rgba(255, 255, 255, 0.03);
        }
        
        #image-placeholder {
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            border: 2px dashed #374151;
        }
        
        #placeholder-icon {
            font-size: 64px;
            color: #9CA3AF;
            opacity: 0.7;
        }
        
        #placeholder-text {
            color: #9CA3AF;
            font-size: 16px;
            margin-bottom: 8px;
        }
        
        #placeholder-subtext {
            color: #9CA3AF;
            font-size: 14px;
            opacity: 0.7;
        }
        
        /* Control Panel */
        #control-panel {
            background-color: #1F2937;
            border-radius: 12px;
            border: 1px solid #374151;
        }
        
        #panel-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        #panel-subtitle {
            color: #9CA3AF;
            font-size: 14px;
            margin-bottom: 16px;
        }
        
        /* Process Section */
        #process-section {
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            border: 1px dashed #374151;
            min-width: 320px;
            max-width: 360px;
            min-height: 320px;
        }
        
        /* Filter Options */
        #filter-option {
            min-height: 200px;
        }
        
        #filter-label {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid #374151;
            border-radius: 12px;
            min-height: 180px;
        }
        
        QRadioButton:checked + #filter-label {
            border-color: #4F46E5;
            background-color: rgba(79, 70, 229, 0.1);
            box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
        }
        
        #filter-label:hover {
            background-color: rgba(255, 255, 255, 0.08);
            transform: translateY(-3px);
        }
        
        #filter-icon {
            background-color: rgba(79, 70, 229, 0.15);
            border-radius: 12px;
            color: #4F46E5;
            font-size: 20px;
            min-width: 48px;
            min-height: 48px;
        }
        
        #filter-name {
            font-weight: 600;
            font-size: 20px;
            color: #F9FAFB;
            margin-bottom: 2px;
            padding-left: 8px;
        }
        
        #filter-description {
            font-size: 14px;
            color: #9CA3AF;
            line-height: 1.4;
            min-height: 60px;
            padding-top: 8px;
        }
        
        /* Threshold Widget */
        #threshold-widget {
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            padding: 16px;
            margin-top: 12px;
        }
        
        #threshold-label {
            color: #9CA3AF;
            font-size: 14px;
            font-weight: 600;
        }
        
        #threshold-value-label {
            color: #4F46E5;
            font-size: 18px;
            font-weight: 700;
        }
        
        #threshold-slider {
            height: 24px;
            margin: 8px 0;
        }
        
        #threshold-slider::groove:horizontal {
            border: 1px solid #374151;
            height: 8px;
            background: #1F2937;
            border-radius: 4px;
        }
        
        #threshold-slider::handle:horizontal {
            background: #4F46E5;
            border: 1px solid #4338CA;
            width: 20px;
            height: 20px;
            border-radius: 10px;
            margin: -6px 0;
        }
        
        #threshold-slider::handle:horizontal:hover {
            background: #4338CA;
        }
        
        #threshold-explanation {
            color: #9CA3AF;
            font-size: 12px;
            margin-top: 8px;
            padding-top: 4px;
        }
        
        /* Process Button */
        #process-btn {
            padding: 20px 36px;
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #4F46E5, stop:1 #4338CA);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            font-size: 18px;
            min-width: 250px;
            min-height: 70px;
        }
        
        #process-btn:hover:enabled {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #4338CA, stop:1 #4F46E5);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.4);
        }
        
        #process-btn:disabled {
            opacity: 0.5;
        }
        
        #button-description {
            color: #9CA3AF;
            font-size: 14px;
            line-height: 1.5;
            padding: 8px 12px;
        }
        
        QRadioButton {
            margin-right: -100px;
        }
        
        /* Hide scrollbar buttons */
        QScrollBar:horizontal, QScrollBar:vertical {
            border: none;
            background-color: #1F2937;
        }
        
        QScrollBar::handle:horizontal, QScrollBar::handle:vertical {
            background-color: #4F46E5;
            border-radius: 5px;
        }
        
        QScrollBar::handle:horizontal:hover, QScrollBar::handle:vertical:hover {
            background-color: #4338CA;
        }
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        """
        
        self.setStyleSheet(style)

def main():
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = ImageProcessingApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()