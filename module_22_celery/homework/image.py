"""
Здесь происходит логика обработки изображения
"""
from typing import Optional
import os
from PIL import Image, ImageFilter

folder_name = "test_photos"
save_path = os.path.join(os.getcwd(), folder_name)
if not os.path.exists(save_path):
    os.makedirs(save_path)

def blur_image(src_filename: str, dst_filename: Optional[str] = None):
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5.
    """
    if not dst_filename:
        dst_filename = f'blur_{src_filename}'

    with Image.open(src_filename) as img:
        img.load()
        new_img = img.filter(ImageFilter.GaussianBlur(5))
        new_img.save(os.path.join(save_path, dst_filename))