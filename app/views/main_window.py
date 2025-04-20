from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QLineEdit, QLabel, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from app.controllers.student_controller import StudentController
from app.views.student_dialog import StudentDialog

class MainWindow(QMainWindow):
    """
    Cửa sổ chính của ứng dụng
    """
    def __init__(self):
        super().__init__()
        self.student_controller = StudentController()
        self.init_ui()
        
    def init_ui(self):
        """Thiết lập giao diện người dùng"""
        self.setWindowTitle("Quản lý Sinh viên")
        self.setMinimumSize(800, 600)
        
        # Widget chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính
        main_layout = QVBoxLayout(central_widget)
        
        # Phần tìm kiếm
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập từ khóa tìm kiếm...")
        self.search_input.textChanged.connect(self.search_students)
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.search_input)
        
        # Nút tìm kiếm
        search_button = QPushButton("Tìm kiếm")
        search_button.clicked.connect(self.search_students)
        search_layout.addWidget(search_button)
        
        # Thêm layout tìm kiếm vào layout chính
        main_layout.addLayout(search_layout)
        
        # Bảng danh sách sinh viên
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(8)
        self.student_table.setHorizontalHeaderLabels([
            "Mã sinh viên", "Họ tên", "Tuổi", "Giới tính", 
            "Lớp", "Khoa", "Email", "Số điện thoại"
        ])
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.student_table)
        
        # Layout cho các nút chức năng
        button_layout = QHBoxLayout()
        
        # Nút thêm sinh viên
        add_button = QPushButton("Thêm Sinh viên")
        add_button.clicked.connect(self.add_student)
        button_layout.addWidget(add_button)
        
        # Nút sửa sinh viên
        edit_button = QPushButton("Sửa Sinh viên")
        edit_button.clicked.connect(self.edit_student)
        button_layout.addWidget(edit_button)
        
        # Nút xóa sinh viên
        delete_button = QPushButton("Xóa Sinh viên")
        delete_button.clicked.connect(self.delete_student)
        button_layout.addWidget(delete_button)
        
        # Nút làm mới
        refresh_button = QPushButton("Làm mới")
        refresh_button.clicked.connect(self.load_students)
        button_layout.addWidget(refresh_button)
        
        # Thêm layout nút vào layout chính
        main_layout.addLayout(button_layout)
        
        # Load danh sách sinh viên khi khởi động
        self.load_students()
        
    def load_students(self):
        """Tải danh sách sinh viên vào bảng"""
        students = self.student_controller.get_all_students()
        self.update_student_table(students)
        
    def update_student_table(self, students):
        """Cập nhật bảng hiển thị sinh viên"""
        self.student_table.setRowCount(0)
        
        for row, student in enumerate(students):
            self.student_table.insertRow(row)
            self.student_table.setItem(row, 0, QTableWidgetItem(student.student_id))
            self.student_table.setItem(row, 1, QTableWidgetItem(student.name))
            self.student_table.setItem(row, 2, QTableWidgetItem(str(student.age)))
            self.student_table.setItem(row, 3, QTableWidgetItem(student.gender))
            self.student_table.setItem(row, 4, QTableWidgetItem(student.class_name))
            self.student_table.setItem(row, 5, QTableWidgetItem(student.department))
            self.student_table.setItem(row, 6, QTableWidgetItem(student.email))
            self.student_table.setItem(row, 7, QTableWidgetItem(student.phone))
            
    def add_student(self):
        """Mở dialog thêm sinh viên mới"""
        dialog = StudentDialog(self)
        if dialog.exec_():  # Note: in PyQt5 it's exec_() not exec()
            student_data = dialog.get_student_data()
            
            # Kiểm tra tính hợp lệ của dữ liệu
            errors = self.student_controller.validate_student_data(student_data)
            
            if errors:
                error_message = "\n".join([f"{k}: {v}" for k, v in errors.items()])
                QMessageBox.critical(self, "Lỗi", f"Dữ liệu không hợp lệ:\n{error_message}")
                return
                
            # Kiểm tra sinh viên đã tồn tại chưa
            existing_student = self.student_controller.get_student_by_id(student_data['student_id'])
            if existing_student:
                QMessageBox.warning(self, "Cảnh báo", "Mã sinh viên đã tồn tại!")
                return
                
            # Thêm sinh viên mới
            if self.student_controller.add_student(student_data):
                QMessageBox.information(self, "Thành công", "Đã thêm sinh viên mới!")
                self.load_students()
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể thêm sinh viên!")
                
    def edit_student(self):
        """Sửa thông tin sinh viên được chọn"""
        selected_row = self.student_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn sinh viên để sửa!")
            return
            
        student_id = self.student_table.item(selected_row, 0).text()
        student = self.student_controller.get_student_by_id(student_id)
        
        if not student:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy thông tin sinh viên!")
            return
            
        dialog = StudentDialog(self, student)
        if dialog.exec_():  # Note: in PyQt5 it's exec_() not exec()
            student_data = dialog.get_student_data()
            
            # Kiểm tra tính hợp lệ của dữ liệu
            errors = self.student_controller.validate_student_data(student_data)
            if errors:
                error_message = "\n".join([f"{k}: {v}" for k, v in errors.items()])
                QMessageBox.critical(self, "Lỗi", f"Dữ liệu không hợp lệ:\n{error_message}")
                return
                
            # Cập nhật thông tin sinh viên
            if self.student_controller.update_student(student_data):
                QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin sinh viên!")
                self.load_students()
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể cập nhật thông tin sinh viên!")
                
    def delete_student(self):
        """Xóa sinh viên được chọn"""
        selected_row = self.student_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn sinh viên để xóa!")
            return
            
        student_id = self.student_table.item(selected_row, 0).text()
        student_name = self.student_table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self, 
            "Xác nhận xóa", 
            f"Bạn có chắc chắn muốn xóa sinh viên {student_name} ({student_id})?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.student_controller.delete_student(student_id):
                QMessageBox.information(self, "Thành công", "Đã xóa sinh viên!")
                self.load_students()
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa sinh viên!")
                
    def search_students(self):
        """Tìm kiếm sinh viên theo từ khóa"""
        keyword = self.search_input.text().strip()
        if keyword:
            students = self.student_controller.search_students(keyword)
        else:
            students = self.student_controller.get_all_students()
            
        self.update_student_table(students)
