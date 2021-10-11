import MeCab
import sqlite3
import random
import re
from datetime import datetime


def main():
    t = TwoContextGen("gingatetsudounoyoru")
    t.set_data()
    #t.get_data(10)
    t.calc_textsize()
    #t.set_textsize(500)
    #t.insert_lines(True)
    #t.create()
    t.create2()
    t.save()
    t.show()
    t.close()
    
    
class TwoContextGen:
    def __init__(self, title):
        self.title = title
        self.title_out = '{}_{:%H%M%S}'.format(title, datetime.now())
        self.conn = sqlite3.connect('{}.db'.format(self.title))
        self.cur = self.conn.cursor()
        self.mecab = MeCab.Tagger("-Osimple")
        
        self.textsize = 2000
        self.newlines = False
        self.alltext = []
        
        
    def create(self, fst_w="\u3000", fst_d="記号-空白"):
        sec_w = fst_w
        sec_d = fst_d
        cnt = 0;
        
        while True:
            print("{} / {} -> {} | {}".format(cnt, self.textsize, sec_w, sec_d), end='\r', flush=True)
            
            sec_w, sec_d = self.select(sec_w, sec_d)
            
            if sec_w == None and sec_d == None:
                sec_w, sec_d = '\u3000', "記号-空白"
                continue
               
            cnt += 1
            if cnt >= self.textsize and sec_w == "。":
                print("finally: {} words".format(len(self.alltext)))
                self.alltext.append("。")
                break
                
                
    def create2(self, fst_w="\u3000", fst_d="記号-空白"):
        sec_w1 = fst_w
        sec_d1 = fst_d
        sec_w2 = None
        sec_d2 = None
        cnt = 1;
        
        sec_w1, sec_d1, sec_w2, sec_d2 = self.select2(sec_w1, sec_d1)
        
        while True:
            print("{} / {} -> {} | {}".format(cnt, self.textsize, sec_w1, sec_d1), end='\r', flush=True)
            
            sec_w1, sec_d1, sec_w2, sec_d2 = self.select3(sec_w1, sec_d1, sec_w2, sec_d2)
            
            if sec_w1 == None and sec_d1 == None and sec_w2 == None and sec_d2 == None:
                sec_w1, sec_d1 = '\u3000', "記号-空白"
                sec_w1, sec_d, sec_w2, sec_d2 = self.select2(sec_w1, sec_d1)
                continue
               
            cnt += 1
            if cnt >= self.textsize and sec_w2 == "。":
                print("finally: {} words".format(len(self.alltext)))
                self.alltext.append(sec_w1)
                self.alltext.append("。")
                break
        
            
    def show(self):
        print(''.join(self.alltext))
        
    def save(self):
        with open('{}.txt'.format(self.title_out), 'w') as f:
            f.write(''.join(self.alltext))
            
        
        
    def select(self, fst_w, fst_d):
        self.cur.execute('SELECT w1, d1, w2, d2, w3, d3 FROM words WHERE w1 = ? and d1 = ?', (fst_w, fst_d))
        rows = self.cur.fetchall()

        if len(rows) > 0:
            idx = random.randrange(len(rows))
            w1 = rows[idx][0]
            w2 = rows[idx][2]
            w3 = rows[idx][4]
            d3 = rows[idx][5]
            
            if self.newlines and w1 == "\u3000":
                self.alltext.append("\n")
            self.alltext.append(w1)
            
            if self.newlines and w2 == "\u3000":
                self.alltext.append("\n")
            self.alltext.append(w2)
            
            return w3, d3

        else:
            return None, None
            
    
    
    def select2(self, fst_w1, fst_d1):
        self.cur.execute('SELECT w1, d1, w2, d2, w3, d3 FROM words WHERE w1 = ? and d1 = ?', (fst_w1, fst_d1))
        rows = self.cur.fetchall()

        if len(rows) > 0:
            idx = random.randrange(len(rows))
            w1 = rows[idx][0]
            d1 = rows[idx][1]
            w2 = rows[idx][2]
            d2 = rows[idx][3]
            w3 = rows[idx][4]
            d3 = rows[idx][5]
            
            if self.newlines and w1 == "\u3000":
                self.alltext.append("\n")
            self.alltext.append(w1)
            
            return w2, d2, w3, d3

        else:
            return None, None, None, None

    
    def select3(self, fst_w1, fst_d1, fst_w2, fst_d2):
        self.cur.execute('SELECT w1, d1, w2, d2, w3, d3 FROM words WHERE w1 = ? and d1 = ? and w2 = ? and d2 = ?', (fst_w1, fst_d1, fst_w2, fst_d2))
        rows = self.cur.fetchall()

        if len(rows) > 0:
            idx = random.randrange(len(rows))
            w1 = rows[idx][0]
            d1 = rows[idx][1]
            w2 = rows[idx][2]
            d2 = rows[idx][3]
            w3 = rows[idx][4]
            d3 = rows[idx][5]
            
            if self.newlines and w1 == "\u3000":
                self.alltext.append("\n")
            self.alltext.append(w1)
            
            return w2, d2, w3, d3

        else:
            return None, None, None, None
            
            
    def calc_textsize(self):
        size = 0
        self.cur.execute('SELECT count(*) from words')
        for row in self.cur:
            size = row[0]
            
        self.textsize = size
        
        
    def set_textsize(self, size):
        self.textsize = size
        
    def insert_lines(self, require=True):
        self.newlines = require
            

    def get_data(self, limit):
        
        self.cur.execute('SELECT w1, d1, w2, d2, w3, d3 FROM words LIMIT ?', (limit,))
        for i, row in enumerate(self.cur):
                print(row)
        
        

    def set_data(self):
        # sqlite3
        self.cur.execute('DROP TABLE IF EXISTS words')
        self.cur.execute('CREATE TABLE words(w1 STRING, d1, STRING, w2 STRING, d2 STRING, w3 STRING, d3 STRING)')
        #file
        f = open('{}.txt'.format(self.title), 'r', encoding='utf-8')
        line = f.read().replace("\n", "")
        words = re.split(r'[\t\n]', self.mecab.parse(line).replace("EOS\n", ""))[:-1]
        
        length = len(words) - 4
        
        for i in range(0, length, 2):
            w1 = words[i]
            d1 = words[i+1]
            w2 = words[i+2]
            d2 = words[i+3]
            w3 = words[i+4]
            d3 = words[i+5]
            
            self.cur.execute('INSERT INTO words(w1, d1, w2, d2, w3, d3) values(?, ?, ?, ?, ?, ?)', (w1, d1, w2, d2, w3, d3,))
            print("{} / {}".format(i, length), end='\r', flush=True)
            
        f.close()
        self.conn.commit()
        
        
    def set_title(self, title):
        self.title_out = title
        
        
    def close(self):
        self.conn.close()


if __name__ == '__main__':
    main()
