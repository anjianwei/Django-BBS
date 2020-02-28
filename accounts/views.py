# Create your views here.

from django.contrib.auth import login as auth_login
# from django.contrib.auth.forms import UserCreationForm # 内置注册表单
from .forms import SignUpForm
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import UpdateView

from accounts.models import UserProfile
import os


def upload(request):
    if request.method == 'POST':
        # 如果有头像，先删除照片再删除数据库
        if not UserProfile.objects.filter(username=request.user, avatar=''):
            project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            media_path = os.path.join(project_path, 'media')
            print(media_path)
            try:
                avatar_name = request.user.User_Profiles.first().avatar.name
                avatar_path = os.path.join(media_path, avatar_name)
                os.remove(avatar_path)
            except Exception as e:
                print(e)
            UserProfile.objects.filter(username=request.user).delete()

        new_img = UserProfile(username=request.user, avatar=request.FILES.get('img'))
        new_img.save()
        return redirect('my_account')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
