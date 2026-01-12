import csv
import json
import os

file_path = r"e:\AI测试用例\接口测试\data\intent_recognition_test_data.csv"
temp_file_path = r"e:\AI测试用例\接口测试\data\intent_recognition_test_data_fixed.csv"

def fix_csv():
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, mode='r', encoding='utf-8', newline='') as infile, \
         open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.DictReader(infile, delimiter='|')
        fieldnames = reader.fieldnames
        
        # 检查 text 字段是否存在
        if 'text' not in fieldnames:
            # 如果不存在，插入到 history 之后
            new_fieldnames = []
            for field in fieldnames:
                new_fieldnames.append(field)
                if field == 'history':
                    new_fieldnames.append('text')
            fieldnames = new_fieldnames
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        
        for row in reader:
            history_str = row.get('history', '')
            extracted_text = ''
            
            if history_str:
                try:
                    # 尝试解析 JSON
                    # CSV 读取时会自动处理双引号转义，所以这里得到的应该是标准的 JSON 字符串
                    # 但如果原始数据是 "[{""role""...}]" 这种格式，csv 模块读取后应该是 [{"role"...}]
                    history_data = json.loads(history_str)
                    
                    if isinstance(history_data, list) and len(history_data) > 0:
                        last_message = history_data[-1]
                        if isinstance(last_message, dict):
                            extracted_text = last_message.get('text', '')
                except json.JSONDecodeError as e:
                    print(f"JSON decode error for row {row.get('user_id')}: {e}")
                except Exception as e:
                    print(f"Error processing row {row.get('user_id')}: {e}")
            
            # 更新或设置 text 字段
            row['text'] = extracted_text
            writer.writerow(row)

    print("CSV fixed successfully.")

if __name__ == "__main__":
    fix_csv()
