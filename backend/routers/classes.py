from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from models import SysUser, CourseClass, StudentClassRel
from routers.auth import get_current_user

router = APIRouter()

# 获取所有班级
@router.get("")
def get_classes(db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    if current_user.user_type == 1:  # 管理员可以查看所有班级
        classes = db.query(CourseClass).all()
    elif current_user.user_type == 2:  # 教师只能查看自己的班级
        classes = db.query(CourseClass).filter(CourseClass.teacher_id == current_user.id).all()
    else:  # 学生只能查看自己所在的班级
        rels = db.query(StudentClassRel).filter(StudentClassRel.student_id == current_user.id).all()
        class_ids = [rel.class_id for rel in rels]
        classes = db.query(CourseClass).filter(CourseClass.id.in_(class_ids)).all()
    return classes

# 获取指定班级
@router.get("/{class_id}")
def get_class(class_id: int, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    class_info = db.query(CourseClass).filter(CourseClass.id == class_id).first()
    if not class_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    # 检查权限
    if current_user.user_type == 3:  # 学生
        rel = db.query(StudentClassRel).filter(
            StudentClassRel.student_id == current_user.id,
            StudentClassRel.class_id == class_id
        ).first()
        if not rel:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    elif current_user.user_type == 2:  # 教师
        if class_info.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    return class_info

# 创建班级（仅教师）
@router.post("")
def create_class(class_data: dict, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    if current_user.user_type != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    new_class = CourseClass(
        class_name=class_data.get("class_name"),
        teacher_id=current_user.id,
        college=class_data.get("college"),
        major=class_data.get("major")
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

# 更新班级信息
@router.put("/{class_id}")
def update_class(class_id: int, class_data: dict, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    class_info = db.query(CourseClass).filter(CourseClass.id == class_id).first()
    if not class_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    # 只有教师本人或管理员可以更新
    if current_user.user_type != 1 and class_info.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    # 更新班级信息
    if "class_name" in class_data:
        class_info.class_name = class_data["class_name"]
    if "college" in class_data:
        class_info.college = class_data["college"]
    if "major" in class_data:
        class_info.major = class_data["major"]
    # 只有管理员可以更改教师
    if "teacher_id" in class_data and current_user.user_type == 1:
        class_info.teacher_id = class_data["teacher_id"]
    db.commit()
    db.refresh(class_info)
    return class_info

# 删除班级
@router.delete("/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    class_info = db.query(CourseClass).filter(CourseClass.id == class_id).first()
    if not class_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    # 只有教师本人或管理员可以删除
    if current_user.user_type != 1 and class_info.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    db.delete(class_info)
    db.commit()
    return {"message": "Class deleted successfully"}

# 添加学生到班级
@router.post("/{class_id}/students")
def add_student_to_class(class_id: int, student_id: int, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    class_info = db.query(CourseClass).filter(CourseClass.id == class_id).first()
    if not class_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    # 只有教师本人或管理员可以添加学生
    if current_user.user_type != 1 and class_info.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    # 检查学生是否存在
    student = db.query(SysUser).filter(SysUser.id == student_id, SysUser.user_type == 3).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    # 检查学生是否已经在班级中
    existing_rel = db.query(StudentClassRel).filter(
        StudentClassRel.class_id == class_id,
        StudentClassRel.student_id == student_id
    ).first()
    if existing_rel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already in class"
        )
    # 添加学生到班级
    new_rel = StudentClassRel(
        class_id=class_id,
        student_id=student_id
    )
    db.add(new_rel)
    db.commit()
    db.refresh(new_rel)
    return new_rel

# 从班级中移除学生
@router.delete("/{class_id}/students/{student_id}")
def remove_student_from_class(class_id: int, student_id: int, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    class_info = db.query(CourseClass).filter(CourseClass.id == class_id).first()
    if not class_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    # 只有教师本人或管理员可以移除学生
    if current_user.user_type != 1 and class_info.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    # 查找关系
    rel = db.query(StudentClassRel).filter(
        StudentClassRel.class_id == class_id,
        StudentClassRel.student_id == student_id
    ).first()
    if not rel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not in class"
        )
    db.delete(rel)
    db.commit()
    return {"message": "Student removed from class successfully"}

# 获取班级学生列表
@router.get("/{class_id}/students")
def get_class_students(class_id: int, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    class_info = db.query(CourseClass).filter(CourseClass.id == class_id).first()
    if not class_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    # 检查权限
    if current_user.user_type == 3:  # 学生
        rel = db.query(StudentClassRel).filter(
            StudentClassRel.student_id == current_user.id,
            StudentClassRel.class_id == class_id
        ).first()
        if not rel:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    elif current_user.user_type == 2:  # 教师
        if class_info.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    # 获取学生列表
    rels = db.query(StudentClassRel).filter(StudentClassRel.class_id == class_id).all()
    student_ids = [rel.student_id for rel in rels]
    students = db.query(SysUser).filter(SysUser.id.in_(student_ids)).all()
    return students
