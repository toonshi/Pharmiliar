from django.urls import path
# from .views import institution_list, institution_detail
from . import views
urlpatterns = [
    path('institutions/', views.institution_list, name='institution_list'),
    path('institution/<int:institution_id>/', views.institution_detail, name='institution_detail'),
    
]
