# Import modules
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import spotipy
import spotipy.util as util
import base64
import re
import argparse

# Function to return ids of Spotify songs
USER_AGENT = 'User-Agent'
MOZILLA_GENERAL_TOKEN = 'Mozilla/5.0'
HTML_SPOTIFY_TITLE = 'spotify'
HREF_ATTRIBUTE = 'href'
SPLITTER = 'track/'

URL = 'https://soulectiontracklists.com/episodes/'
HEADER = {USER_AGENT:MOZILLA_GENERAL_TOKEN}

SPOTIFY_HREFS_LIST = list()
SPOTIFY_IDS_LIST = list()
CLEANED_SPOTIFY_IDS_LIST = list()

def loop_spotify_titles(spotify_id_list, spotify_title_soup):
    """

    :param spotify_id_list (list): Empty list for the found Spotify "Title" tags to be appended into
    :param spotify_title_soup (bs4 object): Object returned from searching for a HTML "Title" tag
    :return spotify_id_list (list): Populated list containing appended "Title" tags
    """
    for spotify_title in spotify_title_soup:
        spotify_id_list.append(spotify_title[HREF_ATTRIBUTE])

    return spotify_id_list

def loop_spotify_ids(spotify_ids_list, spotify_href_list):
    """

    :param spotify_id_list (list): Populated list containing appended "Title" tag
    :param spotify_href_list (list): Empty list for the found hrefs in the "Title" tag
    :return spotify_ids_list(list): Populated list containing appended hrefs tags
    """
    for spotify_song_id in spotify_href_list:
        spotify_ids_list.append(spotify_song_id.split(SPLITTER)[1])

    return spotify_ids_list


def clean_spotify_ids(clean_spotify_ids_list, spotify_ids_list):
    """

    :param clean_spotify_ids_list (list): Populated list containing Spotify hrefs
    :param spotify_ids_list (list): Empty list used to append cleaned Spotify IDs
    :return clean_spotify_ids_list (list): Populated list containing appended cleaned Spotify IDs
    """
    for id in spotify_ids_list:
        clean_spotify_ids_list.append(id[:22])

    return clean_spotify_ids_list

def soulection_show_spotify_song_ids(show_id):
    """

    :param show_id (int): Integer value for the Soulection Radio Show
    :return clean_spotify_ids_list (list): List with Spotify song IDs for searched Soulection Show
    """
    soulection_tracklist_url = URL + str(show_id)
    request = Request(soulection_tracklist_url, headers=HEADER)
    soulection_tracklist_url_response = urlopen(request)
    soup = BeautifulSoup(soulection_tracklist_url_response)
    spotify_title_soup = soup.find_all(title=HTML_SPOTIFY_TITLE)

    spotify_href_list = loop_spotify_titles(SPOTIFY_HREFS_LIST, spotify_title_soup)
    spotify_id_list = loop_spotify_ids(SPOTIFY_IDS_LIST, spotify_href_list)
    clean_spotify_ids_list = clean_spotify_ids(CLEANED_SPOTIFY_IDS_LIST, spotify_id_list)

    return clean_spotify_ids_list


# Function for Spotipy authentication
SPOTIFY_API_CREDENTIALS = pd.read_csv(r'spotify_api_keys.csv',
                                      header=None)

SPOTIFY_USER_ID = SPOTIFY_API_CREDENTIALS[1].iloc[0]
SPOTIFY_CLIENT_ID = SPOTIFY_API_CREDENTIALS[1].iloc[1]
SPOTIFY_CLIENT_SECRET = SPOTIFY_API_CREDENTIALS[1].iloc[2]
REDIRECT_URL = 'http://127.0.0.1:9090'

## All scope
SPOTIFY_AUTHORIZATION_SCOPE = 'ugc-image-upload user-read-playback-state streaming ' \
                              'user-read-email playlist-read-collaborative '  \
                              'user-modify-playback-state user-read-private  ' \
                              'playlist-modify-public user-library-modify user-top-read ' \
                              'user-read-playback-position user-read-currently-playing ' \
                              'playlist-read-private user-follow-read app-remote-control ' \
                              'user-read-recently-played user-follow-modify user-library-read'

def spotify_authentication(spotify_user_id, spotify_authorization_scope, spotify_client_id,
                           spotify_client_secret, redicrect_url):
    """

    :param spotify_user_id (int): Soptify user ID
    :param spotify_authorization_scope (string): Spotify scope shares information only declared
    :param spotify_client_id (string): Spotify Developer Client ID
    :param spotify_client_secret (string): Spotify Developer Client Secret
    :param redicrect_url (url): Spotify Developer redirect URI
    :return:
    """
    token = util.prompt_for_user_token(
        spotify_user_id,
        spotify_authorization_scope,
        client_id = spotify_client_id,
        client_secret = spotify_client_secret,
        redirect_uri=redicrect_url)

    sp = spotipy.Spotify(auth=token)

    return sp


sp = spotify_authentication(SPOTIFY_USER_ID, SPOTIFY_AUTHORIZATION_SCOPE, SPOTIFY_CLIENT_ID,
                       SPOTIFY_CLIENT_SECRET, REDIRECT_URL)


PLAYLIST_PREFFIX = 'Soulection Show'

def create_and_add_tracks_to_playlist(spotify_song_ids, playlist_name):
    """

    :param spotify_song_ids (list): List of Spotify song IDs
    :param playlist_name (string): Name of playlist to be created
    :return playlist['id'] (string): Spotify ID of created playlist
    """
    playlist = sp.user_playlist_create(SPOTIFY_USER_ID, playlist_name)
    sp.playlist_add_items(playlist['id'], spotify_song_ids)

    return playlist['id']


