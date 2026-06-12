"""fix_tables_macros_indicators_id_sequence

Revision ID: c86b15737c56
Revises: ccb59cb90494
Create Date: 2026-06-09 18:51:09.752192

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c86b15737c56'
down_revision: Union[str, None] = 'ccb59cb90494'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


MACRO_TABLES = [
    "t_macro_bce_mro",
    "t_macro_bce_inflation",
    "t_macro_bce_unemployment",
    "t_macro_bce_monetary_m3",
]


def upgrade() -> None:
    """Upgrade schema: create id sequences for macro indicator tables."""
    for table_name in MACRO_TABLES:
        sequence_name = f"{table_name}_id_seq"

        op.execute(
            f"CREATE SEQUENCE IF NOT EXISTS {sequence_name} START WITH 1 INCREMENT BY 1;"
        )

        op.execute(
            f"""
            SELECT setval(
                '{sequence_name}',
                COALESCE((SELECT MAX(id) FROM {table_name}), 0) + 1,
                false
            );
            """
        )

        op.execute(
            f"ALTER TABLE {table_name} ALTER COLUMN id SET DEFAULT nextval('{sequence_name}');"
        )

        op.execute(
            f"ALTER SEQUENCE {sequence_name} OWNED BY {table_name}.id;"
        )


def downgrade() -> None:
    """Downgrade schema: remove id sequences from macro indicator tables."""
    for table_name in MACRO_TABLES:
        sequence_name = f"{table_name}_id_seq"

        op.execute(
            f"ALTER TABLE {table_name} ALTER COLUMN id DROP DEFAULT;"
        )

        op.execute(
            f"DROP SEQUENCE IF EXISTS {sequence_name};"
        )
