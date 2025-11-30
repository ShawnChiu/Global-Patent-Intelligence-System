import easyocr
import numpy as np
from PIL import Image, ImageOps
import io
import streamlit as st

class CaptchaSolver:
    _reader = None

    @classmethod
    def get_reader(cls):
        """使用 Singleton 模式或 Streamlit cache 避免重複載入模型"""
        if cls._reader is None:
            # 這裡可以根據硬體調整 gpu=True/False
            cls._reader = easyocr.Reader(['en'], gpu=True)
        return cls._reader

    @staticmethod
    def solve(img_bytes):
        """接收圖片 bytes，回傳辨識字串"""
        reader = CaptchaSolver.get_reader()
        
        # 圖像前處理
        original_image = Image.open(io.BytesIO(img_bytes)).convert('L')
        scale_factor = 5 # 放大以利辨識
        new_width = original_image.width * scale_factor
        new_height = original_image.height * scale_factor
        
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.NEAREST)
        bordered_image = ImageOps.expand(resized_image, border=20, fill='white')
        image_np = np.array(bordered_image)
        
        # 辨識
        result = reader.readtext(image_np, detail=0)
        return result[0] if result else "?"