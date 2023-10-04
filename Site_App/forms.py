from django import forms
from .models import  MessageToAdmin
class MessageForm(forms.ModelForm):
    class Meta:
        model=MessageToAdmin
        fields=['title','name','message']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'title':forms.TextInput(attrs={'class':'form-control'}),
        }

