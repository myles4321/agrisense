from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import InputRequired

class FarmingInfoForm(FlaskForm):
    q1 = SelectField('What is the average temperature range in your area during the growing season?',
                    choices=[
                        ('',''),
                        ('Below 10°C (Cold)', 'Below 10°C (Cold)'),
                        ('10-20°C (Cool)', '10-20°C (Cool)'),
                        ('20-30°C (Moderate)', '20-30°C (Moderate)'),
                        ('30-40°C (Warm)', '30-40°C (Warm)'),
                        ('Above 40°C (Hot)', 'Above 40°C (Hot)')
                    ],
                    validators=[InputRequired()])
    q2 = SelectField('How much rainfall does your region receive annually?',
                    choices=[
                        ('',''),
                        ('Less than 500 mm annually (Arid)', 'Less than 500 mm annually (Arid)'),
                        ('500-1000 mm annually (Semi-arid)', '500-1000 mm annually (Semi-arid)'),
                        ('1000-1500 mm annually (Sub-humid)', '1000-1500 mm annually (Sub-humid)'),
                        ('More than 1500 mm annually (Humid)', 'More than 1500 mm annually (Humid)')
                    ],
                    validators=[InputRequired()])
    q3 = SelectField('What crops were grown on your land in the previous season?',
                    choices=[
                        ('',''),
                        ('Corn (Maize)', 'Corn (Maize)'),
                        ('Rice', 'Rice'),
                        ('Wheat', 'Wheat'),
                        ('Potatoes', 'Potatoes'),
                        ('Tomatoes', 'Tomatoes'),
                        ('Onions', 'Onions'),
                        ('Beans', 'Beans')
                    ],
                    validators=[InputRequired()])
    q4 = SelectField('What crops are currently in high demand in your local market?',
                    choices=[
                        ('',''),
                        ('Corn (Maize)', 'Corn (Maize)'),
                        ('Rice', 'Rice'),
                        ('Wheat', 'Wheat'),
                        ('Potatoes', 'Potatoes'),
                        ('Tomatoes', 'Tomatoes'),
                        ('onions', 'Onions'),
                        ('Beans', 'Beans')
                    ],
                    validators=[InputRequired()])
    q5 = SelectField('Does your soil retain moisture well, or does it tend to dry out quickly?',
                    choices=[
                        ('',''),
                        ('Poor (Dries quickly)', 'Poor (Dries quickly)'),
                        ('Fair', 'Fair'),
                        ('Good (retains moisture well)', 'Good (Retains Moisture Well)')
                    ],
                    validators=[InputRequired()])
    q6 = SelectField('What is the altitude of your farming location?',
                    choices=[
                        ('',''),
                        ('Below 500 meters (Plain)', 'Below 500 meters (Plain)'),
                        ('500-1000 meters (Moderate)', '500-1000 meters (Moderate)'),
                        ('1000-1500 meters (Highland)', '1000-1500 meters (Highland)'),
                        ('1500-2000 meters (Mountainous)', '1500-2000 meters (Mountainous)'),
                        ('Above 2000 meters (High Alpine)', 'Above 2000 meters (High Alpine)')
                    ],
                    validators=[InputRequired()])
