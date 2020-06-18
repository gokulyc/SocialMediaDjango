from django import forms
from .models import *

class AddUser_Form(forms.ModelForm):
    class Meta:
        model = UserDataBase
        exclude = ("usr","dob","location","degree","website","experience","company","profile_title","facebook_url" ,"twitter_url","google_url","linkdin_url")
        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control", }),
            "email":forms.EmailInput(attrs={"class":"form-control", }),
            "number":forms.NumberInput(attrs={"class":"form-control", }),
            "image":forms.FileInput(attrs={"class":"form-control","onchange":"loadFile(event)" }),
            "about":forms.Textarea(attrs={"class":"form-control", "rows":"5"}),

        }

class Edit_User_Form(forms.ModelForm):
    class Meta:
        model = UserDataBase
        exclude = ("usr","image" ,"facebook_url" ,"twitter_url","google_url","linkdin_url")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", }),
            "email": forms.EmailInput(attrs={"class": "form-control", }),
            "number": forms.NumberInput(attrs={"class": "form-control", }),
            "about": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            "location": forms.TextInput(attrs={"class": "form-control", }),
            "degree": forms.TextInput(attrs={"class": "form-control", }),
            "website": forms.TextInput(attrs={"class": "form-control", }),
            "experiance": forms.TextInput(attrs={"class": "form-control", }),
            "company": forms.TextInput(attrs={"class": "form-control", }),
            "dob":forms.DateInput(attrs={"class": "form-control",'type': 'date' }),
            "profile_title":forms.TextInput(attrs={"class": "form-control", }),

        }

class Register_Company_Form(forms.ModelForm):
    class Meta:
        model = Company_Model
        exclude = ("usr",)
        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control", }),
            "email":forms.EmailInput(attrs={"class":"form-control", }),
            "number":forms.NumberInput(attrs={"class":"form-control", }),
            "logo":forms.FileInput(attrs={"class":"form-control","onchange":"loadFile(event)" }),
            "website": forms.TextInput(attrs={"class": "form-control", }),
            "title": forms.TextInput(attrs={"class": "form-control", }),
            "address": forms.TextInput(attrs={"class": "form-control", }),
            "map_embed": forms.Textarea(attrs={"class": "form-control", }),

        }

class UserBlog_Form(forms.ModelForm):
    class Meta:
        model = Blog_Model
        exclude = ("usr",)
        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control", }),
            "blog":forms.Textarea(attrs={"class":"form-control", "placeholder":"Share your thoughts...!"}),
            "ytd_video":forms.Textarea(attrs={"class":"form-control","onchange":"loadFile(event)" }),

        }