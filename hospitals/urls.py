from django.urls import path
from . import views

app_name = 'hospitals'

urlpatterns = [
    path('hospitals', views.institutions, name='institutions'),  # Assuming this is the view for listing institutions
    path('institution/<int:institution_id>/', views.institution_detail, name='institution_detail'),
]
