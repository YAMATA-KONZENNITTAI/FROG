#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

from tkinter import *
from PIL import Image,ImageTk
from random import randint


'''
    オブジェクト指向でない場合？？？？？？？
    メインとなるウィンドウ(root)を先に生成しないと
    画像を読み込もうとした時にエラーがでてしまう
    関数だけをまとめたファイルを作ることで解決できるかも
'''

#ウィンドウ作成その他調整
#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*

#メインウィンドウ
root = Tk()
root.geometry("400x200+810+40")
root.title("ワンダーボーイキラージェネレータ操作パネル")

#サブウィンドウ
sub = Toplevel()
sub.geometry("800x800+5+40")
sub.title("ワンダーボーイキラージェネレータver2.00")

#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*

#ここでいろいろな変数を宣言しておきます（いろいろ管理する為の変数が多い）
font = "Impact"#                   ボタンなどのフォントを一元管理する時に使う
fontsize = 20#                     同様にサイズも
#fontcolor = "#7fffd4" #            同様にカラーも
imgnum = 1#                        画像表示順番を管理する為の変数
img = Image.open("smile.png")#     大元の画像をいれる変数
img_tk = ImageTk.PhotoImage(img)#  挿入する用の画像をいれる変数
reimg_tk = []#                     リサイズした画像を入れる配列
num = 0#                           配列を管理する為の変数

'''
    なぜわざわざ配列を作るか
    いろいろと試行錯誤している中で気づいたことがいくつかある
    まず通常サイズの画像を表示する場合、一つの変数(image_tk)を参照し続ける、或いは同じ画像であることに問題がない
    しかし、大きさが違う画像を表示する場合に一つの変数を使いまわしてしまうと、リサイズして変数の情報を更新する際に
    すでに画面に表示されている画像が参照している変数の情報も更新されてしまう。どういう理由かはわからないが、この時
    すでに表示されている画像は消えてしまう。デバッガー求む
    以下に上記の現象が発生していたコードを記述しておく
'''


#キャンバスの大きさに合わせて上限が変わる乱数(以前はラムダ式で定義していたけど普通の関数にしてみた)
def rndW():#幅用
    return randint(0,cv.winfo_width())

def rndH():#高さ用
    return randint(0,cv.winfo_height())

#画像をリサイズする為の関数
def resize():
    global img,reimg_tk,num#上の方で宣言した変数を参照すると宣言
    reimg = img.resize((randint(1,1000),randint(1,1000)))#リサイズ
    reimg_tk.append(ImageTk.PhotoImage(reimg))#挿入ように変換
    return reimg_tk[num]

#ボタンを押した時に呼び出す関数
def drawer(event):#普通の画像を挿入する関数
    global imgnum
    #画像を表示
    cv.create_image(rndW(),rndH(),image=img_tk,anchor=CENTER,tag=("p"*imgnum))
    #画像管理用の変数を更新
    imgnum += 1

def resizedDrawer(event):#リサイズした画像を挿入する関数
    global imgnum,num
    #画像を表示
    cv.create_image(rndW(),rndH(),image=resize(),anchor=CENTER,tag=("p"*imgnum))
    #配列管理用変数更新
    num += 1
    #画像管理用変数の更新
    imgnum += 1

def allClear(event):
    global imgnum,num
    #画像を全部消す
    for i in range(imgnum + 1):#普通の画像を全部消す
        cv.delete("p"*i)
    del reimg_tk[:]#リサイズ画像を全部消す
    #管理用変数リセット
    imgnum = 1
    num = 0

def undo(event):#画像を一つ消す
    global imgnum
    #表示した画像の順番が狂わないように調整
    if(imgnum > 1):
        imgnum -= 1
    cv.delete("p"*imgnum)

'''
    画像の順番の管理の仕組み
    画像を表示する時にタグ付けすることができる
    今はタグで画像の順番を管理している
    １番目に挿入された画像はtag="p",２番目に挿入された画像はtag="pp"、３番目はtag="ppp"という風にタグ付け
    "p"の数はimgnumで管理
    ingnum=1の時,"p"*imgnum = "p"*1 = "p"
    imgnum=2の時,"p"*imgnum = "p"*2 = "pp"
    imgnum=3の時,"p"*imgnum = "p"*3 = "ppp"
    というような感じ
    画像を消す時にタグで画像を指定できる
    これを利用してundoを実装
    undoすると順番が一つ戻る
    ３番目の画像をundoで決して新たに画像を表示したらそれは３番目の画像になる(スタックみたいな感じ)
    後入れ先出し
    allClearはメタキャラクタ(ワイルドカード)を使って一括で消せないかといろいろ試したが無理だた
'''

#ウィジェット関連
#フレーム生成#操作パネル
F0 = LabelFrame(root,relief="raised",borderwidth=15,bg="gray",text="操作パネル",font=(font,fontsize),fg="#7fffd4")
#ボタン生成
#生成ボタン
drwrbtn = Button(F0,text=u'標準画像生成',font=(font,fontsize))
drwrbtn.bind("<Button-1>",drawer)
drwrbtn.grid(row=1,column=1)

sdrwbtn = Button(F0,text=u'リサイズ挿入',font=(font,fontsize))
sdrwbtn.bind("<Button-1>",resizedDrawer)
sdrwbtn.grid(row=2,column=1)

#全消しボタン
clnbtn = Button(F0,text=u'画像全消し',font=(font,fontsize))
clnbtn.bind("<Button-1>",allClear)
clnbtn.grid(row=2,column=2)

#undoボタン
undobtn = Button(F0,text=u'直前の画像を消す',font=(font,fontsize))
undobtn.bind("<Button-1>",undo)
undobtn.grid(row=1,column=2)

#やめるボタン
exitter = Button(F0,text=u'終了',font=(font,fontsize),command=quit)
exitter.grid(row=1,column=3)

#画面いっぱいに表示できるよ
F0.pack(fill=BOTH,expand=True)

'''
    xxx.grid(row=行,column=列)みたいな感じでフレームの中で配置してる
'''


#キャンバス作成
cv = Canvas(sub,bg="#00a2e7",width=800,height=800)
cv.pack(fill=BOTH,expand=True)
cv.update()

root.mainloop()

