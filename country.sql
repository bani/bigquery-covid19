SELECT
  location,
  admin,
  country,
  last_update,
  MAX(IFNULL(confirmed,0)) AS confirmed,
  MAX(IFNULL(deaths,0)) AS deaths,
  MAX(IFNULL(recovered,0)) AS recovered
FROM
  `bani.covid19.daily_reports`
GROUP BY 1, 2, 3, 4),
country_agg AS (
SELECT
  CASE
    WHEN REGEXP_CONTAINS(country, '.*China.*') THEN 'China'
    WHEN REGEXP_CONTAINS(country, '^US$') THEN 'United States'
    WHEN REGEXP_CONTAINS(country, 'Hong Kong') THEN 'Hong Kong SAR, China'
    WHEN REGEXP_CONTAINS(country, '^UK$') THEN 'United Kingdom'
    WHEN REGEXP_CONTAINS(country, '^Iran.*') THEN 'Iran, Islamic Rep.'
    WHEN REGEXP_CONTAINS(country, 'Korea, South') THEN 'Korea, Rep.'
    WHEN REGEXP_CONTAINS(country, 'South Korea') THEN 'Korea, Rep.'
    WHEN REGEXP_CONTAINS(country, 'Republic of Korea') THEN 'Korea, Rep.'
  ELSE
  country
END
  AS country,
  last_update,
  SUM(confirmed) AS confirmed,
  SUM(deaths) AS deaths,
  SUM(recovered) AS recovered
FROM
  dedup
GROUP BY 1, 2)
SELECT
country,
confirmed,
deaths,
recovered,
last_update,
MIN(last_update) OVER (PARTITION BY country) as first_case,
DATE_DIFF(last_update, MIN(last_update) OVER (PARTITION BY country), DAY) as days,
confirmed - IFNULL(LAG(confirmed) OVER (PARTITION BY country ORDER BY last_update),0) as confirmed_day,
deaths - IFNULL(LAG(deaths) OVER (PARTITION BY country ORDER BY last_update),0) as deaths_day,
recovered - IFNULL(LAG(recovered) OVER (PARTITION BY country ORDER BY last_update),0) as recovered_day
FROM
country_agg
