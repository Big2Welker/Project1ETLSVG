import pandas as pd
import numpy as np

def prepare_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Ejecuta la estrategia de preparación: filtros de grano, tipos de dato y estandarización.
    """
    print("[TRANSFORM - PREP] Limpiando y estandarizando datos...")
    df_clean = df_raw.copy()
    
    # 1. Aislar grano atómico (Eliminar agregaciones departamentales)
    if 'Municipio' in df_clean.columns:
        df_clean = df_clean[df_clean['Municipio'] != '#TODOS']
    
    # 2. Estandarizar textos geográficos
    if 'Departamento' in df_clean.columns:
        df_clean['Departamento'] = df_clean['Departamento'].str.strip().str.upper()
    if 'Municipio' in df_clean.columns:
        df_clean['Municipio'] = df_clean['Municipio'].str.strip().str.upper()

    # 3. Tratamiento de nulos y casteo de métricas (Hechos)
    for col in ['IRCAurbano', 'IRCArural']:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].replace('ND', np.nan)
            df_clean[col] = (df_clean[col].astype(str)
                             .str.replace(',', '.', regex=False)
                             .replace(['nan', 'ND'], np.nan)
                             .astype(float))
        
    # 4. Formato de Fechas
    if 'Año' in df_clean.columns:
        df_clean['Año'] = df_clean['Año'].astype(str).str.replace(r'[,\.]', '', regex=True).astype(int)
    
    return df_clean
