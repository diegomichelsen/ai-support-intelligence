
import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# 1. Carrega as credenciais do PostgreSQL salvas no .env
load_dotenv(Path(__file__).resolve().parent / ".env")

# 2. Localiza os arquivos JSON na pasta Downloads
PASTA = (
    Path.home()
    / "Downloads"
    / "ai_support_dataset_validado"
    / "ai_support_dataset"
    / "conversations"
)

# 3. Encontra todos os arquivos JSON
arquivos = sorted(PASTA.rglob("*.json"))

if not arquivos:
    raise SystemExit(
        f"Nenhum JSON encontrado. Verifique a pasta: {PASTA}"
    )

print(f"Encontrados {len(arquivos)} arquivos JSON.")

inseridos = 0
ignorados = 0

# 4. Conecta ao PostgreSQL do Supabase
with psycopg.connect(os.environ["DATABASE_URL"]) as conexao:
    with conexao.cursor() as cursor:

        # 5. Lê e importa cada conversa
        for arquivo in arquivos:
            conversa = json.loads(
                arquivo.read_text(encoding="utf-8")
            )

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

# 6. Exibe o resultado após confirmar a transação
print("Importação concluída!")
print(f"Conversas inseridas: {inseridos}")
print(f"Conversas já existentes: {ignorados}")
