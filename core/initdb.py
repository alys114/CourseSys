# Author: Vincent.chan
# Blog: http://blog.alys114.com

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DECIMAL,Table,ForeignKey,DateTime,SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy import func,desc
import datetime
import time
import common
import dataAccess


engine = create_engine(common.ReadConfig('db','dns'))
db = dataAccess.dbProxy(engine)

class School(db.Base):
	__tablename__ = 'school'
	id = Column(Integer,primary_key=True)
	name = Column(String(100),nullable=False)
	addr = Column(String(200))

class Teacher(db.Base):
	__tablename__='teacher'
	id = Column(Integer,primary_key=True)
	name = Column(String(100),nullable=False)
	login_user = Column(String(100),nullable=False)
	password = Column(String(500))
	qq = Column(String(20), nullable=False)
	school_id = Column(Integer, ForeignKey('school.id'), nullable=False)
	# 建立关系
	school = relationship("School", backref="teachers")

class Student(db.Base):
	__tablename__='student'
	id = Column(Integer,primary_key=True)
	name = Column(String(100),nullable=False)
	login_user = Column(String(100),nullable=False)
	password = Column(String(500))
	qq = Column(String(20),nullable=False)
	school_id = Column(Integer, ForeignKey('school.id'), nullable=False)
	# 建立关系
	school = relationship("School", backref="students")

	def __repr__(self):
		return '学生姓名:[%s],QQ:[%s]' %(self.name,self.qq)

class Course(db.Base):
	__tablename__ = 'course'
	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	price = Column(DECIMAL(8,2), nullable=False)
	school_id = Column(Integer, ForeignKey('school.id'),nullable=False)
	# 建立关系
	school = relationship("School",backref="courses")

	def __repr__(self):
		return '课程ID:[%s],课程名称:[%s],课程价格:[%s]' %(self.id,self.name,self.price)

teacher_m2m_classes = Table('teacher_m2m_classes', db.Base.metadata,
                        Column('teacher_id',Integer,ForeignKey('teacher.id'),nullable=False),
                        Column('classes_id',Integer,ForeignKey('classes.id'),nullable=False),
                        )

student_m2m_classes = Table('student_m2m_classes', db.Base.metadata,
                        Column('student_id',Integer,ForeignKey('student.id'),nullable=False),
                        Column('classes_id',Integer,ForeignKey('classes.id'),nullable=False),
                        )

class Classes(db.Base):
	__tablename__ = 'classes'
	id = Column(Integer, primary_key=True)
	name = Column(String(50),nullable=False)
	period = Column(String(100))
	openDate = Column(String(100))
	course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
	# 建立关系
	course = relationship("Course", backref="classes_list")
	teachers = relationship('Teacher', secondary=teacher_m2m_classes, backref='classes_list')
	students = relationship('Student', secondary=student_m2m_classes, backref='classes_list')

	def __repr__(self):
		tec_list=[]
		for t in self.teachers:
			tec_list.append(t.name)
		return '班级编号:[%s],班级:[%s],课程名称:[%s],学习周期:[%s],开课日期:[%s],导师:[%s]' \
			   %(self.id,self.name,self.course.name,self.period,self.openDate,''.join(tec_list))

class ClassesRecord(db.Base):
	'''开课记录'''
	__tablename__ = 'classes_record'
	id = Column(Integer, primary_key=True)
	sessionNo = Column(String(100))
	opDate = Column(String(100))
	classes_id = Column(Integer, ForeignKey('classes.id'),nullable=False)
	classes = relationship("Classes", backref="classesRecords")
	teacher_id = Column(Integer, ForeignKey('teacher.id'),nullable=False)
	teacher = relationship("Teacher", backref="classesRecords")

	def __repr__(self):
		return '课时ID:[%s],开课日期:[%s],课程主题:[%s]' %(self.id,self.opDate,self.sessionNo)

