from requests.api import request
import telebot
import os
import requests
from libgen_api import LibgenSearch
from bs4 import BeautifulSoup
from lxml import etree
from telebot.types import Message

class book:
    isbn = []

    def find_isbn(search):
        cookies = {
            'PHPSESSID': 'j34dogr211ktkme77bisrrv9gt',
        }

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://isbnsearch.org/',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
        }

        params = (
            ('s', search),
        )

        response = requests.get('https://isbnsearch.org/search', headers=headers, params=params, cookies=cookies)

        data = response.content.decode('utf-8')
        content = BeautifulSoup(data,'lxml') 
        titles = content.select('h2 a')
        isbns = content.select("p:nth-child(3)")
        ll = len(titles)
        reply='Please Select One Book\n\n\n'
        i=0
        while(i<ll):
            reply+=f'{i+1}. {titles[i].get_text(strip=True)}\n'
            book.isbn.append(isbns[i].get_text(strip=True).replace('ISBN-13: ',""))
            i+=1
        return reply
    
    
    def find_book(isbn):
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://libgen.li/index.php',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
        }

        params = (
            ('req', isbn),
            ('columns[]', 'i'),
            ('objects[]', ['f', 'e', 's', 'a', 'p', 'w']),
            ('topics[]', ['l', 'c', 'f', 'a', 'm', 'r', 's']),
            ('res', '25'),
            ('gmode', 'on'),
        )

        response = requests.get('https://libgen.li/index.php', headers=headers, params=params)
        data = response.content.decode('utf-8')
        content = BeautifulSoup(data,'html.parser') 
        dom = etree.HTML(str(content))
        k= dom.xpath('//*[@id="tablelibgen"]/tbody/tr[1]/td[9]/a[1]//@href')[0]
        response2 = requests.get(k)
        data = response2.content.decode('utf-8')
        content = BeautifulSoup(data,'lxml')         
        lk = content.select_one('a')
        link = f'https://libgen.gs/{lk.get("href")}'
        return link
        
        
    def findBookTitle(search):

        cookies = {
            'objects': 'f%7Ce%7Cs%7Ca%7Cp%7Cw',
            'PHPSESSID': 'ukqi2ura0dd5rrrd6nhjulj2n3',
            'phpbb3_9na6l_u': '1',
            'phpbb3_9na6l_k': '',
            'phpbb3_9na6l_sid': '51b66dd33b2da3806157ee675491bf90',
            'gmode': 'on',
            'curtab': 'f',
            'columns': 't',
            'topics': 'l%7Cf%7Cr%7Cs',
        }

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://libgen.li/index.php',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
        }

        params = (
            ('req', search),
            ('columns[]', 't'),
            ('objects[]', ['f', 'e', 's', 'a', 'p', 'w']),
            ('topics[]', ['l', 'f', 'r', 's']),
            ('res', '25'),
            ('gmode', 'on'),
        )

        response = requests.get('https://libgen.li/index.php', headers=headers, params=params, cookies=cookies)
        data = response.content.decode('utf-8')
        content = BeautifulSoup(data,'html.parser') 
        dom = etree.HTML(str(content))
        k= dom.xpath('//*[@id="tablelibgen"]/tbody/tr[1]/td[9]/a[1]//@href')[0]
        response2 = requests.get(k)
        
        data = response2.content.decode('utf-8')
        content = BeautifulSoup(data,'lxml')         
        lk = content.select_one('a')
        link = f'https://libgen.gs/{lk.get("href")}'
        return link



bot = telebot.TeleBot('5010104630:AAGG0nvUqmIlz0BET-MDCqwbHQ4HcMgnEwM',parse_mode=None)
@bot.message_handler(commands=['start'])
def openingMessage(message):
    test = f'Welcome to test bot { message.from_user.first_name} \nWe currently offer song downloads directly to your telegram device \n Enter Command /download book_name'
    bot.reply_to(message,text=test)

@bot.message_handler(commands=['download'])
def search_isbn(message):
    search = str(message.text)
    search = search.replace('/download ','').strip()
    print(search)
    reply=book.findBookTitle(search)
    bot.send_message(message.chat.id,reply)

@bot.message_handler(commands=['select'])
def search_book(message):
    print(message.text)
    sk = str(message.text).strip().replace('/select ',"")
    bookNo = int(sk)-1
    print(bookNo)
    isbnOfBook = book.isbn[bookNo]
    print(isbnOfBook)
    link = book.find_book(isbn=isbnOfBook)
    bot.send_message(message.chat.id,text=link)
    
    
      
bot.infinity_polling()    



