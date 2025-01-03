"""empty message

Revision ID: 26e74bb7d56d
Revises: 
Create Date: 2024-12-22 16:00:34.382467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26e74bb7d56d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('objectives',
    sa.Column('objectiveId', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('parent_objectiveId', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['parent_objectiveId'], ['objectives.objectiveId'], ),
    sa.PrimaryKeyConstraint('objectiveId')
    )
    op.create_table('projects',
    sa.Column('projectId', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('projectId')
    )
    op.create_table('users',
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('registered', sa.Date(), nullable=True),
    sa.Column('is_mail_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('userId'),
    sa.UniqueConstraint('email')
    )
    op.create_table('email_verifications',
    sa.Column('verification_id', sa.UUID(), nullable=False),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.Column('verification_code', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['userId'], ['users.userId'], ),
    sa.PrimaryKeyConstraint('verification_id'),
    sa.UniqueConstraint('userId')
    )
    op.create_table('organizations',
    sa.Column('organizationId', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('leaderId', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['leaderId'], ['users.userId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('organizationId')
    )
    op.create_table('user_profiles',
    sa.Column('userProfileId', sa.UUID(), nullable=False),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('patronymic', sa.String(), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['userId'], ['users.userId'], ),
    sa.PrimaryKeyConstraint('userProfileId')
    )
    op.create_table('teams',
    sa.Column('teamId', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('leaderId', sa.UUID(), nullable=True),
    sa.Column('organizationId', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['leaderId'], ['users.userId'], ),
    sa.ForeignKeyConstraint(['organizationId'], ['organizations.organizationId'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('teamId')
    )
    op.create_table('team_invitations',
    sa.Column('teamInvitationId', sa.UUID(), nullable=False),
    sa.Column('invited_user_id', sa.UUID(), nullable=False),
    sa.Column('invited_by_leader_id', sa.UUID(), nullable=False),
    sa.Column('teamId', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['invited_by_leader_id'], ['users.userId'], ),
    sa.ForeignKeyConstraint(['invited_user_id'], ['users.userId'], ),
    sa.ForeignKeyConstraint(['teamId'], ['teams.teamId'], ),
    sa.PrimaryKeyConstraint('teamInvitationId')
    )
    op.create_table('team_members',
    sa.Column('teamMemberId', sa.UUID(), nullable=False),
    sa.Column('userId', sa.UUID(), nullable=False),
    sa.Column('teamId', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['teamId'], ['teams.teamId'], ),
    sa.ForeignKeyConstraint(['userId'], ['users.userId'], ),
    sa.PrimaryKeyConstraint('teamMemberId')
    )
    op.create_table('team_projects',
    sa.Column('teamProjectId', sa.UUID(), nullable=False),
    sa.Column('teamId', sa.UUID(), nullable=False),
    sa.Column('projectId', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['projectId'], ['projects.projectId'], ),
    sa.ForeignKeyConstraint(['teamId'], ['teams.teamId'], ),
    sa.PrimaryKeyConstraint('teamProjectId')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team_projects')
    op.drop_table('team_members')
    op.drop_table('team_invitations')
    op.drop_table('teams')
    op.drop_table('user_profiles')
    op.drop_table('organizations')
    op.drop_table('email_verifications')
    op.drop_table('users')
    op.drop_table('projects')
    op.drop_table('objectives')
    # ### end Alembic commands ###
