import tkinter as tk
from sentence_transformers import SentenceTransformer
import pandas as pd
from scripts.events import event_list_similarity
from scripts.words import words_in_lyrics_occurance

pd.set_option('display.max_rows', None) 
pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000) 
pd.set_option('display.colheader_justify', 'center')  
pd.set_option('display.float_format', '{:.2f}'.format) 

def process_form():
    global df, model
    global album_vars, add_info_vars, events_entry, words_entry, selected_emotion

    selected_albums = [album for album, var in zip(all_albums, album_vars) if var.get()]
    selected_add_info = [info for info, var in zip(all_add_info, add_info_vars) if var.get()]
    events_input = events_entry.get().split(';')
    words_input = words_entry.get().split(';')
    df_filtered = df
    selected_emotion_string = selected_emotion.get()
    
    print(selected_albums)
    print(selected_add_info)
    print(selected_emotion_string)
    print(events_input)
    print(words_input)

    #album match
    if selected_albums:
        album_match = [1.0 if album in selected_albums else 0.0 for album in df_filtered['album']]
        df_filtered['album_match'] = album_match
    else:
        df_filtered['album_match'] = [1.0] * len(df_filtered['title'])

    #additional info match
    if selected_add_info:
        addinfo_match = []
        for song_info in df_filtered['additional info']:
            if isinstance(song_info, str):
                matching_infos = 0
                song_infos = song_info.split(',')
                for info in selected_add_info:
                    if info in song_infos:
                        matching_infos += 1
                addinfo_match.append(matching_infos / len(selected_add_info))
            else:
                addinfo_match.append(0.0)
        df_filtered['addinfo_match'] = addinfo_match
    else:
        df_filtered['addinfo_match'] = [1.0] * len(df_filtered['title'])

    # emotion match
    if selected_emotion_string != '':
        emotion_match = [1.0 if emotion == selected_emotion_string else 0.0 for emotion in df_filtered['emotions']]
        df_filtered['emotion_match'] = emotion_match
    else:
        df_filtered['emotion_match'] = [1.0] * len(df_filtered['title'])

    #events similarity
    if events_input != ['']:
        df_filtered['similarity'] = event_list_similarity(events_input, model, df_filtered)
    else:
        df_filtered['similarity'] = [1.0] * len(df_filtered['title'])

    #words occurance
    if words_input != ['']:
        df_filtered['occurance'] = words_in_lyrics_occurance(words_input, df_filtered)
    else:
        df_filtered['occurance'] = [1.0] * len(df_filtered['title'])

    #score
    df_filtered['score'] = 2 * df_filtered['similarity'] + df_filtered['occurance'] +  df_filtered["addinfo_match"] + df_filtered["album_match"] + df_filtered['emotion_match']
    df_filtered = df_filtered.sort_values(by='score', ascending=False)
    print(df_filtered[['title', 'album', 'album_match', 'addinfo_match', 'emotion_match', 'similarity', 'occurance', 'score']])
    show_results(df_filtered)

