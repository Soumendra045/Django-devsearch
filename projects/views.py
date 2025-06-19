from django.shortcuts import render
from django.shortcuts import redirect
from .models import Project,Tag
from .forms import ProjectForm
# Create your views here.
def projects(request):
    project = Project.objects.all()
    return render(request,'projects/projects.html',{'projects':project})

def project(request,pk):
    projectObj = Project.objects.get(pk=pk)
    tags = projectObj.tag.all()
    return render(request,'projects/single-project.html',{'projectObj':projectObj,'tags':tags})

def create_project(req):
    form=ProjectForm()

    if req.method=="POST":
        form = ProjectForm(req.POST,req.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context={'form':form}
    return render(req,'projects/project_form.html',context)

def Updateproject(req,pk):
    project = Project.objects.get(pk=pk)
    form=ProjectForm(instance=project)

    if req.method=="POST":
        form = ProjectForm(req.POST,req.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context={'form':form}
    return render(req,'projects/project_form.html',context)

def DeleteProject(req,pk):
    project = Project.objects.get(pk=pk)
    if req.method=="POST":
        project.delete()
        return redirect('/')
    context={'object':project}
    return render(req,'projects/delete_template.html',context)