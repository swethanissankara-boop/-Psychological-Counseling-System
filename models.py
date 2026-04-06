from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(20))
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Student(db.Model):     
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100)) # Updated!
    guardian_name = db.Column(db.String(100), nullable=True)
    parent_occupation = db.Column(db.String(50))
    financial_status = db.Column(db.String(20))
    siblings = db.Column(db.Integer)
    medical_history = db.Column(db.Text)
    hosteller = db.Column(db.Boolean, default=False)
    screen_time = db.Column(db.String(20))
    sleep_pattern = db.Column(db.String(50))
    jp_observation = db.Column(db.Text)
    jp_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    jp = db.relationship('User', backref='students')
    issues = db.relationship('Issue', backref='student')

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_name = db.Column(db.String(100))
    issue_type = db.Column(db.String(50))
    issue_status = db.Column(db.String(20), default='Active')
    issue_date = db.Column(db.Date)
    case_id = db.Column(db.String(10), unique=True)
    issue_description = db.Column(db.Text)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_number = db.Column(db.Integer, nullable=False)
    counselling_status = db.Column(db.String(20))          
    analysis = db.Column(db.Text)                          
    remarks = db.Column(db.Text)                           
    session_date = db.Column(db.DateTime, nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    issue = db.relationship('Issue', backref='sessions', lazy=True)