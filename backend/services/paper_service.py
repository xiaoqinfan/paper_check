from sqlalchemy.orm import Session
from models import PaperDocument, CheckTask, CheckErrorDetail, FormatTemplate, FormatRuleItem
from services.check_engine import CheckEngine
from typing import List, Dict

class PaperService:
    @staticmethod
    def upload_paper(
        db: Session,
        student_id: int,
        class_id: int,
        paper_name: str,
        file_path: str
    ) -> PaperDocument:
        new_paper = PaperDocument(
            student_id=student_id,
            class_id=class_id,
            paper_name=paper_name,
            file_path=file_path
        )
        db.add(new_paper)
        db.commit()
        db.refresh(new_paper)
        return new_paper
    
    @staticmethod
    def check_paper_format(
        db: Session,
        paper_id: int,
        template_id: int = 1
    ) -> CheckTask:
        paper = db.query(PaperDocument).filter(PaperDocument.id == paper_id).first()
        if not paper:
            raise ValueError("Paper not found")
        
        # 获取模板规则
        rules = db.query(FormatRuleItem).filter(FormatRuleItem.template_id == template_id).all()
        rule_list = []
        for rule in rules:
            rule_list.append({
                'target_part': rule.target_part,
                'rule_key': rule.rule_key,
                'rule_value': rule.rule_value,
                'error_tip': rule.error_tip
            })
        
        # 使用检测引擎进行格式检测
        engine = CheckEngine(paper.file_path)
        error_details = engine.check_format(rule_list)
        
        # 计算格式得分和错误数量
        total_error = len(error_details)
        format_score = max(0, 100 - total_error * 2)
        
        # 创建检测任务
        new_task = CheckTask(
            paper_id=paper_id,
            format_score=format_score,
            total_error=total_error
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        # 创建错误详情
        for error in error_details:
            error_detail = CheckErrorDetail(
                task_id=new_task.id,
                paper_id=paper_id,
                position=error['position'],
                error_message=error['error_message'],
                expect=error['expect'],
                actual=error['actual']
            )
            db.add(error_detail)
        db.commit()
        
        return new_task
    
    @staticmethod
    def get_paper_report(db: Session, paper_id: int) -> Dict:
        paper = db.query(PaperDocument).filter(PaperDocument.id == paper_id).first()
        if not paper:
            raise ValueError("Paper not found")
        
        # 获取最新的检测任务
        task = db.query(CheckTask).filter(CheckTask.paper_id == paper_id).order_by(CheckTask.id.desc()).first()
        if not task:
            raise ValueError("No check task found")
        
        # 获取错误详情
        error_details = db.query(CheckErrorDetail).filter(CheckErrorDetail.task_id == task.id).all()
        
        return {
            'task': task,
            'error_details': error_details
        }
    
    @staticmethod
    def get_student_papers(db: Session, student_id: int) -> List[PaperDocument]:
        papers = db.query(PaperDocument).filter(PaperDocument.student_id == student_id).all()
        return papers
    
    @staticmethod
    def get_class_papers(db: Session, class_id: int) -> List[PaperDocument]:
        papers = db.query(PaperDocument).filter(PaperDocument.class_id == class_id).all()
        return papers
