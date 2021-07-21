import pickle
import tkinter
import os
from tkinter import messagebox
from tkinter.constants import END
from tkinter.scrolledtext import ScrolledText
from functools import partial

A = 32  # ASCIIコードのA番以降を使う(delも除外) 途中の処理により改行文字も使用可能


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

# ウィンドウの作成
root = tkinter.Tk()
root.title("送信側（暗号化）")
root.geometry("540x670")

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

# チェックボタン作成
bln = tkinter.BooleanVar()
bln.set(False)
chk = tkinter.Checkbutton(root, variable=bln, text='keyを保存', command=write_state)
chk.place(x=440, y=9)

# 入出力欄の作成
key_box = ScrolledText(root, font=("", 10), height=5, width=72)
key_box.pack()
key_box.place(x=10, y=31)

p_box = ScrolledText(root, font=("", 15), height=10, width=50)
p_box.pack()
p_box.place(x=10, y=166)

c_box = ScrolledText(root, font=("", 15), height=10, width=50)
c_box.pack()
c_box.place(x=10, y=436)

# ラベルの作成
key_label = tkinter.Label(text="keyを入力")
key_label.place(x=10, y=10)

p_label = tkinter.Label(text="平文を入力")
p_label.place(x=10, y=145)

c_label = tkinter.Label(text="暗号文")
c_label.place(x=10, y=415)

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

# ボタンクリック時の動作
def encryption(x):
    key_txt = key_box.get(1.0,END)
    key_txt = key_txt[:-1]
    with open('encryption.pickle', mode='wb') as f:
            pickle.dump(chk_flag, f)
            pickle.dump(key_txt, f)
    try:
        n, e = map(int, key_txt.split())
    except:
        messagebox.showwarning("エラー","keyが間違っています。")
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

# 入力欄クリア処理
def key_delete():
    key_box.delete(1.0, END)
def p_delete():
    p_box.delete(1.0, END)

# クリップボード処理（保留）-----------------------
#def set_c():
#    root.clipboard_append(encryption(0))
#------------------------------------------------

# ボタンの作成
key_del_button = tkinter.Button(text="クリア",command=key_delete)
key_del_button.place(x=480, y=105)

encry_button = tkinter.Button(text="暗号化実行",command=partial(encryption, 1))
encry_button.place(x=10, y=375)

p_del_button = tkinter.Button(text="クリア",command=p_delete)
p_del_button.place(x=480, y=375)

# クリップボードへのコピーが不安定なため保留----------------------------------------
#copy_button = tkinter.Button(text="暗号文をクリップボードにコピー",command=set_c)
#copy_button.place(x=10, y=642)
#-------------------------------------------------------------------------------

root.mainloop()