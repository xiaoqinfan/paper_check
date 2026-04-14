from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from db import Base

class SysUser(Base):
    __tablename__ = "sys_user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    real_name = Column(String(50), nullable=False)
    user_type = Column(Integer, nullable=False)  # 1: 管理员, 2: 教师, 3: 学生

class CourseClass(Base):
    __tablename__ = "course_class"
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False)
    college = Column(String(100), nullable=False)
    major = Column(String(100), nullable=False)
    teacher = relationship("SysUser", backref="classes")

class StudentClassRel(Base):
    __tablename__ = "student_class_rel"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("course_class.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False)
    class_info = relationship("CourseClass", backref="students")
    student = relationship("SysUser", backref="classes_rel")

class FormatTemplate(Base):
    __tablename__ = "format_template"
    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String(100), nullable=False)

class FormatRuleItem(Base):
    __tablename__ = "format_rule_item"
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("format_template.id"), nullable=False)
    target_part = Column(String(50), nullable=False)
    rule_key = Column(String(50), nullable=False)
    rule_value = Column(String(200), nullable=False)
    error_tip = Column(String(200), nullable=False)
    template = relationship("FormatTemplate", backref="rules")

class PaperDocument(Base):
    __tablename__ = "paper_document"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("course_class.id"), nullable=False)
    paper_name = Column(String(200), nullable=False)
    file_path = Column(String(200), nullable=False)
    student = relationship("SysUser", backref="papers")
    class_info = relationship("CourseClass", backref="papers")

class CheckTask(Base):
    __tablename__ = "check_task"
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("paper_document.id"), nullable=False)
    format_score = Column(Float, nullable=False)
    total_error = Column(Integer, nullable=False)
    paper = relationship("PaperDocument", backref="check_tasks")

class CheckErrorDetail(Base):
    __tablename__ = "check_error_detail"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("check_task.id"), nullable=False)
    paper_id = Column(Integer, ForeignKey("paper_document.id"), nullable=False)
    position = Column(String(100), nullable=False)
    error_message = Column(String(200), nullable=False)
    expect = Column(String(200), nullable=False)
    actual = Column(String(200), nullable=False)
    task = relationship("CheckTask", backref="error_details")
    paper = relationship("PaperDocument", backref="error_details")
