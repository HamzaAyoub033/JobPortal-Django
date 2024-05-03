from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from JobPortal import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('candidate_register/', views.candidate_register.as_view(), name='candidate_register'),
    path('profile/', views.CandidateDetailView.as_view(), name='detail'),
    path('update_candidate/<int:pk>',views.candidate_update.as_view(success_url="/profile"),name="update_candidate"),
    path('recruiter_register/', views.recruiter_register.as_view(), name='recruiter_register'),
    path('recruiterprofile/', views.recruiterDetailView.as_view(), name='detail'),
    path('recuiter_candidate/<int:pk>',views.recruiter_update.as_view(success_url="/recruiterprofile"),name="update_recuiter"),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('full_time/', views.full_time, name='full_time'),
    path('internship/', views.internship, name='internship'),
    path('recruiter_posting', views.recruiter_posting.as_view(success_url='/'), name='recruiter_posting'),
    path('jobs_result/', views.jobs_result, name='jobs_result'),
    path('applied_for/', views.Applied_For, name='applied_for'),
    path('search/', views.search, name='search'),
    path('candidate_apply/<int:pk>', views.candidate_apply, name='candidate_apply'),
    path('application_view/', views.application_view, name='application_view'),
    path('contact/', views.contact, name='contact'),
    path('jobs_detail/<int:pk>', views.jobs_detail, name='detailview'),
    path('cand_status/<int:pk>', views.cand_status, name='cand_status'),
    path('cand_reject/<int:pk>', views.cand_reject, name='cand_reject'),
    path('all_posting/', views.all_posting, name='all_posting'),


]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
