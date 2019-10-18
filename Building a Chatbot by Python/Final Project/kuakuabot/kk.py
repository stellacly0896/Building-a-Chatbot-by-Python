#author:Linyi Chen

from chatterbot.logic import LogicAdapter
from chatterbot.trainers import ChatterBotCorpusTrainer
import chatterbot
import json
from random import shuffle
import re

#create a corpus to train the bot
dialog = []
answerset = set()#so that we don't have repeated questions or answers
regex = re.compile("[^\u4e00-\u9fa5^。^，^！^a-zA-Z0-9]") #omit emojis in the text
with open ('douban_kuakua_qa.txt','r',encoding = 'utf-8') as f1:
    q = None
    a = None
    count = 0
    for line in f1.readlines():
        if "Q:\t" in line:
            q = line.strip().split('\t')[-1] # to get the utterance that we need
            q = q.replace("<br/>","")
            q = regex.sub("",q)
            
        elif "A:\t" in line:
            a = line.strip().split('\t')[-1]
            a = a.replace("<br/>","")
            a = regex.sub("",a)
            answerset.add(a)
            count += 1
            
            if len(q) > 5 and a is not None and count <= 2000: # to omit questions that are meaningless or have no answers
                dialog.append([q,a])

corpus = {"conversations":dialog}
json.dump(corpus, open('kuakua_corpus.json','w',encoding="utf-8"), ensure_ascii=False)


#%%
 
class kkLogicAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.items = {'学习':['学习','考试','成绩','学业','奖学金','名次'],
                      '工作':['工作', '老板', '业绩','上班','职场'],
                      '分手':['前男友','前女友','失恋','前任','现任'],
                      '丧': ['开心','加油','笑','祝福','快乐','优秀'],
                      '难过': ['开心','加油','笑','祝福','快乐','优秀'],
                      '抑郁': ['开心','加油','笑','祝福','快乐','优秀']
                      }

    
    def can_process(self,statement):   # can only process sentences that contain 求表扬，求夸，求安慰，求鼓励     
        return statement.text.find("求") >= 0 
    
    
    def get_kk(self, statement):
        choices = self.items[statement.text] 
        answerlist = list(answerset)
        shuffle(answerlist)
        for answer in answerlist:
            for choice in choices:
                if answer.find(choice) >=0:
                    statement.text = answer
                    return statement
    
    
    def process(self, input_statement, additional_response_selection_parameters=None):
        rst_statement = input_statement
        for key in self.items.keys():
            if input_statement.text.find(key) >=0 :
                input_statement.text = key
                rst_statement = self.get_kk(input_statement)
                rst_statement.confidence = 1
                break
            else:
                rst_statement = self.get_default_response(input_statement)
        
        return rst_statement

#%%     
if __name__ == "__main__":
    print("I am running")

    
    bot = chatterbot.ChatBot("My ChatterBot",
                            logic_adapters=[
                                {
                                    "import_path": "kk.kkLogicAdapter",
                                    'default_response': '你真的好棒！'
                                }
                                ]
                             )    
    #bot.set_trainer( chatterbot.trainers.ChatterBotCorpusTrainer )
    trainer = ChatterBotCorpusTrainer(bot)
    
    trainer.train('./kuakua_corpus.json')
    
    #print(bot.get_response("学习了十个小时求夸奖！"))
    #print( bot.get_response("要去打球赛了求夸") )
    print("你来了我好开心呀！怎么啦？")
    
    while True:
        try:
            user_input = input('USER:')
            if user_input == "再见":
                print("要一直保持积极的心态哟！再见！")
                break
            response = bot.get_response(user_input)
            print("BOT:",response)
        except (KeyboardInterrupt, EOFError,SystemExit):
           break