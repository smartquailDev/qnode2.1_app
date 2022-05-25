from django.urls import path
from . import views

app_name = 'courses_exams'

urlpatterns = [
    path('instructions/', views.instruc, name ='intruciones'),
    path('test_list', views.test_list, name='test_list'),
    path('<slug:subject_test_slug>/', views.test_list,
         name='test_list_by_subject_test'),
    path('<int:id>/<slug:slug>/', views.test_detail,
         name='test_detail'),
]
