import ddddocr
from PIL import Image, ImageOps
import io

class CaptchaSolver:
    _ocr = None

    @classmethod
    def get_ocr(cls):
        """使用 Singleton 模式避免重複載入 OCR 模型"""
        if cls._ocr is None:
            cls._ocr = ddddocr.DdddOcr(show_ad=False)
        return cls._ocr

    @staticmethod
    def solve(img_bytes):
        """接收圖片 bytes，回傳辨識字串"""
        ocr = CaptchaSolver.get_ocr()
        
        # 圖像前處理
        original_image = Image.open(io.BytesIO(img_bytes)).convert('L')
        scale_factor = 3 # 放大以利辨識
        new_width = original_image.width * scale_factor
        new_height = original_image.height * scale_factor
        
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.NEAREST)
        bordered_image = ImageOps.expand(resized_image, border=10, fill='white')

        processed = io.BytesIO()
        bordered_image.save(processed, format="PNG")
        processed_bytes = processed.getvalue()
        
        # 辨識
        result = ocr.classification(processed_bytes)
        return result.strip() if result else "?"
