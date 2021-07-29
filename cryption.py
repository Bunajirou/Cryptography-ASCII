import math
import sympy
import pickle
import os
import tkinter as tk
from tkinter.constants import END
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox


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


def write_state_de():  # others = [n,e,d]
    if bln_de.get():
        with open('decryption.pickle', mode='rb') as f:
            chk_de_flag = pickle.load(f)
            others = pickle.load(f)
        with open('decryption.pickle', mode='wb') as f:
            chk_de_flag = 1
            pickle.dump(chk_de_flag, f)
            pickle.dump(others, f)
    else:
        with open('decryption.pickle', mode='rb') as f:
            chk_de_flag = pickle.load(f)
            others = pickle.load(f)
        with open('decryption.pickle', mode='wb') as f:
            chk_de_flag = 0
            pickle.dump(chk_de_flag, f)
            pickle.dump(others, f)


def write_state_en():
    if bln_en.get():
        with open('encryption.pickle', mode='wb') as f:
            key_txt = key_box.get(1.0,END)
            key_en = key_txt[:-1]
            chk_en_flag = 1
            pickle.dump(chk_en_flag, f)
            pickle.dump(key_en, f)
    else:
        with open('encryption.pickle', mode='rb') as f:
            chk_en_flag = pickle.load(f)
            key_en = pickle.load(f)
        with open('encryption.pickle', mode='wb') as f:
            chk_en_flag = 0
            pickle.dump(chk_en_flag, f)
            pickle.dump(key_en, f)


def create_key():
    max_prime = pow(10, 200)
    min_prime = pow(10, 199)

    while(True):
        p = sympy.randprime(min_prime, max_prime)
        q = sympy.randprime(min_prime, max_prime)
        if(p != q):break

    n = p * q
    L = math.lcm(p-1, q-1)
    mx = max(p, q)
    while(True):
        e = sympy.randprime(mx+1, L)
        if(sympy.gcd(e, L)==1):break
    x = sympy.gcdex(e, L)
    d = int(x[0] % L)
    key_de = str(n) + " " +str(e)

    with open('decryption.pickle', mode='wb') as f:
        chk_de_flag = 0
        others = [n,e,d]
        pickle.dump(chk_de_flag, f)
        pickle.dump(others, f)
        bln_de.set(False)
    return d, n, key_de


def decryption():
    c_txt = input_box.get(1.0,END)
    c_txt_list = list(c_txt)  # 文字列をリストへ変換
    c_txt_list.pop()

    c_ascii_list = []
    for i in c_txt_list:  # ASCIIコードへ変換
        if(ord(i)>=128):
            messagebox.showerror('エラー','使用できない文字が含まれています。')
            output_box.delete(1.0, END)
            break
        c_ascii_list.append(ord(i)-33) 

    C = N_to_dec(c_ascii_list, 93)
    P = pow(C, d, n)
    p_ascii_list = dec_to_N(P, 128-A)

    p_txt_list = []
    for i in p_ascii_list:  # ASCIIコードを文字へ変換
        if(i==95):
            p_txt_list.append(chr(10))
        else:
            p_txt_list.append(chr(i+A))
    p_txt = (''.join(p_txt_list))  # リスト内の文字を結合
    output_box.delete(1.0, END)
    output_box.insert(1.0, p_txt)


def encryption():
    key_txt = key_box.get(1.0,END)
    key_txt = key_txt[:-1]
    with open('encryption.pickle', mode='rb') as f:
            chk_en_flag = pickle.load(f)
            pickle.load(f)
    with open('encryption.pickle', mode='wb') as f:
            pickle.dump(chk_en_flag, f)
            pickle.dump(key_txt, f)
    try:
        n, e = map(int, key_txt.split())
    except:
        messagebox.showwarning('エラー','公開鍵が正しくありません。')
    P = n + 1
    p_txt = input_box.get(1.0, END)

    p_txt_list = list(p_txt)  # 文字列をリストへ変換

    p_ascii_list = []
    for i in p_txt_list:  # ASCIIコードへ変換（改行文字の場合95をリストへ追加）
        if(ord(i)>=128):
            messagebox.showerror('エラー','使用できない文字が含まれています。')
            output_box.delete(1.0, END)
            break
        elif(ord(i)==10):
            p_ascii_list.append(95) 
        else:
            p_ascii_list.append(ord(i)-A) 

    P = N_to_dec(p_ascii_list, 128-A)

    if(P < n):
        C = pow(P, e, n)
        c_ascii_list = dec_to_N(C, 93)

        c_txt_list = []
        for i in c_ascii_list:  # ASCIIコードを文字へ変換
            c_txt_list.append(chr(i+33))

        c_txt = (''.join(c_txt_list))  # リスト内の文字を結合
        output_box.delete(1.0, END)
        output_box.insert(1.0, c_txt)

    else:
        messagebox.showwarning('エラー','平文が長すぎます。')


