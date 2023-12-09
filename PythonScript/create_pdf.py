from PIL import Image
from reportlab.pdfgen import canvas
import os

# 输入图片文件夹路径
image_folder = "images"

# 获取图片文件夹中所有的jpg文件
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

# 创建一个PDF文件
pdf_filename = "output.pdf"
c = canvas.Canvas(pdf_filename)

# 遍历图片文件列表
for image_file in image_files:
    # 打开图片文件
    image_path = os.path.join(image_folder, image_file)
    im = Image.open(image_path)

    # 获取图片的尺寸
    width, height = im.size

    # 将图片绘制到PDF中
    c.setPageSize((width, height))
    c.drawImage(image_path, 0, 0)

    # 添加新的页
    c.showPage()

# 保存PDF文件并关闭画布
c.save()

print("图片已成功转换为PDF文件：", pdf_filename)