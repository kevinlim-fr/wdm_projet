import requests
import math
import pandas as pd
import urllib


def getCoordinates(adresse):
    adresse = adresse.replace(" ", "+")
    requete = "https://api-adresse.data.gouv.fr/search/?q="+adresse
    response = requests.get(requete)
    json = response.json()
    lat = json["features"][0]["geometry"]["coordinates"][1]
    lon = json["features"][0]["geometry"]["coordinates"][0]
    return lat, lon


def convRadiusKM(radius_km):
    return math.pow(radius_km/111.1949, 2)


def requete(adresse, radius):
    lat, lon = getCoordinates(adresse)
    radius_degree = convRadiusKM(radius_km)
    phi = round(lat)
    val1 = math.cos(phi)*math.sin(phi) * math.pi/180
    val2 = math.cos(phi)*(math.cos(phi) - math.sin(phi)
                          * math.pi/180 * (lat-2*phi))

    # Lyon Velos
    PREFIX = "PREFIX ns: <http://www.semanticweb.org/joula/ontologies/2021/2/projetWeb/> "\
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "\
    "PREFIX rdfs:<http://www.w3.org/2001/XMLSchema#> "\
    "PREFIX http: <http://www.w3.org/2011/http#>"\

    FILTER = "FILTER (("+str(lat)+"-?lat)*("+str(lat)+"-?lat) + ("+str(lon)+"-?long)*("+str(lon)+"-?long)* " \
        "("+str(val2)+"-("+str(val1)+"*?lat)) < "+str(radius_degree)+")}"

    requete = "SELECT ?name ?place ?ville ?lat ?lng WHERE { "\
    "?station rdf:type ns:station . "\
    "?station ns:name ?name . "\ 
    "?station ns:ville ?ville .	"\
    "?station ns:lng ?lng . "\
    "?station ns:lat ?lat . "\
    "?station ns:place ?place . "
    
    sparql_query1 = PREFIX + requete + FILTER
    # print(sparql_query1)
    sparql_query1 = urllib.parse.quote(sparql_query1, safe='')
    url1 = "http://localhost:3030/db/sparql?query="+sparql_query1
    # print(url1)
    response1 = requests.get(url1)
    json1 = response1.json()
    json1 = json1["results"]["bindings"]

    requete1 = pd.DataFrame()

    for i in range(len(json1)):
        name = json1[i]["name"]["value"]
        ville = json1[i]["ville"]["value"]
        lat = json1[i]["lat"]["value"]
        lon = json1[i]["long"]["value"]
        place = json1[i]["place"]["value"]
        list_to_append = [name] + [ville] + [lat] + [lon] + [place]
        line_labels = ["name"] + ["ville"] + ["lat"] + ["lon"] + ["place"]
        dic1 = {line_labels[i]: list_to_append[i]
                for i in range(len(list_to_append))}
        requete1 = requete1.append(dic1, ignore_index=True)

    if len(requete1) > 1:
        requete1 = requete1[["name", "place", "ville", "lat", "lon"]]
        print(requete1)

    # Lille Hopitaux
    PREFIX = "PREFIX ns: <http://schema.org/> " \
        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "\
        "PREFIX rdfs:<http://www.w3.org/2001/XMLSchema#> "\
        "PREFIX owl: <http://www.owl-ontologies.com/unnamed.owl#> "

    requete = "SELECT ?commune ?place ?ville ?lat ?long " \
        "WHERE { ?hospital rdf:type ns:hospital . "\
        "?hospital ns:commune ?commune . "\
        "?hospital ns:ville ?ville . "\
        "?hospital ns:long ?long . "\
        "?hospital ns:lat ?lat . "\
        "?hospital ns:place ?place ."

    sparql_query2 = PREFIX + requete + FILTER
    # print(sparql_query2)
    sparql_query2 = urllib.parse.quote(sparql_query2, safe='')
    url2 = "http://localhost:3030/db/sparql?query="+sparql_query2
    response2 = requests.get(url2)
    json2 = response2.json()
    json2 = json2["results"]["bindings"]
    # print(json2)
    requete2 = pd.DataFrame()

    for i in range(len(json2)):
        name = json2[i]["commune"]["value"]
        ville = json2[i]["ville"]["value"]
        lat = json2[i]["lat"]["value"]
        lon = json2[i]["long"]["value"]
        place = json2[i]["place"]["value"]
        list_to_append = [name] + [ville] + [lat] + [lon] + [place]
        line_labels = ["name"] + ["ville"] + ["lat"] + ["lon"] + ["place"]
        dic = {line_labels[i]: list_to_append[i]
               for i in range(len(list_to_append))}
        requete2 = requete2.append(dic, ignore_index=True)

    if len(requete2) > 1:
        requete2 = requete2[["name", "place", "ville", "lat", "lon"]]
        print(requete2)

    # Rennes Velos
    PREFIX = "PREFIX ns: <http://schema.org/> "\
        + "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "\
        + "PREFIX rdfs:<http://www.w3.org/2001/XMLSchema#> "\
        + "PREFIX owl: <http://www.owl-ontologies.com/unnamed.owl#> "

    requete = "SELECT ?nom ?place ?ville ?lat ?long "\
        "WHERE { ?station rdf:type ns:station . ?station ns:nom ?nom ."\
        " ?station ns:ville ?ville . ?station ns:long ?long ."\
        " ?station ns:lat ?lat ." \
        " ?station ns:place ?place .  "

    sparql_query3 = PREFIX + requete + FILTER
    print(sparql_query3)
    sparql_query3 = urllib.parse.quote(sparql_query3, safe='')
    url3 = "http://localhost:3030/db/sparql?query="+sparql_query3
    response3 = requests.get(url3)
    json3 = response3.json()
    json3 = json3["results"]["bindings"]

    requete3 = pd.DataFrame()

    for i in range(len(json3)):
        name = json3[i]["nom"]["value"]
        ville = json3[i]["ville"]["value"]
        lat = json3[i]["lat"]["value"]
        lon = json3[i]["long"]["value"]
        place = json3[i]["place"]["value"]
        list_to_append = [name] + [ville] + [lat] + [lon] + [place]
        line_labels = ["name"] + ["ville"] + ["lat"] + ["lon"] + ["place"]
        dic3 = {line_labels[i]: list_to_append[i]
                for i in range(len(list_to_append))}
        requete3 = requete3.append(dic3, ignore_index=True)

    if len(requete3) > 1:
        requete3 = requete3[["name", "place", "ville", "lat", "lon"]]
        print(requete3)


while True:
    adresse = input(
        "Veuillez saisir une adresse complete ex: 10 rue de Paris Paris 75001 \n").replace(" ", "+")
    lat, lon = getCoordinates(adresse)
    radius_km = int(input("Saisir la portee en km : \n"))
    resultat = requete(adresse, radius_km)
    resultat
