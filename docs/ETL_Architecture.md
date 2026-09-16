# ETL Architecture Pipeline

Este diagrama ilustra el flujo de datos desde la extracción del archivo crudo hasta su carga en el Data Warehouse, mostrando las transformaciones específicas aplicadas.

```mermaid
flowchart LR
    classDef source fill:#E2EFDA,stroke:#548235,stroke-width:2px,color:black
    classDef transform fill:#DDEBF7,stroke:#2E75B6,stroke-width:2px,color:black
    classDef validate fill:#FFF2CC,stroke:#D6B656,stroke-width:2px,color:black
    classDef load fill:#FCE4D6,stroke:#C55A11,stroke-width:2px,color:black

    A[(Fuente de Datos\nCSV)]:::source -->|Lectura| B(Extracción)
    subgraph 1. PREPARACIÓN
        B --> C[Eliminar\n#TODOS]:::transform
        C --> D[Limpiar 'ND'\ny Formatos]:::transform
    end
    subgraph 2. DIMENSIONAL
        D --> E[Crear Dimensiones\nTiempo y Geografía]:::transform
        E --> F[Mapear Claves FK\nFact_IRCA]:::transform
    end
    F --> G{Reglas de\nCalidad QA}:::validate
    subgraph 3. CARGA DW
        G -->|Si pasa validación| H[(MySQL)]:::load
        H --> I[Insertar Tablas\nRespetando PK/FK]:::load
    end
```
