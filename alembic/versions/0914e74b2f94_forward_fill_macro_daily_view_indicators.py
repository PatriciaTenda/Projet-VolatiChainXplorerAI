"""forward fill macro daily view indicators

Revision ID: 0914e74b2f94
Revises: 74406a9e1813
Create Date: 2026-06-12 06:56:42.196170

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '0914e74b2f94'
down_revision: Union[str, None] = '74406a9e1813'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Forward-fill macro indicators in the daily view."""
    op.execute(
        """
        CREATE OR REPLACE VIEW v_macro_indicators_daily_v1 AS
        WITH bounds AS (
            SELECT
                DATE '2010-07-14' AS start_date,
                (
                    DATE_TRUNC(
                        'month',
                        GREATEST(
                            COALESCE((SELECT MAX(date) FROM t_macro_bce_mro), DATE '2010-07-14'),
                            COALESCE((SELECT MAX(date) FROM t_macro_bce_inflation), DATE '2010-07-14'),
                            COALESCE((SELECT MAX(date) FROM t_macro_bce_unemployment), DATE '2010-07-14'),
                            COALESCE((SELECT MAX(date) FROM t_macro_bce_monetary_m3), DATE '2010-07-14')
                        )
                    ) + INTERVAL '1 month - 1 day'
                )::date AS end_date
        ),
        calendar AS (
            SELECT generate_series(start_date, end_date, INTERVAL '1 day')::date AS date
            FROM bounds
        )
        SELECT
            calendar.date,
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
        """
    )


def downgrade() -> None:
    """Restore view limited to the common range of monthly indicators."""
    op.execute(
        """
        CREATE OR REPLACE VIEW v_macro_indicators_daily_v1 AS
        WITH bounds AS (
            SELECT
                DATE '2010-07-14' AS start_date,
                (
                    DATE_TRUNC(
                        'month',
                        LEAST(
                            (SELECT MAX(date) FROM t_macro_bce_inflation),
                            (SELECT MAX(date) FROM t_macro_bce_unemployment),
                            (SELECT MAX(date) FROM t_macro_bce_monetary_m3)
                        )
                    ) + INTERVAL '1 month - 1 day'
                )::date AS end_date
        ),
        calendar AS (
            SELECT generate_series(start_date, end_date, INTERVAL '1 day')::date AS date
            FROM bounds
        )
        SELECT
            calendar.date,
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
        LEFT JOIN t_macro_bce_inflation inf
            ON DATE_TRUNC('month', inf.date) = DATE_TRUNC('month', calendar.date)
        LEFT JOIN t_macro_bce_unemployment unemp
            ON DATE_TRUNC('month', unemp.date) = DATE_TRUNC('month', calendar.date)
        LEFT JOIN t_macro_bce_monetary_m3 m3
            ON DATE_TRUNC('month', m3.date) = DATE_TRUNC('month', calendar.date)
        ORDER BY calendar.date;
        """
    )
