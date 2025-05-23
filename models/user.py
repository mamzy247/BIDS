"""
User model for authentication and base user functionality
"""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import sqlite3
from flask import g

class User(UserMixin):
    """Base User class for all user types"""
    
    def __init__(self, id, email, full_name, phone, user_type, is_active=True, 
                 created_at=None, last_login=None):
        self.id = id
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.user_type = user_type
        self.is_active = is_active
        self.created_at = created_at
        self.last_login = last_login
    
    @staticmethod
    def get(user_id):
        """Get user by ID"""
        db = g.get('db')
        cursor = db.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        )
        row = cursor.fetchone()
        
        if row:
            return User(
                id=row['id'],
                email=row['email'],
                full_name=row['full_name'],
                phone=row['phone'],
                user_type=row['user_type'],
                is_active=row['is_active'],
                created_at=row['created_at'],
                last_login=row['last_login']
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        db = g.get('db')
        cursor = db.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE email = ?',
            (email,)
        )
        row = cursor.fetchone()
        
        if row:
            return User(
                id=row['id'],
                email=row['email'],
                full_name=row['full_name'],
                phone=row['phone'],
                user_type=row['user_type'],
                is_active=row['is_active'],
                created_at=row['created_at'],
                last_login=row['last_login']
            )
        return None
    
    @staticmethod
    def authenticate(email, password):
        """Authenticate user with email and password"""
        db = g.get('db')
        cursor = db.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE email = ? AND is_active = 1',
            (email,)
        )
        row = cursor.fetchone()
        
        if row and check_password_hash(row['password_hash'], password):
            # Update last login
            cursor.execute(
                'UPDATE users SET last_login = ? WHERE id = ?',
                (datetime.now(), row['id'])
            )
            db.commit()
            
            return User(
                id=row['id'],
                email=row['email'],
                full_name=row['full_name'],
                phone=row['phone'],
                user_type=row['user_type'],
                is_active=row['is_active'],
                created_at=row['created_at'],
                last_login=datetime.now()
            )
        return None
    
    def create(self, password):
        """Create a new user"""
        db = g.get('db')
        cursor = db.cursor()
        
        password_hash = generate_password_hash(password)
        
        try:
            cursor.execute(
                '''INSERT INTO users (email, password_hash, full_name, phone, user_type)
                   VALUES (?, ?, ?, ?, ?)''',
                (self.email, password_hash, self.full_name, self.phone, self.user_type)
            )
            db.commit()
            self.id = cursor.lastrowid
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update(self, **kwargs):
        """Update user information"""
        db = g.get('db')
        cursor = db.cursor()
        
        allowed_fields = ['full_name', 'phone', 'is_active']
        update_fields = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                update_fields.append(f'{field} = ?')
                values.append(value)
        
        if update_fields:
            values.append(self.id)
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            db.commit()
            
            # Update object attributes
            for field, value in kwargs.items():
                if field in allowed_fields:
                    setattr(self, field, value)
    
    def change_password(self, new_password):
        """Change user password"""
        db = g.get('db')
        cursor = db.cursor()
        
        password_hash = generate_password_hash(new_password)
        cursor.execute(
            'UPDATE users SET password_hash = ? WHERE id = ?',
            (password_hash, self.id)
        )
        db.commit()
    
    def log_activity(self, action, entity_type=None, entity_id=None, 
                     ip_address=None, user_agent=None):
        """Log user activity"""
        db = g.get('db')
        cursor = db.cursor()
        
        cursor.execute(
            '''INSERT INTO activity_logs 
               (user_id, action, entity_type, entity_id, ip_address, user_agent)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (self.id, action, entity_type, entity_id, ip_address, user_agent)
        )
        db.commit()
    
    def get_notifications(self, unread_only=False):
        """Get user notifications"""
        db = g.get('db')
        cursor = db.cursor()
        
        if unread_only:
            cursor.execute(
                '''SELECT * FROM notifications 
                   WHERE user_id = ? AND is_read = 0 
                   ORDER BY created_at DESC''',
                (self.id,)
            )
        else:
            cursor.execute(
                '''SELECT * FROM notifications 
                   WHERE user_id = ? 
                   ORDER BY created_at DESC''',
                (self.id,)
            )
        
        return cursor.fetchall()
    
    def mark_notification_read(self, notification_id):
        """Mark a notification as read"""
        db = g.get('db')
        cursor = db.cursor()
        
        cursor.execute(
            '''UPDATE notifications 
               SET is_read = 1, read_at = ? 
               WHERE id = ? AND user_id = ?''',
            (datetime.now(), notification_id, self.id)
        )
        db.commit()
    
    @property
    def is_student(self):
        return self.user_type == 'student'
    
    @property
    def is_hod(self):
        return self.user_type == 'hod'
    
    @property
    def is_supervisor(self):
        return self.user_type == 'supervisor'
    
    @property
    def is_admin(self):
        return self.user_type == 'admin'
    
    def get_profile_data(self):
        """Get additional profile data based on user type"""
        db = g.get('db')
        cursor = db.cursor()
        
        if self.is_student:
            cursor.execute(
                'SELECT * FROM students WHERE user_id = ?',
                (self.id,)
            )
        elif self.is_hod:
            cursor.execute(
                'SELECT * FROM hods WHERE user_id = ?',
                (self.id,)
            )
        elif self.is_supervisor:
            cursor.execute(
                'SELECT * FROM organization_supervisors WHERE user_id = ?',
                (self.id,)
            )
        else:
            return None
        
        return cursor.fetchone()
    
    def __repr__(self):
        return f'<User {self.email}>'