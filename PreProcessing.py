import io
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


def to_xml(key, value):
    return "<" + key + ">" + value + "</" + key + ">"


def make_xml_from_list(word_list) :
    tagger_words = "<words>\n"
    for token in word_list:
        tagger_words += "\t" + to_xml(token[0], token[1]) + "\n"
    tagger_words += "</words>"

    return tagger_words


#word_tokenize accepts a string as an input, not a file.
stop_words = set(stopwords.words('english'))
apostrophes = {"won't":"will not","can't":"cannot","couldn't":"could not","shouldn't":"should not","shan't":"shall not"}
ps = PorterStemmer()
file1 = open("text.txt")
line = file1.read()                    #Read file content as a stream

result = re.sub(r"http\S+", "", line)  #Remove URL

for k, v in apostrophes.items():       #Replace apostrophes
    result = result.replace(k, v)

result = result.replace("'", "")
result = result.replace(",", "")
result = result.replace(";", "")
result = result.replace(":", "")
result = result.replace("/", "")
result = result.replace("(", "")
result = result.replace(")", "")
result = result.replace("#", "")
result = result.replace("!", "")
result = result.replace(".", ". ")
result = result.replace("<3", "love")

words = result.split()

streaming_words = ""
for r in words:
    if not r in stop_words:             #stop word removal
        r = ps.stem(r)                    #stemming
        streaming_words += " " + r


# If we want to save data and want to see it
appendFile = open('filteredtext.txt','a')
appendFile.write(" "+ streaming_words)
appendFile.close()


# f = open("filteredtext.txt")
# data = str.readlines()

# for line in data:
tokens = word_tokenize(streaming_words)          #Generate list of tokens
tokens_pos = nltk.pos_tag(tokens)
xml_string_pos = make_xml_from_list(tokens_pos)

xml_string_file = open('pos.xml', 'w')
xml_string_file.write(xml_string_pos)
xml_string_file.close()

# f.close()