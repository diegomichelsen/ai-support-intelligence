"""
Gera conversas de atendimento 100% fictícias no formato de schema/conversation.schema.json.

Uso (na raiz do projeto):
    python scripts/generate_synthetic_data.py            # gera 50 conversas
    python scripts/generate_synthetic_data.py --total 200

Os arquivos são gravados em data/synthetic/conversations/, um JSON por conversa.
A semente fixa (--seed) garante que o mesmo comando gere sempre os mesmos dados,
o que deixa testes e demonstrações reproduzíveis.
"""

import argparse
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Raiz do projeto (um nível acima de scripts/)
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "synthetic" / "conversations"

BRANDS = ["brand_alpha", "brand_beta", "brand_gamma", "brand_delta"]
CHANNELS = ["chat", "email", "whatsapp"]
FIRST_NAMES = ["Ana", "Bruno", "Carla", "Daniel", "Elisa", "Felipe", "Gabriela", "Hugo", "Isabela", "João"]
LAST_NAMES = ["Almeida", "Barros", "Cardoso", "Duarte", "Esteves", "Freitas", "Gomes", "Henriques"]
AGENTS = [("agent_01", "Analista 01"), ("agent_02", "Analista 02"), ("agent_03", "Analista 03")]

# Pares (mensagem do cliente, resposta do analista) por tipo de demanda
SCENARIOS = {
    "saque": (
        "Solicitei um saque ontem e ainda não caiu na minha conta.",
        "Verifiquei aqui: o saque está em processamento e deve ser concluído em até 24 horas úteis.",
    ),
    "deposito": (
        "Fiz um depósito, mas o saldo não foi atualizado.",
        "Encontrei o depósito pendente de confirmação bancária. Assim que confirmado, o saldo é atualizado.",
    ),
    "cadastro": (
        "Não consigo concluir a validação do meu cadastro.",
        "O documento enviado está ilegível. Pode enviar uma nova foto com boa iluminação?",
    ),
    "acesso": (
        "Esqueci minha senha e o e-mail de recuperação não chega.",
        "Reenviei o link de recuperação. Confira também a caixa de spam, por favor.",
    ),
}


def iso(dt: datetime) -> str:
    """Converte data/hora para texto no padrão ISO 8601 (ex.: 2026-10-01T14:30:00Z)."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def build_conversation(index: int, rng: random.Random) -> dict:
    conv_id = f"conv_{index:05d}"
    created = datetime(2026, 9, 1, tzinfo=timezone.utc) + timedelta(minutes=rng.randint(0, 60 * 24 * 45))
    status = rng.choices(["closed", "open", "pending"], weights=[80, 12, 8])[0]
    agent_id, agent_name = rng.choice(AGENTS)
    first, last = rng.choice(FIRST_NAMES), rng.choice(LAST_NAMES)
    customer_id = f"cust_{rng.randint(1, 9999):05d}"
    question, answer = SCENARIOS[rng.choice(list(SCENARIOS))]

    # Sequência da conversa: bot recepciona, cliente explica, analista resolve
    turns = [
        ("bot", "bot_welcome", "Olá! Sou o assistente virtual. Como posso ajudar?"),
        ("customer", customer_id, question),
        ("human_agent", agent_id, answer),
        ("customer", customer_id, rng.choice(["Obrigado!", "Perfeito, obrigada.", "Ok, vou aguardar."])),
    ]

    messages = []
    moment = created
    for seq, (author_type, author_id, body) in enumerate(turns, start=1):
        moment += timedelta(minutes=rng.randint(1, 8))
        messages.append({
            "id": f"{conv_id}_msg_{seq:02d}",
            "sequence": seq,
            "author_type": author_type,
            "author_id": author_id,
            "body": body,
            "created_at": iso(moment),
            "attachments": [],
        })

    return {
        "id": conv_id,
        "brand_id": rng.choice(BRANDS),
        "channel": rng.choice(CHANNELS),
        "status": status,
        "created_at": iso(created),
        "closed_at": iso(moment) if status == "closed" else None,
        "customer": {
            "id": customer_id,
            "name": f"{first} {last}",
            "email": f"{first.lower()}.{last.lower()}@example.com",  # domínio reservado para exemplos
        },
        "assignee": {"id": agent_id, "name": agent_name},
        "messages": messages,
        "source": {
            "type": "synthetic",
            "metadata_origin": "synthetic",
            "original_reference": None,
            "synthetic_fields": ["*"],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera conversas sintéticas.")
    parser.add_argument("--total", type=int, default=50, help="Quantidade de conversas")
    parser.add_argument("--seed", type=int, default=42, help="Semente para resultados reproduzíveis")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i in range(1, args.total + 1):
        conversation = build_conversation(i, rng)
        path = OUTPUT_DIR / f"{conversation['id']}.json"
        path.write_text(json.dumps(conversation, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{args.total} conversas geradas em {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
