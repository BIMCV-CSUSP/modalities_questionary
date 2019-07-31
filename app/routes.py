from app import app, db
from app.models import User, NiftyImage, Tagged

import random
import csv

from flask import render_template, Response, redirect, url_for
from flask_login import login_required

from flask_login import current_user

from app.questForm import QuestionaryForm

import nibabel
import numpy
import io
import os
import json

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
@login_required
def index():
    form = QuestionaryForm()

    if form.validate_on_submit():
        if current_user.last_image_id is not None:
            dict = form.to_dict()
            headers = QuestionaryForm.get_header()
            nii_image = NiftyImage.query.get(current_user.last_image_id)
            dict["image_path"] = nii_image.path
            dict["image_section"] = current_user.image_section
            headers.insert(0,"image_path")
            headers.insert(1,"image_section")

            results_dir = app.config['RESULTS_FOLDER']
            results_file = os.path.join(results_dir,"{}.csv".format(current_user.username))
            write_headers = False
            if not os.path.isfile(results_file):
                write_headers = True

            tagged = Tagged(id_user=current_user.id, id_image=current_user.last_image_id, id_frame=current_user.image_section)
            db.session.add(tagged)
            with open(results_file, 'a') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                if write_headers: writer.writeheader()
                writer.writerow(dict)

        max_image = NiftyImage.query.order_by(-NiftyImage.id).first()
        if max_image is not None:
            rand_id = random.randint(1,max_image.id)
            img = NiftyImage.query.get(rand_id)

            path = img.path
            max_slices = 0
            for r, d, f in os.walk(path):
                for file in f:
                    if '.nii.gz' in file:
                        slices = (nibabel.load(os.path.join(r,file))
                                                     .get_fdata()
                                                     .shape[2])
                        if slices > max_slices:
                            max_slices = slices
                            nib_img = nibabel.load(os.path.join(r,file))

            nib_img_data = nib_img.get_fdata()
            nib_shape = nib_img_data.shape
            rand_slice = random.randint(nib_shape[2]//2-nib_shape[2]//4,nib_shape[2]//2+nib_shape[2]//4)
            user = User.query.get(current_user.id)
            user.last_image_id = img.id
            user.image_section = rand_slice

        db.session.commit()
        return redirect(url_for('index'))
    files = []
    tags = []
    if current_user.last_image_id is not None :
        path = NiftyImage.query.get(current_user.last_image_id).path

        with open(os.path.join(path,"dicom.json"), "r") as read_file:
            data = json.load(read_file)

        tags = [{"name":d["desc"],"value":d["value"]} for d in data
                                                 if d["tag1"] in ["(0018,0020)",
                                                                  "(0018,0080)",
                                                                  "(0018,0081)",
                                                                  "(0018,0082)",
                                                                  "(0018,1314)",
                                                                  "(0018,0091)",
                                                                  "(0018,0083)",
                                                                  "(0018,0095)",
                                                                  "(0018,0050)",
                                                                  "(0018,0088)",
                                                                  "(0008,0070)"]]


        for t in tags:
            try:
                val = "{:.2f}".format(float(t["value"]))
                t["value"] = val
            except ValueError:
                pass

        for r, d, f in os.walk(path):
            for file in f:
                files.append({"name":file,"slices":""})
                if '.nii.gz' in file:
                    files[-1]["slices"]=str(nibabel.load(os.path.join(r,files[-1]["name"]))
                                                 .get_fdata()
                                                 .shape[2])
    return render_template("index.html", quest_form=form, files=files, tags=tags)

@app.route("/img/img.png")
@login_required
def img():

    img = ""
    max_slices=0
    if current_user.last_image_id is not None :
        path = NiftyImage.query.get(current_user.last_image_id).path
        for r, d, f in os.walk(path):
            for file in f:
                if '.nii.gz' in file:
                    slices = (nibabel.load(os.path.join(r,file))
                                                 .get_fdata()
                                                 .shape[2])
                    if slices > max_slices:
                        max_slices = slices
                        img = os.path.join(r,file)

    if img != "":
        nib_img = nibabel.load(img)

        nib_img_data = nib_img.get_fdata()
        nib_shape = nib_img_data.shape
        slice_count = current_user.image_section
        #slice=(nib_img_data[slice_count, : , :] if axe==0
        #        else (nib_img_data[:, slice_count , :] if axe==1
        #            else nib_img_data[:, :, slice_count]))
        slice=nib_img_data[: , : ,slice_count]

        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.axis("off")
        axis.imshow(slice.T, cmap="gray", origin="lower")


        output = io.BytesIO()
        #image_obj = Image.fromarray(slice.T.astype('uint8'),'L')
        #image_obj = image_obj.transpose(Image.FLIP_TOP_BOTTOM)
        #image_obj.save(output,"png")


        fig.tight_layout()
        fig.subplots_adjust(bottom = 0)
        fig.subplots_adjust(top = 1)
        fig.subplots_adjust(right = 1)
        fig.subplots_adjust(left = 0)
        fig.savefig(output,format="png",bbox_inches="tight",transparent=True,pad_inches=0)
        #FigureCanvas(fig).print_png(output)

        return Response(output.getvalue(), mimetype='image/png')

    output = io.BytesIO()
    fig = Figure()
    arr=([[0 for _ in range(25)] for _ in range(5)]
      + [[0 for _ in range(5)]+[255 for _ in range(4)]+[0 for _ in range(7)]+[255 for _ in range(4)]+[0 for _ in range(5)] for _ in range(4)]
      + [[0 for _ in range(25)] for _ in range(5)]
      + [[0 for _ in range(9)]+[255 for _ in range(7)]+[0 for _ in range(9)]]
      + [[0 for _ in range(8)]+[255 for _ in range(9)]+[0 for _ in range(8)]]
      + [[0 for _ in range(7)]+[255 for _ in range(5)]+[0 for _ in range(1)]+[255 for _ in range(5)]+[0 for _ in range(7)]]
      + [[0 for _ in range(6)]+[255 for _ in range(4)]+[0 for _ in range(5)]+[255 for _ in range(4)]+[0 for _ in range(6)]]
      + [[0 for _ in range(5)]+[255 for _ in range(4)]+[0 for _ in range(7)]+[255 for _ in range(4)]+[0 for _ in range(5)]]
      + [[0 for _ in range(5)]+[255 for _ in range(3)]+[0 for _ in range(9)]+[255 for _ in range(3)]+[0 for _ in range(5)]]
      + [[0 for _ in range(25)] for _ in range(5)])
    arr=numpy.array(arr)

    image_obj = Image.fromarray(arr.astype('uint8'),'L')
    image_obj.save(output,"png")

    return Response(output.getvalue(), mimetype='image/png')
    #response=make_response(png_output.getvalue())
    #response.headers['Content-Type'] = 'image/png'
