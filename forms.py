from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class StudentForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired()]) # Updated!
    guardian_name = StringField('Guardian Name (optional)')
    parent_occupation = StringField('Parent Occupation', validators=[DataRequired()])
    financial_status = SelectField('Financial Status', choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')
    ], validators=[DataRequired()])
    siblings = IntegerField('Number of Siblings', validators=[DataRequired()])
    medical_history = TextAreaField('Medical History')
    hosteller = BooleanField('Hosteller (checked=Yes)')
    screen_time = StringField('Screen Time (ex: 2hrs/day)')
    sleep_pattern = SelectField('Sleep Pattern', choices=[
        ('continuous', 'Continuous'), ('broken', 'Broken/interrupted')
    ])
    jp_observation = TextAreaField('JP Observation')
    submit = SubmitField('Save Student')

class IssueForm(FlaskForm):
    issue_name = StringField('Issue Name', validators=[DataRequired()])
    issue_type = SelectField('Issue Type', choices=[
        ('emotional', 'Emotional'), ('academic', 'Academic'),
        ('behavioral', 'Behavioral'), ('social', 'Social')
    ], validators=[DataRequired()])
    issue_status = SelectField('Status', choices=[
        ('active', 'Active'), ('in_progress', 'In Progress'), ('resolved', 'Resolved')
    ], validators=[DataRequired()])
    issue_date = StringField('Issue Date (YYYY-MM-DD)', validators=[DataRequired()])
    issue_description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save Issue')

class SessionForm(FlaskForm):
    session_number = IntegerField('Session Number', validators=[DataRequired()])
    counselling_status = SelectField('Status', choices=[
        ('Planned', 'Planned'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')
    ])
    session_date = StringField('Date (YYYY-MM-DD)')
    analysis = TextAreaField('Analysis')
    remarks = TextAreaField('Remarks')
    submit = SubmitField('Save Session')