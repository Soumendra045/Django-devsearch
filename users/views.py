from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request,'users/profiles.html',context)

def userProfile(req,pk):
    profile = Profile.objects.get(id = pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile':profile,'topSkills':topSkills,'otherSkills':otherSkills}
    return render(req,'users/user-profile.html',context)


# Login page view
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Username doesnot exits')
        
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('profiles')
        else:
            messages.error(request,'Username or Password is incorrect')

    return render(request,'users/login_register.html')
def logoutUser(request):
    logout(request)
    messages.info(request,'User was logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,'User account was created')

            login(request,user)
            return redirect('profiles')
        
        else:
            messages.error(request,'An error has occured during registrations')

    context = {'page':page,'form':form}
    return render(request,'users/login_register.html',context)

@login_required(login_url='login')
def userAccount(requset):
    profile = requset.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context={'profile':profile,'skills':skills,'projects':projects}
    return render(requset,'users/account.html',context)