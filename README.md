# College-ERP
A college management system built using Django framework. It is designed for interactions between students and teachers. Features include attendance, marks and time table.

## Installation

Python and Django need to be installed

```bash
pip install django
```

## Usage

Go to the College-ERP folder and run

```bash
python manage.py runserver
```

Then go to the browser and enter the url **http://127.0.0.1:8000/**


## Login

The login page is common for students and teachers.  
The username is their name and password for everyone is 'project123'.  

Example usernames:  
student- 'samarth'  
teacher- 'trisila'  

You can access the django admin page at **http://127.0.0.1:8000/admin** and login with username 'admin' and the above password.

Also a new admin user can be created using

```bash
python manage.py createsuperuser
```

## Users

New students and teachers can be added through the admin page. A new user needs to be created for each. 

The admin page is used to modify all tables such as Students, Teachers, Departments, Courses, Classes etc.

**For more details regarding the system and features please refer the reports included.**

## Update (29/11/2020)

Added method to reset attendance time range in Django Admin page.

![alt_text](https://i.imgur.com/0xOWmUZ.png)

This is present in Django Admin -> Attendance (http://127.0.0.1:8000/admin/info/attendanceclass/).  
Start Date: Start Date of Attendance period  
End Date: End Date of Attendance period

This will delete all present attendance data and create new attendance objects for the given time range. 

## Update (Session Security & Logout)

Authentication and session handling have been hardened:

- Logging out now fully clears the session (`auth_logout` + `request.session.flush()`) and redirects to the login page, instead of using Django's default logout view.
- The Attendance and Marks pages are decorated with `@never_cache`, so they can no longer be viewed via the browser back button after logging out.
- `LOGIN_URL` and `LOGOUT_REDIRECT_URL` are now set in `settings.py`, so `@login_required` correctly redirects unauthenticated users to `/accounts/login/`.
- All templates use `{% url 'logout' %}` / `{% url 'login' %}` instead of hardcoded paths, so the links won't break if the URL configuration changes.
- A duplicate URL include for the `info` app was removed to fix double-routing issues.

## Update (Admin Directory - Edit & Delete)

The Admin Directory page (`/view-directory/`) now supports full management of Teacher and Student records, restricted to superuser accounts:

- **Edit Teacher / Edit Student**: Inline modal forms let an admin update a person's name, department/class assignment, username and email directly from the directory table. Department and class options are shown as readable dropdowns (e.g. "Computer Science", "Computer Science : 3 A") instead of free-text fields.
- **Delete Teacher / Delete Student**: A confirmation modal allows an admin to permanently remove a Teacher or Student. This deletes the underlying Django `User` account, which cascades to remove all related profile records.
- **Access control**: All four new views require login and `request.user.is_superuser`; non-admin users attempting to access these URLs are redirected to the homepage.
- New URL routes were added under `/admin-list/teacher/edit/<id>/`, `/admin-list/teacher/delete/<id>/`, `/admin-list/student/edit/<usn>/` and `/admin-list/student/delete/<usn>/`.

## Screenshots

### Teacher Page

![alt text](https://imgur.com/pMAoEbG.png)

![alt text](https://imgur.com/ZiQ3RRA.png)

![alt text](https://imgur.com/i025CJW.png)

![alt text](https://imgur.com/HQlLYmC.png)

![alt text](https://imgur.com/j6RyBmU.png)

![alt text](https://imgur.com/xIKEMvQ.png)

![alt text](https://imgur.com/4Rl7Fpv.png)

### Student Page

![alt text](https://imgur.com/isL9cjz.png)

![alt text](https://imgur.com/5pzl7m3.png)

![alt text](https://imgur.com/7zWhHZx.png)

![alt text](https://imgur.com/fu7gxk8.png)

![alt text](https://imgur.com/NZqU268.png)

### Admin Page

![alt text](https://imgur.com/sDvDc9N.png)

![alt text](https://imgur.com/tMKWx6f.png)

![alt text](https://imgur.com/PvCsNeB.png)
