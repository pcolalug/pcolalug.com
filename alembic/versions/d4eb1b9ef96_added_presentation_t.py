"""added presentation table

Revision ID: d4eb1b9ef96
Revises: None
Create Date: 2012-03-26 11:27:15.364498

"""

# revision identifiers, used by Alembic.
revision = 'd4eb1b9ef96'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('pk', sa.Integer(), nullable=False),
    sa.Column('user_pk', sa.Integer(), nullable=False),
    sa.Column('mimetype', sa.UnicodeText(), nullable=False),
    sa.Column('uid', sa.UnicodeText(), nullable=False),
    sa.Column('filename', sa.UnicodeText(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_pk'], ['user.pk'], ),
    sa.PrimaryKeyConstraint('pk')
    )
    op.add_column(u'presentation', sa.Column('presenter_pk', sa.Integer(), nullable=False))
    op.add_column(u'presentation', sa.Column('file_pk', sa.Integer(), nullable=True))
    op.drop_column(u'presentation', u'presenter')
    op.alter_column(u'presentation', u'date', 
               existing_type=postgresql.TIMESTAMP(), 
               nullable=False)
    ### end Alembic commands ###

def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file')
    op.drop_column(u'presentation', 'presenter_pk')
    op.drop_column(u'presentation', 'file_pk')
    op.add_column(u'presentation', sa.Column(u'presenter', sa.TEXT(), nullable=True))
    op.alter_column(u'presentation', u'date', 
               existing_type=postgresql.TIMESTAMP(), 
               nullable=True)
    ### end Alembic commands ###
