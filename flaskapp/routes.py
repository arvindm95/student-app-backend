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


class Teacher(db.Model, Serializer):
    teacher_id = db.Column(db.Integer, primary_key=True)
    teacher_first_name = db.Column(db.String(45))
    teacher_last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))

    def __init__(self, teacher_first_name, teacher_last_name, email):
        self.teacher_first_name = teacher_first_name
        self.teacher_last_name = teacher_last_name
        self.email = email

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


class Student_questions(db.Model, Serializer):
    question_id = db.Column(db.Integer, primary_key=True)
    question_description = db.Column(db.String(250))

    def __init__(self, question_id, question_description):
        self.question_id = question_id
        self.question_description = question_description

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Teacher_questions(db.Model, Serializer):
    question_id = db.Column(db.Integer, primary_key=True)
    question_description = db.Column(db.String(250))

    def __init__(self, question_id, question_description):
        self.question_id = question_id
        self.question_description = question_description

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Student_answers(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    question_answer = db.Column(db.String(45))
    question_description = db.Column(db.String(250))

    def __init__(self, student_id, question_id, question_description):
        self.student_id = student_id
        self.question_id = question_id
        self.question_description = question_description

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Teacher_answers(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    question_answer = db.Column(db.String(45))
    question_description = db.Column(db.String(250))

    def __init__(self, teacher_id, student_id, question_id, question_description):
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.question_id = question_id
        self.question_description = question_description

    def serialize(self):
        d = Serializer.serialize(self)
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
    students = Student.serialize_list(students)
    for i in range(0, len(students)):
        semester = Student_marks.query.filter_by(
            student_id=students[i]['student_id'], semester=1).all()
        semester = Student_marks.serialize_list(semester)
        students[i]['student_marks'] = semester

    return jsonify(students)


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
def getStudentMarks(student_id):
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


@app.route('/student/questions/all')
def getAllQuestions():
    questions = Questions.query.all()
    response = Questions.serialize_list(questions)
    return jsonify(response)


@app.route('/student/questions/populate')
def populateQuestions():
    students = Student.query.order_by(Student.student_first_name).all()
    students = Student.serialize_list(students)
    questions = Student_questions.query.all()
    questions = Student_questions.serialize_list(questions)

    for i in range(0, len(students)):
        for j in range(0, len(questions)):
            student = Student_answers(
                students[i]['student_id'], questions[j]['question_id'], questions[j]['question_description'])
            db.session.add(student)
            db.session.commit()

    return jsonify({'status': 'success'})


@app.route('/teacher/questions/populate')
def populateTeacherQuestions():
    teachers = Teacher.query.order_by(Teacher.teacher_first_name).all()
    teachers = Teacher.serialize_list(teachers)
    students = Student.query.order_by(Student.student_first_name).all()
    students = Student.serialize_list(students)
    questions = Teacher_questions.query.all()
    questions = Teacher_questions.serialize_list(questions)

    for i in range(0, len(teachers)):
        for j in range(0, len(students)):
            for k in range(0, len(questions)):
                teacher = Teacher_answers(teachers[i]['teacher_id'],
                                          students[j]['student_id'], questions[k]['question_id'], questions[k]['question_description'])
                db.session.add(teacher)
                db.session.commit()

    return jsonify({'status': 'success'})


@app.route('/student/questions/<student_id>')
def getStudentQuestions(student_id):
    answers = Student_answers.query.filter_by(student_id=student_id).all()
    response = Student_answers.serialize_list(answers)
    return jsonify(response)


@app.route('/teacher/questions/<teacher_id>')
def getTeacherQuestions(teacher_id):
    student_id = request.args.get('student')
    answers = Teacher_answers.query.filter_by(
        teacher_id=teacher_id, student_id=student_id).all()
    response = Teacher_answers.serialize_list(answers)
    return jsonify(response)


@app.route('/student/questions/save', methods=['POST'])
def saveStudentAnswer():
    requestJson = request.json
    student_id = requestJson['student_id']
    question_id = requestJson['question_id']
    question_answer = requestJson['question_answer']
    student = Student_answers.query.filter_by(
        student_id=student_id, question_id=question_id).first()
    student.question_answer = question_answer
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/teacher/questions/save', methods=['POST'])
def saveTeacherAnswer():
    requestJson = request.json
    teacher_id = requestJson['teacher_id']
    student_id = requestJson['student_id']
    question_id = requestJson['question_id']
    question_answer = requestJson['question_answer']
    teacher = Teacher_answers.query.filter_by(teacher_id=teacher_id,
                                              student_id=student_id, question_id=question_id).first()
    teacher.question_answer = question_answer
    db.session.commit()
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
