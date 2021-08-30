from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .form import UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def loginView(request):
    if request.method == 'POST':
        form  = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, 
            username = form.cleaned_data['username'], 
            password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                if hasattr(user, 'company'):
                    return HttpResponseRedirect('/company/')
                elif hasattr(user, 'dealer'):
                    return HttpResponseRedirect('/dealer/')
                elif hasattr(user, 'siteer'):
                    return HttpResponseRedirect('/siteEr/')
                else:
                    return HttpResponseRedirect('/success/')
                
            else:
                messages.warning(request, 'Enter a valid username and password')
        else:
            #form non_field_error
            pass
    else:
        form = UserLoginForm()
    return render(request, 'home/login.html', { 'form' : form })

def logoutView(request):
    logout(request)
    return render(request, 'home/logout.html')
            
