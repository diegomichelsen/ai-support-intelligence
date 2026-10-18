
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="AI Support Intelligence API",
    description="API for support conversation monitoring and operational intelligence.",
    version="0.1.0",
)


# Verifica se a API está funcionando
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Dados fictícios para testar a consulta de conversas
conversations = [
    {
        "id": "conv_001",
        "brand_id": "brand_001",
        "channel": "chat",
        "status": "closed",
        "messages": [
            {
                "author_type": "customer",
                "body": "Não consigo acessar minha conta.",
            },
            {
                "author_type": "human_agent",
                "body": "Vou ajudar você a recuperar o acesso.",
            },
        ],
    },
    {
        "id": "conv_002",
        "brand_id": "brand_001",
        "channel": "email",
        "status": "open",
        "messages": [
            {
                "author_type": "customer",
                "body": "Gostaria de uma atualização sobre meu chamado.",
            },
        ],
    },
]


# Retorna a lista de todas as conversas
@app.get("/conversations")
def get_conversations():
    return conversations


# Retorna uma conversa específica pelo ID
@app.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    for conversation in conversations:
        if conversation["id"] == conversation_id:
            return conversation

    raise HTTPException(
        status_code=404,
        detail="Conversation not found",
    )
