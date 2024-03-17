import requests
import json

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

# Define the SPARQL query
sparql_query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?filme ?filmName ?actorName ?directorName ?writerName ?musicName ?screenName ?duration
WHERE {
    ?filme a dbo:Film;
              rdfs:label ?filmName.
   Optional {
             ?filme dbo:starring ?actor.
              ?actor rdfs:label ?actorName.
              FILTER (LANG(?actorName) = 'en')
   }
   Optional {
             ?filme dbo:director ?director.
              ?director rdfs:label ?directorName.
              FILTER (LANG(?directorName) = 'en')
   }
   Optional {
             ?filme dbo:writer ?writer.
              ?writer rdfs:label ?writerName.
              FILTER (LANG(?writerName) = 'en')
   }
   Optional {
             ?filme dbo:musicComposer ?music.
              ?music rdfs:label ?musicName.
              FILTER (LANG(?musicName) = 'en')
   }
   Optional {
             ?filme dbp:screenplay ?screen.
              ?screen rdfs:label ?screenName.
              FILTER (LANG(?screenName) = 'en')
   }
  Optional {
             ?filme dbo:runtime ?duration.
   }
  FILTER (LANG(?filmName) = 'en')
}
"""

# Define the headers
headers = {
    "Accept": "application/sparql-results+json"
}

# Define the parameters
params = {
    "query": sparql_query,
    "format": "json"
}

# Send the SPARQL query using requests
response = requests.get(sparql_endpoint, params=params, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    results = response.json()
    # Print the results
    cinema = {}
    for result in results["results"]["bindings"]:
        film_uri = result["filme"]["value"]
        film = result["filmName"]["value"]

        # Check if the key exists before accessing its value
        actor = result.get("actorName", {}).get("value", None)
        director = result.get("directorName", {}).get("value", None)
        writer = result.get("writerName", {}).get("value", None)
        music = result.get("musicName", {}).get("value", None)
        screenwriter = result.get("screenName", {}).get("value", None)
        duration = result.get("duration", {}).get("value", None)

        if film_uri in cinema:
            if actor and actor not in cinema[film_uri]["actors"]:
                cinema[film_uri]["actors"].append(actor)
            if director and director not in cinema[film_uri]["directors"]:
                cinema[film_uri]["directors"].append(director)
            if writer and writer not in cinema[film_uri]["writers"]:
                cinema[film_uri]["writers"].append(writer)
            if music and music not in cinema[film_uri]["musicians"]:
                cinema[film_uri]["musicians"].append(music)
            if screenwriter and screenwriter not in cinema[film_uri]["screenwriters"]:
                cinema[film_uri]["screenwriters"].append(screenwriter)
            if duration and cinema[film_uri]["duration"] != float(duration):
                cinema[film_uri]["duration"] = float(duration)/60
        else:
            cinema[film_uri] = {
                "uri" : film_uri,
                "film" : film,
                "actors" : [actor] if actor else [],
                "directors" : [director] if director else [],
                "writers" : [writer] if writer else [],
                "musicians" : [music] if music else [],
                "screenwriters" : [screenwriter] if screenwriter else [],
                "duration" : [float(duration)/60] if duration else -1
            }

    cinemaList = list(cinema.values())
    # Write to JSON file
    with open("cinema.json", "w") as f:
        json.dump(cinemaList, f)

else:
    print("Error:", response.status_code)
    print(response.text)