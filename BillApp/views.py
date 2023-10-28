from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.


def login(request):
    return render(request, "login.html")


@login_required(login_url="login")
def goDashboard(request):
    return render(request, "dashboard.html")


def registerUser(request):
    try:
        if request.method == "POST":
            usrnm = request.POST["username"]
            eml = request.POST["email"]
            phn = request.POST["phone"]
            adrs = request.POST["address"]
            gstn = request.POST["gstnum"]
            cmpny = request.POST["company"]
            pswrd = request.POST["password"]
            cpswrd = request.POST["confirmPassword"]

            if User.objects.filter(username=usrnm).exists():
                messages.info(
                    request, f"`{usrnm}` already exists!! Please Login or try another.."
                )
                return redirect(login)
            elif User.objects.filter(email=eml).exists():
                messages.info(request, f"`{eml}` already exists!! Please try another..")
                return redirect(login)
            else:
                if pswrd == cpswrd:
                    userInfo = User.objects.create_user(
                        username=usrnm,
                        email=eml,
                        password=pswrd,
                    )
                    userInfo.save()
                    print("auth user saved...")
                    cData = User.objects.get(id=userInfo.id)
                    cmpnyData = Company(
                        user=cData,
                        company_name=cmpny,
                        phone_number=phn,
                        address=adrs,
                        gst_number=gstn,
                    )
                    cmpnyData.save()
                    # messages.info(request, 'Registration Successful..')
                    return redirect(login)
                else:
                    # messages.warning(request, "Passwords doesn't match..Please try again.")
                    # return HttpResponse('please! verify your passwords')
                    return redirect(login)
        else:
            return redirect(login)
    except Exception as e:
        print(e)
        return redirect(login)


def userLogin(request):
    if request.method == "POST":
        uName = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=uName, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(goDashboard)
        else:
            messages.info(request, "Incorrect Username or Password..Please try again")
            return redirect(login)
    else:
        return redirect(login)


@login_required(login_url="login")
def userLogout(request):
    request.session["uid"] = ""
    auth.logout(request)
    return redirect("/")


def validateEmail(request):
    email = request.GET['email']

    if User.objects.filter(email = email).exists():
        return JsonResponse({'is_taken':True})
    JsonResponse({'is_taken':False})


def validateUsername(request):
    uName = request.GET['username']

    if User.objects.filter(username = uName).exists():
        return JsonResponse({'is_taken':True})
    JsonResponse({'is_taken':False})