from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import mlflow
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def train_model():
    # Charger le dataset
    diabetes = load_diabetes()
    X_train, X_test, y_train, y_test = train_test_split(
        diabetes.data, diabetes.target, test_size=0.2, random_state=42
    )
    
    # Configurer MLflow
    mlflow.set_experiment("diabetes_regression")
    with mlflow.start_run():
        model = LinearRegression()
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        
        mlflow.log_param("model", "LinearRegression")
        mlflow.log_metric("score", score)
        print(f"Score du modèle : {score:.3f}")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
}

with DAG(
    dag_id='diabetes_training',
    default_args=default_args,
    schedule_interval=None,  # Exécution manuelle uniquement
    catchup=False,
) as dag:
    training_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model
    )