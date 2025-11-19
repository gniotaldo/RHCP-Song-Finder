import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from nltk import word_tokenize

# wczytywanie danych
df = pd.read_csv('tfidf_logistic_regression/emotions.csv', sep=',')
df["emotion"] = df["emotion"].astype(int)

# podzial danych
X_train, X_val, y_train, y_val = train_test_split(df["text"], df["emotion"], test_size=0.2, random_state=42)

# vectorizer tf-idf
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_val_tfidf = vectorizer.transform(X_val)

# trenowanie modelu
model = LogisticRegression(max_iter=100)
model.fit(X_train_tfidf, y_train)

# predykcje na testowym zbiorze
y_pred = model.predict(X_val_tfidf)

# ewaluacja
accuracy = accuracy_score(y_val, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

print("Classification Report:")
print(classification_report(y_val, y_pred))


# ----------------------------- zastosowanie modelu do predykcji emocji tekstów piosenek

def preprocessing(text):
    word_list = [word.lower() for word in word_tokenize(text) if word.isalpha()]
    return ' '.join(word_list)

songs_database = pd.read_csv('database4.csv', sep=';')

emotion_map = {
    0: 'sadness',
    1: 'joy',
    2: 'love',
    3: 'anger',
    4: 'fear',
    5: 'surprise'
}

# preprocessowanie tekstów
preprocessed_lyrics = [preprocessing(item) for item in songs_database["lyrics"]]

# tf-idf
songs_tfidf = vectorizer.transform(preprocessed_lyrics)

emotions_predictions = model.predict(songs_tfidf)

emotions_predictions_text = [emotion_map[emotion] for emotion in emotions_predictions]

# nowa kolumna z emocjami
songs_database['emotions'] = emotions_predictions_text

songs_database.to_csv('databases/songs_with_emotions.csv', sep=';', index=False)