from django import forms

from .models import Post

from django.core.validators import MinValueValidator
TYPES = (  
    ('1','mp3'),
    ('2','mp4'),
    ('3','mkv'),

)

class PostForm(forms.ModelForm):
    format = forms.ChoiceField(choices=TYPES, required=True )
    class Meta:
        model = Post
        fields = ( 'text','format') 
        labels = { "text": "Youtube link",
                  "format":"Format"}        



class GenerateRandomUserForm(forms.Form):
    total_user = forms.IntegerField(
        #label='Number of users',
        required=False,
        validators=[
            MinValueValidator(10)
        ]
    ) 
