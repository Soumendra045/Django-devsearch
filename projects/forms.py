from django.forms import ModelForm
from django import forms
from .models import Project,Review,Tag

class ProjectForm(ModelForm):
    class Meta:
        model=Project
        fields=['title','discription','featured_image','demo_link','source_link','tag']
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
        }
    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)

        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Title'}) 
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})  

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']

        lebels = {
            'value':'Place your vote',
            'body':'Add a comment with your vote'
        }
    def __init__(self,*args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)

        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Title'}) 
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})