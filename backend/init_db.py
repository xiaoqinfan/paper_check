from db import engine, Base, SessionLocal
from models import SysUser
from routers.auth import get_password_hash

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 初始化管理员账户
db = SessionLocal()
try:
    # 检查是否已存在管理员账户
    admin = db.query(SysUser).filter(SysUser.username == "admin").first()
    if not admin:
        # 创建管理员账户
        admin = SysUser(
            username="admin",
            password=get_password_hash("admin123"),
            real_name="系统管理员",
            user_type=1
        )
        db.add(admin)
        db.commit()
        print("管理员账户初始化成功")
    else:
        print("管理员账户已存在")
finally:
    db.close()
