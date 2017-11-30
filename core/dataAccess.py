# Author: Vincent.chan
# Blog: http://blog.alys114.com


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class dbProxy():
	def __init__(self,engine):
		self.engine =engine
		self.Base = declarative_base()  # 生成orm基类
		# 生成session实例
		self.db_session = sessionmaker(bind=self.engine)()

	def close(self):
		self.db_session.close()