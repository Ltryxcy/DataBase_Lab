from django.urls import path

from . import views

urlpatterns = [
    path('branches/', views.branches, name='branches'),
]