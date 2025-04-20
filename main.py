import sys
import os

# Try to use PyQt5 instead of PyQt6
try:
    # First attempt to import PyQt5
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    print("Using PyQt5 successfully")
    
    # We need to modify the import path for the main window
    # Add the current directory to path to make imports work
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Import our custom MainWindow
    from app.views.main_window import MainWindow
    
except ImportError as e:
    print(f"Error importing PyQt5: {e}")
    print(f"Python version: {sys.version}")
    print(f"Path: {os.environ.get('PATH')}")
    sys.exit(1)

def main():
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        # PyQt5 uses exec_() instead of exec()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
