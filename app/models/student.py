class Student:
    """
    Class đại diện cho một sinh viên với các thuộc tính cơ bản
    """
    def __init__(self, student_id=None, name="", age=0, gender="", 
                 class_name="", department="", email="", phone=""):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.class_name = class_name
        self.department = department
        self.email = email
        self.phone = phone
    
    def __str__(self):
        return f"Student(ID: {self.student_id}, Name: {self.name}, Age: {self.age})"
    
    def to_dict(self):
        """Chuyển đổi thông tin sinh viên thành dictionary"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'class_name': self.class_name,
            'department': self.department,
            'email': self.email,
            'phone': self.phone
        }
    
    @classmethod
    def from_dict(cls, data):
        """Tạo một đối tượng Student từ dictionary"""
        return cls(
            student_id=data.get('student_id'),
            name=data.get('name', ""),
            age=data.get('age', 0),
            gender=data.get('gender', ""),
            class_name=data.get('class_name', ""),
            department=data.get('department', ""),
            email=data.get('email', ""),
            phone=data.get('phone', "")
        )
