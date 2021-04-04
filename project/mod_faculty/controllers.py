from project.mod_faculty.models import Faculty,Courses,Feedback,Theory,Lab,Tutorial,UploadCourses,Admin
from project.mod_student.models import Section
from project import db_session, bcrypt,app
from flask import Flask, render_template, request, redirect, url_for, Blueprint, session,abort,flash

mod_faculty = Blueprint('faculty', __name__)

@mod_faculty.route("/", methods=['GET', 'POST'])
def faculty_dashboard():
    if 'faculty' in session:
        print('hey')
        faculty = Faculty.query.filter(Faculty.id == session['faculty']).first()
        return render_template('faculty/faculty_dashboard.html',
        faculty = faculty,
        course_names = Courses,
        )
    else:
        return redirect(url_for('home'))


@mod_faculty.route('/logout')
def logout():
    if('faculty' in session):
        session.pop('faculty', None)
    return redirect(url_for('home'))

@mod_faculty.route('/view/<int:id>',methods=['GET', 'POST'])
def view_responses(id):
    if 'faculty' in session:
        my_obj = UploadCourses.query.filter(UploadCourses.id==id).first()
        faculty = Faculty.query.filter(Faculty.id == session['faculty']).first()
        if my_obj.course == 0:
            theory = Theory.query.filter(Theory.id == id).first()
            if theory is None:
                abort(404)
            theory_dict = theory.fetch_dict()
            theory_dict['no_respones'] = theory.no_respones
            remarks = Feedback.query.with_entities(Feedback.remark).filter(Feedback.upload_courses_id==id).all()
            print(remarks)
            return render_template('faculty/view_responses_theory.html',
            dict=theory_dict,
            faculty=faculty,
            remarks=remarks,)
        elif my_obj.course==1:
            lab = Lab.query.filter(Lab.id == id).first()
            if lab is None:
                abort(404)
            lab_dict = lab.fetch_dict()
            lab_dict['no_respones'] = lab.no_respones
            remarks = Feedback.query.with_entities(Feedback.remark).filter(Feedback.upload_courses_id==id).all()
            return render_template('faculty/view_responses_lab.html',
            dict=lab_dict,
            faculty=faculty,
            remarks=remarks,)
        else:
            tutorial = Tutorial.query.filter(Lab.id == id).first()
            if tutorial is None:
                abort(404)
            tutorial_dict = lab.fetch_dict()
            tutorial_dict['no_respones'] = tutorial.no_respones
            remarks = Feedback.query.with_entities(Feedback.remark).filter(Feedback.upload_courses_id==id).all()
            return render_template('faculty/view_responses_tutorial.html',
            dict=tutorial_dict,
            faculty=faculty,
            remarks=remarks,)
    else:
        return redirect(url_for('home'))

@mod_faculty.route('/create',methods=['GET', 'POST'])
def create_course():
    if 'faculty' in session:
        faculty = Faculty.query.filter(Faculty.id == session['faculty']).first()
        if request.method=='POST':
            course_id = request.form['course_id'].upper()
            section_id = request.form['section_id'].upper()
            dict = {'Theory':0, 'Lab':1, 'Tutorial':2}
            type = dict[request.form['type']]
            course = Courses.query.filter(Courses.id == course_id).first()
            section = Section.query.filter(Section.id == section_id).first()
            print("Debug1")
            if course is None:
                flash('Invalid Course ID')
                return redirect(url_for('faculty.create_course'))
            if section is None:
                flash('Invalid Section iD')
                return redirect(url_for('faculty.create_course'))
            print("Debug2")
            try:
                check = UploadCourses.query.filter(UploadCourses.course_id == course_id,
                UploadCourses.section_id == section_id,
                UploadCourses.faculty_id == faculty.id,
                UploadCourses.course  == type).first()
                print("Debug3")
                if check is not None:
                    flash('Course already exists')
                    return redirect(url_for('faculty.create_course'))
                print("Debug4")
                my_obj = UploadCourses(course_id,section_id,faculty.id,type)
                db_session.add(my_obj)
                db_session.commit()
                print('Debug5')
                if type == 0:
                    db_session.add(Theory(my_obj.id))
                elif type==1:
                    db_session.add(Lab(my_obj.id))
                else:
                    db_session.add(Tutorial(my_obj.id))
                db_session.commit()
                print('Debug6')
                flash('Course Created Successfully')
                return redirect(url_for('faculty.faculty_dashboard'))
            except Exception as e:
                print(e)
        else:
            return render_template('faculty/create_course.html',
            faculty=faculty,)
    return redirect(url_for('home'))
