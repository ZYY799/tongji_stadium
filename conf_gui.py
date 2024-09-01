import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
import sys
from conf import basic_info_input
import tkinter.font as tkFont

class RedirectText(object):
    def __init__(self, text_widget):
        self.output = text_widget

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)  # 自动滚动到底部

    def flush(self):
        pass

def browse_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def update_complexes_name(*args):
    selected_sport = sports_type_var.get()
    complexes_name_entry['values'] = complexes_options.get(selected_sport, [])
    if complexes_options.get(selected_sport):
        complexes_name_entry.set(complexes_options[selected_sport][0])
    else:
        complexes_name_entry.set('')

def run_script():
    try:
        # 获取用户输入的信息
        config = {
            'driver_path': driver_path_entry.get(),
            'url_input': url_input_entry.get(),
            'sleep_time': int(sleep_time_entry.get()),
            'password_path': password_path_entry.get(),
            'sports_type': sports_type_var.get(),
            'complexes_name': complexes_name_entry.get(),
            'date_data': date_data_entry.get(),
            'time_threshold': time_threshold_entry.get(),
            'time_choice': int(time_choice_entry.get()),
            'selected_seat_index': int(selected_seat_index_entry.get()),
            'response_time': float(response_time_entry.get()),
            'chrome_path': chrome_path_entry.get(),
            'selected_seat_index_alt': [int(x) for x in selected_seat_index_alt_entry.get().strip('[]').split(',')],
            'time_choice_limit': int(time_choice_limit_entry.get()),
            'zy_mode': zy_mode_var.get()
        }

        # 使用独立线程运行脚本以避免阻塞GUI
        threading.Thread(target=basic_info_input, kwargs=config).start()
        messagebox.showinfo("Success", "The script is running in the background.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

app = tk.Tk()
app.title("配置页面（部分参考值请勿随意修改）")

bold_red_color = "red"

labels = ["Driver Path", "URL Input", "Sleep Time (seconds)", "Password File Path",
          "Sports Type", "Complexes Name", "Date Data", "Time Threshold (HH:MM:SS.fff)",
          "Time Choice 预约时间点", "Selected Seat Index 选择几号场地", "Response Time (seconds)", "Chrome Path",
          "Selected Seat Index Alt (comma-separated)", "Time Choice Limit", "Enable ZY Mode"]

default_values = [
    "chromedriver.exe", "https://stadium.tongji.edu.cn", "3", "credentials.txt",
    "网球", "四平校区南大道网球场", "2024-09-08", "23:00", "10", "1", "0.25",
    "chrome-win64\\chrome.exe", "[1, 2, 4]", "21"
]

complexes_options = {
    "羽毛球": ["四平校区攀岩馆", "四平校区一·二九训练馆"],
    "网球": ["四平校区南大道网球场"],
    "乒乓球": []  # 空选项表示可以自行输入
}

entries = []
for i, (label, default_value) in enumerate(zip(labels, default_values)):
    color = bold_red_color if label in ["Sports Type", "Complexes Name","Time Choice 预约时间点", "Selected Seat Index 选择几号场地", "Response Time (seconds)"] else None

    tk.Label(app, text=label, fg=color).grid(row=i, column=0, sticky=tk.W)
    if label == "Sports Type":
        sports_type_var = tk.StringVar()
        sports_type_entry = ttk.Combobox(app, textvariable=sports_type_var, values=list(complexes_options.keys()))
        sports_type_entry.grid(row=i, column=1)
        sports_type_var.set(default_value)
        sports_type_var.trace("w", update_complexes_name)
        entries.append(sports_type_entry)
    elif label == "Complexes Name":
        complexes_name_entry = ttk.Combobox(app, values=complexes_options.get(default_values[4], []))
        complexes_name_entry.grid(row=i, column=1)
        complexes_name_entry.set(default_value)
        entries.append(complexes_name_entry)
    else:
        entry = tk.Entry(app, width=50)
        entry.insert(0, default_value)  # 设置默认值
        entry.grid(row=i, column=1)
        entries.append(entry)

driver_path_entry = entries[0]
url_input_entry = entries[1]
sleep_time_entry = entries[2]
password_path_entry = entries[3]
sports_type_entry = entries[4]
complexes_name_entry = entries[5]
date_data_entry = entries[6]
time_threshold_entry = entries[7]
time_choice_entry = entries[8]
selected_seat_index_entry = entries[9]
response_time_entry = entries[10]
chrome_path_entry = entries[11]
selected_seat_index_alt_entry = entries[12]
time_choice_limit_entry = entries[13]

tk.Button(app, text="Browse", command=lambda: browse_file(driver_path_entry)).grid(row=0, column=2)
tk.Button(app, text="Browse", command=lambda: browse_file(password_path_entry)).grid(row=3, column=2)
tk.Button(app, text="Browse", command=lambda: browse_file(chrome_path_entry)).grid(row=11, column=2)

zy_mode_var = tk.BooleanVar(value=False)
tk.Checkbutton(app, text="zy_model", variable=zy_mode_var).grid(row=14, column=1, sticky=tk.W)

output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=60, height=20, state='normal')
output_text.grid(row=16, column=0, columnspan=3, pady=10)

sys.stdout = RedirectText(output_text)

tk.Button(app, text="Run (点击运行)", command=run_script).grid(row=15, column=0, columnspan=3, pady=10)

app.mainloop()
