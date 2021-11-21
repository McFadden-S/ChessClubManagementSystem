"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('change_password/', views.change_password, name='change_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('members_list/', views.members_list, name='members_list'),
    path('applicants_list/', views.applicants_list, name='applicants_list'),
    path('show_applicant/<int:applicant_id>', views.show_applicant, name='show_applicant'),
    path('approve_applicant/<int:applicant_id>', views.approve_applicant, name='approve_applicant'),
    path('show_member/<int:member_id>', views.show_member, name='show_member'),
    path('waiting_list/',views.waiting_list, name='waiting_list'),
    path('promote_member/<int:member_id>',views.promote_member, name='promote_member'),
    path('demote_officer/<int:member_id>',views.demote_officer, name='demote_officer'),
    path('transfer_ownership/<int:member_id>',views.transfer_ownership, name='transfer_ownership'),
]
