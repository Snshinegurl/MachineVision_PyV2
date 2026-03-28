from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import qtawesome as qta

class HistogramWidget(QWidget):
    """Custom widget to draw RGB histogram."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.setMaximumHeight(200)
        self.r_hist = [0] * 256
        self.g_hist = [0] * 256
        self.b_hist = [0] * 256
        self.max_count = 1  # to avoid division by zero

    def set_histograms(self, r_hist, g_hist, b_hist):
        self.r_hist = r_hist
        self.g_hist = g_hist
        self.b_hist = b_hist
        self.max_count = max(max(r_hist), max(g_hist), max(b_hist)) if any(r_hist) else 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        margin = 20  # top/bottom margin

        # Draw background
        painter.fillRect(0, 0, w, h, QColor(31, 41, 55))  # dark background

        # Draw axes
        painter.setPen(QColor(75, 85, 99))
        painter.drawLine(margin, h - margin, w - margin, h - margin)  # x-axis
        painter.drawLine(margin, margin, margin, h - margin)          # y-axis

        # Draw histograms
        bar_width = (w - 2 * margin) / 256
        if bar_width < 1:
            bar_width = 1

        # Red
        painter.setPen(Qt.red)
        for i, count in enumerate(self.r_hist):
            if count == 0:
                continue
            x = margin + i * bar_width
            bar_height = (count / self.max_count) * (h - 2 * margin)
            painter.fillRect(x, h - margin - bar_height, bar_width, bar_height, QColor(255, 0, 0, 100))

        # Green
        painter.setPen(Qt.green)
        for i, count in enumerate(self.g_hist):
            if count == 0:
                continue
            x = margin + i * bar_width
            bar_height = (count / self.max_count) * (h - 2 * margin)
            painter.fillRect(x, h - margin - bar_height, bar_width, bar_height, QColor(0, 255, 0, 100))

        # Blue
        painter.setPen(Qt.blue)
        for i, count in enumerate(self.b_hist):
            if count == 0:
                continue
            x = margin + i * bar_width
            bar_height = (count / self.max_count) * (h - 2 * margin)
            painter.fillRect(x, h - margin - bar_height, bar_width, bar_height, QColor(0, 0, 255, 100))

        # Draw legend
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 8))
        painter.drawText(10, 20, "Red")
        painter.drawText(50, 20, "Green")
        painter.drawText(100, 20, "Blue")


def create_control_panel(app_instance):
    widget = QWidget()
    widget.setObjectName("control-panel")
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(16)

    header = create_panel_header()
    layout.addWidget(header)

    # Stacked widget for filter‑specific descriptions
    stacked_widget = QStackedWidget()
    stacked_widget.setObjectName("filter-stack")

    # Grayscale page
    grayscale_page = QWidget()
    grayscale_layout = QVBoxLayout(grayscale_page)
    grayscale_layout.addWidget(QLabel("Convert image to grayscale using the luminosity method."))
    grayscale_layout.addStretch()
    stacked_widget.addWidget(grayscale_page)

    # Black & White page
    bw_page = QWidget()
    bw_layout = QVBoxLayout(bw_page)
    bw_layout.addWidget(QLabel("Apply a threshold to create a binary black and white image.\nAdjust the threshold using the slider in the original image panel."))
    bw_layout.addStretch()
    stacked_widget.addWidget(bw_page)

    # Background Removal page
    bg_page = QWidget()
    bg_layout = QVBoxLayout(bg_page)
    bg_layout.addWidget(QLabel("Remove background using color detection. The result will have transparency."))
    bg_layout.addStretch()
    stacked_widget.addWidget(bg_page)

    layout.addWidget(stacked_widget)

    # Histogram widget
    histogram = HistogramWidget()
    histogram.setObjectName("histogram-widget")
    layout.addWidget(histogram)

    app_instance.histogram_widget = histogram
    app_instance.filter_stack = stacked_widget

    return widget, (stacked_widget,)

def create_panel_header():
    header = QWidget()
    header_layout = QVBoxLayout(header)
    header_layout.setContentsMargins(0, 0, 0, 0)
    header_layout.setSpacing(8)

    title = QLabel("Processing Controls")
    title.setObjectName("panel-title")

    subtitle = QLabel("Select a filter tab above to see its description")
    subtitle.setObjectName("panel-subtitle")

    header_layout.addWidget(title)
    header_layout.addWidget(subtitle)

    return header