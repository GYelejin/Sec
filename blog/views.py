from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm

def landing(request):
    profiles = Profile.objects.all()
    context = {'profiles': list(profiles.values())}

    return render(request, 'landing.html', context)


def landingLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 
                'Такого пользователя нет в системе')
        user = authenticate(request, username=username, 
            password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' 
                in request.GET else 'account')
        else:
            messages.error(request, 
                'Неверное имя пользователя или пароль')
    return redirect('landing')

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('landing')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 
                'Такого пользователя нет в системе')

        user = authenticate(request, 
            username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' 
                in request.GET else 'account')

        else:
            messages.error(request, 
                'Неверное имя пользователя или пароль')

    return render(request, 'login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'Вы вышли из учетной записи')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 
                'Аккаунт успешно создан!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(request, 
                'Во время регистрации возникла ошибка')

    context = {'page': page, 'form': form}
    return render(request, 
        'login_register.html', context)



@login_required
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, 
            instance=profile)
        if form.is_valid():
            form.save()

            return redirect('landing')
    context = {'form': form}
 
    return render(request, 
        'profile_form.html', context)
