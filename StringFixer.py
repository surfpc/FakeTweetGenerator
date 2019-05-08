# -*- coding: utf-8 -*-

import MarkovTweet as mt
import tkinter as tk

def main():
    
    
    m = tk.Tk()
    f = tk.Frame(m, width=100, height=10)
    
    l = tk.Label(f, text='', width=75, height=10)
    b = tk.Button(f, text='Generate Tweet', width=25, command=lambda: l.config(text=mt.tweet(user_id=25073877))) #changeLabelText(l, mt.tweet(user_id=25073877)))
    
    
    f.pack()
    b.pack()
    l.pack()
    m.mainloop()
    #tweet = mt.tweet(user_id=25073877)
    #print(tweet)
    
def changeLabelText(label, text):
    label.config(text=text)

    
if __name__ == '__main__':
    main()
