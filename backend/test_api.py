import requests

# 测试/paper/content接口
response = requests.get('http://localhost:8000/paper/content/20')
print(f"Status code: {response.status_code}")
print(f"Response content: {response.text}")

# 保存响应到文件
with open('response.txt', 'w', encoding='utf-8') as f:
    f.write(response.text)
print('Response saved to response.txt')