def show_results(df_filtered):
    for widget in root.winfo_children():
        widget.grid_forget()

    title_label = tk.Label(root, text="Top 10 results", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(root, text="Album", font=("Arial", 12, "bold"), width=30, anchor="w").grid(row=1, column=0, sticky="w", padx=5)
    tk.Label(root, text="Title", font=("Arial", 12, "bold"), width=30, anchor="w").grid(row=1, column=1, sticky="w", padx=5)
    tk.Label(root, text="Score", font=("Arial", 12, "bold"), width=10, anchor="w").grid(row=1, column=2, sticky="w", padx=5)
    tk.Label(root, text="", font=("Arial", 12, "bold"), width=10, anchor="w").grid(row=1, column=3, sticky="w", padx=5)

    df_filtered_sorted = df_filtered.sort_values(by='score', ascending=False).reset_index(drop=True)

    for idx, row in df_filtered_sorted.head(10).iterrows():
        tk.Label(root, text=row['album'], font=("Arial", 12), anchor="w", width=30).grid(row=2 + idx, column=0, sticky="w")
        tk.Label(root, text=row['title'], font=("Arial", 12), anchor="w", width=30).grid(row=2 + idx, column=1, sticky="w")
        tk.Label(root, text=f"{row['score']:.2f}", font=("Arial", 12), anchor="w", width=10).grid(row=2 + idx, column=2, sticky="w")
        
        lyrics_button = tk.Button(root, text="Show Lyrics", font=("Arial", 12), command=lambda title=row['title']: show_lyrics(title))
        lyrics_button.grid(row=2 + idx, column=3, sticky="w")

    back_button = tk.Button(root, text="Back", font=("Arial", 12), command=show_form)
    back_button.grid(row=12, column=1, columnspan=2, pady=20)

def show_form():
    global album_vars, add_info_vars, events_entry, words_entry, selected_emotion

    for widget in root.winfo_children():
        widget.grid_forget()

    title_label = tk.Label(root, text="RHCP Song Finder", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    album_label = tk.Label(root, text="Choose album:", font=("Arial", 12))
    album_label.grid(row=1, column=0, sticky="w")
    album_vars = [tk.BooleanVar() for _ in all_albums]
    for idx, album in enumerate(all_albums):
        tk.Checkbutton(root, text=album, variable=album_vars[idx]).grid(row=2 + idx, column=0, sticky="w")

    add_info_label = tk.Label(root, text="Choose additional info:", font=("Arial", 12))
    add_info_label.grid(row=1, column=1, sticky="w")
    add_info_vars = [tk.BooleanVar() for _ in all_add_info]
    for idx, info in enumerate(all_add_info):
        tk.Checkbutton(root, text=info, variable=add_info_vars[idx]).grid(row=2 + idx, column=1, sticky="w")

    events_label = tk.Label(root, text="Song description or events (semicolon separated):", font=("Arial", 12))
    events_label.grid(row=6, column=1, sticky="w")
    events_entry = tk.Entry(root, font=("Arial", 12))
    events_entry.grid(row=7, column=1, columnspan=2, pady=5)

    words_label = tk.Label(root, text="Words and phrases (semicolon separated):", font=("Arial", 12))
    words_label.grid(row=8, column=1, sticky="w")
    words_entry = tk.Entry(root, font=("Arial", 12))
    words_entry.grid(row=9, column=1, columnspan=2, pady=5)

    emotion_label = tk.Label(root, text="Emotion:", font=("Arial", 12))
    emotion_label.grid(row=10, column=1, sticky="w")

    selected_emotion = tk.StringVar(root)
    selected_emotion.set(all_emotions[0])

    emotion_menu = tk.OptionMenu(root, selected_emotion, *all_emotions)
    emotion_menu.grid(row=11, column=1, sticky="w")

    submit_button = tk.Button(root, text="Send", font=("Arial", 12), command=process_form)
    submit_button.grid(row=12, column=1, columnspan=2, pady=0)

def show_lyrics(song_title):
    song_lyrics = df.loc[df['title'] == song_title, 'lyrics'].values
    lyrics = song_lyrics[0] if len(song_lyrics) > 0 else "Lyrics not found."
    
    lyrics_window = tk.Toplevel(root)
    lyrics_window.title(f"Lyrics: {song_title}")

    tk.Label(lyrics_window, text=f"Lyrics of {song_title}", font=("Arial", 16)).pack(pady=10)
    text_widget = tk.Text(lyrics_window, font=("Arial", 12), wrap="word", width=60, height=20)
    text_widget.insert("1.0", lyrics)
    text_widget.config(state="disabled")
    text_widget.pack(padx=10, pady=10)

    tk.Button(lyrics_window, text="Close", font=("Arial", 12), command=lyrics_window.destroy).pack(pady=10)


model = SentenceTransformer('all-MiniLM-L6-v2')
df = pd.read_csv('databases/database7.csv', sep=';', header=0)

all_albums = ["The Red Hot Chili Peppers", "Freaky Styley", "The Uplift Mofo Party Plan", "Mother's Milk", 
              "Blood Sugar Sex Magik", "One Hot Minute", "Californication", "By The Way", "Stadium Arcadium", 
              "I'm With You", "I'm With You Sessions", "The Getaway", "Unlimited Love", "Return Of The Dream Canteen"]
all_add_info = ['Instrumental', 'Bonus Track', 'video', 'single']
all_emotions = ['', 'sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

root = tk.Tk()
root.title("RHCP Song Finder")

show_form()

root.mainloop()
