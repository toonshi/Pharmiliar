from django.urls import path
# from .views import institutions, institution_detail
from . import views
urlpatterns = [
    path('institutions/', views.institutions, name='institutions'),
    path('institution/<int:institution_id>/', views.institution_detail, name='institution_detail'),
    
]
