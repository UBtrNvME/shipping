import gmaps

values = {
    'static_map_key': "AIzaSyBw8yje65xRnvNt36p72Xl1keaDptSy0QA",
    'url'           : "https://maps.googleapis.com/maps/api/staticmap"
    }
gmaps.configure(api_key=values['static_map_key'])
def get_map_image(lat, lng):
    result = gmaps.figure(center=(lat,lng), zoom_level=15)
    return result