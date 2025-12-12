import cv2, os

# 获取脚本所在目录并构建绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
yolo_task_dir = os.path.dirname(script_dir)  # 直接回到 yolo_task 目录

VIDEO = os.path.join(yolo_task_dir, "datasets", "my_products", "video", "raw.mp4")
OUT_DIR = os.path.join(yolo_task_dir, "datasets", "my_products", "images", "raw")
SKIP = 10

os.makedirs(OUT_DIR, exist_ok=True)

# 使用 imdecode/imencode 解决中文路径问题
import numpy as np

cap = cv2.VideoCapture(VIDEO)

frame_id, saved = 0, 0
while True:
    ret, frame = cap.read()
    if not ret: break
    if frame_id % SKIP == 0:
        output_path = os.path.join(OUT_DIR, f"frame_{saved:05d}.jpg")
        # 使用 imencode 获取字节，再写入文件
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            with open(output_path, 'wb') as f:
                f.write(buffer.tobytes())
            saved += 1
    frame_id += 1
cap.release()
print(f"✅ 抽帧完成：{saved} 张图片")
