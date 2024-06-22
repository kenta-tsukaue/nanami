import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import pandas as pd


class ImageApp:
    def __init__(self, root):
        self.root = root
        self.zero = True
        self.step = 0
        self.root.title("Image Viewer")
        
        self.folder_path = os.path.join(os.getcwd(), "imgs")
        self.tutorial_folder_path = os.path.join(os.getcwd(), "test_img")
        self.current_set_index = 0
        self.images_set = []
        self.tutorial_images_set = []
        self.state_file = "image_viewer_state.json"
        self.load_state()
        
        self.red_labels = []
        self.blue_labels = []
        self.score_dict = {}
        self.results_file = "results.csv"
        self.df = self.load_or_create_results()

        # チュートリアルタイトルとボタン
        self.title = tk.Label(self.root, text="チュートリアル", font=("Helvetica", 50))
        self.title.grid(row=0, column=0, columnspan=5, pady=300, padx=540)
        self.start_button = tk.Button(root, text="開始", command=self.on_next_button_click, font=("Helvetica", 16), width=20, height=5)
        self.start_button.place(x=600, y=400)

        # 本番タイトルとボタン
        self.title_h = tk.Label(self.root, text="本番", font=("Helvetica", 50))
        #self.title_h.grid(row=0, column=0, columnspan=5, pady=300, padx=600)
        self.start_button_h = tk.Button(root, text="開始", command=self.on_next_button_click, font=("Helvetica", 16), width=20, height=5)
        #self.start_button_h.place(x=600, y=400)

        # 説明文を追加
        self.description_text = tk.Text(root, height=8, width=100, font=("Helvetica", 14), wrap="word", borderwidth=0)
        description = (
            "『魅力的である』と感じる料理画像を【左クリック】で【2枚】選択してください.\n"
            "『魅力的でない』と感じる料理画像を【右クリック】で【2枚】選択してください.\n"
            "全ての選択が終了したら【ウィンドウ上の（次へ）】あるいは【Enterキー】を押して次へ進んでください.\n"
            "※注意事項\n"
            "『魅力度』とは『フォントの印象が料理画像の印象に合っており，直感的に美味しさを想起させる度合い』と定義します.\n"
            "料理画像を選択する際には,テキストの配置やテキストの色は無視して考えてください."
        )

        self.description_text.insert("1.0", description)
        
         # 太文字にする範囲を設定
        bold_ranges = [
            ("1.1", "1.7"),     # 魅力的である
            ("2.1", "2.8"),     # 魅力的でない
            ("1.20", "1.27"),   # 【左クリック】
            ("2.20", "2.27"),   # 【右クリック】
            ("1.28", "1.32"),   # 【2枚】
            ("2.28", "2.32"),   # 【2枚】
            ("3.16", "3.29"),   # 【ウィンドウ上の（次へ）】
            ("3.30", "3.39")    # 【Enterキー】
        ]

        for start, end in bold_ranges:
            self.description_text.tag_add("bold", start, end)

        self.description_text.tag_config("bold", font=("Helvetica", 14, "bold"))        
    

        # 画像ラベルを配置
        self.image_labels = [tk.Label(root, borderwidth=2, relief="solid", highlightbackground="white", highlightthickness=7) for _ in range(7)]

        self.next_button = tk.Button(root, text="次へ", command=self.on_next_button_click, font=("Helvetica", 16), width=20, height=10)
        #self.next_button.grid(row=2, column=3, pady=5)  # Nextボタンを画像の横に配置

        self.root.bind('<Return>', lambda event: self.on_next_button_click())


        self.image_labels = [tk.Label(root, borderwidth=2, relief="solid", highlightbackground="white", highlightthickness=7) for _ in range(7)]
        self.text_labels = [tk.Label(root, text="", font=("Helvetica", 16, "bold"), fg="white", bg="red", width=20, height=1) for _ in range(7)]
        self.load_images()
        self.load_tutorial_images()

    def load_or_create_results(self):
        if os.path.exists(self.results_file):
            df = pd.read_csv(self.results_file)
            print("Loaded results.csv")
        else:
            titles = ['img_title_bowl', 'img_title_omret', 'img_title_pasta', 'img_title_salad', 'img_title_soup']
            fonts = ['DelaGothic', 'HachiMaruPop', 'KaiseiDecol', 'NotoSansJP', 'NotoSerif', 'Reggae', 'Stick']
            data = []
            for title in titles:
                for font in fonts:
                    for i in range(1, 101):
                        data.append([title, font, i, 0, 0, 0])
            df = pd.DataFrame(data, columns=['title', 'font', 'number', '5', '1', '0'])
            df.to_csv(self.results_file, index=False)
            print("Created new results.csv")
        return df

    def load_images(self):
        titles = ['img_title_bowl', 'img_title_omret', 'img_title_pasta', 'img_title_salad', 'img_title_soup']
        fonts = ['DelaGothic', 'HachiMaruPop', 'KaiseiDecol', 'NotoSansJP', 'NotoSerif', 'Reggae', 'Stick']
        
        image_collections = {
            'img_title_bowl': [],
            'img_title_omret': [],
            'img_title_pasta': [],
            'img_title_salad': [],
            'img_title_soup': []
        }

        for title in titles:
            title_path = os.path.join(self.folder_path, title)
            if os.path.exists(title_path):
                for i in range(1, 101):
                    image_set = []
                    for font in fonts:
                        font_path = os.path.join(title_path, font, f"{i}_{font}.jpg")
                        if os.path.exists(font_path):
                            image_set.append(font_path)
                    if len(image_set) == len(fonts):
                        image_collections[title].append(image_set)

        if self.current_set_index == 0:
            for key in image_collections:
                random.shuffle(image_collections[key])
            
            all_images = []
            while any(image_collections.values()):
                for title in titles:
                    for _ in range(5):
                        if image_collections[title]:
                            all_images.append(image_collections[title].pop(0))
            
            self.images_set = all_images[:500]
            self.save_state()
        else:
            self.load_images_set()
    
    def load_tutorial_images(self):
        fonts = ['DelaGothic', 'HachiMaruPop', 'KaiseiDecol', 'NotoSansJP', 'NotoSerif', 'Reggae', 'Stick']
        for font in fonts:
            img_path = os.path.join(self.tutorial_folder_path, f"test_{font}.jpg")
            if os.path.exists(img_path):
                self.tutorial_images_set.append(img_path)

    def display_next_set(self):
        self.description_text.grid(row=0, column=0, columnspan=5, pady=10)
        self.next_button.grid(row=2, column=3, pady=5)  # Nextボタンを画像の横に配置
        print(f"Displaying set {self.current_set_index}")  # デバッグ情報
        if self.current_set_index < len(self.images_set):
            self.reset_label_borders()  # 追加：枠の色をリセット
            image_paths = self.images_set[self.current_set_index]
            for idx, img_path in enumerate(image_paths):
                try:
                    img = Image.open(img_path)
                    img.thumbnail((280, 280)) #ここで画像サイズ調整
                    img = ImageTk.PhotoImage(img)
                    label = self.image_labels[idx]
                    label.config(image=img)
                    label.image = img
                    label.image_path = img_path  # ここで画像パスをラベルに格納
                    label.bind("<Button-1>", lambda e, l=label, t=self.text_labels[idx]: self.on_left_click(l, t))
                    label.bind("<Button-2>", lambda e, l=label, t=self.text_labels[idx]: self.on_right_click(l, t))
                    label.grid(row=idx // 4 + 1, column=idx % 4, padx=30, pady=8) #ここで画像サイズ調整
                    text_label = self.text_labels[idx]
                    text_label.grid(row=idx // 4 + 1, column=idx % 4, padx=30, pady=8, sticky="n")
                    text_label.lower()
                    print(f"Label {idx} placed at row {idx // 3 + 1}, column {idx % 3}")  # デバッグ情報
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")  # エラーメッセージ
            if self.current_set_index % 25 == 0:
                if self.zero:
                    self.zero = False
                else:
                    self.save_state()
                    self.root.after(0, self.show_end_message)
            self.current_set_index += 1
            self.root.update_idletasks()
            
        else:
            self.current_set_index = 0
            self.save_state()
            self.root.after(0, self.show_end_message)

    def display_tutorial(self):
        print(f"Displaying set tutorial")  # デバッグ情報
        self.description_text.grid(row=0, column=0, columnspan=5, pady=10)
        self.next_button.grid(row=2, column=3, pady=5)  # Nextボタンを画像の横に配置
        image_paths = self.tutorial_images_set
        for idx, img_path in enumerate(image_paths):
            try:
                img = Image.open(img_path)
                img.thumbnail((280, 280)) #ここで画像サイズ調整
                img = ImageTk.PhotoImage(img)
                label = self.image_labels[idx]
                label.config(image=img)
                label.image = img
                label.image_path = img_path  # ここで画像パスをラベルに格納
                label.bind("<Button-1>", lambda e, l=label, t=self.text_labels[idx]: self.on_left_click(l, t))
                label.bind("<Button-2>", lambda e, l=label, t=self.text_labels[idx]: self.on_right_click(l, t))
                label.grid(row=idx // 4 + 1, column=idx % 4, padx=30, pady=8) #ここで画像サイズ調整
                text_label = self.text_labels[idx]
                text_label.grid(row=idx // 4 + 1, column=idx % 4, padx=30, pady=8, sticky="n")
                text_label.lower()
                print(f"Label {idx} placed at row {idx // 3 + 1}, column {idx % 3}")  # デバッグ情報
            except Exception as e:
                print(f"Error loading image {img_path}: {e}")  # エラーメッセージ
        self.root.update_idletasks()

    def reset_label_borders(self):
        for label in self.image_labels:
            label.config(highlightbackground="white", highlightcolor="white")
        self.red_labels = []
        self.blue_labels = []

    def on_next_button_click(self):
        if self.step == 0:
            self.title.grid_remove()
            self.start_button.place_forget()
            self.display_tutorial()
            self.step += 1
        elif self.step == 1:
            if len(self.red_labels) < 2 or len(self.blue_labels) < 2:
                self.show_error_message("赤と青の枠はそれぞれ二つ選んでください")
            else:
                #タイトルの表示
                self.title_h.grid(row=0, column=0, columnspan=5, pady=300, padx=630)
                self.start_button_h.place(x=600, y=400)
                self.description_text.grid_remove()
                self.next_button.grid_remove()
                for label in self.image_labels:
                    label.grid_forget()
                for label in self.text_labels:
                    print(label)
                    label.grid_remove()
                self.step += 1
        elif self.step == 2:
            self.title_h.grid_remove()
            self.start_button_h.place_forget()
            self.display_next_set()
            self.step += 1
        elif self.step == 3:
            if len(self.red_labels) < 2 or len(self.blue_labels) < 2:
                self.show_error_message("赤と青の枠はそれぞれ二つ選んでください")
            else:
                self.update_scores()
                self.display_next_set()
            

    def on_left_click(self, label, text_label):
        if label in self.red_labels:
            label.config(highlightbackground="white", highlightcolor="white", highlightthickness=7)
            text_label.lower()  # 非表示にする
            self.red_labels.remove(label)
        else:
            if len(self.red_labels) < 2:
                if label in self.blue_labels:
                    self.blue_labels.remove(label)
                label.config(highlightbackground="red", highlightcolor="red", highlightthickness=7)
                text_label.config(text="魅力的である", bg="red")
                text_label.lift()  # 表示する
                self.red_labels.append(label)
            else:
                self.show_error_message("赤色の枠は二つ以上選べません")

    def on_right_click(self, label, text_label):
        if label in self.blue_labels:
            label.config(highlightbackground="white", highlightcolor="white", highlightthickness=7)
            text_label.lower()  # 非表示にする
            self.blue_labels.remove(label)
        else:
            if len(self.blue_labels) < 2:
                if label in self.red_labels:
                    self.red_labels.remove(label)
                label.config(highlightbackground="blue", highlightcolor="blue", highlightthickness=7)
                text_label.config(text="魅力的でない", bg="blue")
                text_label.lift()  # 表示する
                self.blue_labels.append(label)
            else:
                self.show_error_message("青色の枠は二つ以上選べません")

    def update_scores(self):
        for label in self.image_labels:
            path = label.image_path
            if label in self.red_labels:
                self.update_score(path, "red")
            elif label in self.blue_labels:
                self.update_score(path, "blue")
            else:
                self.update_score(path, "white")


    def update_score(self, path, color, remove=False):
        title, font, number = self.extract_info_from_path(path)
        key = f"{title}_{font}_{number}"
        if color == "red":
            score = 5
        elif color == "blue":
            score = 0
        else:
            score = 1
        if remove:
            self.score_dict.pop(key, None)
        else:
            self.score_dict[key] = score

    def extract_info_from_path(self, path):
        parts = path.split(os.sep)
        title = parts[-3]
        font = parts[-2]
        number = parts[-1].split('_')[0]
        return title, font, number

    def show_error_message(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("エラー")
        tk.Label(error_window, text=message, font=("Helvetica", 14)).pack(padx=20, pady=20)
        tk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)
    
    def show_end_message(self):
        print("Showing end message")  # デバッグ情報
        self.description_text.grid_remove()
        for label in self.image_labels:
            label.grid_forget()
            print(f"Label {label} hidden")  # デバッグ情報
        for label in self.text_labels:
            label.grid_remove()
        end_label = tk.Label(self.root, text="以上で終了します。\nありがとうございました。", font=("Helvetica", 16))
        end_label.grid(row=1, column=1, padx=5, pady=5)
        print("End message displayed")  # デバッグ情報
        self.next_button.grid_remove()
        print("Next button disabled")  # デバッグ情報
        self.print_scores()

    def print_scores(self):
        print("Scores:")
        for key, score in self.score_dict.items():
            print(f"{key}: {score}")
            title, font, number = key.rsplit('_', 2)
            print(title, font, number)
            number = int(number)
            if score == 5:
                self.df.loc[(self.df['title'] == title) & (self.df['font'] == font) & (self.df['number'] == number), '5'] += 1
            elif score == 1:
                self.df.loc[(self.df['title'] == title) & (self.df['font'] == font) & (self.df['number'] == number), '1'] += 1
            elif score == 0:
                self.df.loc[(self.df['title'] == title) & (self.df['font'] == font) & (self.df['number'] == number), '0'] += 1
                self.df.to_csv(self.results_file, index=False)
        print('Updated results.csv')

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                state = json.load(f)
                self.current_set_index = state.get("current_set_index", 0)
                print(f"Loaded state: {state}")  # デバッグ情報
        else:
            self.current_set_index = 0
            print("No state file found, starting from index 0")  # デバッグ情報

    def load_images_set(self):
        with open(self.state_file, "r") as f:
            state = json.load(f)
            self.images_set = state.get("images_set", [])
            print(f"Loaded images set: {len(self.images_set)} sets")  # デバッグ情報

    def save_state(self):
        with open(self.state_file, "w") as f:
            state = {
                "current_set_index": self.current_set_index,
                "images_set": self.images_set
            }
            json.dump(state, f)
            #print(f"Saved state: {state}")  # デバッグ情報
    

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()