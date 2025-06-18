import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image


def clear_folder(folder_path):
    """
    清空指定文件夹。

    参数：
        folder_path (str): 需要清空的文件夹路径。
    """
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)  # 删除文件
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)  # 删除子文件夹
            except Exception as e:
                print(f"无法删除 {file_path}: {e}")


def save_images_from_html(html_content, save_folder="images"):
    """
    从HTML内容中提取图片并下载到本地文件夹。

    参数：
        html_content (str): HTML内容。
        save_folder (str): 保存图片的本地文件夹路径。
    """
    try:
        # 解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 查找所有图片标签及其对应的页码
        img_tags = soup.find_all('li')

        # 创建保存图片的文件夹
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        images = []

        # 下载图片并保存到本地
        for img_tag in img_tags:
            img_url = img_tag.find('img').get('src')
            page_num = img_tag.find('span', class_='pageNum').text.strip()

            if not img_url:
                continue

            # 获取图片内容
            try:
                img_data = requests.get(img_url).content
                img_name = f"{page_num}.png"  # 使用页码作为文件名
                save_path = os.path.join(save_folder, img_name)

                # 保存图片到本地
                with open(save_path, 'wb') as img_file:
                    img_file.write(img_data)

                images.append((page_num, save_path))  # 保存页码和路径
                print(f"已保存图片: {save_path}")
            except Exception as e:
                print(f"无法下载图片 {img_url}: {e}")

        # 按照页码排序图片
        images.sort(key=lambda x: int(x[0]))  # 按照数字顺序排序

        return [img[1] for img in images]  # 返回排序后的图片路径列表

    except Exception as e:
        print(f"发生错误: {e}")
        return []


def images_to_pdf(image_paths, output_pdf="output.pdf"):
    """
    将指定的图片路径列表转换为单个PDF文件。

    参数：
        image_paths (list): 图片路径列表。
        output_pdf (str): 生成的PDF文件路径。
    """
    try:
        # 确保有图片可供转换
        if not image_paths:
            print("没有找到图片文件，无法生成PDF。")
            return

        # 打开图片并转换为PDF格式
        image_list = []
        for image_path in image_paths:
            img = Image.open(image_path).convert("RGB")
            image_list.append(img)

        # 保存为PDF
        image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:])
        print(f"PDF文件已生成: {output_pdf}")

    except Exception as e:
        print(f"生成PDF时发生错误: {e}")


if __name__ == "__main__":
    # 示例HTML，可以替换为实际HTML内容
    html_content =''''''
    image_folder = "images"

    # 清空图片文件夹
    clear_folder(image_folder)

    # 保存图片并获取排序后的图片路径列表
    image_paths = save_images_from_html(html_content, save_folder=image_folder)

    # 将排序后的图片转换为PDF
    images_to_pdf(image_paths, output_pdf="output.pdf")


