from sentence_transformers import util
import numpy as np

def event_similarity(event: str, model, df):
    event_embedding = model.encode(event, convert_to_tensor=True)
    lyrics_embeddings = model.encode(df['lyrics'].tolist(), convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(event_embedding, lyrics_embeddings)
    return similarities[0].cpu().numpy()

def event_list_similarity(event_list: list[str], model, df):
    num_events = len(event_list)
    similarity = np.array([0.0 * num_events])
    for event in event_list:
        result = np.array(event_similarity(event, model, df))
        similarity = similarity + result
    return similarity