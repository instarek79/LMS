from flask import Blueprint, flash, jsonify, redirect, render_template,request, url_for
from flask_login import login_required
# Create a Blueprint for your routes
home = Blueprint('home', __name__)

app=home

@app.route('/slides')
def method_name():
    return render_template('slides.html')

@app.route('/create-question')
def create_question():
    return render_template('my_index.html')

@app.route('/')
def index():
    return render_template('index.html')    
    

@app.route('/view-questions')
# @login_required
def view_questions():
    return render_template('view_question.html')

@app.route('/create-quiz')
def create_quiz():
    questions=Question.query.all()
    return render_template('create_quiz.html',questions=questions)

@app.route('/question2/<int:id>')
def open_question2(id):
    question=Question.query.filter_by(id=id).first_or_404()
    return render_template('get_question.html',data=question)

@app.route('/question/<int:id>',methods=['GET','POST'])
def open_question(id):
    question=Question.query.filter_by(id=id).first_or_404()
    if request.method=='POST':
        data=request.form
        print(data)
        options=request.form.getlist('options')
        print(options)
        options=set(options)
        correct_options=set(question.correct_options)
        if options==correct_options:
            print(True)
            flash('Correct!','success')
        else:
            print(False)
    return render_template('open_question.html',data=question)

@app.route('/view-quiz/<int:id>')
def view_quiz(id):
    quiz=Quiz.query.filter_by(id=id).first_or_404()
    return render_template('view_quiz.html',quiz=quiz)