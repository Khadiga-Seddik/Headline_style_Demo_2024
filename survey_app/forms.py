from django import forms
from survey_app.models import Personal_info
from .choices import *


class Personal_infoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(Personal_infoForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Personal_info
        # fields = ['name', 'preferred_headline', 'preferred_headline2', 'preferred_headline3']
        exclude = ('id', 'created', 'selected_articles_list', 'manipulated_headlines', 'headline_style', 'session_id', 'score')
        widgets = {
            'name':  forms.TextInput(attrs={'class': 'textinput_mturk','required': True}),
            'preferred_headline': forms.RadioSelect(attrs={'class': 'radio-inline', 'required': True}),
            'preferred_headline2': forms.RadioSelect(attrs={'class': 'radio-inline', 'required': True}),
            'preferred_headline3': forms.RadioSelect(attrs={'class': 'radio-inline', 'required': True}),
        }

        labels = {
            'name': 'Name',
            'preferred_headline': 'https://images.dngroup.com/image/eyJ3Ijo5ODAsImsiOiJiMDZmN2JkZGU2ODllODkwOTFkOWM1NzdiMTRkNjNmZSIsImYiOiJ3ZWJwIiwiY3JvcCI6WzIsMCwxNTk5LDEwNjZdLCJyIjoxLjUsIm8iOiJkbiJ9',
            'preferred_headline2': 'https://gfx.nrk.no/z5-hkABJ0CV7xmly4GLfEQEeBDKoIrKMzJJdGoa-ChIA.jpg',
            'preferred_headline3': 'https://www.cdn.tv2.no/images/16965093.webp?imageId=16965093&width=1956&height=1102&compression=92&format=webp',
        
        }

   