def check_rdo():
    if(mode.get()==0):  # 復号モード
        chk_en.grid_remove()
        en_key_label.grid_remove()
        en_in_label.grid_remove()
        en_out_label.grid_remove()
        key_del_button.grid_remove()
        encry_button.grid_remove()
        chk_de.grid()
        de_key_label.grid()
        de_in_label.grid()
        de_out_label.grid()
        key_button.grid()
        decry_button.grid()
        key_delete()
        box_delete()
        key_box.insert(1.0, key_de)
    else:  # 暗号化モード
        chk_de.grid_remove()
        de_key_label.grid_remove()
        de_in_label.grid_remove()
        de_out_label.grid_remove()
        key_button.grid_remove()
        decry_button.grid_remove()
        chk_en.grid()
        en_key_label.grid()
        en_in_label.grid()
        en_out_label.grid()
        key_del_button.grid()
        encry_button.grid()
        key_delete()
        box_delete()
        if(os.path.exists('./encryption.pickle')):
            with open('encryption.pickle', mode='rb') as f:
                chk_en_flag = pickle.load(f)
                if(chk_en_flag == 1):
                    key_en = pickle.load(f)
                    key_box.insert(1.0, key_en)


def box_delete():
    input_box.delete(1.0, END)
    output_box.delete(1.0, END)

def key_delete():
    key_box.delete(1.0, END)

def set_clip_key():
    root.clipboard_append(key_de)


if __name__ == '__main__':
    A = 32  # ASCIIコードのA番以降を使用

    # ウィンドウの作成
    root = tk.Tk()
    root.title("公開鍵暗号")
    root.geometry("540x725")

    # チェックボタン作成
    bln_de = tk.BooleanVar()
    bln_en = tk.BooleanVar()
    bln_de.set(False)
    bln_en.set(False)
    chk_de = tk.Checkbutton(root, variable=bln_de, text='公開鍵を固定する', command=write_state_de)
    chk_en = tk.Checkbutton(root, variable=bln_en, text='公開鍵を保存する', command=write_state_en)
    chk_de.grid(row=3, column=0, padx=10, sticky=tk.E)
    chk_en.grid(row=3, column=0, padx=10, sticky=tk.E)

    # chk_de_flagをdecryption.pickleを参照し初期化
    if(os.path.exists('./decryption.pickle')):
        with open('decryption.pickle', mode='rb') as f:
            chk_de_flag = pickle.load(f)
            n, e, d = pickle.load(f)
    else:
        chk_de_flag = 0
    # chk_de_flagの値に応じてkeyの作成
    if (chk_de_flag == 1):
        key_de = str(n) + " " +str(e)
        bln_de.set(True)
    else:
        d, n, key_de = create_key()

    # chk_en_flagをencryption.pickleを参照し初期化
    if(os.path.exists('./encryption.pickle')):
        with open('encryption.pickle', mode='rb') as f:
            chk_en_flag = pickle.load(f)
            key_en = pickle.load(f)
        if(chk_en_flag == 1):
            bln_en.set(True)
    else:
        chk_en_flag = 0

    # ラジオボタン作成
    mode = tk.IntVar()
    mode.set(0)
    en_rdo = tk.Radiobutton(root, value=0, variable=mode, text='復号(鍵生成)モード', command=check_rdo)
    en_rdo.grid(row=1, column=0, padx=10, pady=0, sticky=tk.W)
    de_rdo = tk.Radiobutton(root, value=1, variable=mode, text='暗号化モード', command=check_rdo)
    de_rdo.grid(row=2, column=0, padx=10, pady=0, sticky=tk.W)

    # ラベルの作成
    mode_label = tk.Label(text='<モード選択>')
    mode_label.grid(row=0, column=0, padx=10, pady=0, sticky=tk.W)

    de_key_label = tk.Label(text='公開鍵')
    de_key_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

    de_in_label = tk.Label(text='暗号文を入力')
    de_in_label.grid(row=6,column=0, padx=10, pady=5, sticky=tk.W)

    de_out_label = tk.Label(text='平文')
    de_out_label.grid(row=9, column=0, padx=10, pady=5, sticky=tk.W)

    en_key_label = tk.Label(text='公開鍵を入力')
    en_key_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

    en_in_label = tk.Label(text='平文を入力')
    en_in_label.grid(row=6,column=0, padx=10, pady=5, sticky=tk.W)
    
    en_out_label = tk.Label(text='暗号文')
    en_out_label.grid(row=9, column=0, padx=10, pady=5, sticky=tk.W)

    # 入出力欄の作成
    key_box = ScrolledText(root, font=('', 10), height=5, width=72)
    key_box.grid(row=4, column=0, padx=10)
    key_box.insert(1.0, key_de)

    input_box = ScrolledText(root, font=('', 15), height=10, width=50)
    input_box.grid(row=7, column=0, padx=10)

    output_box = ScrolledText(root, font=('', 15), height=10, width=50)
    output_box.grid(row=10, column=0, padx=10)

    # ボタンの作成
    key_button = tk.Button(text='公開鍵をクリップボードにコピー',command=set_clip_key)
    key_button.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

    decry_button = tk.Button(text='復号実行',command=decryption)
    decry_button.grid(row=8, column=0, padx=13, pady=5, sticky=tk.W)

    box_del_button = tk.Button(text='クリア',command=box_delete)
    box_del_button.grid(row=8, column=0, padx=13, pady=5, sticky=tk.E)

    key_del_button = tk.Button(text='クリア',command=key_delete)
    key_del_button.grid(row=5, column=0, padx=13, pady=5, sticky=tk.E)

    encry_button = tk.Button(text='暗号化実行',command=encryption)
    encry_button.grid(row=8, column=0, padx=13, pady=5, sticky=tk.W)

    check_rdo()


    root.mainloop()