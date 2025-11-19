"""
ColleXo - Database Models
SQLAlchemy ORM models for users, societies, forms, and responses
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication (admin, society, student)"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'society', 'student'), nullable=False, default='society')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    society = db.relationship('Society', backref='owner', uselist=False, lazy=True)
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Society(db.Model):
    """Society model - one registration per society enforced by unique constraints"""
    __tablename__ = 'societies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    short_desc = db.Column(db.String(512))
    long_desc = db.Column(db.Text)
    category = db.Column(db.Enum('cultural', 'technical', 'sports', 'literary', 'social', 'other'), 
                         default='other')
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(20))
    faculty_incharge = db.Column(db.String(255))
    logo_path = db.Column(db.String(512), default='placeholder-logo.png')
    
    # Social media links
    social_instagram = db.Column(db.String(255))
    social_twitter = db.Column(db.String(255))
    social_facebook = db.Column(db.String(255))
    social_linkedin = db.Column(db.String(255))
    website_url = db.Column(db.String(512))
    
    # Status flags
    is_approved = db.Column(db.Boolean, default=False, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    
    # Metrics
    views_count = db.Column(db.Integer, default=0)
    members_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    forms = db.relationship('SocietyForm', backref='society', lazy='dynamic', cascade='all, delete-orphan')
    
    # Unique constraint on name + contact_email
    __table_args__ = (
        db.UniqueConstraint('name', 'contact_email', name='unique_society_registration'),
        db.Index('idx_category', 'category'),
    )
    
    def __repr__(self):
        return f'<Society {self.name}>'
    
    def to_dict(self, include_forms=False):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'short_desc': self.short_desc,
            'long_desc': self.long_desc,
            'category': self.category,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'faculty_incharge': self.faculty_incharge,
            'logo_path': self.logo_path,
            'social_links': {
                'instagram': self.social_instagram,
                'twitter': self.social_twitter,
                'facebook': self.social_facebook,
                'linkedin': self.social_linkedin,
                'website': self.website_url
            },
            'is_approved': self.is_approved,
            'is_active': self.is_active,
            'views_count': self.views_count,
            'members_count': self.members_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_forms:
            data['forms'] = [form.to_dict() for form in self.forms.filter_by(is_active=True).all()]
        
        return data


class SocietyForm(db.Model):
    """Dynamic forms created by societies for recruitment/registration"""
    __tablename__ = 'society_forms'
    
    id = db.Column(db.Integer, primary_key=True)
    society_id = db.Column(db.Integer, db.ForeignKey('societies.id', ondelete='CASCADE'), 
                          nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    form_schema = db.Column(db.JSON, nullable=False)  # Stores field definitions
    is_active = db.Column(db.Boolean, default=True, index=True)
    max_submissions = db.Column(db.Integer, nullable=True)  # NULL = unlimited
    submissions_count = db.Column(db.Integer, default=0)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    responses = db.relationship('FormResponse', backref='form', lazy='dynamic', 
                               cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SocietyForm {self.title}>'
    
    def is_accepting_submissions(self):
        """Check if form is currently accepting submissions"""
        if not self.is_active:
            return False
        
        now = datetime.utcnow()
        
        if self.start_date and now < self.start_date:
            return False
        
        if self.end_date and now > self.end_date:
            return False
        
        if self.max_submissions and self.submissions_count >= self.max_submissions:
            return False
        
        return True
    
    def get_schema(self):
        """Parse JSON schema"""
        if isinstance(self.form_schema, str):
            return json.loads(self.form_schema)
        return self.form_schema
    
    def to_dict(self, include_responses=False):
        data = {
            'id': self.id,
            'society_id': self.society_id,
            'title': self.title,
            'description': self.description,
            'form_schema': self.get_schema(),
            'is_active': self.is_active,
            'is_accepting_submissions': self.is_accepting_submissions(),
            'max_submissions': self.max_submissions,
            'submissions_count': self.submissions_count,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_responses:
            data['responses'] = [resp.to_dict() for resp in self.responses.all()]
        
        return data


class FormResponse(db.Model):
    """Student submissions to society forms"""
    __tablename__ = 'form_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('society_forms.id', ondelete='CASCADE'), 
                       nullable=False, index=True)
    submission_data = db.Column(db.JSON, nullable=False)  # Stores field responses
    submitter_email = db.Column(db.String(255), nullable=False, index=True)
    submitter_name = db.Column(db.String(255))
    submitter_phone = db.Column(db.String(20))
    files_json = db.Column(db.JSON, nullable=True)  # Uploaded file metadata
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    honeypot_value = db.Column(db.String(255))  # Anti-bot field
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Unique constraint to prevent duplicate submissions
    __table_args__ = (
        db.UniqueConstraint('form_id', 'submitter_email', name='unique_submission'),
    )
    
    def __repr__(self):
        return f'<FormResponse {self.id} for Form {self.form_id}>'
    
    def get_submission_data(self):
        """Parse JSON submission data"""
        if isinstance(self.submission_data, str):
            return json.loads(self.submission_data)
        return self.submission_data
    
    def get_files_data(self):
        """Parse JSON files data"""
        if not self.files_json:
            return []
        if isinstance(self.files_json, str):
            return json.loads(self.files_json)
        return self.files_json
    
    def to_dict(self):
        return {
            'id': self.id,
            'form_id': self.form_id,
            'submission_data': self.get_submission_data(),
            'submitter_email': self.submitter_email,
            'submitter_name': self.submitter_name,
            'submitter_phone': self.submitter_phone,
            'files': self.get_files_data(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
