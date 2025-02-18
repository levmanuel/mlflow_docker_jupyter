# Utiliser une image Python officielle
FROM python:3.9-slim

# Définir les variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV MLFLOW_PORT=5000
ENV JUPYTER_PORT=8888

# Mettre à jour et installer les dépendances système
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Créer et définir le répertoire de travail
WORKDIR /app

# Copier les requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers du projet
COPY . .

# Exposer les ports pour Jupyter et MLflow
EXPOSE ${JUPYTER_PORT} ${MLFLOW_PORT}

# Commande de démarrage
CMD ["sh", "-c", "mlflow server --host 0.0.0.0 --port $MLFLOW_PORT --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns & jupyter lab --ip=0.0.0.0 --port=$JUPYTER_PORT --no-browser --allow-root --NotebookApp.token=''"]