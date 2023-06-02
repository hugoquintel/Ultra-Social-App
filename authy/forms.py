from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from authy.models import Profile
import re

def ForbiddenUsers(value):
	forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
	if value.lower() in forbidden_users:
		raise ValidationError('Invalid name for user, this is a reserverd word.')

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this email already exists.')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('User with this username already exists.')
	

class SignupForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "input is-medium"}), max_length=30, required=True,)
	email = forms.CharField(widget=forms.EmailInput(attrs={"class": "input is-medium"}), max_length=100, required=True,)
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input is-medium"}))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input is-medium"}), required=True, label="Confirm your password.")

	class Meta:

		model = User
		fields = ('username', 'email', 'password')

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(ForbiddenUsers)
		self.fields['username'].validators.append(InvalidUser)
		self.fields['username'].validators.append(UniqueUser)
		self.fields['email'].validators.append(UniqueEmail)

	def clean(self):
		super(SignupForm, self).clean()
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		pattern = re.compile("^(?=.*[A-Z])(?=.*[!@#$%^&*()\-__+.])(?=.*[0-9]).{8,20}$")

		if bool(pattern.match(password)) == False:
			self._errors['password'] = self.error_class(['Password must be 8-20 characters consisting of numbers, uppercase and lowercase letters and special character. Please try again'])
		if password != confirm_password:
			self._errors['password'] = self.error_class(['Passwords do not match. Please Try again'])
		return self.cleaned_data

class ChangePasswordForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input is-large"}), label="Old password", required=True)
	new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input is-large"}), label="New password", required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input is-large"}), label="Confirm new password", required=True)

	class Meta:
		model = User
		fields = ('id', 'old_password', 'new_password', 'confirm_password')

	def clean(self):
		super(ChangePasswordForm, self).clean()
		id = self.cleaned_data.get('id')
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		user = User.objects.get(pk=id)

		pattern = re.compile("^(?=.*[A-Z])(?=.*[!@#$%^&*()\-__+.])(?=.*[0-9]).{8,20}$")

		if bool(pattern.match(new_password)) == False:
			self._errors['password'] = self.error_class(['Password must be 8-20 characters consisting of numbers, uppercase and lowercase letters and special character. Please try again'])
		if not user.check_password(old_password):
			self._errors['old_password'] =self.error_class(['Old password do not match.'])
		if new_password != confirm_password:
			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
		return self.cleaned_data

class EditProfileForm(forms.ModelForm):
	picture = forms.ImageField(widget = forms.FileInput(attrs={"class": "img-input"}), required=False)
	backgroundimage = forms.ImageField(widget = forms.FileInput(attrs={"class": "img-input"}), required=False)
	first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "input is-medium"}), max_length=50, required=False)
	last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "input is-medium"}), max_length=50, required=False)
	location = forms.CharField(widget=forms.TextInput(attrs={"class": "input is-medium"}), max_length=25, required=False)
	url = forms.URLField(widget=forms.TextInput(attrs={"class": "input is-medium"}), max_length=60, required=False)
	profile_info = forms.CharField(widget=forms.Textarea(attrs={"class": "input is-medium"}), max_length=150, required=False)

	class Meta:
		model = Profile
		fields = ('picture', 'backgroundimage', 'first_name', 'last_name', 'location', 'url', 'profile_info')