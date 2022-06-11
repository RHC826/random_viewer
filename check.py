"""
渡されたパスが開けるか、存在しているかを調べる。
"""

import os
import itertools
from typing import Any, List
from PIL import Image


def openable_checker(src: List[Any]) -> List[Any]:
    """ 開らく画像リストを返す"""
    return list(filter(lambda x: is_openable_checker(x.strip()), iter(src)))


def is_openable_checker(src: str) -> bool:
    """ 開らく画像なら True を返す"""
    try:
        Image.open(src.strip())
    except:
        return False

    return True


def false_image_checker(src: List[Any]) -> List[Any]:
    """ 開けない画像リストを返す"""
    answer = list()

    for i in src:
        try:
            Image.open(i.strip())
        except:
            answer.append(i)

    return list(answer)


def false_checker(src: List[Any]) -> List[Any]:
    """ 存在しないファイルのリスト を返す"""
    answer = itertools.filterfalse(lambda x: os.path.isfile(x.strip()), iter(src))

    return list(answer)


def checker(src: List[Any]) -> List[Any]:
    """ 存在するファイルのリスト を返す"""
    answer = filter(lambda x: os.path.isfile(x.strip()), iter(src))

    return list(answer)


if __name__ == "__main__":
    with open(
            r".\.random_viewer\bookmark.ini",
            "r",
            encoding="utf-8",
        ) as r:
        LINES = r.readlines()

    SENCERD = openable_checker(LINES)
    for e, path in enumerate(list(set(SENCERD))):
        print(f"{str(e)} : {path})")
