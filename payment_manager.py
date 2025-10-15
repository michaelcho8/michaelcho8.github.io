"""
Tutoring Payment Management System
A Python script to manage student payments, sessions, and billing
"""

import sqlite3
import pandas as pd
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import os

class TutoringPaymentManager:
    def __init__(self, db_path: str = "tutoring_payments.db"):
        """Initialize the payment manager with database connection"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with schema if it doesn't exist"""
        if not os.path.exists(self.db_path):
            # Read and execute the SQL schema
            with open('tutoring_payments.sql', 'r') as f:
                schema = f.read()
            
            conn = sqlite3.connect(self.db_path)
            conn.executescript(schema)
            conn.commit()
            conn.close()
            print(f"Database initialized at {self.db_path}")
        else:
            print(f"Using existing database at {self.db_path}")
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # Student Management Functions
    def add_student(self, name: str, email: str, phone: str = None, 
                   parent_name: str = None, parent_email: str = None, 
                   package_type: str = 'Individual', hourly_rate: float = 50.00) -> int:
        """Add a new student to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO students (name, email, phone, parent_name, parent_email, package_type, hourly_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, email, phone, parent_name, parent_email, package_type, hourly_rate))
            
            student_id = cursor.lastrowid
            conn.commit()
            print(f"Student '{name}' added successfully with ID: {student_id}")
            return student_id
            
        except sqlite3.IntegrityError as e:
            print(f"Error adding student: {e}")
            return None
        finally:
            conn.close()
    
    def get_students(self, active_only: bool = True) -> pd.DataFrame:
        """Get all students as a pandas DataFrame"""
        conn = self.get_connection()
        
        query = "SELECT * FROM students"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_student_by_email(self, email: str) -> Optional[Dict]:
        """Get student information by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM students WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    
    # Session Management Functions
    def add_session(self, student_id: int, session_date: str, start_time: str, 
                   end_time: str, duration_hours: float, subject: str, 
                   session_cost: float, notes: str = None) -> int:
        """Add a new tutoring session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sessions (student_id, session_date, start_time, end_time, 
                                duration_hours, subject, session_cost, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_id, session_date, start_time, end_time, duration_hours, 
              subject, session_cost, notes))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"Session added successfully with ID: {session_id}")
        return session_id
    
    def update_session_status(self, session_id: int, status: str):
        """Update session status (Scheduled, Completed, Cancelled, No-Show)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE sessions SET status = ? WHERE id = ?", (status, session_id))
        conn.commit()
        conn.close()
        
        print(f"Session {session_id} status updated to '{status}'")
    
    def get_sessions(self, student_id: int = None, start_date: str = None, 
                    end_date: str = None) -> pd.DataFrame:
        """Get sessions with optional filtering"""
        conn = self.get_connection()
        
        query = """
            SELECT s.*, st.name as student_name, st.email as student_email
            FROM sessions s
            JOIN students st ON s.student_id = st.id
            WHERE 1=1
        """
        params = []
        
        if student_id:
            query += " AND s.student_id = ?"
            params.append(student_id)
        
        if start_date:
            query += " AND s.session_date >= ?"
            params.append(start_date)
            
        if end_date:
            query += " AND s.session_date <= ?"
            params.append(end_date)
        
        query += " ORDER BY s.session_date DESC, s.start_time DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    # Payment Management Functions
    def add_payment(self, student_id: int, amount: float, payment_method: str,
                   payment_date: str = None, reference_number: str = None, 
                   notes: str = None) -> int:
        """Record a payment from a student"""
        if not payment_date:
            payment_date = date.today().isoformat()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO payments (student_id, payment_date, amount, payment_method, 
                                reference_number, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, payment_date, amount, payment_method, reference_number, notes))
        
        payment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"Payment of ${amount} recorded successfully with ID: {payment_id}")
        return payment_id
    
    def get_payments(self, student_id: int = None, start_date: str = None, 
                    end_date: str = None) -> pd.DataFrame:
        """Get payment records with optional filtering"""
        conn = self.get_connection()
        
        query = """
            SELECT p.*, s.name as student_name, s.email as student_email
            FROM payments p
            JOIN students s ON p.student_id = s.id
            WHERE 1=1
        """
        params = []
        
        if student_id:
            query += " AND p.student_id = ?"
            params.append(student_id)
        
        if start_date:
            query += " AND p.payment_date >= ?"
            params.append(start_date)
            
        if end_date:
            query += " AND p.payment_date <= ?"
            params.append(end_date)
        
        query += " ORDER BY p.payment_date DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    # Reporting Functions
    def get_student_balance(self, student_id: int = None) -> pd.DataFrame:
        """Get student balance summary"""
        conn = self.get_connection()
        
        query = "SELECT * FROM student_balance"
        params = []
        
        if student_id:
            query += " WHERE id = ?"
            params.append(student_id)
        
        query += " ORDER BY balance_due DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_monthly_revenue(self, months: int = 12) -> pd.DataFrame:
        """Get monthly revenue report"""
        conn = self.get_connection()
        
        df = pd.read_sql_query(f"""
            SELECT * FROM monthly_revenue 
            ORDER BY month DESC 
            LIMIT {months}
        """, conn)
        
        conn.close()
        return df
    
    def get_payment_summary(self, months: int = 6) -> pd.DataFrame:
        """Get payment method summary"""
        conn = self.get_connection()
        
        df = pd.read_sql_query(f"""
            SELECT * FROM payment_summary 
            ORDER BY month DESC, total_received DESC
            LIMIT {months * 5}
        """, conn)
        
        conn.close()
        return df
    
    def generate_invoice_data(self, student_id: int, month_year: str) -> Dict[str, Any]:
        """Generate invoice data for a student for a specific month"""
        conn = self.get_connection()
        
        # Get student info
        student_df = pd.read_sql_query(
            "SELECT * FROM students WHERE id = ?", conn, params=[student_id]
        )
        
        if student_df.empty:
            return None
        
        student = student_df.iloc[0]
        
        # Get sessions for the month
        sessions_df = pd.read_sql_query("""
            SELECT * FROM sessions 
            WHERE student_id = ? 
            AND strftime('%Y-%m', session_date) = ?
            AND status = 'Completed'
            ORDER BY session_date
        """, conn, params=[student_id, month_year])
        
        # Get payments for the month
        payments_df = pd.read_sql_query("""
            SELECT * FROM payments 
            WHERE student_id = ? 
            AND strftime('%Y-%m', payment_date) = ?
            ORDER BY payment_date
        """, conn, params=[student_id, month_year])
        
        conn.close()
        
        total_owed = sessions_df['session_cost'].sum() if not sessions_df.empty else 0
        total_paid = payments_df['amount'].sum() if not payments_df.empty else 0
        balance_due = total_owed - total_paid
        
        return {
            'student': student.to_dict(),
            'sessions': sessions_df.to_dict('records'),
            'payments': payments_df.to_dict('records'),
            'summary': {
                'month': month_year,
                'total_sessions': len(sessions_df),
                'total_hours': sessions_df['duration_hours'].sum() if not sessions_df.empty else 0,
                'total_owed': total_owed,
                'total_paid': total_paid,
                'balance_due': balance_due
            }
        }
    
    def export_data(self, table_name: str, file_path: str):
        """Export table data to CSV"""
        conn = self.get_connection()
        
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        df.to_csv(file_path, index=False)
        
        conn.close()
        print(f"Data exported to {file_path}")


