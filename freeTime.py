import json
from collections import defaultdict
from datetime import datetime, timedelta
import os
# 读取JSON数据的函数
def find_json_files(directory):
    return [file for file in os.listdir(directory) if file.endswith('.json')]


# 获取用户想要查询的时间段
def get_time_of_day():
    while True:
        period = input("请输入你要查询的时间段，上午/下午/全天 (输入1/2/3)").lower()
        if period in ['1', '2', '3']:
            return period
        else:
            print("请输入正确格式，上午/下午/全天 (输入1/2/3), 输入4退出")

# 检查时间是否在指定的时间段内
def is_time_in_period(start, end, period):
    morning_end = datetime.strptime('12:20', '%H:%M')
    if period == '1':
        return start < morning_end
    elif period == 'afternoon':
        return end >= morning_end
    return True  # 'all' should return True for all time slots

# 合并时间段的函数
def merge_time_slots(slots):
    merged_slots = []
    for start, end in sorted(slots):
        if not merged_slots or start - merged_slots[-1][1] > timedelta(minutes=5):
            merged_slots.append([start, end])
        else:
            merged_slots[-1][1] = max(merged_slots[-1][1], end)
    return merged_slots

# 主循环函数，处理用户的多次查询
def main_loop(data):
    while True:
        time_of_day = get_time_of_day()
        if time_of_day == "exit":
            break

        classroom_free_time = defaultdict(list)
        for entry in data["data"]:
            start_time, end_time = entry["NODETIME"].split("-")
            start_dt = datetime.strptime(start_time, '%H:%M')
            end_dt = datetime.strptime(end_time, '%H:%M')

            if is_time_in_period(start_dt, end_dt, time_of_day):
                for classroom in entry["CLASSROOMS"].split(","):
                    if classroom.startswith("3-"):
                        room_number = classroom.split("(")[0]
                        classroom_free_time[room_number].append((start_dt, end_dt))

        for room_number, slots in classroom_free_time.items():
            classroom_free_time[room_number] = merge_time_slots(slots)

        sorted_classrooms = sorted(
            classroom_free_time.items(),
            key=lambda item: sum((end - start).total_seconds() for start, end in item[1]),
            reverse=True
        )

        for classroom, slots in sorted_classrooms:
            total_free_time = sum((end - start).total_seconds() for start, end in slots)
            print(f"教三 {classroom} 有 {total_free_time / 60:.0f} 分钟空闲时间，空闲时间如下：")
            for start, end in slots:
                print(f"  {start.strftime('%H:%M')} 到 {end.strftime('%H:%M')}")
            print()

# 脚本执行入口点
if __name__ == "__main__":
    # 获取当前脚本的目录
    directory = os.path.dirname(os.path.abspath(__file__))
    json_files = find_json_files(directory)

    # 检查 JSON 文件的数量
    if not json_files:
        print("请将json文件放于和脚本相同的文件夹内")
    elif len(json_files) > 1:
        print("请确保文件夹中只有一个json文件")
    else:
        # 读取找到的 JSON 文件
        file_path = os.path.join(directory, json_files[0])
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        main_loop(data)
