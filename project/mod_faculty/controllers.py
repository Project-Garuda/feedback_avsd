from project.mod_faculty.models import Faculty,Courses,Feedback,Theory,Lab,Tutorial,UploadCourses,Admin
from project import db_session, bcrypt,app
from flask import Flask, render_template, request, redirect, url_for, Blueprint, session,abort

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

@app.route("/admin/dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    if 'user' in session:
        admin = Admin.query.filter(Admin.id == session['user']).first()
        upload_coures = UploadCourses.query.all()
        return render_template('admin/admin_dashboard.html',
        upload_coures=upload_coures,
        faculty = Faculty,
        course_names = Courses,
        admin = admin,
        )
    else:
        return redirect(url_for('home'))

@mod_faculty.route('/logout')
def logout():
    if('user' in session):
        session.pop('user', None)
    return redirect(url_for('home'))

@mod_faculty.route('/view/<int:id>',methods=['GET', 'POST'])
def view_responses(id):
    if 'user' in session:
        my_obj = UploadCourses.query.filter(UploadCourses.id==id).first()
        faculty = Faculty.query.filter(Faculty.id == session['user']).first()
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
