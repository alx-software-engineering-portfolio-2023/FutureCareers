from __init__ import create_app, scheduler
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import base64
import os

from __init__ import create_app
from flask import render_template

app = create_app()

@scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
def SendMail():
    print("working")

def send_email_using_sendgrid():
    os.getenv("SENDGRID_API_KEY")
    message = Mail(
    from_email='futurecareersalx@gmail.com',
    to_emails='futurecareersalx@gmail.com',
    subject='Your Jobs list',
    html_content='')
    # with open('results.csv', 'rb') as file:
    #     data = file.read()
    #     file.close()
    # encoded_file = base64.b64encode(data).decode()

    # attachedFile = Attachment(
    #     FileContent(encoded_file),
    #     FileName('results.csv'),
    #     FileType('text/csv'),
    #     Disposition('attachment')
    # )
    # message.attachment = attachedFile
    try:
        #sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

if __name__ == "__main__":
    app.run(debug=True)
    