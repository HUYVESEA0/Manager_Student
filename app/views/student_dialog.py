from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QSpinBox, QPushButton, 
                            QFormLayout, QDialogButtonBox)
from app.models.student import Student

class StudentDialog(QDialog):
    """
    Dialog để thêm/sửa thông tin sinh viên
    """
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.student = student
        self.init_ui()
        
    def init_ui(self):
        """Thiết lập giao diện dialog"""
        # Thiết lập tiêu đề cho dialog
        if self.student:
            self.setWindowTitle("Sửa thông tin sinh viên")
        else:
            self.setWindowTitle("Thêm sinh viên mới")
            
        self.setMinimumWidth(400)
        
        # Layout chính
        layout = QVBoxLayout(self)
        
        # Form layout cho các trường thông tin
        form_layout = QFormLayout()
        
        # Mã sinh viên
        self.student_id_input = QLineEdit()
        form_layout.addRow("Mã sinh viên:", self.student_id_input)
        
        # Họ tên
        self.name_input = QLineEdit()
        form_layout.addRow("Họ tên:", self.name_input)
        
        # Tuổi
        self.age_input = QSpinBox()
        self.age_input.setRange(1, 100)
        self.age_input.setValue(18)
        form_layout.addRow("Tuổi:", self.age_input)
        
        # Giới tính
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Nam", "Nữ", "Khác"])
        form_layout.addRow("Giới tính:", self.gender_input)
        
        # Lớp
        self.class_input = QLineEdit()
        form_layout.addRow("Lớp:", self.class_input)
        
        # Khoa
        self.department_input = QLineEdit()
        form_layout.addRow("Khoa:", self.department_input)
        
        # Email
        self.email_input = QLineEdit()
        form_layout.addRow("Email:", self.email_input)
        
        # Số điện thoại
        self.phone_input = QLineEdit()
        form_layout.addRow("Số điện thoại:", self.phone_input)
        
        # Thêm form vào layout chính
        layout.addLayout(form_layout)
        
        # Các nút OK và Cancel
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
        # Nếu đang sửa, điền thông tin có sẵn
        if self.student:
            self.fill_student_data()
            self.student_id_input.setReadOnly(True)  # Không cho phép sửa ID
            
    def fill_student_data(self):
        """Điền thông tin sinh viên vào form"""
        self.student_id_input.setText(self.student.student_id)
        self.name_input.setText(self.student.name)
        self.age_input.setValue(self.student.age)
        
        # Thiết lập giới tính
        gender_index = 0  # Mặc định là Nam
        if self.student.gender == "Nữ":
            gender_index = 1
        elif self.student.gender == "Khác":
            gender_index = 2
        self.gender_input.setCurrentIndex(gender_index)
        
        self.class_input.setText(self.student.class_name)
        self.department_input.setText(self.student.department)
        self.email_input.setText(self.student.email)
        self.phone_input.setText(self.student.phone)
        
    def get_student_data(self):
        """Lấy thông tin sinh viên từ form"""
        return {
            'student_id': self.student_id_input.text(),
            'name': self.name_input.text(),
            'age': self.age_input.value(),
            'gender': self.gender_input.currentText(),
            'class_name': self.class_input.text(),
            'department': self.department_input.text(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text()
        }
