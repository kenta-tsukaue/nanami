import os
import json
import shutil

# delete_list.jsonファイルを読み込む
with open('delete_list.json', 'r') as f:
    delete_list = json.load(f)

# 対象となるディレクトリ名とサブディレクトリ名のリスト
titles = ['bowl', 'omret', 'pasta', 'salad', 'soup']
fonts = ['DelaGothic', 'HachiMaruPop', 'KaiseiDecol', 'NotoSansJP', 'NotoSerif', 'Reggae', 'Stick']

base_dir = 'imgs_pre'
new_base_dir = 'imgs'

# 新しいディレクトリを作成
os.makedirs(new_base_dir, exist_ok=True)

# 削除リストの数が50に満たない場合はエラーを出力
for title in titles:
    if len(delete_list[title]) < 50:
        raise ValueError(f"The delete list for {title} has less than 50 items.")

# 指定された画像を削除
for title in titles:
    for font in fonts:
        font_dir = os.path.join(base_dir, f'img_title_{title}', font)
        if os.path.exists(font_dir):
            for num in delete_list[title]:
                img_path = os.path.join(font_dir, f'{num}_{font}.jpg')
                if os.path.exists(img_path):
                    os.remove(img_path)

# 残った画像を連番にリネームして新しいディレクトリに保存
for title in titles:
    for font in fonts:
        font_dir = os.path.join(base_dir, f'img_title_{title}', font)
        new_font_dir = os.path.join(new_base_dir, f'img_title_{title}', font)
        os.makedirs(new_font_dir, exist_ok=True)
        
        if os.path.exists(font_dir):
            images = sorted(os.listdir(font_dir))
            for idx, img in enumerate(images):
                old_img_path = os.path.join(font_dir, img)
                new_img_name = f'{idx + 1}_{font}.jpg'
                new_img_path = os.path.join(new_font_dir, new_img_name)
                
                # 新しいディレクトリに移動
                shutil.move(old_img_path, new_img_path)
                if os.path.exists(new_img_path):
                    print(f'Successfully moved {old_img_path} to {new_img_path}')
                else:
                    print(f'Failed to move {old_img_path} to {new_img_path}')

# 新しいディレクトリのファイルリストを表示（デバッグ用）
for title in titles:
    for font in fonts:
        new_font_dir = os.path.join(new_base_dir, f'img_title_{title}', font)
        if os.path.exists(new_font_dir):
            print(f'Files in {new_font_dir}:')
            print(sorted(os.listdir(new_font_dir)))