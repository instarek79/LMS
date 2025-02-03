from .extentions import db
from datetime import date, datetime
from flask_login import UserMixin, current_user
from sqlalchemy import Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite
from sqlalchemy import ForeignKey, CheckConstraint
from typing import Optional


class EnrollYear(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(nullable=False,unique=True)
    students: Mapped[list["Student"]] = db.relationship()

    def __repr__(self):
        return f"Year {self.year} / {self.year + 1}"


class Faculty(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    professors: Mapped[list["Professor"]] = db.relationship(
        "Professor", back_populates="faculty"
    )
    students: Mapped[list["Student"]] = db.relationship(
        "Student", back_populates="faculty"
    )

    courses: Mapped[list["Course"]] = db.relationship(
        "Course", back_populates="faculty"
    )

    def __repr__(self):
        return f"Faculty of {self.name}"


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    comments: Mapped[Optional[list["Comment"]]] = db.relationship(
        "Comment",
    )
    role: Mapped[str]
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "role",
    }

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    # return dict of user attributes


class Student(User):
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculty.id"))
    enrollyear_id: Mapped[int] = mapped_column(ForeignKey("enroll_year.id"))
    enrolled_at: Mapped["EnrollYear"] = db.relationship(
        "EnrollYear", back_populates="students"
    )
    faculty: Mapped["Faculty"] = db.relationship("Faculty", back_populates="students")
    courses: Mapped[Optional[list["Course"]]] = db.relationship(
        "Course", secondary="course_student_association", back_populates="students"
    )
    viewed_topics: Mapped[Optional[list["Topic"]]] = db.relationship(
        "Topic", secondary="student_topic_view"
    )
    taken_quizzes: Mapped[Optional[list["Quiz"]]] = db.relationship(
        "Quiz", secondary="quiz_student_association"
    )
    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


class Professor(User):
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    managed_courses: Mapped[Optional[list["Course"]]] = db.relationship(
        "Course", back_populates="professor"
    )
    created_quizzes: Mapped[list["Quiz"]] = db.relationship("Quiz", backref="author")
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculty.id"))
    faculty: Mapped["Faculty"] = db.relationship("Faculty", back_populates="professors")
    created_questions: Mapped[list["Question"]] = db.relationship(
        "Question", backref="author"
    )
    __mapper_args__ = {
        "polymorphic_identity": "professor",
    }


class Admin(User):
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }


class Course(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    image: Mapped[str] = mapped_column(String(200), nullable=False)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculty.id"))
    faculty: Mapped["Faculty"] = db.relationship("Faculty", back_populates="courses")
    students: Mapped[list["Student"]] = db.relationship(
        "Student", secondary="course_student_association", back_populates="courses"
    )
    professor_id: Mapped[int] = mapped_column(ForeignKey("professor.id"),nullable=True)
    professor: Mapped["Professor"] = db.relationship(
        "Professor", back_populates="managed_courses"
    )

    topics: Mapped[Optional[list["Topic"]]] = db.relationship(
        "Topic", back_populates="course"
    )
    quizzes: Mapped[Optional[list["Quiz"]]] = db.relationship(
        "Quiz", secondary="quiz_course_assosciation"
    )

    def __repr__(self):

        return f"{self.name}"


class CourseStudentAssociation(db.Model):
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    grade: Mapped[int] = mapped_column(default=0)


class Topic(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    # very long text content
    content: Mapped[str] = mapped_column(Text, nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    course: Mapped["Course"] = db.relationship("Course", back_populates="topics")
    comments: Mapped[Optional[list["Comment"]]] = db.relationship(
        "Comment",
    )

    def __repr__(self):
        return f"{self.name}"


class StudentTopicView(db.Model):
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topic.id"), primary_key=True)


class Question(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("professor.id"))
    option_1: Mapped[str] = mapped_column(String(200), nullable=False)
    option_2: Mapped[str] = mapped_column(String(200), nullable=False)
    option_3: Mapped[str] = mapped_column(String(200), nullable=False)
    option_4: Mapped[str] = mapped_column(String(200), nullable=False)
    correct_option: Mapped[int] = mapped_column(
        CheckConstraint("correct_option>0 and correct_option<5")
    )
    quizzes: Mapped[list["QuizQuestionAssosciation"]] = db.relationship(
        "QuizQuestionAssosciation", back_populates="question"
    )

    def __repr__(self):
        return f"{self.text}"


class Quiz(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("professor.id"))
    marks: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column()
    questions: Mapped[list["QuizQuestionAssosciation"]] = db.relationship(
        "QuizQuestionAssosciation",
        back_populates="quiz",
        cascade="all, delete-orphan",
    )
    students: Mapped[list["Student"]] = db.relationship(
        "Student", secondary="quiz_student_association", back_populates="taken_quizzes"
    )

    # course=Mapped["Course"]=db.relationship("Course",back_populates="quizzes")
    def __repr__(self):
        return f"{self.name}"


class QuizQuestionAssosciation(db.Model):
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"), primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("question.id"), primary_key=True
    )
    marks: Mapped[int] = mapped_column(nullable=False, default=1)
    quiz: Mapped["Quiz"] = db.relationship("Quiz", back_populates="questions")
    question: Mapped["Question"] = db.relationship("Question", back_populates="quizzes")


class QuizStudentAssociation(db.Model):
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"), primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    total_marks: Mapped[int] = mapped_column()


class QuestionStudentAssociation(db.Model):
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"), primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("question.id"), primary_key=True
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    marks_obtained: Mapped[int] = mapped_column()


class QuizCourseAssosciation(db.Model):
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"), primary_key=True)


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    date_posted: Mapped[datetime] = mapped_column(
        default=datetime.now(), nullable=False
    )
    author_name: Mapped[str] = mapped_column(nullable=False)
    topic_id = mapped_column(ForeignKey("topic.id"))
    author_id = mapped_column(ForeignKey("user.id"))
