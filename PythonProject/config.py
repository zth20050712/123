import os

# 上传文件夹路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
# 最大文件大小限制
MAX_CONTENT_LENGTH = 16 * 1024 * 1024