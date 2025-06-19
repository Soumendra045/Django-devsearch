from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from .models import Profile
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
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user=User.objects.get(username=username)
        except:
            print('Username doesnot exits')
        
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('profiles')
        else:
            print('Username or Password is incorrect')

    return render(request,'users/login_register.html')
def logoutUser(request):
    logout(request)
    return redirect('login')