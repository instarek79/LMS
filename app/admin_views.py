import uuid
from flask_admin.contrib.sqla import ModelView
import pandas as pd
from wtforms import (
    PasswordField,
    FileField,
    SelectField,
    StringField,
    SelectMultipleField,
)
from wtforms.validators import DataRequired
from .extentions import  db, bcrypt
from .models import  Course, EnrollYear, Faculty, Professor, Student
from flask_login import current_user
from flask import flash, redirect, request, url_for
from werkzeug.utils import secure_filename
from flask_admin import expose,AdminIndexView,BaseView,Admin
from wtforms.validators import DataRequired
import os
from flask_admin.contrib.fileadmin import FileAdmin
import plotly.express as px

class MyAdminIndexView(AdminIndexView):
        def is_accessible(self):
            return current_user.is_authenticated and current_user.role=='admin'

        def inaccessible_callback(self, name, **kwargs):
            # Redirect to login page if user is not authenticated
            return redirect(url_for('auth.login',next=request.url))
        @expose('/', methods=['GET', 'POST'])
        def index(self):
            # Logic to handle both GET and POST requests
            try:
                x, y = zip(*[(faculty.name, len(faculty.students)) for faculty in Faculty.query.all()])

                fig = px.bar(x=x, y=y, labels={'x': 'Faculty', 'y': 'Student Counts'},title="Faculties")
                fig.update_layout(title_x=0.5,title_font_size=25,margin=dict(l=0, r=0, t=50, b=0))

                plot=fig.to_html(full_html=False)
            except:
                plot=None
            

            return self.render('admin/index.html',plot1=plot)

admin=Admin(name='AdminPage',index_view=MyAdminIndexView(),template_mode='bootstrap4')
def load_admin_views():
   
    class BaseVieww(ModelView):
        create_modal = True
        edit_modal = True
        can_export = True

        def is_accessible(self):
            return current_user.is_authenticated and current_user.role == "admin"

        def inaccessible_callback(self, name, **kwargs):
            # redirect to login page if user doesn't have access
            return redirect(url_for("auth.login", next=request.url))



    class StudentView(BaseVieww):
        # column_display_all_relations=True

        column_searchable_list = ["first_name", "last_name", "email"]
        form_excluded_columns = [
            "role",
            "viewed_topics",
            "taken_quizzes",
            "comments",
            "courses",
        ]
        column_list = [
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "faculty",
            "enrolled_at",
        ]

        def on_model_change(self, form, user, is_created):
            if is_created:  # Check if a new user is being created
                user.password = bcrypt.generate_password_hash(form.password.data)

        def is_accessible(self):
            return current_user.is_authenticated and current_user.role == "admin"

        def inaccessible_callback(self, name, **kwargs):
            # redirect to login page if user doesn't have access
            return redirect(url_for("auth.login", next=request.url))

    class FacultyView(BaseVieww):
    
        column_list = ["name", "professors", "students", "courses"]
        pass

    class CourseView(BaseVieww):
        can_export = True
        create_modal = True
        edit_modal = True
        column_list = [
            "name",
            "description",
            "image",
            "professor",
            "faculty",
        ]
        form_excluded_columns = ["topics", "quizzes", "image", "students"]
        form_extra_fields = {"image": FileField("image", validators=[DataRequired()])}

        def on_model_change(self, form, user, is_created):
            if is_created:  # Check if a new user is being created
                img = form.image.data
                name = secure_filename(
                    str(uuid.uuid4()) + "." + img.filename.split(".")[-1]
                )
                img.save(f"app/static/courseimages/{name}")
                user.image = f"/static/courseimages/{name}"

    class ProfessorView(BaseVieww):
        form_excluded_columns = [
            "role",
            "created_quizzes",
            "created_questions",
            "comments",
        ]
        column_list = [
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "faculty",
            "managed_courses",
        ]

        def on_model_change(self, form, user, is_created):
            if is_created:  # Check if a new user is being created
                user.password = bcrypt.generate_password_hash(form.password.data)

    class enrollYearView(BaseVieww):
        form_excluded_columns = [
            "students",
        ]


    class AddStudentCourse(BaseVieww):
        can_create = None
        can_export = True
        can_delete = False

        def edit_form(self, obj=None):
            print(obj)
            form = super(AddStudentCourse, self).edit_form(obj)
            form.students.query = Student.query.filter_by(faculty_id=obj.faculty_id)
            return form

        column_list = ["name", "students"]

        form_widget_args = {"faculty": {"disabled": True}}
        form_excluded_columns = [
            "name",
            "professor",
            "topics",
            "quizzes",
            "description",
            "image",
            "faculty",
        ]

    class UserCSVUploadView(BaseVieww):
        @expose('/', methods=['GET', 'POST'])
        def index(self):
            if request.method == 'POST':
                file = request.files['csv_file']
                if not file:
                    flash('No file provided', 'error')
                    return redirect(url_for('.index'))

                # Read the CSV file using pandas
                try:
                    df = pd.read_csv(file)
                    for index, row in df.iterrows():
                        row["password"] = bcrypt.generate_password_hash(row["password"])
                        try:
                            name=row.pop("faculty")
                            row["faculty_id"]=Faculty.query.filter_by(name=name).first().id
                        except Exception as e:
                            flash(f'Error faculty "{name}" does not exist!', 'error')
                            return self.render('admin/upload.html')
                        try:
                            row["enrollyear_id"]=EnrollYear.query.filter_by(year=int(row.pop("enrolled_at"))).first().id
                        except:
                            flash(f'Error Enroll Year Must be created first!', 'error')
                            return self.render('admin/upload.html')
                        print(row)
                        user = Student(**row)
                        db.session.add(user)
                    db.session.commit()
                    flash(f'{len(df)} users created successfully', 'success')
                except Exception as e:
                    flash(f'Error processing file: {e}', 'error')
                    db.session.rollback()

                return redirect(url_for('.index'))

            return self.render('admin/upload.html')
    
    admin.add_view(StudentView(Student, db.session,category="Users"))
    admin.add_view(ProfessorView(Professor, db.session,category="Users"))
    admin.add_view(UserCSVUploadView(Student, db.session,endpoint="UploadStudents",name="Upload Students",category="Users"))

    admin.add_view(CourseView(Course, db.session,category="Courses"))
    admin.add_view(
        AddStudentCourse(
            Course, db.session, name="Add student in courses", endpoint="StudentCourse",category="Courses"
        )
    )
    admin.add_view(FacultyView(Faculty, db.session,name="Faculties"))
    admin.add_view(enrollYearView(EnrollYear, db.session))
    path = os.path.join(os.path.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

  

