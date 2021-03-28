# Web Data Mining project

## Authors: Jihane OUL ALI | Clément MUFFAT-JOLY | Kevin LIM

## STEP 0 : Setup

### Database installation Apache Jena Fuseki

#### Run the fuseki server

Click on manage datasets > add one > put db in dataset name and click on Persistent TDB2 > Validate with create dataset

Now upload the data by doing the following:

Click on "upload data" > Click on "select files" > Then navigate to the "fichierXML" folder.

Select all the XML files click "open" and then "upload all"

### Verify if it's possible to query the database
The dataset is now uploaded, to check if it's working you can try the following sparql query:

PREFIX ns: <http://www.semanticweb.org/joula/ontologies/2021/2/projetWeb/> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX rdfs:<http://www.w3.org/2001/XMLSchema#> 
PREFIX http: <http://www.w3.org/2011/http#>

SELECT ?place ?ville ?lng ?lat
WHERE {
	?hospital rdf:type ns:hospital .
  	?hospital ns:ville ?ville .	
  	?hospital ns:lng ?lng .
  	?hospital ns:lat ?lat .
  	?hospital ns:place ?place .
}

### Python installation for the server

Install if necessary through command line 



#### Windows

python -m pip3 install requests

python -m pip3 install pandas

python -m pip3 install urllib 

#### macOS

pip3 install requests

pip3 install pandas 

pip3 install urllib

## STEP 1 : Run the Jena Fuseki server

## STEP 2 : Run the Python App

### Démarrage de l'app

macOS: 
python3 "chemin vers le fichier" (glisser le fichier dans le Terminal)

Windows
pytohn3 -m "chemin vers le fichier"


### Fonctionnalité : Saisir une adresse et une portée et découvrir les lieux autour 
Saisir l'adresse que vous souhaitez à Lille, Lyon ou Rennes

Par exemple: 

Mairie de Lille (Hopitaux) : Place Augustin Laurent, 59033 Lille

Mairie de Lyon (Vélos) : 2 Place Sathonay, 69001 Lyon

Mairie de Rennes (Vélos) : Place de la Mairie, 35000 Rennes

Mairie de Montpellier : 1 Place Georges Frêche, 34000 Montpellier

### ATTENTION : SI VOUS AVEZ UNE ERREUR 

Il faut faire une manipulation avec la librairie JSON. Veuillez vous rendre sur le repo github afin d'avoir le dernier readme avec les manipulations à réaliser.
https://github.com/kevinlim-fr/wdm_proje

### Une video de démonstration est disponible dans à la racine du repo
