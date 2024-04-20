## 简介

这是一个专为Windows系统设计的工具，用于快速获取资源管理器（文件夹）中选中图片文件的Base64编码。

## 背景

由于工作需求经常需要获取图片的Base64并粘贴到postman中调用接口。最开始的做法是使用在线工具将图片转换为Base64编码，这样不仅操作繁琐，而且需要在线转换，可能存在数据泄露的风险。因此，开发了这个工具，可以直接从资源管理器中选中的图片文件中获取Base64编码，大大提高了工作效率并确保数据安全。

## 功能特点

- **从资源管理器中选中图片文件**：用户可以通过资源管理器选择一个图片文件。
- **生成Base64编码**：选中的图片文件将被转换为Base64编码。
- **复制到剪贴板**：生成的Base64编码会自动复制到系统剪贴板，方便粘贴使用。

## 使用方法

1. **打开资源管理器**：导航到你的图片文件所在的目录。
2. **选择图片文件**：使用鼠标单击选中一个或多个图片文件。
3. **运行工具**：按下预设的快捷键（例如，Ctrl+B）来运行工具。
4. **获取Base64编码**：工具会自动获取选中图片文件的Base64编码。
5. **粘贴使用**：你现在可以在其他应用程序中粘贴（Ctrl+V）Base64编码。

## 注意事项

- 仅支持以下图片格式：**.jpg**、**.jpeg**、**.png**、**.gif**、**.bmp**。
- 当选中多个图片文件时，仅支持从中选中一个进行Base64编码。

## 示例

![img](https://github.com/x-brook/copy_image_base64_from_explorerv/blob/main/demo-3m.gif)

## 常见问题

**Q: 我选中了多个图片文件，为什么不能生成Base64编码？** A: 本工具目前仅支持从选中的图片文件中选择一个进行Base64编码。

## 源码

GitHub地址：https://github.com/x-brook/copy_image_base64_from_explorerv

```python
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
```

## 作者简介

鑫茂，深圳，Java开发工程师。

希望通过文章，结识更多同道中人。
