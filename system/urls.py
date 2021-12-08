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
    path('log_out/', views.LogOutView.as_view(), name='log_out'),
    path('update_user/', views.UpdateUserView.as_view(), name='update_user'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('create_club/',views.CreateClubView.as_view(), name='create_club'),
    path('show_club/<int:club_id>', views.ShowClubView.as_view(), name='show_club'),
    path('apply_club/<int:club_id>',views.ApplyClubView.as_view(), name='apply_club'),
    path('<int:club_id>/waiting_list/',views.WaitingListView.as_view(), name='waiting_list'),
    path('<int:club_id>/members_list/', views.MembersListView.as_view(), name='members_list'),
    path('<int:club_id>/show_member/<int:member_id>', views.ShowMemberView.as_view(), name='show_member'),
    path('<int:club_id>/applicants_list/', views.ApplicantsListView.as_view(), name='applicants_list'),
    path('<int:club_id>/show_applicant/<int:applicant_id>', views.ShowApplicantView.as_view(), name='show_applicant'),
    path('<int:club_id>/approve_applicant/<int:applicant_id>', views.ApproveApplicantView.as_view(), name='approve_applicant'),
    path('<int:club_id>/reject_applicant/<int:applicant_id>', views.RejectApplicantView.as_view(), name='reject_applicant'),
    path('<int:club_id>/promote_member/<int:member_id>', views.PromoteMemberView.as_view(), name='promote_member'),
    path('<int:club_id>/demote_officer/<int:member_id>', views.DemoteOfficerView.as_view(), name='demote_officer'),
    path('<int:club_id>/remove_user/<int:user_id>', views.RemoveUserView.as_view(), name='remove_user'),
    path('<int:club_id>/transfer_ownership/<int:member_id>', views.TransferOwnershipView.as_view(), name='transfer_ownership'),
    path('delete_account/',views.DeleteAccountView.as_view(), name='delete_account'),
]
