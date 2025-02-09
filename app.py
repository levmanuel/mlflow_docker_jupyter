import streamlit as st
import mlflow
import requests
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

st.title("Entraînement sur le dataset Diabetes avec MLflow et Airflow")

st.write("Cette application permet d'entraîner un modèle de régression sur le dataset diabetes et de suivre l'expérimentation avec MLflow.")

# Bouton pour entraîner directement le modèle
if st.button("Entraîner directement le modèle"):
    st.info("Chargement du dataset et entraînement du modèle...")
    # Charger le dataset
    diabetes = load_diabetes()
    X_train, X_test, y_train, y_test = train_test_split(
        diabetes.data, diabetes.target, test_size=0.2, random_state=42)
    
    # Afficher un aperçu du dataset
    st.subheader("Aperçu du dataset Diabetes")
    st.dataframe(diabetes.head())

    # Afficher des statistiques descriptives
    st.subheader("Statistiques descriptives")
    st.write(diabetes.describe())

    # Afficher un graphique de distribution de la cible
    st.subheader("Distribution de la cible (Diabètes progression)")
    fig, ax = plt.subplots()
    ax.hist(df['target'], bins=30, color='skyblue', edgecolor='black')
    ax.set_xlabel("Diabètes progression")
    ax.set_ylabel("Fréquence")
    st.pyplot(fig)


    # Configurer et démarrer l'expérience MLflow
    mlflow.set_experiment("diabetes_regression")
    with mlflow.start_run():
        model = LinearRegression()
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        
        # Enregistrer les paramètres et métriques dans MLflow
        mlflow.log_param("model", "LinearRegression")
        mlflow.log_metric("score", score)
        
        st.success(f"Entraînement terminé ! Score du modèle : {score:.3f}")
        st.write("Les paramètres et métriques ont été enregistrés dans MLflow.")

# Bouton pour déclencher le DAG Airflow
if st.button("Déclencher l'exécution du DAG Airflow"):
    st.info("Tentative de déclenchement du DAG Airflow...")
    # URL de l'API REST d'Airflow pour lancer un DAG (ici 'diabetes_training')
    airflow_url = "http://localhost:8080/api/v1/dags/diabetes_training/dagRuns"
    try:
        response = requests.post(airflow_url, json={"conf": {}})
        if response.status_code in [200, 201]:
            st.success("Le DAG Airflow a été déclenché avec succès !")
        else:
            st.error(f"Erreur lors du déclenchement du DAG Airflow : {response.text}")
    except Exception as e:
        st.error(f"Erreur de connexion à Airflow : {e}")