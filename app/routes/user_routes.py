from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import uuid
import shutil
import os
from ..services.face_service import get_normalized_embedding, calculate_distance
from ..services.password_service import hash_password, verify_password
from ..services.chroma_service import get_all_users, add_user_to_collection

router = APIRouter()

IMG_DIR = "face_store"
os.makedirs(IMG_DIR, exist_ok=True)

@router.post("/cadastrar")
async def cadastrar(nome: str = Form(...), email: str = Form(...), senha: str = Form(...), imagem: UploadFile = File(...)):
    users = get_all_users()
    if any(u["email"] == email for u in users["metadatas"]):
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    
    img_path = os.path.join(IMG_DIR, f"{uuid.uuid4().hex}_{imagem.filename}")
    with open(img_path, "wb") as f:
        shutil.copyfileobj(imagem.file, f)

    embedding = get_normalized_embedding(img_path)
    user_id = uuid.uuid4().hex
    metadata = {
        "nome": nome,
        "email": email,
        "senha_hash": hash_password(senha),
        "img_path": img_path
    }

    add_user_to_collection(user_id, embedding, metadata)
    return {"mensagem": "Cadastro realizado com sucesso!", "id": user_id}

@router.post("/verificar")
async def verificar(email: str = Form(...), senha: str = Form(...), imagem: UploadFile = File(...)):
    temp_path = f"temp_{uuid.uuid4().hex}.jpg"
    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(imagem.file, f)

        users = get_all_users()
        user_index = next((i for i, meta in enumerate(users["metadatas"]) if meta["email"] == email), None)

        if user_index is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
        user = users["metadatas"][user_index]
        if not verify_password(senha, user["senha_hash"]):
            raise HTTPException(status_code=403, detail="Senha incorreta.")

        login_emb = get_normalized_embedding(temp_path)
        stored_emb = users["embeddings"][user_index]
        distance = calculate_distance(stored_emb, login_emb)

        if distance <= 0.65:
            return {"match": True, "mensagem": f"Bem-vindo, {user['nome']}.", "distancia": distance}
        else:
            return {"match": False, "mensagem": "Imagem não corresponde.", "distancia": distance}

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)