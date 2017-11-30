# Author: Vincent.chan
# Blog: http://blog.alys114.com

import common
from initdb import *


class User(object):
	def __init__(self,dbproxy):
		self.db = dbproxy

	def Login(self, member):
		'''登录'''
		result = []
		password = common.md5Encode(member[2])
		login_user = None
		if member[0]==1:
			login_user = self.db.db_session.query(Student).filter(Student.login_user==member[1]).first()
		else:
			login_user = self.db.db_session.query(Teacher).filter(Teacher.login_user == member[1]).first()

		if login_user:
			if login_user.password == password:
				result = [True, 'login success..',login_user]
			else:
				result = [False, 'password not match..']
		else:
			result = [False, 'login_user is not exist..']

		return result

	def Register_Check_LoginUser(self,login_user):
		exist_user = self.db.db_session.query(Student).filter(Student.login_user == login_user).first()

		if exist_user:
			result = [False, 'login user is exist..']
		else:
			result = [True,'']
		return result

	def Register_Check_qq(self,qq):
		exist_user = self.db.db_session.query(Student).filter(Student.qq == qq).first()
		if exist_user:
			result = [False, 'qq is exist..']
		else:
			result = [True, '']
		return result

	def Register(self,stu):
		school = self.db.db_session.query(School).filter().first()
		stu.school = school
		passwd = common.md5Encode(stu.password)
		stu.password = passwd
		self.db.db_session.add(stu)
		self.db.db_session.commit()


class StudentRole(object):
	def __init__(self,student,dbproxy):
		self.stu = student
		self.db = dbproxy

class TeacherRole(object):
	def __init__(self,teacher,dbproxy):
		self.tec = teacher
		self.db = dbproxy

	def QueryClasses(self):
		pass

