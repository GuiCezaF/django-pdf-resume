from django.urls import path

from core import views

app_name= 'core'

urlpatterns = [
  path('', views.home, name='resume.home'),
  path('generate-resume/', views.generate_resume, name='resume.generate')
]