from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.http import JsonResponse
import datetime
from django.template.loader import render_to_string
from django.http import HttpResponse


from .models import UserProfile,MaidAssign
from .forms import SignupForm, SigninForm, MaidWorkDetailForm, ForgotPassword, SearchBar,UpdateProfile


# View For Index 
def index(request):
	all_maids = UserProfile.objects.filter(user_role='maid')
	search_term = request.GET.get('search')
	apply_sorting_term = request.GET.get('select_sorting')
	if search_term:
		all_maids = all_maids.filter(Q(user__username__startswith = search_term)| Q(user__first_name__startswith = search_term))
	if apply_sorting_term:
		if apply_sorting_term == 'work_type':
			all_maids = all_maids.order_by('work_type')
		elif apply_sorting_term == 'address':
			all_maids = all_maids.order_by('address')

	form = SearchBar(request.GET)

	paginator = Paginator(all_maids, 7)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request,"maid/index.html",{'page_obj': page_obj,'form':form})







# View for Sign UP using Django Form 
def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data

			username = clean_data['username']
			first_name = clean_data['first_name'].lower()
			last_name = clean_data['last_name'].lower()
			email = clean_data['email']
			password = clean_data['password']
			mobile = clean_data['mobile']

			address = clean_data['address'].lower()
			user_type = clean_data['user_type'].lower()
			addhar = clean_data['addhar']
			work_type = clean_data['work_type'].lower()

			user = User.objects.create_user(username,email,password,first_name=first_name,last_name=last_name)
			userprofile = UserProfile.objects.create(user=user,mobile_number = mobile,address = address,user_role = user_type,addhar=addhar,work_type=work_type)

			return redirect('/maid/login/')
	else:
		form = SignupForm()
	return render(request,'maid/signup.html',{'form' : form })



# View for Login / Sign in using Django Form 
def logged_in(request):
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data
			username = clean_data['username']
			password = clean_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('/maid/')
	else:
		form = SigninForm()
	return render(request,'maid/login.html',{'form' : form })


def logout_view(request):
	logout(request)
	return render(request,'maid/logout_message.html')




# View definaion for showing all maids which are available for work or whih are not added to work , and a button Add-to-Work 
def maid_work_detail(request):
	if request.method == 'POST':
		form = MaidWorkDetailForm(request.POST, request=request)
		if form.is_valid():
			clean_data = form.cleaned_data
			# print(clean_data)
			start_date = clean_data['start_date']
			end_date =  clean_data['end_date']
			add_maid_to_work = clean_data['add_maid_to_work']
			user_maid = User.objects.get(id = add_maid_to_work)			
			assigned_maid = MaidAssign.objects.create(user_customer = request.user, maid_user = user_maid, start_date = start_date, end_date= end_date)
			return HttpResponseRedirect(reverse('maid:working'))
	else:
		form = MaidWorkDetailForm(request=request)
	return render(request,'maid/maid_work_detail.html',{'form': form})



# This is view defination for showing all maids which are working at username
def working_maid_at_user(request):
	worked_maid = MaidAssign.objects.filter(user_customer = request.user).order_by('-is_working')
	return render(request, 'maid/working_maid_at_user.html', {'worked_maid': worked_maid } )

# This is view defination for showing all maids History with their customer
def work_history_of_maid(request):
	maids = UserProfile.objects.filter(user_role = 'maid')
	list_of_maid_with_customer = []
	for maid in maids:
		list_of_maid_with_customer.append({maid:maid.user.maidassign_set.all()})
	return render(request,'maid/maid_work_history.html',{'list_of_maid_with_customer':list_of_maid_with_customer})


# This is view defination for remove maid button
def remove_maid(request, maid_id):
	MaidAssign.objects.filter(user_customer = request.user, maid_user__id = maid_id).update(updated_date = datetime.date.today(),is_working = False)
	return HttpResponseRedirect(reverse('maid:working'))

# This is view defination for resetting password 
def forgot_password(request):
	if request.method == 'POST':
		form = ForgotPassword(request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data
			username = clean_data['enter_username']
			password = clean_data['enter_new_password']
			user = User.objects.get(username = username)
			user.set_password(password)
			user.save()
			return redirect('/maid/login/')
	else:
		form = ForgotPassword()
	return render(request,'maid/forgot_password.html',{'form':form })



# This view defination for Deleting maids

def delete_maid(request, maid_id):
	User.objects.get(id=maid_id).delete()
	return HttpResponseRedirect(reverse('maid:index'))


def update_maid_profile(request, maid_id):
	# maid_id = request.GET['maid_id']
	update_maid = User.objects.get(id=maid_id)
	print(update_maid)
	# import pdb;pdb.set_trace();
	if request.method == 'POST':
		form = UpdateProfile(request.POST, id = maid_id)
		if form.is_valid():
			clean_data = form.cleaned_data
			first_name = clean_data['first_name'].lower()
			last_name = clean_data['last_name'].lower()
			email = clean_data['email']
			addhar = clean_data['addhar']
			mobile = clean_data['mobile']
			address = clean_data['address'].lower()
			work_type = clean_data['work_type'].lower()
			updated_maid = User.objects.filter(id=maid_id).update(first_name = first_name, last_name = last_name, email=email,)
			updated_maid = UserProfile.objects.filter(user = update_maid).update(addhar = addhar,  mobile_number = mobile, work_type = work_type)
			return HttpResponseRedirect(reverse('maid:index'))
	else:
		
		initial_dict = {
		# "username" : update_maid.username ,
		"first_name" : update_maid.first_name ,
		"last_name": update_maid.last_name ,
		"email": update_maid.email ,
		"addhar": update_maid.userprofile.addhar,
		"mobile": update_maid.userprofile.mobile_number,
		"address":update_maid.userprofile.address,
		"work_type": update_maid.userprofile.work_type
		}

		# form = UpdateProfile(request.POST or None,initial = initial_dict)
		form = UpdateProfile(initial = initial_dict,id = maid_id)
		rendered = render_to_string('maid/update_profile.html', {'form':form,"maid_id":maid_id},request=request)
		return HttpResponse(rendered)
