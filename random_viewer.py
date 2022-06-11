#!/usr/bin/env python3
"""
簡単な画像ビューワー
"""
import glob
import os
import random
import tkinter
from sys import argv
from typing import Any, List

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
        self.hello_label.configure(
            text=f"[{len(PICT.pict_list)}/1] {PICT.pict_list[0]}"
        )

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

        if len(PICT.pict_list) > 0:
            # create a image on canvas
            tmp = Image.open(PICT.pict_list[0])
            self.img_target = ImageTk.PhotoImage(
                tmp.resize((400, 400), Image.ANTIALIAS)
            )
        self.img_on_canvas = self.canvas.create_image(
            0, 0, image=self.img_target, anchor=tkinter.NW
        )

        ###########################################
        ###########################################
        # 追加機能
        # 方針:
        #   1. 名前をまともにする。
        #   2. mypy に怒られないようにする。
        #       1. ラムダ式を def式に改める？
        #       2. ラムダ式のまま mypy の "foo of bar does not return a value" error を避ける？
        PICT.register = []
        self.book_mark_button = tkinter.Button(
            self,
            text="book mark",
            width=20,
            command=lambda: [
                PICT.register.append(PICT.pict_list.pop(0)),
                self.pict_shuffle(),
            ],
        )
        self.book_mark_save = tkinter.Button(
            self,
            text="save",
            width=20,
            command=lambda: open(
                r".\.random_viewer\bookmark.ini", "w+", encoding="utf-8"
            ).write(("\n").join(PICT.register)),
        )
        # キーボードショートカット
        self.bind_all(
            "<KeyPress-b>",
            lambda key: [PICT.book_mark(), self.pict_shuffle()],
        )
        self.bind_all(
            "<KeyPress-y>",
            lambda key: [
                PICT.register.append(PICT.pict_list.pop(0)),
                self.pict_shuffle(),
            ],
        )
        self.bind_all(
            "<KeyPress-Y>",
            lambda key: [
                [PICT.register.append(i) for i in PICT.pict_list],
                self.pict_shuffle(),
            ],
        )
        self.bind_all(
            "<KeyPress-x>",
            lambda key: [PICT.pict_list.pop(0), self.pict_shuffle()],
        )
        self.bind_all("<KeyPress-q>", lambda key: self.quit())
        self.bind_all("<KeyPress-v>", lambda key: viewer())
        self.bind_all("<KeyPress-Return>", lambda key: self.pict_shuffle())
        ###########################################
        ###########################################

        self.hello_label.pack()
        self.canvas.pack()
        self.pict_shuffle_button.pack()
        self.text_box.pack()
        self.text_box_button.pack()
        self.viewer_button.pack()
        self.quit_button.pack()
        self.book_mark_button.pack()
        self.book_mark_save.pack()

    def set_current_dir(self) -> None:
        """ディレクトリを交換する。無を入力することで最初に開いたディレクトリに戻る。"""
        self.current_dir = self.text_box.get()
        if self.current_dir == "":
            self.current_dir = self.first_dir

        self.hello_label.configure(text=self.current_dir)
        os.chdir(self.current_dir)

        PICT.pict_list.clear()
        PICT.pict_list.extend(glob.glob("*.jpg"))
        PICT.pict_list.extend(glob.glob("*.png"))

        random.shuffle(PICT.pict_list)

    def pict_shuffle(self) -> bool:
        """画像ファイルリストをシャッフルして、画像を表示する。"""
        random.shuffle(PICT.pict_list)

        if len(PICT.pict_list) <= 0:
            return False

        tmp = Image.open(PICT.pict_list[0].strip())
        tmp = tmp.resize((400, 400), Image.ANTIALIAS)
        self.hello_label.configure(
            text=f"[{len(PICT.pict_list)}/1] {PICT.pict_list[0]}"
        )
        self.img_target = ImageTk.PhotoImage(tmp)

        self.canvas.itemconfig(self.img_on_canvas, image=self.img_target)

        return True

class Picture:
    """
    画像リストなどを管理する。
    リファクタリング として Application class の属性を一部引き受ける。
    """

    def __init__(self, pict_list: List[str]):
        self.pict_list: List[str] = pict_list
        self.register: List[str] = list()

    def book_mark(self) -> bool:
        """PICT＿LISTをブックマ－クの内容にする。"""
        PICT.pict_list.clear()
        with open(
            r".\.random_viewer\bookmark.ini", "r+", encoding="utf-8"
        ) as r_book_mark:
            PICT.pict_list = list(map(lambda x: x.strip(), r_book_mark.readlines()))

        return True


def viewer() -> None:
    """画像ファイルを表示する。"""
    target_path = PICT.pict_list[0]
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

    PICT = Picture(PICT_LIST)
    APP = Application(master=WINDOW)
    APP.mainloop()
