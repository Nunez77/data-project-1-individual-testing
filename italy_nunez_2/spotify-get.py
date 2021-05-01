import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# to use this file register a spotify dev account from : https://developer.spotify.com/dashboard/login
# once the account is created make an app and get a client id and a client secret

client_id =  # enter client id
client_secret =  # enter client secret

client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# time stuffs
starting_month = 2
ending_month = 10
starting_year = 2018
ending_year = 2020
years = ending_year - starting_year

# country use an ISO code from below
country = "GB" # great britain

"""
['AD', 'AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'EC', 'SV', 'EE', 'FI'
, 'FR','DE', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'ID', 'IE', 'IT', 'JP', 'LV', 'LI', 'LT', 'LU', 'MY', 'MT', 'MX', 'MC'
, 'NL', 'NZ','NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'ES', 'SK', 'SE', 'CH', 'TW', 'TR', 'GB', 'US', 'UY']
"""

#new_releases()

# initialize dataset
df = pd.DataFrame([["chicago rap", 0]], columns=["genre", "total popularity"])

genres_within = []
for l in range(years):
	for i in range(1): # this loop gets a sample of 50 tracks per loop
		track_results = sp.search(market=country, q='year:' + str(starting_year + l), type='track', limit=50,offset=i)
		for track in track_results['tracks']['items']:

			# ensure within timeline
			album = sp.album(track["album"]["external_urls"]["spotify"])
			try:
				if int(album["release_date"].split("-")[1]) < starting_month and int(album["release_date"].split("-")[0]) == starting_year:
					continue
				if int(album["release_date"].split("-")[1]) > ending_month and int(album["release_date"].split("-")[0]) == ending_year:
					continue
			except IndexError:
				continue # sometimes there are no month dates


			# get genre from artist, cant get the genre from track because spotify does not have that data
			artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
			for genre in artist["genres"]:
				if len(df.loc[df["genre"] == genre]) == 0:
					df = pd.concat(
						[pd.DataFrame([[genre, track["popularity"]]], columns=["genre", "total popularity"]), df],
						ignore_index=True) # if new genre append to dataset
				df.loc[df["genre"] == genre, ["total popularity"]] += track["popularity"] # add popularity to count



df.to_csv("genre_data.csv") # save to csv
print(df.loc[df["total popularity"] > max(df["total popularity"])]) # print most popular genre
