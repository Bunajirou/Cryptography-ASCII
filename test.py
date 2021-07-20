import math
import sympy
import pickle
import os
import tkinter as tk
from tkinter.constants import END
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox

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
root = tk.Tk()
root.title("受信側（復号）")
root.geometry("560x670")

# チェックボタンの状態をdecryption.pickleに書き込む関数
def write_state():
    if bln.get():
        with open('decryption.pickle', mode='rb') as f:
            chk_flag = pickle.load(f)
            hoka = pickle.load(f)
        with open('decryption.pickle', mode='wb') as f:
            chk_flag = 1
            pickle.dump(chk_flag, f)
            pickle.dump(hoka, f)
    else:
        with open('decryption.pickle', mode='rb') as f:
            chk_flag = pickle.load(f)
            hoka = pickle.load(f)
        with open('decryption.pickle', mode='wb') as f:
            chk_flag = 0
            pickle.dump(chk_flag, f)
            pickle.dump(hoka, f)

# チェックボタン作成
bln = tk.BooleanVar()
bln.set(False)
chk = tk.Checkbutton(root, variable=bln, text='keyを固定', command=write_state)
chk.grid(row=0, column=0, padx=10, sticky=tk.E)

# chk_flagをdecryption.pickleを参照し初期化
if(os.path.exists('./decryption.pickle')):
    with open('decryption.pickle', mode='rb') as f:
        chk_flag = pickle.load(f)
        n, e, d = pickle.load(f)
else:
    chk_flag = 0

# chk_flagの値に応じてkeyの作成(chk_flag==0) or 読み込み(chk_flag==1)
if (chk_flag == 1):
    key = str(n) + " " +str(e)
    bln.set(True)
else:
    # p,qの最大値、最小値
    max_prime = pow(10, 201)
    min_prime = pow(10, 200)

    # p,qを範囲内のランダムな素数で初期化
    while(True):
        p = sympy.randprime(min_prime, max_prime)
        q = sympy.randprime(min_prime, max_prime)
        if(p != q):break

    n = p * q
    L = math.lcm(p-1, q-1)
    max = max(p, q)
    while(True):
        e = sympy.randprime(max+1, L)
        if(sympy.gcd(e, L)==1):break
    x = sympy.gcdex(e, L)
    d = int(x[0] % L)
    key = str(n) + " " +str(e)

    with open('decryption.pickle', mode='wb') as f:
        chk_flag = 0
        hoka = [n,e,d]
        pickle.dump(chk_flag, f)
        pickle.dump(hoka, f)
        bln.set(False)

# 入出力欄の作成
key_box = ScrolledText(root, font=("", 10), height=5, width=72)
key_box.grid(row=1, column=0, padx=10)
key_box.insert(1.0, key)

c_box = ScrolledText(root, font=("", 15), height=10, width=50)
c_box.grid(row=3, column=0, padx=10)

p_box = ScrolledText(root, font=("", 15), height=10, width=50)
p_box.grid(row=6, column=0, padx=10)

# ラベルの作成
key_label = tk.Label(text="key")
key_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

input_label = tk.Label(text="暗号文を入力")
input_label.grid(row=2,column=0, padx=10, pady=5, sticky=tk.W)

p_label = tk.Label(text="平文")
p_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

# 復号処理
def decryption():
    c_txt = c_box.get(1.0,END)
    c_txt_list = list(c_txt)  # 文字列をリストへ変換
    c_txt_list.pop()

    c_ascii_list = []
    for i in c_txt_list:  # ASCIIコードへ変換
        if(ord(i)>=128):
            messagebox.showerror('エラー','使用できない文字が含まれています')
            p_box.delete(1.0, END)
            break
        if(ord(i)==10):
            c_ascii_list.append(95)
        else:
            c_ascii_list.append(ord(i)-A) 

    C = N_to_dec(c_ascii_list, 128-A)
    P = pow(C, d, n)
    p_ascii_list = dec_to_N(P, 128-A)

    p_txt_list = []
    for i in p_ascii_list:  # ASCIIコードを文字へ変換
        if(i==95):
            p_txt_list.append(chr(10))
        else:
            p_txt_list.append(chr(i+A))
    p_txt = (''.join(p_txt_list))  # リスト内の文字を結合
    p_box.delete(1.0, END)
    p_box.insert(1.0, p_txt)

# 入力欄クリア処理
def c_delete():
    c_box.delete(1.0, END)

# ボタンの作成
decry_button = tk.Button(text="復号実行",command=decryption)
decry_button.grid(row=4, column=0, padx=13, pady=5, sticky=tk.W)

c_del_button = tk.Button(text="クリア",command=c_delete)
c_del_button.grid(row=4, column=0, padx=13, pady=5, sticky=tk.E)


root.mainloop()