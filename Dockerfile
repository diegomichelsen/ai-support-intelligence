FROM python:3.12-slim

WORKDIR /app

# Instala as dependências primeiro: se só o código mudar,
# o Docker reaproveita esta camada do cache e o build fica mais rápido.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação mantendo a estrutura src/
COPY src/ ./src/

EXPOSE 8000

# src.api.main:app = arquivo src/api/main.py, objeto app
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
