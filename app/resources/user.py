from flask import flash, redirect, request, url_for,get_flashed_messages
from flask_restx import Namespace, Resource, marshal, marshal_with
import flask_login
from ..extentions import login_manager, db, bcrypt
from ..models import User,Student
from ..extentions import api
from flask_restx import fields
from ..resources.student import student_model


def init_user():
    @login_manager.user_loader
    def user_loader(user):
        return User.query.get(user)
    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Please login first','info')
        return redirect(url_for('auth.login',next=request.path))
    


login_model = api.model('Login', {
    'username': fields.String(required=True, description='User name'),
    'password': fields.String()
})

user_model = api.model('User Model', {
    'username': fields.String(required=True, description='User username'),
    'password': fields.String(desciprtion='User Password'),
    'email': fields.String(description='User email', example='asd@asd.com'),
    'first_name': fields.String(description='User first name', example='joe'),
    'last_name': fields.String(description='User last name', example='joe')


})


ns = Namespace(name='Authentication', path="/api/user",
               description='User Authentication Functions')


@ns.route('/login')
class login(Resource):
    @ns.response(200, 'Successfully Logged in')
    @ns.response(404, 'User Not Found')
    @ns.response(400, 'Password Incorrect')
    @ns.expect(login_model, mask=None)
    def post(self):
        """Logs in User"""
        user = ns.payload.copy()
        user_password = user.pop('password')
        user_object = User.query.filter_by(**user).first_or_404()
        if user_object:
            if bcrypt.check_password_hash(user_object.password, user_password):
                flask_login.login_user(user_object)
                return 'Successfully Logged in', 200
            else:
                return 'Password Incorrect', 400


@ns.route('/logout')
class logout(Resource):
    @flask_login.login_required
    @ns.response(200, 'User Logged out successfully')
    @ns.response(401, description= "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.")
    def get(self):
        """Logs out User"""
        flask_login.logout_user()
        return 'User Logged out successfully', 200


@ns.route('/create_user')
class create_user(Resource):
    @ns.response(201, 'User Successfully Created')
    @ns.response(500, 'Error Reading Data')
    @ns.expect(user_model)
    def post(self):
        """Creates a new User"""
        try:
            user = ns.payload.copy()
            user['password'] = bcrypt.generate_password_hash(
                user['password'])
            user_object = User(**user)
            db.session.add(user_object)
            db.session.commit()
            return 'User Succesfully Created', 201
        except:
            db.session.rollback()
            return 'Error Reading Data', 500

@ns.route('/get_flash')
class get_message(Resource):
    def get(self):
        return get_flashed_messages(with_categories=True) 
    
@ns.route('/get_id')
class get_id(Resource):
    def get(self):
        return {'id':flask_login.current_user.id} , 200
    
@ns.route('/get_all_students')
class get_all_students(Resource):
    @marshal_with(student_model)    
    def get(self):
        return Student.query.all() , 200
    
