# Author: Vincent.chan
# Blog: http://blog.alys114.com

'''讲师子页面'''

import common
import time,os
from business import TeacherRole
from business import User
from constConfig import *
from initdb import *

def classesManage(role):
	'''创建班级'''
	while True:
		for c in role.tec.school.courses:
			print(c)
			for cls in c.classes_list:
				print('|--',cls)
		choice = input('请选择课程编号:([q]退出)')
		if choice=='q':
			break
		else:
			for c in role.tec.school.courses:
				if c.id == int(choice):
					cur_course = c
			if cur_course:
				input_name = input('班级名称:')
				input_period = input('学习周期:')
				input_openDate = input('开班日期(%Y-%m-%d):')
				new_classes = Classes(name=input_name, openDate=input_openDate
									  , period=input_period)
				new_classes.course = cur_course
				new_classes.teachers = [role.tec]
				role.db.db_session.add(new_classes)
				role.db.db_session.commit()

			else:
				common.errorPrompt('..录入错误..')

def addStu(role):
	while True:
		for cls in role.tec.classes_list:
			print(cls)
		choice = input('请选择班级编号:([q]退出)')
		if choice == 'q':
			break
		else:
			cur_cls = None
			for cls in role.tec.classes_list:
				if cls.id == int(choice):
					cur_cls = cls
			if cur_cls:
				input_qq = input('加入班级的学生QQ号:')
				stu = role.db.db_session.query(Student).filter(Student.qq == input_qq).first()
				if stu:
					try:
						if cur_cls.students.index(stu) > -1:
							common.errorPrompt('..该学生已在读..')
					except Exception as e:
						cur_cls.students.append(stu)
						role.db.db_session.commit()
				else:
					common.errorPrompt('没有该QQ号的学生信息..')
			else:
				common.errorPrompt('..录入错误..')

def flushData(role):
	pass

def sessionArrange(role):
	'''开课'''
	while True:
		for cls in role.tec.classes_list:
			print(cls)
			for r in cls.classesRecords:
				print('|--',r)
		choice = input('请选择班级编号:（[q]退出）')
		if choice == 'q':
			break

		else:
			for cls in role.tec.classes_list:
				if cls.id ==int(choice):
					cur_classes = cls
					break
			if cur_classes:
				# 选择后记录开课内容
				input_opDate = input('请录入开课日期(%Y-%m-%d):')
				input_sessionDesc = input('请录入课程内容:')
				new_record = ClassesRecord(sessionNo = input_sessionDesc,opDate = input_opDate)
				new_record.classes = cur_classes
				new_record.teacher = role.tec
				role.db.db_session.add(new_record)
				role.db.db_session.commit()
				print('...开课成功...')
				# flush
				role.tec = role.db.db_session.query(Teacher).filter(Teacher.id==role.tec.id).first()

def queryStudent(role):
	'''获取班级成员'''
	for cls in role.tec.classes_list:
		print(cls)
	choice = input('请选择班级编号:')
	for cls in role.tec.classes_list:
		if cls.id == int(choice):
			cur_classes = cls
			break
	if cur_classes:
		for stu in cur_classes.students:
			print(stu)
	else:
		print('Sorry,该班级没有学员报名...')

def ChangeScore(role):
	'''修改成绩'''
	while True:
		# 显示已开课的情况
		if len(role.tec.classesRecords)<1:
			print('暂时没有上课记录....')
			break
		for cr in role.tec.classesRecords:
			print(cr)
		choice = input('请选择你要修改成绩的课时：([q]退出)')
		if choice == 'q':
			break
		else:
			cur_classes = None
			for cr in role.tec.classesRecords:
				if cr.id == int(choice):
					cur_classes = cr
					break
			if cur_classes:
				if len(cur_classes.studentRecords)<1:
					common.errorPrompt('没有学生上传作业...')
					break
				for st in cur_classes.studentRecords:
					print(st)
				choice = input('请录入要修改成绩的记录编号:（[q]退出）')
				if choice == 'q':
					break
				else:
					for st in cur_classes.studentRecords:
						if st.id == int(choice):
							cur_st = st
							input_score = input('成绩为:')
							cur_st.score = input_score
							role.db.db_session.commit()
			else:
				common.errorPrompt('录入错误...')
				break


def displayMenu(teacher,db):
	role = TeacherRole(teacher,db)

	menu = ''
	menu += '[1]新增班级'.ljust(menu_width)
	menu += '[2]添加学员'.ljust(menu_width)
	menu += '[3]上课安排'.ljust(menu_width)+os.linesep
	menu += '[4]记录成绩'.ljust(menu_width)
	menu += '[5]查看班级成员'.ljust(menu_width)
	# menu += '[88]修改密码'.ljust(menu_width)+os.linesep
	menu += '[99]退出'.ljust(menu_width)

	while True:
		# print('负责的课程'.center(center_width,'-'))
		# for cls in role.tec.classes_list:
		# 	print(cls)
		common.menuDisplay(menu)
		choice = input('请录入菜单代码:')
		if choice == '99':
			break
		elif choice == '1':
			classesManage(role)
		elif choice == '2':
			addStu(role)
		elif choice == '3':
			sessionArrange(role)
		elif choice == '4':
			ChangeScore(role)
		elif choice =='5':
			queryStudent(role)
		elif choice == '88':
			cur_pwd = input('请录入旧密码:')
			new_pwd = input('请录入新密码:')
			User.Change_Password(teacher.login_user, cur_pwd, new_pwd,2)
		else:
			pass


# # unit test
# tec = model.Teacher('1', 'oldboy', 'oldboy', '','8001')
# role = TeacherRole(tec)
# displayMenu(tec)
# sessionArrange(role)