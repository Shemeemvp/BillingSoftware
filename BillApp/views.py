from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.db import connection
# import requests
from decimal import Decimal
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
            state = request.POST['state']
            cntry = request.POST['country']
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
                        state = state,
                        country = cntry,
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


def showProfile(request):
    if request.user:
        cmp = Company.objects.get(user=request.user.id)
        try:
            context = {
                'cmp':cmp,
            }
            return render(request, 'profile.html',context)
        except Exception as e:
            print(e)
            return redirect("/")
    return redirect("/")


@login_required(login_url="login")
def updateUserProfile(request):
    if request.user:
        user = User.objects.get(id = request.user.id)
        cmp = Company.objects.get(user = user.id)
        try:
            if request.method == 'POST':
                cmp.company_name = request.POST['company_name']
                cmp.gst_number = request.POST['gst_number']
                cmp.phone_number = request.POST['phone_number']
                cmp.address = request.POST['address']
                cmp.state = request.POST['state']
                cmp.country = request.POST['country']
                cmp.save()
            
                if User.objects.filter(username = request.POST['username']).exists():
                    messages.error(request, 'Username already exists, Try another.!')
                    return redirect(showProfile)
                if User.objects.filter(email = request.POST['email']).exists():
                    messages.error(request, 'Email already exists, Try another.!')
                    return redirect(showProfile)
                    
                user.username = request.POST['username']
                user.email = request.POST['email']
                user.save()
                
                messages.success(request, 'Profile updated successfully.!')
                return redirect(showProfile)
        except Exception as e:
            print(e)
            return redirect(showProfile)
    return redirect('/')


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
    

@login_required(login_url="login")
def updateLogo(request,id):
    if request.user:
        cmp = Company.objects.get(user = id)
        try:
            if request.method == 'POST':
                cmp.logo = request.FILES.get('logo')
                cmp.save()
                return redirect(showProfile)
        except Exception as e:
            print(e)
            return redirect(showProfile)
    return redirect('/')


@login_required(login_url="login")
def removeLogo(request):
    if request.user:
        cmp = Company.objects.get(user = request.user.id)
        try:
            cmp.logo = None
            cmp.save()
            return redirect(showProfile)
        except Exception as e:
            print(e)
            return redirect(showProfile)
    return redirect('/')



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
    return redirect("/")


@login_required(login_url="login")
def editItem(request,id):
        if request.user:
            cmp = Company.objects.get(user=request.user.id)
            try:
                itemData = Items.objects.get(cid = cmp, id = id)
                trns = Item_transactions.objects.get(cid = cmp, item = itemData, type = "Opening Stock")
                op_stock = trns.quantity
                context = {
                    'cmp':cmp,
                    'item':itemData,
                    'op_stock': op_stock,
                    "itemunit": Item_units.objects.filter(cid=Company.objects.get(user=request.user.id)),
                }
                return render(request,'edititem.html',context)
            except Exception as e:
                print(e)
                return redirect(showItemData, id)
        return redirect("/")


@login_required(login_url="login")
def editItemData(request,id):
    if request.user:
        cmp = Company.objects.get(user=request.user.id)
        item = Items.objects.get(cid = cmp, id = id)
        trns = Item_transactions.objects.filter(cid = cmp , item = item.id).filter(type = 'Opening Stock').first()
        crQty = trns.quantity
        chQty = int(request.POST['stock'])
        diff = abs(crQty - chQty)
        try:
            if request.method == 'POST':
                item.name = request.POST['name']
                item.hsn = request.POST['hsn']
                item.unit = request.POST['item_unit']
                item.tax = request.POST['tax']
                item.sale_price = request.POST['sale_price']
                if chQty > crQty:
                    item.stock += diff
                elif chQty < crQty:
                    item.stock -= diff
                # item.stock = request.POST['stock']
                item.purchase_price = request.POST['purchase_price']

                item.save()

                trns.quantity = request.POST['stock']
                trns.save()

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
    return redirect("/")


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
    return redirect("/")


@login_required(login_url="login")
def editTransaction(request,id):
    if request.user:
        cmp = Company.objects.get(user=request.user.id)
        try:
            trns = Item_transactions.objects.get(cid=cmp, id=id)
            context = {
                'cmp':cmp,
                'transaction':trns,
            }
            return render(request, 'edit_transaction.html',context)
        except Exception as e:
            print(e)
            return redirect(showItemData, trns.item.id)
    return redirect("/")


