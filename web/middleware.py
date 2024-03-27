# myapp/middleware.py
from .models import *
from django.utils import timezone
from django import forms

from django.contrib.sessions.models import Session

from geopy.geocoders import Nominatim

def get_location_from_ip(ip_address):
    geolocator = Nominatim(user_agent="myGeocoder")

    try:
        location = geolocator.geocode(ip_address)
        if location:
            return location.address
        else:
            return "Location not found"
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error occurred while fetching location"


class UserAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user's session already has an access record
        if not request.session.get('access_recorded', False):

            referer = request.META.get('HTTP_REFERER')
            if referer:
                UserAccess.objects.create(
                    ip_address=request.META.get('REMOTE_ADDR'),
                    location=request.META.get('HTTP_USER_AGENT'),
                    access_time=timezone.now(),
                    referer=referer
                )


            # Mark that the access has been recorded for this session
            request.session['access_recorded'] = True

        response = self.get_response(request)
        return response