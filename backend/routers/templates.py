from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from models import SysUser, FormatTemplate, FormatRuleItem
from routers.auth import get_current_user

router = APIRouter()

# 获取所有模板
@router.get("")
def get_templates(db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    templates = db.query(FormatTemplate).all()
    return templates

# 获取指定模板
@router.get("/{template_id}")
def get_template(template_id: int, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    template = db.query(FormatTemplate).filter(FormatTemplate.id == template_id).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    return template

# 创建模板（仅教师和管理员）
@router.post("")
def create_template(template_data: dict, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    if current_user.user_type not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    new_template = FormatTemplate(
        template_name=template_data.get("template_name")
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template

# 更新模板
@router.put("/{template_id}")
def update_template(template_id: int, template_data: dict, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    template = db.query(FormatTemplate).filter(FormatTemplate.id == template_id).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    if current_user.user_type not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    if "template_name" in template_data:
        template.template_name = template_data["template_name"]
    db.commit()
    db.refresh(template)
    return template

# 删除模板
@router.delete("/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    template = db.query(FormatTemplate).filter(FormatTemplate.id == template_id).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    if current_user.user_type not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    db.delete(template)
    db.commit()
    return {"message": "Template deleted successfully"}

# 获取模板的规则列表
@router.get("/{template_id}/rules")
def get_template_rules(template_id: int, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    template = db.query(FormatTemplate).filter(FormatTemplate.id == template_id).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    rules = db.query(FormatRuleItem).filter(FormatRuleItem.template_id == template_id).all()
    return rules

# 添加规则到模板
@router.post("/{template_id}/rules")
def add_rule_to_template(template_id: int, rule_data: dict, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    template = db.query(FormatTemplate).filter(FormatTemplate.id == template_id).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    if current_user.user_type not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    new_rule = FormatRuleItem(
        template_id=template_id,
        target_part=rule_data.get("target_part"),
        rule_key=rule_data.get("rule_key"),
        rule_value=rule_data.get("rule_value"),
        error_tip=rule_data.get("error_tip")
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule

# 更新规则
@router.put("/rules/{rule_id}")
def update_rule(rule_id: int, rule_data: dict, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    rule = db.query(FormatRuleItem).filter(FormatRuleItem.id == rule_id).first()
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    if current_user.user_type not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    # 更新规则信息
    if "target_part" in rule_data:
        rule.target_part = rule_data["target_part"]
    if "rule_key" in rule_data:
        rule.rule_key = rule_data["rule_key"]
    if "rule_value" in rule_data:
        rule.rule_value = rule_data["rule_value"]
    if "error_tip" in rule_data:
        rule.error_tip = rule_data["error_tip"]
    db.commit()
    db.refresh(rule)
    return rule

# 删除规则
@router.delete("/rules/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    rule = db.query(FormatRuleItem).filter(FormatRuleItem.id == rule_id).first()
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    if current_user.user_type not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    db.delete(rule)
    db.commit()
    return {"message": "Rule deleted successfully"}
