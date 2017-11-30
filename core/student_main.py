# Author: Vincent.chan
# Blog: http://blog.alys114.com

'''学生子页面'''
import time,datetime
from sqlalchemy import func,desc
from business import StudentRole
from business import User
import common
from constConfig import *
from initdb import *


def checkIn(role):
	return classes_action(role,'C')

def classes_action(role,action):
	'''上课签到/上传作业'''
	print('上课的时间表'.center(center_width, '-'))
	for cls in role.stu.classes_list:
		print(cls)
		for cr in cls.classesRecords:
			print('|--',cr)
	choice = input('请选择签到的课时编号:（[q]退出）')
	if choice == 'q':
		return
	else:
		cur_classRecord = None
		for cls in role.stu.classes_list:
			for cr in cls.classesRecords:
				if cr.id == int(choice):
					cur_classRecord = cr
					break

		if cur_classRecord:
			input_checkDate = datetime.datetime.now()
			exist_record = None
			for sr in role.stu.studentRecords:
				if sr.classes_record_id == cur_classRecord.id:
					exist_record = sr
					break
			if exist_record:
				if action=='C':
					exist_record.checkDate = input_checkDate
				else:
					exist_record.status = 1
			else:
				if action=='C':
					new_record = StudentRecord(checkDate=input_checkDate,status=0)
				else:
					new_record = StudentRecord(status=1)
				new_record.student = role.stu
				new_record.classesRecord = cur_classRecord
				role.db.db_session.add(new_record)
			role.db.db_session.commit()
			if action=='C':
				print('签到成功...')
			else:
				print('上传作业成功...')
		else:
			common.errorPrompt('录入错误...')

def push_job(role):
	'''提交作业'''
	return classes_action(role,'P')

def queryScore(role):
	'''查询成绩'''
	for sr in role.stu.studentRecords:
		print(sr)

def queryScoreList(role):
	for cls in role.stu.classes_list:
		print(cls.name)
		data = (
		role.db.db_session.query(func.sum(StudentRecord.score).label('total'), StudentRecord.student_id, Student.name). \
		filter(StudentRecord.classes_record_id == ClassesRecord.id). \
		filter(StudentRecord.student_id == Student.id).filter(ClassesRecord.classes_id == cls.id)).group_by(
			StudentRecord.student_id).order_by(desc('total')).all()
		for d in data:
			print('|--',d.total,d.name)


def displayMenu(stu,db):
	role = StudentRole(stu,db)

	menu = ''
	menu += '[1]上课签到'.ljust(menu_width)
	menu += '[2]提交作业'.ljust(menu_width)
	menu += '[3]查看个人成绩'.ljust(menu_width)+os.linesep
	menu += '[4]查看成绩排名'.ljust(menu_width)
	# menu += '[88]修改密码'.ljust(menu_width)
	menu += '[99]退出'.ljust(menu_width)
	while True:

		common.menuDisplay(menu)
		choice = input('请录入菜单代码:')
		if choice == '99':
			break
		elif choice =='1':
			checkIn(role)
		elif choice =='2':
			push_job(role)
		elif choice =='3':
			queryScore(role)
		elif choice =='4':
			queryScoreList(role)
		elif choice == '5':
			cur_pwd = input('请录入旧密码:')
			new_pwd = input('请录入新密码:')
			User.Change_Password(stu.login_user,cur_pwd,new_pwd)
		else:
			pass

