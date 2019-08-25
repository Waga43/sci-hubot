from pyrogram import Client, Filters

import requests

from bs4 import BeautifulSoup

import traceback

API_URL = "http://sci-hub.tw/"

users = {}

@Client.on_message(Filters.private & Filters.incoming)
def _core(c, m):

    if(users.get(m.chat.id)):
        return
    
    users[m.chat.id] = True
    
    m.reply_chat_action("typing")
    
    MSG = "Processing....."
    
    snt = m.reply_text(text = MSG, disable_notification = True, quote = True)
    
    session = requests.Session()
    
    req_url = API_URL+m.text

    try:
        
        r = session.get(req_url)
        print(r.status_code)
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        article = soup.find("div", id="article")
        print(article)
        
        if(not article):
            
            print('Error!')
            
            snt.edit_text(text = "The document you tried to unlock might not be available or the link/DOI you provided is invalid.")
            
            users.pop(m.chat.id)
            
            return
        
        file_url = article.iframe['src'].split('#')[0]
        
        if(not file_url.startswith('http')):
            
            file_url = 'http:'+file_url
        
        snt.edit_text(text = f"Unlocked document URL.\n\n{file_url}", disable_web_page_preview = True)
        
        users.pop(m.chat.id)
        
        return
    
    except:
        
        traceback.print_exc()
        
        snt.edit_text(text = "The document you tried to unlock might not be available or the link/DOI you provided is invalid.")
        
        users.pop(m.chat.id)
        
        return
    
