from django.contrib import admin


from .models import UserProfile,MaidAssign
from .models import User


	

admin.site.register(UserProfile)
admin.site.register(MaidAssign)

