from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from .models import  Discussion
from .models import Answer
from .models import Category
from .forms import DiscussionForm
from django.views.generic import (
    # DetailView,
    CreateView,
    UpdateView,
    DeleteView
# #      ListView,

)

def discuss_seaction_home(request):
   
    category = request.GET.get('category')
    if category == None:
        allquestions = Discussion.objects.all()
    else:
        allquestions = Discussion.objects.filter(category__name=category)
    categories = Category.objects.all()

    search_input = request.GET.get('search-area') or ''
    allquestions = Discussion.objects.all()
    if search_input:
        allquestions = allquestions.filter(title__startswith=search_input)

    search_input = search_input

    return render(request,'Forum/discuss.html',{'allquestions':allquestions,'categories':categories,
    'search_input':search_input})


def discuss_seaction_details(request,id):
    details=Discussion.objects.get(id=id)
    post = get_object_or_404(Discussion, id=id)
    latest= Discussion.objects.order_by('-qustion_date')[:5]
   
    Discussion_form = DiscussionForm()  

    if request.method == 'POST': 
        Discussion_form = DiscussionForm(request.POST ) 
        if Discussion_form.is_valid(): 
            # Discussion_form.instance.created_by = profile.request.user
            comment = Discussion_form.save(commit=False)
            comment.post = details
            Discussion_form.save() 
            return redirect("Forum:articale-detail", id=post.id )  
        else: 
            Discussion_form = DiscussionForm() 

    discussion=Answer.objects.filter(post=post)
    return render(request,'Forum/discuss_detail.html',{'details':details,'discussion':discussion,'latest':latest})



#post Create page view
class DiscussCreateView(CreateView):
    model= Discussion
    fields= ['title','qustion','image','category']
    template_name='Forum/discuss_create_form.html'
    success_url = reverse_lazy("Forum:home")  

    def form_valid(self,form):
        form.instance.creator =self.request.user
        return super().form_valid(form)



#post Update page view
class DiscussUpdateView(UpdateView):
    model= Discussion
    fields ='__all__'
    # fields = ['title','image','details']
    template_name='Forum/discuss_update_form.html'
    success_url = reverse_lazy("Forum:profile-page")

    # def form_valid(self,form):
    #     form.instance.author =self.request.user
    #     return super().form_valid(form)


#post Delete page view
class DiscussDeleteView(DeleteView):
    model= Discussion
    template_name='Forum/discuss_delete_form.html'
    success_url = reverse_lazy("Forum:profile-page")



