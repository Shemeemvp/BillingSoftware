from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from random import randint
from django.core.mail import send_mail
from django.conf import settings
# import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.


def login(request):
    return render(request, "login.html")


@login_required(login_url="login")
def goDashboard(request):
    cmp = Company.objects.get(user=request.user.id)
    context = {
        "cmp": cmp,
    }
    return render(request, "dashboard.html", context)


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
    email = request.GET["email"]

    if User.objects.filter(email=email).exists():
        return JsonResponse({"is_taken": True})
    JsonResponse({"is_taken": False})


def validateUsername(request):
    uName = request.GET["username"]

    if User.objects.filter(username=uName).exists():
        return JsonResponse({"is_taken": True})
    JsonResponse({"is_taken": False})


@login_required(login_url="login")
def goItems(request):
    cmp = Company.objects.get(user=request.user.id)
    iData = Items.objects.filter(cid=cmp).first()
    context = {
        "cmp": cmp,
        "items": Items.objects.filter(cid=cmp),
        "item_data": iData,
        "item_transaction": Item_transactions.objects.filter(
            cid=cmp, item=iData
        ).order_by("-id"),
    }
    return render(request, "items.html", context)


@login_required(login_url="login")
def showItemData(request, id):
    cmp = Company.objects.get(user=request.user.id)
    iData = Items.objects.get(cid=cmp, id=id)
    context = {
        "cmp": cmp,
        "items": Items.objects.filter(cid=cmp),
        "item_data": iData,
        "item_transaction": Item_transactions.objects.filter(
            cid=cmp, item=iData
        ).order_by("-id"),
    }
    return render(request, "items.html", context)


@login_required(login_url="login")
def addNewItem(request):
    context = {
        "cmp": Company.objects.get(user=request.user.id),
        "itemunit": Item_units.objects.filter(
            cid=Company.objects.get(user=request.user.id)
        ),
    }
    return render(request, "additem.html", context)


@login_required(login_url="login")
def createNewItem(request):
    if request.user:
        cmp = Company.objects.get(user=request.user.id)
        try:
            if request.method == "POST":
                item = Items(
                    cid=cmp,
                    name=request.POST["name"],
                    hsn=request.POST["hsn"],
                    unit=request.POST["item_unit"],
                    tax=request.POST["tax"],
                    sale_price=request.POST["sale_price"],
                    purchase_price=request.POST["purchase_price"],
                    stock=request.POST["stock"],
                )
                item.save()

                # Opening stock transaction
                transaction = Item_transactions(
                    cid=cmp, item=item, type="Opening Stock", quantity=item.stock
                )
                transaction.save()

                if "next_item" in request.POST:
                    return redirect(addNewItem)
                else:
                    return redirect(goItems)
            else:
                messages.error(request, "Something went wrong, Please try again..!")
                return redirect(addNewItem)
        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong, Please try again..!")
            return redirect(addNewItem)
    else:
        messages.error(request, "Something went wrong, Please try again..!")
        return redirect(addNewItem)

@login_required(login_url="login")
def deleteItem(request, id):
    if request.user:
        cmp = Company.objects.get(user=request.user.id)
        try:
            item = Items.objects.get(cid=cmp, id=id)
            item.delete()
            return redirect(goItems)
        except Exception as e:
            print(e)
            return redirect(showItemData, id)



@login_required(login_url="login")
def editItem(request,id):
        if request.user:
            cmp = Company.objects.get(user=request.user.id)
            try:
                context = {
                    'cmp':cmp,
                    'item':Items.objects.get(cid = cmp, id = id),
                    "itemunit": Item_units.objects.filter(cid=Company.objects.get(user=request.user.id)),
                }
                return render(request,'edititem.html',context)
            except Exception as e:
                print(e)
                return redirect(showItemData, id)



@login_required(login_url="login")
def editItemData(request,id):
    if request.user:
        cmp = Company.objects.get(user=request.user.id)
        item = Items.objects.get(cid = cmp, id = id)
        try:
            if request.method == 'POST':
                item.name = request.POST['name']
                item.hsn = request.POST['hsn']
                item.unit = request.POST['item_unit']
                item.tax = request.POST['tax']
                item.sale_price = request.POST['sale_price']
                item.stock = request.POST['stock']
                item.purchase_price = request.POST['purchase_price']

                item.save()
                return redirect(showItemData,id)
        except Exception as e:
            print(e)
            return redirect(editItem,id)
    return redirect('/')


@login_required(login_url="login")
def createitemunit(request):
    if request.user:
        cmp = Company.objects.get(user=request.user.id)
        try:
            if request.method == "POST":
                unit = Item_units(
                    cid=cmp, symbol=request.POST["usymbol"], name=request.POST["uname"]
                )
                unit.save()
                return JsonResponse({"message": "success"})
            else:
                return JsonResponse({"message": "failed"})
        except Exception as e:
            print(e)
            return JsonResponse({"message": "failed"})
    return JsonResponse({"message": "failed"})


def getItemUnits(request):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            options = {}
            list = []
            option_objects = Item_units.objects.filter(cid=cmp)

            for item in option_objects:
                itemUnitDict = {
                    "symbol": item.symbol,
                    "name": item.name,
                }
                list.append(itemUnitDict)

            print(list)
            return JsonResponse({"units": list}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "failed"})
    else:
        return JsonResponse({"message": "failed"})


@login_required(login_url="login")
def updateStock(request, id):
    if request.user:
        cmp = Company.objects.get(user=request.user.id)
        try:
            if request.method == "POST":
                item = Items.objects.get(cid=cmp, id=id)
                print("data---", request.POST)
                if not "update_qty" in request.POST:
                    print("num===", int(request.POST["qty_update"]))
                    item.stock += int(request.POST["qty_update"])
                    item.save()

                    trns = Item_transactions(
                        cid=cmp,
                        item=item,
                        type="Add Stock",
                        date=request.POST["update_date"],
                        quantity=request.POST["qty_update"],
                    )
                    trns.save()
                    return redirect(showItemData, id)
                else:
                    print("num===", int(request.POST["qty_update"]))
                    item.stock -= int(request.POST["qty_update"])
                    item.save()

                    trns = Item_transactions(
                        cid=cmp,
                        item=item,
                        type="Reduce Stock",
                        date=request.POST["update_date"],
                        quantity=request.POST["qty_update"],
                    )
                    trns.save()
                    return redirect(showItemData, id)
        except Exception as e:
            print(e)
            return redirect(showItemData, id)


@login_required(login_url="login")
def deleteTransaction(request, id):
    if request.user:
        cmp = Company.objects.get(user=request.user.id)
        try:
            trns = Item_transactions.objects.get(cid=cmp, id=id)
            trns.delete()
            return redirect(showItemData, trns.item.id)
        except Exception as e:
            print(e)
            return redirect(showItemData, trns.item.id)
    return redirect(showItemData, trns.item.id)


def forgotPassword(request):
    try:
        email = request.POST['email']
        user = User.objects.filter(email = email).first()
        if User.objects.filter(email = email).exists():
            password = str(randint(100000, 999999))
            # print(password)
            user.set_password(password)
            user.save()

            # SEND MAIL CODE
            # subject = "Forgot Password"
            # message = f"Dear user,\nYour Password has been reset as you requested. You can login with the password given below\n\nPassword:{password}"
            # recipient = user.email
            # send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])


            return JsonResponse({'message':'success'})
        else:
            return JsonResponse({'message':'not_found'})
    except Exception as e:
        print(e)
        return redirect(login)