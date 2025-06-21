from django.shortcuts import render
from django.shortcuts import redirect
from .models import Project,Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def projects(request):
    project = Project.objects.all()
    return render(request,'projects/projects.html',{'projects':project})

def project(request,pk):
    projectObj = Project.objects.get(pk=pk)
    tags = projectObj.tag.all()
    return render(request,'projects/single-project.html',{'projectObj':projectObj,'tags':tags})

@login_required(login_url='login')
def create_project(req):
    profile = req.user.profile
    form=ProjectForm()

    if req.method=="POST":
        form = ProjectForm(req.POST,req.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context={'form':form}
    return render(req,'projects/project_form.html',context)

@login_required(login_url='login')
def Updateproject(req,pk):
    profile = req.user.profile
    project = profile.project_set.get(pk=pk)
    form=ProjectForm(instance=project)

    if req.method=="POST":
        form = ProjectForm(req.POST,req.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context={'form':form}
    return render(req,'projects/project_form.html',context)

@login_required(login_url='login')
def DeleteProject(req,pk):
    profile = req.user.profile
    project = profile.project_set.get(pk=pk)
    if req.method=="POST":
        project.delete()
        return redirect('/')
    context={'object':project}
    return render(req,'delete_template.html',context)