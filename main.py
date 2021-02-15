"""
Films Map app!!!
"""
import csv
import folium
import geopy.distance
from geopy.distance import geodesic
from geopy.exc import GeocoderUnavailable
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="vihtoriaaa")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
file_path = 'newlocations.list'
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geolocator = Nominatim(user_agent="vihtoriaaa", scheme='http')


def read_data(file_path):
    """
    str -> list
    this function reads the information from the csv file and returns the
    it as DataFrame. if path is not str the function returns None
    >>> read_data([])

    """
    if not isinstance(file_path, str):
        return None
    with open(file_path, "r", encoding="utf-8", errors='ignore') as file:
        content = []
        for line in file:
            if 'Federal' not in line and 'Highway' not in line:
                line = line.strip().split('\t')
                line = list(filter(lambda elem: elem != '', line))
                content.append(line)
    new_base = []
    for one_object in content:
        film = one_object[0].split('(')[0][1:-2].strip()
        year = one_object[0].split('(')[1][:4]
        place = one_object[-1]
        if year.isdigit():
            year = int(year)
            one_object = [film, year, place]
            if one_object not in new_base:
                new_base.append(one_object)
    return new_base


def needed_year_base(year):
    """
    int -> list
    This function returns a list of lists with films of inputed year
    If year type is not integer, the function returns None
    >>> needed_year_base('abalasdf')

    """
    if not isinstance(year, int):
        return None
    base = read_data(file_path)
    film_list = []
    for film_info in base:
        if int(film_info[1]) == year:
            film_list.append(film_info)
    return film_list


def find_distance(year, user_lar, user_long):
    """
    float, float -> list
    This function returns list of lists, in every each of them there is
    an information about a film (name, year, location, (lat, long), distance)
    distance is between a location of a film and the user
    if user_lar or iser_long type is not float, the function returns None
    >>> find_distance([a], '2344')

    """
    if not isinstance(user_lar, float):
        return None
    if not isinstance(user_long, float):
        return None
    user_coordinates = (user_lar, user_long)
    base = needed_year_base(year)
    for one_object in base:
        try:
            location = geolocator.geocode(one_object[2])
            film_loc = (location.latitude, location.longitude)
            one_object.append(film_loc)
            distance = geopy.distance.geodesic(user_coordinates, film_loc).km
            one_object.append(distance)
        except AttributeError:
            pass
        except GeocoderUnavailable:
            pass
        except GeocoderTimedOut:
            pass
    return base


def find_ten_films(base, user_lar, user_long, year):
    """
    list, float, float, int -> list
    This function outputs lists of lists with 10 nearest films to user
    if base type is not list, user_lar, user_long type is not float or
    year type is not int, the function returns None
    >>> find_ten_films([], 'aaa', [123], 2002)

    """
    base = find_distance(year, user_lar, user_long)
    ten_films = list(filter(lambda lst: len(lst) == 5, base))
    sort_films = sorted(ten_films, key=lambda obj: obj[-1])
    final_list = sort_films[:10]
    return final_list


def build_map(base, user_lar, user_long, year):
    """
    list, float, float, int -> htmp map
    This Function builds a map of needed year films around the user
    if base type is not list, user_lar and user_log type is not float
    and year type is not int, the function returns None
    >>> build_map('aaa', 123, [], '2015')

    """
    user_coord = [user_lar, user_long]
    film_base = find_ten_films(base, user_lar, user_long, year)
    map = folium.Map(location=user_coord, zoom_start=10)
    folium.TileLayer('cartodbdark_matter').add_to(map)
    folium.TileLayer('stamentoner').add_to(map)
    fg_user = folium.FeatureGroup(name="Your Location")
    # add location layer
    fg_user.add_child(folium.Marker(location=user_coord,
                                popup='Your Location',
                                icon=folium.Icon(color='pink', icon='user')))
    # add films layer
    fg_films = folium.FeatureGroup(name='Film Names')
    for film in film_base:
        film_name = film[0]
        film_cord = list(film[3])
        distance = film[-1]
        if float(distance) <= 500:
            color_film = 'darkgreen'
        if float(distance) <= 1000 and float(distance) > 500:
            color_film = 'red'
        if float(distance) <= 2000 and float(distance) > 1000:
            color_film = 'cadetblue'
        if float(distance) <= 3000 and float(distance) > 2000:
            color_film = 'lightred'
        if float(distance) <= 5000 and float(distance) > 3000:
            color_film = 'darkpurple'
        if float(distance) > 5000:
            color_film = 'darkred'
        fg_films.add_child(folium.Marker(location=film_cord,
                            popup=film_name,
                            icon=folium.Icon(color=color_film, icon='star')))
    # add Kolomiya Pisanka layer
    pisanka = [48.5285448649131, 25.0391746576719]
    fg_hometowm = folium.FeatureGroup(name='Kolomyiska Pisanka')
    fg_hometowm.add_child(folium.Marker(location=pisanka,
                                popup='Kolomyiska Pisanka',
                                icon=folium.Icon(color='beige', icon='heart')))
    map.add_child(fg_user)
    map.add_child(fg_films)
    map.add_child(fg_hometowm)
    map.add_child(folium.LayerControl())
    map.save('Map.html')
    return map


def main():
    """
    The main function to build a map
    """
    year = int(input("Please enter a year you would like to have a map for: "))
    user_lar, user_long = [float(x) for x in input(
    "Please enter your location (format: lat, long): ").split(',')]
    print('Map is generating, please wait...')
    file_path = 'newlocations.list'
    base = read_data(file_path)
    base = needed_year_base(year)
    find_distance(year, user_lar, user_long)
    base = find_distance(year, user_lar, user_long)
    base = find_ten_films(base, user_lar, user_long, year)
    print(build_map(base, user_lar, user_long, year))
    return 'Map is finished. Please look at: '


if __name__ == "__main__":
    main()
