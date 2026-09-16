import pandas as pd
from sqlalchemy import create_engine, text

def load_warehouse(dim_tiempo: pd.DataFrame, dim_geo: pd.DataFrame, fact_irca: pd.DataFrame, db_uri: str):
    print(f"[LOAD] Conectando a Data Warehouse...")
    engine = create_engine(db_uri)
    
    # DDL Estricto: Borra tablas viejas, crea estructura con PRIMARY KEY y FOREIGN KEY
    ddl = """
    DROP TABLE IF EXISTS fact_irca;
    DROP TABLE IF EXISTS dim_geografia;
    DROP TABLE IF EXISTS dim_tiempo;

    CREATE TABLE dim_tiempo (
        sk_tiempo INT PRIMARY KEY,
        anio INT NOT NULL
    );

    CREATE TABLE dim_geografia (
        sk_geografia INT PRIMARY KEY,
        departamento VARCHAR(150) NOT NULL,
        municipio VARCHAR(150) NOT NULL
    );

    CREATE TABLE fact_irca (
        fk_geografia INT,
        fk_tiempo INT,
        irca_urbano DECIMAL(6,2),
        irca_rural DECIMAL(6,2),
        PRIMARY KEY (fk_geografia, fk_tiempo),
        FOREIGN KEY (fk_geografia) REFERENCES dim_geografia(sk_geografia),
        FOREIGN KEY (fk_tiempo) REFERENCES dim_tiempo(sk_tiempo)
    );
    """
    
    with engine.begin() as conn:
        print("[LOAD] Inyectando esquema de tablas con sus restricciones (PK/FK)...")
        # Separar comandos por ; e inyectar
        for statement in ddl.split(';'):
            if statement.strip():
                conn.execute(text(statement.strip()))
        
        print("[LOAD] Insertando datos en las dimensiones...")
        # Usamos if_exists='append' para que Pandas respete nuestras llaves primarias
        dim_tiempo.to_sql('dim_tiempo', conn, if_exists='append', index=False)
        dim_geo.to_sql('dim_geografia', conn, if_exists='append', index=False)
        
        print("[LOAD] Insertando datos en la tabla de hechos...")
        fact_irca.to_sql('fact_irca', conn, if_exists='append', index=False)
        
    print("[LOAD] -> Carga en Base de Datos finalizada con éxito. ¡Modelo Estrella íntegro!")
