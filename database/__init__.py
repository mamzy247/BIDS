#!/usr/bin/env python3
"""
Database initialization script for Baze Internship Database System
"""

import sqlite3
import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def init_database():
    """Initialize the database with schema and sample data"""
    
    # Create database directory if it doesn't exist
    db_dir = os.path.dirname(Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', ''))
    os.makedirs(db_dir, exist_ok=True)
    
    # Connect to database
    db_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read and execute schema
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    cursor.executescript(schema)
    print("✓ Database schema created successfully")
    
    # Insert sample data
    try:
        # Create admin user
        admin_password = generate_password_hash('admin123')
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, phone, user_type)
            VALUES (?, ?, ?, ?, ?)
        """, ('admin@baze.edu.ng', admin_password, 'System Administrator', '08012345678', 'admin'))
        
        # Create sample HOD
        hod_password = generate_password_hash('hod123')
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, phone, user_type)
            VALUES (?, ?, ?, ?, ?)
        """, ('hod.cs@baze.edu.ng', hod_password, 'Dr. John Doe', '08023456789', 'hod'))
        
        hod_user_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO hods (user_id, staff_id, department, designation)
            VALUES (?, ?, ?, ?)
        """, (hod_user_id, 'HOD001', 'Computer Science', 'Head of Department'))
        
        # Create sample student
        student_password = generate_password_hash('student123')
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, phone, user_type)
            VALUES (?, ?, ?, ?, ?)
        """, ('john.smith@baze.edu.ng', student_password, 'John Smith', '08034567890', 'student'))
        
        student_user_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO students (user_id, student_id, department, level, matriculation_number)
            VALUES (?, ?, ?, ?, ?)
        """, (student_user_id, 'BU/CS/20/001', 'Computer Science', '300', 'BU/20/CS/001'))
        
        # Create sample organization supervisor
        supervisor_password = generate_password_hash('supervisor123')
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, phone, user_type)
            VALUES (?, ?, ?, ?, ?)
        """, ('supervisor@techcorp.com', supervisor_password, 'Jane Manager', '08045678901', 'supervisor'))
        
        supervisor_user_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO organization_supervisors (user_id, organization_name, organization_address, position, department)
            VALUES (?, ?, ?, ?, ?)
        """, (supervisor_user_id, 'TechCorp Nigeria', 'Plot 123, Tech Avenue, Abuja', 'HR Manager', 'Human Resources'))
        
        conn.commit()
        print("✓ Sample data inserted successfully")
        
        # Display login credentials
        print("\n" + "="*50)
        print("SAMPLE LOGIN CREDENTIALS:")
        print("="*50)
        print("Admin:")
        print("  Email: admin@baze.edu.ng")
        print("  Password: admin123")
        print("\nHOD:")
        print("  Email: hod.cs@baze.edu.ng")
        print("  Password: hod123")
        print("\nStudent:")
        print("  Email: john.smith@baze.edu.ng")
        print("  Password: student123")
        print("\nOrganization Supervisor:")
        print("  Email: supervisor@techcorp.com")
        print("  Password: supervisor123")
        print("="*50 + "\n")
        
    except sqlite3.IntegrityError as e:
        print(f"✗ Sample data already exists: {e}")
    except Exception as e:
        print(f"✗ Error inserting sample data: {e}")
        conn.rollback()
    finally:
        conn.close()

def reset_database():
    """Drop all tables and recreate the database"""
    response = input("⚠️  This will delete all data. Are you sure? (yes/no): ")
    if response.lower() != 'yes':
        print("Database reset cancelled.")
        return
    
    db_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
    
    # Delete the database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✓ Old database removed")
    
    # Reinitialize
    init_database()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        reset_database()
    else:
        init_database()