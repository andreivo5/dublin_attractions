from pathlib import Path
from django.contrib.gis.geos import Point
from .models import TouristAttraction
import json

tourist_attraction_geojson = Path(__file__).resolve().parent / 'data' / 'tourism.geojson'

def run(verbose=True):
    with open(tourist_attraction_geojson, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    for feature in data['features']:
        properties = feature.get('properties', {})
        name = properties.get('name')
        
        # skipping entries without a valid name
        if not name:
            if verbose:
                print("Skipping feature with no valid name.")
            continue
        
        # extracting properties, and defaulting to N/A if missing
        tourism = properties.get('tourism', "N/A")
        address = ", ".join([properties.get('addr:street', ''),
                             properties.get('addr:housenumber', ''),
                             properties.get('addr:city', ''),
                             properties.get('addr:country', '')]).strip(', ') or "N/A"
        website = properties.get('website', "N/A")
        phone = properties.get('phone', "N/A")
        email = properties.get('email', "N/A")
        opening_hours = properties.get('opening_hours', "N/A")

        # Check for type Point and retrieving coordinates
        geometry = feature.get('geometry', {})
        if geometry.get('type') == 'Point':
            coordinates = geometry.get('coordinates', [])
            if coordinates:
                # Creating and saving as model instance
                point = Point(coordinates[0], coordinates[1])
                tourist_attraction = TouristAttraction(
                    name=name,
                    tourism=tourism,
                    address=address,
                    website=website,
                    phone=phone,
                    email=email,
                    opening_hours=opening_hours,
                    mpoint=point
                )
                tourist_attraction.save()
                count += 1

    if verbose:
        print(f"Loaded {count} tourist attractions.")
