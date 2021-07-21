import pickle
import os
import tkinter as tk
from tkinter import messagebox
from tkinter.constants import END
from tkinter.scrolledtext import ScrolledText
from functools import partial


def dec_to_N(num,N):
    digit=0
    for i in range(10**9):
        if num<N**i:
            digit+=i
            break
    ans=[0]*digit
    check=0
    for i in range(1,digit+1):
        j=num//(N**(digit-i))
        ans[check]=j
        check+=1
        num-=(j)*(N**(digit-i))
    return ans


def N_to_dec(list, N):
    l=len(list)
    ans=0
    for i in range(1,l+1):
        ans+=list[-i]*(N**(i-1))
    return ans

# チェックボタンの状態とkeyをencryption.pickleに書き込む関数
def write_state():
    if bln.get():
        with open('encryption.pickle', mode='wb') as f:
            key_txt = key_box.get(1.0,END)
            key = key_txt[:-1]
            chk_flag = 1
            pickle.dump(chk_flag, f)
            pickle.dump(key, f)
    else:
        with open('encryption.pickle', mode='rb') as f:
            chk_flag = pickle.load(f)
            key = pickle.load(f)
        with open('encryption.pickle', mode='wb') as f:
            chk_flag = 0
            pickle.dump(chk_flag, f)
            pickle.dump(key, f)


def encryption(x):
    key_txt = key_box.get(1.0,END)
    key_txt = key_txt[:-1]
    with open('encryption.pickle', mode='wb') as f:
            pickle.dump(chk_flag, f)
            pickle.dump(key_txt, f)
    try:
        n, e = map(int, key_txt.split())
    except:
        messagebox.showwarning("エラー","公開鍵が正しくありません。")
    P = n + 1
    p_txt = p_box.get(1.0, END)

    p_txt_list = list(p_txt)  # 文字列をリストへ変換

    p_ascii_list = []
    for i in p_txt_list:  # ASCIIコードへ変換（改行文字の場合95をリストへ追加）
        if(ord(i)==10):
            p_ascii_list.append(95) 
        else:
            p_ascii_list.append(ord(i)-A) 

    P = N_to_dec(p_ascii_list, 128-A)

    if(P < n):
        C = pow(P, e, n)
        c_ascii_list = dec_to_N(C, 128-A)

        c_txt_list = []
        for i in c_ascii_list:  # ASCIIコードを文字へ変換
            if(i==95):
                c_txt_list.append(chr(10))  # 改行文字用の処理
            else:
                c_txt_list.append(chr(i+A))

        c_txt = (''.join(c_txt_list))  # リスト内の文字を結合
        if(x==1):
            c_box.delete(1.0, END)
            c_box.insert(1.0, c_txt)
        else:
            return c_txt
    else:
        messagebox.showwarning("エラー","平文が長すぎます。")


def key_delete():
    key_box.delete(1.0, END)


def box_delete():
    p_box.delete(1.0, END)
    c_box.delete(1.0, END)


if __name__ == '__main__':
    A = 32  # ASCIIコードのA番以降を使用

    # ウィンドウの作成
    root = tk.Tk()
    root.title("送信側（暗号化）")
    root.geometry("540x670")

    # チェックボタン作成
    bln = tk.BooleanVar()
    bln.set(False)
    chk = tk.Checkbutton(root, variable=bln, text='公開鍵を保存する', command=write_state)
    chk.grid(row=0, column=0, padx=10, sticky=tk.E)

    # 入出力欄の作成
    key_box = ScrolledText(root, font=("", 10), height=5, width=72)
    key_box.grid(row=1, column=0, padx=10)

    p_box = ScrolledText(root, font=("", 15), height=10, width=50)
    p_box.grid(row=4, column=0, padx=10)

    c_box = ScrolledText(root, font=("", 15), height=10, width=50)
    c_box.grid(row=7, column=0, padx=10)

    # ラベルの作成
    key_label = tk.Label(text="公開鍵を入力")
    key_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

    p_label = tk.Label(text="平文を入力")
    p_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

    c_label = tk.Label(text="暗号文")
    c_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

    # ボタンの作成
    key_del_button = tk.Button(text="クリア",command=key_delete)
    key_del_button.grid(row=2, column=0, padx=13, pady=5, sticky=tk.E)

    encry_button = tk.Button(text="暗号化実行",command=partial(encryption, 1))
    encry_button.grid(row=5, column=0, padx=13, pady=5, sticky=tk.W)

    p_del_button = tk.Button(text="クリア",command=box_delete)
    p_del_button.grid(row=5, column=0, padx=13, pady=5, sticky=tk.E)

    # chk_flagをencryption.pickleを参照し初期化
    if(os.path.exists('./encryption.pickle')):
        with open('encryption.pickle', mode='rb') as f:
            chk_flag = pickle.load(f)
            key = pickle.load(f)
        if(chk_flag == 1):
            key_box.insert(1.0, key)
            bln.set(True)
    else:
        chk_flag = 0


    root.mainloop()