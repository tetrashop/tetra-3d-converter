#!/usr/bin/env python3
from PIL import Image
import numpy as np

# ایجاد یک تصویر تست 100x100 پیکسل
width, height = 100, 100
image_array = np.zeros((height, width, 3), dtype=np.uint8)

# ایجاد یک گرادیانت ساده
for y in range(height):
    for x in range(width):
        image_array[y, x, 0] = int(255 * x / width)  # Red
        image_array[y, x, 1] = int(255 * y / height) # Green
        image_array[y, x, 2] = 128                   # Blue

image = Image.fromarray(image_array)
image.save('test_image.jpg')
print("✅ تصویر تست ایجاد شد: test_image.jpg")
