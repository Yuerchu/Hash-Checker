import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
import hashlib
import os
import configparser
import threading
from sv_ttk import *

# 读取ini文件，没有则创建
config = configparser.ConfigParser()
config.read('sv_config.ini', encoding='utf-8')
try:
    theme = config.get('config','theme')
    lang = config.get('config','lang')
except:
    # 程序首次启动，需要初始化
    config.add_section('config')
    config.set('config','theme','light')
    config.set('config','lang','zh_cn')
    with open('sv_config.ini', 'w') as configfile:
        config.write(configfile)
    
    theme = config.get('config','theme')
    lang = config.get('config','lang')

md5 = "0"
sha256 = "0"

#语言相关
zh_cn = {'load':'选择文件：','select':'浏览……','sizeprepare':'大小：等待导入','progress':'        进度：','result':'输出结果：','option':'首选项'}
en_us = {'load':'File dir:','select':'Open..','sizeprepare':'size:No file','progress':'Progress:','result':'Result:','option':'Option'}

lang = zh_cn

# 首选项相关代码
def StartOptionPage():
    def SaveOption():
        ThemeChoose = ThemeCombobox.get()
        if ThemeChoose == '浅色 Light':
            config.set('config','theme','light')
            set_theme('light')
            theme = 'light'
        elif ThemeChoose == '深色 Dark':
            config.set('config','theme','dark')
            set_theme('dark')
            theme = 'dark'
        with open('sv_config.ini', 'w') as configfile:
            config.write(configfile)
            OptionPage.destroy()
    
    OptionPage = tk.Tk()
    OptionPage.title("Hash Checker 首选项")
    OptionPage.geometry(f"{700}x{300}")
    OptionPage.iconbitmap('.\\icon.ico')
    OptionPage.resizable(width=False, height=False)

    WarningLabel = ttk.Label(OptionPage, text="将程序作为携带版使用时，请一并拷贝config.ini文件，否则设置不会被保存")
    WarningLabel.place(x=20,y=25)

    ThemeLabel = ttk.Label(OptionPage, text="主题")
    ThemeLabel.place(x=20, y=60)

    ThemeCombobox = ttk.Combobox(OptionPage, width=15,)
    if theme == 'light':
        ThemeCombobox['values'] = ('浅色 Light','深色 Dark')
    elif theme == 'dark':
        ThemeCombobox['values'] = ('深色 Dark','浅色 Light')
    ThemeCombobox.current(0)
    ThemeCombobox.place(x=150, y=60)

    SaveButton = ttk.Button(OptionPage, text="保存",command=SaveOption)
    SaveButton.place(x=575, y=250)

    OptionPage.mainloop()

def OpenFile():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    else:
        InputFileEntry.delete(0, 'end')
        InputFileEntry.insert(0, file_path)
        fsize = os.path.getsize(file_path)
        if fsize < 1024:
            SizePrint = '大小：', round(fsize, 2), '字节'
        else:
            KBX = fsize / 1024
            if KBX < 1024:
                SizePrint = '大小：', round(KBX, 2), 'KB'
            else:
                MBX = KBX / 1024
                if MBX < 1024:
                    SizePrint = '大小：', round(MBX, 2), 'MB'
                else:
                    GBX = MBX / 1024
                    if GBX < 1024:
                        SizePrint = '大小：', round(GBX, 2), 'GB'
        FileSize.configure(text=SizePrint)

def StartCal():
    file_path = InputFileEntry.get()
    if not file_path:
        tkinter.messagebox.showerror('错误', '文件路径不能为空。')
        return 0

    def calculate():
        MD5Entry.delete(0, 'end')
        SHA256Entry.delete(0, 'end')
        try:
            file_size = os.path.getsize(file_path)
        except:
            tkinter.messagebox.showerror('错误', '找不到指定的文件。')
            return 0
        use_chunking = file_size > CHUNK_SIZE_THRESHOLD

        md5_hash = hashlib.md5()
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                progress_var.set(0)
                root.update_idletasks()
        except:
            tkinter.messagebox.showerror('错误', '找不到指定的文件。\n原始错误信息：No such file or Directory.')
            return 0
        if use_chunking:
            total_chunks = (file_size + CHUNK_SIZE - 1) // CHUNK_SIZE
            chunk_count = 0
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                md5_hash.update(chunk)
                sha256_hash.update(chunk)
                chunk_count += 1
                progress = min(100, int(chunk_count / total_chunks * 100))
                progress_var.set(progress)
                root.update_idletasks()
                progress_label.configure(text=f"{progress_var.get()}%")

        progress_var.set(100)
        md5 = md5_hash.hexdigest()
        sha256 = sha256_hash.hexdigest()
        progress_label.configure(text=f"{progress_var.get()}%  完成！")
        MD5Entry.insert(0, md5)
        SHA256Entry.insert(0, sha256)

    thread = threading.Thread(target=calculate)
    thread.start()

def Checking():
    Input = SmartCheckEntry.get()
    md5 = MD5Entry.get()
    sha256 = SHA256Entry.get()
    if Input == md5:
        ResultLabel.configure(text='这是文件的MD5，文件完整')
    elif Input == sha256:
        ResultLabel.configure(text='这是文件的SHA256，文件完整')
    else:
        ResultLabel.configure(text='输入有误或文件损坏，请检查')

CHUNK_SIZE_THRESHOLD = 8 * 1024 * 1024 * 1024  # 8 GB
CHUNK_SIZE = 4096

root = tk.Tk()
root.title("Hash Checker V0.1.2 开发版本")
root.geometry(f"{700}x{300}")
root.iconbitmap('.\\icon.ico')
root.resizable(width=False, height=False)

InputFileLabel = ttk.Label(text=lang['load'])
InputFileLabel.place(x=20, y=25)

InputFileEntry = ttk.Entry()
InputFileEntry.place(x=90, y=20)

button = ttk.Button(root, text=lang['select'], command=OpenFile)
button.place(x=300, y=20)

FileSize = ttk.Label(text="大小：等待导入")
FileSize.place(x=400, y=25)

OptionButton = ttk.Button(root,text=lang['option'],command=StartOptionPage)
OptionButton.place(x=600, y=20)



ProgressLabel = ttk.Label(text=lang['progress'])
ProgressLabel.place(x=20, y=75)
progress_var = tk.IntVar()
progressBar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progressBar.place(x=100, y=85, width=300)
progress_label = ttk.Label(root)
progress_label.place(x=425, y=75)
OutputLabel = ttk.Label(text="输出结果：")
OutputLabel.place(x=20, y=125)
MD5Label = ttk.Label(text="MD5:")
MD5Label.place(x=90, y=125)
MD5Entry = ttk.Entry()
MD5Entry.place(x=135, y=120, width=300)
SHA256Label = ttk.Label(text="SHA256:")
SHA256Label.place(x=90, y=175)
SHA256Entry = ttk.Entry()
SHA256Entry.place(x=155, y=170, width=540)
SmartCheckLabel = ttk.Label(text="智能比对：")
SmartCheckLabel.place(x=20, y=225)
SmartCheckEntry = ttk.Entry()
SmartCheckEntry.place(x=90, y=220)
Check = ttk.Button(root, text="比对", command=Checking)
Check.place(x=300, y=220)
ResultLabel = ttk.Label()
ResultLabel.place(x=375, y=225)
Version = ttk.Label(text="作者：@于小丘       一个现代化UI的文件MD5与SHA256的检查工具")
Version.place(x=20, y=262.5)
button = ttk.Button(root, text="开始", command=StartCal)
button.place(x=625, y=250)

set_theme(config.get("config", "theme"))

root.mainloop()