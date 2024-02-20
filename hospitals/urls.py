from django.urls import path
from .views import institution_list, institution_detail

urlpatterns = [
    path('institutions/', institution_list, name='institution_list'),
    path('institution/<int:institution_id>/', institution_detail, name='institution_detail'),
]
