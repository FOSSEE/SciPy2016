from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm
from website.models import Proposal
from django.core.validators import MinLengthValidator, MinValueValidator, \
RegexValidator, URLValidator


class CommentForm(forms.Form):
    pass

class ProposalForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    # content_link = forms.CharField(required=False, help_text='Link to the content of your Talk')
    # speaker_link = forms.CharField(required=False, help_text='Link to information about the Speaker')
    about_me = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About Me'}),
                        required = True,
                        error_messages = {'required':'Title field required.'},  
                        label = '')
    attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))   
    phone = forms.CharField(max_length = 12, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),required=False, label = '', validators = [RegexValidator(regex = '^[0-9-_+.]*$')])
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                        required = True,
                        error_messages = {'required':'Title field required.'},  
                        label = ''
                        )
    abstract = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Abstract'}),
                        required = True,
                        error_messages = {'required':'Title field required.'},  
                        label = ''
                        )
    class Meta:
        model = Proposal
        exclude = ('user', 'email','prerequisite','status')

    def clean_title(self):
        title = self.cleaned_data['title']
        if Proposal.objects.filter(title=title).exists():
            raise forms.ValidationError("This title already exist.")
        return title

    def clean_attachment(self):
        import os
        cleaned_data = self.cleaned_data
        attachment = cleaned_data.get('attachment', None)
        if attachment:
            ext = os.path.splitext(attachment.name)[1]
            valid_extensions = ['.pdf','.zip','.rar']
            if not ext in valid_extensions:
                raise forms.ValidationError(u'File not supported!')
            if attachment.size > (5*1024*1024):
                raise forms.ValidationError('File size exceeds 5MB')
        return attachment


class WorkshopForm(forms.ModelForm):
    # content_link = forms.CharField(required=False, help_text='Link to the content of your Talk')
    # speaker_link = forms.CharField(required=False, help_text='Link to information about the Speaker')
    about_me = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About Me'}),
                        required = True,
                        error_messages = {'required':'Title field required.'},  
                        label = '')
    attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))   
    phone = forms.CharField(max_length = 12, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),required=False, label = '', validators = [RegexValidator(regex = '^[0-9-_+.]*$')])
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                        required = True,
                        error_messages = {'required':'Title field required.'},  
                        label = ''
                        )
    abstract = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Abstract'}),
                        required = True,
                        error_messages = {'required':'Title field required.'},  
                        label = ''
                        )
    prerequisite = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prerequisite'}),
                        required = True,
                        error_messages = {'required':'Title field required.'},  
                        label = ''
                        )
    class Meta:
        model = Proposal
        exclude = ('user', 'email','status')

    def clean_title(self):
        title = self.cleaned_data['title']
        if Proposal.objects.filter(title=title).exists():
            raise forms.ValidationError("This title already exist.")
        return title


class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password1',
		          'password2')
        first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
                        label = ''
                        )
        last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
                        label = ''
                        )
        email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}),
                        required = True,
                        error_messages = {'required':'Email field required.'},  
                        label = ''
                        )
        username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                        required = True,
                        error_messages = {'required':'Username field required.'},  
                        label = ''
                        )
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                        required = True,
                        error_messages = {'required':'Password field required.'},  
                        label = ''
                        )
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
                        required = True,
                        error_messages = {'required':'Password Confirm field required.'},  
                        label = ''
                        )


class UserLoginForm(forms.Form):
    username = forms.CharField(
			widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), 
			label=''
		)
    password = forms.CharField(
			widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), 
			label=''
		)
