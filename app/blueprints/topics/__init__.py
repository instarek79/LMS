import glob
from importlib import import_module
import os
from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
    Blueprint,
)
from flask_login import current_user, login_required
import os
from app.extentions import db
import urllib.parse
import subprocess
import pandas as pd
import json
from app.models import Course, Student, Topic

topics = Blueprint(
    "topics",
    __name__,
    "static",
    url_prefix="/courses",
    template_folder="app/blueprints/topics/templates",
)


app = topics
app.jinja_loader.searchpath.append("app/blueprints/topics/templates")


@app.route("/")
@login_required
def index():
        return render_template("course/std_course.html")


@app.route("/managment/")
@login_required
def managment():
        if current_user.role == "professor":
            return render_template("course/prof_course_home.html")
        else:
            flash("Unauthorized access", "danger")
            return redirect(url_for("home.index"))

@app.route("/<string:domain>/")
@login_required
def home(domain):

    # Replace with your actual root directory path
    headings = []
    # Get list of folders and HTML files
    print(current_user.role)
    # try:
    if current_user.role == "student":
        for course in current_user.courses:
            if course.name == domain:
                course=course
                for topic in course.topics:
                    headings.append(topic)
    elif current_user.role=="professor":
        for course in current_user.managed_courses:
            if course.name==domain:
                course=course
                for topic in course.topics:
                    headings.append(topic)
     
    # except:
        # abort(404)
    return render_template("topics/topics.html", chapters=headings, domain=domain,course=course)


@app.route("/add_document", methods=["GET", "POST"])
def add_document():
    domains = Domain.query.all()
    topics = Topic.query.all()
    if request.method == "POST":
        domain = Domain.query.filter_by(name=request.form.get("domain")).first_or_404()
        topic_name = f"{len(domain.topics)+1}. {request.form.get('topic')}"
        print(domain.topics)

        doc = request.form.get("ckeditor")
        directory = (
            "app/blueprints/topics/templates/docs/"
            + request.form.get("domain")
            + "/"
            + topic_name
        )

        file_path = directory + ".html"

        # Write the HTML content to a file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(str(doc))

        topic_obj = Topic(name=topic_name, domain_id=domain.id)
        try:

            db.session.add(topic_obj)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)
        # from app import update_db
        # update_db()
        flash("Successfully added", "success")
        return jsonify({"response": "Successful"})

    return render_template("topics/add.html", domains=domains, topics=topics)


@app.route("/get_docs/<string:lesson_name>")
def get_docs(lesson_name):
    # if current_user.is_authenticated:

    content = Topic.query.filter_by(name=lesson_name).first_or_404().content
    return content
    # else:
    #     return "<h1>405 Method Not Allowed. Please log in first! </h1>",405


@app.route("/edit/<path:page>", methods=["GET", "POST"])
@login_required
def edit_page(page):
    if current_user.role == "admin":
        if request.method == "POST":
            doc = request.form.get("ckeditor")
            directory = (
                "app/blueprints/topics/templates/docs/"
                + request.form.get("domain")
                + "/"
                + request.form.get("topic")
            )
            # directory = 'path/to/directory'
            if str(request.form.get("name")) != "":
                file_name = str(request.form.get("name")) + ".html"
            else:
                return render_template("add.html"), 500

            file_path = os.path.join(directory, file_name)

            # Check if the directory exists, create it if not
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Write the HTML content to a file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(str(doc))
        return render_template("topics/edit_page.html", page=page)
    else:
        flash("You do not have access to this page!", "danger")
        return redirect(url_for("home.index"))


@app.route("/load_projects/<string:project_name>")
def load_projects(project_name):
    project_name = str(project_name).strip()
    project_obj = Project.query.filter_by(name=project_name).first_or_404()
    module_name = (
        f"app.blueprints.topics.projects.{project_obj.topic.domain.name}.{project_name}"
    )
    imported_module = import_module(module_name)
    head = imported_module.head
    content = imported_module.content
    project = imported_module.project

    return render_template("projects/test.html", projs=head, body=content, file=project)


@app.route("/load_project_slides/<string:project_name>")
def load_projects_slides(project_name):
    project_name = project_name.strip()
    project_obj = Project.query.filter_by(name=project_name).first_or_404()
    project_name = str(project_name)
    module_name = (
        f"app.blueprints.topics.projects.{project_obj.topic.domain.name}.{project_name}"
    )
    imported_module = import_module(module_name)
    head = imported_module.head
    content = imported_module.content
    project = imported_module.project

    return render_template(
        "projects/slides_test.html", projs=head, body=content, file=project
    )


@app.route("/load_algorithms/<string:algorithm_name>")
def load_algorithm(algorithm_name):
    algorithm_name = str(algorithm_name)

    return render_template(
        "algorithms/algorithm.html", ckcontent=f"algorithms/{algorithm_name}.html"
    )


