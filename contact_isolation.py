import json
import os

INPUT_FILE = 'survey_ans.json'
CONTACT_FILE = 'contacts.json'

with open(INPUT_FILE) as f:
    survey = json.load(f)

contacts = []
for entry in survey:
    person = {}
    person['ID'] = entry['ID']
    person['name'] = entry['名前']
    person['email'] = entry['メール']
    contacts.append(person)

with open(CONTACT_FILE, 'w') as f:
    json.dump(contacts, f, ensure_ascii=False, indent=4)

print('連絡先情報を保存しました。')
print('\tFILE:', CONTACT_FILE)

for entry in survey:
    del entry['メール']
    del entry['名前']

with open(INPUT_FILE, 'w') as f:
    json.dump(survey, f, ensure_ascii=False, indent=4)

print('個人情報を削除しました。')

# パスワードで暗号化
# GPGがない場合はコメントアウトしてください。
# """"
os.system('gpg -c ' + CONTACT_FILE)
os.remove(CONTACT_FILE)
# """"
