from project import app
import unittest
from flask import url_for, request
from base import BaseTestCase
from project.mod_faculty.models import Faculty,Courses , Feedback, Theory, Lab, Tutorial, UploadCourses, Admin
from project.mod_student.models import Student,Section,UploadSection
"""All the testcases for checking the app"""
class TestLogin(BaseTestCase):

    def test_student_login(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '1801083', secretkey= '1801083', role = 'student'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('student.student_dashboard', _external=True))

    def test_faculty_login(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('faculty.faculty_dashboard', _external=True))

    def test_admin_login(self):
        with self.app.test_client() as c:
            response = c.post('/admin', data=dict(login_username = '3801081', secretkey= '3801081'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('admin.admin_dashboard', _external=True))

    def test_invalid_faculty_login(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '380', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Login failed!", response.data)

    def test_invalid_student_login(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '380', secretkey= '2801083', role = 'student'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Login failed!", response.data)

    def test_invalid_admin_login(self):
        with self.app.test_client() as c:
            response = c.post('/admin', data=dict(login_username = '380', secretkey= '2801083'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Login failed!", response.data)

class TestLogOut(BaseTestCase):

    def test_if_logout_redirects_to_login_student(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '1801083', secretkey= '1801083', role = 'student'))
            self.assertEqual(response.status_code, 302)
            response = c.get(url_for('student.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)
            self.assert_template_used('index.html')

    def test_if_logout_redirects_to_login_faculty(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get(url_for('faculty.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)
            self.assert_template_used('index.html')

    def test_if_logout_redirects_to_login_admin(self):
        with self.app.test_client() as c:
            response = c.post('/admin', data=dict(login_username = '3801081', secretkey= '3801081'))
            self.assertEqual(response.status_code, 302)
            response = c.get(url_for('admin.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)
            self.assert_template_used('admin_index.html')


class TestInvalidAccess(BaseTestCase):
    def test_invalid_access_faculty(self):
        with self.app.test_client() as c:
            response = c.get('/faculty',follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/faculty/logout',follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/faculty/view/1',follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/faculty/create',follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/faculty/change', follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/faculty/delete', follow_redirects = True)
            self.assert_template_used('index.html')

    def test_invalid_access_student(self):
        with self.app.test_client() as c:
            response = c.get('/student',follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/student/logout',follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/student/view/1',follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/student/create',follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/student/change', follow_redirects = True)
            self.assert_template_used('index.html')
            response = c.get('/student/delete', follow_redirects = True)
            self.assert_template_used('index.html')

    def test_invalid_access_admin(self):
        with self.app.test_client() as c:
            response = c.get('/admin',follow_redirects = True)
            self.assert_template_used('admin_index.html')
            response = c.get('/admin/logout',follow_redirects = True)
            self.assert_template_used('admin_index.html')
            response = c.get('/admin/view/1',follow_redirects = True)
            self.assert_template_used('admin_index.html')
            response = c.get('/admin/create',follow_redirects = True)
            self.assert_template_used('admin_index.html')
            response = c.get('/admin/change', follow_redirects = True)
            self.assert_template_used('admin_index.html')
            response = c.get('/admin/delete', follow_redirects = True)
            self.assert_template_used('admin_index.html')

class TestFacultyControllers(BaseTestCase):

    def test_create_course_theory(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.post('/faculty/create', data=dict(course_id = 'CS351', section_id = 'CG31', type = 'Theory'), follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Course Created Successfully", response.data)
            self.assert_template_used('faculty/faculty_dashboard.html')
            check = UploadCourses.query.filter(
                        UploadCourses.course_id == 'CS351',
                        UploadCourses.section_id == 'CG31',
                        UploadCourses.faculty_id == '2801083',
                        UploadCourses.course == 0
                    ).first()
            theory = Theory.query.filter(check.id == Theory.id).first()
            self.assertNotEqual(check, None)
            self.assertNotEqual(theory, None)

    def test_create_course_lab(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.post('/faculty/create', data=dict(course_id = 'CS351', section_id = 'CG31', type = 'Lab'), follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Course Created Successfully", response.data)
            self.assert_template_used('faculty/faculty_dashboard.html')
            check = UploadCourses.query.filter(
                        UploadCourses.course_id == 'CS351',
                        UploadCourses.section_id == 'CG31',
                        UploadCourses.faculty_id == '2801083',
                        UploadCourses.course == 1
                    ).first()
            lab = Lab.query.filter(check.id == Lab.id).first()
            self.assertNotEqual(check, None)
            self.assertNotEqual(lab, None)

    def test_create_course_tutorial(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.post('/faculty/create', data=dict(course_id = 'CS351', section_id = 'CG31', type = 'Tutorial'), follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Course Created Successfully", response.data)
            self.assert_template_used('faculty/faculty_dashboard.html')
            check = UploadCourses.query.filter(
                        UploadCourses.course_id == 'CS351',
                        UploadCourses.section_id == 'CG31',
                        UploadCourses.faculty_id == '2801083',
                        UploadCourses.course == 2
                    ).first()
            tutorial = Tutorial.query.filter(check.id == Tutorial.id).first()
            self.assertNotEqual(check, None)
            self.assertNotEqual(tutorial, None)

    def test_create_course_invalid_course(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.post('/faculty/create', data=dict(course_id = 'CS352', section_id = 'CG31', type = 'Theory'), follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Invalid Course ID", response.data)
            self.assert_template_used('faculty/create_course.html')
            check = UploadCourses.query.filter(
                        UploadCourses.course_id == 'CS352',
                        UploadCourses.section_id == 'CG31',
                        UploadCourses.faculty_id == '2801083',
                        UploadCourses.course == 0
                    ).first()
            self.assertEqual(check, None)

    def test_create_course_invalid_section(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.post('/faculty/create', data=dict(course_id = 'CS351', section_id = 'CG32', type = 'Theory'), follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Invalid Section ID", response.data)
            self.assert_template_used('faculty/create_course.html')
            check = UploadCourses.query.filter(
                        UploadCourses.course_id == 'CS352',
                        UploadCourses.section_id == 'CG32',
                        UploadCourses.faculty_id == '2801083',
                        UploadCourses.course == 0
                    ).first()
            self.assertEqual(check, None)

    def test_create_course_already_existing_course(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.post('/faculty/create', data=dict(course_id = 'CS350', section_id = 'CG31', type = 'Theory'), follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Course already exists", response.data)
            self.assert_template_used('faculty/create_course.html')
            check = UploadCourses.query.filter(
                        UploadCourses.course_id == 'CS350',
                        UploadCourses.section_id == 'CG31',
                        UploadCourses.faculty_id == '2801083',
                        UploadCourses.course == 0
                    ).count()
            self.assertEqual(check, 1)

    def test_view_responses_invalid_id(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get('/faculty/view/69420')
            self.assertEqual(response.status_code, 404)

    def test_view_responses_theory(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get('/faculty/view/4',  follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assert_template_used('faculty/view_responses_theory.html')

    def test_view_responses_lab(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get('/faculty/view/2',  follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assert_template_used('faculty/view_responses_lab.html')

    def test_view_responses_tutorial(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get('/faculty/view/3',  follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assert_template_used('faculty/view_responses_tutorial.html')

    def test_delete_course(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            response = c.get('/faculty/delete/1', follow_redirects = True)
            self.assert_template_used('faculty/faculty_dashboard.html')
            self.assertIn(b"Course Deleted Successfully", response.data)

    def test_change_password_faculty(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801083', role = 'faculty'),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = c.post('/faculty/change', data=dict(old_pass = '2801083', new_pass = '2801084'),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Successfully updated the password",response.data)
            response = c.get(url_for('faculty.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)
            response = c.post('/', data=dict(login_username = '2801083', secretkey= '2801084', role = 'faculty'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('faculty.faculty_dashboard', _external=True))
            response = c.post('/faculty/change', data=dict(old_pass = '2801084', new_pass = '2801083'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('faculty.faculty_dashboard', _external=True))
            response = c.get(url_for('faculty.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)

class TestAdminControllers(BaseTestCase):

    def test_add_user(self):
        with self.app.test_client() as c:
            response = c.post('/admin', data=dict(login_username = '3801081', secretkey= '3801081'))
            self.assertEqual(response.status_code, 302)
            response = c.post('/admin/add', data=dict(id = '1901037',name='pushpa',section='CG31', role = 'student'),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"User added Successfully",response.data)
            response = c.post('/admin/add', data=dict(id = '2901037', name='sukumar', role = 'faculty'),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"User added Successfully",response.data)
            self.assert_template_used('admin/admin_dashboard.html')
            check = Student.query.filter(Student.id=='1901037',Student.name == 'pushpa').first()
            self.assertNotEqual(check, None)
            check = UploadSection.query.filter(UploadSection.id=='CG31',UploadSection.student_id=='1901037').first()
            self.assertNotEqual(check, None)
            check = Faculty.query.filter(Faculty.id=='2901037',Faculty.name == 'sukumar').first()
            self.assertNotEqual(check, None)

    def test_change_password_admin(self):
        with self.app.test_client() as c:
            response = c.post('/admin', data=dict(login_username = '3801081', secretkey= '3801081'),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = c.post('/admin/change', data=dict(old_pass = '3801081', new_pass = '3801082'),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Successfully updated the password",response.data)
            response = c.get(url_for('admin.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)
            response = c.post('/admin', data=dict(login_username = '3801081', secretkey= '3801082'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('admin.admin_dashboard', _external=True))
            response = c.post('/admin/change', data=dict(old_pass = '3801082', new_pass = '3801081'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('admin.admin_dashboard', _external=True))
            response = c.get(url_for('admin.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)

    def test_toggle_status(self):
        with self.app.test_client() as c:
            response = c.post('/admin', data=dict(login_username = '3801081', secretkey= '3801081'),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(app.config['feedback_status'],1)
            response = c.get('/admin/toggle',follow_redirects=True)
            self.assertEqual(app.config['feedback_status'],0)
            self.assert_template_used('admin/admin_dashboard.html')

class TestStudentControllers(BaseTestCase):

    def test_change_password_student(self):
        with self.app.test_client() as c:
            response = c.post('/', data=dict(login_username = '1801083', secretkey= '1801083', role = 'student'),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = c.post('/student/change', data=dict(old_pass = '1801083', new_pass = '1801084'),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Successfully updated the password",response.data)
            response = c.get(url_for('student.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)
            response = c.post('/', data=dict(login_username = '1801083', secretkey= '1801084', role = 'student'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('student.student_dashboard', _external=True))
            response = c.post('/student/change', data=dict(old_pass = '1801084', new_pass = '1801083'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, url_for('student.student_dashboard', _external=True))
            response = c.get(url_for('student.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You have been logged out", response.data)

if __name__ == '__main__':
    unittest.main()
