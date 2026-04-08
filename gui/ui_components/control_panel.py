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
from modules.convolution_filters import ConvolutionFilter

# ---------- Histogram Canvas ----------
class HistogramCanvas(FigureCanvas):
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

# ---------- Projection Widget (horizontal bars for row sums, vertical bars for col sums) ----------
class ProjectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Single figure with two subplots
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor='#1F2937')
        self.canvas = FigureCanvas(self.fig)

        # Top subplot: horizontal projection as HORIZONTAL bars (row index on Y, count on X)
        self.ax_h = self.fig.add_subplot(2, 1, 1)
        self.ax_h.set_facecolor('#1F2937')
        self.ax_h.tick_params(colors='white')
        self.ax_h.set_xlabel('White Pixel Count', color='white')
        self.ax_h.set_ylabel('Row Index', color='white')
        self.ax_h.set_title('Horizontal Projection (Row Sums)', color='white')
        self.ax_h.grid(True, linestyle='--', alpha=0.5, color='gray', axis='x')

        # Bottom subplot: vertical projection as VERTICAL bars (column index on X, count on Y)
        self.ax_v = self.fig.add_subplot(2, 1, 2)
        self.ax_v.set_facecolor('#1F2937')
        self.ax_v.tick_params(colors='white')
        self.ax_v.set_xlabel('Column Index', color='white')
        self.ax_v.set_ylabel('White Pixel Count', color='white')
        self.ax_v.set_title('Vertical Projection (Column Sums)', color='white')
        self.ax_v.grid(True, linestyle='--', alpha=0.5, color='gray', axis='y')

        self.fig.tight_layout()
        layout.addWidget(self.canvas)

    def update_projections(self, binary_image):
        if binary_image is None:
            return
        width, height = binary_image.size
        if binary_image.mode != 'L':
            gray = binary_image.convert('L')
        else:
            gray = binary_image
        pixels = gray.load()

        # Row sums (horizontal projection)
        row_sums = [0] * height
        for y in range(height):
            total = 0
            for x in range(width):
                if pixels[x, y] >= 128:
                    total += 1
            row_sums[y] = total

        # Column sums (vertical projection)
        col_sums = [0] * width
        for x in range(width):
            total = 0
            for y in range(height):
                if pixels[x, y] >= 128:
                    total += 1
            col_sums[x] = total

        # ----- Update horizontal projection (HORIZONTAL bars) -----
        self.ax_h.clear()
        self.ax_h.set_facecolor('#1F2937')
        self.ax_h.tick_params(colors='white')
        self.ax_h.set_xlabel('White Pixel Count', color='white')
        self.ax_h.set_ylabel('Row Index', color='white')
        self.ax_h.set_title('Horizontal Projection (Row Sums)', color='white')
        self.ax_h.grid(True, linestyle='--', alpha=0.5, color='gray', axis='x')
        # Use barh for horizontal bars: y = row indices, width = row_sums
        rows = np.arange(height)
        self.ax_h.barh(rows, row_sums, color='#4F46E5', alpha=0.7)
        self.ax_h.set_ylim(height - 0.5, -0.5)  # invert so row 0 is at top (optional)
        self.ax_h.set_xlim(0, max(row_sums) if row_sums else 1)

        # ----- Update vertical projection (VERTICAL bars) -----
        self.ax_v.clear()
        self.ax_v.set_facecolor('#1F2937')
        self.ax_v.tick_params(colors='white')
        self.ax_v.set_xlabel('Column Index', color='white')
        self.ax_v.set_ylabel('White Pixel Count', color='white')
        self.ax_v.set_title('Vertical Projection (Column Sums)', color='white')
        self.ax_v.grid(True, linestyle='--', alpha=0.5, color='gray', axis='y')
        cols = np.arange(width)
        self.ax_v.bar(cols, col_sums, color='#10B981', alpha=0.7)
        self.ax_v.set_xlim(-0.5, width - 0.5)
        self.ax_v.set_ylim(0, max(col_sums) if col_sums else 1)

        self.canvas.draw()

