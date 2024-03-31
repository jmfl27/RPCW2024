import requests
import json

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

# Define the SPARQL query
sparql_query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?filme ?filmName ?description ?releaseDate ?movieCountry ?actorName ?birthDate ?birthCountry ?directorName ?producerName ?writerName ?musicName ?screenName ?duration ?genreName
WHERE {
    ?filme a dbo:Film;
              rdfs:label ?filmName.
  OPTIONAL {
       ?filme dbo:abstract ?description.
       FILTER (LANG(?description) = 'en')
  }
   OPTIONAL {
         ?filme dbo:starring ?actor.
          ?actor rdfs:label ?actorName.
          OPTIONAL {
            ?actor dbo:birthDate ?birthDate.
          }
          OPTIONAL {
            ?actor dbo:birthPlace ?birthPlace.
            ?birthPlace a dbo:Country.
            BIND(REPLACE(STR(?birthPlace), "http://dbpedia.org/resource/", "") AS ?birthCountry)
          }
          FILTER (LANG(?actorName) = 'en')
   }
Optional {
             ?filme dbo:releaseDate ?releaseDate.
   }
Optional {
             ?filme dbo:country ?country.
              ?country rdfs:label ?movieCountry.
              FILTER (LANG(?movieCountry) = 'en')
   }
Optional {
             ?filme dbo:director ?director.
              ?director rdfs:label ?directorName.
              FILTER (LANG(?directorName) = 'en')
   }
Optional {
             ?filme dbo:producer ?producer.
              ?producer rdfs:label ?producerName.
              FILTER (LANG(?producerName) = 'en')
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
Optional {
             ?filme dbo:genre ?genre.
              ?genre rdfs:label ?genreName.
              FILTER (LANG(?genreName) = 'en')
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
        description = result.get("description", {}).get("value", None)
        releaseDate = result.get("releaseDate", {}).get("value", None)
        movieCountry = result.get("movieCountry", {}).get("value", None)
        actor = result.get("actorName", {}).get("value", None)
        birthDate = result.get("birthDate", {}).get("value", None)
        birthCountry = result.get("birthCountry", {}).get("value", None)
        director = result.get("directorName", {}).get("value", None)
        producer = result.get("producerName", {}).get("value", None)
        writer = result.get("writerName", {}).get("value", None)
        music = result.get("musicName", {}).get("value", None)
        screenwriter = result.get("screenName", {}).get("value", None)
        duration = result.get("duration", {}).get("value", None)
        genre = result.get("genreName", {}).get("value", None)

        if film_uri in cinema:
            if description and description not in cinema[film_uri]["description"]:
                cinema[film_uri]["description"] = description
            if releaseDate and releaseDate not in cinema[film_uri]["releaseDate"]:
                cinema[film_uri]["releaseDate"] = releaseDate
            if movieCountry and movieCountry not in cinema[film_uri]["movieCountries"]:
                cinema[film_uri]["movieCountries"].append(movieCountry)   
            if actor and actor not in list(map(lambda x: x["name"], cinema[film_uri]["actors"])):
                cinema[film_uri]["actors"].append(
                    {'name': actor,
                      "birthDate": birthDate if birthDate else "",
                      "birthCountry": birthCountry if birthCountry else ""
                    }
                )
            if director and director not in cinema[film_uri]["directors"]:
                cinema[film_uri]["directors"].append(director)
            if producer and producer not in cinema[film_uri]["producers"]:
                cinema[film_uri]["producers"].append(producer)
            if writer and writer not in cinema[film_uri]["writers"]:
                cinema[film_uri]["writers"].append(writer)
            if music and music not in cinema[film_uri]["composers"]:
                cinema[film_uri]["composers"].append(music)
            if screenwriter and screenwriter not in cinema[film_uri]["screenwriters"]:
                cinema[film_uri]["screenwriters"].append(screenwriter)
            if duration and cinema[film_uri]["duration"] != float(duration):
                #cinema[film_uri]["duration"] = float(duration)/60
                cinema[film_uri]["duration"] = float(duration)
            if genre and genre not in cinema[film_uri]["genres"]:
                cinema[film_uri]["genres"].append(genre)
        else:
            cinema[film_uri] = {
                "uri" : film_uri,
                "film" : film,
                "description" : description,
                "releaseDate" : releaseDate,
                "movieCountries" : [movieCountry] if movieCountry else [],
                "actors" : [{'name': actor, "birthDate": birthDate if birthDate else "", "birthCountry": birthCountry if birthCountry else ""}] if actor else [],
                "directors" : [director] if director else [],
                "producers" : [producer] if producer else [],
                "writers" : [writer] if writer else [],
                "composers" : [music] if music else [],
                "screenwriters" : [screenwriter] if screenwriter else [],
                #"duration" : [float(duration)/60] if duration else -1,
                "duration" : [float(duration)] if duration else -1,
                "genres" : [genre] if genre else []
            }

    cinemaList = list(cinema.values())
    # Write to JSON file
    with open("cinemaFast.json", "w") as f:
        json.dump(cinemaList, f)

else:
    print("Error:", response.status_code)
    print(response.text)