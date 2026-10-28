
import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# ==========================================
# 1. CONFIGURAÇÕES DO PROJETO
# ==========================================

# Raiz do projeto (um nível acima da pasta scripts/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Arquivo privado com as credenciais do Supabase
ENV_PATH = BASE_DIR / ".env"

if not ENV_PATH.is_file():
    raise SystemExit(
        f"ERRO: Arquivo .env não encontrado em:\n{ENV_PATH}"
    )

# Carrega as credenciais, independentemente da pasta do terminal
load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if not DATABASE_URL:
    raise SystemExit(
        "ERRO: DATABASE_URL não encontrada no arquivo .env.\n"
        "Verifique se a linha começa com DATABASE_URL="
    )

print("OK: Credenciais do PostgreSQL carregadas.")


# ==========================================
# 2. LOCALIZAÇÃO DOS ARQUIVOS JSON
# ==========================================

# Pasta com os JSONs de conversas.
# Padrão: data/synthetic/conversations (dentro do projeto).
# Para usar outra pasta, defina CONVERSATIONS_DIR no arquivo .env.
PASTA = Path(
    os.getenv("CONVERSATIONS_DIR")
    or BASE_DIR / "data" / "synthetic" / "conversations"
)

if not PASTA.is_dir():
    raise SystemExit(
        f"ERRO: Pasta de conversas não encontrada:\n{PASTA}"
    )

arquivos = sorted(PASTA.rglob("*.json"))

if not arquivos:
    raise SystemExit("ERRO: Nenhum arquivo JSON encontrado.")

print(f"OK: Encontrados {len(arquivos)} arquivos JSON.")


# ==========================================
# 3. VALIDAÇÃO DOS DADOS
# ==========================================

conversas = []

for arquivo in arquivos:
    try:
        conversa = json.loads(arquivo.read_text(encoding="utf-8"))

        if not isinstance(conversa, dict):
            raise ValueError("O JSON não contém um objeto.")

        if not conversa.get("id"):
            raise ValueError("Campo id ausente ou vazio.")

        if not conversa.get("brand_id"):
            raise ValueError("Campo brand_id ausente ou vazio.")

        conversas.append(conversa)

    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as erro:
        raise SystemExit(
            f"ERRO ao validar {arquivo.name}: {erro}"
        )

print(f"OK: {len(conversas)} conversas prontas para importação.")


# ==========================================
# 4. CONEXÃO COM POSTGRESQL
# ==========================================

inseridos = 0
ignorados = 0

print("Conectando ao PostgreSQL do Supabase...")

try:
    with psycopg.connect(
        DATABASE_URL,
        connect_timeout=15
    ) as conexao:

        print("OK: Conexão estabelecida!")

        # Uma transação: se houver erro, desfaz a importação
        with conexao.cursor() as cursor:

            # ==========================================
            # 5. IMPORTAÇÃO DAS CONVERSAS
            # ==========================================

            for conversa in conversas:

                cursor.execute(
                    """
                    INSERT INTO public.conversations
                        (id, brand_id, payload)
                    VALUES (%s, %s, %s::jsonb)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        conversa["id"],
                        conversa["brand_id"],
                        json.dumps(conversa, ensure_ascii=False),
                    ),
                )

                if cursor.rowcount == 1:
                    inseridos += 1
                else:
                    ignorados += 1

    # A transação foi confirmada ao sair do bloco
    print("\nIMPORTAÇÃO CONCLUÍDA!")
    print(f"Conversas inseridas: {inseridos}")
    print(f"Conversas já existentes: {ignorados}")
    print(f"Total processado: {len(conversas)}")

except psycopg.OperationalError as erro:
    raise SystemExit(
        "ERRO: Não foi possível conectar ao PostgreSQL.\n"
        "Verifique a senha, a conexão de internet e o endereço "
        "do banco no Supabase.\n"
        f"Detalhes: {erro}"
    )

except psycopg.Error as erro:
    raise SystemExit(
        "ERRO: O PostgreSQL recusou uma operação.\n"
        "A importação desta execução foi desfeita.\n"
        f"Detalhes: {erro}"
    )
