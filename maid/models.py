from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class UserProfile(models.Model):

	role = [
		('customer','customer'),
		('maid','maid'),
	]

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_role = models.CharField(max_length=30,choices = role,default='customer')	
	addhar = models.IntegerField(null = True,blank = True)
	mobile_number = models.IntegerField()
	address = models.CharField(max_length=200)	
	work_type  = models.CharField(max_length=30,null=True,blank = True)

	def __str__(self):
		return self.user.username


class MaidAssign(models.Model):
	user_customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'customer_user')
	maid_user = models.ForeignKey(User,on_delete=models.CASCADE)
	start_date = models.DateField()
	end_date = models.DateField()
	updated_date = models.DateField(null = True)
	is_working = models.BooleanField(default=False,null = True,blank = True)
	def __str__(self):
		return self.maid_user.username
		




