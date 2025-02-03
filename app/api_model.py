from .extentions import api
from flask_restx import fields
option_model = api.model('Option', {
    'id': fields.Integer(readonly=True,  description='Option ID'),
    'text': fields.String( description='Option Text'),
    'is_correct': fields.Boolean( description='Indicates whether the option is correct or not'),
    'question_id': fields.Integer( description='Option ID'),
})
keyword_model = api.model('Keyword', {
    'id': fields.Integer(readonly=True,  description='Keyword ID'),
    'name': fields.String( description='Keyword Name'),
    #'questions':fields.Nested(question_model,as_list=True)
})
# Define serializers
question_model = api.model('Question', {
    'id': fields.Integer(readonly=True,  description='Question ID'),
    'title': fields.String( description='Question Title'),
    'description': fields.String( description='Question Description'),
    'language': fields.String( description='Language of the question'),
    'author': fields.String( description='Author of the question'),
    'created_date': fields.Date(readonly=True, description='Date when the question was created'),
    'skill_level': fields.String( enum=['knowledge', 'comprehension', 'application', 'analysis', 'synthesis', 'evaluation'], description='Skill level of the question'),
    'module_title': fields.String( description='Title of the module'),
    'module_number': fields.Integer( description='Number of the module'),
    #'education_degree': fields.String( description='Education degree related to the question'),
    #'level': fields.String( description='Level of the question'),
    'difficulty': fields.String( enum=['very easy', 'easy', 'medium', 'difficult', 'very difficult'], description='Difficulty level of the question'),
    'interaction_type': fields.String( enum=['choice', 'text input'], description='Interaction type of the question'),
    'keywords': fields.List(fields.String, readonly=True, description='List of keywords associated with the question'),
    'options': fields.Nested(option_model, as_list=True,readonly=True),
    'keywords': fields.Nested(keyword_model, as_list=True,readonly=True),
})

quiz_model_creation =api.model('Quiz Creation',{
    'id':fields.Integer(readonly=True,description='Quiz ID'),
    'name':fields.String(description='Quiz Name'),
    'questions':fields.List(fields.Integer,example=[0,1,2,3],description='List of questions ids'),
    'marks':fields.List(fields.Integer,example=[0,1,2,3],description='list of marks per question'),

})


quiz_list_model=api.model('Quizzes List',{
    'id':fields.Integer(readonly=True,description='Quiz ID'),
    'name':fields.String(readonly=True,description='Quiz Name')
})



get_exam=api.model('Exam Check',{
    'found':fields.Boolean(default=True,description="This will be true if the student has an exam to take"),
    'link':fields.String(example="http://asd.com",description='Link to the exam for redirect')
})

user_model=api.model('User Model',{
    'id':fields.Integer(readonly=True),
    'username':fields.String(description='User username'),
    'first_name':fields.String(description='User first name')
})


project_model=api.model('Project Model',{
    'name':fields.String(description='Project Name'),
    'path': fields.String(description='Path to Project')
})

application_model=api.model('Application Model',{
    'name':fields.String(description='Project Name'),
    'path': fields.String(description='Path to Application')
})

algorithm_model=api.model('Algorithm Model',{
    'name':fields.String(description='Algorithm Name'),
    'path': fields.String(description='Path to Algorithm')
})