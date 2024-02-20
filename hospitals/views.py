
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .forms import UserReviewForm
from .models import Institution, Insurance, UserReview, Service

def institution_detail(request, institution_id):
    institution = get_object_or_404(Institution, pk=institution_id)
    insurances = Insurance.objects.filter(institution=institution)
    reviews = UserReview.objects.filter(institution=institution)
    services = Service.objects.filter(institution=institution)

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
    }
    return render(request, 'reason.html', context)
def institution_list(request):
    institutions = Institution.objects.all()
    return render(request, 'institution_list.html', {'institutions': institutions})