-- public.v_bitcoin_macro_indicator_daily source

CREATE OR REPLACE VIEW public.v_bitcoin_macro_indicator_daily
AS SELECT btc.date AS day,
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
   FROM t_bitcoin_prices btc
     LEFT JOIN v_macro_indicators_daily_v1 macro ON macro.date = btc.date;