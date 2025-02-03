from flask import Flask, Response
from .extentions import db, api, login_manager
from .resources import  user, courses,student,quizzes,topic
from .blueprints.home import home
from .blueprints.topics import topics
from .blueprints.user import login_blueprint
from .blueprints.questions import questions_blueprint
# from .blueprints.courses import courses_blueprint
from .admin_views import load_admin_views, admin
import os
from jinja_markdown2 import MarkdownExtension
from flask_restx import Api

def register_app_config(app: Flask):
    app.config["FLASK_ADMIN_SWATCH"] = "litera"
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir,  'project.db')}"
)
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", ""
    )
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
        "SECURITY_PASSWORD_SALT", ""
    )
    app.config.from_prefixed_env(".env")

def register_extensions(app: Flask):
    login_manager.init_app(app)
    user.init_user()
    db.init_app(app)
    api.init_app(app)
    admin.init_app(app)
    load_admin_views()

def register_api_namespaces(api: Api):
    api.add_namespace(user.ns)
    api.add_namespace(courses.ns)
    api.add_namespace(student.ns)
    api.add_namespace(quizzes.ns)
    api.add_namespace(topic.ns)

def register_blueprint(app: Flask):
    app.register_blueprint(home)
    app.register_blueprint(topics)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(questions_blueprint)
    # app.register_blueprint(courses_blueprint)
def create_app():
    app = Flask(__name__)
    register_app_config(app)
    register_blueprint(app)
    register_extensions(app)
    register_api_namespaces(api)
    with app.app_context():
        pass
        # update_db()
    @app.after_request
    def add_cache_control(response: Response):
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    app.jinja_env.add_extension(MarkdownExtension)
    return app


def update_db():
    from .models import Domain, Topic

    try:
        Domain.__table__.drop(db.engine)
        Topic.__table__.drop(db.engine)
    except:
        print("Tables do not exist or error")

    db.create_all()

    import os
    import glob

    root_directory = f"app/blueprints/topics/templates/docs/"
    # Get list of folders and HTML files
    # try:
    if True:
        for domain_name in os.listdir(root_directory):
            domain_path = os.path.join(root_directory, domain_name)
            new_domain = Domain(name=str(domain_name))
            db.session.add(new_domain)
            db.session.commit()
            files_sorted = sorted(
                os.listdir(domain_path), key=lambda x: int(x.split(".")[0])
            )

            for topic_name in files_sorted:
                topic_path = os.path.join(domain_path, topic_name)
                if os.path.exists(topic_path):
                    new_topic = Topic(
                        name=topic_name.split(".html")[0], domain_id=new_domain.id
                    )
                    db.session.add(new_topic)
                    db.session.commit()
                    html_files = glob.glob(os.path.join(topic_path, "*.html"))
        print("**Succesfully Loaded lessons**")
    # except:
    #     print('Error Loading Database Files')
    #     print('Skipped updating Database')


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
