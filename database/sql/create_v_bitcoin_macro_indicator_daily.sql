CREATE OR REPLACE VIEW public.v_bitcoin_macro_indicator_daily AS
SELECT
    btc.date AS day,
    btc.open,
    btc.high,
    btc.low,
    btc.close,
    btc.volume,
    btc.market_cap,
    macro.rate_mro,
    macro.inflation_rate,
    macro.unemployment_rate,
    macro.monetary_m3_rate
FROM public.t_bitcoin_prices AS btc
LEFT JOIN public.v_macro_indicators_daily_v1 AS macro
    ON macro.date = btc.date;