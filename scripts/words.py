from scripts.stem import stem_word

def words_in_lyrics_occurance(words, df):
    phrases = []
    words_stems = []
    for word in words:
        if ' ' in word:
            phrases.append(word)
        else:
            words_stems.append(stem_word(word))
    occurance_list = []
    for lyrics in df['preprocessed_lyrics']:
        lyrics_stems = [stem_word(word) for word in lyrics.split(" ")]
        occurance = 0.0
        for stem in words_stems:
            if stem in lyrics_stems:
                occurance += 1.0
        for phrase in phrases:
            if phrase in lyrics:
                print("jest")
                occurance += 1.0
        occurance_list.append(occurance/len(words))
    return occurance_list
