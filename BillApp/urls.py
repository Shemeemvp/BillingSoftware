from django.contrib import admin
from django.urls import path, include
from BillApp import views

urlpatterns = [
    path('',views.login, name='login'),
    path('register_user',views.registerUser, name='registerUser'),
    path('user_login',views.userLogin, name='userLogin'),
    path('logout',views.userLogout, name='userLogout'),
    path('validate_email',views.validateEmail, name='validateEmail'),
    path('validate_username',views.validateUsername, name='validateUsername'),
    path('forgot_password',views.forgotPassword, name='forgotPassword'),
    path('show_profile',views.showProfile, name='showProfile'),
    path('update_user_profile',views.updateUserProfile, name='updateUserProfile'),
    path('update_logo/<int:id>',views.updateLogo, name='updateLogo'),
    path('remove_company_logo',views.removeLogo, name='removeLogo'),


    path('go_dashboard', views.goDashboard, name='goDashboard'),

    path('show_items',views.goItems, name='goItems'),
    path('show_item_details/<int:id>',views.showItemData, name= 'showItemData'),


    path('show_purchases',views.goPurchases, name='goPurchases'),
    path('add_new_purchase',views.addNewPurchase, name='addNewPurchase'),
    path('get_item_data',views.getItemData, name='getItemData'),
    path('create_new_purchase',views.createNewPurchase, name='createNewPurchase'),
    path('purchases_in_between',views.purchasesInBetween, name='purchasesInBetween'),
    path('view_purchase_bill/<int:id>',views.viewPurchaseBill, name='viewPurchaseBill'),
    path('edit_purchase_bill/<int:id>',views.editPurchaseBill, name='editPurchaseBill'),
    path('update_purchase_bill/<int:id>',views.updatePurchaseBill, name='updatePurchaseBill'),


    path('show_sales',views.goSales, name='goSales'),
    path('add_new_sale',views.addNewSale, name='addNewSale'),
    path('create_new_sale',views.createNewSale,name='createNewSale'),
    path('sales_in_between',views.salesInBetween, name='salesInBetween'),


    path('add_new_item',views.addNewItem, name='addNewItem'),
    path('delete_item/<int:id>',views.deleteItem, name='deleteItem'),
    path('edit_item/<int:id>',views.editItem, name='editItem'),
    path('edit_item_data/<int:id>',views.editItemData, name='editItemData'),
    path('create_new_item',views.createNewItem, name='createNewItem'),
    path('create_new_itemunit',views.createitemunit, name='createitemunit'),
    path('get_item_units',views.getItemUnits, name='getItemUnits'),
    path('update_stock/<int:id>',views.updateStock, name='updateStock'),


    path('edit_transaction/<int:id>',views.editTransaction, name='editTransaction'),
    path('edit_transaction_data/<int:id>',views.editTransactionData, name='editTransactionData'),
    path('delete_transaction/<int:id>',views.deleteTransaction, name='deleteTransaction'),
    


]