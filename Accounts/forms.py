from django import forms
from . models import User
from  Order.models import Address
class RecordFormUser(forms.Form):
    username = forms.CharField(max_length=50, label='نام کاربری',
                               widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}), label='نام',
                           required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="ایمیل", required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='رمز',
                               required=True)
    passwordAgain = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    required=True,
                                    label='رمز دوباره')


class LoginFormUser(forms.Form):
    username = forms.CharField(max_length=100, label='نام کاربری',
                               widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               required=True, label='رمز')


class ChangePassForm(forms.Form):
    password = forms.CharField(max_length=100, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='رمز')
    passwordAgain = forms.CharField(max_length=100, required=True,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    label='رمزدوباره')


class FormEmail(forms.Form):
    Email = forms.CharField(max_length=100, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}),
                            label='ایمیل')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'lname', 'job', 'natiional_code']
        widgets = {
            'name': forms.TextInput(attrs={
                 'class': 'form-control'
            }),
            'lname': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'job': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'natiional_code': forms.TextInput(attrs={
                'class': 'form-control'

            })
        }

