from dataclasses import fields
from pyexpat import model
from re import A
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from todo_list.models import Task

class Register_Form(UserCreationForm):
    '''An extension of the Django's UserCreationForm class used in registering users. It handles password hashes 
    and password confirmation.'''
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs) -> None:
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})

class Edit_Details_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)


class Change_Password_Form(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class Reset_Password_Form(PasswordResetForm):
    class Meta:
        model = User
        fields = '__all__'

class Reset_Password_Confirm_Form(SetPasswordForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs) -> None:
        super(Reset_Password_Confirm_Form, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class':'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class':'form-control'})

class Add_Task_Form(forms.ModelForm):
    class Meta:
        model = Task
        fields = {'description'}
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'})
        }
