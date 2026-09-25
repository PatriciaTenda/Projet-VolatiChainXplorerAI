| Variable                | Rôle                    | Définition / calcul                                                  | Type     | Unité                   |
| ----------------------- | ----------------------- | -------------------------------------------------------------------- | -------- | ----------------------- |
| `date`                  | Identifiant temporel    | Date de l’observation                                                | datetime | jour                    |
| `log_return`            | Feature                 | `ln(close_t / close_t-1)`                                            | float    | rendement logarithmique |
| `volatility_3d`         | Feature                 | Écart-type des rendements sur les 3 derniers jours                   | float    | volatilité              |
| `volatility_7d`         | Feature                 | Écart-type des rendements sur les 7 derniers jours                   | float    | volatilité              |
| `volatility_14d`        | Feature                 | Écart-type des rendements sur les 14 derniers jours                  | float    | volatilité              |
| `volatility_30d`        | Feature                 | Écart-type des rendements sur les 30 derniers jours                  | float    | volatilité              |
| `daily_range`           | Feature                 | `(high - low) / close`                                               | float    | variation relative      |
| `volume_change`         | Feature                 | Variation relative quotidienne du volume                             | float    | taux de variation       |
| `market_cap_change`     | Feature                 | Variation relative quotidienne de la capitalisation                  | float    | taux de variation       |
| `rate_mro`              | Feature macroéconomique | Taux directeur des opérations principales de refinancement de la BCE | float    | %                       |
| `inflation_rate`        | Feature macroéconomique | Taux d’inflation                                                     | float    | %                       |
| `unemployment_rate`     | Feature macroéconomique | Taux de chômage                                                      | float    | %                       |
| `monetary_m3_rate`      | Feature macroéconomique | Taux de variation de l’agrégat monétaire M3                          | float    | %                       |
| `log_return_lag_1d`     | Feature retardée        | Rendement logarithmique observé 1 jour auparavant                    | float    | rendement               |
| `log_return_lag_7d`     | Feature retardée        | Rendement logarithmique observé 7 jours auparavant                   | float    | rendement               |
| `log_return_lag_30d`    | Feature retardée        | Rendement logarithmique observé 30 jours auparavant                  | float    | rendement               |
| `target_volatility_7d`  | Cible                   | Écart-type des rendements des 7 jours futurs non anualisés          | float    | volatilité              |
| `target_volatility_30d` | Cible                   | Écart-type des rendements des 30 jours futurs non annualisés         | float    | volatilité              |
