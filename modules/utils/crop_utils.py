from PySide6.QtCore import QRect, QPoint, Qt
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PIL import Image
from modules.pixel_processor import get_image_info   # use the module

class CropUtils:
    @staticmethod
    def validate_crop_rect(rect, image_size):
        if rect.isNull():
            return False
        if rect.width() < 10 or rect.height() < 10:
            return False
        if (rect.x() < 0 or rect.y() < 0 or 
            rect.right() > image_size.width() or 
            rect.bottom() > image_size.height()):
            return False
        return True
    
    @staticmethod
    def scale_crop_rect(rect, label_size, pixmap_size):
        scale_x = pixmap_size.width() / label_size.width()
        scale_y = pixmap_size.height() / label_size.height()
        scaled_rect = QRect(
            int(rect.x() * scale_x),
            int(rect.y() * scale_y),
            int(rect.width() * scale_x),
            int(rect.height() * scale_y)
        )
        return scaled_rect
    
    @staticmethod
    def apply_crop_to_image(image, crop_rect):
        """
        Crop the image using manual pixel copying (no PIL crop).
        Uses pixel_processor.get_image_info to get dimensions.
        """
        # Get image info using pixel_processor module
        width, height, channels, total_pixels, mode = get_image_info(image)
        
        # Ensure the crop rectangle is within bounds
        x1 = max(0, crop_rect.x())
        y1 = max(0, crop_rect.y())
        x2 = min(width, crop_rect.x() + crop_rect.width())
        y2 = min(height, crop_rect.y() + crop_rect.height())
        if x2 <= x1 or y2 <= y1:
            raise ValueError("Invalid crop rectangle")
        
        new_width = x2 - x1
        new_height = y2 - y1
        
        # Determine output mode (keep same as input)
        output_mode = image.mode
        
        # Create a new PIL image of the cropped size
        cropped = Image.new(output_mode, (new_width, new_height))
        src_pixels = image.load()
        dst_pixels = cropped.load()
        
        # Manual pixel copying (algorithmic loop)
        for y in range(new_height):
            for x in range(new_width):
                dst_pixels[x, y] = src_pixels[x1 + x, y1 + y]
        
        return cropped
    
    @staticmethod
    def draw_crop_rectangle(painter, rect):
        painter.setPen(QPen(QColor(79, 70, 229), 2, Qt.DashLine))
        painter.setBrush(QBrush(QColor(79, 70, 229, 30)))
        painter.drawRect(rect)
        
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        size_text = f"{rect.width()} x {rect.height()}"
        painter.drawText(rect.bottomRight() + QPoint(5, 15), size_text)
        
        marker_size = 8
        corners = [
            rect.topLeft(),
            rect.topRight(),
            rect.bottomLeft(),
            rect.bottomRight()
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