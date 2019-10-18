from chatterbot.logic import LogicAdapter
import chatterbot

import re, json
from urllib import request

#%%
#
#url = "http://www.baidu.com"
#req = request.Request( url )
#html_content = request.urlopen( req ).read().decode("utf-8")
#
#print(html_content)
#
##%%
#url = "http://www.weather.com.cn/weather/101020100.shtml" 
#
## Note: in most case, you don't need hdr; unless the website has restriction
#hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#       'Accept-Encoding': 'none',
#       'Accept-Language': 'en-US,en;q=0.8',
#       'Connection': 'keep-alive'}
#
#
#req = request.Request( url , headers = hdr)
#
#weekly_weather = request.urlopen( req ).read().decode("utf-8")
#        
#
#seven_days = re.findall(r'\<h1\>([1-9].*)\</h1>\n.*\n.*\n.*\>(.*)\</p>\n.*\n\<span\>([0-9]*).*\>([0-9].*)\</i\>\n', weekly_weather)
#
##%% Get City ID
##f = open("dirty_weather_id.txt", "r", encoding = "utf-8")
#
#url = "http://my.oschina.net/cart/blog/189839"
#req = request.Request( url , headers = hdr)
#html = request.urlopen( req ).read().decode("utf-8")
## NOTE: you will ge error. forbidden
#
#city_ids = {}
#for line in html.split('\n'):
#    m = re.findall( 'name="(\w+)"\s+weatherCode="(\d+)"', line )
#    
#    if len(m) > 0:
#        print( m[0] )
#        city_ids[ m[0][0] ] = int( m[0][1]   )
#    
#
#json.dump(city_ids, open("city_id.json", "w", encoding="utf-8"), 
#          ensure_ascii=False, indent=4) 
## ensure_ascii = False is necessary!!!

#%%

class WeatherLogicAdapter(LogicAdapter):



    def __init__(self, **kwargs):
        super(WeatherLogicAdapter, self).__init__(**kwargs)
        
        self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

        try:
            self.cities = json.load( open("city_id.json", "r", encoding="utf-8")  )
        except Exception as e:
            print(e)
            print("unable to load city id")
            self.cities = {
                "上海" : 101020100,
                "北京" : 101010100,
                "深圳" : 101280601,
                "广州" : 101280101
            }    


        
    def can_process(self, statement):
#         statement.text 
        if statement.text.find("天气") >= 0:
            return True
        else:
            return False
        
        return statement.text.find("天气") >= 0

        
        

    def __get_weather( self, city_id ):
        """
        return a string that describes the weawther in following 7 days
        """
        
        url = "http://www.weather.com.cn/weather/%d.shtml" % city_id 
        
#        print( url )
        
        req = request.Request( url, headers=self.hdr)
        
        weekly_weather = request.urlopen( req ).read().decode("utf-8")
        
        seven_days = re.findall(r'\<h1\>([1-9].*)\</h1>\n.*\n.*\n.*\>(.*)\</p>\n.*\n\<span\>([0-9]*).*\>([0-9].*)\</i\>\n', weekly_weather)
        
        rst = ""
        
        for day in seven_days:
            rst += day[0] + day[1] + " " + day[3].replace("℃", "") + " - " + day[2] + "℃\n"
        
        return rst

    def process(self, statement):


        # For this example, we will just return the input as output
        rst_statement = statement
        
        
        
        # tokenize ["北京", "天气", "是", "多少"]
        city_name = statement.text.replace("天气", "")
        
        # city_name = '上海怎么样？'
        
        
        try:
            city_id = self.cities[ city_name ]
            rst_statement.text = self.__get_weather( city_id )
        except Exception as e:
            print( e )
            rst_statement.text = "我知道你在问我天气，但我就是不告诉你啊"

            # adsfasdf
        rst_statement.confidence = 1.0

        return rst_statement


# %%

if __name__ == "__main__":
    print("I am running")
    
    bot = chatterbot.ChatBot( "Naive", 
                             logic_adapters = [
                                     { 'import_path' : 'WeatherAdapter.WeatherLogicAdapter'  }
                                     
                                     ]
                             )    
    bot.set_trainer( chatterbot.trainers.ChatterBotCorpusTrainer )
    bot.train('chatterbot.corpus.chinese.greetings')
    
#    print( bot.get_response('你好') )

    print( bot.get_response('上海天气') )
    
    print( bot.get_response('上海天气怎么样？') )
    
