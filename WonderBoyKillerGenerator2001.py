#! /usr/local/bin python3
# -*- coding: utf-8 -*-

from tkinter import *
from PIL import Image,ImageTk
from random import randint
from time import sleep

'''
    オブジェクト指向でない場合？？？？？？？
    メインとなるウィンドウ(root)を先に生成しないと
    画像を読み込もうとした時にエラーがでてしまう
'''

#ウィンドウ作成その他調整
#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*

#メインウィンドウ
root = Tk()
root.geometry("400x200+810+40")
root.title("ワンダーボーイキラージェネレータ操作パネル")

#サブウィンドウ
sub = Toplevel()
sub.geometry("800x800+5+40")
sub.title("ワンダーボーイキラージェネレータver2.01")

#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*

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
    なぜわざわざリストを作るか
    いろいろと試行錯誤している中で気づいたことがいくつかある
    まず通常サイズの画像を表示する場合、一つの変数(image_tk)を参照し続ける、或いは同じ画像であることに問題がない
    しかし、大きさが違う画像を表示する場合に一つの変数を使いまわしてしまうと、リサイズして変数の情報を更新する際に
    すでに画面に表示されている画像が参照している変数の情報も更新されてしまう。どういう理由かはわからないが、この時
    すでに表示されている画像は消えてしまう。デバッガー求む
    以下に上記の現象が発生していたコードを記述しておく書きません
'''

#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*
#キャンバスの大きさに合わせて上限が変わる乱数(以前はラムダ式で定義していたけど普通の関数にしてみた)
def rndX():#X座標
    return randint(0,cv.winfo_width())

def rndY():#Y座標
    return randint(0,cv.winfo_height())

#画像をリサイズする為の関数
def resize(wLow,wHigh,hLow,hHigh):
    global img,reimg_tk,num#上の方で宣言した変数を参照すると宣言
    reimg = img.resize((randint(wLow,wHigh),randint(hLow,hHigh)))#リサイズ
    reimg_tk.append(ImageTk.PhotoImage(reimg))#挿入ように変換
    return reimg_tk[num]

#ボタンを押した時に呼び出す関数
def drawer(event):#普通の画像を挿入する関数
    global imgnum
    #画像を表示
    cv.create_image(rndX(),rndY(),image=img_tk,anchor=CENTER,tag=("p"*imgnum))
    #画像管理用の変数を更新
    imgnum += 1

def resizedDrawer(event):#リサイズした画像を挿入する関数
    global imgnum,num
    #画像を表示
    #大きすぎる画像の出現頻度を下げる 1/6ぐらいの確率で一つ目の
    if(randint(1,6) == 1):
        cv.create_image(rndX(),rndY(),image=resize(1,1000,1,1000),anchor=CENTER,tag=("p"*imgnum))
    else:
        cv.create_image(rndX(),rndY(),image=resize(1,400,1,400),anchor=CENTER,tag=("p"*imgnum))
    #配列管理用変数更新
    num += 1
    #画像管理用変数の更新
    imgnum += 1

def fusion(event):
    global imgnum,num
    X = rndX()#初回だけX座標ランダムにする為
    Y = rndY()#初回だけY座標ランダムにする為
    for i in range(3):#３匹縦に表示する
        cv.create_image(X,Y,image=resize(100,100,100,100),anchor=CENTER,tag="fusion")
        Y += 100#Y座標すらし
        num+=1#resizeを呼び出してるからリストの添字を更新
        cv.update()#キャンバスを更新しないと画像表示が反映されない
        sleep(0.5)#ディレイ0.5秒
    num -= 3#表示した3つを消すからリストの添字を戻しておく
    cv.delete("fusion")#画像削除
    del reimg_tk[:-4:-1]#画像データ削除
    cv.create_image(X,Y-200,image=resize(100,100,300,300),anchor=CENTER,tag=("p"*imgnum))#合体後表示
    #配列管理用変数更新
    num += 1
    #画像管理用変数の更新
    imgnum += 1
    #print(reimg_tk)#デバッグよう

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

def OWARI(event):
    quit()

#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*

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

#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*
#ウィジェット関連
#ラベルフレーム生成#操作パネル
F0 = LabelFrame(root,relief="raised",borderwidth=15,bg="gray",text="操作パネル",font=(font,fontsize),fg="#7fffd4")

#キーバインド
root.focus_set()
root.bind_all("<q>",OWARI)
root.bind_all("<Return>",drawer)
root.bind_all("<Shift-Return>",resizedDrawer)
root.bind_all("<Control-Return>",fusion)
root.bind_all("<Delete>",allClear)
root.bind_all("<BackSpace>",undo)

#ボタン生成
#生成ボタン
drwrbtn = Button(F0,text=u'標準画像生成',font=(font,fontsize))
drwrbtn.bind("<Button-1>",drawer)
drwrbtn.grid(row=1,column=1)

#リサイズ生成ボタン
sdrwbtn = Button(F0,text=u'リサイズ挿入',font=(font,fontsize))
sdrwbtn.bind("<Button-1>",resizedDrawer)
sdrwbtn.grid(row=2,column=1)

#合体挿入ボタン
fusionner = Button(F0,text=u'三位一体挿入',font=(font,fontsize))
fusionner.bind("<Button-1>",fusion)
fusionner.grid(row=3,column=1)

#全消しボタン
clnbtn = Button(F0,text=u'画像全消し',font=(font,fontsize))
clnbtn.bind("<Button-1>",allClear)
clnbtn.grid(row=2,column=2)

#undoボタン
undobtn = Button(F0,text=u'直前の画像を消す',font=(font,fontsize))
undobtn.bind("<Button-1>",undo)
undobtn.grid(row=1,column=2)

#やめるボタン
exitter = Button(F0,text=u'終了',font=(font,fontsize),command=root.destroy)
exitter.grid(row=1,column=3)

#画面いっぱいに表示できるよ
F0.pack(fill=BOTH,expand=True)

#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*

'''
    xxx.grid(row=行,column=列)みたいな感じでフレームの中で配置してる
