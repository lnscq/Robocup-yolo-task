import os
import random
import shutil

# --- 配置参数 ---
# 获取当前脚本的运行目录作为项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 定位到 yolo_task 根目录

# 存放原始图片和标注文件的目录 (所有标注完成后，文件都在这里)
RAW_IMAGES_DIR = os.path.join(BASE_DIR, 'datasets', 'my_products', 'images', 'raw')
RAW_LABELS_DIR = os.path.join(BASE_DIR, 'datasets', 'my_products', 'labels', 'raw')

# 划分后图片存放的目录 (train/val)
TARGET_IMAGES_DIR = os.path.join(BASE_DIR, 'datasets', 'my_products', 'images')
# 划分后标注存放的目录 (train/val)
TARGET_LABELS_DIR = os.path.join(BASE_DIR, 'datasets', 'my_products', 'labels')

# 划分比例：80% 训练集，20% 验证集
TRAIN_RATIO = 0.8
VAL_RATIO = 1.0 - TRAIN_RATIO  

# --- 核心函数 ---

def create_dirs():
    """创建目标 train 和 val 文件夹。"""
    for folder in ['train', 'val']:
        os.makedirs(os.path.join(TARGET_IMAGES_DIR, folder), exist_ok=True)
        os.makedirs(os.path.join(TARGET_LABELS_DIR, folder), exist_ok=True)
    print("目标文件夹创建完毕。")

def split_data():
    """执行数据集划分和文件移动。"""
    if not os.path.exists(RAW_IMAGES_DIR):
        print(f"错误：未找到原始图片目录 '{RAW_IMAGES_DIR}'。请检查。")
        return

    # 1. 收集所有图片文件名
    all_images = os.listdir(RAW_IMAGES_DIR)
    
    # 过滤出图片文件 (只处理常见的图片格式)
    image_files = [f for f in all_images if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    
    if not image_files:
        print(f"警告：在 '{RAW_IMAGES_DIR}' 中没有找到任何图片文件。请检查。")
        return

    # 2. 随机打乱文件列表
    random.shuffle(image_files)
    total_count = len(image_files)
    train_count = int(total_count * TRAIN_RATIO)
    
    # 3. 划分列表
    train_files = image_files[:train_count]
    val_files = image_files[train_count:]

    print(f"总图片数：{total_count}")
    print(f"训练集数量 ({TRAIN_RATIO*100}%): {len(train_files)}")
    print(f"验证集数量 ({VAL_RATIO*100}%): {len(val_files)}")
    print("-" * 30)

    # 4. 移动文件
    def move_files(file_list, target_set):
        """移动图片及其对应的标注文件。"""
        images_target = os.path.join(TARGET_IMAGES_DIR, target_set)
        labels_target = os.path.join(TARGET_LABELS_DIR, target_set)
        
        for image_name in file_list:
            # 移动图片
            src_image = os.path.join(RAW_IMAGES_DIR, image_name)
            dst_image = os.path.join(images_target, image_name)
            shutil.copy(src_image, dst_image)  # 改为 copy，保留原文件
            
            # 移动对应的 YOLO 标注文件 (.txt)，如果存在的话
            base_name, _ = os.path.splitext(image_name)
            label_name = base_name + '.txt'
            src_label = os.path.join(RAW_LABELS_DIR, label_name)
            dst_label = os.path.join(labels_target, label_name)
            
            if os.path.exists(src_label):
                shutil.copy(src_label, dst_label)  # 改为 copy，保留原文件

    print("开始复制训练集文件...")
    move_files(train_files, 'train')
    
    print("开始复制验证集文件...")
    move_files(val_files, 'val')
    
    print("\n✅ 数据集划分完成！")
    print(f"   训练集图片: {os.path.join(TARGET_IMAGES_DIR, 'train')}")
    print(f"   验证集图片: {os.path.join(TARGET_IMAGES_DIR, 'val')}")
    print(f"   对应的标注文件会自动放在 labels/train 和 labels/val 中")

if __name__ == '__main__':
    create_dirs()
    split_data()