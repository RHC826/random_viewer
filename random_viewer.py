#!/usr/bin/env python3
"""
簡単な画像ビューワー
"""
import glob
import os
import random
import tkinter
from typing import Any
from sys import argv
from PIL import Image, ImageTk


class Application(tkinter.Frame):
    """
    ビューワーのGUIに改善の余地あり
        1. 思った位置に配置できていない。
        2. 最初と2回目のシャッフルのときにボタンの位置が移動している。
        3. 一直線にボタンが並んでいない。
    """

    def __init__(self, master: Any) -> None:
        tkinter.Frame.__init__(self, master)
        master.title("tkinter canvas trial")
        self.img_target: Any = None
        self.current_dir: str = str(argv[1]) if len(argv) >= 2 else os.getcwd()
        self.first_dir: str = str(argv[1]) if len(argv) >= 2 else os.getcwd()
        self.create_widgets()
        self.pack()

    def create_widgets(self) -> None:
        """要素の配置を決定する"""
        # create a label
        self.hello_label = tkinter.Label(self, text="Random_Viewer")
        self.hello_label.configure(text=self.current_dir)

        # create a text box
        self.text_box = tkinter.Entry(self, width=25)

        # create Buttons
        self.viewer_button = tkinter.Button(
            self, text="viewer", width=20, command=viewer
        )
        self.quit_button = tkinter.Button(
            self, text="Quit", width=20, command=self.quit
        )
        self.pict_shuffle_button = tkinter.Button(
            self, text="pict shuffle", width=20, command=self.pict_shuffle
        )
        self.text_box_button = tkinter.Button(
            self, text="change directory", width=20, command=self.set_current_dir
        )

        # pack()
        # create a canvas
        self.canvas = tkinter.Canvas(self, width=400, height=400)

        if len(PICT_LIST) > 0:
            # create a image on canvas
            tmp = Image.open(PICT_LIST[0])
            self.img_target = ImageTk.PhotoImage(
                tmp.resize((400, 400), Image.ANTIALIAS)
            )
        self.img_on_canvas = self.canvas.create_image(
            0, 0, image=self.img_target, anchor=tkinter.NW
        )

        self.hello_label.pack()
        self.canvas.pack()
        self.pict_shuffle_button.pack()
        self.text_box.pack()
        self.text_box_button.pack()
        self.viewer_button.pack()
        self.quit_button.pack()

    def set_current_dir(self) -> None:
        """ディレクトリを交換する。無を入力することで最初に開いたディレクトリに戻る。"""
        self.current_dir = self.text_box.get()
        if self.current_dir == "":
            self.current_dir = self.first_dir

        self.hello_label.configure(text=self.current_dir)
        os.chdir(self.current_dir)

        PICT_LIST.clear()
        PICT_LIST.extend(glob.glob("*.jpg"))
        PICT_LIST.extend(glob.glob("*.png"))

        random.shuffle(PICT_LIST)

    def pict_shuffle(self) -> None:
        """画像ファイルリストをシャッフルして、画像を表示する。"""
        random.shuffle(PICT_LIST)

        if len(PICT_LIST) <= 0:
            return

        tmp = Image.open(PICT_LIST[0])
        tmp = tmp.resize((400, 400), Image.ANTIALIAS)
        self.hello_label.configure(text=PICT_LIST[0])
        self.img_target = ImageTk.PhotoImage(tmp)

        self.canvas.itemconfig(self.img_on_canvas, image=self.img_target)


def viewer() -> None:
    """画像ファイルを表示する。"""
    target_path = PICT_LIST[0]
    tmp = Image.open(target_path)
    (tmp).show()


if __name__ == "__main__":
    print(argv[1] if len(argv) >= 2 else os.getcwd())
    # ウィンドウを作成
    WINDOW = tkinter.Tk()
    # ウィンドウサイズ
    WINDOW.geometry("900x600")
    # ディレクトリの中のファイルをリストにして返す
    PICT_LIST = glob.glob(
        os.path.join(argv[1] if len(argv) >= 2 else os.getcwd(), "*.jpg")
    )
    PICT_LIST.extend(
        glob.glob(os.path.join(argv[1] if len(argv) >= 2 else os.getcwd(), "*.png"))
    )

    random.shuffle(PICT_LIST)

    APP = Application(master=WINDOW)
    APP.mainloop()
