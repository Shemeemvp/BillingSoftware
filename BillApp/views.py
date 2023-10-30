from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
# import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.


def login(request):
    return render(request, "login.html")


@login_required(login_url="login")
def goDashboard(request):
    cmp = Company.objects.get(user = request.user.id)
    context = {
        'cmp':cmp,
    }
    return render(request, "dashboard.html",context)


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


@login_required(login_url='login')
def goItems(request):
    cmp = Company.objects.get(user = request.user.id)
    iData = Items.objects.filter(cid = cmp).first()
    context = {
        'cmp':cmp,
        'items':Items.objects.filter(cid = cmp),
        'item_data':iData,
        'item_transaction': Item_transactions.objects.filter(cid = cmp, item = iData)
    }
    return render(request, 'items.html',context)


@login_required(login_url='login')
def showItemData(request,id):
    cmp = Company.objects.get(user = request.user.id)
    iData = Items.objects.get(cid = cmp, id = id)
    context = {
        'cmp':cmp,
        'items':Items.objects.filter(cid = cmp),
        'item_data':iData,
        'item_transaction': Item_transactions.objects.filter(cid = cmp, item = iData)
    }
    return render(request, 'items.html',context)


@login_required(login_url='login')
def addNewItem(request):
    context = {
        'cmp':Company.objects.get(user = request.user.id),
        'itemunit':Item_units.objects.filter(cid = Company.objects.get(user = request.user.id))
    }
    return render(request, 'additem.html',context)

@login_required(login_url='login')
def createNewItem(request):
    if request.user:
        cmp = Company.objects.get(user = request.user.id)
        try:
            if request.method =='POST':
                item = Items(
                    cid = cmp,
                    name = request.POST['name'],
                    hsn = request.POST['hsn'],
                    unit = request.POST['item_unit'],
                    tax = request.POST['tax'],
                    sale_price = request.POST['sale_price'],
                    purchase_price = request.POST['purchase_price'],
                    stock = request.POST['stock']
                )
                item.save()
                
                #Opening stock transaction
                transaction = Item_transactions(cid = cmp, item = item, type = 'Opening Stock', quantity = item.stock)
                transaction.save()

                if 'next_item' in request.POST:
                    return redirect(addNewItem)
                else:
                    return redirect(goItems)
            else:
                messages.error(request, 'Something went wrong, Please try again..!')
                return redirect(addNewItem)
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong, Please try again..!')
            return redirect(addNewItem)
    else:
        messages.error(request, 'Something went wrong, Please try again..!')
        return redirect(addNewItem)



def createitemunit(request):
    if request.user:
        cmp = Company.objects.get(user = request.user.id)
        try:
            if request.method == 'POST':
                unit = Item_units(cid = cmp, symbol = request.POST['usymbol'], name = request.POST['uname'])
                unit.save()
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'message':'failed'})
        except Exception as e:
            print(e)
            return JsonResponse({'message':'failed'})
    return JsonResponse({'message':'failed'})


def getItemUnits(request):
        if request.user:
            try:
                cmp= Company.objects.get(user = request.user.id)
                options = {}
                list= []
                option_objects = Item_units.objects.filter(cid = cmp)

                for item in option_objects:
                    itemUnitDict = {
                    'symbol': item.symbol,
                    'name': item.name,
                    }
                    list.append(itemUnitDict)
                
                print(list)
                return JsonResponse({'units':list},safe=False)
            except Exception as e:
                print(e)
                return JsonResponse({'message':'failed'})
        else:
            return JsonResponse({'message':'failed'})