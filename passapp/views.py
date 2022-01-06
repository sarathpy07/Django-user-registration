from django.shortcuts import render
from passapp.forms import Userform, Userprofileinfoform
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'html/index.html')

@login_required
def special(request):
    return HttpResponse("You are loggrd IN Welome..")

@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = Userform(data=request.POST)
        profile_form = Userprofileinfoform(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = Userform()
        profile_form = Userprofileinfoform()
    return render(request, 'html/registration.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered ': registered})

def userlogin(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT is Not Active")
        else:
            print("someone tried  to Login and Failed")
            print("Username:{} and Password {}".format(username,password))
            return HttpResponse("INvalid login details applied")
    else:
        return render(request,'html/login.html',{})