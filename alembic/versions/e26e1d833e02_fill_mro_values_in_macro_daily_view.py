"""fill mro values in macro daily view

Revision ID: e26e1d833e02
Revises: c86b15737c56
Create Date: 2026-06-12 06:21:12.536663

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'e26e1d833e02'
down_revision: Union[str, None] = 'c86b15737c56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rebuild macro daily view with last known MRO value per day."""
    op.execute(
        """
        CREATE OR REPLACE VIEW v_macro_indicators_daily_v1 AS
        WITH bounds AS (
            SELECT
                DATE '2010-07-14' AS start_date,
                GREATEST(
                    COALESCE((SELECT MAX(date) FROM t_macro_bce_mro), DATE '2010-07-14'),
                    COALESCE((SELECT MAX(date) FROM t_macro_bce_inflation), DATE '2010-07-14'),
                    COALESCE((SELECT MAX(date) FROM t_macro_bce_unemployment), DATE '2010-07-14'),
                    COALESCE((SELECT MAX(date) FROM t_macro_bce_monetary_m3), DATE '2010-07-14')
                ) AS end_date
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


def downgrade() -> None:
    """Restore previous month-based macro daily view."""
    op.execute(
        """
        CREATE OR REPLACE VIEW v_macro_indicators_daily_v1 AS
        SELECT 
            COALESCE(mro.date, inf.date, unemp.date, m3.date) AS date,
            mro.value AS rate_mro,
            inf.value AS inflation_rate,
            unemp.value AS unemployment_rate,
            m3.value AS monetary_m3_rate
        FROM t_macro_bce_mro mro
        FULL OUTER JOIN t_macro_bce_inflation inf 
            ON DATE_TRUNC('month', mro.date) = DATE_TRUNC('month', inf.date)
        FULL OUTER JOIN t_macro_bce_unemployment unemp 
            ON DATE_TRUNC('month', COALESCE(mro.date, inf.date)) = DATE_TRUNC('month', unemp.date)
        FULL OUTER JOIN t_macro_bce_monetary_m3 m3 
            ON DATE_TRUNC('month', COALESCE(mro.date, inf.date, unemp.date)) = DATE_TRUNC('month', m3.date)
        WHERE COALESCE(mro.date, inf.date, unemp.date, m3.date) >= '2010-07-14'
        ORDER BY date;
        """
    )
