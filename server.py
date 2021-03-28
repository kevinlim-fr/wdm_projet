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

    FILTER = "FILTER (("+str(lat)+"-?lat)*("+str(lat)+"-?lat) + ("+str(lon)+"-?lng)*("+str(lon)+"-?lng)* " \
        "("+str(val2)+"-("+str(val1)+"*?lat)) < "+str(radius_degree)+")}"

    requete = "SELECT ?name ?place ?ville ?lat ?lng WHERE { "\
    "?station rdf:type ns:station . "\
    "?station ns:name ?name . "\
    "?station ns:ville ?ville .	"\
    "?station ns:lng ?lng . "\
    "?station ns:lat ?lat . "\
    "?station ns:place ?place . "
    
    sparql_query1 = PREFIX + requete + FILTER
    #print(sparql_query1)
    sparql_query1 = urllib.parse.quote(sparql_query1, safe='')
    url1 = "http://localhost:3030/db/sparql?query="+sparql_query1
    #print(url1)
    response1 = requests.get(url1)
    json1 = response1.json()
    json1 = json1["results"]["bindings"]
    
    requete1 = pd.DataFrame()
    
    for i in range(len(json1)):
        name = json1[i]["name"]["value"] 
        ville = json1[i]["ville"]["value"]
        lat = json1[i]["lat"]["value"]
        lng = json1[i]["lng"]["value"]
        place = json1[i]["place"]["value"]
        list_to_append = [name] + [ville] + [lat] + [lng] + [place]
        line_labels = ["name"] + ["ville"] + ["lat"] + ["lng"] + ["place"]
        dic1 = {line_labels[i]: list_to_append[i] for i in range(len(list_to_append))}
        requete1 = requete1.append(dic1,ignore_index=True)
    
    if len(requete1)>1:
        requete1 = requete1[["name","place","ville","lat","lng"]]
        print(requete1)

    # Lille Hopitaux
    
    requete = "SELECT ?place ?ville ?lng ?lat WHERE { "\
    "?hospital rdf:type ns:hospital . "\
    "?hospital ns:ville ?ville . "\
    "?hospital ns:lng ?lng . "\
    "?hospital ns:lat ?lat . "\
    "?hospital ns:place ?place . "

    sparql_query2 = PREFIX + requete + FILTER
    print(sparql_query2)
    sparql_query2 = urllib.parse.quote(sparql_query2, safe='')
    url2 = "http://localhost:3030/db/sparql?query="+sparql_query2
    response2 = requests.get(url2)
    json2 = response2.json()
    json2 = json2["results"]["bindings"]
    # print(json2)
    requete2 = pd.DataFrame()

    for i in range(len(json2)):
        ville = json2[i]["ville"]["value"]
        lat = json2[i]["lat"]["value"]
        lng = json2[i]["lng"]["value"]
        place = json2[i]["place"]["value"]
        list_to_append = [ville] + [lat] + [lng] + [place]
        line_labels = ["ville"] + ["lat"] + ["lng"] + ["place"]
        dic = {line_labels[i]: list_to_append[i]
               for i in range(len(list_to_append))}
        requete2 = requete2.append(dic, ignore_index=True)

    if len(requete2) > 1:
        requete2 = requete2[["ville","place", "lat", "lng"]]
        print(requete2)


while True:
    adresse = input(
        "Veuillez saisir une adresse complete ex: Place de la Mairie, 35000 Rennes \n").replace(" ", "+")
    lat, lon = getCoordinates(adresse)
    radius_km = int(input("Saisir la portee en km : \n"))
    resultat = requete(adresse, radius_km)
    resultat
