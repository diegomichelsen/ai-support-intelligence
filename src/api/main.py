
import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

# Carrega as variáveis de ambiente.
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(
    title="AI Support Intelligence API",
    description="API for support conversation monitoring and operational intelligence.",
    version="0.4.0",
)


# Verifica se a API está funcionando.
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Conexão com PostgreSQL / Supabase.
def get_connection():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL não configurada no arquivo .env"
        )

    return psycopg.connect(DATABASE_URL)


# Lista conversas com paginação e metadados.
@app.get("/conversations")
def get_conversations(
    limit: int = 20,
    offset: int = 0,
):

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100",
        )

    if offset < 0:
        raise HTTPException(
            status_code=400,
            detail="Offset must be greater than or equal to 0",
        )

    with get_connection() as conn:
        with conn.cursor() as cursor:

            # Quantidade total de conversas.
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM public.conversations
                """
            )

            total = cursor.fetchone()[0]

            # Busca a página solicitada.
            cursor.execute(
                """
                SELECT payload
                FROM public.conversations
                ORDER BY id
                LIMIT %s
                OFFSET %s
                """,
                (limit, offset),
            )

            rows = cursor.fetchall()

    conversations = [row[0] for row in rows]

    # Verifica se existem mais registros.
    has_more = offset + len(conversations) < total

    # Resposta estruturada com metadados.
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "returned": len(conversations),
        "has_more": has_more,
        "data": conversations,
    }


# Consulta uma conversa específica pelo ID.
@app.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str):

    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT payload
                FROM public.conversations
                WHERE id = %s
                """,
                (conversation_id,),
            )

            row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return row[0]
