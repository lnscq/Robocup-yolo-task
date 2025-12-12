# RoboCup 视觉识别项目 - 产品检测 (Product Detection)

本项目基于 **YOLOv8** 框架，专门用于 RoboCup 比赛中的物体识别任务（如：洗发水、饼干等超市货架物品的自动检测与定位）。

-----

## 📂 项目结构 (Project Structure)

```text
robocup/
├── yolo_task/
│   ├── scripts/
│   │   └── train.py           # 训练启动脚本
│   └── datasets/
│       └── my_products/       # 数据集目录
│           ├── data.yaml      # 数据集配置文件
│           ├── images/        # 训练和验证图片
│           └── labels/        # YOLO格式标签 (.txt)
├── runs/                      # 训练结果 (模型权重、曲线图)
├── yolov8s.pt                 # 预训练权重
└── README.md
```

-----

## 🛠️ 环境要求 (Environment Setup)

### 1\. 硬件要求

  * **GPU**: NVIDIA GeForce RTX 4060 (Laptop)
  * **Driver**: CUDA 12.7 Supported (Installed CUDA 12.1 for PyTorch compatibility)

### 2\. 软件依赖

推荐使用 Conda 创建纯净环境：

```bash
conda create -n yolo_gpu python=3.10 -y
conda activate yolo_gpu

# 安装支持 GPU 加速的 PyTorch (CUDA 12.1)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 安装 YOLOv8 核心库及依赖
pip install ultralytics "numpy<2.0.0" opencv-python matplotlib
```

-----

## 🚀 快速开始 (Quick Start)

### 1\. 数据标注

使用 `labelImg` 进行标注。确保类别顺序与 `data.yaml` 一致。

```bash
# 启动标注工具
labelImg
```

*注意：请确保选择 **YOLO** 模式，并检查 `classes.txt`。*

### 2\. 模型训练

运行脚本开始训练。由于已配置 GPU 环境，系统将自动调用 RTX 4060。

```bash
python yolo_task/scripts/train.py
```

-----

## 📊 数据集配置 (Dataset Configuration)

`yolo_task/datasets/my_products/data.yaml` 示例：

```yaml
path: D:/XJTU/robocup/yolo_task/datasets/my_products
train: images/train
val: images/val

names:
  0: biscuit
  1: coke
  2: shampoo
  3: noodle
  4: bread
```
