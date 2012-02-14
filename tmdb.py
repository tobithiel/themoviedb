#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author:doganaydin
#project:themoviedb
#repository:http://github.com/doganaydin/themoviedb
#license: LGPLv3 http://www.gnu.org/licenses/lgpl.html

"""An interface to the themoviedb.org API"""

__author__ = "doganaydin"
__version__ = "0.1"

try:
    import simplejson
except:
    import json as simplejson

import requests

config = {}

def configure(api_key):
    config['apikey'] = api_key
    config['urls'] = {}
    config['urls']['movie.search'] = "http://api.themoviedb.org/3/search/movie?query=%%s&api_key=%(apikey)s&page=%%s" % (config)
    config['urls']['movie.info'] = "http://api.themoviedb.org/3/movie/%%s?api_key=%(apikey)s" % (config)
    config['urls']['people.search'] = "http://api.themoviedb.org/3/search/person?query=%%s&api_key=%(apikey)s" % (config)
    config['urls']['collection.info'] = "http://api.themoviedb.org/3/collection/%%s&api_key=%(apikey)s" % (config)
    config['urls']['movie.alternativetitles'] = "http://api.themoviedb.org/3/movie/%%s/alternative_titles?api_key=%(apikey)s" % (config)
    config['urls']['movie.casts'] = "http://api.themoviedb.org/3/movie/%%s/casts?api_key=%(apikey)s" % (config)
    config['urls']['movie.images'] = "http://api.themoviedb.org/3/movie/%%s/images?api_key=%(apikey)s" % (config)
    config['urls']['movie.keywords'] = "http://api.themoviedb.org/3/movie/%%s/keywords?api_key=%(apikey)s" % (config)
    config['urls']['movie.releases'] = "http://api.themoviedb.org/3/movie/%%s/releases?api_key=%(apikey)s" % (config)
    config['urls']['movie.trailers'] = "http://api.themoviedb.org/3/movie/%%s/trailers?api_key=%(apikey)s" % (config)
    config['urls']['movie.translations'] = "http://api.themoviedb.org/3/movie/%%s/translations?api_key=%(apikey)s" % (config)
    config['urls']['person.info'] = "http://api.themoviedb.org/3/person/%%s&api_key=%(apikey)s" % (config)
    config['urls']['person.credits'] = "http://api.themoviedb.org/3/person/%%s/credits&api_key=%(apikey)s" % (config)
    config['urls']['person.images'] = "http://api.themoviedb.org/3/person/%%s/images&api_key=%(apikey)s" % (config)
    config['urls']['latestmovie'] = "http://api.themoviedb.org/3/latest/movie?api_key=%(apikey)s" % (config)
    config['urls']['config'] = "http://api.themoviedb.org/3/configuration?api_key=%(apikey)s" % (config)

    config['api'] = {}
    config['api']['backdrop.sizes'] = ""
    config['api']['base.url'] = ""
    config['api']['poster.sizes'] = ""
    config['api']['profile.sizes'] = ""

class Core(object):
    def getJSON(self,url):
        url = url.replace(" ","+")
        page = requests.get(url).content
        try:
            return simplejson.loads(page)
        except:
            return simplejson.loads(page.decode('utf-8'))

    def update_configuration(self):
        c = self.getJSON(config['urls']['config'])
        config['api']['backdrop.sizes'] = c['images']['backdrop_sizes']
        config['api']['base.url'] = c['images']['base_url']
        config['api']['poster.sizes'] = c['images']['poster_sizes']
        config['api']['profile.sizes'] = c['images']['profile_sizes']
        return "ok"

    def backdrop_sizes(self,img_size):
        size_list = {'s':'w300','m':'w780','l':'w1280','o':'original'}
        return size_list[img_size]

    def poster_sizes(self,img_size):
        size_list = {'s':'w92','m':'185','l':'w500','o':'original'}
        return size_list[img_size]

class Movie(Core):
    def __init__(self, title="", id=-1):
        self.id = id
        self.update_configuration()
        self.movies = self.getJSON(config['urls']['movie.search'] % (title,str(1)))
        self.movies_full = ""
        pages = self.movies["total_pages"]
        for i in range(int(pages)):
            self.movies["results"].extend(self.getJSON(config['urls']['movie.search'] % (title,str(i)))["results"]) 
        if self.id > -1:
            self.movies_full = self.getJSON(config['urls']['movie.info'] % self.id)

    def full_info(self,movie_id):
        self.movies_full = self.getJSON(config['urls']['movie.info'] % str(movie_id))

    def get_total_results(self):
        return self.movies["total_results"]   

    def get_id(self,movie_index=0):
        return self.movies["results"][movie_index]["id"]

    # Sizes = s->w300 m->w780 l->w1280 o->original(default)
    def get_backdrop(self,img_size="o",movie_index=0):
        img_path = self.movies["results"][movie_index]["backdrop_path"]
        return config['api']['base.url']+self.backdrop_size(img_size)+img_path

    def get_original_title(self,movie_index=0):
        return self.movies["results"][movie_index]["original_title"]

    def get_popularity(self,movie_index=0):
        return self.movies["results"][movie_index]["popularity"]

    def get_release_date(self,movie_index=0):
        return self.movies["results"][movie_index]["release_date"]

    def get_title(self,movie_index=0):
        return self.movies["results"][movie_index]["title"]

    # Sizes = s->w92 m->w185 l->w500 o->original(default)
    def get_poster(self,img_size="o",movie_index=0):
        img_path = self.movies["results"][movie_index]["poster_path"]
        return config['api']['base.url']+self.poster_sizes(img_size)+img_path

    def is_adult(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['adult']

    def get_collection_id(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['belongs_to_collection']["id"]

    def get_collection_name(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['belongs_to_collection']["name"]

    # Sizes = s->w300 m->w780 l->w1280 o->original(default)
    def get_collection_backdrop(self,img_size="o",movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        img_path = self.movies_full["belongs_to_collection"]["backdrop_path"]
        return config['api']['base.url']+self.poster_sizes(img_size)+img_path

    # Sizes = s->w92 m->w185 l->w500 o->original(default)    
    def get_collection_poster(self,img_size="o",movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        img_path = self.movies_full["belongs_to_collection"]["poster_path"]
        return config['api']['base.url']+self.poster_sizes(img_size)+img_path

    def get_budget(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['budget']

    def get_genres(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        for i in self.movies_full['genres']:
            genres = {"id":i["id"],"name":i["name"]}
        return genres

    def get_homepage(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['homepage']

    def get_imdb_id(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['imdb_id']

    def get_overview(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['overview']

    def get_production_companies(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        for i in self.movies_full['production_companies']:
            companies = {"id":i["id"],"name":i["name"]}
        return companies

    def get_productions_countries(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        for i in self.movies_full['production_countries']:
            countries = {"iso_3166":i["iso_3166"],"name":i["name"]}
        return countries

    def get_revenue(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['revenue']

    def get_runtime(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['runtime']

    def get_spoken_languages(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        for i in self.movies_full['spoken_languages']:
            langs = {"iso_639_1":i["iso_639_1"],"name":i["name"]}
        return langs

    def get_tagline(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['tagline']

    def get_vote_average(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['vote_average']

    def get_vote_count(self,movie_id=0):
        if movie_id > 0:
            self.full_info(movie_id)
        return self.movies_full['vote_count']