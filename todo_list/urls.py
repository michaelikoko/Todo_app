from django.urls import path
from todo_list import views

app_name = 'todo_list'
urlpatterns = [
    path('', views.Landing_Page.as_view(), name='landing_page'),
    path('register', views.Register_User_View.as_view(), name='registration_page'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('add_task', views.Add_Task_View.as_view(), name='add_task'),
    path('edit_details/<int:pk>', views.Edit_Details_View.as_view(), name='edit_details'),
    path('change_password/<int:pk>', views.Change_Password_View.as_view(), name='change_password'),
    path('delete_task/<int:pk>', views.Delete_Task.as_view(), name='delete_task'),
    path('search', views.Search.as_view(), name='search'),
]