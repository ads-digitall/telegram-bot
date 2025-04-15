from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cd324a36214'
down_revision = '<предыдущая_ревизия>'  # Укажи свою предыдущую ревизию
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        sa.Column('subscription_status', sa.String(), nullable=True, server_default='free')
    )


def downgrade():
    op.drop_column('users', 'subscription_status')
