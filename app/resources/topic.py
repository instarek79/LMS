from datetime import datetime
from flask import current_app, flash, jsonify, redirect, request, url_for
from flask_restx import Namespace, Resource, marshal, marshal_with
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
import werkzeug
from ..extentions import db
from ..models import Topic, User, Course, Student, CourseStudentAssociation, Comment
from ..extentions import api
from flask_restx import fields, reqparse
from .student import student_model

ns = Namespace(
    name="Topic Management", path="/api/topics", description="Topics Management Api"
)
topic_model = api.model(
    "Topic",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String(),
        "content": fields.String(),
    },
)

comment_model = api.model(
    "Comment",
    {
        "id": fields.Integer(readonly=True),
        "text": fields.String(),
        "author_name": fields.String(),
        "date_posted": fields.DateTime(),
    },
)


@ns.route("/")
class topic(Resource):
    reqparse = reqparse.RequestParser()
    reqparse.add_argument(
        "topic_id", type=int, help="Topic Id", required=True, location="args"
    )

    @ns.response(401, "Unauthorized")
    @ns.response(404, "Topic Not Found")
    @ns.response(200, "Topic Found", model=topic_model)
    @ns.expect(reqparse, validate=True)
    def get(self):
        if current_user.is_anonymous:
            return {"message": "Unauthorized"}, 401
        get_topic = Topic.query.get_or_404(request.args.get("topic_id"))
        return marshal(get_topic, topic_model)

    reqparse.add_argument("name", type=str, help="Name",
                          required=True, location="json")
    reqparse.add_argument(
        "content", type=str, help="Content", required=True, location="json"
    )

    @ns.expect(reqparse, validate=True)
    def put(self):
        if current_user.is_anonymous:
            return {"message": "Unauthorized"}, 401
        get_topic = Topic.query.get_or_404(request.args.get("topic_id"))
        get_topic.name = ns.payload["name"]
        get_topic.content = ns.payload["content"]
        db.session.commit()
        flash("Topic Edited Successfully", "success")
        return {"message": "Topic Edited"}, 200


@ns.route("/comments")
class commen(Resource):
    reqparse = reqparse.RequestParser()
    reqparse.add_argument(
        "topic_id", type=int, help="Topic Id", required=True, location="args"
    )

    @ns.response(401, "Unauthorized")
    @ns.response(404, "Topic Not Found ")
    @ns.response(200, "Comments Found", model=comment_model, aslist=True)
    @ns.expect(reqparse, validate=True)
    @ns.marshal_list_with(comment_model, mask=None)
    def get(self):
        if current_user.is_anonymous:
            return {"message": "Unauthorized"}, 401
        get_topic = Topic.query.get_or_404(request.args.get("topic_id"))
        return get_topic.comments

    reqparse.add_argument(
        "comment", type=str, help="Comment", required=True, location="json"
    )

    @ns.response(401, "Unauthorized")
    @ns.response(404, "Topic Not Found ")
    @ns.response(200, "Success", comment_model)
    @ns.expect(reqparse)
    def post(self):
        if current_user.is_anonymous:
            return {"message": "Unauthorized"}, 401
        get_topic = Topic.query.get_or_404(request.args.get("topic_id"))
        new_comment = Comment(
            text=ns.payload.get("comment"),
            author_name=current_user.first_name + " " + current_user.last_name,
            author_id=current_user.id,
            topic_id=get_topic.id,
            date_posted=datetime.now(),
        )
        try:
            db.session.add(new_comment)
            db.session.commit()
            flash("Comment Added", "success")
            return ns.marshal(new_comment, comment_model)
        except:
            db.session.rollback()
            flash("Error Occured", "danger")
            return {"response": "Error Occured"}, 500

    @ns.expect(reqparse, validate=True)
    def delete(self):
        if current_user.is_anonymous:
            return {"message": "Unauthorized"}, 401

        get_topic = Topic.query.get_or_404(request.args.get("topic_id"))

        if current_user.role != "professor" or current_user.id != get_topic.course.professor_id:
            return {"message": "Unauthorized"}, 401

        for comment in get_topic.comments:
            db.session.delete(comment)

        db.session.commit()
        flash("Comments Deleted", "success")
        return {"message": "Comments Deleted"}, 200
