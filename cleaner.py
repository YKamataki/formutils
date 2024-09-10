import json
import re

SURVEY_FILE = 'survey_ans.json'

def normal_int_parse(s:str) -> int:
    # 数字があればそれを返す
    m = re.search(r'\d+', s)
    if m:
        return int(m.group())
    else:
        return None

def hours_and_minutes_parse(s:str) -> float:
    # N時間またはNhの形式であればそれを返す
    m = re.search(r'(\d+)時間', s)
    if m:
        return int(m.group(1))
    m = re.search(r'(\d+)h', s)
    if m:
        return int(m.group(1))
    # N分またはNmの形式であればそれを時間に変換して返す
    m = re.search(r'(\d+)分', s)
    if m:
        return int(m.group(1)) / 60
    m = re.search(r'(\d+)m', s)
    if m:
        return int(m.group(1)) / 60
    return None

with open(SURVEY_FILE) as f:
    survey = json.load(f)
print("アンケートデータを読み込みました。")
print("\tFILE:", SURVEY_FILE)

output = []
# IDをintにする
for entry in survey:
    entry['ID'] = int(entry['ID'])
    output.append(entry)
print("IDをintに変換しました。")

# キーのrenameと削除
old_keys = [x for x in output[0].keys()]
new_keys = []
print("キーのリネームと削除を行います。")
print("新しいキーを入力してください。")
print("変更しない場合はそのままEnterを押してください。")
print("削除する場合はremoveと入力してください。")
# プロンプト
for key in old_keys:
    new_key = input(f"{key} \n\t-> ")
    if new_key == "":
        new_keys.append(key)
    else:
        new_keys.append(new_key)

for entry in output:
    for i in range(len(old_keys)):
        if new_keys[i] == "remove":
            del entry[old_keys[i]]
        elif new_keys[i] != old_keys[i]:
            entry[new_keys[i]] = entry.pop(old_keys[i])
print("キーのリネームと削除が完了しました。")

# 年齢などを数値にパース
for key in output[0].keys():
    if input(f"{key}を数値に変換しますか?(y/N) ") == "y":
        print("パース方法を選択してください。")
        print("\t1: 数字があればそれを返す\n\t2: 時間または分をパースする(出力は時間)")
        p = input("parser type: ")
        if p == "1":
            for entry in output:
                entry[key] = normal_int_parse(entry[key])
        elif p == "2":
            for entry in output:
                entry[key] = hours_and_minutes_parse(entry[key])
print("数値へのパースが完了しました。")

# "その他"が空欄のとき、リストから削除
# リストの最後が"その他"に対応していると仮定
for entry in output:
    for key in entry.keys():
        # 値はリストか
        if isinstance(entry[key], list):
            # 最後が空欄か
            if entry[key][-1] == "":
                entry[key].pop()
print("リストから空の'その他'を削除しました。")

# 出力
print("出力先を指定するか、そのままEnterを押してください。")
print("そのままEnterを押すと元のファイルに上書きされます。")
output_file = input("output file: ")
if output_file == "":
    output_file = SURVEY_FILE
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)
print("アンケートデータを保存しました。")
print("\tFILE:", output_file)