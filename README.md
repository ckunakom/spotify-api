# spotify-usage
What's your top 50 most listened tracks on spotify? 🎵🎧

Reference: [Spotify REST API Documentation](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app)

## Purpose
Invoke an API endpoint to get json data of your most listened tracks. Then visualize that in whatever BI tools for some analysis. My initial use case was just listing it out in a table. <i>Why?</i> It's useful for when going for a karaoke marathon where you can just queue up all the songs based on what you have in the list 🎤

### Pre-Requisite
- Get your virtual env and `pip install` set up by run the following on your Windows(👀) cmd:
    - >`python -m venv .env`
    - >`.env/Scripts/activate`
    - >`pip install -r ./env_req.txt`
- Download [chromedriver](https://chromedriver.chromium.org/downloads) - version of your Chrome browser
    - You will need to update the path in the `main.py` to wherever the habitat of the `chromedriver.exe` is 
- Create an app on your account [dashboard](https://developer.spotify.com/dashboard)
    - This is where you will get your client id and client secret

### Steps  -- still need to finish writing
Note: `splinter` module was working for me the other day and it decides to not work, so I switched to using `selenium` module instead. Comment out the code according to what module you end up using.
    
https://developer.spotify.com/documentation/general/guides/authorization-guide/#list-of-scopes

User's top track endpoint: https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks