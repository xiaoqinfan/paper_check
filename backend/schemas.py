from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    real_name: str
    user_type: int

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    real_name: str
    user_type: int

class ClassBase(BaseModel):
    class_name: str
    college: str
    major: str

class ClassCreate(ClassBase):
    pass

class ClassResponse(ClassBase):
    id: int
    teacher_id: int

class TemplateBase(BaseModel):
    template_name: str

class TemplateCreate(TemplateBase):
    pass

class TemplateResponse(TemplateBase):
    id: int

class RuleBase(BaseModel):
    target_part: str
    rule_key: str
    rule_value: str
    error_tip: str

class RuleCreate(RuleBase):
    pass

class RuleResponse(RuleBase):
    id: int
    template_id: int

class PaperResponse(BaseModel):
    id: int
    student_id: int
    class_id: int
    paper_name: str
    file_path: str

class CheckTaskResponse(BaseModel):
    id: int
    paper_id: int
    format_score: float
    total_error: int

class ErrorDetailResponse(BaseModel):
    id: int
    task_id: int
    paper_id: int
    position: str
    error_message: str
    expect: str
    actual: str

class ReportResponse(BaseModel):
    task: CheckTaskResponse
    error_details: list[ErrorDetailResponse]
