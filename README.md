themoviedb.org wrapper for api v3
---

- Old wrapper renamed to themoviedb_oldapi : https://github.com/doganaydin/themoviedb_oldapi
- Temporarily, only movie search api is implemented -
- Please edit wiki page to add yourself to WhoUses page.

Installation:
---

- pip install requests
- (for py2x) sudo python setup.py install
- (for py3x) sudo python3 setup.py install


Usage:
---

- import tmdb
- tmdb.configure(yourapikey)
- movie = tmdb.Movie("Alien")
- movie.get_id() # or other methods..

For more detailed data..

- movie.full_info(movie_id)
- movie.is_adult() #true false

or..

- movie.is_adult(movie_id)

This methods usable without movie_id:

+ get_total_results(self)
+ get_id(self,movie_index=0)
+ get_backdrop(self,img_size="o",movie_index=0)
+ get_original_title(self,movie_index=0)
+ get_popularity(self,movie_index=0)
+ get_release_date(self,movie_index=0)
+ get_title(self,movie_index=0)
+ get_poster(self,img_size="o",movie_index=0)

With movie_id:

+ is_adult(self,movie_id=0)
+ get_collection_id(self,movie_id=0)
+ get_collection_name(self,movie_id=0)
+ get_collection_backdrop(self,img_size="o",movie_id=0)
+ get_collection_poster(self,img_size="o",movie_id=0)
+ get_budget(self,movie_id=0)
+ get_genres(self,movie_id=0)
+ get_homepage(self,movie_id=0)
+ get_imdb_id(self,movie_id=0)
+ get_overview(self,movie_id=0)
+ get_production_companies(self,movie_id=0)
+ get_productions_countries(self,movie_id=0)
+ get_revenue(self,movie_id=0)
+ get_runtime(self,movie_id=0)
+ get_spoken_languages(self,movie_id=0)
+ get_tagline(self,movie_id=0)
+ get_vote_average(self,movie_id=0)
+ get_vote_count(self,movie_id=0)



(Api v3 is very silly.tmdb.py is a little bit complicated now because of f***ed api developers.)