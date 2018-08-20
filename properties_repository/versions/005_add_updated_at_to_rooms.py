from sqlalchemy import Table, MetaData, String, Column, Float, DateTime, Integer

meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    rooms = Table('rooms', meta, autoload=True)
    updated_at_c = Column('updated_at', DateTime)
    external_id = Column('external_id', Integer)
    updated_at_c.create(rooms)
    external_id.create(rooms)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    rooms = Table('rooms', meta, autoload=True)
    rooms.c.updated_at.drop()
    rooms.c.external_id.drop()
