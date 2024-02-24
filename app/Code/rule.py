from pythainlp import word_tokenize, sent_tokenize
from pythainlp.tag import pos_tag
import psycopg2


rule2 = {('เรียก', 'ว่า', 'ฮ้องว่า'),
         ('เพราะ', 'ว่า', 'ย้อนว่า'),
         ('ชอบ', 'กิน', 'มัก'),
         ('พูด', 'ชัด', 'อู้ถอบ'),
         ('ทำ', 'อะไร', 'ยะหยัง'),
         ('อย่า','ไป','ไปไป'),
         ('ทั้ง','วัน','หมดวัน')}
rule3 = {('หนึ่ง', 'สอง', 'สาม', 'สี่'), ('', '', '', ''), ('', '', '', '')}
rules = [rule2, rule3]


class translator:
    def __init__(self, inputtext, direction, dictionary):
        self.inputtext = inputtext
        self.dictionary = dictionary
        self.sentencelist = sent_tokenize(inputtext)
        self.outputtext = list()
        self.direction = direction
        self.output = ''
        self.haveOutputState = False
        self.outputPerSentence = tuple()

    def senttrans(self, sentence):
        n = 0
        count = 0
        self.tempoutputtext = sentence[:]
        matchRuleState = False
        matchState = False
        while n < (len(sentence)):
            matchRuleState = False #รีใหม่ตอนเริ่มคำใหม่
            matchState = False
            if self.direction % 2 == 0:
                for rule in rules:
                    if rule == rule2:
                        for (x, y, z) in rule:
                            if n+1 < len(sentence):
                                if sentence[n][0] == x and sentence[n+1][0] == y:
                                    self.haveOutputState = True
                                    self.tempoutputtext[count] = z
                                    del self.tempoutputtext[count+1]
                                    del sentence[n+1]
                                    count += 1
                                    n += 1
                                    matchRuleState = True
                                    break

                    elif rule == rule3:
                        for (w, x, y, z) in rule:
                            if n+2 < len(sentence):
                                if sentence[n][0] == w and sentence[n+1][0] == x and sentence[n+2][0] == y:
                                    self.haveOutputState = True
                                    self.tempoutputtext[count] = z
                                    del self.tempoutputtext[count+2]
                                    del sentence[n+2]
                                    del self.tempoutputtext[count+1]
                                    del sentence[n+1]
                                    count += 1
                                    n += 1
                                    matchRuleState = True
                                    break

            if not matchRuleState:
                rateTemp=[]
                for word_info in self.dictionary:
                    if self.direction % 2 == 0:
                        if sentence[n][0] == word_info['thTran'] and sentence[n][1] == word_info['pos']:
                            self.haveOutputState = True
                            rateTemp.append((word_info['word'], word_info['rate']))
                            matchState = True

                    else:
                        if sentence[n][0] == word_info['word'] and sentence[n][1] == word_info['pos']:
                            self.haveOutputState = True
                            rateTemp.append((word_info['thTran'], word_info['rate']))
                            matchState = True
                if rateTemp:
                    Max = 0
                    for (w, r) in rateTemp:
                        if r >= Max:
                            Max = r
                            self.tempoutputtext[count] = w
                    count += 1
                    n += 1

            if not matchState and not matchRuleState:
                self.tempoutputtext[count] = sentence[n][0]
                count += 1
                n += 1
        print(self.tempoutputtext)
        return (self.tempoutputtext, self.haveOutputState)

    def trans(self):
        matchState = False
        output = "ไม่พบคำแปล"
        if self.direction % 2 == 0: #ไทยกลางเป็นคำเมือง
            synonyms = set()
            definitions = set()
            lanna = ''
            rateTemp=[]
            for word_info in self.dictionary:
                if self.inputtext == word_info['thTran']:
                    matchState = True
                    rateTemp.append((word_info['word'],word_info['lanna'], word_info['rate']))
                    synonyms.add((word_info['pos'], word_info['word']))
                    if word_info['definition'] != "":
                        definitions.add((word_info['pos'], word_info['definition']))
            if rateTemp:
                Max = 0
                for (w, l, r) in rateTemp:
                    if r >= Max:
                        Max = r
                        output = w
                        if l:
                            lanna = l
                        else:
                            lanna = ""

            synonym = []

            if synonyms:
                POSs = ["NOUN", "VERB", "ADJ", "PRON", "CCONJ", "ADP", "INTJ", "PART", "PH"]
                POSth = ["คำนาม", "คำกริยา", "คำคุณศัพท์", "คำสรรพนาม", "คำสันธาน", "คำบุพบท", "คำอุทาน", "Particle", "วลี"]
                noun = dict()
                verb = dict()
                adj = dict()
                pron = dict()
                cconj = dict()
                adp = dict()
                intj = dict()
                part = dict()
                POSLists = [noun, verb, adj, pron, cconj, adp, intj, part]
                for (pos, word) in synonyms:
                    for I in range(len(POSs)):
                        if pos == POSs[I]:
                            synonymList = set()
                            for word_info in self.dictionary:
                                if word_info["word"] == word:
                                    synonymList.add(word_info["thTran"])
                            POSLists[I][word] = synonymList
                            break
                for I in range(len(POSLists)):
                    synonymsGroup = []
                    for nth in POSLists[I].keys():
                        synonymList = POSLists[I][nth]
                        synonymsGroup.append((nth,synonymList))
                    if synonymsGroup:
                        synonym.append((POSth[I], synonymsGroup))
            else:
                synonym.append("none")
            definition = list()
            if definitions:
                POSs = ["NOUN", "VERB", "ADJ", "PRON", "CCONJ", "ADP", "INTJ", "PART", "PH"]
                POSth = ["คำนาม", "คำกริยา", "คำวิเศษณ์", "คำสรรพนาม", "คำสันธาน", "คำบุพบท", "คำอุทาน", "Particle", "วลี"]
                noun = []
                verb = []
                adj = []
                pron = []
                cconj = []
                adp = []
                intj = []
                part = []
                POSLists = [noun, verb, adj, pron, cconj, adp, intj, part]
                for (pos, defi) in definitions:
                    for I in range(len(POSs)):
                        if pos == POSs[I]:
                            POSLists[I].append(defi)
                            break
                for I in range(len(POSLists)):
                    if POSLists[I]:
                        POSLists[I] = list(set(POSLists[I]))
                        defList = []
                        for defi in POSLists[I]:
                            defList.append(defi)
                        definition.append((POSth[I], defList))

            else:
                definition.append('none')
            
            if not lanna:
                lanna = 'none'
            return [
                    output,
                    synonym,
                    definition,
                    lanna
                    ]

        elif self.direction % 2 == 1: #คำเมืองเป็นไทยกลาง
            synonyms = set()
            definitions = set()
            lanna = ''
            rateTemp=[]
            for word_info in self.dictionary:
                if self.inputtext == word_info['word']:
                    matchState = True
                    rateTemp.append((word_info['thTran'],word_info['lanna'], word_info['rate']))
                    synonyms.add((word_info['pos'], word_info['thTran']))
                    if word_info['definition'] != "":
                        definitions.add((word_info['pos'], word_info['definition']))
            
            if rateTemp:
                Max = 0
                for (w, l, r) in rateTemp:
                    if r >= Max:
                        Max = r
                        output = w
                        if l:
                            lanna = l
                        else:
                            lanna = ""

            synonym = []

            if synonyms:
                POSs = ["NOUN", "VERB", "ADJ", "PRON", "CCONJ", "ADP", "INTJ", "PART", "PH"]
                POSth = ["คำนาม", "คำกริยา", "คำวิเศษณ์", "คำสรรพนาม", "คำสันธาน", "คำบุพบท", "คำอุทาน", "Particle", "วลี"]
                noun = dict()
                verb = dict()
                adj = dict()
                pron = dict()
                cconj = dict()
                adp = dict()
                intj = dict()
                part = dict()
                POSLists = [noun, verb, adj, pron, cconj, adp, intj, part]
                for (pos, thTran) in synonyms:
                    for I in range(len(POSs)):
                        if pos == POSs[I]:
                            synonymList = set()
                            for word_info in self.dictionary:
                                if word_info["thTran"] == thTran:
                                    synonymList.add(word_info["word"])
                            POSLists[I][thTran] = synonymList
                            break
                for I in range(len(POSLists)):
                    synonymsGroup = []
                    for th in POSLists[I].keys():
                        synonymList = POSLists[I][th]
                        synonymsGroup.append((th,synonymList))
                    if synonymsGroup:
                        synonym.append((POSth[I], synonymsGroup))
            else:
                synonym.append("none")
            definition = list()
            if definitions:
                POSs = ["NOUN", "VERB", "ADJ", "PRON", "CCONJ", "ADP", "INTJ", "PART", "PH"]
                POSth = ["คำนาม", "คำกริยา", "คำวิเศษณ์", "คำสรรพนาม", "คำสันธาน", "คำบุพบท", "คำอุทาน", "Particle", "วลี"]
                noun = []
                verb = []
                adj = []
                pron = []
                cconj = []
                adp = []
                intj = []
                part = []
                POSLists = [noun, verb, adj, pron, cconj, adp, intj, part]
                for (pos, defi) in definitions:
                    for I in range(len(POSs)):
                        if pos == POSs[I]:
                            POSLists[I].append(defi)
                            break
                for I in range(len(POSLists)):
                    if POSLists[I]:
                        POSLists[I] = list(set(POSLists[I]))
                        defList = []
                        for defi in POSLists[I]:
                            defList.append(defi)
                        definition.append((POSth[I], defList))

            else:
                definition.append('none')
            
            if not lanna:
                lanna = 'none'
            return [
                    output,
                    synonym,
                    definition,
                    lanna
                    ]

        if not matchState: #เป็นกลุ่มคำ                       
            for sentence in self.sentencelist:
                self.wordlist = word_tokenize(sentence)
                self.wordlistpos = pos_tag(self.wordlist, corpus='orchid_ud')
                #print(self.wordlistpos)
                #print(translator(input, self.direction).senttrans(self.wordlist))
                self.outputPerSentence = translator(input, self.direction, self.dictionary).senttrans(self.wordlistpos)
                self.outputtext = self.outputtext + self.outputPerSentence[0]
                self.haveOutputState = self.outputPerSentence[1]
            
            self.output = ''.join(self.outputtext)
            if self.output == self.inputtext:
                self.output = 'ไม่พบคำแปล'

        return [self.output]