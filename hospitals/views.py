from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .forms import UserReviewForm
from .models import Institution, Insurance, UserReview, Service

def institutions(request):
    institutions = Institution.objects.all()
    return render(request, 'hospitals/institutions.html', {'institutions': institutions})

def get_reviews(request):
    if request.method == 'GET' and request.is_ajax():
        institution_id = request.GET.get('institution_id')
        institution = get_object_or_404(Institution, pk=institution_id)
        reviews = UserReview.objects.filter(institution=institution)
        
        # Extracting reviews data
        reviews_data = [{'review_summary': review.review_summary} for review in reviews]
        
        # Including institution name in the response
        data = {
            'institution_name': institution.institution_name,
            'reviews': reviews_data
        }
        
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request'})
def institution_detail(request, institution_id=None):
    if institution_id:
        institution = get_object_or_404(Institution, pk=institution_id)
        insurances = Insurance.objects.filter(institution=institution)
        reviews = UserReview.objects.filter(institution=institution)
        services = Service.objects.filter(institution=institution)
        all_institutions = Institution.objects.all() 

        if request.method == 'POST' and request.is_ajax():
            form = UserReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.institution = institution
                review.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'errors': form.errors}, status=400)
        else:
            form = UserReviewForm()

        context = {
            'institution': institution,
            'insurances': insurances,
            'reviews': reviews,
            'services': services,
            'form': form,
            'latitude': institution.latitude,
            'longitude': institution.longitude,
            'userProfile': institution.user_profile,
            'all_institutions': all_institutions,
            "google_api_key": settings.GOOGLE_API_KEY,
	        "base_country": settings.BASE_COUNTRY,
        }

        return render(request, 'hospitals/institutions.html', context)
    else:
        return institutions(request)
