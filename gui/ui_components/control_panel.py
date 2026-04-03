from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import qtawesome as qta
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from modules.color_filter import ColorFilter

class HistogramCanvas(FigureCanvas):
    """Matplotlib canvas for RGB histograms."""
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 2.5), dpi=100, facecolor='#1F2937')
        super().__init__(self.fig)
        self.setParent(parent)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#1F2937')
        self.axes.tick_params(colors='white')
        self.axes.set_xlabel('Pixel Intensity', color='white')
        self.axes.set_ylabel('Frequency', color='white')
        self.axes.grid(True, linestyle='--', alpha=0.5, color='gray')
        self.fig.tight_layout()

    def set_histograms(self, r_hist, g_hist, b_hist):
        self.axes.clear()
        self.axes.set_facecolor('#1F2937')
        self.axes.tick_params(colors='white')
        self.axes.set_xlabel('Pixel Intensity', color='white')
        self.axes.set_ylabel('Frequency', color='white')
        self.axes.grid(True, linestyle='--', alpha=0.5, color='gray')
        x = np.arange(256)
        self.axes.fill_between(x, 0, r_hist, color='red', alpha=0.4, label='Red')
        self.axes.fill_between(x, 0, g_hist, color='green', alpha=0.4, label='Green')
        self.axes.fill_between(x, 0, b_hist, color='blue', alpha=0.4, label='Blue')
        self.axes.legend(loc='upper right', facecolor='#1F2937', edgecolor='white', labelcolor='white')
        self.axes.set_xlim(0, 255)
        self.draw()

