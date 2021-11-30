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
    path('', views.HomeView.as_view(), name='home'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('update_user/', views.UpdateUserView.as_view(), name='update_user'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('create_club/',views.create_club, name='create_club'),
    path('show_club/<int:club_id>', views.show_club, name='show_club'),
    path('apply_club/<int:club_id>',views.apply_club, name='apply_club'),
    path('<int:club_id>/waiting_list/',views.WaitingListView.as_view(), name='waiting_list'),
    path('<int:club_id>/members_list/', views.members_list, name='members_list'),
    path('<int:club_id>/show_member/<int:member_id>', views.show_member, name='show_member'),
    path('<int:club_id>/applicants_list/', views.applicants_list, name='applicants_list'),
    path('<int:club_id>/show_applicant/<int:applicant_id>', views.show_applicant, name='show_applicant'),
    path('<int:club_id>/approve_applicant/<int:applicant_id>', views.approve_applicant, name='approve_applicant'),
    path('<int:club_id>/reject_applicant/<int:applicant_id>', views.reject_applicant, name='reject_applicant'),
    path('<int:club_id>/promote_member/<int:member_id>',views.promote_member, name='promote_member'),
    path('<int:club_id>/demote_officer/<int:member_id>',views.demote_officer, name='demote_officer'),
    path('<int:club_id>/transfer_ownership/<int:member_id>',views.transfer_ownership, name='transfer_ownership'),
    path('delete_account/',views.delete_account, name='delete_account'),
]
