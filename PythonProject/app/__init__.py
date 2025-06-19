# app/__init__.py
import sys
from pathlib import Path
import logging
from flask import Flask
import os
from config import UPLOAD_FOLDER, MAX_CONTENT_LENGTH

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def create_app():
    app = Flask(__name__)

    # 配置上传文件夹和文件大小限制
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

    # 确保上传文件夹存在
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # 导入蓝图时避免循环导入，放在函数内部
    from .routes import main
    app.register_blueprint(main)

    return app