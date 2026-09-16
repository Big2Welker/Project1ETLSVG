-- ==========================================
-- SCRIPT: CREATE DATA WAREHOUSE (MYSQL)
-- ==========================================

-- 0. CREAR BASE DE DATOS DEL PROYECTO
CREATE DATABASE IF NOT EXISTS dw_calidad_agua_colombia;
USE dw_calidad_agua_colombia;

-- Se borran en cascada inversa para no romper llaves foráneas
DROP TABLE IF EXISTS fact_irca;
DROP TABLE IF EXISTS dim_geografia;
DROP TABLE IF EXISTS dim_tiempo;

-- 1. DIMENSIÓN TIEMPO
CREATE TABLE dim_tiempo (
    sk_tiempo INT PRIMARY KEY,
    anio INT NOT NULL
);

-- 2. DIMENSIÓN GEOGRAFÍA
CREATE TABLE dim_geografia (
    sk_geografia INT PRIMARY KEY,
    departamento VARCHAR(150) NOT NULL,
    municipio VARCHAR(150) NOT NULL
);

-- 3. TABLA DE HECHOS (IRCA)
CREATE TABLE fact_irca (
    fk_geografia INT,
    fk_tiempo INT,
    irca_urbano DECIMAL(6,2),
    irca_rural DECIMAL(6,2),
    PRIMARY KEY (fk_geografia, fk_tiempo),
    FOREIGN KEY (fk_geografia) REFERENCES dim_geografia(sk_geografia),
    FOREIGN KEY (fk_tiempo) REFERENCES dim_tiempo(sk_tiempo)
);
