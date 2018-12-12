#! /usr/local/bin python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Notebook
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
    precv.create_image(precv.winfo_width()//2,precv.winfo_height()//2,image=img_tk[combo.get()],tag="prev")

def OWARI(event):
    quit()

def passer():
    pass

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


if __name__ == "__main__":

    #操作パネル管理？？
    root = Tk()
    root.geometry("400x200+810+40")
    root.title("操作")

    #キャンバス管理？？
    sub = Toplevel()
    sub.geometry("800x800+5+40")
    sub.title("キャンバス")

    #これがキャンバス
    cv = Canvas(sub,bg="#00a2e7",width=800,height=800)
    cv.pack(fill=BOTH,expand=True)
    cv.update()

    #タブで切り替え
    subsub = Toplevel()
    subsub.geometry("500x500+810+280")
    subsub.title("いろいろな機能")

    nb = Notebook(subsub)
    nb.pack(fill=BOTH,expand=True)

    tab1 = Frame(nb)
    nb.add(tab1,text="プレビュー")

    tab2 = Frame(nb)
    nb.add(tab2,text="キーチェック")

    precv = Canvas(tab1,bg="#00a2e7",width=360,height=360)
    precv.pack(fill=BOTH,expand=True)
    precv.update()

    cvver = Canvas(tab2,bg="gray",width=400,height=500)
    cvver.pack(fill=BOTH,expand=True)

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
    combo.current(46)
    combo.pack()

    #ウィジェット関連
    #ラベルフレーム生成#操作パネル
    F0 = LabelFrame(root,relief="raised",borderwidth=15,background="gray",text="操作パネル",font=(font,fontsize),fg="#7fffd4")

    #キーバインド
    root.focus_set()
    root.bind_all("<Key-q>",OWARI)
    root.bind_all("<Return>",drawer)
    root.bind_all("<Shift-Return>",resizedDrawer)
    root.bind_all("<Control-Return>",FUISION)
    root.bind_all("<Delete>",allClear)
    root.bind_all("<BackSpace>",undo)
    root.bind_all("<Key-p>",updatePrev)

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


    QRelease(True)
    SHIFTRelease(True)
    DELETERelease(True)
    BACKSPACERelease(True)
    RETURNRelease(True)
    CONTROLRelease(True)

    root.mainloop()