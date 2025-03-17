# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /src

# Copia los archivos de requisitos
COPY etc/requirements/base.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY src/ .

# Expone el puerto en el que la aplicación correrá
EXPOSE 8000

# Comando para correr la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]