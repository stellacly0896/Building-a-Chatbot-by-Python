import re

def get_href():
    html = open( "sina.html", "r", encoding = "utf-8" ).read()
    result = []
    # TODO
    """
    Do NOT use other libraries (e.g. Beautiful soup)
    Only use regular expression!
    
    find all the hyperlink address in the html file.
    The output should be stored in the variable "result".
    e.g. 
    result = [
    'http://www.sina.com.cn/favicon.svg', 'http://i3.sinaimg.cn/home/2013/0331/U586P30DT20130331093840.png', 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js', 
    ...
    ]
    """
    
    links = re.findall('http[s]?://[a-zA-Z0-9-+&@#/%?=~_!:,.;]+[a-zA-Z0-9-+&@#/%=~_]', html)
    result.append(links)
    return result

print(get_href())