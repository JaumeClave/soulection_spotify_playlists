# soulection_spotify_playlists
Repo containing code and files used to build a tool that creates a Spotify playlist from
available  Spotify songs played on a Soulection radio show
soulection_to_spotify

The main Python file for this project is called soulection_to_spotify.py found in the src folder.

## Running soulection_to_spotify.py From Your Terminal
You can run soulection_to_spotify.py from the terminal by providing the websites for which the scraper
should check by using the --shows argument. The format passed must be "460" (without
the quotations). For instance:

python soulection_to_spotify.py --shows 460

A dictionary will be returned containing the URL of the scraped website and a boolean (True/False
)  value for its Google Analytics, Chartbeat and Facebook Pixel JavaScript request.

{'URL': 'www.echobox.com', 'Google Analytics': True, 'Chartbeat': False, 'Facebook Pixel': True}

From this result one could infer that the www.echobox.com website has a Google Analytics tracking
code, a Facebook Pixel tracking code and no Chartbeat tracking code.

From the terminal, it is also possible to provide several websites for the scraper to check. To
do this, pass two or more websites after the --domains argument. For instance:

python soulection_to_spotify.py --domains www.echobox.com www.wikipedia.com

This will return one dictionary (as above) for each website.

## Using soulection_to_spotify.py as a Module in Your Python Scripts
The file may be imported as a module and used to return JavaScript requests of any website.

``` python
import soulection_to_spotify as ss

spotify_playlist_show_400 = ss.soulection_to_spotify(400)

spotify_playlist_show_274 = ss.soulection_to_spotify(274)

spotify_playlist_show_462 = ss.soulection_to_spotify(462) 
```


## Technologies
This project is created with

Selenium a popular Python library used to automate web browser interaction. Version: 3.141.0  
Webdrive-Manager which simplifies the management of binary drivers for different browsers
.  Version: 3.2.2