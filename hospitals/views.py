from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .forms import UserReviewForm
from .models import Institution

def institutions(request):
    institutions = Institution.objects.all()
    google_api_key = settings.GOOGLE_API_KEY
    base_country = settings.BASE_COUNTRY
    return render(request, 'hospitals/institutions.html', {'institutions': institutions, 'google_api_key': google_api_key, 'base_country': base_country})

def get_reviews(request):
    if request.method == 'GET' and request.is_ajax():
        institution_id = request.GET.get('institution_id')
        institution = get_object_or_404(Institution, pk=institution_id)
        reviews = institution.userreview_set.all()

        reviews_data = [{'review_summary': review.review_summary} for review in reviews]

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
        insurances = institution.insurance_set.all()
        reviews = institution.userreview_set.all()
        services = institution.service_set.all()

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
            "google_api_key": settings.GOOGLE_API_KEY,
            "base_country": settings.BASE_COUNTRY,
        }

        return render(request, 'hospitals/institution_detail.html', context)
    else:
        return JsonResponse({'error': 'Invalid request'})
