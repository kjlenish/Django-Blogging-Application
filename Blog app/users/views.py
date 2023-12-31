from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from . forms import UserSignUpForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!!   Log in...")
            return redirect('signin')
        else:
            messages.warning(request, "Failed to create account !!!")
    else:
        form = UserSignUpForm()
    
    context = {'form':form}
    return render(request, 'users\signup.html', context)

def terms(request):
    return render(request, 'users/terms.html')

def profile(request, username):

    obj_user = User.objects.get(username=username)
    obj_profile = obj_user.profile
    context = {
        'obj_user' : obj_user,
        'obj_profile' : obj_profile
    }
    return render(request, 'users\profile.html', context)


def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/update.html', context)