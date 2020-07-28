from tkinter import *
from tkinter.font import Font
import os

def myClick():
    brandfile = open("thebrand.txt", "w")
    brandfile.write(str(brandentry.get()))
    brandfile.close()
    chromepathf = open("chromepath.txt", "w")
    chromepathf.write(str(chromepath.get()))
    chromepathf.close()
    currencyf = open("currency.txt", "w")
    currencyf.write(str(currencyinput.get()))
    currencyf.close()
    if subitovar.get()==1:
        print("Subito")
        os.system("python3 subitoscrapper.py")
    if feelwayvar.get()==1:
        print("Feelway")
        os.system("python3 feelwayscrapper.py")
    if poshmarkvar.get()==1:
        print("Poshmark")
        os.system("python3 poshmarkscrape.py")
    if rebellevar.get()==1:
        print("Rebelle")
        os.system("python3 rebellescrapper.py")
    if yjvar.get()==1:
        print("Y!J")
        os.system("python3 yjscrape.py")
    if kindalvar.get()==1:
        print("Kindal")
        os.system("python3 kindalscraper.py")
    if depopvar.get()==1:
        print("Depop")
        os.system("python3 depopscraper.py")
    if tncvar.get()==1:
        print("TheNextCloset")
        os.system("python3 thenextclosetscrapper.py")
    if sobumpvar.get()==1:
        print("Sobump")
        os.system("python3 sobumpspider.py")
    if ricardovar.get()==1:
        print("Ricardo")
        os.system("python3 ricardoscrapper.py")
    if trefacvar.get()==1:
        print("Trefac")
        os.system("python3 trefacscrapper.py")
    if frilvar.get()==1:
        print("Fril")
        os.system("python3 frilscraper.py")

#--Home page pimping--
master = Tk(className="GETGOT")
master.wm_title("GETGOT")
master.geometry('600x800'.format(600, 800))
master.configure(bg='black')

title = Label(master, text="GETGOT",anchor='w')
title.configure(foreground='purple',bg='black',font=("Times",250),anchor='w')
title.grid(row=0,column=0,columnspan=5)

authour = Label(master, text="by distraught (v1)",anchor='w')
authour.configure(foreground='purple',bg='black',font=("Times",50),anchor='w')
authour.grid(row=1,column=0,columnspan=5)

about = Text(master, width=56, height=15)
about.configure(foreground='purple',bg='black',font=("Times",30), borderwidth=0, highlightthickness=0)
about.grid(row=2,column=0,columnspan=5)
abouttext = """Open source data-mining tool for luxury second hand
clothing sites that collects images & listing data

1) Input chrome path into "Enter Chrome path".
(e.g '/usr/local/share/chromedriver')

2) Input Currency into "Enter Currency"
(e.g 'USD', 'YEN', 'Whatever')

3) Input brand name into "Enter brand name"
(e.g 'Rick Owens', 'Damir Doma', 'Gucci')

4) Select which vendors
(See site details for differences)

5) Press button
(Recommend using over night)"""
about.insert(END, abouttext)

currencyinput= Entry(master, width=30, fg='purple',bg='white', font=("Times",35))
currencyinput.insert(0,"Entry Currency")
currencyinput.grid(row=3,column=0,columnspan=5)

chromepath= Entry(master, width=30, fg='purple',bg='white', font=("Times",35))
chromepath.insert(0,"Enter Chrome path")
chromepath.grid(row=4,column=0,columnspan=5)

brandentry= Entry(master, width=30, fg='purple',bg='white', font=("Times",40))
brandentry.insert(0,"Enter brand name")
brandentry.grid(row=5,column=0,columnspan=5)

subitovar = IntVar()
subito = Checkbutton(master, text="Subito", variable=subitovar ,onvalue=1,offvalue=0)
subito.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
subito.grid(row=6,column=0,columnspan=1,sticky=W)

feelwayvar = IntVar()
feelway = Checkbutton(master, text="FeelWay", variable=feelwayvar ,onvalue=1,offvalue=0)
feelway.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
feelway.grid(row=6,column=1,columnspan=1,sticky=W)

poshmarkvar = IntVar()
poshmark = Checkbutton(master, text="Poshmark", variable=poshmarkvar ,onvalue=1,offvalue=0)
poshmark.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
poshmark.grid(row=6,column=2,columnspan=1,sticky=W)

rebellevar = IntVar()
rebelle = Checkbutton(master, text="Rebelle", variable=rebellevar ,onvalue=1,offvalue=0)
rebelle.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
rebelle.grid(row=6,column=3,columnspan=1,sticky=W)

yjvar = IntVar()
yj = Checkbutton(master, text="Y!J", variable=yjvar ,onvalue=1,offvalue=0)
yj.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
yj.grid(row=7,column=0,columnspan=1,sticky=W)

kindalvar = IntVar()
kindal = Checkbutton(master, text="Kindal", variable=kindalvar ,onvalue=1,offvalue=0)
kindal.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
kindal.grid(row=7,column=1,columnspan=1,sticky=W)

depopvar = IntVar()
depop = Checkbutton(master, text="Depop", variable=depopvar ,onvalue=1,offvalue=0)
depop.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
depop.grid(row=7,column=2,columnspan=1,sticky=W)

tncvar = IntVar()
tnc = Checkbutton(master, text="NextCloset", variable=tncvar ,onvalue=1,offvalue=0)
tnc.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
tnc.grid(row=7,column=3,columnspan=1,sticky=W)

sobumpvar = IntVar()
sobump = Checkbutton(master, text="Sobump", variable=sobumpvar ,onvalue=1,offvalue=0)
sobump.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
sobump.grid(row=8,column=0,columnspan=1,sticky=W)

ricardovar = IntVar()
ricardo = Checkbutton(master, text="Ricardo", variable=ricardovar ,onvalue=1,offvalue=0)
ricardo.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
ricardo.grid(row=8,column=1,columnspan=1,sticky=W)

trefacvar = IntVar()
trefac = Checkbutton(master, text="Trefac", variable=trefacvar ,onvalue=1,offvalue=0)
trefac.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
trefac.grid(row=8,column=2,columnspan=1,sticky=W)

frilvar = IntVar()
fril = Checkbutton(master, text="Fril", variable=frilvar ,onvalue=1,offvalue=0)
fril.configure(foreground='purple',bg='black',font=("Times",40), borderwidth=0, highlightthickness=0)
fril.grid(row=8,column=3,columnspan=2,sticky=W)

myButton = Button(master, text='Mine !', command=myClick, width=10,height=1)
myButton.configure(foreground='purple',bg='white',font=("Times",80), borderwidth=1, highlightthickness=1)
myButton.grid(row=9,column=0,columnspan=5)

master.mainloop()
