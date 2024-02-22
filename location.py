import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pharm.settings") 
django.setup()

import requests
from django.conf import settings

from hospitals.models import Institution
from django.core.files.base import ContentFile

def update_institutions_from_google_places(base_country):
    api_key = settings.GOOGLE_API_KEY
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

    # Define parameters for the API request
    params = {
        'query': f'hospitals in {base_country}',
        'key': api_key
    }

    print("Requesting data from Google Places API...")
    response = requests.get(url, params=params)
    
    print("Response status code:", response.status_code)
    
    data = response.json()
    
    print("API Response:", data)
    
    # Inside the for loop
    if 'results' in data:
        hospitals = data['results']
        for hospital in hospitals:
            institution_name = hospital['name']
            country = base_country
            latitude = hospital['geometry']['location']['lat']
            longitude = hospital['geometry']['location']['lng']
            address_components = hospital.get('address_components', [])
            county = next((comp['long_name'] for comp in address_components if 'administrative_area_level_2' in comp['types']), None)
            postal_code = next((comp['long_name'] for comp in address_components if 'postal_code' in comp['types']), None)
            photo_reference = None

            opening_hours_data = hospital.get('opening_hours', {})
            opening_hours = {
                'monday': opening_hours_data.get('monday'),
                'tuesday': opening_hours_data.get('tuesday'),
                'wednesday': opening_hours_data.get('wednesday'),
                'thursday': opening_hours_data.get('thursday'),
                'friday': opening_hours_data.get('friday'),
                'saturday': opening_hours_data.get('saturday'),
                'sunday': opening_hours_data.get('sunday'),
            }
            if 'photos' in hospital:
                photo_reference = hospital['photos'][0]['photo_reference']
                photo_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}'
                photo_response = requests.get(photo_url)
                if photo_response.status_code == 200:
                    institution_image = ContentFile(photo_response.content, name=f"{institution_name}_photo.jpg")
                    # Create or update Institution instance
                    institution, created = Institution.objects.update_or_create(
                        institution_name=institution_name,
                        country=country,
                        latitude=latitude,
                        longitude=longitude,
                        county=county,
                        postal_code=postal_code,
                        image=institution_image
                    )

                    # Handle opening hours
                    if 'opening_hours' in hospital:
                        opening_hours_data = hospital['opening_hours']
                        institution.opening_hours_monday = opening_hours_data.get('monday')
                        institution.opening_hours_tuesday = opening_hours_data.get('tuesday')
                        institution.opening_hours_wednesday = opening_hours_data.get('wednesday')
                        institution.opening_hours_thursday = opening_hours_data.get('thursday')
                        institution.opening_hours_friday = opening_hours_data.get('friday')
                        institution.opening_hours_saturday = opening_hours_data.get('saturday')
                        institution.opening_hours_sunday = opening_hours_data.get('sunday')
                        institution.save()

                    # Handle photos
                    if 'photos' in hospital:
                        photo_reference = hospital['photos'][0]['photo_reference']
                        photo_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}'
                        photo_response = requests.get(photo_url)
                        if photo_response.status_code == 200:
                            institution_photo = ContentFile(photo_response.content, name=f"{institution_name}_photo.jpg")
                            institution.photo = institution_photo
                            institution.save()

                    print(f'{"Created" if created else "Updated"} institution: {institution.institution_name}')
                else:
                    print(f"Failed to fetch photo for {institution_name}. Status code: {photo_response.status_code}")

def run_script():
    base_country = settings.BASE_COUNTRY
    update_institutions_from_google_places(base_country)

if __name__ == '__main__':
    run_script()
