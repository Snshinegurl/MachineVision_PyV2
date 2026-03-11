from PySide6.QtCore import QRect, QPoint, Qt
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PIL import Image
from modules.pixel_stats import PixelStats   # new impor

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
        return image.crop((
            crop_rect.x(),
            crop_rect.y(),
            crop_rect.x() + crop_rect.width(),
            crop_rect.y() + crop_rect.height()
        ))
    
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