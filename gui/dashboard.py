import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import io
import qtawesome as qta

# Import our custom modules
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
        self.setWindowTitle("CPEP 323A")
        self.setMinimumSize(1400, 900)
        
        self.create_scroll_area()
        self.create_main_layout()
        
    def create_scroll_area(self):
        """Create the main scroll area"""
        central_widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_area.setStyleSheet(self.get_scrollbar_style())
        self.setCentralWidget(scroll_area)
        self.main_widget = central_widget
        
    def create_main_layout(self):
        """Create the main layout with all components"""
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        main_layout.addWidget(self.create_header())
        main_layout.addWidget(self.create_content_widget())
        
    def create_content_widget(self):
        """Create the scrollable content area"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)
        
        content_layout.addWidget(self.create_page_header())
        content_layout.addWidget(self.create_status_bar())
        content_layout.addWidget(self.create_file_info_cards())
        content_layout.addWidget(self.create_image_processing_section())
        content_layout.addWidget(self.create_control_panel())
        content_layout.addStretch()
        
        return content_widget
        
    def create_header(self):
        from gui.ui_components.header import create_header
        return create_header()
    
    def create_page_header(self):
        from gui.ui_components.page_header import create_page_header
        return create_page_header()
    
    def create_status_bar(self):
        from gui.ui_components.status_bar import create_status_bar
        widget, self.status_value = create_status_bar()
        return widget
    
    def create_file_info_cards(self):
        from gui.ui_components.info_cards import create_file_info_cards
        widget, cards = create_file_info_cards()
        self.file_name_card, self.file_size_card, self.dimensions_card, self.pixels_card, self.format_card = cards
        return widget
    
    def create_image_processing_section(self):
        from gui.ui_components.image_section import create_image_processing_section
        widget, components = create_image_processing_section(self)
        (
            self.original_placeholder, self.original_image_label,
            self.processed_placeholder, self.processed_image_label,
            self.processed_status, self.save_btn
        ) = components
        return widget
    
    def create_control_panel(self):
        from gui.ui_components.control_panel import create_control_panel
        widget, components = create_control_panel(self)
        (
            self.filter_group, self.threshold_widget, self.threshold_value_label,
            self.threshold_slider, self.process_btn, self.bw_radio
        ) = components
        return widget
    
    def get_scrollbar_style(self):
        """Get scrollbar style as string"""
        return """
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
        """
    
    def on_filter_changed(self, filter_name, checked):
        """Handle filter selection change"""
        if checked:
            self.current_filter = filter_name
            if hasattr(self, 'threshold_widget'):
                self.threshold_widget.setVisible(filter_name == "custom_bw")
    
    def on_threshold_changed(self, value):
        """Handle threshold slider change"""
        self.threshold_value_label.setText(str(value))
        self.black_white_converter.threshold = value
    
    def upload_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select Image", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp)"
        )
        
        if file_path:
            try:
                image_info = self.image_processor.load_image(file_path)
                self.original_image = self.image_processor.pil_image
                
                pixmap = QPixmap(file_path)
                scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.original_image_label.setPixmap(scaled_pixmap)
                self.original_placeholder.hide()
                self.original_image_label.show()
                
                self.update_info_cards(image_info)
                self.status_value.setText("Image Uploaded")
                self.status_value.setObjectName("status-value-uploaded")
                self.apply_styles()
                self.process_btn.setEnabled(True)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")
    
    def update_info_cards(self, image_info):
        """Update all information cards with image data"""
        from gui.ui_components.info_cards import update_info_cards
        update_info_cards(
            image_info,
            self.file_name_card,
            self.file_size_card,
            self.dimensions_card,
            self.pixels_card,
            self.format_card
        )
    
    def process_image(self):
        if not self.original_image:
            QMessageBox.warning(self, "Warning", "Please upload an image first!")
            return
        
        selected_filter = self.current_filter or "custom_grayscale"
        
        self.status_value.setText("Processing...")
        self.status_value.setObjectName("status-value-processing")
        self.processed_status.setText("Processing")
        self.processed_status.setObjectName("status-badge-processing")
        self.process_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.apply_styles()
        
        QApplication.processEvents()
        
        try:
            processed = self.apply_filter(self.original_image, selected_filter)
            self.processed_image = processed
            
            byte_arr = io.BytesIO()
            processed.save(byte_arr, format='PNG')
            pixmap = QPixmap()
            pixmap.loadFromData(byte_arr.getvalue())
            
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.processed_image_label.setPixmap(scaled_pixmap)
            self.processed_placeholder.hide()
            self.processed_image_label.show()
            
            self.status_value.setText("Processing Complete")
            self.status_value.setObjectName("status-value-complete")
            self.processed_status.setText("Complete")
            self.processed_status.setObjectName("status-badge-ready")
            self.save_btn.setEnabled(True)
            
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
        
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Save Processed Image", "",
            "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;BMP Image (*.bmp);;TIFF Image (*.tiff);;All Files (*)"
        )
        
        if file_path:
            try:
                if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                    format = 'JPEG'
                elif file_path.lower().endswith('.png'):
                    format = 'PNG'
                elif file_path.lower().endswith('.bmp'):
                    format = 'BMP'
                elif file_path.lower().endswith('.tiff'):
                    format = 'TIFF'
                else:
                    file_path += '.png'
                    format = 'PNG'
                
                self.processed_image.save(file_path, format=format)
                QMessageBox.information(self, "Success", f"Image saved successfully to:\n{file_path}")
                self.status_value.setText("Image Saved")
                self.status_value.setObjectName("status-value-complete")
                self.apply_styles()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")
    
    def apply_filter(self, image, filter_name):
        """Apply selected filter to image"""
        if filter_name == "custom_grayscale":
            return self.grayscale_converter.convert_manual_loop(image)
        elif filter_name == "custom_bw":
            threshold = self.threshold_slider.value()
            return self.black_white_converter.convert_to_black_white(image, threshold=threshold)
        else:
            return self.grayscale_converter.convert_manual_loop(image)

    
    def apply_styles(self):
        from gui.styles.app_styles import get_app_styles
        self.setStyleSheet(get_app_styles())