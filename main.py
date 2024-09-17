from flask import Flask, request, jsonify
from student.studentDao import insert_student_data, update_student_data, delete_student_data, get_all_students
from datetime import datetime
from flask_cors import CORS 
import re

app = Flask(__name__)
CORS(app)


@app.route("/insert_data", methods=['POST'])
def insert_student():
    data = request.get_json()

    if not data:
        return jsonify({'status': False, 'message': 'Invalid parameters.'}) ,400
    
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    gender = data.get('gender')
    email = data.get('email')
    phone_number = data.get('phone_number')

    if not all([first_name, last_name, gender, email, phone_number]):
        return jsonify({'message': 'Invalid parameter.', 'status': False}), 400

    if not re.match(r'^[A-Za-z]{1,50}$', first_name):
        return jsonify(
            {"message": "Invalid first name format (only letters allowed, max 50 characters)", "status": False}), 400

    if not re.match(r'^[A-Za-z]{1,50}$', last_name):
        return jsonify(
            {"message": "Invalid last name format (only letters allowed, max 50 characters)", "status": False}), 400

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return jsonify({"message": "Invalid email address format", "status": False}), 400

    phone_pattern = r'^[67890]\d{9}$'
    if not re.match(phone_pattern, phone_number):
        return jsonify({'message': 'Invalid phone number.', 'status': False}), 400

    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    std_insert_data = insert_student_data(first_name, last_name, gender, email, phone_number, created_at)
    if std_insert_data:
        return jsonify(
            {"status": True, 'message': 'Student data inserted successfully.'}), 200
    else:
        return jsonify({"status": False, 'message': 'Failed to insert student data.'}), 500



@app.route('/update_data/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid Parameter', 'status': False}), 400

    VALID_FIELDS = {'first_name', 'last_name', 'gender', 'email', 'phone_number'}

    if not any(field in data for field in VALID_FIELDS):
        return jsonify({'message': 'No valid parameter provided to update', 'status': False}), 400

    name_pattern = r'^[A-Za-z]+$'
    if 'first_name' in data and not re.match(name_pattern, data['first_name']):
        return jsonify({'message': 'Invalid first name', 'status': False}), 400
    if 'last_name' in data and not re.match(name_pattern, data['last_name']):
        return jsonify({'message': 'Invalid last name.', 'status': False}), 400

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if 'email' in data and not re.match(email_pattern, data['email']):
        return jsonify({'message': 'Invalid email format.', 'status': False}), 400

    phone_pattern = r'^[67890]\d{9}$'
    if 'phone_number' in data and not re.match(phone_pattern, data['phone_number']):
        return jsonify({'message': 'Invalid phone number.', 'status': False}), 400

    result = update_student_data(student_id, data)

    if result is False:
        return jsonify({'message': 'Student not found or no update made', 'status': False}), 404
    elif isinstance(result, Exception):
        return jsonify({'message': str(result), 'status': False}), 500

    return jsonify({'message': 'Student data updated successfully', 'status': True, 'data': result}), 200


@app.route('/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        result = delete_student_data(student_id)
        if result is False:
            return jsonify({'message': 'Invalid student ID, student not found', 'status': False}), 404
        elif isinstance(result, Exception):
            return jsonify({'message': str(result), 'status': False}), 500

        return jsonify({'message': 'Student data deleted successfully', 'status': True}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e), 'status': False}), 500


@app.route('/get_student', methods=['GET'])
@app.route('/get_student/<int:student_id>', methods=['GET'])
def get_student_details(student_id=None):
    student_details = get_all_students(student_id)

    if student_details:
        if student_id:
            return jsonify({"status": True, "message": "Details fetched successfully", "data": student_details})
        else:
            return jsonify({"status": True, "message": "Details fetched successfully", "data": student_details})
    else:
        return jsonify({"status": False, "message": "Error fetching data or no data found"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
