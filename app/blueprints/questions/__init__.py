from datetime import datetime,timedelta
from flask import Blueprint, flash, jsonify, redirect, render_template,request, url_for
from flask_login import current_user, login_required
from app import db
from app.models import Quiz, QuizStudentAssociation
# Create a Blueprint for your routes
questions_blueprint = Blueprint('questions', __name__,url_prefix='/quizzes')

app=questions_blueprint



@app.route('/<int:quiz_id>',methods=['GET', 'POST'])
@login_required
def create_question(quiz_id):
    quiz=Quiz.query.get_or_404(quiz_id)
    if current_user.role=="student" and quiz in current_user.taken_quizzes:
        flash('You have already taken this quiz','danger')
        return redirect(url_for('home.index'))
    if quiz.date-datetime.now()<timedelta(minutes=-30):
        flash('Quiz time already passed','danger')
        return redirect(url_for('home.index'))
    if quiz.date<=datetime.now() and quiz.date-datetime.now()<timedelta(minutes=30):
        if request.method=='POST':
            data=request.form
            print(data)
            marks=0
            for i,questionassociation in enumerate(quiz.questions):
                if questionassociation.question.correct_option==int(data[f"correct_option_{i+1}"]):
                    marks+=int(questionassociation.marks)
            quiz_student =QuizStudentAssociation(quiz_id=int(quiz.id),student_id=int(current_user.id),total_marks=int(marks))
            db.session.add(quiz_student)
            db.session.commit()
            return redirect(url_for('home.index'))
        return render_template('my_index.html',quiz=quiz)

    flash("you cannot access this quiz yet", "danger")
    return redirect(url_for("home.index"))

@app.route('/')
@login_required
def index():
        
    return render_template('course/quizzes.html',QuizStudentAssociation=QuizStudentAssociation)
# @app.route('/view-questions')
# # @login_required
# def view_questions():
#     return render_template('view_question.html')

# @app.route('/create-quiz')
# def create_quiz():
#     questions=Question.query.all()
#     return render_template('create_quiz.html',questions=questions)

# @app.route('/question2/<int:id>')
# def open_question2(id):
#     question=Question.query.filter_by(id=id).first_or_404()
#     return render_template('get_question.html',data=question)

# @app.route('/question/<int:id>',methods=['GET','POST'])
# def open_question(id):
#     question=Question.query.filter_by(id=id).first_or_404()
#     if request.method=='POST':
#         data=request.form
#         print(data)
#         options=request.form.getlist('options')
#         print(options)
#         options=set(options)
#         correct_options=set(question.correct_options)
#         if options==correct_options:
#             print(True)
#             flash('Correct!','success')
#         else:
#             print(False)
#     return render_template('open_question.html',data=question)

# @app.route('/view-quiz/<int:id>')
# def view_quiz(id):
#     quiz=Quiz.query.filter_by(id=id).first_or_404()
#     return render_template('view_quiz.html',quiz=quiz)

# @app.route('/add_quiz_to_topic',methods=["GET","POST"])
# def add_quiz_to_topic():
#     topics=topic.query.all()
#     quizes=Quiz.query.all()
#     if request.method=='POST':
#         topic=request.form.get('topic')
#         quiz=request.form.get('quiz')
#         topic_obj=topic.query.filter_by(id=topic).first_or_404()
#         quiz_obi=Quiz.query.filter_by(id=quiz).first_or_404()
#         topic_quiz=topicQuizAssociation(topic_id=topic_obj.id,quiz_id=quiz_obi.id)
#         db.session.add(topic_quiz)
#         db.session.commit()
#     return render_template('add_lesson.html',lessons=topics,quizes=quizes)