@login_required(login_url="login")
def editTransactionData(request, id):
    if request.user:
        cmp = Company.objects.get(user=request.user.id)
        trns = Item_transactions.objects.get(cid=cmp, id=id)
        item = Items.objects.get(cid =cmp, id = trns.item.id)
        crQty = trns.quantity
        chQty = int(request.POST['quantity'])
        diff = abs(crQty - chQty)
        try:
            if request.method == 'POST':
                trns.type = request.POST['type']
                if str(request.POST['type']).lower() == 'reduce stock' and chQty > crQty:
                    item.stock -= diff
                elif str(request.POST['type']).lower() == 'reduce stock' and chQty < crQty:
                    item.stock += diff
                elif str(request.POST['type']).lower() == 'add stock' and chQty > crQty:
                    item.stock += diff
                elif str(request.POST['type']).lower() == 'add stock' and chQty < crQty:
                    item.stock -= diff

                if str(request.POST['type']).lower() == 'opening stock' and  chQty > crQty:
                    item.stock += diff
                elif str(request.POST['type']).lower() == 'opening stock' and chQty < crQty:
                    item.stock -= diff

                trns.quantity = request.POST['quantity']
                trns.date = request.POST['date']
                trns.save()
                item.save()

                return redirect(showItemData, trns.item.id)
        except Exception as e:
            print(e)
            return redirect(editTransaction, id)
    return redirect("/")



# PURCHASES
    
@login_required(login_url="login")
def goPurchases(request):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            context = {
                'cmp': cmp,
                'purchases': Purchases.objects.filter(cid = cmp)
            }
            return render(request, 'purchases.html',context)
        except Exception as e:
            print(e)
            return redirect(goDashboard)
    return redirect('/')


@login_required(login_url="login")
def addNewPurchase(request):
    if request.user:
        try:
            model_meta = Purchases._meta
            pk_name = model_meta.pk.name
            table_name = model_meta.db_table
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_NAME = %s", [table_name])
                next_id = cursor.fetchone()[0]

            cmp = Company.objects.get(user=request.user.id)
            items = Items.objects.filter( cid = cmp)
            context = {
                'cmp': cmp,
                'bill_no':next_id,
                'items': items,

            }
            return render(request, 'add_purchase.html',context)
        except Exception as e:
            print(e)
            return redirect(goDashboard)
    return redirect('/')


def getItemData(request):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            id = request.GET.get('id')

            item = Items.objects.get(name = id, cid=cmp)
            hsn = item.hsn
            pur_rate = item.purchase_price
            sale_rate = item.sale_price
            tax = item.tax
            return JsonResponse({"status":True,'hsn':hsn,'pur_rate':pur_rate,'sale_rate':sale_rate, 'tax':tax})
        except Exception as e:
            print(e)
            return JsonResponse({"status":False})
    return redirect('/')


@login_required(login_url="login")
def createNewPurchase(request):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            if request.method == 'POST':
                purchase = Purchases(
                    cid = cmp,
                    date = request.POST['date'],
                    party_name = request.POST['party_name'],
                    phone_number = request.POST['party_phone'],
                    gstin = request.POST['party_gstin'],
                    subtotal = request.POST['subtotal'],
                    tax = request.POST['tax'],
                    adjustment = request.POST['adjustment'],
                    total_amount = request.POST['grand_total'],
                )
                purchase.save()

                item = request.POST.getlist("item[]")
                hsn  = request.POST.getlist("hsn[]")
                qty = request.POST.getlist("qty[]")
                price = request.POST.getlist("price[]")
                tax = request.POST.getlist("tax[]")
                total = request.POST.getlist("total[]")

                pid = Purchases.objects.get( bill_no = purchase.bill_no)

                if len(item)==len(hsn)==len(qty)==len(price)==len(tax)==len(total) and item and hsn and qty and price and tax and total:
                    mapped = zip(item,hsn,qty,price,tax,total)
                    mapped = list(mapped)
                    for ele in mapped:
                        pItems = Purchase_items.objects.create(name = ele[0],hsn=ele[1],quantity=ele[2],rate=ele[3],tax=ele[4],total=ele[5],pid = pid, cid=cmp)


                if 'new_purchase' in request.POST:
                    return redirect(addNewPurchase)
                return redirect(goPurchases)
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong, Please try again.!')
            return redirect(addNewPurchase)
    return redirect('/')


