# Usar uma imagem leve do Python
FROM python:3.11-slim

# Define a pasta de trabalho dentro do container
WORKDIR /code

# Copia as dependências e instala
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia o resto do código
COPY ./app /code/app

# Comando para rodar a API quando o container subir
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]