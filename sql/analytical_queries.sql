-- ==========================================
-- SCRIPT: CONSULTAS ANALÍTICAS (R1 A R5)
-- ==========================================

-- R1: Cambio histórico del nivel de riesgo del agua a nivel nacional desde 2007.
SELECT 
    t.anio, 
    ROUND(AVG(f.irca_urbano), 2) as prom_irca_urbano, 
    ROUND(AVG(f.irca_rural), 2) as prom_irca_rural
FROM fact_irca f
JOIN dim_tiempo t ON f.fk_tiempo = t.sk_tiempo
GROUP BY t.anio
ORDER BY t.anio ASC;


-- R2: Identificar los (Top 5) departamentos que presentan el peor índice de calidad de agua en la actualidad.
SELECT 
    g.departamento,
    -- Se promedia urbano y rural para un consolidado departamental
    ROUND(AVG((COALESCE(f.irca_urbano, 0) + COALESCE(f.irca_rural, 0)) / 2), 2) AS prom_riesgo_total
FROM fact_irca f
JOIN dim_geografia g ON f.fk_geografia = g.sk_geografia
JOIN dim_tiempo t ON f.fk_tiempo = t.sk_tiempo
WHERE t.anio = (SELECT MAX(anio) FROM dim_tiempo)
GROUP BY g.departamento
ORDER BY prom_riesgo_total DESC
LIMIT 5;


-- R3: Comparar el nivel de riesgo del agua entre la zona urbana y rural dentro de cada departamento.
SELECT 
    g.departamento,
    ROUND(AVG(f.irca_urbano), 2) as prom_urbano,
    ROUND(AVG(f.irca_rural), 2) as prom_rural,
    ROUND(AVG(f.irca_rural) - AVG(f.irca_urbano), 2) as brecha_riesgo
FROM fact_irca f
JOIN dim_geografia g ON f.fk_geografia = g.sk_geografia
GROUP BY g.departamento
ORDER BY brecha_riesgo DESC;


-- R4: Detectar los municipios que se han mantenido en "alto riesgo" de forma constante en los últimos 5 años.
-- Nota de negocio: IRCA > 35 se considera 'Alto Riesgo' e 'Inviable Sanitariamente'.
SELECT 
    g.departamento,
    g.municipio,
    COUNT(t.anio) as mediciones_alta_peligrosidad
FROM fact_irca f
JOIN dim_geografia g ON f.fk_geografia = g.sk_geografia
JOIN dim_tiempo t ON f.fk_tiempo = t.sk_tiempo
WHERE f.irca_rural > 35 
  AND t.anio >= ((SELECT MAX(anio) FROM dim_tiempo) - 4) -- Últimos 5 años incluyentes
GROUP BY g.departamento, g.municipio
HAVING COUNT(t.anio) = 5;


-- R5: Medir qué departamentos han logrado reducir más su riesgo de agua rural a lo largo del tiempo.
WITH min_anio AS (
    SELECT g.departamento, AVG(f.irca_rural) as irca_base
    FROM fact_irca f
    JOIN dim_geografia g ON f.fk_geografia = g.sk_geografia
    JOIN dim_tiempo t ON f.fk_tiempo = t.sk_tiempo
    WHERE t.anio = (SELECT MIN(anio) FROM dim_tiempo)
    GROUP BY g.departamento
),
max_anio AS (
    SELECT g.departamento, AVG(f.irca_rural) as irca_actual
    FROM fact_irca f
    JOIN dim_geografia g ON f.fk_geografia = g.sk_geografia
    JOIN dim_tiempo t ON f.fk_tiempo = t.sk_tiempo
    WHERE t.anio = (SELECT MAX(anio) FROM dim_tiempo)
    GROUP BY g.departamento
)
SELECT 
    a.departamento,
    ROUND(a.irca_base, 2) AS riesgo_base,
    ROUND(b.irca_actual, 2) AS riesgo_actual,
    ROUND(b.irca_actual - a.irca_base, 2) AS progreso_absoluto
FROM min_anio a
JOIN max_anio b ON a.departamento = b.departamento
WHERE b.irca_actual - a.irca_base < 0 -- Filtra solo los que redujeron riesgo
ORDER BY progreso_absoluto ASC; -- Los más negativos (mayor reducción) primero
