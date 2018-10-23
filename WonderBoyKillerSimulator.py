import sys
from tkinter import *
from random import randint
from PIL import Image,ImageTk

#ウィンドウサイズ
WIDTH = 800
HEIGHT = 800
GEOMETRY = (str(WIDTH) + "x" + str(HEIGHT))

#ランダム変数関数#画像挿入用
rndW = lambda : randint(0,cv.winfo_width())
rndH = lambda : randint(0,cv.winfo_height())

#ウィンドウ作成その他調整
root = Tk()
root.geometry(GEOMETRY)
root.title("ワンボキジェネレータver1.00")

#ボタンを押した時に呼び出される関数
def drawer(event):
    #画像を表示
    cv.create_image(rndW(),rndH(),image=image_tk,anchor=CENTER,tag="pic")

#ボタン押して全消し？
def cleaner(event):
    cv.delete("pic")

#画像読み込み
img = Image.open("smile.png")
image_tk = ImageTk.PhotoImage(img)

#ボタンの設置
#フレーム
F0 = Frame(root)
#生成ボタン
drwrbtn = Button(F0,text=u'標準画像生成')
drwrbtn.bind("<Button-1>",drawer)
drwrbtn.pack(side=LEFT)

#全消しボタン
clnbtn = Button(F0,text=u'画像全消し')
clnbtn.bind("<Button-1>",cleaner)
clnbtn.pack(side=LEFT)

#やめるボタン
exitter = Button(F0,text=u'終了',command=sys.exit)
exitter.pack(side=LEFT)

F0.pack()

#キャンバス作成
cv = Canvas(root,bg="#00a2e7",width=800,height=800)
#cv.create_image(250,250,image=image_tk,anchor=CENTER)
#cv.create_image(100,100,image=image_tk2,anchor=CENTER)
cv.pack(fill=BOTH,expand=True)
cv.update()
print(cv.winfo_height())


root.mainloop()