# ---------- Convolution Controls ----------
class ConvolutionControls(QWidget):
    def __init__(self, app_instance, parent=None):
        super().__init__(parent)
        self.app = app_instance
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        preset_label = QLabel("FILTER PRESET")
        preset_label.setObjectName("panel-subtitle")
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Smoothing (Average)",
            "Gaussian Blur",
            "Sharpening",
            "Mean Removal (High-pass)",
            "Emboss",
            "Custom kernel"
        ])
        self.preset_combo.currentTextChanged.connect(self.on_preset_changed)
        layout.addWidget(preset_label)
        layout.addWidget(self.preset_combo)

        self.kernel_group = QGroupBox("KERNEL VALUES (3×3)")
        kernel_layout = QGridLayout(self.kernel_group)
        kernel_layout.setSpacing(8)
        self.kernel_entries = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                entry = QLineEdit()
                entry.setAlignment(Qt.AlignRight)
                entry.setText("0.0")
                entry.setFixedWidth(80)
                kernel_layout.addWidget(entry, i, j)
                self.kernel_entries[i][j] = entry

        # Kernel sum display
        sum_layout = QHBoxLayout()
        sum_layout.addStretch()
        sum_label = QLabel("Kernel sum:")
        sum_label.setObjectName("threshold-label")
        self.kernel_sum_value = QLabel("0.0000")
        self.kernel_sum_value.setObjectName("centroid-value")
        sum_layout.addWidget(sum_label)
        sum_layout.addWidget(self.kernel_sum_value)
        sum_layout.addStretch()
        layout.addLayout(sum_layout)

        # Connect signals
        for i in range(3):
            for j in range(3):
                self.kernel_entries[i][j].textChanged.connect(self.update_kernel_sum)

        # Default identity kernel
        self.kernel_entries[0][0].setText("0.0")
        self.kernel_entries[0][1].setText("0.0")
        self.kernel_entries[0][2].setText("0.0")
        self.kernel_entries[1][0].setText("0.0")
        self.kernel_entries[1][1].setText("1.0")
        self.kernel_entries[1][2].setText("0.0")
        self.kernel_entries[2][0].setText("0.0")
        self.kernel_entries[2][1].setText("0.0")
        self.kernel_entries[2][2].setText("0.0")

        layout.addWidget(self.kernel_group)
        self.kernel_group.setEnabled(False)
        app_instance.conv_controls = self

    def on_preset_changed(self, text):
        is_custom = (text == "Custom kernel")
        self.kernel_group.setEnabled(is_custom)
        if not is_custom:
            kernel = self.get_preset_kernel(text)
            if kernel:
                for i in range(3):
                    for j in range(3):
                        self.kernel_entries[i][j].setText(f"{kernel[i][j]:.6f}")
                for row in self.kernel_entries:
                    for entry in row:
                        entry.setReadOnly(True)
            else:
                for i in range(3):
                    for j in range(3):
                        self.kernel_entries[i][j].setText("0.0")
                self.kernel_entries[1][1].setText("1.0")
                for row in self.kernel_entries:
                    for entry in row:
                        entry.setReadOnly(True)
        else:
            for row in self.kernel_entries:
                for entry in row:
                    entry.setReadOnly(False)
            self.update_kernel_sum()

    def get_preset_kernel(self, preset_name):
        if preset_name == "Smoothing (Average)":
            return ConvolutionFilter.get_smoothing_kernel(3)
        elif preset_name == "Gaussian Blur":
            return ConvolutionFilter.get_gaussian_kernel(3, sigma=1.0)
        elif preset_name == "Sharpening":
            return ConvolutionFilter.get_sharpening_kernel()
        elif preset_name == "Mean Removal (High-pass)":
            return ConvolutionFilter.get_mean_removal_kernel()
        elif preset_name == "Emboss":
            return ConvolutionFilter.get_emboss_kernel()
        else:
            return None

    def update_kernel_sum(self):
        total = 0.0
        for i in range(3):
            for j in range(3):
                try:
                    val = float(self.kernel_entries[i][j].text())
                except ValueError:
                    val = 0.0
                total += val
        self.kernel_sum_value.setText(f"{total:.4f}")

    def get_custom_kernel(self):
        kernel = []
        for i in range(3):
            row = []
            for j in range(3):
                try:
                    row.append(float(self.kernel_entries[i][j].text()))
                except ValueError:
                    return None
            kernel.append(row)
        return kernel

# ---------- Main control panel creation ----------
def create_control_panel(app_instance):
    widget = QWidget()
    widget.setObjectName("control-panel")
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(16)

    header = create_panel_header()
    layout.addWidget(header)

    # Controls stack
    controls_stack = QStackedWidget()
    controls_stack.setObjectName("filter-controls")
    controls_stack.addWidget(QWidget())  # empty
    controls_stack.addWidget(create_color_filter_buttons(app_instance))
    controls_stack.addWidget(ConvolutionControls(app_instance))
    controls_stack.setVisible(False)
    layout.addWidget(controls_stack)

    # Histogram, projection, centroid
    histogram = HistogramCanvas()
    histogram.setObjectName("histogram-widget")
    layout.addWidget(histogram)

    projection_widget = ProjectionWidget()
    projection_widget.setObjectName("projection-widget")
    layout.addWidget(projection_widget)

    centroid_widget = QWidget()
    centroid_layout = QVBoxLayout(centroid_widget)
    centroid_layout.setContentsMargins(0, 16, 0, 0)
    centroid_layout.setSpacing(8)
    centroid_label = QLabel("Centroid Coordinates:")
    centroid_label.setObjectName("panel-subtitle")
    centroid_value = QLabel("Not computed")
    centroid_value.setObjectName("centroid-value")
    centroid_value.setWordWrap(True)
    centroid_btn = QPushButton(" Show Centroid")
    centroid_btn.setCursor(Qt.PointingHandCursor)
    centroid_btn.setObjectName("centroid-btn")
    try:
        centroid_btn.setIcon(qta.icon('fa5s.crosshairs', color='white'))
    except:
        centroid_btn.setText("🎯 Show Centroid")
    centroid_btn.clicked.connect(app_instance.show_centroids)
    centroid_layout.addWidget(centroid_label)
    centroid_layout.addWidget(centroid_value)
    centroid_layout.addWidget(centroid_btn)
    layout.addWidget(centroid_widget)

    # Store references
    app_instance.histogram_widget = histogram
    app_instance.filter_stack = None
    app_instance.filter_controls_stack = controls_stack
    app_instance.projection_widget = projection_widget
    app_instance.centroid_label = centroid_value
    app_instance.centroid_btn = centroid_btn

    return widget, (None, controls_stack)

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
    subtitle = QLabel("Select a filter tab above to access its controls")
    subtitle.setObjectName("panel-subtitle")
    header_layout.addWidget(title)
    header_layout.addWidget(subtitle)
    return header