'''


#キャンバス作成
cv = Canvas(sub,bg="#00a2e7",width=800,height=800)
cv.pack(fill=BOTH,expand=True)
cv.update()

#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*
#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*

roottter = Toplevel()
roottter.geometry("400x500+810+280")
roottter.title("キーチェッカー")
roottter.resizable(0,0)

def QRelease(event):
    cvver.delete("q")
    cvver.create_polygon(20,20,100,20,100,100,20,100,fill="white",outline="black",width=6,tag="q")
    cvver.create_text(60,57,text="Q",font=("Impact",80),tag="q")
    cvver.update()

def QPress(event):
    cvver.delete("q")
    cvver.create_polygon(20,20,100,20,100,100,20,100,fill="black",outline="white",width=6,tag="q")
    cvver.create_text(60,57,text="押",fill="white",font=("Impact",70),tag="q")
    cvver.update()

def DELETERelease(event):
    cvver.delete("delete")
    cvver.create_polygon(20,110,100,110,100,190,20,190,fill="white",outline="black",width=6,tag="delete")
    cvver.create_text(60,150,text="DELETE\ndelete",font=("Impact",30),fill="black",tag="delete")
    cvver.update()

def DELETEPress(event):
    cvver.delete("delete")
    cvver.create_polygon(20,110,100,110,100,190,20,190,fill="black",outline="white",width=6,tag="delete")
    cvver.create_text(60,150,text="isPre-\nssing!",font=("Impact",30),fill="white",tag="delete")
    cvver.update()

def BACKSPACERelease(event):
    cvver.delete("backspace")
    cvver.create_polygon(250,20,330,20,330,100,250,100,fill="white",outline="black",width=6,tag="backspace")
    cvver.create_text(290,60,text="back\nspace",font=("Impact",31),justify=CENTER,fill="black",tag="backspace")
    cvver.update()

def BACKSPACEPress(event):
    cvver.delete("backspace")
    cvver.create_polygon(250,20,330,20,330,100,250,100,fill="black",outline="white",width=6,tag="backspace")
    cvver.create_text(290,60,text="oshi\nteiru",font=("Impact",31),justify=CENTER,fill="white",tag="backspace")
    cvver.update()

def RETURNRelease(event):
    cvver.delete("return")
    cvver.create_polygon(250,110,360,110,360,220,269,220,269,160,250,160,fill="white",outline="black",width=6,tag="return")
    cvver.create_text(310,150,text="Return\n  Enter",font=("Impact",33),fill="black",tag="return")
    cvver.update()

def RETURNPress(event):
    cvver.delete("return")
    cvver.create_polygon(250,110,360,110,360,220,269,220,269,160,250,160,fill="black",outline="white",width=6,tag="return")
    cvver.create_text(310,150,text="isPre-\n  ssing",font=("Impact",33),fill="white",tag="return")
    cvver.update()

def SHIFTRelease(event):
    cvver.delete("shift")
    cvver.create_polygon(250,230,360,230,360,290,250,290,fill="white",outline="black",width=6,tag="shift")
    cvver.create_text(305,260,text="Shift",font=("Impact",50),fill="black",tag="shift")
    cvver.update()

def SHIFTPress(event):
    cvver.delete("shift")
    cvver.create_polygon(250,230,360,230,360,290,250,290,fill="black",outline="white",width=6,tag="shift")
    cvver.create_text(305,260,text="Press",font=("Impact",50),fill="white",tag="shift")
    cvver.update()

def CONTROLRelease(event):
    cvver.delete("control")
    cvver.create_polygon(20,200,180,200,180,280,20,280,fill="white",outline="black",width=6,tag="control")
    cvver.create_text(100,240,text="Control",font=("Impact",50),fill="black",tag="control")
    cvver.update()

def CONTROLPress(event):
    cvver.delete("control")
    cvver.create_polygon(20,200,180,200,180,280,20,280,fill="black",outline="white",width=6,tag="control")
    cvver.create_text(100,240,text="押now",font=("Impact",50),fill="white",tag="control")
    cvver.update()

def shiftReturn(event):
    SHIFTPress(event)
    RETURNPress(event)

def controlReturn(event):
    CONTROLPress(event)
    RETURNPress(event)


root.bind_all("<Key-q>",QPress,"+")
root.bind_all("<KeyRelease-q>",QRelease,"+")

root.bind_all("<Key-Shift_R>",SHIFTPress,"+")
root.bind_all("<KeyRelease-Shift_R>",SHIFTRelease,"+")

root.bind_all("<Key-Shift_L>",SHIFTPress,"+")
root.bind_all("<KeyRelease-Shift_L>",SHIFTRelease,"+")

root.bind_all("<Key-Delete>",DELETEPress,"+")
root.bind_all("<KeyRelease-Delete>",DELETERelease,"+")

root.bind_all("<Key-Return>",RETURNPress,"+")
root.bind_all("<KeyRelease-Return>",RETURNRelease,"+")

root.bind_all("<Key-BackSpace>",BACKSPACEPress,"+")
root.bind_all("<KeyRelease-BackSpace>",BACKSPACERelease,"+")

root.bind_all("<Key-Control_L>",CONTROLPress,"+")
root.bind_all("<KeyRelease-Control_L>",CONTROLRelease,"+")

root.bind_all("<Shift-Return>",shiftReturn,"+")
root.bind_all("<Control-Return>",controlReturn,"+")

piyo = LabelFrame(roottter,relief="raised",borderwidth=10,bg="gray",text="キーチェッカー",font=("Impact",20),fg="#7fffd4")
piyo.pack(fill=BOTH,expand=True)
cvver = Canvas(piyo,bg="gray",width=400,height=500)
cvver.pack(fill=BOTH,expand=True)


QRelease(True)
SHIFTRelease(True)
DELETERelease(True)
BACKSPACERelease(True)
RETURNRelease(True)
CONTROLRelease(True)
#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*
#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*


root.mainloop()

#◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*:☆:*:◇:*