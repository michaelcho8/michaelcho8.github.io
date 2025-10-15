# Tutoring Business Management System

A complete system for managing tutoring sessions, student payments, and scheduling using Google Calendar integration and a local SQLite database for payment tracking.

## Features

### 🌐 Website Integration
- **tutoring.html**: Professional tutoring services page with Google Calendar booking
- **Pricing Display**: Clear pricing for Individual ($50/hr), Weekly ($180/month), and Intensive ($380/month) packages
- **Two Booking Options**: Quick Google Calendar booking or detailed consultation form

### 💾 Payment Tracking Database
- **SQLite Database**: Local database for tracking all student and payment information
- **Student Management**: Store student details, contact info, and package preferences
- **Session Tracking**: Record tutoring sessions with dates, times, subjects, and costs
- **Payment Records**: Track all payments with multiple payment methods
- **Reports & Analytics**: Generate balance reports, revenue summaries, and invoices

### 🖥️ Web Admin Interface
- **Dashboard**: Overview of key metrics and outstanding balances
- **Student Management**: Add and view student information
- **Session Recording**: Log completed tutoring sessions
- **Payment Entry**: Record payments from students/parents
- **Reports**: View detailed analytics and generate invoices

## Setup Instructions

### 1. Install Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
# Run this to create the database with sample data
python payment_manager.py
```

This will create `tutoring_payments.db` with the complete schema.

### 3. Google Calendar Setup

1. Go to [Google Calendar](https://calendar.google.com)
2. Create a new calendar for "Tutoring Sessions"
3. Set up booking appointments:
   - Go to Settings & sharing for your tutoring calendar
   - Enable "Make available for booking"
   - Set your availability hours
   - Configure booking settings (duration, buffer times, etc.)
4. Get your booking link and replace the URL in `tutoring.html`

### 4. Start the Web Interface

```bash
# Launch the admin web interface
python app.py
```

Visit `http://localhost:5000` to access the admin dashboard.

## Usage Guide

### For Website Visitors (tutoring.html)
1. **Quick Booking**: Click "Book on Google Calendar" for immediate scheduling
2. **Consultation**: Use "Contact Me First" for detailed discussions
3. **Form Submission**: Fills out email with student requirements

### For Admin Management (Web Interface)

#### Adding Students
1. Go to Students → Add New Student
2. Enter student details, parent contact info, and package type
3. Student gets assigned ID for tracking

#### Recording Sessions
1. Go to Sessions → Record New Session
2. Select student, date, time, and subject
3. System calculates cost based on duration and rate
4. Mark sessions as Completed, Cancelled, or No-Show

#### Recording Payments
1. Go to Payments → Record New Payment
2. Select student and payment details
3. Track payment method (Cash, Check, Venmo, Zelle, etc.)
4. Add reference numbers for checks/transfers

#### Generating Reports
1. Dashboard shows key metrics and outstanding balances
2. Reports page provides detailed analytics
3. Generate monthly invoices for individual students
4. Export data to CSV for external analysis

### Command Line Interface

```bash
# Run the CLI version for quick access
python payment_manager.py
```

Options include:
- Add students and sessions
- Record payments
- View balances and reports
- Export data

## Database Schema

### Tables Created:
- **students**: Student information and contact details
- **sessions**: Individual tutoring session records
- **payments**: Payment tracking with methods and references
- **monthly_packages**: Package-based billing (for future use)

### Key Views:
- **student_balance**: Outstanding balances for each student
- **monthly_revenue**: Revenue and session counts by month
- **payment_summary**: Payment method breakdown by month

## File Structure

```
├── tutoring.html              # Main tutoring services webpage
├── payment_manager.py         # Core payment management system
├── app.py                    # Flask web interface
├── tutoring_payments.sql     # Database schema
├── requirements.txt          # Python dependencies
├── templates/               # Web interface templates
│   ├── base.html
│   ├── dashboard.html
│   ├── students.html
│   ├── add_student.html
│   ├── sessions.html
│   ├── add_session.html
│   ├── payments.html
│   ├── add_payment.html
│   └── reports.html
└── tutoring_payments.db     # SQLite database (created on first run)
```

## Security Notes

- Database is stored locally - ensure regular backups
- Web interface runs locally (localhost) by default
- For production deployment, configure proper security settings
- Change the Flask secret key in `app.py`

## Customization

### Updating Prices
- Edit pricing in `tutoring.html` (display and form options)
- Update default rates in `payment_manager.py`

### Adding Payment Methods
- Modify the payment method options in templates
- Update database constraints in SQL schema

### Google Calendar Integration
- Replace the Google Calendar URL in `tutoring.html` with your actual booking link
- Customize booking availability and duration settings in Google Calendar

## Backup and Export

- Database: `tutoring_payments.db` contains all data
- Export: Use web interface Reports → Export or CLI export functions
- Regular backups recommended for student and payment data

## Support

The system is designed to be self-contained and easy to use. All student data remains on your local system for privacy and security.