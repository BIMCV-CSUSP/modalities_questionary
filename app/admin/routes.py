from app.models import User, NiftyImage
from app import db
from flask import current_app as app


from flask import render_template, flash, redirect, url_for, request, send_file
from flask import Markup, abort
from flask_login import current_user, login_user,login_required
from app.admin import bp

from os import urandom, listdir, path, walk
from binascii import hexlify
from io import BytesIO
import random, nibabel
from threading import Thread

from app.admin.admin_forms import RegenerateImagesForm, DownloadXMLForm, NewUserForm

import zipfile
import smtplib, traceback

def load_new_images(str_file_dir):
    with open(str_file_dir) as f:
        for line in f:
            line = line.strip()
            if db.session.query(NiftyImage.id).filter_by(path=line).scalar() is None:
                i = NiftyImage(path=line)
                db.session.add(i)
        db.session.commit()

@bp.route('/admin',methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        abort(404)

    images_form = RegenerateImagesForm()
    download_data_form = DownloadXMLForm()
    new_user_form = NewUserForm()

    if images_form.submit1.data and images_form.validate_on_submit():
        if not path.exists(images_form.dir.data) and not path.isdir(images_form.dir.data):
            images_form.dir.errors.append("Incorrect path")

        else:
            process = Thread(target=load_new_images, args=[images_form.dir.data])
            process.start()

    if download_data_form.submit2.data and download_data_form.validate_on_submit():
        print(download_data_form.format.data)
        if download_data_form.format.data == "0":
            return redirect(url_for('admin.download_zip'))
        if download_data_form.format.data == "1":
            return redirect(url_for('admin.download_csv'))

    if new_user_form.submit3.data and new_user_form.validate_on_submit():
        if User.query.filter_by(username=new_user_form.username.data).first() is not None:
            flash("User already exists")
        elif User.query.filter_by(email=new_user_form.mail.data).first() is not None:
            flash("Email already in use")
        else:
            u = User(username=new_user_form.username.data, email=new_user_form.mail.data)
            max_image = NiftyImage.query.order_by(-NiftyImage.id).first()
            if max_image is not None:
                rand_id = random.randint(1,max_image.id)
                path_file = NiftyImage.query.get(rand_id).path

                img = ""
                max_slices=0


                for r, d, f in walk(path_file):
                    for file in f:
                        if '.nii.gz' in file:
                            sh = (nibabel.load(path.join(r,file))
                                                         .get_fdata()
                                                         .shape)
                            if sh[2] > max_slices:
                                max_slices = sh[2]
                                img = file
                                nib_shape = sh

                rand_slice = random.randint(nib_shape[2]//2-nib_shape[2]//4,nib_shape[2]//2+nib_shape[2]//4)
                u.last_image_id = rand_id
                u.image_section = rand_slice

            if not new_user_form.password.data:
                token = urandom(16)
                u.token = hexlify(token).decode()
            else:
                u.set_password(new_user_form.password.data)

            mail_body = ['This is an automaticlly generated message, please do not respond back.',
                    ""
                    "Hello"
                    "",
                    "The information to access to the site is stated below, please guard this message for future reference.",
                    ""]


            if not new_user_form.password.data:
                url = "{}?user={}&token={}".format(
                                '/'.join(request.url_root.split('/')[:3])
                                + url_for('auth.login'),u.username,u.token)
                flash(Markup('new user: <a href="{0}">{0}</a>'.format(url)))
                mail_body.append("Use the following url to acces the site: {}".format(url))
                mail_body.append("")
                mail_body.append("You can add it to your bookmarks for faster acces")
            else:
                flash("New user: {}".format(u.username))
                mail_body.append("To log in use the next link: {}".format('/'.join(request.url_root.split('/')[:3]) + url_for('auth.login')))
                mail_body.append("username:{}".format(""))
                mail_body.append("password:{}")

            mail_body += [
                "",
                "You will be able to change the login information in the foreseeable futureself."
                ""
                "Best regards,"
                "the ceib team"

            ]
            error = False
            if new_user_form.send_mail.data:

                gmail_user = app.config["MAIL_DIR"]
                gmail_password = app.config["MAIL_PASS"]
                print(gmail_user, gmail_password)

                sent_from = gmail_user
                to = [new_user_form.mail.data]
                subject = 'New acces to image poll'

                email_text = "\r\n".join([
                      "From: {:s}".format(sent_from),
                      "To: {:s}".format(", ".join(to)),
                      "Subject: {:s}".format(subject),
                      ""
                      ]+mail_body)


                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login(gmail_user, gmail_password)
                    server.sendmail(sent_from, to, email_text)
                    server.close()


                    print ('Email sent!')
                except Exception as e:
                    print ('Something went wrong...')
                    error = True
                    traceback.print_exc()


            if not error:
                db.session.add(u)
                db.session.commit()






    return render_template('admin/admin.html', title='Sign In',
                            images_form=images_form,
                            download_data_form=download_data_form,
                            new_user_form=new_user_form)



@bp.route('/download.zip')
@login_required
def download_zip():
    if not current_user.is_admin:
        abort(404)

    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:

        results_dir = app.config['RESULTS_FOLDER']
        contents = listdir(results_dir)
        for file_name in contents:
            zf.write(path.join(results_dir,file_name),file_name)


    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='data.zip')


@bp.route('/download.csv')
@login_required
def download_csv():
    abort(503)
    if not current_user.is_admin:
        abort(404)
