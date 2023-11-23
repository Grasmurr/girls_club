from django.urls import path
from . import views

urlpatterns = [
    path('event/create/', views.create_event),
    path('event/update/<str:name>/', views.update_event),
    path('event/delete/<str:name>/', views.delete_event),
    path('event/get/<str:name>/', views.get_event),

    path('member_girl/create/', views.create_member_girl),
    path('member_girl/update/<int:telegram_id>/', views.update_member_girl),
    path('member_girl/delete/<int:telegram_id>/', views.delete_member_girl),
    path('member_girl/get/<int:telegram_id>/', views.get_member_girl),
    path('member_girl/get_all/', views.get_all),

    path('newsletter/create_or_update/<int:number>/', views.create_or_update_newsletter),
    path('newsletter/delete/<int:number>/', views.delete_newsletter),
    path('newsletter/get/<int:number>/', views.get_newsletter),
]