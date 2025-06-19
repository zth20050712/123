# app/utils.py
import os
import base64
import requests
from PIL import Image
import numpy as np
from dotenv import load_dotenv
import logging

load_dotenv()

# 获取环境变量中的API密钥
LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_API_URL = 'https://api.deepseek.com/v1'

def process_image(image_path):
    """处理上传的图片，调整尺寸并转换为Base64编码"""
    try:
        logging.info(f"开始处理图片: {image_path}")
        # 打开图片并调整尺寸
        img = Image.open(image_path)
        # 调整为模型适合的尺寸，例如224x224
        img = img.resize((224, 224), Image.LANCZOS)

        # 转换为Base64编码
        import io
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        logging.info(f"图片处理成功: {image_path}")
        return img_base64
    except Exception as e:
        logging.error(f'图片处理错误: {str(e)}', exc_info=True)
        raise


def call_llm_api(image_data):
    """调用LLM API生成图片描述"""
    if not LLM_API_KEY:
        raise ValueError("未设置LLM_API_KEY环境变量")

    try:
        logging.info("开始调用LLM API")
        # 根据所选LLM API构建请求格式
        # 以DeepSeek VLM为例，不同API可能有不同的请求格式
        payload = {
            "model": "deepseek-vlm-chat",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                        {"type": "text", "text": "请描述这张图片的内容："}
                    ]
                }
            ],
            "temperature": 0.7
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLM_API_KEY}"
        }

        # 发送API请求
        response = requests.post(LLM_API_URL, json=payload, headers=headers, timeout=30)
        logging.info(f"API响应状态码: {response.status_code}")
        response.raise_for_status()  # 抛出HTTP错误

        # 解析响应
        result = response.json()
        logging.info(f"API响应内容: {result}")
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']['content']
            # 提取文本内容（忽略可能的图像标记）
            text_content = next((item['text'] for item in message if item['type'] == 'text'), '')
            return text_content.strip()
        else:
            logging.error(f"API响应格式错误: {result}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"API请求错误: {str(e)}", exc_info=True)
        raise
    except KeyError as e:
        logging.error(f"API响应解析错误，缺少键: {str(e)}", exc_info=True)
        raise
    except Exception as e:
        logging.error(f"调用LLM API时发生错误: {str(e)}", exc_info=True)
        raise