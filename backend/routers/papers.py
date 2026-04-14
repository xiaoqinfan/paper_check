from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import os
import uuid
from db import get_db
from models import SysUser, PaperDocument, CheckTask, CheckErrorDetail, CourseClass, StudentClassRel
from services import PaperService
from routers.auth import get_current_user

router = APIRouter()

# 确保上传目录存在
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 上传论文
@router.post("/upload")
async def upload_paper(
    class_id: int,
    paper_name: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_user)
):
    if current_user.user_type != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can upload papers"
        )
    # 检查班级是否存在
    class_info = db.query(CourseClass).filter(CourseClass.id == class_id).first()
    if not class_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    # 检查学生是否在班级中
    rel = db.query(StudentClassRel).filter(
        StudentClassRel.student_id == current_user.id,
        StudentClassRel.class_id == class_id
    ).first()
    if not rel:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this class"
        )
    # 检查文件类型
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ['.docx', '.doc']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only docx and doc files are allowed"
        )
    # 保存文件
    file_name = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    # 创建论文记录
    new_paper = PaperService.upload_paper(
        db=db,
        student_id=current_user.id,
        class_id=class_id,
        paper_name=paper_name,
        file_path=file_path
    )
    return new_paper

# 格式检测
@router.post("/{paper_id}/check")
def check_paper_format(
    paper_id: int,
    template_id: int = 1,  # 默认使用第一个模板
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_user)
):
    paper = db.query(PaperDocument).filter(PaperDocument.id == paper_id).first()
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )
    # 检查权限
    if current_user.user_type == 3 and paper.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    elif current_user.user_type == 2:
        class_info = db.query(CourseClass).filter(CourseClass.id == paper.class_id).first()
        if class_info.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    # 使用服务层进行格式检测
    try:
        new_task = PaperService.check_paper_format(db, paper_id, template_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return new_task

# 查看检测报告
@router.get("/{paper_id}/report")
def get_paper_report(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_user)
):
    paper = db.query(PaperDocument).filter(PaperDocument.id == paper_id).first()
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )
    # 检查权限
    if current_user.user_type == 3 and paper.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    elif current_user.user_type == 2:
        class_info = db.query(CourseClass).filter(CourseClass.id == paper.class_id).first()
        if class_info.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    # 使用服务层获取报告
    try:
        report = PaperService.get_paper_report(db, paper_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return report

# 获取学生的论文列表
@router.get("/student/list")
def get_student_papers(
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_user)
):
    if current_user.user_type != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view their papers"
        )
    papers = PaperService.get_student_papers(db, current_user.id)
    return papers

# 获取班级的论文列表（教师）
@router.get("/class/{class_id}/list")
def get_class_papers(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_user)
):
    if current_user.user_type != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can view class papers"
        )
    # 检查班级是否属于该教师
    class_info = db.query(CourseClass).filter(CourseClass.id == class_id).first()
    if not class_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    if class_info.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    papers = PaperService.get_class_papers(db, class_id)
    return papers
