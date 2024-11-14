from django.shortcuts import render, redirect
import json
from .models import Profile, TouristAttraction
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.contrib.gis.db.models.functions import Distance

def map_view(request):
    # checking if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('profile_setup')

    # default location if the user's location is not set
    if profile.location is None:
        user_location = (53.3498, -6.2603)  # Dublin coordinates
    else:
        user_location = (profile.location.y, profile.location.x)

    # retrieving all TouristAttraction entries to show on the map
    attractions = TouristAttraction.objects.all()

    # distance to the user's location
    attractions_with_distance = attractions.annotate(
        distance=Distance('mpoint', profile.location)
    )

    # formatting the attractions
    formatted_attractions = [
        {
            'name': attraction.name,
            'tourism': attraction.tourism or "N/A",
            'address': attraction.address or "N/A",
            'website': attraction.website or "N/A",
            'phone': attraction.phone or "N/A",
            'email': attraction.email or "N/A",
            'opening_hours': attraction.opening_hours or "N/A",
            'latitude': attraction.mpoint.y,  
            'longitude': attraction.mpoint.x,  
            'distance': attraction.distance.km if attraction.distance else "N/A",  # Distance in km
        }
        for attraction in attractions_with_distance
    ]

    # getting nearby attractions within 5 km, limit to 20, and sorting by distance
    nearby_attractions = attractions_with_distance.filter(distance__lte=5 * 1000).order_by('distance')[:20]

    # formatting for display
    nearby_attractions_list = [
        {
            'name': attraction.name,
            'tourism': attraction.tourism or "N/A",
            'address': attraction.address or "N/A",
            'website': attraction.website or "N/A",
            'phone': attraction.phone or "N/A",
            'email': attraction.email or "N/A",
            'opening_hours': attraction.opening_hours or "N/A",
            'distance': attraction.distance.km if attraction.distance else "N/A",
        }
        for attraction in nearby_attractions
    ]
    
    attractions_json = json.dumps(formatted_attractions)

    return render(request, 'map.html', {
        'attractions': attractions_json,
        'user_latitude': user_location[0],
        'user_longitude': user_location[1],
        'nearby_attractions': nearby_attractions_list,
    })

    
#login & logout views
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.gis.geos import Point

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            
            if latitude and longitude:
                location = Point(float(longitude), float(latitude))
                Profile.objects.create(user=user, location=location)
            else:
                Profile.objects.create(user=user)  # No location provided
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def update_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        user = request.profile
        user.location = Point(float(longitude), float(latitude))
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})