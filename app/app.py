from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_caching import Cache
from Code.rule import translator
import psycopg2
import re

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
hostname = ''
database = ''
username = ''
pwd = ''
port_id = 5432

dictionary = list()
wordList = list()
thTranList = list()

def collectDictionary():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)

        cur = conn.cursor()
        cur.execute(f"SELECT word, thtran, pos, definition, lanna, rate FROM dictionary4")
        conn.commit()
        for (word, thtran, pos, definition, lanna, rate) in cur.fetchall():
            if not rate:
                    rate = 0
            if word and thtran:
                wordList.append(word)
                thTranList.append(thtran)
                dictionary.append({
                    'word': word,
                    'lanna': lanna,
                    'definition': definition,
                    'pos': pos,
                    'thTran': thtran,
                    'rate': rate
                })
                
            

        
    except Exception as error:
        print(error)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

collectDictionary()

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sinsuda:SmkjeFj7wdUMZZc08KUBSYD3gtVXdJ8i@dpg-cii6d9lph6erq6mrtjkg-a.singapore-postgres.render.com/dbname_vx2a'


@app.route('/')
def home():
    return render_template('index.html', lang1="ไทยกลาง", lang2="ไทยถิ่นเหนือ", wordList=wordList, thTranList=thTranList)
@app.route('/<int:Direction>')
def home2(Direction):
    if Direction % 2 == 0:
        lang1 = "ไทยกลาง"
        lang2 = "ไทยถิ่นเหนือ"
    elif Direction % 2 == 1:
        lang1 = "ไทยถิ่นเหนือ"
        lang2 = "ไทยกลาง"
    return render_template('index.html', lang1=lang1, lang2=lang2, wordList=wordList, thTranList=thTranList)
@app.route('/<int:Direction>/<Input>')
def index(Direction, Input):
    Direction= int(Direction)
    if Direction % 2 == 0:
        lang1 = "ไทยกลาง"
        lang2 = "ไทยถิ่นเหนือ"
    elif Direction % 2 == 1:
        lang1 = "ไทยถิ่นเหนือ"
        lang2 = "ไทยกลาง"
    output_list = translator(Input, Direction, dictionary).trans()
    
    if Input == "":
        return render_template('index.html', theinput=Input, theoutput="", lang1=lang1, lang2=lang2, wordList=wordList, thTranList=thTranList)


    output = output_list[0]
    messages = []

    if len(output_list) > 1 and output_list[1]:
        synonyms = output_list[1]
        #synonyms = [('noun', [('ไก่', ['chicken', 'cock', 'hen']),('ลูกไก่',['chick'])]),('adj', [('ตาขาว', ['timit', 'fearful', 'chicken'])])]
        messages.append(synonyms)

#definitions = [('noun',['ความหมายที่1','ความหมายที่2']),('adjective',['ความหมายที่1'])]
    if len(output_list) > 2 and output_list[2]:
        definitions = output_list[2]
        messages.append(definitions)
    if len(output_list) > 3 and output_list[3]:
        lanna = output_list[3]
        messages.append(lanna)

    flash(messages)
    return render_template('index.html', theinput=Input, theoutput=output, lang1=lang1, lang2=lang2, wordList=wordList, thTranList=thTranList)

@app.route("/rated", methods=['POST'])
def rate():
    conn = None
    cur = None
    rateInput = dict(request.form.items())
    direction = int(rateInput.get('direction', ''))
    add = int(rateInput.get('addOrRedo', ''))
    if direction % 2 == 0:
        thWord = rateInput.get('inputWord', '')
        nWord = rateInput.get('outputWord', '')
    else:
        thWord = rateInput.get('outputWord', '')
        nWord = rateInput.get('inputWord', '')
    
    if add % 2 == 1:
        add = True
    else:
        add = False
    
    try:
        conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)

        cur = conn.cursor()

        cur.execute(f"SELECT word, thtran, rate FROM dictionary WHERE word='{nWord}' AND thtran='{thWord}'")

        if add:
            for (word, thtran, rate) in cur.fetchall():
                if rate:
                    rate += 1
                    cur.execute(f"UPDATE dictionary SET rate = {rate} WHERE word='{nWord}' AND thtran='{thWord}'")
                else:
                    cur.execute(f"UPDATE dictionary SET rate = 1 WHERE word='{nWord}' AND thtran='{thWord}'")
        else:
            for (word, thtran, rate) in cur.fetchall():
                rate -= 1
                cur.execute(f"UPDATE dictionary SET rate = {rate} WHERE word='{nWord}' AND thtran='{thWord}'")
        conn.commit()
        
    except Exception as error:
        print(error)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    return jsonify(messages = "success")

@app.route("/added", methods=['POST'])
def addWord():
    addWordInput = dict(request.form.items())
    nWord = addWordInput.get('nword', '')
    thWord = addWordInput.get('thword', '')
    pos = addWordInput.get('pos', '')
    definition = addWordInput.get('definition', '')

    try:
        conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)

        cur = conn.cursor()
        insert_script = 'INSERT INTO add_word (word, thtran, pos, definition) VALUES (%s, %s, %s, %s)'
        insert_value = (nWord, thWord, pos, definition)
        cur.execute(insert_script, insert_value)
        conn.commit()
        
    except Exception as error:
        print(error)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return jsonify(messages = "success")

if __name__ == "__main__":
    #app.run(debug=True)
    app.run()
