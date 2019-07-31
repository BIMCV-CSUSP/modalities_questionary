from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, StringField, RadioField, TextField
from wtforms.validators import DataRequired

class QuestionaryForm(FlaskForm):
    questionMD = "Which sequences do you see in the image?"
    question_mod = RadioField('', choices=[('T1w','T1 weighted'),
                                                ('T2w','T2 weighted'),
                                                ('acq-gre_T2w','Gradient echo T2 weighted '),
                                                ('T1rho','T1 Rho map'),
                                                ('T1map','T1 map'),
                                                ('T2map','T2 map'),
                                                ('T2star','T2*'),
                                                ('FLAIR','FLAIR'),
                                                ('FLASH','FLASH'),
                                                ('PD','Proton density'),
                                                ('PDmap','Proton density map'),
                                                ('PDT2','Combined PD/T2'),
                                                ('inplaneT1','Inplane T1'),
                                                ('inplaneT2','Inplane T2'),
                                                ('angio','Angiography'),
                                                ('dwi','dwi'),
                                                ('pwi','pwi'),
                                                ('swi','swi'),
                                                ('minIP','minIP'),
                                                ('fieldmap','Fieldmap'),
                                                ('asl','asl'),
                                                ('unknown', 'Unknown'),
                                                ('other','Other')])
    other = TextField('Name:')

    observation_text = "Other observations"
    contrast = BooleanField("With contrast")

    noise_text = "Noise type if apreciable"
    coverage = BooleanField("A) Coverage Artifact")
    ringing = BooleanField("B) Ringing/Blurring")
    ghosting = BooleanField("C) Ghosting")
    radio = BooleanField("D) Radio Frequency Noise")




    submit = SubmitField('Send')

    def to_dict(self):
        dict={}
        dict["modality"]=self.question_mod.data
        dict["other_modality"]=self.other.data
        dict["contrast"]=self.contrast.data
        dict["coverage"]=self.coverage.data
        dict["ringing/blurring"]=self.ringing.data
        dict["ghosting"]=self.ghosting.data
        dict["radio"]=self.radio.data


        return dict

    def get_header():
        return ["modality",
          "other_modality",
          "contrast",
          "coverage",
          "ringing/blurring",
          "ghosting",
          "radio"]
