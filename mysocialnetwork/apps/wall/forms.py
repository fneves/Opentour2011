from django import forms
 
from wall.models import Post
 
class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        
        
    class Meta:
        model = Post
        fields = ('text',)
 
    