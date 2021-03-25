from django import forms 
from .models import Answer
  
class DiscussionForm(forms.ModelForm): 
    class Meta: 
        model = Answer
        fields =['text']
