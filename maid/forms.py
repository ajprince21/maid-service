import re
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import UserProfile, MaidAssign
from django.forms.widgets import NumberInput
import datetime



class SignupForm(forms.Form):
	role = [
		('customer','Customer'),
		('maid','Maid'),
	]


	username = forms.CharField(max_length=50)
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	email = forms.EmailField(max_length=50)

	# More Details of User
	addhar = forms.IntegerField(required=False)
	mobile = forms.IntegerField()
	address = forms.CharField(max_length=100)

	# user_type = forms.IntegerField(widget=forms.Select(choices=role))
	user_type = forms.ChoiceField(required=True,widget=forms.RadioSelect, choices=role)
	work_type = forms.CharField(max_length=50, required=False)

	password = forms.CharField(max_length=20,widget=forms.PasswordInput())
	confirm_password = forms.CharField(max_length=20,widget=forms.PasswordInput())
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('Username is already in use.')
		if not re.findall("^(?=[a-zA-Z0-9._]{4,20}$)(?!.*[_.]{2})[^_.].*[^_.]$",username):
			raise forms.ValidationError('Username can Contain only alphanumeric characters')
		return username

	def clean_password(self):
		password = self.cleaned_data['password']
		if not re.findall("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{5,}$", password):
			raise forms.ValidationError('You have entered an invalid password pattern your pattern should contain min 5 character and At least one (uppercase, lowercase, digit, & special character) ')
		return password
	
	def clean_first_name(self):
		first_name = self.cleaned_data['first_name']
		if not re.findall("^[A-Za-z][-a-zA-Z]+$",first_name):
			raise forms.ValidationError('You have entered an invalid First name , First name can Contain only alphabates and First letter must be in uppercase')
		return first_name

	def clean_last_name(self):
		last_name = self.cleaned_data['last_name']
		if not re.findall("^[A-Za-z][-a-zA-Z]+$",last_name):
			raise forms.ValidationError('You have entered an invalid Last name , Last Name contains only alphabates and First letter must be in uppercase ')
		return last_name

	'''
	def clean_addhar(self):
		addhar = self.cleaned_data['addhar']
		if not re.findall("^[2-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}$",str(addhar)):
			raise forms.ValidationError('Please enter a valid Adhar Card Number')
		return addhar
	'''

	
	def clean_mobile(self):
		mobile = self.cleaned_data['mobile']
		if not re.findall("^[0-9]{10}$",str(mobile)):
			raise forms.ValidationError('Please enter a valid Mobile Number')
		return mobile




	# Validation for Password and Confirm Password input
	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		if password != confirm_password:
			raise forms.ValidationError("password and confirm_password does not match")




class SigninForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50,widget=forms.PasswordInput())
	
	def clean(self):
		cleaned_data = super().clean()
		username = cleaned_data.get('username')
		password = cleaned_data.get('password')
		# user = User.objects.filter(username=username)
		try:
			user = User.objects.get(username = username)
		except:
			raise forms.ValidationError('Username does not exist !! .')
		if not check_password(password, user.password):
			raise forms.ValidationError('You have entered wrong password')



# This is form for showing maid and for adding to work by selecting maid , start_date, end_date

class MaidWorkDetailForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request")
		super(MaidWorkDetailForm, self).__init__(*args, **kwargs)
		current_user = self.request.user
		worked_maid = MaidAssign.objects.filter(user_customer = current_user).values_list('maid_user',flat=True)
		available_maid_list = UserProfile.objects.filter(user_role = 'maid').exclude(user_id__in = worked_maid).values_list('user_id','user__username')
		self.fields['add_maid_to_work'] = forms.ChoiceField(widget=forms.RadioSelect,choices = list(available_maid_list))
	start_date = forms.DateField(initial=datetime.date.today)
	end_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
	


class ForgotPassword(forms.Form):
	enter_username = forms.CharField(max_length=50)
	enter_new_password = forms.CharField(max_length=20,widget=forms.PasswordInput())
	re_enter_new_password = forms.CharField(max_length=20,widget=forms.PasswordInput())

	def clean_enter_username(self):
		enter_username = self.cleaned_data['enter_username']
		try:
			user = User.objects.get(username = enter_username)
		except:
			raise forms.ValidationError('Username does not exist !! .')
		return enter_username


	def clean(self):
		cleaned_data = super().clean()
		enter_new_password = cleaned_data.get('enter_new_password')
		re_enter_new_password = cleaned_data.get('re_enter_new_password')
		if enter_new_password != re_enter_new_password:
			raise forms.ValidationError("Password not did't, Please re-enter")


class SearchBar(forms.Form):
	sort_choice= [

	('', 'Select for sorting'),
	('address', 'Sort by Address'),
	('work_type', 'Sort by Work Type'),

	]

	select_sorting = forms.CharField(widget=forms.Select(choices=sort_choice),required=False)
	search = forms.CharField(max_length=100, required=False)


class UpdateProfile(forms.Form):
	def __init__(self, *args, **kwargs):
		self.id = kwargs.pop("id")
		super(UpdateProfile, self).__init__(*args, **kwargs)
		username = User.objects.get(id=self.id).username
		self.fields['username'].initial = username


	username = forms.CharField(max_length=50,disabled = True)
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	email = forms.EmailField(max_length=50)
	addhar = forms.IntegerField(required=False)
	mobile = forms.IntegerField()
	address = forms.CharField(max_length=100)
	work_type = forms.CharField(max_length=50)

	def clean(self):
		cleaned_data = super().clean()
		username = cleaned_data.get('username')
		email = cleaned_data.get('email')
		maid_by_email = User.objects.filter(email = email)
		if maid_by_email.exists():
			if maid_by_email[0].username == username:
				pass
			else:
				raise forms.ValidationError("Email already in exists")

		