@login_required(login_url="login")
def purchasesInBetween(request):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            if request.method == 'GET':
                start_date = request.GET['start_date']
                end_date = request.GET['end_date']
                purchases = Purchases.objects.filter(cid = cmp).filter(date__gte = start_date, date__lte = end_date)
                if not purchases:
                    messages.warning(request, f'No purchases found in between {start_date} to {end_date}')
                    purchases = Purchases.objects.filter(cid = cmp)
                context = {
                    'cmp': cmp,
                    'purchases': purchases,
                    'start':start_date,
                    'end':end_date,
                }
                return render(request, 'purchases.html',context)
        except Exception as e:
            print(e)
            return redirect(goPurchases)
    return redirect('/')


@login_required(login_url="login")
def viewPurchaseBill(request,id):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            purchases = Purchases.objects.filter(cid = cmp)
            bill = Purchases.objects.get(cid = cmp, bill_no = id)
            items = Purchase_items.objects.filter(cid = cmp, pid = bill)
            context = {
                'cmp': cmp,
                'purchases':purchases,
                'bill': bill,
                'items':items,
            }
            return render(request, 'purchase_bill.html',context)
        except Exception as e:
            print(e)
            return redirect(goPurchases)
    return redirect('/')


@login_required(login_url="login")
def editPurchaseBill(request,id):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            bill = Purchases.objects.get(cid = cmp, bill_no = id)
            p_items = Purchase_items.objects.filter(cid = cmp, pid = bill)
            items = Items.objects.filter(cid = cmp)
            context = {
                'cmp': cmp,
                'bill': bill,
                'items':items,
                'purchase_items':p_items,
            }

            return render(request, 'edit_purchase_bill.html',context)
        except Exception as e:
            print(e)
            return redirect(viewPurchaseBill, id)
    return redirect('/')


@login_required(login_url="login")
def updatePurchaseBill(request,id):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            bill = Purchases.objects.get(cid = cmp, bill_no = id)

            bill.date = request.POST['date']
            if 'party' in request.POST:
                bill.party_name = request.POST['party_name']
                bill.phone_number = request.POST['party_phone']
                bill.gstin = request.POST['party_gstin']
            else:
                bill.party_name = ""
                bill.phone_number = ""
                bill.gstin = ""
            
            bill.subtotal = request.POST['subtotal']
            bill.tax = request.POST['tax']
            bill.adjustment = request.POST['adjustment']
            bill.total_amount = request.POST['grand_total']

            bill.save()

            item = request.POST.getlist("item[]")
            hsn  = request.POST.getlist("hsn[]")
            qty = request.POST.getlist("qty[]")
            price = request.POST.getlist("price[]")
            tax = request.POST.getlist("tax[]")
            total = request.POST.getlist("total[]")
            prchs_item_ids = request.POST.getlist("id[]")
            item_ids = [int(id) for id in prchs_item_ids]

            
            prchs_item = Purchase_items.objects.filter(pid = bill)
            object_ids = [obj.id for obj in prchs_item]

            ids_to_delete = [obj_id for obj_id in object_ids if obj_id not in item_ids]
            Purchase_items.objects.filter(id__in=ids_to_delete).delete()
            
            count = Purchase_items.objects.filter(pid = bill, cid = cmp).count()
            if len(item)==len(hsn)==len(qty)==len(price)==len(tax)==len(total):
                try:
                    mapped=zip(item,hsn,qty,price,tax,total,item_ids)
                    mapped=list(mapped)
                    
                    for ele in mapped:
                        if int(len(item))>int(count):
                            if ele[6] == 0:
                                itemAdd= Purchase_items.objects.create(name = ele[0], hsn=ele[1],quantity=ele[2],rate=ele[3],tax=ele[4],total=ele[5] ,pid = bill ,cid = cmp)
                            else:
                                itemAdd = Purchase_items.objects.filter( id = ele[6],cid = cmp).update(name = ele[0],hsn=ele[1],quantity=ele[2],rate=ele[3],tax=ele[4],total=ele[5])
                        else:
                            itemAdd = Purchase_items.objects.filter( id = ele[6],cid=cmp).update(name = ele[0],hsn=ele[1],quantity=ele[2],rate=ele[3],tax=ele[4],total=ele[5])
                            
                except Exception as e:
                        print(e)
                        mapped=zip(item,hsn,qty,price,tax,total,item_ids)
                        mapped=list(mapped)
                        
                        for ele in mapped:
                            created =Purchase_items.objects.filter(id=ele[6] ,cid=cmp).update(name = ele[0],hsn=ele[1],quantity=ele[2],rate=ele[3],tax=ele[4],total=ele[5])



            return redirect(viewPurchaseBill,id)
        except Exception as e:
            print(e)
            return redirect(editPurchaseBill, id)
    return redirect('/')