@app.route("/add_projects", methods=["GET", "POST"])
def add_projects():
    domains = Domain.query.all()
    topics = Topic.query.all()

    if request.method == "POST":
        py_file = request.files.get("project")
        name = request.form.get("name")
        topic = request.form.get("topic")
        print(py_file.filename)
        if py_file.filename == "":
            flash("File Not Found!", "danger")
            return redirect(request.url)
        if name == "":
            flash("Name Missing!", "danger")
            return redirect(request.url)
        if topic == "":
            flash("Topic Missing!", "danger")
            return redirect(request.url)
        else:
            lesson_obj = Topic.query.filter_by(name=topic).first_or_404()
            py_file.save(f"app/blueprints/topics/projects/{name}.py")
            # asd=urllib.parse.quote_plus("%20".join(name.split()))
            # print(asd)
            project = Project(
                name=name,
                path=f"/topics//load_projects/{name}",
                lesson_id=lesson_obj.id,
            )
            db.session.add(project)
            db.session.commit()

    return render_template(
        "/projects/add_projects.html", domains=domains, topics=topics
    )


@app.route("/delete_lesson/<string:lesson_name>", methods=["POST"])
def delete_lesson(lesson_name):
    topic_obj = Topic.query.filter_by(name=lesson_name).first_or_404()
    if os.path.exists(
        f"app/blueprints/topics/templates/docs/{topic_obj.domain.name}/{topic_obj.name}.html"
    ):
        os.remove(
            f"app/blueprints/topics/templates/docs/{topic_obj.domain.name}/{topic_obj.name}.html"
        )
    topic_obj.quizzes.clear()
    db.session.delete(topic_obj)
    db.session.commit()
    # from app import update_db
    # update_db()
    flash("Successfully Deleted", "success")
    return jsonify({"message": "Success"})


@app.route("/add_algorithm", methods=["GET", "POST"])
def add_algorithm():
    domains = Domain.query.all()
    if request.method == "POST":
        document = request.form.get("ckeditor")
        topic = request.form.get("lesson")
        topic_obj = Topic.query.filter_by(name=topic).first_or_404()
        name = request.form.get("name")
        file_path = f"app/blueprints/topics/templates/algorithms/{name}.html"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(str(document))
        alg_obj = Algorithm(
            name=name, path=f"/topics/load_algorithms/{name}", topic_id=topic_obj.id
        )
        db.session.add(alg_obj)
        db.session.commit()
        flash("Successfully added algorithm", "success")
        return jsonify({"message": "success"}), 200
    return render_template("/algorithms/add_algorithm.html", domains=domains)


@app.route("/delete_algorithms/<string:algorithm_name>", methods=["POST"])
def delete_algorithm(algorithm_name):
    alg_obj = Algorithm.query.filter_by(name=algorithm_name).first_or_404()
    db.session.delete(alg_obj)
    db.session.commit()
    os.remove(f"app/blueprints/topics/templates/algorithms/{algorithm_name}.html")
    flash("Deleted algorithm succesffully", "info")
    return jsonify({"message": "success"}), 200


@app.route("/projects-jupyter/<string:project_name>")
def projects_jupyter(project_name):
    Folder_Path = "app/blueprints/topics/projects_jupyter"
    subprocess.Popen(
        f".venv\Scripts\python.exe -m jupyter notebook --no-browser --ip {request.host.split(':')[0]} --port 8888 --notebook-dir={Folder_Path} --ServerApp.token='' --ServerApp.password=''"
    )
    proj = Project.query.filter_by(name=project_name).first_or_404()
    print(request.host.split(":")[0])
    return redirect(
        f"http://{request.host.split(':')[0]}:8888/notebooks/{project_name}.ipynb"
    )


@app.route("/load_notebook")
def method_name():
    import nbformat
    from nbconvert import HTMLExporter

    notebook_name = "Apply Identity Transform"
    # Open the .ipynb file and load it as a JSON object
    with open(
        f"app/blueprints/topics/templates/notebooks/{notebook_name}.ipynb",
        "r",
        encoding="utf-8",
    ) as f:
        notebook_json = json.load(f)
    return render_template(
        "notebook_temp.html", notebook_name=notebook_name, notebook_data=notebook_json
    )
    # with open(f"app/blueprints/topics/templates/notebooks/{notebook_name}.ipynb", 'r', encoding='utf-8') as f:
    #     notebook = nbformat.read(f, as_version=4)

    # html_exporter = HTMLExporter(theme='light')

    # # Convert the notebook to HTML
    # (body, resources) = html_exporter.from_notebook_node(notebook)
    # print(resources)
    # return body
