"""fix_bitcoin_prices_id_sequence

Revision ID: ccb59cb90494
Revises: 325ae849c379
Create Date: 2026-06-05 01:38:48.913222

"""
from typing import Sequence, Union

from alembic import op
# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccb59cb90494'
down_revision: Union[str, None] = '325ae849c379'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Create SEQUENCE for t_bitcoin_prices.id column."""
    # Créer la SEQUENCE pour auto-incrémenter la colonne id
    op.execute("CREATE SEQUENCE IF NOT EXISTS t_bitcoin_prices_id_seq START WITH 1 INCREMENT BY 1;")
    
    # Associer la SEQUENCE à la colonne id comme valeur par défaut
    op.execute("ALTER TABLE t_bitcoin_prices ALTER COLUMN id SET DEFAULT nextval('t_bitcoin_prices_id_seq');")
    
    # Associer la SEQUENCE à la colonne id (propriété)
    op.execute("ALTER SEQUENCE t_bitcoin_prices_id_seq OWNED BY t_bitcoin_prices.id;")


def downgrade() -> None:
    """Downgrade schema: Remove SEQUENCE from t_bitcoin_prices.id column."""
    # Retirer la valeur par défaut de la colonne id
    op.execute("ALTER TABLE t_bitcoin_prices ALTER COLUMN id DROP DEFAULT;")
    
    # Supprimer la SEQUENCE
    op.execute("DROP SEQUENCE IF EXISTS t_bitcoin_prices_id_seq;")