class ProjectionWidget(QWidget):
    """Widget to display horizontal and vertical projection graphs for binary images."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Horizontal projection (row sums)
        self.fig_h = Figure(figsize=(3, 2.5), dpi=100, facecolor='#1F2937')
        self.canvas_h = FigureCanvas(self.fig_h)
        self.ax_h = self.fig_h.add_subplot(111)
        self.ax_h.set_facecolor('#1F2937')
        self.ax_h.tick_params(colors='white')
        self.ax_h.set_xlabel('Row Index', color='white')
        self.ax_h.set_ylabel('White Pixel Count', color='white')
        self.ax_h.set_title('Horizontal Projection', color='white')
        self.ax_h.grid(True, linestyle='--', alpha=0.5, color='gray')

        # Vertical projection (column sums)
        self.fig_v = Figure(figsize=(3, 2.5), dpi=100, facecolor='#1F2937')
        self.canvas_v = FigureCanvas(self.fig_v)
        self.ax_v = self.fig_v.add_subplot(111)
        self.ax_v.set_facecolor('#1F2937')
        self.ax_v.tick_params(colors='white')
        self.ax_v.set_xlabel('Column Index', color='white')
        self.ax_v.set_ylabel('White Pixel Count', color='white')
        self.ax_v.set_title('Vertical Projection', color='white')
        self.ax_v.grid(True, linestyle='--', alpha=0.5, color='gray')

        layout.addWidget(self.canvas_h)
        layout.addWidget(self.canvas_v)

    def update_projections(self, binary_image):
        """
        Compute and display projections from a binary PIL image (mode 'L' or 'RGB' with equal channels).
        binary_image is expected to be a binary image (0 for black, 255 for white).
        """
        if binary_image is None:
            return
        width, height = binary_image.size
        # Convert to grayscale if needed
        if binary_image.mode != 'L':
            gray = binary_image.convert('L')
        else:
            gray = binary_image
        pixels = gray.load()

        # Manual row sums (horizontal projection)
        row_sums = [0] * height
        for y in range(height):
            total = 0
            for x in range(width):
                if pixels[x, y] >= 128:
                    total += 1
            row_sums[y] = total

        # Manual column sums (vertical projection)
        col_sums = [0] * width
        for x in range(width):
            total = 0
            for y in range(height):
                if pixels[x, y] >= 128:
                    total += 1
            col_sums[x] = total

        # Update horizontal graph
        self.ax_h.clear()
        self.ax_h.set_facecolor('#1F2937')
        self.ax_h.tick_params(colors='white')
        self.ax_h.set_xlabel('Row Index', color='white')
        self.ax_h.set_ylabel('White Pixel Count', color='white')
        self.ax_h.set_title('Horizontal Projection', color='white')
        self.ax_h.grid(True, linestyle='--', alpha=0.5, color='gray')
        self.ax_h.bar(range(height), row_sums, color='#4F46E5', alpha=0.7)
        self.ax_h.set_xlim(0, height-1)
        self.canvas_h.draw()

        # Update vertical graph
        self.ax_v.clear()
        self.ax_v.set_facecolor('#1F2937')
        self.ax_v.tick_params(colors='white')
        self.ax_v.set_xlabel('Column Index', color='white')
        self.ax_v.set_ylabel('White Pixel Count', color='white')
        self.ax_v.set_title('Vertical Projection', color='white')
        self.ax_v.grid(True, linestyle='--', alpha=0.5, color='gray')
        self.ax_v.bar(range(width), col_sums, color='#10B981', alpha=0.7)
        self.ax_v.set_xlim(0, width-1)
        self.canvas_v.draw()

def create_control_panel(app_instance):
    widget = QWidget()
    widget.setObjectName("control-panel")
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(16)

    header = create_panel_header()
    layout.addWidget(header)

    # Stacked widget for filter descriptions
    stacked_widget = QStackedWidget()
    stacked_widget.setObjectName("filter-stack")
    # Description pages
    grayscale_page = QWidget()
    grayscale_layout = QVBoxLayout(grayscale_page)
    grayscale_layout.addWidget(QLabel("Convert image to grayscale using the luminosity method."))
    grayscale_layout.addStretch()
    stacked_widget.addWidget(grayscale_page)

    bw_page = QWidget()
    bw_layout = QVBoxLayout(bw_page)
    bw_layout.addWidget(QLabel("Apply a threshold to create a binary black and white image.\nAdjust the threshold using the slider in the original image panel."))
    bw_layout.addStretch()
    stacked_widget.addWidget(bw_page)

    bg_page = QWidget()
    bg_layout = QVBoxLayout(bg_page)
    bg_layout.addWidget(QLabel("Remove background using color detection. The result will have transparency."))
    bg_layout.addStretch()
    stacked_widget.addWidget(bg_page)

    color_page = QWidget()
    color_layout = QVBoxLayout(color_page)
    color_layout.addWidget(QLabel("Apply a variety of grayscale‑based colour filters. Choose one from the buttons below."))
    color_layout.addStretch()
    stacked_widget.addWidget(color_page)

    layout.addWidget(stacked_widget)

    # Stacked widget for filter‑specific controls
    controls_stack = QStackedWidget()
    controls_stack.setObjectName("filter-controls")
    empty_widget = QWidget()
    controls_stack.addWidget(empty_widget)
    color_buttons_widget = create_color_filter_buttons(app_instance)
    controls_stack.addWidget(color_buttons_widget)
    layout.addWidget(controls_stack)

    # Histogram widget
    histogram = HistogramCanvas()
    histogram.setObjectName("histogram-widget")
    layout.addWidget(histogram)

    # Projection widget (always visible, updates automatically)
    projection_widget = ProjectionWidget()
    projection_widget.setObjectName("projection-widget")
    layout.addWidget(projection_widget)

    # Store references
    app_instance.histogram_widget = histogram
    app_instance.filter_stack = stacked_widget
    app_instance.filter_controls_stack = controls_stack
    app_instance.projection_widget = projection_widget

    return widget, (stacked_widget, controls_stack)

def create_color_filter_buttons(app_instance):
    widget = QWidget()
    layout = QGridLayout(widget)
    layout.setSpacing(10)
    layout.setContentsMargins(0, 10, 0, 0)

    filters = [
        ("Blue Ocean", ColorFilter.blue_ocean),
        ("Green Forest", ColorFilter.green_forest),
        ("Red Sunset", ColorFilter.red_sunset),
        ("Purple Night", ColorFilter.purple_night),
        ("Gold Metal", ColorFilter.gold_metal),
        ("Pink Candy", ColorFilter.pink_candy),
        ("Cyan Water", ColorFilter.cyan_water),
        ("Autumn Leaves", ColorFilter.autumn_leaves),
        ("Neon Glow", ColorFilter.neon_glow),
        ("Heatmap", ColorFilter.heatmap),
        ("Rainbow", ColorFilter.rainbow),
        ("Vintage Paper", ColorFilter.vintage_paper),
        ("Electric Blue", ColorFilter.electric_blue),
        ("Sunset Gradient", ColorFilter.sunset_gradient),
        ("Forest Canopy", ColorFilter.forest_canopy)
    ]
    row, col = 0, 0
    for name, func in filters:
        btn = QPushButton(name)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda checked, f=func: app_instance.apply_color_filter(f))
        btn.setToolTip(f"Apply {name} filter")
        layout.addWidget(btn, row, col)
        col += 1
        if col >= 3:
            col = 0
            row += 1
    return widget

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