import sqlalchemy as sa

engine = sa.create_engine('sqlite:///Broni.db')
meta = sa.MetaData()


Broni = sa.Table("PC",
                 meta,
                 sa.Column("id", sa.Integer, primary_key=True),
                 sa.Column("value", sa.String, default="N/A"))
