from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from .models import  Discussion
from .models import Answer
from .models import Category
from user_feeds.models import Post
from .forms import DiscussionForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    # DetailView,
    CreateView,
    UpdateView,
    DeleteView
# #      ListView,

)

@login_required(login_url ='/profiles/login/')
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
    blog_latest= Post.objects.order_by('-post_date')[:5]
   
    Discussion_form = DiscussionForm()  

    if request.method == 'POST': 
        Discussion_form = DiscussionForm(request.POST ) 
        if Discussion_form.is_valid(): 
            Discussion_form.instance.created_by= request.user.profile
            comment = Discussion_form.save(commit=False)
            comment.post = details
            Discussion_form.save() 
            return redirect("Forum:articale-detail", id=post.id )  
        else: 
            Discussion_form = DiscussionForm() 

    discussion=Answer.objects.filter(post=post)
    return render(request,'Forum/discuss_detail.html',{'details':details,
    'discussion':discussion,'latest':latest,'blog_latest':blog_latest})



#post Create page view
@method_decorator(login_required, name='dispatch')
class DiscussCreateView(CreateView):
    model= Discussion
    fields= ['title','qustion','image']
    template_name='Forum/discuss_create_form.html'
    success_url = reverse_lazy("Forum:forum_homepage")  

    def form_valid(self,form):
        form.instance.creator =self.request.user.profile
        return super().form_valid(form)


#post Update page view
@method_decorator(login_required, name='dispatch')
class DiscussUpdateView(UpdateView):
    model= Discussion
    fields =['title','qustion','image','category']
    # fields = ['title','image','details']
    template_name='Forum/discuss_update_form.html'
    success_url = reverse_lazy("Forum:profile-page")

    def form_valid(self,form):
        form.instance.creator =self.request.user.profile
        return super().form_valid(form)


#post Delete page view
@method_decorator(login_required, name='dispatch')
class DiscussDeleteView(DeleteView):
    model= Discussion
    template_name='Forum/discuss_delete_form.html'
    success_url = reverse_lazy("Forum:profile-page")



