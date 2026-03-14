#!/usr/bin/env python3
"""
Forms for BranchFit application using Flask-WTF.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange
from wtforms.widgets import TextArea

class RegistrationForm(FlaskForm):
    """User registration form."""
    
    first_name = StringField('First Name', validators=[
        DataRequired(message="First name is required"),
        Length(min=2, max=50, message="First name must be between 2 and 50 characters")
    ])
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message="Last name is required"),
        Length(min=2, max=50, message="Last name must be between 2 and 50 characters")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address"),
        Length(max=255, message="Email must be less than 255 characters")
    ])
    
    student_id = StringField('Student ID', validators=[
        Optional(),
        Length(max=50, message="Student ID must be less than 50 characters")
    ])
    
    college = StringField('College/University', validators=[
        Optional(),
        Length(max=200, message="College name must be less than 200 characters")
    ])
    
    year_of_study = SelectField('Year of Study', 
        choices=[
            ('', 'Select Year'),
            (1, 'First Year'),
            (2, 'Second Year'),
            (3, 'Third Year'),
            (4, 'Fourth Year'),
            (5, 'Fifth Year'),
            (0, 'Other/Graduate')
        ],
        coerce=lambda x: int(x) if x else None,
        validators=[Optional()]
    )
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """User login form."""
    
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    
    submit = SubmitField('Login')

class ProfileUpdateForm(FlaskForm):
    """User profile update form."""
    
    first_name = StringField('First Name', validators=[
        DataRequired(message="First name is required"),
        Length(min=2, max=50, message="First name must be between 2 and 50 characters")
    ])
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message="Last name is required"),
        Length(min=2, max=50, message="Last name must be between 2 and 50 characters")
    ])
    
    student_id = StringField('Student ID', validators=[
        Optional(),
        Length(max=50, message="Student ID must be less than 50 characters")
    ])
    
    college = StringField('College/University', validators=[
        Optional(),
        Length(max=200, message="College name must be less than 200 characters")
    ])
    
    year_of_study = SelectField('Year of Study', 
        choices=[
            ('', 'Select Year'),
            (1, 'First Year'),
            (2, 'Second Year'),
            (3, 'Third Year'),
            (4, 'Fourth Year'),
            (5, 'Fifth Year'),
            (0, 'Other/Graduate')
        ],
        coerce=lambda x: int(x) if x else None,
        validators=[Optional()]
    )
    
    submit = SubmitField('Update Profile')

class PasswordChangeForm(FlaskForm):
    """Password change form."""
    
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message="Current password is required")
    ])
    
    new_password = PasswordField('New Password', validators=[
        DataRequired(message="New password is required"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message="Please confirm your new password"),
        EqualTo('new_password', message="Passwords must match")
    ])
    
    submit = SubmitField('Change Password')

class TestFeedbackForm(FlaskForm):
    """Form for collecting test feedback."""
    
    rating = SelectField('How would you rate this test?',
        choices=[
            ('', 'Select Rating'),
            (5, '5 - Excellent'),
            (4, '4 - Good'),
            (3, '3 - Average'),
            (2, '2 - Poor'),
            (1, '1 - Very Poor')
        ],
        coerce=lambda x: int(x) if x else None,
        validators=[DataRequired(message="Please provide a rating")]
    )
    
    feedback = TextAreaField('Additional Comments', 
        validators=[
            Optional(),
            Length(max=1000, message="Feedback must be less than 1000 characters")
        ],
        widget=TextArea(),
        render_kw={"rows": 4, "placeholder": "Share your thoughts about the test..."}
    )
    
    submit = SubmitField('Submit Feedback')

class ContactForm(FlaskForm):
    """Contact/Support form."""
    
    subject = SelectField('Subject',
        choices=[
            ('', 'Select Subject'),
            ('technical', 'Technical Issue'),
            ('feedback', 'General Feedback'),
            ('suggestion', 'Suggestion'),
            ('other', 'Other')
        ],
        validators=[DataRequired(message="Please select a subject")]
    )
    
    message = TextAreaField('Message', 
        validators=[
            DataRequired(message="Message is required"),
            Length(min=10, max=2000, message="Message must be between 10 and 2000 characters")
        ],
        widget=TextArea(),
        render_kw={"rows": 6, "placeholder": "Describe your issue or feedback..."}
    )
    
    submit = SubmitField('Send Message')