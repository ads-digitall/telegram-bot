from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3csdv5a5sefg'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('interests', sa.ARRAY(sa.Text())))

def downgrade():
    op.drop_column('users', 'interests')
