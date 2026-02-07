#!/usr/bin/env python3
"""
VisionPro AI Image Processing Application
Main entry point
"""

import sys
import os

# Add the parent directory to Python path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Launch the application
if __name__ == "__main__":
    try:
        from gui.dashboard import ImageProcessingApp, QApplication, QFont
        app = QApplication(sys.argv)
        
        # Set application font
        font = QFont("Segoe UI", 10)
        app.setFont(font)
        
        window = ImageProcessingApp()
        window.show()
        
        sys.exit(app.exec())
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("\nPlease make sure you have installed all dependencies:")
        print("pip install PySide6 pillow qtawesome numpy")
        print("\nIf you're running from the gui folder, run from the project root instead.")
        sys.exit(1)