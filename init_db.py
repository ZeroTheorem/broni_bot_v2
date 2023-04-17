import sqlalchemy as sa

engine = sa.create_engine('sqlite:///broni.db')
meta = sa.MetaData()


broni = sa.Table("PC",
                 meta,
                 sa.Column("id", sa.Integer, primary_key=True),
                 sa.Column("value", sa.String, default="N/A"),
                 sa.Column("actual_time", sa.String, default="N/A"))
