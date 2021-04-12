import spotipy
from spotipy import oauth2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('agg')

SPOTIPY_CLIENT_ID = '/////'
SPOTIPY_CLIENT_SECRET = '////////'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read'
user_id = 'ktj24522'
playlist_id = '1FQj4iqi8vvEOKZdREDonR'
credentials = oauth2.SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET)

token = credentials.get_access_token()
sp = spotipy.Spotify(auth=token)

def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

all_tracks = get_playlist_tracks(user_id,playlist_id)
pd.set_option('display.max_columns',None)
features_list = ['Title', 'Artist','Album','Popularity','Release Date','Explicit','Duration']
df = pd.DataFrame(columns=features_list)

for track in all_tracks:
    df = df.append({'Title': track['track']['name'],
                    'Artist': track['track']['artists'][0]['name'],
                    'Album': track["track"]["album"]["name"],
                    'Popularity': track['track']['popularity'],
                    'Release Date': track['track']['album']['release_date'],
                    'Explicit':track['track']['explicit'],
                    'Duration':track['track']['duration_ms']},ignore_index=True)

def getReleaseYear(cols):
    yr = cols.split('-')
    return yr[0]
def timeinMins(cols):
    seconds, milliseconds = divmod(cols, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds}"

df['Release Year'] = df['Release Date'].apply(getReleaseYear)
df['Time'] = df['Duration'].apply(timeinMins)
df.drop('Release Date',axis=1,inplace=True)

def mostPopularArtists():

    mostCommon = pd.DataFrame(df['Artist'].value_counts()[:5].sort_values(ascending=False))

    lst = []
    for idx, value in mostCommon.stack().iteritems():
        lst.append('You have {1} songs from {0[0]} '.format(idx, value))

    sns.barplot(x=mostCommon.index, y=mostCommon['Artist'],ci=None)
    plt.xlabel('Artist')
    plt.ylabel('Number of Songs')
    plt.title('Most Popular Artists in Your Playlist')
    plt.show()
    return lst

def explicitPct():

    pct= df['Explicit'].value_counts(normalize=True) * 100
    pctExplicit = pct[True]
    pctClean = pct[False]
    statement = []
    if pctExplicit >= 50:
        statement.append(f"{pctExplicit}% of your playlist is explicit 😮")
    else:
        statement.append(f"Just {pctExplicit} of your playlist is explicit. Nice job!")
    fig, ax = plt.subplots()
    sns.barplot(x=pct.index,y=[pct[True],pct[False]],ci=None)
    ax.set_xticklabels(['Clean','Explicit'])
    plt.ylabel('Percent of Playlist')
    plt.title('Naughty or Nice?')
    plt.show()
    return statement

def favAlbums():

    albums = pd.DataFrame(df['Album'].value_counts()[:5].sort_values(ascending=False))
    lst = []
    for idx, value in albums.stack().iteritems():
        lst.append('You have {1} songs from {0[0]} '.format(idx, value))

    plt.figure(figsize=(14, 6))
    sns.barplot(x=albums.index, y=albums['Album'], ci=None)
    plt.xlabel('Album')
    plt.ylabel('Number of Songs')
    plt.title('Most Common Albums in Your Playlist')
    plt.show()
    return lst

def mostPopularYears():
    yrs = pd.DataFrame(df['Release Year'].value_counts()[:5].sort_values(ascending=False))
    lst = []
    for idx, value in yrs.stack().iteritems():
        lst.append('You have {1} songs from {0[0]} '.format(idx, value))

    fig, (ax1, ax2) = plt.subplots(ncols=2)
    sns.distplot(df['Release Year'], kde=False, ax=ax1)
    plt.ylabel('Number of Songs')
    plt.title('Distribution Plot of Years')
    ax1.yaxis.set_label_position('left')
    ax1.yaxis.tick_left()
    ax1.yaxis.labelpad = 25

    sns.barplot(x=yrs.index, y=yrs['Release Year'], ci=None, ax=ax2)
    plt.xlabel('Year')
    plt.ylabel('Number of Songs')
    plt.title('Most Common Years in Your Playlist')
    plt.show()
    return lst


def longestAndShortest():
    df['Duration'] = df['Duration'].astype('float64')
    longestidx = df['Duration'].idxmax()
    longestSong = df.iloc[longestidx]['Title']
    shortestidx = df['Duration'].idxmin()
    shortestSong = df.iloc[shortestidx]['Title']
    lst = []
    lst.append(f"The shortest song on your playlist is {shortestSong} at {df.iloc[shortestidx]['Time']}")
    lst.append(f"The longest song on your playlist is {longestSong} at {df.iloc[longestidx]['Time']}")
    return lst
