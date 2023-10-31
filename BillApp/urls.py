from django.contrib import admin
from django.urls import path, include
from BillApp import views

urlpatterns = [
    path('',views.login, name='login'),
    path('register_user',views.registerUser, name='registerUser'),
    path('user_login',views.userLogin, name='userLogin'),
    path('logout',views.userLogout, name='userLogout'),
    path('go_dashboard', views.goDashboard, name='goDashboard'),
    path('validate_email',views.validateEmail, name='validateEmail'),
    path('validate_username',views.validateUsername, name='validateUsername'),
    path('show_items',views.goItems, name='goItems'),
    path('show_item_details/<int:id>',views.showItemData, name= 'showItemData'),
    path('add_new_item',views.addNewItem, name='addNewItem'),
    path('delete_item/<int:id>',views.deleteItem, name='deleteItem'),
    path('edit_item/<int:id>',views.editItem, name='editItem'),
    path('edit_item_data/<int:id>',views.editItemData, name='editItemData'),
    path('create_new_item',views.createNewItem, name='createNewItem'),
    path('create_new_itemunit',views.createitemunit, name='createitemunit'),
    path('get_item_units',views.getItemUnits, name='getItemUnits'),
    path('update_stock/<int:id>',views.updateStock, name='updateStock'),
    path('delete_transaction/<int:id>',views.deleteTransaction, name='deleteTransaction'),
    path('forgot_password',views.forgotPassword, name='forgotPassword')


]