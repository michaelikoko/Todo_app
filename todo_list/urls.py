from django.urls import path
from todo_list import views

app_name = 'todo_list'
urlpatterns = [
    path('', views.Landing_Page.as_view(), name='landing_page'),
    path('register', views.Register_User_View.as_view(), name='registration_page'),
    path('verify_email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('reset_password', views.Reset_Password_View.as_view(), name='reset_password'),
    path('reset_password_confirm/<uidb64>/<token>/', views.Reset_Password_Confirm_View.as_view(), name='reset_password_confirm'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('add_task', views.Add_Task_View.as_view(), name='add_task'),
    path('edit_details/<int:pk>', views.Edit_Details_View.as_view(), name='edit_details'),
    path('change_password/<int:pk>', views.Change_Password_View.as_view(), name='change_password'),
    path('delete_task/<int:pk>', views.Delete_Task.as_view(), name='delete_task'),
    path('search', views.Search.as_view(), name='search'),
]