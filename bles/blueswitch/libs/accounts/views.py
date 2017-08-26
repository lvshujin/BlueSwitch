from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_admin and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, "accounts/login.html", {'error': 'Incorrect email or password'})
        else:
            return render(request, "accounts/login.html", {'error': 'Incorrect email or password.'})

    return render(request, "accounts/login.html")



def logout_view(request):
    '''
    '''
    logout(request)

    return HttpResponseRedirect('/accounts/login/')
