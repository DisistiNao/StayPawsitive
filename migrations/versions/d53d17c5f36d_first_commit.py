"""first commit

Revision ID: d53d17c5f36d
Revises: 
Create Date: 2024-10-01 10:01:58.067559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd53d17c5f36d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('credits', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=False),
    sa.Column('birthdate', sa.DateTime(), nullable=False),
    sa.Column('address', sa.String(length=64), nullable=False),
    sa.Column('cpf', sa.String(length=11), nullable=False),
    sa.Column('avatar', sa.String(length=100), nullable=False),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_address'), ['address'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_avatar'), ['avatar'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_birthdate'), ['birthdate'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_cpf'), ['cpf'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_phone'), ['phone'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('pet',
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('pet_type', sa.String(length=50), nullable=False),
    sa.Column('photo', sa.String(length=100), nullable=False),
    sa.Column('breed', sa.String(length=40), nullable=False),
    sa.Column('sex', sa.String(length=10), nullable=False),
    sa.Column('friendly', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('name', 'username')
    )
    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_pet_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_pet_username'), ['username'], unique=False)

    op.create_table('possible_pet_boarding',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('max_pets', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('possible_pet_boarding', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_possible_pet_boarding_username'), ['username'], unique=False)

    op.create_table('possible_walk',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('max_pets', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('start_hour', sa.Time(), nullable=False),
    sa.Column('end_hour', sa.Time(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('possible_walk', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_possible_walk_username'), ['username'], unique=False)

    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('pet_name', sa.String(length=64), nullable=False),
    sa.Column('boarding_id', sa.Integer(), nullable=True),
    sa.Column('walk_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['boarding_id'], ['possible_pet_boarding.id'], ),
    sa.ForeignKeyConstraint(['pet_name'], ['pet.name'], ),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.ForeignKeyConstraint(['walk_id'], ['possible_walk.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_service_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_service_username'), ['username'], unique=False)

    op.create_table('requested_service',
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('id_service', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['id_service'], ['service.id'], ),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('username', 'id_service')
    )
    with op.batch_alter_table('requested_service', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_requested_service_username'), ['username'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('requested_service', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_requested_service_username'))

    op.drop_table('requested_service')
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_service_username'))
        batch_op.drop_index(batch_op.f('ix_service_id'))

    op.drop_table('service')
    with op.batch_alter_table('possible_walk', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_possible_walk_username'))

    op.drop_table('possible_walk')
    with op.batch_alter_table('possible_pet_boarding', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_possible_pet_boarding_username'))

    op.drop_table('possible_pet_boarding')
    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_pet_username'))
        batch_op.drop_index(batch_op.f('ix_pet_name'))

    op.drop_table('pet')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_phone'))
        batch_op.drop_index(batch_op.f('ix_user_name'))
        batch_op.drop_index(batch_op.f('ix_user_email'))
        batch_op.drop_index(batch_op.f('ix_user_cpf'))
        batch_op.drop_index(batch_op.f('ix_user_birthdate'))
        batch_op.drop_index(batch_op.f('ix_user_avatar'))
        batch_op.drop_index(batch_op.f('ix_user_address'))

    op.drop_table('user')
    # ### end Alembic commands ###