# spotify-api
What's your top 50 most listened tracks on spotify? 🎵🎧

Reference: 
- [Spotify REST API Documentation](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app)
- [User's top track endpoint](https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks)
- [Get Artist endpoint](https://developer.spotify.com/documentation/web-api/reference/get-an-artist)
- [Get Album endpoint](https://developer.spotify.com/documentation/web-api/reference/get-an-album)

## Purpose
Invoke an API endpoint to get json data of your most listened tracks. Then visualize that in whatever BI tools for some analysis. My initial use case was just listing it out in a table. <i>Why?</i> It's useful for when going for a karaoke marathon where you can just queue up all the songs based on what you have in the list 🎤

## Pre-Requisite
- Turn the `env.txt` to `.env` file.
- Get your virtual env and `pip install` set up by run the following on your Windows(👀) cmd:
    - >`python -m venv .venv`
    - >`.venv\Scripts\activate`
    - >`pip install -r ./env_req.txt`
- Download [chromedriver](https://chromedriver.chromium.org/downloads) - version of your Chrome browser
    - You will need to update the path in the `main.py` to wherever the habitat of the `chromedriver.exe` is 
- Create an app on your account [dashboard](https://developer.spotify.com/dashboard)
    - This is where you will get your client id and client secret

## Steps to Produce the same result in [`data`](<add link to data folder>)

1. Fill in `.env` file with your client id and client secret from Pre-Requisite section.
1. Update `executable_path` to be wherever you downloaded chromedriver from pre-req step.
1. Run the script in `main.py`.
1. You will get prompted to input your username and password for spotify since the data will be from your account.
1. Once the program finishes running, you should get 2 json files: `raw_artists` and `raw_top_tracks`
1. Run the script in `data_cleaning.py` and this will get you `spotify.csv`.
1. Drop the csv file into Tableau template if you wish or connect it to your own BI tool (you might need to do your own data transformation for that BI tool.) OR do whatever you wish!

Note: 
- `splinter` module was working for me in jupyter notebook but not `main.py`, so I switched to using `selenium` module instead since it was a good learning opportunity. Comment out the code according to what module you end up using.
- `api` directory has all the different endpoints that I broke apart from `main.py`.