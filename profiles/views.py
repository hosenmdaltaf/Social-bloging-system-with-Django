from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm     #UserCreationForm,
from django.contrib.auth import login,logout
from django.contrib import messages
from .forms import UserRegisterForm
from profiles.models import Profile
from django.contrib.auth.models import User
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import (
      DetailView,
      CreateView,
      UpdateView,
      ListView,
      DeleteView
)

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def follow_and_unfolow(request):
    if request.method =='POST':
        my_profile = Profile.objects.get(user=request.user)
        pk= request.POST.get('profile_pk')
        obj= Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all_profile')
    


class Profile_list_View(ListView):
    model = Profile
    # paginate_by = 3
    context_object_name = 'profiles_list'
    template_name='profiles/profile_list.html'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)

    

#post Create page view
class ProfileCreateView(CreateView):
    model=Profile
    fields=['profile_picture','bio','full_name','work','loaction','educations']
    template_name='profiles/profile_create_form.html'
    success_url = reverse_lazy("profiles:profile_create")

    def form_valid(self,form):
        form.instance.author =self.request.user
        return super().form_valid(form)


class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'profiles/user_profile_page.html' 

    def get_object(self,**kwargs):
        pk= self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.following.all():
            follow=True
        else:
            follow= False
        context['follow'] = follow 
        return context

#post Update page view
class ProfileUpdateView(UpdateView):
    model = Profile
    # context_object_name = 'profiles'
    fields=['profile_picture','bio','full_name','work','loaction','educations','email']
    template_name='profiles/profile_update_form.html'
    success_url = reverse_lazy("user_feeds:profile-page")

    # def form_valid(self,form):
    #     form.instance.author =self.request.user
    #     return super().form_valid(form)


#post Delete page view
class ProfileDeleteView(DeleteView):
    model=Profile
    # context_object_name = 'profile_delete'
    template_name='profiles/profile_delete_form.html'
    success_url = reverse_lazy("homepage:article-list")



# def profiles_detail(request,id): 
    
#     profiles=Profile.objects.get(id=id)
#     # profiles = get_object_or_404(Profile, id=id)
#     # profiles= Profile.objects.get(user=request.user)
#     return render(request,'profiles/user_profile_page.html',{'profiles':profiles})




def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request,f'Your account has created ! You are now able to log in')
            return redirect ('profiles:login')
    else:
        form =UserRegisterForm()
    return render (request,'profiles/signup.html',{'form':form})

# def signup(request):
#     #user register form
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#            user = form.save()
#             #log in user
#            login(request,user)
#            return redirect('accounts:login')
#     else:
#         form=UserCreationForm()

#     return render(request,'accounts/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            #login the user
            user=form.get_user()
            login(request,user)
            return redirect('user_feeds:profile-page')
    else:
        form=AuthenticationForm()
    return render(request,'profiles/login.html',{'form':form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('profiles:logout')
    return render(request,'profiles/logout.html')




