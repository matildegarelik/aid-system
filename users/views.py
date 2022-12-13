from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse, request
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .forms import CreateUserForm

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

#Decorators
from .decorators import *
from django.contrib.auth.decorators import login_required

#Importar Grupos para delimitar vistas
from django.contrib.auth.models import Group

# Modelos
from .models import Counter


# Create your views here.

#Pagina de Registro
#@allowed_users(allowed_roles=[''])
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm() 
        if request.method == 'POST':
            form= CreateUserForm(request.POST)
            if form.is_valid():
                user= form.save()
                try:
                    group= Group.objects.get(name=request.POST['group'])
                except ObjectDoesNotExist:
                    group = Group(name=request.POST['group'])
                    group.save()
                user.groups.add(group)
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '+username)
                return redirect('login/')
        context={'form':form}
        return render(request, 'register.html', context)

#LOGIN
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method =='POST' and request.POST.get('submit')=='Login B':
            username= request.POST.get('username')
            password= request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request,'Username or password is incorrect')
        elif request.method =='POST' and request.POST.get('submit')=='Login A':
            username= request.POST.get('username')
            user = User.objects.get(username=username)
            #manually set the backend attribute
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request,'Username or password is incorrect')
        context={'users':User.objects.filter(groups__name="groupA")}
        return render (request, 'login.html', context)

#LOGOUT
def logoutUser(request):
    logout(request)
    messages.info(request,'Logged out successfully!')
    return redirect ('login')


# Pagina de Usuario
@login_required(login_url='login')
def home(request):
    if(Group.objects.get(name='groupA') in request.user.groups.all()):
        try:
            counter = Counter.objects.get(user=request.user)
        except ObjectDoesNotExist:
            counter = Counter(user=request.user)
            counter.save()
        return render(request, 'homeA.html',{'counter':counter})
    else:

        return render(request, 'homeB.html',{'counters':Counter.objects.all()})

def count(request):
    pk = request.GET.get('id')
    if(pk):
        counter = Counter.objects.get(id=pk)
        new_count = counter.count+1
        counter.count=new_count
        counter.save()
        return HttpResponse('success')
    return HttpResponse('error')
def toggleBreak(request):
    pk = request.GET.get('id')
    if(pk):
        counter = Counter.objects.get(id=pk)
        counter.onBreak=not counter.onBreak
        counter.save()
        if(counter.onBreak):
            messages.info(request, 'Break set sucessfully')
        else:
            messages.info(request,'Break stopped')
    return redirect('home')

@allowed_users(allowed_roles=['groupB'])
def resetCounters(request):
    Counter.objects.all().update(count=0)
    messages.info(request,'Counter units reset successful')
    return redirect('home')
