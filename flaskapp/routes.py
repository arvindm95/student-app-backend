from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/student_app_db'
db = SQLAlchemy(app)


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

    def __init__(self, student_id, student_first_name, student_last_name, student_department, student_regno):
        self.student_id = student_id
        self.student_first_name = student_first_name
        self.student_last_name = student_last_name
        self.student_department = student_department
        self.student_regno = student_regno

    def serialize(self):
        d = Serializer.serialize(self)
        # del d['student_password']
        return d


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/student/all')
def getAllStudents():
    students = Student.query.all()
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
    student = Student(requestJson['student_id'], requestJson['student_name'], requestJson['student_email'],
                      requestJson['student_username'], requestJson['student_password'], requestJson['student_department'])
    db.session.add(student)
    db.session.commit()

    return jsonify({'status': 'success'})


@app.route('/status')
def getStatus():
    # response.headers['Content-Type'] = 'application/json'
    return jsonify({'status': 'service working'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
