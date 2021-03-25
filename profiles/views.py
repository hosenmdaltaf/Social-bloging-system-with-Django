from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm     #UserCreationForm,
from django.contrib.auth import login,logout
from django.contrib import messages
from .forms import UserRegisterForm
from profiles.models import Profile
from django.contrib.auth.models import User
# from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.views.generic import (
#     #  DetailView,
      CreateView,
      UpdateView,
#      ListView,
     DeleteView
)

# class My_profileView(ListView):
#     model = Profile
#     # paginate_by = 10
#     context_object_name = 'profiles'
#     template_name='profiles/user_profile_page.html'

#     # def get_context_data(self,*args,**kwargs):
#     #     context = super().get_context_data(*args,**kwargs)
#     #     context['latest']= Post.objects.order_by('-post_date')[:5]
#     #     return context

#post Create page view
class ProfileCreateView(CreateView):
    model=Profile
    fields=['profile_picture','bio','full_name','work','loaction','educations']
    template_name='profiles/profile_create_form.html'
    success_url = reverse_lazy("profiles:profile_create")

    def form_valid(self,form):
        form.instance.author =self.request.user
        return super().form_valid(form)

 

 

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



def my_profile(request):
    # profiles =Profile.objects.all()
    profiles= Profile.objects.get(user=request.user)
    return render(request,'profiles/user_profile_page.html',{'profiles':profiles})



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




