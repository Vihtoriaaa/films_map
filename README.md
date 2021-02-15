Films_map

films_map is an app for generating a map with locations of films which were
released in the needed year (the one the user inputed). There are 10 nearest
films depending on user's location

Functions and Module

Program consists of 1 module:

main.py - this is main module in which the map is generating and all functions
are based there.

Main.py consists of 6 functions:

- read_data. Function reads a file from path ('locations.list').
Returns list of lists with data of each film(film name, year, location).
- needed_year_base. Function returns a list of lists with films
released in inputed year. The base is the one outputed from read_data function. 
- find_distance. Function returns list of lists, in every each of them there is
an information about a film released in needed year (name, year, location,
(lat, long), distance). distance is the one between a location of every film
and the user. Base is the one outputed from needed_year_base function.
- find_ten_films. Function outputs lists of lists with 10 nearest films to user
The base is the one outputed from find_distance function. 
- create_map. Function creates a map with 10 (or less) film locations, user's
location and a location of Pysanka Museam in Kolomyia. It creates an html file
with different markers of locations.
- main. Function is the main one which calls all function and generates the map.

Example of usage

!!!Program with locations.list works more than 2-3 minutes. to get a map quickly
I recommend to use newlocation.list.!!!

The program will ask you to input some characteristics. 
(example of input in Terminal)
![text](inputask.png?raw=true "text")

The user needs to indicate the year of films released in he/she wants to build
a map of, and his location as latitude and longitude. The output is an
HTML file (map).
(example is a map of year 2009 and lat, long are 49.83826,24.02324)
![text](2009map.png?raw=true "text")

Also there are 3 designs of a map. The one mentioned before is the basic one.
Here is a 'cartodbdark_matter' one:
![text](cartodbdark_matter.png?raw=true "text")

And here is a 'stamentoner' one:
![text](stamentoner.png?raw=true "text")

