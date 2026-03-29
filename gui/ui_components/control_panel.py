from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import qtawesome as qta
import matplotlib
matplotlib.use('Qt5Agg')                 # Set backend before importing pyplot
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
        self.r_hist = None
        self.g_hist = None
        self.b_hist = None
        self.lines = {}

    def set_histograms(self, r_hist, g_hist, b_hist):
        """Update the plot with new histograms."""
        self.r_hist = r_hist
        self.g_hist = g_hist
        self.b_hist = b_hist
        self.axes.clear()
        self.axes.set_facecolor('#1F2937')
        self.axes.tick_params(colors='white')
        self.axes.set_xlabel('Pixel Intensity', color='white')
        self.axes.set_ylabel('Frequency', color='white')
        self.axes.grid(True, linestyle='--', alpha=0.5, color='gray')

        x = np.arange(256)
        # Plot with semi-transparency
        self.axes.fill_between(x, 0, r_hist, color='red', alpha=0.4, label='Red')
        self.axes.fill_between(x, 0, g_hist, color='green', alpha=0.4, label='Green')
        self.axes.fill_between(x, 0, b_hist, color='blue', alpha=0.4, label='Blue')
        self.axes.legend(loc='upper right', facecolor='#1F2937', edgecolor='white', labelcolor='white')
        self.axes.set_xlim(0, 255)
        self.draw()

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

    # Grayscale description page
    grayscale_page = QWidget()
    grayscale_layout = QVBoxLayout(grayscale_page)
    grayscale_layout.addWidget(QLabel("Convert image to grayscale using the luminosity method."))
    grayscale_layout.addStretch()
    stacked_widget.addWidget(grayscale_page)

    # Black & White description page
    bw_page = QWidget()
    bw_layout = QVBoxLayout(bw_page)
    bw_layout.addWidget(QLabel("Apply a threshold to create a binary black and white image.\nAdjust the threshold using the slider in the original image panel."))
    bw_layout.addStretch()
    stacked_widget.addWidget(bw_page)

    # Background Removal description page
    bg_page = QWidget()
    bg_layout = QVBoxLayout(bg_page)
    bg_layout.addWidget(QLabel("Remove background using color detection. The result will have transparency."))
    bg_layout.addStretch()
    stacked_widget.addWidget(bg_page)

    # Color Filters description page
    color_page = QWidget()
    color_layout = QVBoxLayout(color_page)
    color_layout.addWidget(QLabel("Apply a variety of grayscale‑based colour filters. Choose one from the buttons below."))
    color_layout.addStretch()
    stacked_widget.addWidget(color_page)

    layout.addWidget(stacked_widget)

    # Stacked widget for filter‑specific controls (e.g., buttons)
    controls_stack = QStackedWidget()
    controls_stack.setObjectName("filter-controls")
    # Page 0: empty (for filters without extra controls)
    empty_widget = QWidget()
    controls_stack.addWidget(empty_widget)
    # Page 1: color filter buttons
    color_buttons_widget = create_color_filter_buttons(app_instance)
    controls_stack.addWidget(color_buttons_widget)

    controls_stack.setVisible(False)   # Hide initially (grayscale tab active)
    layout.addWidget(controls_stack)   # (make sure it's added before setVisible)

    # Histogram canvas (matplotlib)
    histogram = HistogramCanvas()
    histogram.setObjectName("histogram-widget")
    layout.addWidget(histogram)

    # Store references in the main app instance
    app_instance.histogram_widget = histogram
    app_instance.filter_stack = stacked_widget
    app_instance.filter_controls_stack = controls_stack

    # Hide the controls stack initially (grayscale tab)
    controls_stack.setVisible(False)

    return widget, (stacked_widget, controls_stack)

def create_color_filter_buttons(app_instance):
    """Create a grid of buttons for the colour filters."""
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