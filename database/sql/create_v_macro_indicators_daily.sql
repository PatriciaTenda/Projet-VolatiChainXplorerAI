-- public.v_macro_indicators_daily_v1 source

CREATE OR REPLACE VIEW public.v_macro_indicators_daily_v1
AS WITH bounds AS (
         SELECT '2010-07-14'::date AS start_date,
            (date_trunc(
            'month'::text, 
            GREATEST(
                  COALESCE(
                  ( SELECT max(t_macro_bce_mro.date) AS max
                        FROM t_macro_bce_mro), '2010-07-14'::date), COALESCE(( SELECT max(t_macro_bce_inflation.date) AS max
                        FROM t_macro_bce_inflation), '2010-07-14'::date), COALESCE(( SELECT max(t_macro_bce_unemployment.date) AS max
                        FROM t_macro_bce_unemployment), '2010-07-14'::date), COALESCE(( SELECT max(t_macro_bce_monetary_m3.date) AS max
                        FROM t_macro_bce_monetary_m3), '2010-07-14'::date))::timestamp with time zone) + '1 mon -1 days'::interval)::date AS end_date
            ), calendar AS (
                  SELECT generate_series(bounds.start_date::timestamp with time zone, bounds.end_date::timestamp with time zone, '1 day'::interval)::date AS date
                  FROM bounds
                  )
            SELECT calendar.date,
            mro.value AS rate_mro,
            inf.value AS inflation_rate,
            unemp.value AS unemployment_rate,
            m3.value AS monetary_m3_rate
            FROM calendar
            LEFT JOIN LATERAL ( 
                        SELECT mro_daily.value
                        FROM t_macro_bce_mro mro_daily
                        WHERE mro_daily.date <= calendar.date
                        ORDER BY mro_daily.date DESC
                        LIMIT 1
                  ) mro ON true
            LEFT JOIN LATERAL ( 
                        SELECT inflation_monthly.value
                        FROM t_macro_bce_inflation inflation_monthly
                        WHERE inflation_monthly.date <= calendar.date
                        ORDER BY inflation_monthly.date DESC
                        LIMIT 1
                  ) inf ON true
            LEFT JOIN LATERAL ( 
                        SELECT unemployment_monthly.value
                        FROM t_macro_bce_unemployment unemployment_monthly
                        WHERE unemployment_monthly.date <= calendar.date
                        ORDER BY unemployment_monthly.date DESC
                        LIMIT 1
                  ) unemp ON true
            LEFT JOIN LATERAL (
                        SELECT m3_monthly.value
                        FROM t_macro_bce_monetary_m3 m3_monthly
                        WHERE m3_monthly.date <= calendar.date
                        ORDER BY m3_monthly.date DESC
                        LIMIT 1
                  ) m3 ON true
            ORDER BY calendar.date;