from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, current_user
from models import User, Student
from extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    # If they are already logged in as admin, send them straight to the dashboard
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect('/admin/dashboard')
        
    error = None # Create an empty error variable by default
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin':
            admin_user = User.query.filter_by(username='admin').first()
            
            # Create admin if it doesn't exist yet
            if not admin_user:
                admin_user = User(username='admin', role='admin')
                admin_user.set_password('admin123') 
                db.session.add(admin_user)
                db.session.commit()
                
            # Check password
            if admin_user and admin_user.check_password(password):
                login_user(admin_user)
                return redirect('/admin/dashboard')
                
        # If the code reaches this line, the login failed! Set the error message.
        error = "❌ Wrong credentials! Please try again."
    
    # Pass the error variable to the HTML template
    return render_template('admin_login.html', error=error)
@admin_bp.route('/dashboard')
def admin_dashboard():
    # Security check
    if not current_user.is_authenticated or current_user.username != 'admin':
        return redirect('/admin/login')
    
    # Fetch data
    students = Student.query.all()
    jps = User.query.filter(User.role == 'jp').all()
    
    # Render the dedicated HTML file
    return render_template('admin_dashboard.html', students=students, jps=jps)
@admin_bp.route('/students/new', methods=['GET', 'POST'])
def admin_new_student():
    if not current_user.is_authenticated or current_user.username != 'admin':
        return redirect('/admin/login')
    
    if request.method == 'POST':
        student = Student(
            student_name=request.form.get('student_name', ''),
            jp_id=int(request.form.get('jp_id', 1))
        )
        db.session.add(student)
        db.session.commit()
        return redirect('/admin/dashboard')
    
    jps = User.query.filter_by(role='jp').all()
    
    # Pass the JP list to the dedicated HTML file
    return render_template('admin_new_student.html', jps=jps)