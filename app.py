"""
Simple Flask web interface for tutoring payment management
Run with: python app.py
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from payment_manager import TutoringPaymentManager
import pandas as pd
from datetime import datetime, date
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Initialize payment manager
pm = TutoringPaymentManager()

@app.route('/')
def dashboard():
    """Main dashboard showing overview"""
    try:
        # Get key metrics
        balance_df = pm.get_student_balance()
        revenue_df = pm.get_monthly_revenue(6)
        
        total_outstanding = balance_df['balance_due'].sum()
        total_students = len(balance_df)
        current_month_revenue = revenue_df.iloc[0]['revenue'] if not revenue_df.empty else 0
        
        return render_template('dashboard.html', 
                             total_outstanding=total_outstanding,
                             total_students=total_students,
                             current_month_revenue=current_month_revenue,
                             balance_df=balance_df,
                             revenue_df=revenue_df)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('dashboard.html')

@app.route('/students')
def students():
    """Student management page"""
    students_df = pm.get_students()
    return render_template('students.html', students=students_df)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """Add new student"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form.get('phone') or None
            parent_name = request.form.get('parent_name') or None
            parent_email = request.form.get('parent_email') or None
            package_type = request.form.get('package_type', 'Individual')
            hourly_rate = float(request.form.get('hourly_rate', 50))
            
            student_id = pm.add_student(name, email, phone, parent_name, 
                                      parent_email, package_type, hourly_rate)
            
            if student_id:
                flash(f'Student {name} added successfully!', 'success')
            else:
                flash('Error adding student. Email may already exist.', 'error')
                
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        return redirect(url_for('students'))
    
    return render_template('add_student.html')

@app.route('/sessions')
def sessions():
    """Session management page"""
    sessions_df = pm.get_sessions()
    return render_template('sessions.html', sessions=sessions_df)

@app.route('/add_session', methods=['GET', 'POST'])
def add_session():
    """Add new session"""
    if request.method == 'POST':
        try:
            student_id = int(request.form['student_id'])
            session_date = request.form['session_date']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            duration_hours = float(request.form['duration_hours'])
            subject = request.form['subject']
            session_cost = float(request.form['session_cost'])
            notes = request.form.get('notes') or None
            
            session_id = pm.add_session(student_id, session_date, start_time, 
                                      end_time, duration_hours, subject, 
                                      session_cost, notes)
            
            flash(f'Session added successfully!', 'success')
                
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        return redirect(url_for('sessions'))
    
    students_df = pm.get_students()
    return render_template('add_session.html', students=students_df)

@app.route('/update_session_status/<int:session_id>/<status>')
def update_session_status(session_id, status):
    """Update session status"""
    try:
        pm.update_session_status(session_id, status)
        flash(f'Session status updated to {status}', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('sessions'))

@app.route('/payments')
def payments():
    """Payment management page"""
    payments_df = pm.get_payments()
    return render_template('payments.html', payments=payments_df)

@app.route('/add_payment', methods=['GET', 'POST'])
def add_payment():
    """Add new payment"""
    if request.method == 'POST':
        try:
            student_id = int(request.form['student_id'])
            amount = float(request.form['amount'])
            payment_method = request.form['payment_method']
            payment_date = request.form.get('payment_date') or date.today().isoformat()
            reference_number = request.form.get('reference_number') or None
            notes = request.form.get('notes') or None
            
            payment_id = pm.add_payment(student_id, amount, payment_method,
                                      payment_date, reference_number, notes)
            
            flash(f'Payment of ${amount} recorded successfully!', 'success')
                
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        return redirect(url_for('payments'))
    
    students_df = pm.get_students()
    return render_template('add_payment.html', students=students_df)

@app.route('/reports')
def reports():
    """Reports page"""
    balance_df = pm.get_student_balance()
    revenue_df = pm.get_monthly_revenue(12)
    payment_summary_df = pm.get_payment_summary(12)
    
    return render_template('reports.html', 
                         balance_df=balance_df,
                         revenue_df=revenue_df,
                         payment_summary_df=payment_summary_df)

@app.route('/invoice/<int:student_id>/<month_year>')
def generate_invoice(student_id, month_year):
    """Generate invoice for student"""
    try:
        invoice_data = pm.generate_invoice_data(student_id, month_year)
        if invoice_data:
            return render_template('invoice.html', invoice=invoice_data)
        else:
            flash('Student not found or no data for this period', 'error')
            return redirect(url_for('reports'))
    except Exception as e:
        flash(f'Error generating invoice: {str(e)}', 'error')
        return redirect(url_for('reports'))

# API endpoints for AJAX calls
@app.route('/api/students')
def api_students():
    """API endpoint to get students as JSON"""
    students_df = pm.get_students()
    return jsonify(students_df.to_dict('records'))

@app.route('/api/student_balance')
def api_student_balance():
    """API endpoint to get student balances"""
    balance_df = pm.get_student_balance()
    return jsonify(balance_df.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)