@login_required(login_url="login")
def deletePurchaseBill(request, id):
    if request.user:
        try:
            cmp = Company.objects.get(user = request.user.id)
            bill = Purchases.objects.get(cid = cmp, bill_no = id)
            items = Purchase_items.objects.filter(cid = cmp, pid = bill).delete()
            bill.delete()
            # items.delete()
            return redirect(goPurchases)
        except Exception as e:
            print(e)
            return redirect(viewPurchaseBill, id)
    return redirect('/')




# SALES

@login_required(login_url="login")
def goSales(request):
    if request.user:
        try:
            cmp = Company.objects.get(user = request.user.id)
            context = {
                'cmp':cmp,
                'sales':Sales.objects.filter(cid = cmp),
            }
            return render(request, 'sales.html',context)
        except Exception as e:
            print(e)
            return redirect(goDashboard)
    return redirect('/')


@login_required(login_url="login")
def addNewSale(request):
    if request.user:
        try:
            model_meta = Sales._meta
            pk_name = model_meta.pk.name
            table_name = model_meta.db_table
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_NAME = %s", [table_name])
                next_id = cursor.fetchone()[0]

            cmp = Company.objects.get(user=request.user.id)
            items = Items.objects.filter( cid = cmp)
            context = {
                'cmp': cmp,
                'bill_no':next_id,
                'items': items,

            }
            return render(request, 'add_sale.html',context)
        except Exception as e:
            print(e)
            return redirect(goDashboard)
    return redirect('/')


@login_required(login_url="login")
def createNewSale(request):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            if request.method == 'POST':
                sale = Sales(
                    cid = cmp,
                    date = request.POST['date'],
                    party_name = request.POST['party_name'],
                    phone_number = request.POST['party_phone'],
                    gstin = request.POST['party_gstin'],
                    subtotal = request.POST['subtotal'],
                    tax = request.POST['tax'],
                    adjustment = request.POST['adjustment'],
                    total_amount = request.POST['grand_total'],
                )
                sale.save()

                item = request.POST.getlist("item[]")
                hsn  = request.POST.getlist("hsn[]")
                qty = request.POST.getlist("qty[]")
                price = request.POST.getlist("price[]")
                tax = request.POST.getlist("tax[]")
                total = request.POST.getlist("total[]")

                sid = Sales.objects.get( bill_no = sale.bill_no)

                if len(item)==len(hsn)==len(qty)==len(price)==len(tax)==len(total) and item and hsn and qty and price and tax and total:
                    mapped = zip(item,hsn,qty,price,tax,total)
                    mapped = list(mapped)
                    for ele in mapped:
                        sItems = Sales_items.objects.create(name = ele[0],hsn=ele[1],quantity=ele[2],rate=ele[3],tax=ele[4],total=ele[5],sid = sid, cid=cmp)


                if 'new_sale' in request.POST:
                    return redirect(addNewSale)
                return redirect(goSales)
        except Exception as e:
            print(e)
            return redirect(addNewSale)
    return redirect('/')


@login_required(login_url="login")
def salesInBetween(request):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            if request.method == 'GET':
                start_date = request.GET['start_date']
                end_date = request.GET['end_date']
                sales = Sales.objects.filter(cid = cmp).filter(date__gte = start_date, date__lte = end_date)
                if not sales:
                    messages.warning(request, f'No sales found in between {start_date} to {end_date}')
                    sales = Sales.objects.filter(cid = cmp)
                context = {
                    'cmp': cmp,
                    'sales': sales,
                    'start':start_date,
                    'end':end_date,
                }
                return render(request, 'sales.html',context)
        except Exception as e:
            print(e)
            return redirect(goSales)
    return redirect('/')


