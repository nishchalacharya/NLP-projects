import numpy as np
import pandas as pd
import time
import requests
import json



API_KEY = '8265bd1679663a7ea12ac168da84d2e8'
# BASE_URL = 'https://api.themoviedb.org/3/discover/movie'



# 1. Get genre id-name mapping
def get_genre_mapping(api_key):
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        return {genre['id']: genre['name'] for genre in genres}
    else:
        raise Exception(f"Failed to get genres: {response.status_code}")
    
    
    
def fetch_movies(api_key, genre_dict, total_pages=10):
    base_url = 'https://api.themoviedb.org/3/discover/movie'
    
    movies = []

    for page in range(1,472):
        params={
            'api_key':API_KEY,
            'language':'en-US',
            'sort_by':'popularity.desc',
            'vote_count.gte':471,
            'page':page
               }

        response=requests.get(base_url,params=params)
        if response.status_code != 200 :
            print (f'Failed to fetch page {page}:{response.status_code}')
            break

        data=response.json()
        for movie in data.get('results',[]):
            genres=[genre_dict.get(gid,'Unknown') for gid in movie.get('genre_ids',[])]
            movies.append({
                'title':movie.get('title'),
                'overview':movie.get('overview'),
                'genres':genres,
                'popularity':movie.get('popularity')
                    })
        print(f'Movies fetched from page {page},total movies collected: {len(movies)}')
        time.sleep(0.3)

    return movies
    


def main():
    print("Fetching genre mapping...")
    genre_dict = get_genre_mapping(API_KEY)

    print("Fetching movie data...")
    movies = fetch_movies(API_KEY, genre_dict, total_pages=461)  # fetch 461 pages 

    print("Creating DataFrame...")
    df = pd.DataFrame(movies)

    # Save to CSV
    df.to_csv("tmdb_custom_dataset.csv", index=False)
    print(f"Dataset saved to 'tmdb_custom_dataset.csv' with shape: {df.shape}")

if __name__ == "__main__":
    main()   
    
    
    
    
#Now lets convert the slang text to dictionary
abbr_dict = {}

with open("slangtext.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()  # remove whitespace or newline
        if line and "=" in line:
            key, value = line.split("=", 1)
            abbr_dict[key.strip()] = value.strip()

print("Total abbreviations loaded:", len(abbr_dict))
print(abbr_dict)


