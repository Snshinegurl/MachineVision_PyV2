#!/usr/bin/env python3
"""
VisionPro AI Image Processing Application
Main entry point
"""

import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import io
import qtawesome as qta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.image_processor import ImageProcessor
from modules.grayscale_converter import GrayscaleConverter
from modules.black_white_converter import BlackWhiteConverter
from modules.pixel_stats import PixelStats
from modules.color_filter import ColorFilter
from modules.rotate_converter import ImageRotator
from modules.mirror_converter import ImageMirror
from modules.translate_converter import ImageTranslator
from modules.object_boxer import ObjectBoxer
from modules.convolution_filters import ConvolutionFilter
from modules.threshold_converter import ThresholdConverter   # NEW

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
        self.image_rotator = ImageRotator()
        self.image_mirror = ImageMirror()
        self.image_translator = ImageTranslator()
        self.object_boxer = ObjectBoxer()
        self.convolution_filter = ConvolutionFilter()
        self.threshold_converter = ThresholdConverter()      # NEW
        self.current_filter = "custom_grayscale"
        self.current_rotation_angle = 0
        self.current_mirror_type = "horizontal"
        self.current_translate_dx = 0
        self.current_translate_dy = 0
        self.current_object_threshold = 128
        self.current_threshold_t1 = 0                       # NEW
        self.current_threshold_t2 = 255                     # NEW
        self.centroid_btn = None
        self.centroid_label = None
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        self.setWindowTitle("CPEP 323A - Advanced Image Processing")
        self.setMinimumSize(1400, 900)
        self.create_scroll_area()
        self.create_main_layout()

    def create_scroll_area(self):
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
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.create_header())
        main_layout.addWidget(self.create_content_widget())

    def create_content_widget(self):
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)
        content_layout.addWidget(self.create_page_header())
        content_layout.addWidget(self.create_status_bar())
        content_layout.addWidget(self.create_file_info_cards())
        from gui.ui_components.header import create_filter_navbar
        filter_navbar = create_filter_navbar(self)
        content_layout.addWidget(filter_navbar)
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
        widget.findChild(QLabel, "page-subtitle").setText("Upload, crop, and apply filters including background removal, rotation, mirroring, translation, object boxing, convolution, and range threshold")
        return widget

    def create_status_bar(self):
        from gui.ui_components.status_bar import create_status_bar
        widget, self.status_value = create_status_bar()
        return widget

    def create_file_info_cards(self):
        from gui.ui_components.info_cards import create_file_info_cards
        widget, cards = create_file_info_cards()
        self.file_name_card, self.file_size_card, self.dimensions_card, self.pixels_card, self.format_card, self.object_area_card = cards
        return widget

    def create_image_processing_section(self):
        from gui.ui_components.image_section import create_image_processing_section
        widget, components = create_image_processing_section(self)
        (
            self.original_placeholder, self.original_image_label,
            self.processed_placeholder, self.processed_image_label,
            self.processed_status, self.save_btn, self.crop_btn, self.process_btn,
            self.bw_threshold_widget, self.rotation_widget, self.mirror_widget,
            self.translation_widget, self.object_boxing_widget, self.range_threshold_widget   # NEW
        ) = components
        self.add_crop_confirmation_controls(widget)
        self.original_image_label.installEventFilter(self)
        return widget

    def add_crop_confirmation_controls(self, parent_widget):
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

    def update_binary_projections(self):
        source_image = self.cropped_image if self.crop_applied and self.cropped_image else self.original_image
        if source_image is None:
            return
        threshold = getattr(self, 'bw_threshold_slider', None)
        thresh_val = threshold.value() if threshold else 128
        binary_img = self.black_white_converter.convert_to_black_white(source_image, threshold=thresh_val)
        if binary_img and hasattr(self, 'projection_widget'):
            self.projection_widget.update_projections(binary_img)

    def create_control_panel(self):
        from gui.ui_components.control_panel import create_control_panel
        widget, components = create_control_panel(self)
        self.filter_stack = components[0]  # will be None
        self.filter_controls_stack = components[1]
        self.filter_controls_stack.setVisible(False)  
        return widget

    def get_scrollbar_style(self):
        return """
            QScrollArea { border: none; background-color: #111827; }
            QScrollBar:vertical { border: none; background-color: #1F2937; width: 10px; border-radius: 5px; }
            QScrollBar::handle:vertical { background-color: #4F46E5; border-radius: 5px; min-height: 20px; }
            QScrollBar::handle:vertical:hover { background-color: #4338CA; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; height: 0px; }
            QLabel { padding: 2px 4px; border-radius: 5px; }
            #crop-btn { background-color: #F59E0B; color: white; border: none; border-radius: 6px; padding: 8px 16px; font-weight: 600; font-size: 13px; }
            #crop-btn:hover:enabled { background-color: #D97706; transform: translateY(-1px); }
            #crop-btn:disabled { opacity: 0.5; cursor: not-allowed; }
            #apply-crop-btn { background-color: #10B981; color: white; border: none; border-radius: 6px; padding: 8px 16px; font-weight: 600; font-size: 13px; }
            #apply-crop-btn:hover:enabled { background-color: #0DA271; transform: translateY(-1px); }
            #apply-crop-btn:disabled { opacity: 0.5; cursor: not-allowed; }
            #cancel-crop-btn { background-color: #EF4444; color: white; border: none; border-radius: 6px; padding: 8px 16px; font-weight: 600; font-size: 13px; }
            #cancel-crop-btn:hover:enabled { background-color: #DC2626; transform: translateY(-1px); }
            #crop-confirmation { background-color: rgba(31, 41, 55, 0.5); border-radius: 8px; margin: 10px 20px; }
            #centroid-btn { background-color: #8B5CF6; color: white; border: none; border-radius: 8px; padding: 10px 20px; font-weight: 600; font-size: 14px; margin-top: 8px; }
            #centroid-btn:hover:enabled { background-color: #7C3AED; transform: translateY(-2px); }
            #centroid-btn:disabled { opacity: 0.5; cursor: not-allowed; }
            #centroid-value { font-size: 14px; font-family: monospace; color: #10B981; }
        """

    def on_filter_tab_changed(self, index):
        filter_map = {
            0: "custom_grayscale",
            1: "custom_bw",
            2: "background_removal",
            3: "color_filter",
            4: "rotate",
            5: "mirror",
            6: "translate",
            7: "object_boxing",
            8: "convolution",
            9: "threshold"                # NEW
        }
        self.current_filter = filter_map.get(index, "custom_grayscale")

        # Show/hide specific control widgets in the original image panel
        if hasattr(self, 'bw_threshold_widget'):
            self.bw_threshold_widget.setVisible(self.current_filter == "custom_bw")
        if hasattr(self, 'rotation_widget'):
            self.rotation_widget.setVisible(self.current_filter == "rotate")
        if hasattr(self, 'mirror_widget'):
            self.mirror_widget.setVisible(self.current_filter == "mirror")
        if hasattr(self, 'translation_widget'):
            self.translation_widget.setVisible(self.current_filter == "translate")
        if hasattr(self, 'object_boxing_widget'):
            self.object_boxing_widget.setVisible(self.current_filter == "object_boxing")
        if hasattr(self, 'range_threshold_widget'):          # NEW
            self.range_threshold_widget.setVisible(self.current_filter == "threshold")

        # Show/hide the controls stack (color filter buttons / convolution panel)
        if hasattr(self, 'filter_controls_stack'):
            if index == 3:                      # Color Filters tab
                self.filter_controls_stack.setCurrentIndex(1)
                self.filter_controls_stack.setVisible(True)
            elif index == 8:                    # Convolution tab
                self.filter_controls_stack.setCurrentIndex(2)
                self.filter_controls_stack.setVisible(True)
            else:
                self.filter_controls_stack.setVisible(False)

        # Enable/disable process button (disabled for color filters because they use apply_color_filter)
        if hasattr(self, 'process_btn'):
            self.process_btn.setEnabled(index != 3)

    def on_threshold_changed(self, value):
        if hasattr(self, 'bw_threshold_value_label'):
            self.bw_threshold_value_label.setText(str(value))
        self.black_white_converter.threshold = value
        self.update_binary_projections()

    def on_rotation_changed(self, value):
        self.current_rotation_angle = value
        if hasattr(self, 'rotation_value_label'):
            self.rotation_value_label.setText(f"{value}°")

    def on_mirror_direction_changed(self):
        if hasattr(self, 'mirror_horizontal_radio') and hasattr(self, 'mirror_vertical_radio'):
            if self.mirror_horizontal_radio.isChecked():
                self.current_mirror_type = "horizontal"
            else:
                self.current_mirror_type = "vertical"

    def on_translation_changed(self):
        if hasattr(self, 'translate_dx_spin') and hasattr(self, 'translate_dy_spin'):
            self.current_translate_dx = self.translate_dx_spin.value()
            self.current_translate_dy = self.translate_dy_spin.value()

    def on_object_threshold_changed(self, value):
        self.current_object_threshold = value
        if hasattr(self, 'object_threshold_value_label'):
            self.object_threshold_value_label.setText(str(value))

    # NEW: Range threshold callback
    def on_range_threshold_changed(self):
        if hasattr(self, 'range_threshold_t1_spin') and hasattr(self, 'range_threshold_t2_spin'):
            self.current_threshold_t1 = self.range_threshold_t1_spin.value()
            self.current_threshold_t2 = self.range_threshold_t2_spin.value()

    # ------------------------------------------------------------
    # Convolution helper
    # ------------------------------------------------------------
    def get_current_convolution_kernel(self):
        """Retrieve the selected kernel from the convolution controls."""
        if not hasattr(self, 'conv_controls'):
            return None
        preset = self.conv_controls.preset_combo.currentText()
        if preset == "Custom kernel":
            kernel = self.conv_controls.get_custom_kernel()
            if kernel is None:
                QMessageBox.warning(self, "Invalid Kernel", "Please enter numeric values for all kernel entries.")
                return None
            return kernel
        # Built‑in presets
        if preset == "Smoothing (Average)":
            return ConvolutionFilter.get_smoothing_kernel(3)
        elif preset == "Gaussian Blur":
            return ConvolutionFilter.get_gaussian_kernel(3, sigma=1.0)
        elif preset == "Sharpening":
            return ConvolutionFilter.get_sharpening_kernel()
        elif preset == "Mean Removal (High-pass)":
            return ConvolutionFilter.get_mean_removal_kernel()
        elif preset == "Emboss":
            return ConvolutionFilter.get_emboss_kernel()
        else:
            return None

    def update_object_area(self, pil_image, filter_name):
        if pil_image is None:
            return
        total_pixels = pil_image.width * pil_image.height
        area = total_pixels
        if filter_name == "background_removal":
            stats = self.black_white_converter.get_background_removal_stats()
            if stats and 'opaque_pixels' in stats:
                area = stats['opaque_pixels']
        elif filter_name == "object_boxing":
            area = self.object_boxer.object_area
        if hasattr(self, 'object_area_card'):
            self.object_area_card.findChild(QLabel, "card-value").setText(f"{area:,}")

    # ------------------------------------------------------------
    # Centroid display
    # ------------------------------------------------------------
    def show_centroids(self):
        if self.processed_image is None:
            QMessageBox.warning(self, "Warning", "No processed image available. Please process an image first.")
            return

        img = self.processed_image.copy()
        width, height = img.size
        img_cx = width / 2.0
        img_cy = height / 2.0

        # If we are in object boxing mode and have detected objects
        if self.current_filter == "object_boxing" and hasattr(self.object_boxer, 'objects') and self.object_boxer.objects:
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            marker_size = 8
            line_width = 2

            # Draw image centroid (red)
            draw.line([(img_cx - marker_size, img_cy), (img_cx + marker_size, img_cy)], fill='red', width=line_width)
            draw.line([(img_cx, img_cy - marker_size), (img_cx, img_cy + marker_size)], fill='red', width=line_width)

            # Draw centroids for each object (green)
            coord_msgs = []
            for i, obj in enumerate(self.object_boxer.objects):
                cx, cy = obj['centroid']
                draw.line([(cx - marker_size, cy), (cx + marker_size, cy)], fill='lime', width=line_width)
                draw.line([(cx, cy - marker_size), (cx, cy + marker_size)], fill='lime', width=line_width)
                draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill='lime')
                coord_msgs.append(f"Object {i+1}: ({cx:.1f}, {cy:.1f})")

            # Update displayed image
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='PNG')
            pixmap = QPixmap()
            pixmap.loadFromData(byte_arr.getvalue())
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.processed_image_label.setPixmap(scaled_pixmap)

            msg = f"Image Centroid: ({img_cx:.1f}, {img_cy:.1f})\n\nDetected Objects: {len(self.object_boxer.objects)}\n" + "\n".join(coord_msgs)
            if self.centroid_label:
                self.centroid_label.setText(msg.replace('\n', '; ')[:100])
            QMessageBox.information(self, "Centroid Coordinates", msg)
        else:
            # Fallback for other filters (e.g., background removal, grayscale, etc.)
            obj_cx, obj_cy = img_cx, img_cy
            has_object = False
            if img.mode == 'RGBA':
                pixels = img.load()
                total_mass = 0
                sum_x = 0.0
                sum_y = 0.0
                for y in range(height):
                    for x in range(width):
                        alpha = pixels[x, y][3]
                        if alpha > 0:
                            total_mass += 1
                            sum_x += x
                            sum_y += y
                if total_mass > 0:
                    obj_cx = sum_x / total_mass
                    obj_cy = sum_y / total_mass
                    has_object = True

            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            marker_size = 15
            line_width = 2
            draw.line([(img_cx - marker_size, img_cy), (img_cx + marker_size, img_cy)], fill='red', width=line_width)
            draw.line([(img_cx, img_cy - marker_size), (img_cx, img_cy + marker_size)], fill='red', width=line_width)
            if has_object:
                draw.line([(obj_cx - marker_size, obj_cy), (obj_cx + marker_size, obj_cy)], fill='lime', width=line_width)
                draw.line([(obj_cx, obj_cy - marker_size), (obj_cx, obj_cy + marker_size)], fill='lime', width=line_width)

            byte_arr = io.BytesIO()
            img.save(byte_arr, format='PNG')
            pixmap = QPixmap()
            pixmap.loadFromData(byte_arr.getvalue())
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.processed_image_label.setPixmap(scaled_pixmap)

            coord_msg = f"Image Centroid: ({img_cx:.1f}, {img_cy:.1f})"
            if has_object:
                coord_msg += f"\nObject Centroid: ({obj_cx:.1f}, {obj_cy:.1f})"
            else:
                coord_msg += "\nObject Centroid: Not available (no segmented object)"
            if self.centroid_label:
                self.centroid_label.setText(coord_msg.replace('\n', '; '))
            QMessageBox.information(self, "Centroid Coordinates", coord_msg)

    # ------------------------------------------------------------
    # Event filter for cropping
    # ------------------------------------------------------------
    def eventFilter(self, obj, event):
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
                    corners = [self.crop_rect.topLeft(), self.crop_rect.topRight(),
                               self.crop_rect.bottomLeft(), self.crop_rect.bottomRight()]
                    painter.setBrush(QBrush(QColor(79, 70, 229)))
                    painter.setPen(Qt.NoPen)
                    for corner in corners:
                        painter.drawRect(corner.x() - marker_size//2, corner.y() - marker_size//2,
                                         marker_size, marker_size)
                    return True
        return super().eventFilter(obj, event)

    def start_cropping(self):
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
        if not self.original_image or self.crop_rect.isNull():
            return None
        pixmap = self.original_image_label.pixmap()
        if not pixmap:
            return None
        pixmap_size = pixmap.size()
        label_size = self.original_image_label.size()
        offset_x = (label_size.width() - pixmap_size.width()) // 2
        offset_y = (label_size.height() - pixmap_size.height()) // 2
        adjusted_rect = QRect(self.crop_rect.x() - offset_x, self.crop_rect.y() - offset_y,
                              self.crop_rect.width(), self.crop_rect.height())
        adjusted_rect = adjusted_rect.intersected(QRect(0, 0, pixmap_size.width(), pixmap_size.height()))
        original_width, original_height = self.original_image.size
        scale_x = original_width / pixmap_size.width()
        scale_y = original_height / pixmap_size.height()
        scaled_rect = QRect(int(adjusted_rect.x() * scale_x), int(adjusted_rect.y() * scale_y),
                            int(adjusted_rect.width() * scale_x), int(adjusted_rect.height() * scale_y))
        scaled_rect = scaled_rect.intersected(QRect(0, 0, original_width, original_height))
        return scaled_rect

    def apply_crop(self):
        if not self.original_image or self.crop_rect.isNull():
            return
        scaled_rect = self.calculate_scaled_crop_rect()
        if not scaled_rect or scaled_rect.width() < 10 or scaled_rect.height() < 10:
            QMessageBox.warning(self, "Warning", "Invalid crop area! Please select a larger area.")
            return
        cropped_pil = self.original_image.crop((scaled_rect.x(), scaled_rect.y(),
                                                scaled_rect.x() + scaled_rect.width(),
                                                scaled_rect.y() + scaled_rect.height()))
        self.cropped_image = cropped_pil
        self.crop_applied = True
        byte_arr = io.BytesIO()
        cropped_pil.save(byte_arr, format='PNG')
        pixmap = QPixmap()
        pixmap.loadFromData(byte_arr.getvalue())
        scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.original_image_label.setPixmap(scaled_pixmap)
        self.processed_image_label.setPixmap(scaled_pixmap)
        self.processed_placeholder.hide()
        self.processed_image_label.show()
        self.processed_image = None
        self.processed_status.setText("Cropped")
        self.processed_status.setObjectName("status-badge-pending")
        self.save_btn.setEnabled(False)
        self.process_btn.setEnabled(True)
        self.update_histogram(cropped_pil)
        self.update_image_info_after_crop(cropped_pil)
        self.cancel_cropping()
        self.update_binary_projections()
        QMessageBox.information(self, "Success",
            f"Image cropped to {scaled_rect.width()} x {scaled_rect.height()} pixels\n"
            f"The cropped image is now ready for processing.")

    def cancel_cropping(self):
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
        width, height = cropped_image.size
        total_pixels = width * height
        self.dimensions_card.findChild(QLabel, "card-value").setText(f"{width} × {height}")
        self.pixels_card.findChild(QLabel, "card-value").setText(f"{total_pixels:,}")
        current_name = self.file_name_card.findChild(QLabel, "card-value").text()
        if not current_name.endswith(" (cropped)"):
            self.file_name_card.findChild(QLabel, "card-value").setText(f"{current_name} (cropped)")

    def upload_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp)")
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
                self.processed_image_label.setPixmap(scaled_pixmap)
                self.processed_placeholder.hide()
                self.processed_image_label.show()
                self.processed_status.setText("Original")
                self.processed_status.setObjectName("status-badge-pending")
                self.save_btn.setEnabled(False)
                self.process_btn.setEnabled(True)
                if self.centroid_btn:
                    self.centroid_btn.setEnabled(False)
                if self.centroid_label:
                    self.centroid_label.setText("Not computed")
                self.update_histogram(self.original_image)
                self.update_info_cards(image_info)
                self.status_value.setText("Image Uploaded")
                self.status_value.setObjectName("status-value-uploaded")
                self.update_binary_projections()
                self.apply_styles()
                self.crop_btn.setEnabled(True)
                if self.is_cropping:
                    self.cancel_cropping()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")

    def update_info_cards(self, image_info):
        from gui.ui_components.info_cards import update_info_cards
        update_info_cards(image_info, self.file_name_card, self.file_size_card,
                          self.dimensions_card, self.pixels_card, self.format_card,
                          self.object_area_card)

    def apply_color_filter(self, filter_func):
        image_to_process = self.cropped_image if self.crop_applied and self.cropped_image else self.original_image
        if not image_to_process:
            QMessageBox.warning(self, "Warning", "Please upload an image first!")
            return
        grayscale_img = self.grayscale_converter.convert_to_grayscale(image_to_process)
        if not grayscale_img:
            QMessageBox.warning(self, "Warning", "Failed to convert to grayscale.")
            return
        try:
            processed = filter_func(grayscale_img)
            self.processed_image = processed
            byte_arr = io.BytesIO()
            processed.save(byte_arr, format='PNG')
            pixmap = QPixmap()
            pixmap.loadFromData(byte_arr.getvalue())
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.processed_image_label.setPixmap(scaled_pixmap)
            self.processed_placeholder.hide()
            self.processed_image_label.show()
            self.processed_status.setText("Color Filter")
            self.processed_status.setObjectName("status-badge-ready")
            self.save_btn.setEnabled(True)
            self.update_histogram(processed)
            self.update_object_area(processed, "color_filter")
            if self.centroid_btn:
                self.centroid_btn.setEnabled(True)
            if self.centroid_label:
                self.centroid_label.setText("Click 'Show Centroid' to compute")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply filter: {str(e)}")

    def process_image(self):
        image_to_process = self.cropped_image if self.crop_applied and self.cropped_image else self.original_image
        if not image_to_process:
            QMessageBox.warning(self, "Warning", "Please upload an image first!")
            return
        self.status_value.setText("Processing...")
        self.status_value.setObjectName("status-value-processing")
        self.processed_status.setText("Processing")
        self.processed_status.setObjectName("status-badge-processing")
        self.process_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.apply_styles()
        QApplication.processEvents()
        try:
            processed = self.apply_filter(image_to_process, self.current_filter)
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
            self.process_btn.setEnabled(True)
            self.update_histogram(processed)
            self.update_object_area(processed, self.current_filter)
            if self.centroid_btn:
                self.centroid_btn.setEnabled(True)
            if self.centroid_label:
                self.centroid_label.setText("Click 'Show Centroid' to compute")
            crop_info = " (cropped)" if self.crop_applied else ""
            if self.current_filter == "custom_bw":
                threshold = self.bw_threshold_slider.value()
                QMessageBox.information(self, "Success",
                    f"Image{crop_info} processed successfully using Black & White filter!\nThreshold: {threshold}")
            elif self.current_filter == "background_removal":
                QMessageBox.information(self, "Success",
                    f"Background removed successfully{crop_info}! The image now has transparency.")
            elif self.current_filter == "rotate":
                angle = self.current_rotation_angle
                QMessageBox.information(self, "Success",
                    f"Image{crop_info} rotated successfully by {angle}°!")
            elif self.current_filter == "mirror":
                direction = "horizontally" if self.current_mirror_type == "horizontal" else "vertically"
                QMessageBox.information(self, "Success",
                    f"Image{crop_info} mirrored {direction} successfully!")
            elif self.current_filter == "translate":
                dx = self.current_translate_dx
                dy = self.current_translate_dy
                QMessageBox.information(self, "Success",
                    f"Image{crop_info} translated by ({dx}, {dy}) pixels!")
            elif self.current_filter == "object_boxing":
                threshold = self.current_object_threshold
                QMessageBox.information(self, "Success",
                    f"Objects detected and boxed successfully!\nDetection threshold: {threshold}\nBackground set to gray.")
            elif self.current_filter == "convolution":
                filter_name = self.conv_controls.preset_combo.currentText() if hasattr(self, 'conv_controls') else "Convolution"
                QMessageBox.information(self, "Success",
                    f"Image{crop_info} processed with {filter_name} filter.")
            elif self.current_filter == "threshold":                              # NEW
                t1 = self.current_threshold_t1
                t2 = self.current_threshold_t2
                QMessageBox.information(self, "Success",
                    f"Image{crop_info} thresholded using range [{t1}, {t2}]!")
            else:
                QMessageBox.information(self, "Success",
                    f"Image{crop_info} processed successfully using Grayscale filter!")
        except Exception as e:
            self.status_value.setText("Processing Failed")
            self.status_value.setObjectName("status-value-ready")
            self.processed_status.setText("Failed")
            self.processed_status.setObjectName("status-badge-pending")
            self.save_btn.setEnabled(False)
            self.process_btn.setEnabled(True)
            QMessageBox.critical(self, "Error", f"Failed to process image: {str(e)}")
        self.apply_styles()

    def save_processed_image(self):
        if not self.processed_image:
            QMessageBox.warning(self, "Warning", "No processed image to save!")
            return
        file_dialog = QFileDialog()
        if self.current_filter in ("background_removal", "object_boxing"):
            file_path, _ = file_dialog.getSaveFileName(self, "Save Processed Image", "",
                "PNG Image (*.png);;All Files (*)")
            if file_path and not file_path.lower().endswith('.png'):
                file_path += '.png'
            format = 'PNG'
        else:
            file_path, _ = file_dialog.getSaveFileName(self, "Save Processed Image", "",
                "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;BMP Image (*.bmp);;TIFF Image (*.tiff);;All Files (*)")
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
        if filter_name == "custom_grayscale":
            return self.grayscale_converter.convert_to_grayscale(image)
        elif filter_name == "custom_bw":
            threshold = self.bw_threshold_slider.value()
            return self.black_white_converter.convert_to_black_white(image, threshold=threshold)
        elif filter_name == "background_removal":
            return self.black_white_converter.remove_background(image, method='otsu')
        elif filter_name == "rotate":
            angle = self.current_rotation_angle
            return self.image_rotator.rotate_image(image, angle)
        elif filter_name == "mirror":
            return self.image_mirror.mirror(image, self.current_mirror_type)
        elif filter_name == "translate":
            return self.image_translator.translate_image(image, self.current_translate_dx, self.current_translate_dy)
        elif filter_name == "object_boxing":
            img, area = self.object_boxer.box_objects(image, threshold=self.current_object_threshold, include_full_image=True)
            self.object_boxer.object_area = area
            return img
        elif filter_name == "convolution":
            kernel = self.get_current_convolution_kernel()
            if kernel is None:
                raise Exception("No valid convolution kernel selected or provided.")
            return self.convolution_filter.apply_convolution(image, kernel, kernel_size=3)
        elif filter_name == "threshold":                                         # NEW
            return self.threshold_converter.apply_range_threshold(image, self.current_threshold_t1, self.current_threshold_t2)
        else:
            return self.grayscale_converter.convert_manual_loop(image)

    def apply_styles(self):
        from gui.styles.app_styles import get_app_styles
        self.setStyleSheet(get_app_styles())

    def update_histogram(self, pil_image):
        if pil_image is None:
            return
        r_hist, g_hist, b_hist = PixelStats.get_rgb_histograms(pil_image)
        if hasattr(self, 'histogram_widget'):
            self.histogram_widget.set_histograms(r_hist, g_hist, b_hist)