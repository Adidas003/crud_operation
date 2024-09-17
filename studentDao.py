#make sure you have a create a folder student in student folder made the studentDao.py file...

from datetime import datetime
import db_connection


def insert_student_data(first_name, last_name, gender, email, phone_number, created_at):
    conn = db_connection.get_connection()  
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO student_info (first_name, last_name, gender, email, phone_number, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, gender, email, phone_number, created_at)
            cursor.execute(query, values)
            conn.commit()

            return values

        except Exception as e:
            return e


def update_student_data(student_id, data):
    conn = db_connection.get_connection() 
    if conn:
        try:
            cursor = conn.cursor()

            updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            query = "UPDATE student_info SET "
            query_params = []

            if 'first_name' in data:
                query += "first_name = %s, "
                query_params.append(data['first_name'])
            if 'last_name' in data:
                query += "last_name = %s, "
                query_params.append(data['last_name'])
            if 'gender' in data:
                query += "gender = %s, "
                query_params.append(data['gender'])
            if 'email' in data:
                query += "email = %s, "
                query_params.append(data['email'])
            if 'phone_number' in data:
                query += "phone_number = %s, "
                query_params.append(data['phone_number'])

            query += "updated_at = %s "
            query_params.append(updated_at)

            query += "WHERE id = %s"
            query_params.append(student_id)

            cursor.execute(query, tuple(query_params))
            conn.commit()

            if cursor.rowcount == 0:
                return False
            
            cursor.execute("SELECT * FROM student_info WHERE id = %s", (student_id,))
            updated_student = cursor.fetchone()
            if updated_student:
                column_names = [desc[0] for desc in cursor.description]
                student_data = dict(zip(column_names, updated_student))
                return student_data

        except Exception as e:
            return e


def delete_student_data(student_id):
    conn = db_connection.get_connection()  
    if conn:
        try:
            cursor = conn.cursor()
            
            check_query = "SELECT 1 FROM student_info WHERE id = %s"
            cursor.execute(check_query, (student_id,))
            student_exists = cursor.fetchone()

            if not student_exists:
                return False  

            delete_query = "DELETE FROM student_info WHERE id = %s"
            cursor.execute(delete_query, (student_id,))
            conn.commit()
            
            return True 
        except Exception as e:
            return e 


def get_all_students(student_id=None):
    conn = db_connection.get_connection()  
    if conn:
        try:
            cursor = conn.cursor()

            if student_id:
                query = "SELECT * FROM student_info WHERE id = %s"
                cursor.execute(query, (student_id,))
                result = cursor.fetchone()

                if result:
                    column_names = [desc[0] for desc in cursor.description]
                    student = dict(zip(column_names, result))
                    return student
                else:
                    return None

            else:
                query = "SELECT * FROM student_info"
                cursor.execute(query)
                result = cursor.fetchall()

                if result:
                    column_names = [desc[0] for desc in cursor.description]
                    students = [dict(zip(column_names, row)) for row in result]
                    return students
                else:
                    return None

        except Exception as e:
            return e
