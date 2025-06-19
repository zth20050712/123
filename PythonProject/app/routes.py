from flask import Blueprint, render_template, request, redirect, url_for, flash
from .utils import process_image, call_llm_api
import os
import uuid
import logging

main = Blueprint('main', __name__)

def handle_file_upload(file):
    # 生成唯一文件名
    filename = str(uuid.uuid4()) + get_file_extension(file.filename)
    upload_folder = os.path.join(os.getcwd(), 'app/static/uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, filename)
    try:
        file.save(file_path)
        logging.info(f"文件保存成功: {file_path}")
        return file_path, filename
    except Exception as e:
        logging.error(f'文件保存错误: {str(e)}', exc_info=True)
        raise

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'image' not in request.files:
            flash('没有文件')
            return redirect(request.url)

        file = request.files['image']

        # 检查文件名是否为空
        if file.filename == '':
            flash('没有选择文件')
            return redirect(request.url)

        # 检查文件类型是否允许
        if file and allowed_file(file.filename):
            try:
                file_path, filename = handle_file_upload(file)

                # 处理图片并调用LLM API
                image_data = process_image(file_path)
                caption = call_llm_api(image_data)

                if caption:
                    return render_template('result.html',
                                           image_path=f'static/uploads/{filename}',
                                           caption=caption)
                else:
                    flash('无法生成图片描述，请重试')
            except Exception as e:
                flash(f'处理过程中出错: {str(e)}')
                logging.error(f'错误: {str(e)}', exc_info=True)

    return render_template('index.html')

# 辅助函数
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    return '.' + filename.rsplit('.', 1)[1].lower() if '.' in filename else ''