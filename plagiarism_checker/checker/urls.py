from django.urls import path
from .views import index, check_plagiarism

urlpatterns = [
    path('', index, name='index'),
    path('check/', check_plagiarism, name='check_plagiarism'),
]
