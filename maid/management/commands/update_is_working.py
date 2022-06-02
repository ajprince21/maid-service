from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from maid.models import *
from datetime import date
import datetime

class Command(BaseCommand):
	help = 'update is_working feild status of maid'

	def handle(self,*args,**kwargs):
		customer_users = UserProfile.objects.filter(user_role ='customer')
		for customer_user in customer_users:
			current_date = datetime.date.today()
			worked_maid = MaidAssign.objects.filter(user_customer = customer_user.user)
			for maid in worked_maid:
				user_worked_maid = worked_maid.filter(maid_user = maid.maid_user)
				if maid.updated_date is None:
					if maid.end_date > current_date:
						user_worked_maid.update(is_working = True)
					else:
						user_worked_maid.update(is_working = False)
				else:
					if maid.updated_date > current_date:
						user_worked_maid.update(is_working = True)
					else:
						user_worked_maid.update(is_working = False)			
		self.stdout.write("Maids is working status updated ")
