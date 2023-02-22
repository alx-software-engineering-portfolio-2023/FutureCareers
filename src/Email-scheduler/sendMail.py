from __init__ import scheduler



@scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
def SendMail():
    print("working")