# Example usage and CLI interface
def main():
    """Command line interface for the payment manager"""
    pm = TutoringPaymentManager()
    
    print("Tutoring Payment Management System")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Add Student")
        print("2. Add Session")
        print("3. Record Payment")
        print("4. View Student Balances")
        print("5. View Monthly Revenue")
        print("6. Generate Invoice Data")
        print("7. Export Data")
        print("8. View Recent Sessions")
        print("9. View Recent Payments")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-9): ")
        
        try:
            if choice == "1":
                name = input("Student name: ")
                email = input("Student email: ")
                phone = input("Phone (optional): ") or None
                parent_name = input("Parent name (optional): ") or None
                parent_email = input("Parent email (optional): ") or None
                package = input("Package type (Individual/Weekly/Intensive): ") or "Individual"
                rate = float(input("Hourly rate (default 50): ") or 50)
                
                pm.add_student(name, email, phone, parent_name, parent_email, package, rate)
            
            elif choice == "2":
                students_df = pm.get_students()
                print("\nStudents:")
                print(students_df[['id', 'name', 'email']].to_string())
                
                student_id = int(input("Student ID: "))
                session_date = input("Session date (YYYY-MM-DD): ")
                start_time = input("Start time (HH:MM): ")
                end_time = input("End time (HH:MM): ")
                duration = float(input("Duration in hours: "))
                subject = input("Subject: ")
                cost = float(input("Session cost: "))
                notes = input("Notes (optional): ") or None
                
                pm.add_session(student_id, session_date, start_time, end_time, 
                             duration, subject, cost, notes)
            
            elif choice == "3":
                students_df = pm.get_students()
                print("\nStudents:")
                print(students_df[['id', 'name', 'email']].to_string())
                
                student_id = int(input("Student ID: "))
                amount = float(input("Payment amount: "))
                method = input("Payment method (Cash/Check/Venmo/Zelle/Bank Transfer/Other): ")
                ref_num = input("Reference number (optional): ") or None
                notes = input("Notes (optional): ") or None
                
                pm.add_payment(student_id, amount, method, reference_number=ref_num, notes=notes)
            
            elif choice == "4":
                balance_df = pm.get_student_balance()
                print("\nStudent Balances:")
                print(balance_df.to_string(index=False))
            
            elif choice == "5":
                revenue_df = pm.get_monthly_revenue()
                print("\nMonthly Revenue:")
                print(revenue_df.to_string(index=False))
            
            elif choice == "6":
                students_df = pm.get_students()
                print("\nStudents:")
                print(students_df[['id', 'name', 'email']].to_string())
                
                student_id = int(input("Student ID: "))
                month_year = input("Month (YYYY-MM): ")
                
                invoice_data = pm.generate_invoice_data(student_id, month_year)
                if invoice_data:
                    print(f"\nInvoice Data for {invoice_data['student']['name']} - {month_year}")
                    print(f"Total Sessions: {invoice_data['summary']['total_sessions']}")
                    print(f"Total Hours: {invoice_data['summary']['total_hours']}")
                    print(f"Amount Owed: ${invoice_data['summary']['total_owed']}")
                    print(f"Amount Paid: ${invoice_data['summary']['total_paid']}")
                    print(f"Balance Due: ${invoice_data['summary']['balance_due']}")
                else:
                    print("Student not found")
            
            elif choice == "7":
                table = input("Table name (students/sessions/payments): ")
                filename = input("Export filename (e.g., students.csv): ")
                pm.export_data(table, filename)
            
            elif choice == "8":
                sessions_df = pm.get_sessions()
                print("\nRecent Sessions:")
                print(sessions_df[['session_date', 'student_name', 'subject', 'session_cost', 'status']].head(10).to_string(index=False))
            
            elif choice == "9":
                payments_df = pm.get_payments()
                print("\nRecent Payments:")
                print(payments_df[['payment_date', 'student_name', 'amount', 'payment_method']].head(10).to_string(index=False))
            
            elif choice == "0":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")
        
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()