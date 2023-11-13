import json
from collections import defaultdict
from datetime import datetime, timedelta
import os

# 找到当前目录下的所有json文件
def find_json_files(directory):
    return [file for file in os.listdir(directory) if file.endswith('.json')]

def get_building():
    buildings = {
        '1': '2-',
        '2': '3-',
        '3': '4-',
        '4': '图书馆一层-',
        '5': '经管楼-'
    }
    while True:
        choice = input("想去哪个楼睡觉：\n1. 教二\n2. 教三\n3. 教四\n4. 图书馆一层\n5. 经管楼\n输入对应数字选择，或输入exit退出: ")
        if choice in buildings:
            return buildings[choice]
        elif choice.lower() == 'exit':
            exit()
        else:
            print("输入有误，请输入对应的数字选择。")

# 获取用户想查询的时间段
def get_time_of_day():
    while True:
        period = input("请输入你要查询的时间段，上午/下午/全天/自定义 (输入1/2/3/4)").lower()
        if period in ['1', '2', '3', '4', 'exit']:
            return period
        else:
            print("输入有误，请输入1/2/3/4进行查询。")

# 检查时间段是否符合查询要求
def is_time_in_period(start, end, period, custom_start=None, custom_end=None):
    morning_end = datetime.strptime('12:20', '%H:%M')
    afternoon_start = morning_end
    if period == '1':  # 上午
        return start < morning_end
    elif period == '2':  # 下午
        return end >= afternoon_start
    elif period == '3':  # 全天
        return True
    elif period == '4' and custom_start and custom_end:  # 自定义时间段
        return start >= custom_start and end <= custom_end
    return False

# 解析自定义时间段
def parse_custom_period():
    while True:
        period_str = input("请输入自定义的时间区间（例如 13:00-15:00）: ")
        try:
            start_str, end_str = period_str.split('-')
            start_dt = datetime.strptime(start_str.strip(), '%H:%M')
            end_dt = datetime.strptime(end_str.strip(), '%H:%M')
            return start_dt, end_dt
        except ValueError:
            print("时间格式错误，请按照 'HH:MM-HH:MM' 的格式输入。")

# 合并时间段
def merge_time_slots(slots):
    merged_slots = []
    for start, end in sorted(slots):
        if not merged_slots or start - merged_slots[-1][1] > timedelta(minutes=10):
            merged_slots.append([start, end])
        else:
            merged_slots[-1][1] = max(merged_slots[-1][1], end)
    return merged_slots

# 主循环
def main_loop(data, building_prefix):
    while True:
        time_of_day = get_time_of_day()
        if time_of_day == 'exit':  # 用户选择退出
            break

        custom_start, custom_end = None, None
        if time_of_day == '4':  # 如果用户选择自定义时间段
            custom_start, custom_end = parse_custom_period()

        classroom_free_time = defaultdict(list)
        for entry in data["data"]:
            start_time, end_time = entry["NODETIME"].split("-")
            start_dt = datetime.strptime(start_time, '%H:%M')
            end_dt = datetime.strptime(end_time, '%H:%M')

            if is_time_in_period(start_dt, end_dt, time_of_day, custom_start, custom_end):
                for classroom in entry["CLASSROOMS"].split(","):
                    if classroom.startswith(building_prefix):  # 根据楼层前缀筛选教室
                        room_number = classroom.split("(")[0]
                        classroom_free_time[room_number].append((start_dt, end_dt))

        # 按照总空闲时间降序排序教室
        sorted_classrooms = sorted(
            classroom_free_time.items(),
            key=lambda item: sum((end - start).total_seconds() for start, end in merge_time_slots(item[1])),
            reverse=True
        )

        for room_number, slots in sorted_classrooms:
            merged_slots = merge_time_slots(slots)
            total_free_time = sum((end - start).total_seconds() for start, end in merged_slots if (not custom_start and not custom_end) or (start >= custom_start and end <= custom_end))
            print(f"教室 {room_number} 在选择的时间段内共有 {total_free_time / 60:.0f} 分钟的空闲时间。空闲时间段如下：")
            for start, end in merged_slots:
                if (not custom_start and not custom_end) or (start >= custom_start and end <= custom_end):
                    print(f"  {start.strftime('%H:%M')} 到 {end.strftime('%H:%M')}")
            print()
# 脚本开始
if __name__ == "__main__":
    directory = os.getcwd()
    json_files = find_json_files(directory)

    if len(json_files) == 0:
        print("请将json文件放于和脚本相同的文件夹内")
    elif len(json_files) > 1:
        print("请确保文件夹中只有一个json文件")
    else:
        building_prefix = get_building()  # 获取用户选择的楼层前缀
        file_path = os.path.join(directory, json_files[0])
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        main_loop(data, building_prefix)  # 传递楼层前缀到主循环
