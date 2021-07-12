import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)  # random name which we are assigning to ur picture
    # Function below returns filename without extention and the extention itself
    # f_name , f_ext ...... '_' is used to name a variable which we are not going to use
    _, f_ext = os.path.splitext(form_picture.filename) #formpicture is the data from the field user uploaded
    picture_fn = random_hex + f_ext  # final filename of picture with extention
    # current_.root.path is going to give us the path to our package directory(flaskblog)
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125,125) # resizing the uploaded image
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
     
    return picture_fn

def send_reset_email(user):    # to user user an email with reset token
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='thakuranukriti7@gmail.com',recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)