class StudentRecord(db.Base):
	'''学习情况'''
	__tablename__ = 'student_record'
	id = Column(Integer, primary_key=True)
	checkDate = Column(DateTime)
	score = Column(DECIMAL(3))
	status = Column(SmallInteger,nullable=False,default=(-1))

	classes_record_id = Column(Integer, ForeignKey('classes_record.id'),nullable=False)
	classesRecord = relationship("ClassesRecord", backref="studentRecords")
	student_id = Column(Integer, ForeignKey('student.id'),nullable=False)
	student = relationship("Student", backref="studentRecords")

	def __repr__(self):
		return '上课记录ID:[%s],学生:[%s],签到时间:[%s],作业:[%s],成绩:[%s],课时:[%s]' \
			   %(self.id,self.student.name,self.checkDate,'已交' if self.status==1 else '未交',self.score,self.classesRecord.sessionNo)

def init_data():


	# 清空数据
	sql = 'delete from student_m2m_classes;delete from student_record;delete from classes_record;delete from teacher_m2m_classes;delete from classes;delete from course;delete from teacher;delete from student;delete from school;'
	db.db_session.execute(sql)

	school_1 = School(name='北京前程似锦教育',addr='北京西单xxxx')
	# db_session.add(school_1)
	teacher_a = Teacher(name='Alex',login_user='alex',qq='99999',school=school_1,password='e10adc3949ba59abbe56e057f20f883e') #123456
	teacher_o = Teacher(name='Oldboy', login_user='oldboy',qq='88888',school=school_1, password='e10adc3949ba59abbe56e057f20f883e')
	db.db_session.add_all([teacher_a, teacher_o])

	stu_name = 'stu1'
	student_1 = Student(name=stu_name, login_user=stu_name,qq='123456',school=school_1, password='e10adc3949ba59abbe56e057f20f883e')
	db.db_session.add(student_1)
	stu_name = 'stu2'
	student_2 = Student(name=stu_name, login_user=stu_name,qq='654321',school=school_1,
						password='e10adc3949ba59abbe56e057f20f883e')
	db.db_session.add(student_2)
	stu_name = 'stu3'
	student_3 = Student(name=stu_name, login_user=stu_name, qq='666666', school=school_1,
						password='e10adc3949ba59abbe56e057f20f883e')
	db.db_session.add(student_3)
	course_python = Course(name='Python',price='6800.00',school=school_1)
	course_linux = Course(name='Linux',price='5800.00',school=school_1)
	db.db_session.add(course_python)
	db.db_session.add(course_linux)
	cur_date = time.strftime("%Y-%m-%d",time.localtime())
	class_1 = Classes(period='6 Month',openDate=cur_date,course=course_python
					  ,name='面授班16期')
	class_1.teachers=[teacher_a]
	class_1.students=[student_1,student_2]
	db.db_session.add(class_1)

	cls_record = ClassesRecord(sessionNo='第1周-Python基础入门',opDate=cur_date)
	cls_record.teacher = teacher_a
	cls_record.classes = class_1
	db.db_session.add(cls_record)

	stu_record_1 = StudentRecord(checkDate=datetime.datetime.now(),status=1,score=90)
	stu_record_1.student = student_1
	stu_record_1.classesRecord = cls_record
	db.db_session.add(stu_record_1)
	stu_record_2 = StudentRecord(checkDate=datetime.datetime.now(), status=1, score=85)
	stu_record_2.student = student_2
	stu_record_2.classesRecord = cls_record
	db.db_session.add(stu_record_2)

	db.db_session.commit()


if __name__ == '__main__':
	db.Base.metadata.create_all(db.engine)
	# init_data()

	# data = db.db_session.query(func.sum(StudentRecord.score), StudentRecord.student_id)\
	# 	.filter(StudentRecord==1) \
	# 	.group_by(StudentRecord.student_id).all()

	data = (db.db_session.query(func.sum(StudentRecord.score).label('total'),StudentRecord.student_id, Student.name). \
			filter(StudentRecord.classes_record_id == ClassesRecord.id). \
			filter(StudentRecord.student_id == Student.id).filter(ClassesRecord.classes_id == 1)).group_by(StudentRecord.student_id).order_by(desc('total'))
	print(data)
	db.close()



