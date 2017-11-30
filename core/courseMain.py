# Author: Vincent.chan
# Blog: http://blog.alys114.com
import os
from sqlalchemy import create_engine
import common,business
from constConfig import info_width,menu_width,center_width
import dataAccess
from initdb import Student
import student_main
import teacher_main



def login(user,db):
	login_user = input('login_user > ').strip()
	password = input('password > ').strip()
	role = input('role[1-stu;2-Teacher] >')
	# login_user = 'stu1'
	# password = '123456'
	# role = '1'
	# login_user = 'alex'
	# password = '123456'
	# role = '2'
	member = [int(role),login_user,password]
	result = user.Login(member)
	if result[0]:
		print(result[1])
		member = result[2]
		if role =='1':
			student_main.displayMenu(member,db)
		else:
			teacher_main.displayMenu(member,db)
	else:
		common.errorPrompt(result[1])

def register(user):
	print('register...')
	input_login_user = input('login_user > ')
	result = user.Register_Check_LoginUser(input_login_user)
	if result[0]:
		input_qq = input('qq >')
		result = user.Register_Check_qq(input_qq)
		if result[0]:
			input_name = input('alias name > ')
			input_password = input('password > ')
			new_stu = Student(name=input_name,login_user=input_login_user
							  ,qq = input_qq,password=input_password)
			user.Register(new_stu)
		else:
			common.errorPrompt(result[1])
			return
	else:
		common.errorPrompt(result[1])
		return


if __name__ == '__main__':
	prompt = "=" * info_width + os.linesep
	prompt += '欢迎来到前程似锦网上教学系统' + os.linesep
	prompt += "=" * info_width
	print("\033[36m%s \033[0m" % prompt)

	menu = ''
	menu += '[1]登录'.ljust(menu_width)
	menu += '[2]注册'.ljust(menu_width)
	menu += '[99]退出'.ljust(menu_width)

	engine = create_engine(common.ReadConfig('db', 'dns'))
	db = dataAccess.dbProxy(engine)
	try:
		user = business.User(db)
		while True:
			common.menuDisplay(menu)
			choice = input('please input your choice:')
			# choice ='1'
			if choice == '99':
				break
			elif choice =='1':
				login(user,db)
			elif choice == '2':
				register(user)
			else:
				pass
	except Exception as e:
		print(e)
	finally:
		db.close()