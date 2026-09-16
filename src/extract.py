import pandas as pd

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Lee el conjunto de datos original desde la carpeta data/raw/
    No aplica reglas de negocio.
    """
    print(f"[EXTRACT] Adquiriendo datos crudos desde: {file_path}")
    # Retorna DataFrame ignorando errores de codificación menores
    df_raw = pd.read_csv(file_path, encoding='utf-8')
    return df_raw
