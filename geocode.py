from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent='iss')


def get_coordinates(address):
	data = geolocator.geocode(address).raw
	latitude = data['lat']
	longitude = data['lon']

	return latitude, longitude


def get_location(lat, lon):
	return geolocator.reverse(f'{lat}, {lon}')
