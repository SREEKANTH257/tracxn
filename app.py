from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import uuid
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = '0a59f84a8b796f260de9ef58d71cf49ac288e7fc5695afd7'  # Change this to a strong secret key
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(36), nullable=False)

# Create the database tables within the application context
with app.app_context():
    db.create_all()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        verification_token = str(uuid.uuid4())

        new_user = User(full_name=full_name, email=email, password=hashed_password, verification_token=verification_token)
        db.session.add(new_user)
        db.session.commit()

        send_verification_email(email, verification_token)

        flash('Signup successful! Please check your email for verification.')
        return redirect(url_for('signup'))

    return render_template('signup.html')
    
    

# AWS Configuration
aws_access_key_id = 'AKIAXTORPF6KCPCBPR6Z'
aws_secret_access_key = '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'
aws_region_name = 'us-east-1'

# Initialize SES client
ses_client = boto3.client(
    'ses',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region_name
)

def send_verification_email(email, token):
    verification_link = f"https://sreekanth257.site/verify?token={token}"

    try:
        response = ses_client.send_email(
            Source='mycloudmail@sreekanth257.site',
            Destination={
                'ToAddresses': [email],
            },
            Message={
                'Subject': {
                    'Data': 'Verify your email',
                },
                'Body': {
                    'Text': {
                        'Data': f'Click on this link to verify your email: {verification_link}',
                    },
                },
            }
        )
        print("Email sent! Message ID:", response['MessageId'])
    except NoCredentialsError:
        print("Credentials not available.")


@app.route('/verify', methods=['GET'])
def verify_email():
    token = request.args.get('token')
    user = User.query.filter_by(verification_token=token).first()
    
    if user:
        user.verified = True
        db.session.commit()
        flash('Email verified successfully! You can now log in.')
    else:
        flash('Invalid verification link.')

    return redirect(url_for('signup'))
    


if __name__ == '__main__':
    app.run(debug=True)
