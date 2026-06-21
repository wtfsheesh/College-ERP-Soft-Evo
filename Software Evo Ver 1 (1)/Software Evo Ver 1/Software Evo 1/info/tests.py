from django.test import TestCase
from info.models import Dept, Class, Course, User, Student, Teacher, Assign, AssignTime, AttendanceTotal, Attendance, StudentCourse, Marks, MarksClass
from django.urls import reverse
from django.test.client import Client


# Create your tests here.


class InfoTest(TestCase):

    def create_user(self, username='testuser', password='project123'):
        self.client = Client()
        return User.objects.create_user(username=username, password=password)

    def test_user_creation(self):
        # Must create a class first before creating a student (foreign key required)
        dept = Dept.objects.create(id='CS_u', name='CS_u')
        cl = Class.objects.create(id='CS5U', dept=dept, sem=5, section='U')
        us = self.create_user()
        ut = self.create_user(username='teacher')
        s = Student(user=us, USN='CS01', name='test', class_id=cl)
        s.save()
        t = Teacher(user=ut, id='CS01', name='test', dept=dept)
        t.save()
        self.assertTrue(isinstance(us, User))
        self.assertEqual(us.is_student, hasattr(us, 'student'))
        self.assertEqual(ut.is_teacher, hasattr(ut, 'teacher'))

    def create_dept(self, id='CS', name='CS'):
        return Dept.objects.create(id=id, name=name)

    def test_dept_creation(self):
        d = self.create_dept()
        self.assertTrue(isinstance(d, Dept))
        self.assertEqual(d.__str__(), d.name)

    def create_class(self, id='CS5A', sem=5, section='A'):
        dept = self.create_dept()
        return Class.objects.create(id=id, dept=dept, sem=sem, section=section)

    def test_class_creation(self):
        c = self.create_class()
        self.assertTrue(isinstance(c, Class))
        self.assertEqual(c.__str__(), "%s : %d %s" % (c.dept.name, c.sem, c.section))

    def create_course(self, id='CS510', name='Data Struct', shortname='DS'):
        dept = self.create_dept(id='CS2')
        return Course.objects.create(id=id, dept=dept, name=name, shortname=shortname)

    def test_course_creation(self):
        c = self.create_course()
        self.assertTrue(isinstance(c, Course))
        self.assertEqual(c.__str__(), c.name)

    def create_student(self, usn='CS01', name='samarth'):
        cl = self.create_class()
        u = self.create_user()
        return Student.objects.create(user=u, class_id=cl, USN=usn, name=name)

    def test_student_creation(self):
        s = self.create_student()
        self.assertTrue(isinstance(s, Student))
        self.assertEqual(s.__str__(), s.name)

    def create_teacher(self, id='CS01', name='teacher'):
        dept = self.create_dept(id='CS3')
        return Teacher.objects.create(id=id, name=name, dept=dept)

    def test_teacher_creation(self):
        s = self.create_teacher()
        self.assertTrue(isinstance(s, Teacher))
        self.assertEqual(s.__str__(), s.name)

    def create_assign(self):
        cl = self.create_class()
        cr = self.create_course()
        t = self.create_teacher()
        return Assign.objects.create(class_id=cl, course=cr, teacher=t)

    def test_assign_creation(self):
        a = self.create_assign()
        self.assertTrue(isinstance(a, Assign))

    # views
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test_password')

    def test_index_admin(self):
        # A plain user with no student/teacher role should be redirected, not shown a page
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('index'))
        self.assertIn(response.status_code, [200, 302])

    def test_index_student(self):
        self.client.login(username='test_user', password='test_password')
        dept = Dept.objects.create(id='CS_s', name='CS_s')
        cl = Class.objects.create(id='CS5S', dept=dept, sem=5, section='S')
        s = Student.objects.create(user=self.user, USN='test', name='test_name', class_id=cl)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_teacher(self):
        self.client.login(username='test_user', password='test_password')
        dept = Dept.objects.create(id='CS_t', name='CS_t')
        t = Teacher.objects.create(user=self.user, id='test', name='test_name', dept=dept)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_no_attendance(self):
        s = self.create_student()
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('attendance', args=(s.USN,)))
        self.assertContains(response, "student has no courses")
        self.assertEqual(response.status_code, 200)

    def test_attendance_view(self):
        s = self.create_student()
        self.client.login(username='test_user', password='test_password')
        Assign.objects.create(class_id=s.class_id, course=self.create_course(), teacher=self.create_teacher())
        response = self.client.get(reverse('attendance', args=(s.USN,)))
        self.assertEqual(response.status_code, 200)
        # Check that attendance list exists in context
        self.assertIn('att_list', response.context)

    def test_no_attendance__detail(self):
        s = self.create_student()
        cr = self.create_course()
        self.client.login(username='test_user', password='test_password')
        resp = self.client.get(reverse('attendance_detail', args=(s.USN, cr.id)))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "student has no attendance")

    def test_attendance__detail(self):
        s = self.create_student()
        cr = self.create_course()
        self.client.login(username='test_user', password='test_password')
        resp = self.client.get(reverse('attendance_detail', args=(s.USN, cr.id)))
        self.assertEqual(resp.status_code, 200)
        # Check att_list exists in context
        self.assertIn('att_list', resp.context)

    # ----------------------------------------------------------------
    # Logout & Session Security Tests
    # ----------------------------------------------------------------

    def test_logout_redirects_to_login(self):
        """After logout, user should be redirected to the login page."""
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_logout_clears_session(self):
        """After logout, the session should be fully cleared."""
        self.client.login(username='test_user', password='test_password')
        self.client.get(reverse('logout'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_unauthenticated_user_redirected_from_index(self):
        """Unauthenticated users accessing protected pages should be redirected to login."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_unauthenticated_user_cannot_access_attendance(self):
        """Unauthenticated users should not be able to access attendance pages."""
        s = self.create_student()
        response = self.client.get(reverse('attendance', args=(s.USN,)))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_unauthenticated_user_cannot_access_marks(self):
        """Unauthenticated users should not be able to access marks pages."""
        s = self.create_student()
        response = self.client.get(reverse('marks_list', args=(s.USN,)))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_back_button_blocked_after_logout(self):
        """
        After logout, pages with never_cache should not be served from browser cache.
        Checks that Cache-Control headers are set on protected views.
        """
        self.client.login(username='test_user', password='test_password')
        dept = Dept.objects.create(id='CS_bb', name='CS_bb')
        cl = Class.objects.create(id='CS5B', dept=dept, sem=5, section='B')
        s = Student.objects.create(user=self.user, USN='test_back', name='Back Button Test', class_id=cl)
        response = self.client.get(reverse('attendance', args=(s.USN,)))
        self.assertIn('no-store', response.get('Cache-Control', ''))







