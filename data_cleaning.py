# Dependencies
import requests
import json
import pandas as pd

##############################
###### raw_top_tracks ########
##############################

# Exporat data to JSON
with open("data/raw_top_tracks.json", "r") as read:
    track_json = json.load(read)


# Map only the datafields I want
def track_func(track):
    artists_name = [artist["name"] for artist in track["artists"]]
    # for getting artist img and url in another file
    artists_id = [artist["id"] for artist in track["artists"]]
    album_name = track["album"]["name"]
    release_date = track["album"]["release_date"]
    title = track["name"]
    popularity = track["popularity"]
    duration_ms = track["duration_ms"]
    song_url = track["external_urls"]["spotify"]
    album_img = track["album"]["images"][1]["url"]
    album_img_phone = track["album"]["images"][2]["url"]
    album_url = track["album"]["external_urls"]["spotify"]
    song_preview_url = track["preview_url"]

    return {
        "title": title,
        "artists_name": str(artists_name)[2:-2],
        "artists_id": str(artists_id)[2:-2],
        "album_name": album_name,
        "album_img": album_img,
        "album_img_phone": album_img_phone,
        "album_url": album_url,
        "release_date": release_date,
        "duration_min": round(duration_ms / 60000, 2),
        "duration_ms": duration_ms,
        "popularity": popularity,
        "song_url": song_url,
        "song_preview_url": song_preview_url,
    }


# Use map to give a list iterator
track_list_iterator = map(track_func, track_json["items"])
# Turn iterator into a list
track_list2 = list(track_list_iterator)

# Convert the array of data into a dataframe
top_tracks_df = pd.DataFrame(track_list2)

# Add rank column here
top_tracks_df = top_tracks_df.sort_values(["popularity"], ascending=False)

# reset index
tracks_df = top_tracks_df.reset_index(drop=True)

# Export to csv
# tracks_df.to_csv('data/top_tracks.csv', encoding='utf-8')

##############################
###### raw_artists ###########
##############################

# Exporat data to JSON
with open("data/raw_artists.json", "r") as read:
    artist_json = json.load(read)


# artist data lister function -- need the img and url + genre
def artist_list(track):
    # for getting artist img and url in another file
    artist_id = track["id"]
    genres = [g for g in track["genres"]]
    artist_popularity = track["popularity"]
    artist_img = track["images"][1]["url"]
    artist_img_phone = track["images"][2]["url"]
    artist_url = track["external_urls"]["spotify"]

    return {
        "artists_id": artist_id,
        "genres": genres,
        "artist_popularity": artist_popularity,
        "artist_img_phone": artist_img_phone,
        "artist_img": artist_img,
        "artist_url": artist_url,
    }


artist_list_iterator = map(artist_list, artist_json)
artist_data = list(artist_list_iterator)

# Turn to df and export to csv
artist_df = pd.DataFrame(artist_data)
# artist_df.to_csv('data/artists.csv', encoding='utf-8')

# Join the tracks and the artist dfs together
track_artist = pd.merge(tracks_df, artist_df, on="artists_id", how="left")

# Create genre df out of artist_df
genres_raw = artist_df[["artists_id", "genres"]]

# Blow up the genre for each artist
genre_df = genres_raw.explode("genres")
# Capitalize first letter
genre_df["genres"] = genre_df["genres"].str.capitalize()

##############################
###### FINAL DATA ###########
##############################

# Merge w top tracks and artist to get one complete data
spotify_df = pd.merge(track_artist, genre_df, on="artists_id", how="left")

# Clean up: del unneeded dup column, rename
spotify_df.drop("genres_x", axis=1)
spotify_df = spotify_df.rename(columns={"genres_y": "genre"})
# Export to csv
spotify_df.to_csv("data/spotify.csv", encoding="utf-8")

print("Data clean-up is complete!")
