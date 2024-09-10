import mysql.connector
from faker import Faker
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to the SQL database
connection = mysql.connector.connect(
    host="localhost",  # Adjust as per your server settings
    user="root",       # Your MySQL username
    password="",  # Your MySQL password
    database="StudentManagementSystem"
)

cursor = connection.cursor()
fake = Faker()

# Insert 20 courses into the course_data table
def populate_courses():
    courses = [
        ("Introduction to AI", "AI101", "Mon/Wed/Fri 10:00-11:00"),
        ("Data Science", "DS201", "Tue/Thu 09:00-10:30"),
        ("Machine Learning", "ML301", "Mon/Wed 12:00-13:30"),
        ("Python Programming", "PY401", "Tue/Thu 11:00-12:30"),
        ("Database Systems", "DB501", "Mon/Wed 14:00-15:30"),
        ("Software Engineering", "SE601", "Tue/Thu 10:00-11:30"),
        ("Computer Networks", "CN701", "Mon/Wed 09:00-10:00"),
        ("Cyber Security", "CS801", "Tue/Thu 13:00-14:30"),
        ("Algorithms", "AL901", "Mon/Wed 11:00-12:00"),
        ("Operating Systems", "OS301", "Tue/Thu 09:00-10:30"),
        ("Web Development", "WD401", "Mon/Wed 10:00-11:30"),
        ("Cloud Computing", "CC101", "Tue/Thu 12:00-13:30"),
        ("Big Data", "BD501", "Mon/Wed 13:00-14:30"),
        ("Artificial Intelligence Ethics", "AI201", "Tue/Thu 10:00-11:00"),
        ("Blockchain Technology", "BT301", "Mon/Wed 15:00-16:00"),
        ("Quantum Computing", "QC101", "Tue/Thu 14:00-15:00"),
        ("Augmented Reality", "AR201", "Mon/Wed 10:00-11:00"),
        ("Virtual Reality", "VR301", "Tue/Thu 11:00-12:00"),
        ("Natural Language Processing", "NLP101", "Mon/Wed 12:00-13:00"),
        ("Ethical Hacking", "EH401", "Tue/Thu 15:00-16:30")
    ]
    
    query = "INSERT INTO course_data (course_name, course_code, schedule) VALUES (%s, %s, %s)"
    
    logging.info("Populating courses...")
    for course in courses:
        cursor.execute(query, course)
    connection.commit()
    logging.info("Courses populated.")

# Insert 5000 fake students into the student_data table and enroll them in random courses
def populate_students(n):
    logging.info(f"Populating {n} students...")
    cursor.execute("SELECT course_id FROM course_data")
    courses = cursor.fetchall()
    
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        
        # Insert student
        student_query = "INSERT INTO student_data (first_name, last_name, email) VALUES (%s, %s, %s)"
        cursor.execute(student_query, (first_name, last_name, email))
        student_id = cursor.lastrowid  # Get the inserted student's ID
        
        # Enroll the student in 1-3 random courses
        enrolled_courses = random.sample(courses, random.randint(1, 3))
        for course in enrolled_courses:
            enrollment_query = "INSERT INTO student_course (student_id, course_id) VALUES (%s, %s)"
            cursor.execute(enrollment_query, (student_id, course[0]))
    
    connection.commit()
    logging.info(f"{n} students populated and enrolled in courses.")

# Insert 500 fake teachers into the teacher_data table
def populate_teachers(n):
    logging.info(f"Populating {n} teachers...")
    cursor.execute("SELECT course_id FROM course_data")
    courses = cursor.fetchall()
    
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        class_id = random.choice(courses)[0]  # Assign teacher to a random course
        
        teacher_query = "INSERT INTO teacher_data (first_name, last_name, email, class_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(teacher_query, (first_name, last_name, email, class_id))
    
    connection.commit()
    logging.info(f"{n} teachers populated.")

# Populate the database
populate_courses()      # Insert 20 courses
populate_students(5000)   # Insert 5000 students
populate_teachers(500)    # Insert 500 teachers

# Close the connection
cursor.close()
connection.close()
