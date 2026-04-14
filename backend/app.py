from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# 允许上传的 WPS 格式
ALLOWED_EXTENSIONS = {'wps', 'et', 'dps', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    preview_url = None
    error_msg = None

    if request.method == 'POST':
        if 'file' not in request.files:
            error_msg = "未选择文件"
        else:
            file = request.files['file']
            if file.filename == '':
                error_msg = "请选择一个文件"
            elif allowed_file(file.filename):
                # 生成在线预览链接（WPS官方免费接口）
                filename = file.filename
                preview_url = f"https://wpsview.ks3-cn-beijing.ksyun.com/view/url?filename={filename}"

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>WPS文档在线预览</title>
        <style>
            body { max-width: 1200px; margin: 30px auto; padding: 20px; font-family: "Microsoft YaHei"; }
            .upload { padding: 30px; border: 1px solid #ddd; border-radius: 10px; text-align: center; }
            button { padding: 10px 25px; background: #1890ff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            .preview { margin-top: 30px; height: 800px; border: 1px solid #eee; border-radius: 10px; overflow: hidden; }
            iframe { width: 100%; height: 100%; border: none; }
            .error { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">📑 WPS 文档在线预览</h1>

        <div class="upload">
            <form method=post enctype=multipart/form-data>
                <input type="file" name="file" accept=".wps,.et,.dps,.docx,.doc,.xls,.xlsx,.ppt,.pptx" required>
                <button type="submit">上传并预览</button>
            </form>
        </div>

        {% if error_msg %}
            <p class="error">{{ error_msg }}</p>
        {% endif %}

        {% if preview_url %}
        <div class="preview">
            <iframe src="{{ preview_url }}"></iframe>
        </div>
        {% endif %}
    </body>
    </html>
    '''
    return render_template_string(html, preview_url=preview_url, error_msg=error_msg)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')