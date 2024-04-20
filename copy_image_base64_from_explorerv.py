import win32com.client
import base64
import pyperclip
import keyboard
import pythoncom


# 使用上下文管理器初始化和释放COM
class ComContext:
    def __enter__(self):
        pythoncom.CoInitialize()

    def __exit__(self, exc_type, exc_value, traceback):
        pythoncom.CoUninitialize()


# 获取资源管理器中选中的文件路径
def get_selected_files_from_explorer():
    with ComContext():  # 初始化COM
        shell = win32com.client.Dispatch("Shell.Application")
        windows = shell.Windows()

        selected_files = []

        for window in windows:
            if "explorer" in window.FullName.lower() or "资源管理器" in window.FullName.lower():
                items = window.Document.SelectedItems()
                for item in items:
                    selected_files.append(item.Path)

        return selected_files


# 检查文件是否是图片文件
def is_image_file(file_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    return any(file_path.lower().endswith(ext) for ext in image_extensions)


# 将文件转换为Base64编码
def file_to_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# 主函数
def main():

    selected_files = get_selected_files_from_explorer()

    # 获取图片Base64，并复制到剪贴板。不支持多张照片。
    if len(selected_files) > 1:
        image_files = [file for file in selected_files if is_image_file(file)]

        if len(image_files) == 1:
            base64_data = file_to_base64(image_files[0])
            pyperclip.copy(base64_data)
            print(f"Base64 data of the selected image has been copied to clipboard.")
        else:
            print("Please select only one image file.")
    elif len(selected_files) == 1:
        if is_image_file(selected_files[0]):
            base64_data = file_to_base64(selected_files[0])
            pyperclip.copy(base64_data)
            print(f"Base64 data of the selected image has been copied to clipboard.")
        else:
            print("The selected file is not an image.")
    else:
        print("No files selected.")


print(f"Start")

# 使用快捷键触发函数
keyboard.add_hotkey('ctrl+b', main)

keyboard.wait('esc')  # 保持程序运行，直到按下'esc'键
