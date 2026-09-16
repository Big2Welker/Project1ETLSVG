# Esquema Estrella (Star Schema)

El modelo dimensional implementado para dar respuesta a los requerimientos analíticos (R1-R5). Centraliza las medidas numéricas del IRCA y las aisla en dimensiones geográficas y temporales.

```mermaid
erDiagram
    Dim_Geografia ||--o{ Fact_IRCA : "Filtra (1:N)"
    Dim_Tiempo ||--o{ Fact_IRCA : "Filtra (1:N)"

    Dim_Geografia {
        int sk_geografia PK "Clave Sustituta"
        string departamento
        string municipio
    }
    
    Dim_Tiempo {
        int sk_tiempo PK "Clave Sustituta"
        int anio
    }
    
    Fact_IRCA {
        int fk_geografia FK, PK
        int fk_tiempo FK, PK
        float irca_urbano "Medida"
        float irca_rural "Medida"
    }
```
