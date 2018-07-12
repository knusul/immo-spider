from sqlalchemy import Table, MetaData, String, Column, Float


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    properties = Table('properties', meta, autoload=True)
    lat = Column('lat', Float)
    lon = Column('lon', Float)
    source = Column('source', String(255))
    lat.create(properties)
    lon.create(properties)
    source.create(properties)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    properties = Table('properties', meta, autoload=True)
    properties.c.lat.drop()
    properties.c.lon.drop()
    properties.c.source.drop()
