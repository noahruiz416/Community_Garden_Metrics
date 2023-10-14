import requests
import json
import pandas as pd

# Replace with your own Google Maps API key
api_key = ''

# List of addresses to geocode
addresses = [
    '4208 N 51st Ave, Phoenix, AZ 85031',
    '212 E 1st Ave, Mesa, AZ 85210',
    '1740 S Roosevelt St, Tempe, AZ 85281',
    '8810 S Avenida del Yaqui, Tempe, AZ 85283',
    '4700 E Warner Rd, Tempe, AZ 85284',
    '1823 E Broadway Rd, Phoenix, AZ 85040',
    '915 E Palm Ln, Phoenix, AZ 85006',
    'S Bonarden Ln, Tempe, AZ 85284',
    '1730 S 2nd St, Phoenix, AZ 85004',
    '1022 E Garfield St, Phoenix, AZ 85006',
    '4308 N 27th St, Phoenix, AZ 85018',
    '9000 E Chaparral Rd, Scottsdale, AZ 85256',
    '4700 E Warner Rd, Phoenix, AZ 85044',
    '3000 E Ray Rd, Gilbert, AZ 85296',
    '2777 S Gilbert Rd, Chandler, AZ 85286',
    '1822 W Pierson St, Phoenix, AZ 85015',
    '3218 N 27th St, Phoenix, AZ 85016',
    '4208 N 51st Ave, Phoenix, AZ 85031',
    '15109 N 102nd Way, Scottsdale, AZ 85255',
    'Fountain Hills, AZ 85268',
    '557-599 N 93rd Ave, Tolleson, AZ 85353',
    'Phoenix, AZ 85007',
    '13500 N El Mirage Rd, El Mirage, AZ 85335',
    '10225 N 83rd Ave, Peoria, AZ 85345',
    '7th Av &, W Cheryl Dr, Phoenix, AZ 85021',
    '1200 W Vineyard Rd, Phoenix, AZ 85041',
    'Mesa, AZ 85212',
    '1200 W Vineyard Rd, Phoenix, AZ 85041',
    '6042 N 68th Dr, Glendale, AZ 85303',
    '3146 E Wier Ave #31, Phoenix, AZ 85040',
]

# Initialize an empty DataFrame
data = pd.DataFrame(columns=['Address', 'City', 'Zip Code', 'Latitude', 'Longitude', 'Rating'])

# Google Maps Geocoding API endpoint
for address in addresses:
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'

    # Send an HTTP GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        geocoding_data = response.json()

        # Check the status in the response
        if geocoding_data['status'] == 'OK':
            # Extract relevant information from the response
            result = geocoding_data['results'][0]
            formatted_address = result['formatted_address']
            location = result['geometry']['location']
            lat = location['lat']
            lng = location['lng']

            # Extract city and zip code
            city = None
            zip_code = None
            for component in result['address_components']:
                if 'locality' in component['types']:
                    city = component['long_name']
                if 'postal_code' in component['types']:
                    zip_code = component['long_name']

            # Retrieve the community garden rating using Place Details
            place_id = 'YOUR_PLACE_ID'  # Replace with the actual Place ID
            place_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}'
            place_response = requests.get(place_url)

            if place_response.status_code == 200:
                place_data = place_response.json()
                rating = place_data.get('result', {}).get('rating')
            else:
                rating = None  # Handle rating retrieval failure

            # Append the data to the DataFrame
            data = data.append({
                'Address': formatted_address,
                'City': city,
                'Zip Code': zip_code,
                'Latitude': lat,
                'Longitude': lng,
                'Rating': rating
            }, ignore_index=True)
        else:
            print(f'Geocoding failed for {address}. Status:', geocoding_data['status'])
    else:
        print(f'Request to Google Maps API failed for {address}. Status code:', response.status_code)

data = data.drop(columns = 'Rating')
