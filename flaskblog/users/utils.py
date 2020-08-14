

def save_picture(form_picture):
    # rename picture with random nr
    random_hex = secrets.token_hex(8)
    # make sure u save with same extension as uploaded: grab f_ext,dont need f_name so use _
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)
    # resize image before we save it:
    output_size = (125, 125)   # tuple of size we want
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # form_picture.save(picture_path) - instead of doing this, we do i.save to save thumbnail instead of big picture
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this emailand no changes will be made.
'''
    mail.send(msg)
