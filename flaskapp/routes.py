from flask import Flask, render_template, jsonify, request
from flask.ext.api import status
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/student_app_db'
db = SQLAlchemy(app)

response_error = {'status': 'failure'}


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class Student(db.Model, Serializer):
    student_id = db.Column(db.Integer, primary_key=True)
    student_first_name = db.Column(db.String(45))
    student_last_name = db.Column(db.String(45))
    student_department = db.Column(db.String(45))
    student_regno = db.Column(db.String(45))
    student_email = db.Column(db.String(45))
    student_gender = db.Column(db.String(45))

    def __init__(self, student_first_name, student_last_name, student_department, student_regno, student_email, student_gender):
        self.student_first_name = student_first_name
        self.student_last_name = student_last_name
        self.student_department = student_department
        self.student_regno = student_regno
        self.student_email = student_email
        self.student_gender = student_gender

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class User(db.Model, Serializer):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45))
    password = db.Column(db.String(45))
    role_name = db.Column(db.String(45))

    def __init__(self, email, password, role_name):
        self.email = email
        self.password = password
        self.role_name = role_name

    def serialize(self):
        d = Serializer.serialize(self)
        del d['password']
        return d


class Student_marks(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    subject_code = db.Column(db.String(45))
    subject_name = db.Column(db.String(45))
    subject_marks = db.Column(db.Integer)
    semester = db.Column(db.Integer)

    def __init__(self, student_id, subject_code, subject_name, subject_marks, semester):
        self.student_id = student_id
        self.subject_code = subject_code
        self.subject_name = subject_name
        self.subject_marks = subject_marks
        self.semester = semester

    def serialize(self):
        d = Serializer.serialize(self)
        del d['id']
        del d['semester']
        return d


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/student/all')
def getAllStudents():
    students = Student.query.order_by(Student.student_first_name).all()
    response = Student.serialize_list(students)
    return jsonify(response)


@app.route('/student/<student_id>')
def getStudent(student_id):
    student = Student.query.get(student_id)
    response = student.serialize()
    return jsonify(response)


@app.route('/student/add', methods=['POST'])
def postStudent():
    requestJson = request.json
    student = Student(requestJson['student_first_name'], requestJson['student_last_name'],
                      requestJson['student_department'], requestJson['student_regno'])
    db.session.add(student)
    db.session.commit()

    return jsonify({'status': 'success'})


@app.route('/student/delete/<student_id>', methods=['DELETE'])
def deleteStudent(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/status')
def getStatus():
    # response.headers['Content-Type'] = 'application/json'
    return jsonify({'status': 'service working'})


@app.route('/user/login', methods=['POST'])
def loginStudent():

    email = request.json['email']
    password = request.json['password']
    student = User.query.filter_by(
        email=email, password=password).first()

    if student:
        response = student.serialize()
        return jsonify(response)

    response_error['message'] = "user does not exist"
    return jsonify(response_error), status.HTTP_404_NOT_FOUND


@app.route('/student/marks/<student_id>')
def getMark(student_id):
    length = 2
    response = list()
    for i in range(0, length):
        semester = Student_marks.query.filter_by(
            student_id=student_id, semester=i+1).all()
        serializedSemester = Student.serialize_list(semester)
        response.append({
            "semester": i+1,
            "semester_details": serializedSemester
        })

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
