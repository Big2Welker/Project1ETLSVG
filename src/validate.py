import pandas as pd

def validate_model(df_clean: pd.DataFrame, dim_tiempo: pd.DataFrame, dim_geo: pd.DataFrame, fact_irca: pd.DataFrame):
    """
    Aplica aserciones de Calidad (QA), Unicidad e Integridad Referencial.
    """
    print("[VALIDATE] Comprobando reglas de integridad...")
    
    # 1. Unicidad de las Claves Primarias (PK)
    assert dim_tiempo['sk_tiempo'].is_unique, "Fallo QA: PK duplicada en dim_tiempo"
    assert dim_geo['sk_geografia'].is_unique, "Fallo QA: PK duplicada en dim_geografia"
    
    # 2. Integridad Referencial (Las FK existen en las dimensiones)
    assert fact_irca['fk_tiempo'].isin(dim_tiempo['sk_tiempo']).all(), "Fallo QA: Clave Foránea de Tiempo no válida"
    assert fact_irca['fk_geografia'].isin(dim_geo['sk_geografia']).all(), "Fallo QA: Clave Foránea de Geografía no válida"
    
    # 3. Conciliación de carga (Misma cantidad de datos a cargar que los limpiados)
    assert len(fact_irca) == len(df_clean), "Fallo QA: Se perdieron filas durante el JOIN dimensional"
    
    print("[VALIDATE] -> Validación aprobada. Modelo listo para inserción.")
