from flask import Flask, render_template, request, url_for
from config import jim, username, code
from string import Template
from pathlib import Path

from email.message import EmailMessage
import smtplib

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/projects')
def projects():
    return render_template('projects.html')

@application.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        user_email = request.form.get("email")
        message = request.form.get("message")

        html = Template(Path('templates/email.html').read_text())

        email = EmailMessage()
        email['from'] = name
        email['to'] = jim
        email['subject'] = name
        email.set_content(html.substitute({'name': name, 'email': user_email, 'message': message}), 'html')

        try:
            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(username, code)
                smtp.send_message(email)
        
            return render_template('success.html', name=name)
        except IndexError:
            return render_template('failure.html')

    return render_template('contact.html')



if (__name__)==('__main__'):
    application.run()