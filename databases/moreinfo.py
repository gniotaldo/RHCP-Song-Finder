import pandas as pd


videos = ["True Men Don't Kill Coyotes",
"Jungle Man",
"Catholic School Girls Rule",
"Fight Like a Brave",
"Good Time Boys",
"Higher Ground",
"Knock Me Down",
"Taste the Pain",
"Show Me Your Soul",
"Give It Away",
"Under the Bridge",
"Suck My Kiss",
"Breaking the Girl",
"Behind the Sun",
"If You Have to Ask",
"Soul to Squeeze",
"Warped",
"My Friends",
"Aeroplane",
"Coffee Shop",
"Love Rollercoaster",
"Scar Tissue",
"Around the World",
"Otherside",
"Californication",
"Road Trippin'",
"By the Way",
"The Zephyr Song",
"Can't Stop",
"Universally Speaking",
"Fortune Faded",
"Dani California",
"Tell Me Baby",
"Snow (Hey Oh)",
"Charlie",
"Desecration Smile",
"Hump de Bump",
"The Adventures of Rain Dance Maggie",
"Monarchy of Roses",
"Look Around",
"Brendan's Death Song",
"Dark Necessities",
"Go Robot",
"Sick Love",
"Goodbye Angels",
"Black Summer",
"Poster Child",
"These Are the Ways",
"Tippa My Tongue",
"The Drummer"]


singles = [
    "Fight Like a Brave",
"Higher Ground",
"Knock Me Down",
"Taste the Pain",
"Show Me Your Soul",
"Give It Away",
"Under the Bridge",
"Suck My Kiss",
"Breaking the Girl",
"Behind the Sun",
"If You Have to Ask",
"Soul to Squeeze",
"Warped",
"My Friends",
"Aeroplane",
"Shallow Be Thy Game",
"Coffee Shop",
"Love Rollercoaster",
"Scar Tissue",
"Around the World",
"Otherside",
"Californication",
"Road Trippin'",
"By the Way",
"The Zephyr Song",
"Can't Stop",
"Dosed",
"Universally Speaking",
"Fortune Faded",
"Dani California",
"Tell Me Baby",
"Snow (Hey Oh)",
"Desecration Smile",
"Hump de Bump",
"The Adventures of Rain Dance Maggie",
"Monarchy of Roses",
"Look Around",
"Brendan's Death Song",
"Dark Necessities",
"Go Robot",
"Sick Love",
"Goodbye Angels",
"Black Summer",
"These Are the Ways",
"Tippa My Tongue",
"The Drummer",
"Get Up and Jump",
"Jungle Man",
"Hollywood (Africa)",
"For the Thrashers",
"Deck the Halls",
"Parallel Universe",
"Save the Population",
"Did I Let You Know",
"Poster Child",
"Not the One",
"Nerve Flip",
"Eddie",
"The Shape I'm Takin'"
]

pd.set_option('display.max_rows', None)  # Wyświetl wszystkie wiersze
pd.set_option('display.max_columns', None)  # Wyświetl wszystkie kolumny
pd.set_option('display.width', 1000)  # Zwiększ szerokość wiersza, aby uniknąć łamania
pd.set_option('display.colheader_justify', 'center')  # Wyrównanie nagłówków kolumn
pd.set_option('display.float_format', '{:.2f}'.format)  # Formatowanie liczb zmiennoprzecinkowych

df = pd.read_csv('databases/database6.csv', sep=';')
is_video = []
is_single = []
titles_lower = df['title'].str.lower().values
for title in titles_lower:
    found1 = False
    found2 = False

    for video in videos:
        if title == video.lower():
            found1 = True
            is_video.append(1)
            break
    if not found1:
        is_video.append(0)

    for single in singles:
        if title == single.lower():
            found2 = True
            is_single.append(1)
            break
    if not found2:
        is_single.append(0)


df['video'] = is_video
df['single'] = is_single

for index, row in df.iterrows():
    if row['video'] == 1:
        if pd.isna(row['additional info']) or row['additional info'] == '':
            df.at[index, 'additional info'] = 'video'
        else:
            df.at[index, 'additional info'] += ',video'

for index, row in df.iterrows():
    if row['single'] == 1:
        if pd.isna(row['additional info']) or row['additional info'] == '':
            df.at[index, 'additional info'] = 'single'
        else:
            df.at[index, 'additional info'] += ',single'

df = df.drop(columns=['video', 'single'])
df.to_csv('databases/database7.csv', sep=';', index=False, encoding='utf-8')