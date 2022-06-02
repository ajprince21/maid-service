from django.urls import path
from . import views
app_name = 'maid'

urlpatterns = [
	path('',views.index, name = 'index'),    
	path('signup/',views.signup, name = 'signup'),
	path('forgot_password/',views.forgot_password, name = 'forget_password'),
	path('login/',views.logged_in, name = 'login'),
	path('maid_work_detail/',views.maid_work_detail, name = 'maid_work_detail'),
	path('workedmaid/',views.working_maid_at_user, name = 'working'),
	path('logout/',views.logout_view, name = 'logout'),
	path('history/',views.work_history_of_maid, name = 'maid_work_history'),	
	path('<int:maid_id>/remove_maid/',views.remove_maid, name = 'remove_maid'),
	path('<int:maid_id>/delete_maid/',views.delete_maid, name = 'delete_maid'),
	path('update_maid_profile/<int:maid_id>',views.update_maid_profile, name = 'update_maid_profile'),	
]