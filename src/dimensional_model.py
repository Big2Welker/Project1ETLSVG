import pandas as pd

def build_star_schema(df_clean: pd.DataFrame):
    """
    Construye las Tablas de Dimensiones y la Tabla de Hechos para el DW.
    """
    print("[TRANSFORM - DIM] Creando Esquema Estrella y Claves Sustitutas...")
    
    # --- DIM_TIEMPO ---
    dim_tiempo = df_clean[['Año']].drop_duplicates().sort_values('Año').reset_index(drop=True)
    dim_tiempo.insert(0, 'sk_tiempo', dim_tiempo.index + 1)
    dim_tiempo = dim_tiempo.rename(columns={'Año': 'anio'})
    
    # --- DIM_GEOGRAFIA ---
    dim_geo = df_clean[['Departamento', 'Municipio']].drop_duplicates().sort_values(['Departamento', 'Municipio']).reset_index(drop=True)
    dim_geo.insert(0, 'sk_geografia', dim_geo.index + 1)
    dim_geo = dim_geo.rename(columns={'Departamento': 'departamento', 'Municipio': 'municipio'})
    
    # --- FACT_IRCA ---
    # Cruzamos (JOIN) para heredar las Surrogate Keys
    fact = df_clean.merge(dim_tiempo, left_on='Año', right_on='anio', how='inner')
    fact = fact.merge(dim_geo, left_on=['Departamento', 'Municipio'], right_on=['departamento', 'municipio'], how='inner')
    
    fact_irca = fact[['sk_geografia', 'sk_tiempo', 'IRCAurbano', 'IRCArural']].rename(
        columns={
            'sk_geografia': 'fk_geografia', 
            'sk_tiempo': 'fk_tiempo', 
            'IRCAurbano': 'irca_urbano', 
            'IRCArural': 'irca_rural'
        }
    )
    
    return dim_tiempo, dim_geo, fact_irca
