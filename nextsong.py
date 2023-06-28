import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

def show_song_info(event):
    song = recommended_songs.get(recommended_songs.curselection())
    if isinstance(song, dict):
        info = f"Name: {song['name']}\nArtist: {song['artists'][0]['name']}\nAlbum: {song['album']['name']}\nDuration: {song['duration_ms'] / 1000} seconds"
        messagebox.showinfo('Song Info', info)
        webbrowser.open(song['external_urls']['spotify'])  # open the song on Spotify


# Mapping from Camelot key notation to Spotify key values
camelot_key_mapping = {
    '1A': 0, '1B': 7,
    '2A': 1, '2B': 8,
    '3A': 2, '3B': 9,
    '4A': 3, '4B': 10,
    '5A': 4, '5B': 11,
    '6A': 5, '6B': 0,
    '7A': 6, '7B': 1,
    '8A': 7, '8B': 2,
    '9A': 8, '9B': 3,
    '10A': 9, '10B': 4,
    '11A': 10, '11B': 5,
    '12A': 11, '12B': 6
}

# Reverse mapping from Spotify key values to Camelot key notation
spotify_key_to_camelot = {v: k for k, v in camelot_key_mapping.items()}

def get_recommendation():
    client_id = client_id_entry.get()
    client_secret = client_secret_entry.get()
    song_name = song_name_entry.get()
    target_tempo = tempo_entry.get()
    target_key = camelot_key_mapping.get(key_entry.get().upper())

    if not client_id or not client_secret:
        messagebox.showerror('Error', 'Please enter your Spotify client ID and client secret.')
        return

    if not song_name:
        messagebox.showerror('Error', 'Please enter a song name.')
        return

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    try:
        results = sp.search(q=song_name, limit=1)  # search for the song
    except Exception as e:
        messagebox.showerror('Error', str(e))
        return

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        recs = sp.recommendations(seed_tracks=[track['id']], target_tempo=target_tempo, target_key=target_key)  # get recommendations based on the song
        if recs['tracks']:
            recommended_songs.delete(0, tk.END)
            for song in recs['tracks']:
                # Get the audio features for the song
                audio_features = sp.audio_features([song['id']])[0]
                if audio_features:
                    song_key = spotify_key_to_camelot.get(audio_features['key'], 'Unknown')
                    song_tempo = audio_features['tempo']
                else:
                    song_key = 'Unknown'
                    song_tempo = 'Unknown'

                song_info = f"{song['name']} by {song['artists'][0]['name']}, Key: {song_key}, Tempo: {song_tempo} BPM"
                recommended_songs.insert(tk.END, song_info)
        else:
            recommended_songs.delete(0, tk.END)
            recommended_songs.insert(tk.END, 'No recommendations found.')
    else:
        recommended_songs.delete(0, tk.END)
        recommended_songs.insert(tk.END, 'Song not found.')

def show_song_info(event):
    song = recommended_songs.get(recommended_songs.curselection())
    if isinstance(song, dict):
        info = f"Name: {song['name']}\nArtist: {song['artists'][0]['name']}\nAlbum: {song['album']['name']}\nDuration: {song['duration_ms'] / 1000} seconds"
        messagebox.showinfo('Song Info', info)

# Set up GUI
root = tk.Tk()
root.title('Next Song')
style = ttk.Style(root)
style.theme_use('clam')

main_frame = ttk.Frame(root, padding="10")
main_frame.pack()

instructions = ttk.Label(main_frame, text='Enter your Spotify client ID and client secret, a song name, target tempo, and target key in Camelot notation, then click Get Recommendations.')
instructions.grid(row=0, column=0, columnspan=2, pady=(0, 10))

client_id_label = ttk.Label(main_frame, text='Client ID:')
client_id_label.grid(row=1, column=0, sticky=tk.W)
client_id_entry = ttk.Entry(main_frame)
client_id_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

client_secret_label = ttk.Label(main_frame, text='Client Secret:')
client_secret_label.grid(row=2, column=0, sticky=tk.W)
client_secret_entry = ttk.Entry(main_frame, show='*')
client_secret_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

song_name_label = ttk.Label(main_frame, text='Song Name:')
song_name_label.grid(row=3, column=0, sticky=tk.W)
song_name_entry = ttk.Entry(main_frame)
song_name_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

tempo_label = ttk.Label(main_frame, text='Target Tempo:')
tempo_label.grid(row=4, column=0, sticky=tk.W)
tempo_entry = ttk.Entry(main_frame)
tempo_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))

key_label = ttk.Label(main_frame, text='Target Key (Camelot):')
key_label.grid(row=5, column=0, sticky=tk.W)
key_entry = ttk.Entry(main_frame)
key_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))

button = ttk.Button(main_frame, text='Get Recommendations', command=get_recommendation)
button.grid(row=6, column=0, columnspan=2, pady=10)

recommended_songs_label = ttk.Label(main_frame, text='Recommended Songs:')
recommended_songs_label.grid(row=7, column=0, sticky=tk.W)
recommended_songs = tk.Listbox(main_frame)
recommended_songs.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
recommended_songs.bind('<<ListboxSelect>>', show_song_info)

main_frame.columnconfigure(1, weight=1)  # allow the second column to grow and shrink
main_frame.rowconfigure(8, weight=1)  # allow the eighth row to grow and shrink

root.mainloop()
