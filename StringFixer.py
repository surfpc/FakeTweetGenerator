# -*- coding: utf-8 -*-

import MarkovTweet as mt
import tkinter as tk
import html as html

def main():
    
    
    m = tk.Tk()
    topf = tk.Frame(m, width=100, height=1)
    botf = tk.Frame(m, width=100, height=10)
    
    tweet = mt.MarkovTweet("", "", "", "")
    
    l = tk.Label(botf, text='', width=75, height=10) 
    w = tk.Entry(topf, text='ID', width=25)
    w.grid(row=0, column=0)
    w.insert(0, '25073877')
    b = tk.Button(topf, text='Generate Tweet', width=25, command=lambda: l.config(text=html.unescape(tweet.tweet(user_id=int(w.get())))))
    b.grid(row=0, column=1) 
    
    
    l.pack()
    topf.pack()
    botf.pack()
    m.mainloop()

    
if __name__ == '__main__':
    main()