@login_required(login_url="login")
def viewSalesBill(request,id):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            sales = Sales.objects.filter(cid = cmp)
            bill = Sales.objects.get(cid = cmp, bill_no = id)
            items = Sales_items.objects.filter(cid = cmp, sid = bill)
            context = {
                'cmp': cmp,
                'sales':sales,
                'bill': bill,
                'items':items,
            }
            return render(request, 'sales_bill.html',context)
        except Exception as e:
            print(e)
            return redirect(goSales)
    return redirect('/')


@login_required(login_url="login")
def editSalesBill(request,id):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            bill = Sales.objects.get(cid = cmp, bill_no = id)
            s_items = Sales_items.objects.filter(cid = cmp, sid = bill)
            items = Items.objects.filter(cid = cmp)
            context = {
                'cmp': cmp,
                'bill': bill,
                'items':items,
                'sales_items':s_items,
            }

            return render(request, 'edit_sale.html',context)
        except Exception as e:
            print(e)
            return redirect(viewSalesBill, id)
    return redirect('/')



@login_required(login_url="login")
def updateSaleBill(request,id):
    if request.user:
        try:
            cmp = Company.objects.get(user=request.user.id)
            bill = Sales.objects.get(cid = cmp, bill_no = id)

            bill.date = request.POST['date']
            if 'party' in request.POST:
                bill.party_name = request.POST['party_name']
                bill.phone_number = request.POST['party_phone']
                bill.gstin = request.POST['party_gstin']
            else:
                bill.party_name = ""
                bill.phone_number = ""
                bill.gstin = ""
            
            bill.subtotal = request.POST['subtotal']
            bill.tax = request.POST['tax']
            bill.adjustment = request.POST['adjustment']
            bill.total_amount = request.POST['grand_total']

            bill.save()

            item = request.POST.getlist("item[]")
            hsn  = request.POST.getlist("hsn[]")
            qty = request.POST.getlist("qty[]")
            price = request.POST.getlist("price[]")
            tax = request.POST.getlist("tax[]")
            total = request.POST.getlist("total[]")
            sales_item_ids = request.POST.getlist("id[]")
            item_ids = [int(id) for id in sales_item_ids]

            
            prchs_item = Purchase_items.objects.filter(pid = bill)
            object_ids = [obj.id for obj in prchs_item]

            ids_to_delete = [obj_id for obj_id in object_ids if obj_id not in item_ids]
            Purchase_items.objects.filter(id__in=ids_to_delete).delete()
            
            count = Purchase_items.objects.filter(pid = bill, cid = cmp).count()
            if len(item)==len(hsn)==len(qty)==len(price)==len(tax)==len(total):
                try:
                    mapped=zip(item,hsn,qty,price,tax,total,item_ids)
                    mapped=list(mapped)
                    
                    for ele in mapped:
                        if int(len(item))>int(count):
                            if ele[6] == 0:
                                itemAdd= Purchase_items.objects.create(name = ele[0], hsn=ele[1],quantity=ele[2],rate=ele[3],tax=ele[4],total=ele[5] ,pid = bill ,cid = cmp)
                            else:
                                itemAdd = Purchase_items.objects.filter( id = ele[6],cid = cmp).update(name = ele[0],hsn=ele[1],quantity=ele[2],rate=ele[3],tax=ele[4],total=ele[5])
                        else:
                            itemAdd = Purchase_items.objects.filter( id = ele[6],cid=cmp).update(name = ele[0],hsn=ele[1],quantity=ele[2],rate=ele[3],tax=ele[4],total=ele[5])
                            
                except Exception as e:
                        print(e)
                        mapped=zip(item,hsn,qty,price,tax,total,item_ids)
                        mapped=list(mapped)
                        
                        for ele in mapped:
                            created =Purchase_items.objects.filter(id=ele[6] ,cid=cmp).update(name = ele[0],hsn=ele[1],quantity=ele[2],rate=ele[3],tax=ele[4],total=ele[5])



            return redirect(viewSalesBill,id)
        except Exception as e:
            print(e)
            return redirect(editSalesBill, id)
    return redirect('/')



@login_required(login_url="login")
def deleteSaleBill(request, id):
    if request.user:
        try:
            cmp = Company.objects.get(user = request.user.id)
            bill = Sales.objects.get(cid = cmp, bill_no = id)
            items = Sales_items.objects.filter(cid = cmp, sid = bill).delete()
            bill.delete()
            # items.delete()
            return redirect(goSales)
        except Exception as e:
            print(e)
            return redirect(viewSalesBill, id)
    return redirect('/')