# -*- coding: utf-8 -*-

import MarkovTweet as mt
import tkinter as tk
import html as html

def main():
    
    
    m = tk.Tk()
    topf = tk.Frame(m, width=100, height=1)
    botf = tk.Frame(m, width=100, height=10)
    
    
    
    l = tk.Label(botf, text='', width=75, height=10)
    
    cKey = tk.Entry(m, width=100)
    cKey.insert(0, 'consumer key')
    
    cSec = tk.Entry(m, width=100)
    cSec.insert(0, 'consumer secret')
    
    aTok = tk.Entry(m, width=100)
    aTok.insert(0, 'access token')
    
    aSec = tk.Entry(m, width=100)
    aSec.insert(0, 'access secret')
    
    
    
    tweet = mt.MarkovTweet(cKey.get(), cSec.get(), aTok.get(), aSec.get())
    
    updateBut = tk.Button(m, width=25, text='update tweepy', command=lambda: tweet.updateValues(cKey.get(), cSec.get(), aTok.get(), aSec.get()))
    
    
    w = tk.Entry(topf, text='ID', width=25)
    w.grid(row=0, column=0)
    w.insert(0, '25073877')
    b = tk.Button(topf, text='Generate Tweet', width=25, command=lambda: l.config(text=html.unescape(tweet.tweet(user_id=int(w.get())))))
    b.grid(row=0, column=1) 
    
    
    cKey.pack()
    cSec.pack()
    aTok.pack()
    aSec.pack()
    updateBut.pack()
    
    l.pack()
    topf.pack()
    botf.pack()
    m.mainloop()

    
if __name__ == '__main__':
    main()
