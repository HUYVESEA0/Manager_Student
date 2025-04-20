import sqlite3
import os
from app.models.student import Student

class DatabaseHandler:
    """
    Class xử lý kết nối và thao tác với cơ sở dữ liệu SQLite
    """
    def __init__(self, db_name="student_database.db"):
        # Đường dẫn đến file cơ sở dữ liệu
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), db_name)
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Thiết lập kết nối đến cơ sở dữ liệu"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self._create_tables()
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
            
    def disconnect(self):
        """Đóng kết nối cơ sở dữ liệu"""
        if self.connection:
            self.connection.close()
            
    def _create_tables(self):
        """Tạo các bảng cần thiết nếu chưa tồn tại"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            class_name TEXT,
            department TEXT,
            email TEXT,
            phone TEXT
        )
        ''')
        self.connection.commit()
        
    def add_student(self, student):
        """Thêm sinh viên vào cơ sở dữ liệu"""
        try:
            self.cursor.execute('''
            INSERT INTO students (student_id, name, age, gender, class_name, department, email, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                student.student_id, 
                student.name, 
                student.age, 
                student.gender, 
                student.class_name, 
                student.department, 
                student.email, 
                student.phone
            ))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding student: {e}")
            return False
            
    def update_student(self, student):
        """Cập nhật thông tin sinh viên"""
        try:
            self.cursor.execute('''
            UPDATE students 
            SET name=?, age=?, gender=?, class_name=?, department=?, email=?, phone=?
            WHERE student_id=?
            ''', (
                student.name, 
                student.age, 
                student.gender, 
                student.class_name, 
                student.department, 
                student.email, 
                student.phone,
                student.student_id
            ))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating student: {e}")
            return False
            
    def delete_student(self, student_id):
        """Xóa sinh viên theo ID"""
        try:
            self.cursor.execute('DELETE FROM students WHERE student_id=?', (student_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting student: {e}")
            return False
            
    def get_all_students(self):
        """Lấy danh sách tất cả sinh viên"""
        try:
            self.cursor.execute('SELECT * FROM students')
            rows = self.cursor.fetchall()
            students = []
            for row in rows:
                student = Student(
                    student_id=row[0],
                    name=row[1],
                    age=row[2],
                    gender=row[3],
                    class_name=row[4],
                    department=row[5],
                    email=row[6],
                    phone=row[7]
                )
                students.append(student)
            return students
        except sqlite3.Error as e:
            print(f"Error fetching students: {e}")
            return []
            
    def get_student_by_id(self, student_id):
        """Lấy thông tin sinh viên theo ID"""
        try:
            self.cursor.execute('SELECT * FROM students WHERE student_id=?', (student_id,))
            row = self.cursor.fetchone()
            if row:
                student = Student(
                    student_id=row[0],
                    name=row[1],
                    age=row[2],
                    gender=row[3],
                    class_name=row[4],
                    department=row[5],
                    email=row[6],
                    phone=row[7]
                )
                return student
            return None
        except sqlite3.Error as e:
            print(f"Error fetching student: {e}")
            return None
            
    def search_students(self, keyword):
        """Tìm kiếm sinh viên theo từ khóa"""
        try:
            keyword = f"%{keyword}%"
            self.cursor.execute('''
            SELECT * FROM students 
            WHERE student_id LIKE ? OR name LIKE ? OR class_name LIKE ? OR department LIKE ?
            ''', (keyword, keyword, keyword, keyword))
            
            rows = self.cursor.fetchall()
            students = []
            for row in rows:
                student = Student(
                    student_id=row[0],
                    name=row[1],
                    age=row[2],
                    gender=row[3],
                    class_name=row[4],
                    department=row[5],
                    email=row[6],
                    phone=row[7]
                )
                students.append(student)
            return students
        except sqlite3.Error as e:
            print(f"Error searching students: {e}")
            return []
