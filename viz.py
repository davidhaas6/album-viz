import spotipy_fork
from spotipy_fork import util
from tqdm import tqdm
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import spotoken

def get_data(max_track_num=15):
    sp = spotipy_fork.Spotify(auth=spotoken._generate_token())

    # Get all albums from all artists in all of my playlists
    playlist_URIs = [playlist['uri'] for playlist in sp.current_user_playlists(limit=50)['items']]
    playlist_tracks = [track for pl_uri in playlist_URIs for track in sp.user_playlist_tracks(sp.me()['uri'], pl_uri, limit=100)['items']]
    artist_URIs = list(set([artist['uri'] for track in playlist_tracks for artist in track['track']['artists']]))

    # Populate a dict with the popularities for each track number
    popularities = defaultdict(list)
    count = 0
    for art_uri in tqdm(artist_URIs):
        try:
            for album in sp.artist_albums(art_uri)['items']:
                track_uris = [track['uri'] for track in sp.album_tracks(album['uri'], limit=max_track_num)['items']]
                for track in sp.tracks(track_uris)['tracks']:
                    popularities[track['track_number']].append(track['popularity'])
                    count += 1
        except Exception as e:
            print(e)
    print("Examined {} songs!".format(count))


    # Calculate average popularities
    track_nums = list()
    avg_pops = list()
    for track_num, pops in popularities.items():
        track_nums.append(track_num)
        avg_pops.append(np.mean(pops))
    
    np.save('pop.npy', (track_nums, avg_pops))
    return track_nums, avg_pops

def plot_data(track_nums, avg_pops):
    plt.bar(track_nums, avg_pops)
    plt.ylabel("Popularity")
    plt.xlabel("Track number")
    plt.title("Popularity ")
    plt.yticks(np.arange(0, 101, 10))
    plt.xticks(np.arange(1, 16, 2))
    plt.show()

if __name__ == "__main__":
    import sys
    nums, pop = get_data()
    plot_data(nums,pop)