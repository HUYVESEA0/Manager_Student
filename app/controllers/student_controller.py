from app.database.db_handler import DatabaseHandler
from app.models.student import Student

class StudentController:
    """
    Controller xử lý logic nghiệp vụ liên quan đến sinh viên
    """
    def __init__(self):
        self.db = DatabaseHandler()
        self.db.connect()
        
    def __del__(self):
        self.db.disconnect()
        
    def add_student(self, student_data):
        """Thêm sinh viên mới"""
        student = Student.from_dict(student_data)
        return self.db.add_student(student)
        
    def update_student(self, student_data):
        """Cập nhật thông tin sinh viên"""
        student = Student.from_dict(student_data)
        return self.db.update_student(student)
        
    def delete_student(self, student_id):
        """Xóa sinh viên"""
        return self.db.delete_student(student_id)
        
    def get_all_students(self):
        """Lấy danh sách tất cả sinh viên"""
        return self.db.get_all_students()
        
    def get_student_by_id(self, student_id):
        """Lấy thông tin sinh viên theo ID"""
        return self.db.get_student_by_id(student_id)
        
    def search_students(self, keyword):
        """Tìm kiếm sinh viên theo từ khóa"""
        return self.db.search_students(keyword)
        
    def validate_student_data(self, student_data):
        """Kiểm tra tính hợp lệ của dữ liệu sinh viên"""
        errors = {}
        
        # Kiểm tra ID sinh viên
        if not student_data.get('student_id'):
            errors['student_id'] = "ID sinh viên không được để trống"
        
        # Kiểm tra tên sinh viên
        if not student_data.get('name'):
            errors['name'] = "Tên sinh viên không được để trống"
            
        # Kiểm tra tuổi
        try:
            age = int(student_data.get('age', 0))
            if age <= 0 or age > 100:
                errors['age'] = "Tuổi không hợp lệ (1-100)"
        except ValueError:
            errors['age'] = "Tuổi phải là số nguyên"
            
        # Kiểm tra email
        email = student_data.get('email', '')
        if email and '@' not in email:
            errors['email'] = "Email không hợp lệ"
            
        return errors
