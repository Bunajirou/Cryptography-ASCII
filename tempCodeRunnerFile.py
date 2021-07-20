# チェックボタン作成
bln = tkinter.BooleanVar()
bln.set(False)
chk = tkinter.Checkbutton(root, variable=bln, text='keyを保存', command=write_state)
chk.place(x=440, y=9)