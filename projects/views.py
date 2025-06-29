from django.shortcuts import render
from django.shortcuts import redirect
from .models import Project,Tag
from .forms import ProjectForm ,ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchProjects , paginationProject
from django.contrib import messages
# Create your views here.
def projects(request):
    projects ,search_query = searchProjects(request)
    custom_range,projects = paginationProject(request,projects,6)

    context = {'projects':projects,'search_query':search_query,'custom_range':custom_range}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projectObj = Project.objects.get(pk=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted.')
        return redirect('project',pk=projectObj.id)


    tags = projectObj.tag.all()
    return render(request,'projects/single-project.html',{'projectObj':projectObj,'tags':tags,'form':form})

@login_required(login_url='login')
def create_project(req):
    profile = req.user.profile
    form=ProjectForm()

    if req.method=="POST":
        newtags = req.POST.get('newtags').replace(','," ").split()
        form = ProjectForm(req.POST,req.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name=tag)
                project.tag.add(tag)            
            return redirect('account')
    context={'form':form}
    return render(req,'projects/project_form.html',context)

@login_required(login_url='login')
def Updateproject(req,pk):
    profile = req.user.profile
    project = profile.project_set.get(pk=pk)
    form=ProjectForm(instance=project)

    if req.method=="POST":
        newtags = req.POST.get('newtags').replace(','," ").split()

        form = ProjectForm(req.POST,req.FILES,instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name=tag)
                project.tag.add(tag)

            return redirect('account')
    context={'form':form,'project':project}
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