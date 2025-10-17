CREATE TABLE IF NOT EXISTS `INTEGRATION.integration_prueba_tecnica` (
    PriceArea STRING,
    HourUTC TIMESTAMP,
    SpotPriceDKK FLOAT64,
    SpotPriceEUR FLOAT64,
    transform_date DATE
);

MERGE `INTEGRATION.integration_prueba_tecnica` T
USING (
    SELECT
        PriceArea,
        TIMESTAMP(HourUTC) AS HourUTC,
        SpotPriceDKK,
        SpotPriceEUR,
        CURRENT_DATE() AS transform_date
    FROM (
        SELECT *,
            ROW_NUMBER() OVER (PARTITION BY PriceArea, HourUTC ORDER BY ingest_timestamp DESC) AS rn
        FROM `core-veld-475310-u0.SANDBOX_apidata.elspot_prices`
    )
    WHERE rn = 1
=======
MERGE `core-veld-475310-u0.INTEGRATION.integration_prueba_tecnica` T
USING (
  SELECT
    PriceArea,
    HourUTC,
    SpotPriceDKK,
    SpotPriceEUR,
    CURRENT_DATE() AS transform_date
  FROM (
    SELECT *,
      ROW_NUMBER() OVER (PARTITION BY PriceArea, HourUTC ORDER BY ingest_timestamp DESC) AS rn
    FROM `core-veld-475310-u0.SANDBOX_apidata.elspot_prices`
  )
  WHERE rn = 1
>>>>>>> 113f7a1 (Todos)
) S
ON T.PriceArea = S.PriceArea AND T.HourUTC = S.HourUTC
WHEN MATCHED THEN
  UPDATE SET
    T.SpotPriceDKK = S.SpotPriceDKK,
    T.SpotPriceEUR = S.SpotPriceEUR,
    T.transform_date = S.transform_date
WHEN NOT MATCHED THEN
  INSERT (PriceArea, HourUTC, SpotPriceDKK, SpotPriceEUR, transform_date)
  VALUES (S.PriceArea, S.HourUTC, S.SpotPriceDKK, S.SpotPriceEUR, S.transform_date);
