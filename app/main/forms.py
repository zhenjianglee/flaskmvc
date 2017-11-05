from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,BooleanField,SelectField,SubmitField,FieldList,HiddenField
from wtforms.validators import Required,Length,Regexp
from ..models import Role,User,LG

class LGDetailForm(FlaskForm):
    #how to put a hidden fi


    lg_no = StringField('保函编号', label='保函编号')

    lg_companyname=StringField('公司名称')
    lg_custom_no=StringField('海关编号')
    submit = SubmitField('提交')

    def __init__(self,lg,*args,**kwargs):
        super(LGDetailForm,self).__init__(*args,**kwargs)
        self.lg=lg

class LGEqueryForm(FlaskForm):
    #how to put a hidden fi

    lg_no = StringField('保函编号')



    submit = SubmitField('提交')

    def __init__(self,*args,**kwargs):
        super(LGEqueryForm,self).__init__(*args,**kwargs)



