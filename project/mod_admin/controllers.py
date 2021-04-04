from project.mod_faculty.models import Faculty,Courses,Feedback,Theory,Lab,Tutorial,UploadCourses,Admin
from project.mod_student.models import Section,Student,UploadSection
from project import db_session, bcrypt,app,Base,engine,create_engine_models,delete_engine_models
from flask import Flask, render_template, request, redirect, url_for, Blueprint, session,abort,flash
from werkzeug.utils import secure_filename
import os
import openpyxl as op

mod_admin = Blueprint('admin', __name__)

@mod_admin.route("/dashboard/", methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' in session:
        admin = Admin.query.filter(Admin.id == session['admin']).first()
        upload_coures = UploadCourses.query.all()
        return render_template('admin/admin_dashboard.html',
        upload_coures=upload_coures,
        faculty = Faculty,
        course_names = Courses,
        admin = admin,
        )
    else:
        return redirect(url_for('admin_home'))

@mod_admin.route('/logout/')
def logout():
    if('admin' in session):
        session.pop('admin', None)
    return redirect(url_for('admin_home'))

@mod_admin.route("/view/<int:id>", methods=['GET', 'POST'])
def view_responses(id):
    if 'admin' in session:
        my_obj = UploadCourses.query.filter(UploadCourses.id==id).first()
        admin = Admin.query.filter(Admin.id == session['admin']).first()
        if my_obj.course == 0:
            theory = Theory.query.filter(Theory.id == id).first()
            if theory is None:
                abort(404)
            theory_dict = theory.fetch_dict()
            theory_dict['no_respones'] = theory.no_respones
            remarks = Feedback.query.with_entities(Feedback.remark).filter(Feedback.upload_courses_id==id).all()
            print(remarks)
            return render_template('admin/view_responses_theory.html',
            dict=theory_dict,
            admin=admin,
            remarks=remarks,)
        elif my_obj.course==1:
            lab = Lab.query.filter(Lab.id == id).first()
            if lab is None:
                abort(404)
            lab_dict = lab.fetch_dict()
            lab_dict['no_respones'] = lab.no_respones
            remarks = Feedback.query.with_entities(Feedback.remark).filter(Feedback.upload_courses_id==id).all()
            return render_template('admin/view_responses_lab.html',
            dict=lab_dict,
            admin=admin,
            remarks=remarks,)
        else:
            tutorial = Tutorial.query.filter(Lab.id == id).first()
            if tutorial is None:
                abort(404)
            tutorial_dict = lab.fetch_dict()
            tutorial_dict['no_respones'] = tutorial.no_respones
            remarks = Feedback.query.with_entities(Feedback.remark).filter(Feedback.upload_courses_id==id).all()
            return render_template('admin/view_responses_tutorial.html',
            dict=tutorial_dict,
            admin=admin,
            remarks=remarks,)
    else:
        return redirect(url_for('admin_home'))

@mod_admin.route("/upload",methods=['GET','POST'])
def admin_upload():
    if 'admin' in session:
        admin = Admin.query.filter(Admin.id == session['admin']).first()
        if request.method == 'POST':
            files = []
            try:
                for file in request.files:
                    current_file = request.files[file]
                    names=current_file.filename.split('.')
                    name=names[len(names)-1]
                    if current_file:
                        filename = secure_filename(file+'.'+name)
                        files.append(filename)
                        current_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if process_data(files)==1:
                    flash('Data processed successfully')
                    return redirect(url_for('admin.admin_dashboard'))
                else:
                    flash('Error')
                    return redirect(url_for('admin.admin_upload'))
            except Exception as e:
                print(e)
                flash('unknown error')
                return redirect(url_for('admin.admin_upload'))
        else:
            return render_template('admin/admin_upload.html',
            admin=admin,)
    else:
        return redirect(url_for('admin_home'))

def process_data(files):
    admin_objs = Admin.query.all()
    try:
        delete_engine_models()
        create_engine_models()
        for obj in admin_objs:
            db_session.add(Admin(obj.id,obj.name,obj.password))
        db_session.commit()
    except Exception as e:
        print(e)
        flash('Error In Clearing Data')
        return redirect(url_for('admin.admin_upload'))

    wb_obj = op.load_workbook(os.path.join(app.config['UPLOAD_FOLDER'], files[0]))
    sheet_obj = wb_obj.active
    print(sheet_obj.max_row)
    print(sheet_obj.max_column)
    m_row = sheet_obj.max_row
    for i in range(2, m_row+1):
        id = int(sheet_obj.cell(row = i, column = 1).value)
        name = sheet_obj.cell(row = i, column = 2).value
        password = bcrypt.generate_password_hash(str(id)).decode('utf-8')
        db_session.add(Faculty(id,name,password))
    try:
        db_session.commit()
    except Exception as e:
        flash('Error in processing Faculty data')
        return redirect(url_for('admin.admin_upload'))

    wb_obj = op.load_workbook(os.path.join(app.config['UPLOAD_FOLDER'], files[1]))
    sheet_obj = wb_obj.active
    print(sheet_obj.max_row)
    print(sheet_obj.max_column)
    m_row = sheet_obj.max_row
    for i in range(2, m_row+1):
        id = int(sheet_obj.cell(row = i, column = 1).value)
        name = sheet_obj.cell(row = i, column = 2).value
        password = bcrypt.generate_password_hash(str(id)).decode('utf-8')
        db_session.add(Student(id,name,password))
    try:
        db_session.commit()
    except Exception as e:
        flash('Error in processing Student data')
        return redirect(url_for('admin.admin_upload'))

    wb_obj = op.load_workbook(os.path.join(app.config['UPLOAD_FOLDER'], files[2]))
    sheet_obj = wb_obj.active
    print(sheet_obj.max_row)
    print(sheet_obj.max_column)
    m_row = sheet_obj.max_row
    for i in range(2, m_row+1):
        id = sheet_obj.cell(row = i, column = 1).value
        name = sheet_obj.cell(row = i, column = 2).value
        db_session.add(Courses(id,name))
    try:
        db_session.commit()
    except Exception as e:
        flash('Error in processing Course data')
        return redirect(url_for('admin.admin_upload'))

    wb_obj = op.load_workbook(os.path.join(app.config['UPLOAD_FOLDER'], files[3]))
    sheet_obj = wb_obj.active
    print(sheet_obj.max_row)
    print(sheet_obj.max_column)
    m_col = sheet_obj.max_column
    for i in range(1, m_col+1):
        id = sheet_obj.cell(row = 1, column = i).value
        db_session.add(Section(id))
        try:
            db_session.commit()
        except Exception as e:
            flash('Error in processing Upload sections data')
            return redirect(url_for('admin.admin_upload'))
        for j in range(2,m_row+1):
            obj = sheet_obj.cell(row = j, column = i).value
            if obj is None:
                break
            db_session.add(UploadSection(id,int(obj)))
    try:
        db_session.commit()
    except Exception as e:
        flash('Error in processing Upload sections data')
        return redirect(url_for('admin.admin_upload'))
    return 1
