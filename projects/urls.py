from django.urls import path
from .views import projects,project,create_project,Updateproject,DeleteProject
urlpatterns = [
    path('',projects, name='projects'),
    path('project/<str:pk>/', project, name='project'),

    path('create-project/',create_project,name='create-project'),

    path('update-project/<str:pk>/',Updateproject,name='update-project'),

    path('delete-project/<str:pk>/',DeleteProject,name='delete-project'),

]