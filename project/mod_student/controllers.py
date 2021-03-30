from project.mod_student.models import Student
from project.mod_faculty.models import UploadCourses, Courses, Faculty,Filled
from project import db_session, bcrypt
from sqlalchemy import and_, func
from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, abort

mod_student = Blueprint('student', __name__)

@mod_student.route("/" ,methods=['GET', 'POST'])
def student_dashboard():
    if 'user' in session:
        student = Student.query.filter(Student.id == session['user']).first()
        print(student)
        section_ids = []
        for section in student.section:
            section_ids.append(section.id)
        upload_courses = UploadCourses.query.filter(UploadCourses.section_id.in_(section_ids)).all()
        return render_template('student/student_dashboard.html',
        student = student,
        upload_courses = upload_courses,
        course_names = Courses,
        faculty = Faculty,
        filled=Filled,
        )
    else:
        return redirect(url_for('home'))

@mod_student.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@mod_student.route('/submit/<int:id>',methods=['GET', 'POST'])
def submit_feedback(id):
    if 'user' in session:
        student = Student.query.filter(Student.id == session['user']).first()
        section_ids = []
        for section in student.section:
            section_ids.append(section.id)
        student_courses = UploadCourses.query.with_entities(UploadCourses.id).filter(UploadCourses.section_id.in_(section_ids)).all()
        not_present = True
        for course in student_courses:
            print(course)
            if id == course[0]:
                print(course[0])
                not_present = False
                break
        if not_present:
            abort(404)
        if Filled.query.filter(Filled.student_id == student.id, Filled.upload_courses_id == id).first() is not None:
            abort(404)
        render_template('student/feedback_form.html')
    else:
        return redirect(url_for('home'))
