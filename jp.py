from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models import User, Student, Issue, Session
from extensions import db
from forms import StudentForm, IssueForm
from datetime import date, datetime
import uuid

jp_bp = Blueprint('jp', __name__)

@jp_bp.route('/jp/dashboard')
@login_required
def jp_dashboard():
    my_students = Student.query.filter_by(jp_id=current_user.id).all()
    
    # Logic for upcoming sessions
    upcoming_sessions = []
    for student in my_students:
        for issue in student.issues:
            for session in issue.sessions:
                if session.counselling_status == 'Planned' and session.session_date >= datetime.now():
                    upcoming_sessions.append({'session': session, 'issue': issue, 'student': student})
    
    upcoming_sessions.sort(key=lambda x: x['session'].session_date)
    upcoming_sessions = upcoming_sessions[:5]
    
    return render_template('jp_dashboard.html', my_students=my_students, upcoming_sessions=upcoming_sessions)

@jp_bp.route('/student/<int:student_id>')
@login_required
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    if student.jp_id != current_user.id:
        return "<h1 style='color:red;text-align:center;'>❌ Access Denied!</h1>", 403
    
    # --- WE MUST CALCULATE THESE VARIABLES BEFORE RENDERING THE HTML ---
    safe_financial = student.financial_status.title() if student.financial_status else "Not Set"
    safe_occupation = student.parent_occupation or "N/A"
    safe_screen_time = student.screen_time or "N/A"
    safe_sleep_pattern = student.sleep_pattern.title() if student.sleep_pattern else "N/A"
    safe_medical = student.medical_history or "None recorded"
    safe_observation = student.jp_observation or "No notes"
    safe_guardian = student.guardian_name or "None"
    safe_siblings = student.siblings or 0
    hosteller_status = "Yes" if student.hosteller else "No"
    
    # --- NOW WE PASS THEM ALL TO THE TEMPLATE ---
    return render_template('jp_student_detail.html', 
                           student=student,
                           safe_financial=safe_financial,
                           safe_occupation=safe_occupation,
                           safe_screen_time=safe_screen_time,
                           safe_sleep_pattern=safe_sleep_pattern,
                           safe_medical=safe_medical,
                           safe_observation=safe_observation,
                           safe_guardian=safe_guardian,
                           safe_siblings=safe_siblings,
                           hosteller_status=hosteller_status)
@jp_bp.route('/student/new', methods=['GET', 'POST'])
@login_required
def new_student():
    form = StudentForm()
    if form.validate_on_submit():
        new_student = Student(
            student_name=form.student_name.data,
            guardian_name=form.guardian_name.data or None,
            parent_occupation=form.parent_occupation.data,
            financial_status=form.financial_status.data,
            siblings=form.siblings.data,
            medical_history=form.medical_history.data or None,
            hosteller=form.hosteller.data,
            screen_time=form.screen_time.data or None,
            sleep_pattern=form.sleep_pattern.data or None,
            jp_observation=form.jp_observation.data or None,
            jp_id=current_user.id
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect('/jp/dashboard') # Standardized the redirect
    
    # We pass the form to the dedicated HTML file
    return render_template('jp_new_student.html', form=form)
@jp_bp.route('/student/<int:student_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    if student.jp_id != current_user.id:
        return "<h1 style='color:red;text-align:center;'>❌ Access Denied!</h1><a href='/jp/dashboard'>← Back</a>", 403
    
    form = StudentForm(obj=student)
    
    if form.validate_on_submit():
        student.student_name = form.student_name.data
        student.guardian_name = form.guardian_name.data or None
        student.parent_occupation = form.parent_occupation.data
        student.financial_status = form.financial_status.data
        student.siblings = form.siblings.data
        student.medical_history = form.medical_history.data or None
        student.hosteller = form.hosteller.data
        student.screen_time = form.screen_time.data or None
        student.sleep_pattern = form.sleep_pattern.data or None
        student.jp_observation = form.jp_observation.data or None
        
        db.session.commit()
        
        # Smooth redirect back to the student detail page instead of a hardcoded HTML success screen!
        return redirect(f'/student/{student.id}')
    
    return render_template('jp_edit_student.html', form=form, student=student)
@jp_bp.route('/student/<int:student_id>/issues', methods=['GET', 'POST'])
@login_required
def student_issues(student_id):
    student = Student.query.get_or_404(student_id)
    if student.jp_id != current_user.id:
        return "<h1 style='color:red;'>❌ Access Denied!</h1>", 403
    
    issue_form = IssueForm()
    if issue_form.validate_on_submit():
        new_issue = Issue(
            issue_name=issue_form.issue_name.data,
            issue_type=issue_form.issue_type.data,
            issue_status=issue_form.issue_status.data,
            issue_date=datetime.strptime(issue_form.issue_date.data, '%Y-%m-%d').date() if issue_form.issue_date.data else date.today(),
            case_id=str(uuid.uuid4())[:8].upper(),
            issue_description=issue_form.issue_description.data,
            student_id=student.id
        )
        db.session.add(new_issue)
        db.session.commit()
        return redirect(f'/student/{student.id}/issues')
    return render_template('jp_issues.html', issue_form=issue_form, student=student, issues=student.issues)

@jp_bp.route('/issue/<int:issue_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    student = issue.student
    
    # Security check: Ensure JP owns this student
    if student.jp_id != current_user.id:
        return "<h1 style='color:red;text-align:center;'>❌ Access Denied!</h1>", 403
        
    form = IssueForm(obj=issue)
    
    if form.validate_on_submit():
        issue.issue_name = form.issue_name.data
        issue.issue_type = form.issue_type.data
        issue.issue_status = form.issue_status.data
        issue.issue_description = form.issue_description.data
        
        db.session.commit()
        return redirect(f'/student/{student.id}/issues')
        
    return render_template('jp_edit_issue.html', form=form, issue=issue, student=student)
@jp_bp.route('/issue/<int:issue_id>/sessions')
@login_required
def issue_sessions(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    if issue.student.jp_id != current_user.id:
        return "❌ Access Denied!", 403
    return render_template('jp_sessions.html', issue=issue, student=issue.student, sessions=issue.sessions)

@jp_bp.route('/session/new', methods=['POST'])
@login_required
def new_session():
    issue_id = int(request.form['issue_id'])
    issue = Issue.query.get_or_404(issue_id)
    student = issue.student
    
    # Security check: Ensure the JP owns this student
    if student.jp_id != current_user.id:
        return "<h1 style='color:red;text-align:center;'>❌ Access Denied!</h1>", 403
    
    # Create the new session
    new_session = Session(
        session_number=int(request.form['session_number']),
        session_date=datetime.fromisoformat(request.form['session_date'] + ':00'),
        counselling_status=request.form['counselling_status'],
        analysis=request.form.get('analysis', ''),
        remarks=request.form.get('remarks', ''),
        issue_id=issue.id
    )
    db.session.add(new_session)
    
    # --- AUTOMATIC STATUS UPDATE LOGIC ---
    if new_session.counselling_status == 'Completed' and issue.issue_status == 'active':
        issue.issue_status = 'in_progress'
    # -------------------------------------
        
    db.session.commit()
    return redirect(f"/issue/{issue.id}/sessions")