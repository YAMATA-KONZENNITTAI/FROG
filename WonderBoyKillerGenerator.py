#! /usr/local/bin python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.ttk import Combobox 
from PIL import Image,ImageTk
from os import listdir
from random import randint
from time import sleep
from threading import Timer

def rndX():#X座標
    return randint(0,cv.winfo_width())

def rndY():#Y座標
    return randint(0,cv.winfo_height())

def resize(wLow,wHigh,hLow,hHigh):
    global img,reimg_tk,num#上の方で宣言した変数を参照すると宣言
    reimg = img[combo.get()].resize((randint(wLow,wHigh),randint(hLow,hHigh)))#リサイズ
    reimg_tk.append(ImageTk.PhotoImage(reimg))#挿入ように変換
    return reimg_tk[num]

def drawer(event):
    global imgnum
    name = combo.get()
    #画像を表示
    cv.create_image(rndX(),rndY(),image=img_tk[name],anchor=CENTER,tag=("p"*imgnum))
    #画像管理用の変数を更新
    imgnum += 1

#応急処置
def anyDraw(X,Y,gazou,tagn=0):
    global imgnum,num
    #画像を表示
    if not tagn == 0:
        cv.create_image(X,Y,image=gazou,anchor=CENTER,tag=("p"*tagn))
    else:
        cv.create_image(X,Y,image=gazou,anchor=CENTER,tag=("any"*X))

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

def undo(event):#画像を一つ消す
    global imgnum,num
    #表示した画像の順番が狂わないように調整
    if(imgnum > 1):
        imgnum -= 1
    cv.delete("p"*imgnum)

#ちょっと無理やりすぎるけど三位一体復活
def FUISION(event):
    global imgnum,num
    X = rndX()
    Y = rndY()
    anyDraw(X,Y,resize(100,100,100,100))
    num += 1
    Timer(0.5,anyDraw,(X,Y+100,resize(100,100,100,100),)).start()
    num += 1
    Timer(1.0,anyDraw,(X,Y+200,resize(100,100,100,100),)).start()
    num += 1
    Timer(1.5,cv.delete,("any"*X,)).start()
    Timer(1.5,anyDraw,(X,Y+100,resize(100,100,300,300),imgnum)).start()
    num += 1
    imgnum += 1

'''
    cv.create_image(X,Y,image=before,anchor=CENTER,tag="f"*(X//10))
    Y += 100#Y座標すらし
    cv.update()#キャンバスを更新しないと画像表示が反映されない
    sleep(0.5)#ディレイ0.5秒
    cv.create_image(X,Y,image=before,anchor=CENTER,tag="f"*(X//10))
    Y += 100#Y座標すらし
    cv.update()#キャンバスを更新しないと画像表示が反映されない
    sleep(0.5)#ディレイ0.5秒
    cv.create_image(X,Y,image=before,anchor=CENTER,tag="f"*(X//10))
    Y += 100#Y座標すらし
    cv.update()#キャンバスを更新しないと画像表示が反映されない
    sleep(0.5)#ディレイ0.5秒
    cv.delete("f"*(X//10))#画像削除
    cv.create_image(X,Y-200,image=After,anchor=CENTER,tag="p"*imgnum)#合体後表示
'''

def allClear(event):
    global imgnum,num
    #画像を全部消す
    for i in range(imgnum + 1):#普通の画像を全部消す
        cv.delete("p"*i)
    del reimg_tk[:]#リサイズ画像を全部消す
    #管理用変数リセット
    imgnum = 1
    num = 0

def updatePrev(event=True):
    precv.delete("prev")
    precv.create_image(170,160,image=img_tk[combo.get()],tag="prev")

def OWARI(event):
    quit()

def passer():
    pass