ALT_TAG = 'Show #'
SRCSET_ATTRIBUTE = 'srcset'
SPLIT_BY_COMMA = ','
SPLIT_BY_SPACE = ' '
INDEX_2 = 2
INDEX_1 = 1
INDEX_0 = 0
REGEX_WILDCARD = '.*'

# Function that returns the href of the cover art
def soulection_show_art_cover_href(show_id, index):
    """

    :param show_id (int): Soulection Radio Show ID
    :param index (int): Integer (index) that determines quality of image to download
    :return (string): HREF of Souecltion Radio Show cover art
    """
    soulection_tracklist_url = URL + str(show_id)
    request = Request(soulection_tracklist_url, headers=HEADER)
    soulection_tracklist_url_response = urlopen(request)
    soup = BeautifulSoup(soulection_tracklist_url_response)
    soulection_show_cover_art_soup = soup.find(alt=re.compile(ALT_TAG + str(show_id) +
                                                              REGEX_WILDCARD))

    soulection_show_cover_art_href_string = soulection_show_cover_art_soup[SRCSET_ATTRIBUTE].split \
        (SPLIT_BY_COMMA)[index].split(SPLIT_BY_SPACE)[INDEX_0][1:]

    return soulection_show_cover_art_href_string

IMAGE_FOLDER = r'C:\Users\Jaume\Documents\Python ' \
               r'Projects\soulection_playlists\soulection_show_cover_art\''
JPEG_STRING = '.jpeg'
WRITING_BINARY = 'wb'
READ_BINARY = 'rb'
UTF_8_ENCODING = 'utf-8'

# Function that saves the cover art href to a jpeg on the local
def save_jepg_from_href(href, playlist_name):
    """

    :param href (string): HREF of Souecltion Radio Show cover art
    :return:
    """
    file = open(IMAGE_FOLDER + playlist_name + JPEG_STRING, WRITING_BINARY)
    file.write(requests.get(href).content)
    file.close()

    pass

# Function that encodes the jpeg to base64 (required by Spotify)
def get_base64_encoded_image(image_path):
    """

    :param image_path (string): Local path of where image is stored
    :return base64 (string): Base64 encoded image
    """
    with open(image_path, READ_BINARY) as img_file:
        return base64.b64encode(img_file.read()).decode(UTF_8_ENCODING)


# Function that groups the entire cover art process
def upload_spotify_playlist_cover_art(show_ids_list, index, playlist_id, playlist_name):
    """

    :param show_ids_list (list): List of Spotify song IDs
    :param index (int): Integer (index) that determines quality of image to download
    :param playlist_id (sting): Spotify ID of created playlist
    :return:
    """

    href = soulection_show_art_cover_href(show_ids_list, index)
    save_jepg_from_href(href, playlist_name)
    base64_encoded_cover_art = get_base64_encoded_image(IMAGE_FOLDER + playlist_name +
                                                        JPEG_STRING)
    sp.playlist_upload_cover_image(playlist_id, base64_encoded_cover_art)

    pass


PLAYLIST_DESCRIPTION_PART1 = 'This playlist contains songs, in order, from Soulection Radio Show '
PLAYLIST_DESCRIPTION_PART2 = '. The playlist only has songs that can be found on Spotify and ' \
                             'therefore is missing "SoundCloud gems". You are welcome to share it' \
                             ' with friends! This playlist and all of the others (Soulection) ' \
                             'have been created automatically using Python.'


def soulection_show_to_spotify_playlist(soulection_show_id):
    """

    :param soulection_show_id (int): Soulection Radio Show ID
    :return:
    """

    playlist_name = PLAYLIST_PREFFIX + ' ' + str(soulection_show_id)
    playlist_description = PLAYLIST_DESCRIPTION_PART1 + str(soulection_show_id) + \
                           PLAYLIST_DESCRIPTION_PART2

    show_spotify_ids = soulection_show_spotify_song_ids(soulection_show_id)
    created_playlist_id = create_and_add_tracks_to_playlist(show_spotify_ids, playlist_name)

    try:
        upload_spotify_playlist_cover_art(soulection_show_id, INDEX_1, created_playlist_id,
                                          playlist_name)
    except:
        upload_spotify_playlist_cover_art(soulection_show_id, INDEX_2, created_playlist_id,
                                          playlist_name)

    sp.playlist_change_details(created_playlist_id, public=True, description=playlist_description)

    pass


IMG_TAG = 'img'
ALT_ELEMENT = 'alt'
SPLIT_BY_POUND = '#'


def most_recent_soulection_show():
    soulection_tracklist_url = URL
    request = Request(soulection_tracklist_url, headers=HEADER)
    soulection_tracklist_url_response = urlopen(request)
    soup = BeautifulSoup(soulection_tracklist_url_response)
    most_recent_soulection_show_id = soup.find(IMG_TAG)[ALT_ELEMENT].split(SPLIT_BY_POUND)[INDEX_1]

    return most_recent_soulection_show_id

returned_show_id = most_recent_soulection_show()
soulection_show_to_spotify_playlist(returned_show_id)


# To run from the terminal provide the Show IDs for which the scraper should create Spotify
# playlists for ```--shows``` argument.
# Example: python soulection_show_to_spotify_playlist.py --shows 404
# if __name__ == "__main__":
#     CLI = argparse.ArgumentParser()
#     CLI.add_argument(
#         "--shows",
#         nargs="*",
#         type=str,
#         default="",
#     )
#
#     # Parse the command line
#     ARGS = CLI.parse_args()
#     for show in ARGS.shows:
#         print(soulection_show_to_spotify_playlist(show))
