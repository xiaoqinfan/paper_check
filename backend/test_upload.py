import requests
import os

# 测试文件上传
url = "http://localhost:8000/student/paper/upload"

# 准备测试文件
# 注意：这里需要替换为实际的doc文件路径
file_path = "test.doc"
if not os.path.exists(file_path):
    # 创建一个简单的doc文件
    with open(file_path, "w") as f:
        f.write("This is a test doc file")

# 准备表单数据
data = {
    "student_id": 3,
    "class_id": 1
}

# 准备文件
files = {
    "file": (file_path, open(file_path, "rb"), "application/msword")
}

# 发送请求
try:
    response = requests.post(url, data=data, files=files)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    # 关闭文件
    if "file" in files:
        files["file"][1].close()
    # 删除测试文件
    if os.path.exists(file_path):
        os.remove(file_path)