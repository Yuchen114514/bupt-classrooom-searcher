import json
import requests
import webbrowser
from collections import defaultdict
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox


# 合并时间段
def merge_time_slots(slots):
    merged_slots = []
    for start, end in sorted(slots):
        if not merged_slots or start - merged_slots[-1][1] > timedelta(minutes=15):
            merged_slots.append([start, end])
        else:
            merged_slots[-1][1] = max(merged_slots[-1][1], end)
    return merged_slots


def filter_time_slots(slots, time_of_day, custom_start=None, custom_end=None):
    filtered_slots = []
    for start, end in slots:
        # 转换为仅时间部分进行比较
        start_time = start.time()
        end_time = end.time()
        custom_start_time = custom_start.time() if custom_start else None
        custom_end_time = custom_end.time() if custom_end else None

        if (
            time_of_day == "上午"
            and start_time < datetime.strptime("12:00", "%H:%M").time()
        ):
            filtered_slots.append((start, end))
        elif (
            time_of_day == "下午"
            and start_time >= datetime.strptime("12:00", "%H:%M").time()
        ):
            filtered_slots.append((start, end))
        elif time_of_day == "全天":
            filtered_slots.append((start, end))
        elif time_of_day == "自定义" and custom_start_time and custom_end_time:
            if custom_start_time <= start_time and custom_end_time >= end_time:
                filtered_slots.append((start, end))
    return filtered_slots


# GUI主循环
def gui_main_loop(data):
    window = Tk()
    window.title("空闲教室查询")
    custom_font = font.Font(size=12)

    # 楼层选择
    building_label = Label(window, text="你想在哪睡觉:")
    building_label.pack()
    building_var = StringVar(window)
    building_options = {
        "教二": "2-",
        "教三": "3-",
        "教四": "4-",
        "图书馆一层": "图书馆一层-",
        "经管楼": "经管楼-",
    }
    building_menu = ttk.Combobox(
        window, textvariable=building_var, values=list(building_options.keys())
    )
    building_menu.pack()
    building_menu.current(0)  # 设置默认选项

    # 时间段选择
    period_label = Label(window, text="选择时间段:")
    period_label.pack()
    period_var = StringVar(window)
    period_options = {"1": "上午", "2": "下午", "3": "全天", "4": "自定义"}
    period_menu = ttk.Combobox(
        window, textvariable=period_var, values=list(period_options.values())
    )
    period_menu.pack()
    period_menu.current(0)  # 设置默认选项

    # 自定义时间段输入
    custom_time_label = Label(window, text="自定义时间(例如 13:00-15:00):")
    custom_time_label.pack()
    custom_time_var = StringVar(window)
    custom_time_entry = Entry(window, textvariable=custom_time_var)
    custom_time_entry.pack()

    # 结果显示
    result_label = Label(window, text="查询结果:")
    result_label.pack()
    result_text = Text(window, height=35, width=100, font=custom_font)
    result_text.pack(fill="both", expand=True)

    # 查询按钮
    def query():
        building_prefix = building_options[building_var.get()]
        time_of_day = period_menu.get()
        custom_start, custom_end = None, None

        if time_of_day == "自定义":
            try:
                start_str, end_str = custom_time_var.get().split("-")
                custom_start = datetime.strptime(start_str.strip(), "%H:%M")
                custom_end = datetime.strptime(end_str.strip(), "%H:%M")

            except ValueError:
                messagebox.showerror("错误", "自定义时间格式错误，请按照 'HH:MM-HH:MM' 的格式输入。")
                return

        classroom_free_time = defaultdict(list)
        for entry in data["data"]:
            start_time, end_time = entry["NODETIME"].split("-")
            start_dt = datetime.strptime(start_time, "%H:%M")
            end_dt = datetime.strptime(end_time, "%H:%M")
            # 根据楼层前缀筛选教室
            for classroom in entry["CLASSROOMS"].split(","):
                if classroom.startswith(building_prefix):
                    room_number = classroom.split("(")[0]
                    classroom_free_time[room_number].append((start_dt, end_dt))

        # 在过滤并合并时间段后进行排序
        for room_number, slots in classroom_free_time.items():
            filtered_slots = filter_time_slots(
                slots, time_of_day, custom_start, custom_end
            )
            merged_slots = merge_time_slots(filtered_slots)
            classroom_free_time[room_number] = merged_slots

        # 按照总空闲时间降序排序教室
        sorted_classrooms = sorted(
            classroom_free_time.items(),
            key=lambda item: sum(
                (end - start).total_seconds() for start, end in item[1]
            ),
            reverse=True,
        )

        # 清空结果显示
        result_text.delete("1.0", END)
        for room_number, slots in sorted_classrooms:
            # 在这里，我们先合并时间段，然后计算总空闲时间
            merged_slots = merge_time_slots(slots)
            total_free_time = sum(
                (end - start).total_seconds() for start, end in merged_slots
            )

            # 只有当总空闲时间大于0时，才显示该教室
            if total_free_time > 0:
                result_text.insert(
                    END,
                    f"教室 {room_number} 在选择的时间段内共有 {total_free_time / 60:.0f} 分钟的空闲时间。\n",
                )
                for start, end in merged_slots:
                    result_text.insert(
                        END, f"  {start.strftime('%H:%M')} 到 {end.strftime('%H:%M')}\n"
                    )
                result_text.insert(END, "\n")

    query_button = Button(window, text="查询", command=query)
    query_button.pack()

    window.mainloop()


def token_input_window():
    token_window = Tk()
    token_window.title("Token 输入")
    token_window.geometry("300x150")

    token_label = Label(token_window, text="请输入Token:")
    token_label.pack()
    token_frame = Frame(token_window)  # 创建一个框架来包含输入框和粘贴按钮
    token_frame.pack()

    token_var = StringVar(token_window)
    token_entry = Entry(token_frame, textvariable=token_var)
    token_entry.pack(side=LEFT)

    def paste_from_clipboard():
        try:
            # 从剪贴板获取文本并插入到输入框
            clipboard_text = token_window.clipboard_get()
            token_entry.insert(0, clipboard_text)
        except:
            messagebox.showerror("错误", "无法从剪贴板粘贴")

    paste_button = Button(token_frame, text="粘贴", command=paste_from_clipboard)
    paste_button.pack(side=LEFT)

    status_label = Label(token_window, text="")
    status_label.pack()

    def validate_token():
        status_label.config(text="验证中，请稍候...")
        token_window.update_idletasks()

        token = token_var.get()
        try:
            response = requests.post(
                url="https://jwglweixin.bupt.edu.cn/bjyddx/todayClassrooms?campusId=01",
                headers={"token": token},
            )
            if "3-" in response.text:
                data = json.loads(response.text)
                token_window.destroy()
                gui_main_loop(data)
            else:
                status_label.config(text="Token 验证失败，请重新输入。")
        except Exception as e:
            status_label.config(text=f"验证错误: {e}")

    confirm_button = Button(token_window, text="确认", command=validate_token)
    confirm_button.pack()

    def open_link():
        webbrowser.open("https://github.com/Yuchen114514/bupt-classrooom-searcher")

    link_label = Label(
        token_window, text="如何获取Token？点击访问GitHub查看readme", fg="blue", cursor="hand2"
    )
    link_label.pack()
    link_label.bind("<Button-1>", lambda e: open_link())

    token_window.mainloop()


# 脚本开始
if __name__ == "__main__":
    token_input_window()
