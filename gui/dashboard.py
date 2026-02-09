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
        self.cropped_image = None
        self.is_cropping = False
        self.crop_start = QPoint()
        self.crop_end = QPoint()
        self.crop_rect = QRect()
        self.crop_applied = False
        self.image_processor = ImageProcessor()
        self.grayscale_converter = GrayscaleConverter()
        self.black_white_converter = BlackWhiteConverter()
        self.current_filter = "custom_grayscale"
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        self.setWindowTitle("CPEP 323A - Advanced Image Processing")
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
        widget = create_page_header()
        widget.findChild(QLabel, "page-title").setText("Advanced Image Processing Dashboard")
        widget.findChild(QLabel, "page-subtitle").setText("Upload, crop, and apply filters including background removal")
        return widget
    
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
            self.processed_status, self.save_btn, self.crop_btn
        ) = components
        
        self.add_crop_confirmation_controls(widget)
        self.original_image_label.installEventFilter(self)
        
        return widget
    
    def add_crop_confirmation_controls(self, parent_widget):
        """Add crop confirmation controls below the original image"""
        original_card = parent_widget.layout().itemAt(0).widget()
        card_layout = original_card.layout()
        
        self.crop_confirmation_widget = QWidget()
        self.crop_confirmation_widget.setObjectName("crop-confirmation")
        self.crop_confirmation_widget.hide()
        
        crop_confirmation_layout = QHBoxLayout(self.crop_confirmation_widget)
        crop_confirmation_layout.setContentsMargins(20, 10, 20, 20)
        crop_confirmation_layout.setSpacing(12)
        
        self.apply_crop_btn = QPushButton(" Apply Crop")
        self.apply_crop_btn.setObjectName("apply-crop-btn")
        self.apply_crop_btn.setCursor(Qt.PointingHandCursor)
        self.apply_crop_btn.clicked.connect(self.apply_crop)
        self.apply_crop_btn.setEnabled(False)
        
        try:
            check_icon = qta.icon('fa5s.check', color='white')
            self.apply_crop_btn.setIcon(check_icon)
            self.apply_crop_btn.setIconSize(QSize(14, 14))
        except:
            self.apply_crop_btn.setText("✓ Apply Crop")
        
        self.cancel_crop_btn = QPushButton(" Cancel")
        self.cancel_crop_btn.setObjectName("cancel-crop-btn")
        self.cancel_crop_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_crop_btn.clicked.connect(self.cancel_cropping)
        
        try:
            cancel_icon = qta.icon('fa5s.times', color='white')
            self.cancel_crop_btn.setIcon(cancel_icon)
            self.cancel_crop_btn.setIconSize(QSize(14, 14))
        except:
            self.cancel_crop_btn.setText("✗ Cancel")
        
        crop_confirmation_layout.addWidget(self.apply_crop_btn)
        crop_confirmation_layout.addWidget(self.cancel_crop_btn)
        crop_confirmation_layout.addStretch()
        
        card_layout.addWidget(self.crop_confirmation_widget)
    
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
            #crop-btn {
                background-color: #F59E0B;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 13px;
            }
            #crop-btn:hover:enabled {
                background-color: #D97706;
                transform: translateY(-1px);
            }
            #crop-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            #apply-crop-btn {
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 13px;
            }
            #apply-crop-btn:hover:enabled {
                background-color: #0DA271;
                transform: translateY(-1px);
            }
            #apply-crop-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            #cancel-crop-btn {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 13px;
            }
            #cancel-crop-btn:hover:enabled {
                background-color: #DC2626;
                transform: translateY(-1px);
            }
            #crop-confirmation {
                background-color: rgba(31, 41, 55, 0.5);
                border-radius: 8px;
                margin: 10px 20px;
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
    
    def eventFilter(self, obj, event):
        """Handle mouse events for crop selection"""
        if obj == self.original_image_label and self.is_cropping:
            if event.type() == QEvent.MouseButtonPress:
                self.crop_start = event.pos()
                self.crop_end = event.pos()
                self.crop_rect = QRect(self.crop_start, self.crop_end)
                self.apply_crop_btn.setEnabled(False)
                return True
                
            elif event.type() == QEvent.MouseMove and event.buttons() & Qt.LeftButton:
                self.crop_end = event.pos()
                self.crop_rect = QRect(self.crop_start, self.crop_end).normalized()
                
                if self.crop_rect.width() > 10 and self.crop_rect.height() > 10:
                    self.apply_crop_btn.setEnabled(True)
                
                obj.update()
                return True
                
            elif event.type() == QEvent.MouseButtonRelease:
                self.crop_end = event.pos()
                self.crop_rect = QRect(self.crop_start, self.crop_end).normalized()
                
                if self.crop_rect.width() > 10 and self.crop_rect.height() > 10:
                    self.apply_crop_btn.setEnabled(True)
                return True
                
            elif event.type() == QEvent.Paint:
                QLabel.paintEvent(obj, event)
                if self.is_cropping and not self.crop_rect.isNull():
                    painter = QPainter(obj)
                    painter.setPen(QPen(QColor(79, 70, 229), 2, Qt.DashLine))
                    painter.setBrush(QBrush(QColor(79, 70, 229, 30)))
                    painter.drawRect(self.crop_rect)
                    
                    painter.setPen(QColor(255, 255, 255))
                    painter.setFont(QFont("Arial", 10))
                    size_text = f"{self.crop_rect.width()} x {self.crop_rect.height()}"
                    painter.drawText(self.crop_rect.bottomRight() + QPoint(5, 15), size_text)
                    
                    marker_size = 8
                    corners = [
                        self.crop_rect.topLeft(),
                        self.crop_rect.topRight(),
                        self.crop_rect.bottomLeft(),
                        self.crop_rect.bottomRight()
                    ]
                    
                    painter.setBrush(QBrush(QColor(79, 70, 229)))
                    painter.setPen(Qt.NoPen)
                    
                    for corner in corners:
                        painter.drawRect(
                            corner.x() - marker_size//2,
                            corner.y() - marker_size//2,
                            marker_size,
                            marker_size
                        )
                    return True
        
        return super().eventFilter(obj, event)
    
    def start_cropping(self):
        """Start crop mode"""
        if not self.original_image:
            QMessageBox.warning(self, "Warning", "Please upload an image first!")
            return
        
        self.is_cropping = True
        self.crop_btn.setEnabled(False)
        self.crop_confirmation_widget.show()
        self.apply_crop_btn.setEnabled(False)
        
        self.original_image_label.setCursor(Qt.CrossCursor)
        
        self.status_value.setText("Crop Mode - Click and drag to select area")
        self.status_value.setObjectName("status-value-processing")
        self.apply_styles()
    
    def calculate_scaled_crop_rect(self):
        """Correctly calculate crop rectangle scaling from display to original image"""
        if not self.original_image or self.crop_rect.isNull():
            return None
        
        # Get the displayed pixmap
        pixmap = self.original_image_label.pixmap()
        if not pixmap:
            return None
        
        # Get actual pixmap size (might be smaller than label if aspect ratio preserved)
        pixmap_size = pixmap.size()
        label_size = self.original_image_label.size()
        
        # Calculate the offset if the pixmap is centered in the label
        offset_x = (label_size.width() - pixmap_size.width()) // 2
        offset_y = (label_size.height() - pixmap_size.height()) // 2
        
        # Adjust crop rectangle by the offset
        adjusted_rect = QRect(
            self.crop_rect.x() - offset_x,
            self.crop_rect.y() - offset_y,
            self.crop_rect.width(),
            self.crop_rect.height()
        )
        
        # Ensure the adjusted rectangle is within pixmap bounds
        adjusted_rect = adjusted_rect.intersected(QRect(0, 0, pixmap_size.width(), pixmap_size.height()))
        
        # Get original image size
        original_width, original_height = self.original_image.size
        
        # Calculate scale factors
        scale_x = original_width / pixmap_size.width()
        scale_y = original_height / pixmap_size.height()
        
        # Scale to original image coordinates
        scaled_rect = QRect(
            int(adjusted_rect.x() * scale_x),
            int(adjusted_rect.y() * scale_y),
            int(adjusted_rect.width() * scale_x),
            int(adjusted_rect.height() * scale_y)
        )
        
        # Ensure final rectangle is within original image bounds
        scaled_rect = scaled_rect.intersected(QRect(0, 0, original_width, original_height))
        
        return scaled_rect
    
    def apply_crop(self):
        """Apply the crop selection"""
        if not self.original_image or self.crop_rect.isNull():
            return
        
        # Get the correctly scaled crop rectangle
        scaled_rect = self.calculate_scaled_crop_rect()
        if not scaled_rect or scaled_rect.width() < 10 or scaled_rect.height() < 10:
            QMessageBox.warning(self, "Warning", "Invalid crop area! Please select a larger area.")
            return
        
        # Apply crop to original image
        cropped_pil = self.original_image.crop((
            scaled_rect.x(),
            scaled_rect.y(),
            scaled_rect.x() + scaled_rect.width(),
            scaled_rect.y() + scaled_rect.height()
        ))
        
        # Set the cropped image as the image to be processed
        self.cropped_image = cropped_pil
        self.crop_applied = True
        
        # Update original image display to show the cropped version
        byte_arr = io.BytesIO()
        cropped_pil.save(byte_arr, format='PNG')
        pixmap = QPixmap()
        pixmap.loadFromData(byte_arr.getvalue())
        
        # Display the cropped image in the original panel
        scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.original_image_label.setPixmap(scaled_pixmap)
        
        # Clear processed image since we have a new crop
        self.processed_image = None
        self.processed_image_label.hide()
        self.processed_placeholder.show()
        self.processed_status.setText("Waiting")
        self.processed_status.setObjectName("status-badge-pending")
        self.save_btn.setEnabled(False)
        
        # Update info cards with cropped dimensions
        self.update_image_info_after_crop(cropped_pil)
        
        # Exit crop mode
        self.cancel_cropping()
        
        QMessageBox.information(self, "Success", 
            f"Image cropped to {scaled_rect.width()} x {scaled_rect.height()} pixels\n"
            f"The cropped image is now ready for processing."
        )
    
    def cancel_cropping(self):
        """Cancel crop mode"""
        self.is_cropping = False
        self.crop_start = QPoint()
        self.crop_end = QPoint()
        self.crop_rect = QRect()
        
        self.crop_btn.setEnabled(True)
        self.crop_confirmation_widget.hide()
        self.apply_crop_btn.setEnabled(False)
        
        self.original_image_label.setCursor(Qt.ArrowCursor)
        self.original_image_label.update()
        
        self.status_value.setText("Ready for Processing")
        self.status_value.setObjectName("status-value-ready")
        self.apply_styles()
    
    def update_image_info_after_crop(self, cropped_image):
        """Update info cards after cropping"""
        width, height = cropped_image.size
        total_pixels = width * height
        
        self.dimensions_card.findChild(QLabel, "card-value").setText(f"{width} × {height}")
        self.pixels_card.findChild(QLabel, "card-value").setText(f"{total_pixels:,}")
        
        current_name = self.file_name_card.findChild(QLabel, "card-value").text()
        if not current_name.endswith(" (cropped)"):
            self.file_name_card.findChild(QLabel, "card-value").setText(f"{current_name} (cropped)")
    
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
                self.cropped_image = None
                self.crop_applied = False
                
                pixmap = QPixmap(file_path)
                scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.original_image_label.setPixmap(scaled_pixmap)
                self.original_placeholder.hide()
                self.original_image_label.show()
                
                self.processed_image = None
                self.processed_image_label.hide()
                self.processed_placeholder.show()
                self.processed_status.setText("Waiting")
                self.processed_status.setObjectName("status-badge-pending")
                self.save_btn.setEnabled(False)
                
                self.update_info_cards(image_info)
                self.status_value.setText("Image Uploaded")
                self.status_value.setObjectName("status-value-uploaded")
                self.apply_styles()
                self.process_btn.setEnabled(True)
                self.crop_btn.setEnabled(True)
                
                if self.is_cropping:
                    self.cancel_cropping()
                
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
        image_to_process = self.cropped_image if self.crop_applied and self.cropped_image else self.original_image
        
        if not image_to_process:
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
            processed = self.apply_filter(image_to_process, selected_filter)
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
            
            crop_info = " (cropped)" if self.crop_applied else ""
            if selected_filter == "custom_bw":
                threshold = self.threshold_slider.value()
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Image{crop_info} processed successfully using Black & White filter!\nThreshold: {threshold}"
                )
            elif selected_filter == "background_removal":
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Background removed successfully{crop_info}! The image now has transparency."
                )
            else:
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Image{crop_info} processed successfully using {selected_filter.replace('_', ' ').title()} filter!"
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
        
        if self.current_filter == "background_removal":
            file_path, _ = file_dialog.getSaveFileName(
                self, "Save Processed Image", "",
                "PNG Image (*.png);;All Files (*)"
            )
            if file_path and not file_path.lower().endswith('.png'):
                file_path += '.png'
            format = 'PNG'
        else:
            file_path, _ = file_dialog.getSaveFileName(
                self, "Save Processed Image", "",
                "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;BMP Image (*.bmp);;TIFF Image (*.tiff);;All Files (*)"
            )
            
            if file_path:
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
        
        if file_path:
            try:
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
        elif filter_name == "background_removal":
            return self.black_white_converter.remove_background(image, method='simple', tolerance=30)
        else:
            return self.grayscale_converter.convert_manual_loop(image)

    
    def apply_styles(self):
        from gui.styles.app_styles import get_app_styles
        self.setStyleSheet(get_app_styles())