from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from models import SysUser
from routers.auth import get_current_user, get_password_hash

router = APIRouter()

# 获取所有用户（仅管理员）
@router.get("/")
def get_users(db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    if current_user.user_type != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    users = db.query(SysUser).all()
    return users

# 获取指定用户
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    user = db.query(SysUser).filter(SysUser.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    # 只有管理员或用户本人可以查看
    if current_user.user_type != 1 and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user

# 创建用户（仅管理员）
@router.post("")
def create_user(user_data: dict, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    if current_user.user_type != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    # 检查用户名是否已存在
    existing_user = db.query(SysUser).filter(SysUser.username == user_data.get("username")).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    # 创建新用户
    hashed_password = get_password_hash(user_data.get("password"))
    new_user = SysUser(
        username=user_data.get("username"),
        password=hashed_password,
        real_name=user_data.get("real_name"),
        user_type=user_data.get("user_type")
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 更新用户信息
@router.put("/{user_id}")
def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    user = db.query(SysUser).filter(SysUser.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    # 只有管理员或用户本人可以更新
    if current_user.user_type != 1 and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    # 更新用户信息
    if "real_name" in user_data:
        user.real_name = user_data["real_name"]
    if "password" in user_data:
        user.password = get_password_hash(user_data["password"])
    # 只有管理员可以更新用户类型
    if "user_type" in user_data and current_user.user_type == 1:
        user.user_type = user_data["user_type"]
    db.commit()
    db.refresh(user)
    return user

# 删除用户（仅管理员）
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: SysUser = Depends(get_current_user)):
    if current_user.user_type != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    user = db.query(SysUser).filter(SysUser.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
