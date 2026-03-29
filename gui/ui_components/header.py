from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import qtawesome as qta

def create_header():
    header = QWidget()
    header.setObjectName("header")
    header.setFixedHeight(70)

    layout = QHBoxLayout(header)
    layout.setContentsMargins(24, 4, 24, 4)

    left_widget = create_header_left()
    right_widget = create_header_right()

    layout.addWidget(left_widget)
    layout.addStretch()
    layout.addWidget(right_widget)

    return header

def create_header_left():
    left_widget = QWidget()
    left_layout = QHBoxLayout(left_widget)
    left_layout.setSpacing(40)

    logo_widget = create_logo()
    left_layout.addWidget(logo_widget)

    nav_menu = create_nav_menu()
    left_layout.addWidget(nav_menu)
    left_layout.addStretch()

    return left_widget

def create_logo():
    logo_widget = QWidget()
    logo_layout = QHBoxLayout(logo_widget)
    logo_layout.setSpacing(12)

    logo_icon = QLabel()
    logo_icon.setFixedSize(36, 36)
    logo_icon.setObjectName("logo-icon")
    logo_icon.setAlignment(Qt.AlignCenter)

    try:
        eye_icon = qta.icon('fa5s.eye', color='white')
        eye_pixmap = eye_icon.pixmap(24, 24)
        logo_icon.setPixmap(eye_pixmap)
    except:
        logo_icon.setText("👁️")

    logo_text = QLabel("CPEP 323A")
    logo_text.setObjectName("logo-text")

    logo_layout.addWidget(logo_icon)
    logo_layout.addWidget(logo_text)

    return logo_widget

def create_nav_menu():
    nav_menu = QWidget()
    nav_layout = QHBoxLayout(nav_menu)
    nav_layout.setSpacing(8)

    dashboard_btn = QPushButton("Dashboard")
    dashboard_btn.setObjectName("nav-item-active")
    dashboard_btn.setCursor(Qt.PointingHandCursor)
    nav_layout.addWidget(dashboard_btn)

    return nav_menu

def create_header_right():
    right_widget = QWidget()
    right_layout = QHBoxLayout(right_widget)
    right_layout.setSpacing(16)

    user_profile = create_user_profile()
    right_layout.addWidget(user_profile)

    return right_widget

def create_user_profile():
    user_profile = QWidget()
    user_profile.setObjectName("user-profile")
    user_profile.setCursor(Qt.PointingHandCursor)
    user_layout = QHBoxLayout(user_profile)
    user_layout.setSpacing(12)
    user_layout.setContentsMargins(8, 8, 8, 8)

    user_avatar = QLabel("JM")
    user_avatar.setObjectName("user-avatar")
    user_avatar.setAlignment(Qt.AlignCenter)
    user_avatar.setFixedSize(32, 32)

    user_info = create_user_info()

    user_layout.addWidget(user_avatar)
    user_layout.addWidget(user_info)

    return user_profile

def create_user_info():
    user_info = QWidget()
    user_info_layout = QVBoxLayout(user_info)
    user_info_layout.setContentsMargins(0, 0, 0, 0)
    user_info_layout.setSpacing(2)

    user_name = QLabel("Marc Jm Arabejo")
    user_name.setObjectName("user-name")

    user_role = QLabel("Developer")
    user_role.setObjectName("user-role")

    user_info_layout.addWidget(user_name)
    user_info_layout.addWidget(user_role)

    return user_info

# ----- NEW: Filter Navigation Bar -----
def create_filter_navbar(app_instance):
    """Create a tab bar for selecting the active filter."""
    widget = QWidget()
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    tab_bar = QTabBar()
    tab_bar.addTab("Grayscale")
    tab_bar.addTab("Black & White")
    tab_bar.addTab("Background Removal")
    tab_bar.addTab("Color Filters")          # <-- new tab
    tab_bar.setExpanding(True)
    tab_bar.setStyleSheet("""
        QTabBar::tab {
            background-color: #1F2937;
            color: #9CA3AF;
            padding: 12px 24px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: 600;
        }
        QTabBar::tab:selected {
            background-color: #4F46E5;
            color: white;
        }
        QTabBar::tab:hover:!selected {
            background-color: #374151;
            color: #F9FAFB;
        }
    """)

    tab_bar.currentChanged.connect(lambda index: app_instance.on_filter_tab_changed(index))

    layout.addWidget(tab_bar)
    return widget