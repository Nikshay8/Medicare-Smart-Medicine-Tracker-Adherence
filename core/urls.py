from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_page, name='home'),
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_page, name='logout'),
    path('add-medicine/', views.add_medicine, name='add_medicine'),
    path('edit-medicine/<int:id>/', views.edit_medicine, name='edit_medicine'),
    path('delete-medicine/<int:id>/', views.delete_medicine, name='delete_medicine'),
    path('mark-status/<int:id>/<str:status>/', views.mark_status, name='mark_status'),
    path('undo-log/<int:log_id>/', views.undo_last_log, name='undo_last_log'),
    path('add-caregiver/', views.add_caregiver, name='add_caregiver'),
    path('view-caregiver/', views.view_caregiver, name='view_caregiver'),
    path('delete-caregiver/', views.delete_caregiver, name='delete_caregiver'),
    path('history/', views.medicine_history, name='medicine_history'),
    path('reports/', views.reports, name='reports'),
    path('profile/', views.profile, name='profile'),
]
