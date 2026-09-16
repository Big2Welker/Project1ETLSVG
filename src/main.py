import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Importación de los módulos locales
from extract import extract_data
from transform import prepare_data
from dimensional_model import build_star_schema
from validate import validate_model
from load import load_warehouse

def run_pipeline():
    load_dotenv()
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE_PATH = os.path.join(BASE_DIR, "data", "raw", "Calidad_del_Agua_para_Consumo_Humano_en_Colombia_20260905.csv")
    
    # Lectura estricta del .env (Sin contraseñas hardcodeadas)
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    # Validación de seguridad
    if not all([db_user, db_pass, db_host, db_port, db_name]):
        raise ValueError("ERROR: Faltan credenciales. Por favor configura tu archivo .env")
    
    db_engine = "mysql+pymysql" if db_port == "3306" else "postgresql"
    
    print("=========================================")
    print("   INICIANDO PIPELINE ETL (ODS 6)        ")
    print("=========================================")

    # 0. CREAR BASE DE DATOS DESDE CERO
    try:
        base_uri = f"{db_engine}://{db_user}:{db_pass}@{db_host}:{db_port}/"
        engine_server = create_engine(base_uri, isolation_level="AUTOCOMMIT")
        with engine_server.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        print(f"[INIT] Base de datos '{db_name}' ha sido creada o asegurada.")
    except Exception as e:
        print(f"[INIT] Advertencia al crear base de datos (revisa si el servidor está activo): {e}")

    DB_URI = f"{db_engine}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    try:
        # 1. EXTRAER
        df_raw = extract_data(FILE_PATH)
        
        # 2. TRANSFORMAR (Limpieza)
        df_clean = prepare_data(df_raw)
        
        # 3. TRANSFORMAR (Dimensional)
        dim_tiempo, dim_geografia, fact_irca = build_star_schema(df_clean)
        
        # 4. VALIDAR
        validate_model(df_clean, dim_tiempo, dim_geografia, fact_irca)
        
        # 5. CARGAR
        load_warehouse(dim_tiempo, dim_geografia, fact_irca, DB_URI)
        
        print("\n=========================================")
        print(" PIPELINE COMPLETADO EXITOSAMENTE ✔️")
        print("=========================================")
        
    except AssertionError as qa_error:
        print(f"\n[ERROR DE CALIDAD] El pipeline se detuvo preventivamente: {qa_error}")
    except FileNotFoundError:
        print(f"\n[ERROR] No se encuentra el archivo fuente en: {FILE_PATH}. Verifica que exista.")
    except Exception as e:
        print(f"\n[ERROR CRÍTICO] Hubo una falla técnica: {e}")

if __name__ == "__main__":
    run_pipeline()
