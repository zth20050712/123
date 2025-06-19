import os
import requests
import logging

class LLMService:
    def __init__(self):
        self.api_key = os.getenv('LLM_API_KEY')
        self.api_url = 'https://api.deepseek.com/v1'
        self._validate_config()

    def _validate_config(self):
        """验证API配置"""
        if not self.api_key:
            raise ValueError("LLM_API_KEY未设置，请检查.env文件")
        if not self.api_url:
            raise ValueError("LLM_API_URL未设置，请检查.env文件")

    def generate_caption(self, image_base64):
        """生成图片描述，包含详细错误处理"""
        payload = {
            "model": "deepseek-vlm-chat",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
                        {"type": "text", "text": "请详细描述这张图片的内容，包括场景、物体、人物动作和环境细节："}
                    ]
                }
            ],
            "temperature": 0.7
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                text_content = next((item['text'] for item in content if item['type'] == 'text'), '')
                return text_content.strip()
            else:
                raise Exception(f"API响应格式错误: {result}")

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP错误 {e.response.status_code}: {e.response.text}"
            if e.response.status_code == 401:
                raise ValueError("API密钥无效") from e
            raise Exception(error_msg) from e
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接失败，请检查网络设置")
        except Exception as e:
            raise Exception(f"LLM调用失败: {str(e)}") from e