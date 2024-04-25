from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User  
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth.password_validation import password_validators_help_text_html
from .models import *

class CustomerRegistrationForm(UserCreationForm):  
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))  
    password2 = forms.CharField(label='Confirm password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))  
    
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels={'email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username= UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))        
    password= forms.CharField(label=_('Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))  

class MyPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label=_('Old password'),strip=False,
                                 widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'})) 
    new_password1=forms.CharField(label=_('New password'),strip=False,
                                 widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),
                                 help_text=password_validators_help_text_html())   
    new_password2=forms.CharField(label=_('Confirm New password'),strip=False,
                                 widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
 email =forms.EmailField(label=_('Email'),max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))       
 
class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label=_('New password'),strip=False,
                                 widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),
                                 help_text=password_validators_help_text_html())   
    new_password2=forms.CharField(label=_('Confirm New password'),strip=False,
                                 widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
    
    # Moddel Form
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','locality','city','state','zipcode']
        widgets={"name":forms.TextInput(attrs={'class':'form-control'}),
                 'locality':forms.TextInput(attrs={'class':'form-control'}),
                 'city':forms.TextInput(attrs={'class':'form-control'}),
                 'state':forms.Select(attrs={'class':'form-control'}),
                 'zipcode':forms.NumberInput(attrs={'class':'form-control'})}
        
                                   