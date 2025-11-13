#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
from PIL import Image
import math
import threading
from utils.tetra_math import TetraMathEngine
from utils.camera_simulator import CameraSimulator
from utils.resource_manager import ResourceManager

class Tetra3DConverter:
    def __init__(self):
        self.math_engine = TetraMathEngine()
        self.camera_sim = CameraSimulator()
        self.resource_mgr = ResourceManager()
        
    def convert_image_to_3d(self, image_path, output_path):
        """تبدیل تصویر 2D به مدل 3D"""
        try:
            print("📁 در حال بارگذاری تصویر...")
            
            # بارگذاری و پردازش تصویر
            image = Image.open(image_path)
            img_array = np.array(image)
            
            print("🎯 در حال تولید دوربین‌های مجازی...")
            # تولید دوربین‌های مجازی
            base_camera = {
                'focal_length': 50.0,
                'center_x': img_array.shape[1] / 2,
                'center_y': img_array.shape[0] / 2,
                'rotation_factor': 0.0
            }
            
            virtual_cameras = self.camera_sim.generate_virtual_cameras(base_camera, 3)
            
            print("🔢 در حال اعمال فرمول ریاضی تترا...")
            # محاسبه عمق با فرمول ریاضی
            depth_map = self.math_engine.calculate_depth_map(
                img_array, virtual_cameras
            )
            
            print("💾 در حال ذخیره مدل 3D...")
            # ذخیره مدل 3D
            self.save_3d_model(depth_map, output_path)
            
            print(f"✅ تبدیل با موفقیت انجام شد: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ خطا در تبدیل: {str(e)}")
            return False
    
    def save_3d_model(self, depth_map, output_path):
        """ذخیره مدل 3D در قالب OBJ"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# مدل 3D تولید شده توسط Tetra Ecosystem\n")
            f.write("# فرمول ریاضی مخترع\n\n")
            
            # ذخیره رئوس (Vertices)
            height, width = depth_map.shape
            for y in range(height):
                for x in range(width):
                    z = depth_map[y, x]
                    f.write(f"v {x} {y} {z}\n")
            
            # ذخیره وجه‌ها (Faces)
            for y in range(height - 1):
                for x in range(width - 1):
                    v1 = y * width + x + 1
                    v2 = y * width + x + 2
                    v3 = (y + 1) * width + x + 2
                    v4 = (y + 1) * width + x + 1
                    f.write(f"f {v1} {v2} {v3} {v4}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("استفاده: python main.py <ورودی.jpg> <خروجی.obj>")
        sys.exit(1)
    
    converter = Tetra3DConverter()
    converter.convert_image_to_3d(sys.argv[1], sys.argv[2])
