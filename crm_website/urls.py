from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register'),
    path('record/<record_id>', views.update_record, name='update_record'),
    path('delete_record/<record_id>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('delete_record/<record_id>', views.delete_record, name='delete_record'),
    path('generate_pdf', views.generate_pdf, name='generate_pdf'),
    path('display_deleted_records', views.display_deleted_records, name="display_deleted_records"),
    
]
