from django.urls import path
from .views import (VacancyListView, VacancyDetailView, filter_vacancies, RevokeApplicationView,
                    ApplicationDetailView)

app_name = 'vacancy'

urlpatterns = [
    path('', VacancyListView.as_view(), name='vacancy_list'),
    path('<int:pk>/', VacancyDetailView.as_view(), name='vacancy_detail'),
    path('filter/', filter_vacancies, name='filter_vacancies'),
    path('revoke_application/<int:pk>/', RevokeApplicationView.as_view(), name='revoke_application'),
    path('application/<int:pk>/', ApplicationDetailView.as_view(), name='application_details'),
]