import csv
import json

def split_field_if_needed(value):
    """
    フィールドにセミコロンが含まれている場合、それをセミコロンで分割します。
    含まれていない場合は、元の値を返します。
    """
    if ";" in value:
        return value.split(";")
    return value

def csv_to_json(csv_file_path, json_file_path):
    # CSVファイルを読み込み
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # JSON形式でデータを保存するリスト
        data = []
        
        # 各行を辞書としてリストに追加
        for row in csv_reader:
            # セミコロンが含まれているフィールドを分割
            processed_row = {key: split_field_if_needed(value) for key, value in row.items()}
            data.append(processed_row)

    # JSONファイルに書き込み
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

# 使用例
csv_file_path = input('input filename')  # 変換したいCSVファイルのパス
json_file_path = input('output filename')  # 出力するJSONファイルのパス

csv_to_json(csv_file_path, json_file_path)
