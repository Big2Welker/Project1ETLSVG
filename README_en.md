# ETL Project: Data Engineering for Sustainable Development in Colombia

## 1. Colombian Problem Definition and SDGs
* **Title:** Dimensional Analysis of Drinking Water Quality Inequality (IRCA) in Colombia.
* **Selected SDG:** SDG 6 - Clean Water and Sanitation (Target 6.1: Universal and equitable access to safe and affordable drinking water).
* **Colombian Problem:** There is a historical gap in the provision of public services between major urban centers and rural areas. While main cities report IRCA (Water Quality Risk Index) levels categorized as "No risk," a large number of remote municipalities consume water with medium, high, or sanitarily unviable risk levels.
* **Technical Context (What is IRCA?):** The Water Quality Risk Index is expressed from 0% to 100%:
  * **0% – 5%:** No risk (Safe water).
  * **5.1% – 14%:** Low risk.
  * **14.1% – 35%:** Medium risk.
  * **35.1% – 80%:** High risk.
  * **80.1% – 100%:** Sanitarily unviable.
* **Stakeholders:** Ministry of Health, Superintendency of Public Services, Governorates, Mayoralties, and NGOs.

## 2. Analytical Requirements Matrix (R1-R5)

| ID | Analytical Requirement | Business Question | Decision / Supported Knowledge |
| :--- | :--- | :--- | :--- |
| **R1** | Analyze the historical change in water risk levels nationwide since 2007. | Has water quality in Colombia improved or worsened over the years? | Evaluate if national health and infrastructure policies are yielding results. |
| **R2** | Identify the departments with the worst water quality index currently. | Which departments have the most dangerous water today? | Prioritize national budget allocation and emergency aid to critical regions. |
| **R3** | Compare water risk levels between urban and rural areas within each department. | How large is the inequality between rural and urban areas in the same region? | Focus aqueducts and treatment plants specifically on neglected rural areas. |
| **R4** | Detect municipalities maintained at constant "high risk" levels over the last 5 years. | Which municipalities have been consuming unsafe water for years without improvement? | Intervene in responsible mayoralties to demand urgent sanitation plans. |
| **R5** | Measure which departments have managed to reduce their rural water risk the most over time. | Which departments achieved the greatest improvement in rural water quality? | Identify governmental success stories to replicate their strategies in other territories. |

## 3. Dataset Selection and Evaluation
* **Institution / Owner:** National Institute of Health (INS) - datos.gov.co.
* **Coverage:** National (Departments and Municipalities) and Temporal (2007 - Present).
* **URL / Acquisition:** Official CSV file. Stored locally at `data/raw/Calidad_del_Agua_para_Consumo_Humano_en_Colombia_20260905.csv`.

## 4. Requirements-to-Data Traceability

| Requirement | Required Attributes | Necessary Transformation | Expected KPI / Analysis |
| :--- | :--- | :--- | :--- |
| **R1** | `Año`, `IRCAurbano`, `IRCArural` | Clean `Año` (cast to int). Replace "ND" nulls. Cast metrics to `float`. | Line chart. KPI: National Average IRCA. |
| **R2** | `Departamento`, `Año`, `IRCAurbano`, `IRCArural` | Filter `Municipio = '#TODOS'`. Filter by the maximum current year. | Horizontal bar chart (Top 5 worst departments). |
| **R3** | `Departamento`, `IRCAurbano`, `IRCArural` | Exclude `#TODOS` aggregations. Derivation (Rural - Urban). | Clustered column chart. KPI: Risk Gap. |
| **R4** | `Municipio`, `Año`, `IRCArural` | Clean `Año`. Filter `Año >= (Max-5)`. Classification > 35%. | Heatmap/Matrix (Count of critical municipalities). |
| **R5** | `Departamento`, `Año`, `IRCArural` | Filter `#TODOS`. Handle "ND" to `NaN`. Calculate temporal Delta. | Ascending bar chart (Historical Delta). |

## 5. Data Preparation Strategy and Profiling
Severe structural anomalies were detected during Data Profiling:
* **Mixed Granularity:** Removal of rows where `Municipio = '#TODOS'` to prevent double counting and ensure an atomic grain.
* **Covert Nulls:** Strict replacement of the string `"ND"` with actual nulls (`NaN`) to avoid biasing mathematical averages.
* **Format Contamination:** Removal of commas and thousands separators in years and measures, transforming them into native `float` and `int` types.

## 6. Grain Declaration and System Architecture
* **Grain:** "One row in `Fact_IRCA` represents the consolidated annual measurement of the Water Quality Risk Index (IRCA), differentiated by urban and rural zones, for a specific municipality in Colombia."
* **Business Process:** Measurement of drinking water safety.
* *(See ETL Architecture diagram in `docs/ETL_Architecture.md`)*

## 7. Star Schema and Justification
* *(See ER Diagram in `docs/Star_Schema.md`)*
* `Dim_Tiempo`: Required for historical groupings (R1, R4, R5).
* `Dim_Geografia`: Denormalized for fluid territorial analysis (R2, R3).
* `Fact_IRCA`: Centralizes numerical measures. Composite primary key to enforce the grain.

## 8. Requirements Validation against the Dimensional Model

| Requirement | Dimension(s) | Measure(s) | Expected Query/KPI | Supported? |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | `Dim_Tiempo` | `irca_urbano`, `irca_rural` | `AVG(irca)` grouped by `anio` (Line chart) | Yes |
| **R2** | `Dim_Geografia`, `Dim_Tiempo` | `irca_urbano`, `irca_rural` | Top 5 `AVG(irca)` by `departamento` where year = MAX | Yes |
| **R3** | `Dim_Geografia` | `irca_urbano`, `irca_rural` | `AVG(rural) - AVG(urbano)` grouped by `departamento` | Yes |
| **R4** | `Dim_Geografia`, `Dim_Tiempo` | `irca_rural` | Count grouped by `municipio` where `irca > 35` (5 years) | Yes |
| **R5** | `Dim_Geografia`, `Dim_Tiempo` | `irca_rural` | Delta `AVG(irca_rural)` Max Year vs Min Year by `departamento` | Yes |

## 9. Data Warehouse Implementation and Reproduction
1. Virtual environment: `pip install pandas numpy sqlalchemy pymysql python-dotenv`
2. Configure the `.env` file at the root with MySQL credentials (port 3306).
3. Ensure the dataset is in `data/raw/`.
4. Run orchestrator: `python src/main.py`. *(Automatically creates the `dw_calidad_agua_colombia` DB, tables with PK/FK constraints, and loads data).*

## 10. Analytical Queries (SQL) and Business Intelligence
* Documented SQL queries are located in `sql/analytical_queries.sql`.
* The **Power BI Dashboard** connects directly to the MySQL DW and incorporates:
  * Specific DAX measures for analyzing the Urban-Rural Gap and the Historical Progress of risk reduction.
  * Structured charts and visualizations to provide exact answers for each requirement (R1-R5).

## 11. Key Findings
1. **Systemic Inequality:** The "gap" between rural and urban areas is positively wide in the vast majority of departments.
2. **Continuous Alert Hotspots:** Peripheral departments have remained in "High Risk" levels uninterruptedly over the last five years.
3. **Success Stories:** Central regions show the largest reductions (negative deltas) in rural IRCA, setting the standard for public policies.

## 12. Team Members
* **Sebastian Rojas Herrera and Juan David Bedoya** - Role: Data Engineer / BI Analyst.
