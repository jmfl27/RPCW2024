from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL
from urllib.parse import quote
import pprint
import json

def parseName(name):
    return name.replace("[", "").replace("]", "").replace(" ", "_").replace("\"", "").replace("%", "percent").replace("|", "_").replace("\n", "")

g = Graph()
g.parse('baseCinema.ttl')

cinema = Namespace("http://rpcw.di.uminho.pt/2024/cinema/")

actors = []
countries = []
directors = []
producers = []
writers = []
composers = []
screenwriters = []
genres = []

with open("cinemaFast.json","r") as f:
    movies = json.load(f)

for movie in movies:
    #print(movie['film'])
    movie_uri = URIRef(f"{cinema}{parseName(movie['film'])}")
    g.add((movie_uri, RDF.type, OWL.NamedIndividual))
    g.add((movie_uri, RDF.type, cinema.Film))
    g.add((movie_uri, cinema.title, Literal(movie['film'])))

    if movie['description'] != '':
        g.add((movie_uri, cinema.description, Literal(movie['description'])))
    if movie["releaseDate"]:
        g.add((movie_uri, cinema.date, Literal(movie['releaseDate'])))
    
    for country in movie['movieCountries']:
        country_uri = URIRef(f"{cinema}{parseName(country)}")
        if country_uri not in countries:
            countries.append(country_uri)
            g.add((country_uri, RDF.type, OWL.NamedIndividual))
            g.add((country_uri, RDF.type, cinema.Country))
            g.add((country_uri, cinema.name, Literal(country)))
        g.add((movie_uri, cinema.hasCountry, country_uri))

    for actor in movie['actors']:
        actor_uri = URIRef(f"{cinema}{parseName(actor['name'])}")
        if actor_uri not in actors:
            actors.append(actor_uri)
            g.add((actor_uri, RDF.type, OWL.NamedIndividual))
            g.add((actor_uri, RDF.type, cinema.Actor))
            g.add((actor_uri, cinema.name, Literal(actor['name'])))
            if actor['birthDate'] != '':
                g.add((actor_uri, cinema.birthDate, Literal(actor['birthDate'])))
            if actor['birthCountry'] != '':
                actor_country_uri = URIRef(f"{cinema}{parseName(actor['birthCountry'])}")
                if actor_country_uri not in countries:
                    countries.append(actor_country_uri)
                    g.add((actor_country_uri, RDF.type, OWL.NamedIndividual))
                    g.add((actor_country_uri, RDF.type, cinema.Country))
                    g.add((actor_country_uri, cinema.name, Literal(actor['birthCountry'])))
        g.add((movie_uri, cinema.hasActor, actor_uri))

    for director in movie["directors"]:
        director_uri = URIRef(f"{cinema}{parseName(director)}")
        if director_uri not in directors:
            directors.append(director_uri)
            g.add((director_uri, RDF.type, OWL.NamedIndividual))
            g.add((director_uri, RDF.type, cinema.Director))
            g.add((director_uri, cinema.name, Literal(director)))
        g.add((movie_uri, cinema.hasDirector, director_uri))
    
    for producer in movie["producers"]:
        producer_uri = URIRef(f"{cinema}{parseName(producer)}")
        if producer_uri not in producers:
            producers.append(producer_uri)
            g.add((producer_uri, RDF.type, OWL.NamedIndividual))
            g.add((producer_uri, RDF.type, cinema.Producer))
            g.add((producer_uri, cinema.name, Literal(producer)))
        g.add((movie_uri, cinema.hasProducer, producer_uri))
    
    for writer in movie["writers"]:
        writer_uri = URIRef(f"{cinema}{parseName(writer)}")
        if writer_uri not in writers:
            writers.append(writer_uri)
            g.add((writer_uri, RDF.type, OWL.NamedIndividual))
            g.add((writer_uri, RDF.type, cinema.Writer))
            g.add((writer_uri, cinema.name, Literal(writer)))
        g.add((movie_uri, cinema.hasWriter, writer_uri))

    for composer in movie["composers"]:
        composer_uri = URIRef(f"{cinema}{parseName(composer)}")
        if composer_uri not in composers:
            composers.append(composer_uri)
            g.add((composer_uri, RDF.type, OWL.NamedIndividual))
            g.add((composer_uri, RDF.type, cinema.Composer))
            g.add((composer_uri, cinema.name, Literal(composer)))
        g.add((movie_uri, cinema.hasComposer, composer_uri))
    
    for screenwriter in movie["screenwriters"]:
        screenwriter_uri = URIRef(f"{cinema}{parseName(screenwriter)}")
        if screenwriter_uri not in screenwriters:
            screenwriters.append(screenwriter_uri)
            g.add((screenwriter_uri, RDF.type, OWL.NamedIndividual))
            g.add((screenwriter_uri, RDF.type, cinema.Screenwriter))
            g.add((screenwriter_uri, cinema.name, Literal(screenwriter)))
        g.add((movie_uri, cinema.hasScreenwriter, screenwriter_uri))
    
    if movie['duration'] != -1:
        g.add((movie_uri, cinema.duration, Literal(movie['duration'])))
    
    for genre in movie["genres"]:
        genre_uri = URIRef(f"{cinema}{parseName(genre)}")
        if genre_uri not in genres:
            genres.append(genre_uri)
            g.add((genre_uri, RDF.type, OWL.NamedIndividual))
            g.add((genre_uri, RDF.type, cinema.Genre))
            g.add((genre_uri, cinema.name, Literal(genre)))
        g.add((movie_uri, cinema.hasGenre, genre_uri))

    #print(len(g))
    print(g.serialize())

    #print("==============================================")

#for stmt in g:
#    pprint.pprint(stmt)