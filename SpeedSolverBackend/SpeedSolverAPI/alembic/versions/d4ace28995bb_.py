"""empty message

Revision ID: d4ace28995bb
Revises: 6452a4cc13cd
Create Date: 2025-01-02 17:47:19.696673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4ace28995bb'
down_revision: Union[str, None] = '6452a4cc13cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('email_verifications_userId_key', 'email_verifications', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('email_verifications_userId_key', 'email_verifications', ['userId'])
    # ### end Alembic commands ###
