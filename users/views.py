from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm, UserUpdate,ProfileUpdate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.views.generic import View
from .models import Profile

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'congratulations {username}. your account has been created!you are now able to login')
            return redirect('login')
    else:

        form = RegistrationForm()

    return render(request,'register.html',{'form':form})

@login_required
def profile(request):

    return render(request,'new_profile.html')


def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdate(request.POST,instance=request.user)
        p_form = ProfileUpdate(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'your account has been updated successfully!')
            return redirect('profile')

    else:
        u_form = UserUpdate(instance=request.user)
        p_form = ProfileUpdate(instance=request.user.profile)
    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request,'profile_update.html',context)



class UserFollowView(View):

    def get(self,request,username,*args,**kwargs):

        toggle_user = get_object_or_404(User,username__iexact=username)
        if request.user.is_authenticated:
            user_profile,created = Profile.objects.get_or_create(user=request.user)
            if toggle_user in user_profile.following.all():
                user_profile.following.remove(toggle_user)
            else:
                user_profile.following.add(toggle_user)

        return redirect('user-detail',username=username)




# @login_required
# def user_list(request):
#
#     users = User.objects.filter(is_active=True)
#     return render(request,'list.html',{'section':'people','users':users})
#
# @login_required
# def user_detail(request):
#
#     user = get_object_or_404(User,username=username,is_active=True)
#
#     return render(request,'detail.html',{'section':'people','user':user})
