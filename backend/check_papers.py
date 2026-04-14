from main import get_db
from models import PaperDocument

# 获取数据库会话
db = next(get_db())

# 查询所有论文记录
papers = db.query(PaperDocument).all()

print('Papers in database:')
for paper in papers:
    print(f'ID: {paper.id}, Name: {paper.paper_name}, File Path: {paper.file_path}')
