
# PyQt5 adapter for the student dialog
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QSpinBox, QPushButton, 
                            QFormLayout, QDialogButtonBox)
from app.models.student import Student

# Compatibility layer for PyQt6 to PyQt5
if not hasattr(QDialogButtonBox, 'StandardButton'):
    QDialogButtonBox.StandardButton = QDialogButtonBox
    QDialogButtonBox.StandardButton.Ok = QDialogButtonBox.Ok
    QDialogButtonBox.StandardButton.Cancel = QDialogButtonBox.Cancel

class StudentDialog(QDialog):
    """
    Dialog de them/sua thong tin sinh vien
    """
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.student = student
        self.init_ui()
        
    def init_ui(self):
        """Thiet lap giao dien dialog"""
        # Thiet lap tieu de cho dialog
        if self.student:
            self.setWindowTitle("Sua thong tin sinh vien")
        else:
            self.setWindowTitle("Them sinh vien moi")
            
        self.setMinimumWidth(400)
        
        # Layout chinh
        layout = QVBoxLayout(self)
        
        # Form layout cho cac truong thong tin
        form_layout = QFormLayout()
        
        # Ma sinh vien
        self.student_id_input = QLineEdit()
        form_layout.addRow("Ma sinh vien:", self.student_id_input)
        
        # Ho ten
        self.name_input = QLineEdit()
        form_layout.addRow("Ho ten:", self.name_input)
        
        # Tuoi
        self.age_input = QSpinBox()
        self.age_input.setRange(1, 100)
        self.age_input.setValue(18)
        form_layout.addRow("Tuoi:", self.age_input)
        
        # Gioi tinh
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Nam", "Nu", "Khac"])
        form_layout.addRow("Gioi tinh:", self.gender_input)
        
        # Lop
        self.class_input = QLineEdit()
        form_layout.addRow("Lop:", self.class_input)
        
        # Khoa
        self.department_input = QLineEdit()
        form_layout.addRow("Khoa:", self.department_input)
        
        # Email
        self.email_input = QLineEdit()
        form_layout.addRow("Email:", self.email_input)
        
        # So dien thoai
        self.phone_input = QLineEdit()
        form_layout.addRow("So dien thoai:", self.phone_input)
        
        # Them form vao layout chinh
        layout.addLayout(form_layout)
        
        # Cac nut OK va Cancel
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
        # Neu dang sua, dien thong tin co san
        if self.student:
            self.fill_student_data()
            self.student_id_input.setReadOnly(True)  # Khong cho phep sua ID
            
    def fill_student_data(self):
        """Dien thong tin sinh vien vao form"""
        self.student_id_input.setText(self.student.student_id)
        self.name_input.setText(self.student.name)
        self.age_input.setValue(self.student.age)
        
        # Thiet lap gioi tinh
        gender_index = 0  # Mac dinh la Nam
        if self.student.gender == "Nu":
            gender_index = 1
        elif self.student.gender == "Khac":
            gender_index = 2
        self.gender_input.setCurrentIndex(gender_index)
        
        self.class_input.setText(self.student.class_name)
        self.department_input.setText(self.student.department)
        self.email_input.setText(self.student.email)
        self.phone_input.setText(self.student.phone)
        
    def get_student_data(self):
        """Lay thong tin sinh vien tu form"""
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
