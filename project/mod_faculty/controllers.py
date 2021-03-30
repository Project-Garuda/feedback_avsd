from project.mod_faculty.models import Faculty,Courses,Theory
from project import db_session, bcrypt
from flask import Flask, render_template, request, redirect, url_for, Blueprint, session

mod_faculty = Blueprint('faculty', __name__)

@mod_faculty.route("/", methods=['GET', 'POST'])
def faculty_dashboard():
    if 'user' in session:
        print('hey')
        faculty = Faculty.query.filter(Faculty.id == session['user']).first()
        print(faculty)
        print(faculty.courses[0].course_id)
        return render_template('faculty/faculty_dashboard.html',
        faculty = faculty,
        course_names = Courses,
        )
    else:
        return redirect(url_for('home'))

@mod_faculty.route('/logout')
def logout():
    if('user' in session):
        session.pop('user', None)
    return redirect(url_for('home'))
