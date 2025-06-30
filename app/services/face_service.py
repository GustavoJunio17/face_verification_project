from deepface import DeepFace
import numpy as np

def get_normalized_embedding(image_path: str) -> list[float]:
    result = DeepFace.represent(img_path=image_path, model_name="Facenet", enforce_detection=False)
    if not result or "embedding" not in result[0]:
        raise ValueError("Nenhum rosto detectado.")
    
    emb_array = np.array(result[0]["embedding"], dtype=np.float32)
    norm = np.linalg.norm(emb_array)
    if norm == 0:
        raise ValueError("Embedding inválido.")
    
    return (emb_array / norm).tolist()

def calculate_distance(embedding1, embedding2):
    return np.linalg.norm(np.array(embedding1) - np.array(embedding2))