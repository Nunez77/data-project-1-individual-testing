import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
us_pd = pd.read_csv("csvs/regional-mx-weekly-latest.csv")
header_row = 0
us_pd.columns = us_pd.iloc[header_row]
us_pd = us_pd.drop(header_row)

track_names = us_pd['Track Name'].to_list()
track_ids = []
count=1
for track in track_names:
    song_name = track
    song_results = sp.search(q=song_name, type='track', limit=1)
    if (len(song_results['tracks']['items']))>0:
        track_ids.append(song_results['tracks']['items'][0]['id'])
    else:
        track_ids.append('0')
us_pd['Track ID'] = track_ids
danceability = []
energy = []
valence = []
genres = []
loudness = []
speechiness = []
acousticness = []
instrumentalness = []
liveness = []
tempo = []
for track in us_pd['Track ID']:
    trackid = track
    if trackid>str(0) :
        trackdetails=sp.track(trackid)
        feat_results = sp.audio_features([track])
        danceability.append(feat_results[0]['danceability'])
        energy.append(feat_results[0]['energy'])
        valence.append(feat_results[0]['valence'])
        loudness.append(feat_results[0]['loudness'])
        speechiness.append(feat_results[0]['speechiness'])
        acousticness.append(feat_results[0]['acousticness'])
        instrumentalness.append(feat_results[0]['instrumentalness'])
        liveness.append(feat_results[0]['liveness'])
        tempo.append(feat_results[0]['tempo'])
        genres.append(sp.artist(trackdetails["artists"][0]["external_urls"]["spotify"])["genres"])

    else:
        danceability.append('0')
        energy.append('0')
        valence.append('0')
        loudness.append('0')
        speechiness.append('0')
        acousticness.append('0')
        instrumentalness.append('0')
        liveness.append('0')
        tempo.append('0')
        genres.append('0')
us_pd['Danceability'] = danceability
us_pd['Valence'] = energy
us_pd['Energy'] = valence
us_pd['Genres'] = genres
us_pd['loudness'] = loudness
us_pd['speechiness'] = speechiness
us_pd['acousticness'] = acousticness
us_pd['instrumentalness'] = instrumentalness
us_pd['liveness'] = liveness
us_pd['tempo'] = tempo
us_pd.to_csv('mexico_weekly_latest.csv',index=False,columns=['Position','Track Name','Artist','Streams','Danceability','Valence','Energy','Genres','loudness','speechiness','acousticness','instrumentalness','liveness','tempo'])
print(us_pd)