if __name__ == "__main__":

    #操作パネル管理？？
    root = Tk()
    root.geometry("400x200+810+40")
    root.title("操作")

    #キャンバス管理？？
    sub = Toplevel()
    sub.geometry("800x800+5+40")
    sub.title("てるそ")

    #これがキャンバス
    cv = Canvas(sub,bg="#00a2e7",width=800,height=800)
    cv.pack(fill=BOTH,expand=True)
    cv.update()

    #プレビュー
    previewer = Toplevel()
    previewer.geometry("350x350+810+280")
    previewer.title("プレビュー")
    previewer.resizable(0,0)

    precv = Canvas(previewer,bg="#00a2e7",width=360,height=360)
    precv.pack(fill=BOTH,expand=True)
    precv.update()

    #ここでいろいろな変数を宣言しておきます（いろいろ管理する為の変数が多い）
    #画像を管理する辞書型
    img = { i : Image.open("../../with_unkochan/" + i) for i in sorted(listdir("../../with_unkochan"))}
    img_tk = { i : ImageTk.PhotoImage(Image.open("../../with_unkochan/" + i)) for i in sorted(listdir("../../with_unkochan"))}
    font = "Impact"#                   ボタンなどのフォントを一元管理する時に使う
    fontsize = 20#                     同様にサイズも
    fontcolor = "#7fffd4" #            同様にカラーも
    imgnum = 1#                        画像表示順番を管理する為の変数
    reimg_tk = []#                     リサイズした画像を入れる配列
    num = 0#                           配列を管理する為の変数

    #画像選択管理
    combo = Combobox(root,state="readonly")
    combo["values"] = list(img_tk.keys())
    combo["postcommand"] = updatePrev#lambda :precv.create_image(170,160,image=img_tk[combo.get()],tag="prev")
    combo.current(0)
    combo.pack()

    #ウィジェット関連
    #ラベルフレーム生成#操作パネル
    F0 = LabelFrame(root,relief="raised",borderwidth=15,background="gray",text="操作パネル",font=(font,fontsize),fg="#7fffd4")

    #キーバインド
    root.focus_set()
    root.bind_all("<q>",OWARI)
    root.bind_all("<Return>",drawer)
    root.bind_all("<Shift-Return>",resizedDrawer)
    root.bind_all("<Control-Return>",FUISION)
    root.bind_all("<Delete>",allClear)
    root.bind_all("<BackSpace>",undo)
    root.bind_all("<p>",updatePrev)

    #ボタン生成
    #生成ボタン
    drwrbtn = Button(F0,text=u'標準画像生成',font=(font,fontsize))
    drwrbtn.bind("<Button-1>",drawer)
    drwrbtn.grid(row=1,column=1,sticky=NSEW)

    #リサイズ生成ボタン
    sdrwbtn = Button(F0,text=u'リサイズ挿入',font=(font,fontsize))
    sdrwbtn.bind("<Button-1>",resizedDrawer)
    sdrwbtn.grid(row=2,column=1,sticky=NSEW)

    #合体挿入ボタン
    fusionner = Button(F0,text=u'三位一体挿入',font=(font,fontsize))
    fusionner.bind("<Button-1>",FUISION)
    fusionner.grid(row=3,column=1,sticky=NSEW)

    #プレビューボタン
    preview = Button(F0,text=u'プレビュー',font=(font,fontsize))
    preview.bind("<Button-1>", updatePrev)
    preview.grid(row=4,column=1,sticky=NSEW)

    #全消しボタン
    clnbtn = Button(F0,text=u'画像全消し',font=(font,fontsize))
    clnbtn.bind("<Button-1>",allClear)
    clnbtn.grid(row=2,column=2,sticky=NSEW)

    #undoボタン
    undobtn = Button(F0,text=u'直前の画像を消す',font=(font,fontsize))
    undobtn.bind("<Button-1>",undo)
    undobtn.grid(row=1,column=2,sticky=NSEW)

    #やめるボタン
    exitter = Button(F0,text=u'終了',font=(font,fontsize),command=root.destroy)
    exitter.grid(row=1,column=3,sticky=NSEW)

    #画面いっぱいに表示できるよ
    F0.pack(fill=BOTH,expand=True)

    root.mainloop()






#print(sorted(listdir("../../with_unkochan")))
#print(list(img_tk.keys()))

#j = 0
#for i in list(img_tk.keys()):
#    cv.create_image(j,j,image=img_tk[i])
#    j += 300

#def drawer(event):
#    name = combo.get()
#    cv.create_image(100,100,image=img_tk[name],anchor=CENTER)