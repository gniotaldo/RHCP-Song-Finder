import requests
import re
import time
import random
import pandas as pd

def preprocessing(text):
    return [char.lower() for char in text if char.isalpha()]

def scrap(title):
    title = "".join(preprocessing(title))
    url = 'https://www.azlyrics.com/lyrics/redhotchilipeppers/' + title + '.html'
    print(url)
    website = requests.get(url)

    website.encoding = 'utf-8'

    html_text = website.text

    regex = r'Sorry about that. -->.+?</div>'

    scrapped_text = re.search(regex, html_text, flags=re.DOTALL).group()

    # usuwanie niepotrzebnych rzeczy
    scrapped_text = re.sub('Sorry about that. -->', '', scrapped_text)
    scrapped_text = re.sub('</div>', '', scrapped_text)
    scrapped_text = re.sub('<br>', '', scrapped_text)
    scrapped_text = re.sub('\n\n', '\n', scrapped_text)

    scrapped_text = re.sub('&quot;', '"', scrapped_text)

    song_lyrics = scrapped_text

    return song_lyrics

def remove_newline(string):
    if string[:2] == '\r\n':
        return string[2 : len(string)]
    else: 
        return string

def update_database(main_database, updated_database):
    # obecna baza danych
    df = pd.read_csv(main_database, sep=';', header=0)

    num_scrapped = 0
    lyrics_list = []

    for index, row in df.iterrows():
        title = row['title']
        existing_lyrics = row.get('lyrics', '') 

        

        wait = True

        if existing_lyrics != '':
            lyrics = existing_lyrics
            print(f"Tekst do {title} jest już w bazie.")
            wait = False
        else:
            try:
                lyrics = scrap(title)
                print(f"Pobrano tekst piosenki {title}.")
            except Exception as e:
                print(f"Błąd przy {title}: {e}")
                lyrics = "error"
            
        # brak napisów dla instrumentali
        additional_info = row.get('additional info', '')
        if additional_info == 'Instrumental':
            lyrics = ''


        lyrics_list.append(lyrics)

        num_scrapped += 1
        
        print(f"Zaktualizowano {num_scrapped} tekstów.")

        if wait:
            time.sleep(random.uniform(2, 5))


    # upewniamy sie, ze seria tekstow jest takiej samej dlugosci co seria tytułów
    while len(lyrics_list) < len(df):
        lyrics_list.append('')

    lyrics_list = [remove_newline(string) for string in lyrics_list]

    df['lyrics'] = lyrics_list

    # stworzenie nowej bazy w pliku csv
    df.to_csv(updated_database, sep=';', index=False, encoding='utf-8')

    print(f"Nowa baza danych została zapisana w pliku {updated_database}.")


update_database('database4.csv', 'database5.csv')