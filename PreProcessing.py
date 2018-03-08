import nltk
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# For sentiment analysis
from SentimentAnalyzer import sentiment_analysis
# For drawing bar chart
from Plot_Bar_Chart import Plot_Bar_Chart
# for lemmatize
from nltk.stem.wordnet import WordNetLemmatizer


def to_xml(key, value):
    return "<" + key + ">" + value + "</" + key + ">"


def make_xml_from_list(word_list) :
    tagger_words = "<words>\n"
    for token in word_list:
        if token[0] == '.':
            tagger_words += "\t" + to_xml('End', '.') + "\n"
        else :
            tagger_words += "\t" + to_xml(token[1], token[0]) + "\n"
    tagger_words += "</words>"

    return tagger_words


apostrophes = {"won't":"will not","can't":"cannot","couldn't":"could not","shouldn't":"should not","shan't":"shall not","'s":" is"}

wnl = nltk.WordNetLemmatizer()

file1 = open("Dataset/Nokia_6610.txt")

# Read file content as a stream
line = file1.read()

# Remove URL
result = re.sub(r"http://www\S+", "", line)

# Replace apostrophes with full form
for k, v in apostrophes.items():
    result = result.replace(k, v)

# Filter everything except letters and '.'
result = re.sub('[^A-Za-z.]+', ' ', result)

result = result.replace("<3", "love")
result = result.replace("image", "picture")
result = result.replace("range", "zoom")

cachedStopWords = set(stopwords.words("english"))

# Add custom words into stopwords list
cachedStopWords.update(('and','I','A','And','This','it','It','These','these','The','the','But','but','Or','or','You','you','My','my','Its'))

# Remove stopwords
result = ' '.join([word for word in result.split() if word not in cachedStopWords])

input_sentences = result.split('.')

words = result.split()

Lem = WordNetLemmatizer()

streaming_words = ""
for r in words:
    r = Lem.lemmatize(r)
    streaming_words += " " + r


# If we want to save data and want to see it
appendFile = open('filteredtext.txt','a')
appendFile.write(" "+ streaming_words)
appendFile=open("filteredtext.txt","r").close()


# Generate list of tokens
tokens = word_tokenize(streaming_words)
tokens_pos = nltk.pos_tag(tokens)


# POS tagging
xml_string_pos = make_xml_from_list(tokens_pos)


# If we want to save tagged data and want to see it
xml_string_file = open('pos.xml', 'w')
xml_string_file.write(xml_string_pos)
xml_string_file.close()


# Count frequent Nouns
s = []

for token in tokens_pos:
    if token[1] == "NN" or token[1] == "NNS" or token[1] == "NNP":
        s.append(token[0])

print(s)

d = {}

for w in s:
    if w in d:
        d[w] += 1
    else:
        d[w] = 1


lst = [(d[w],w) for w in d]
lst.sort()
lst.reverse()


print('\n The 10 most frequent nouns are /n')

i = 1
for count, word in lst[:10]:
    print('%2s. %4s %s' %(i, count, word))
    i += 1


#Get Features

#For camera
#notable_features = ["body", "weight", "battery", "image","viewfinder","color", "zoom", "range","use","picture", "sensor", "video", "usb", "design", "performance", "price", "resolution", "lens"]

#For mobile
notable_features = ["network", "display", "sound", "body","screen", "weight", "battery", "image", "camera", "use","picture", "ram", "sensor", "video", "usb", "design", "performance", "price", "touch", "resolution" ]

frequent_features = []

for token in tokens_pos:
    if token[1] == "NN" or token[1] == "NNS" or token[1] == "NNP":
        if token[0] in notable_features:
            frequent_features.append(token[0])


print(frequent_features)

feature_counts = {}

for f_feature in frequent_features:
    if f_feature in feature_counts:
        feature_counts[f_feature] += 1
    else:
        feature_counts[f_feature] = 1


print(feature_counts)

lst1 = [(feature_counts[wd], wd) for wd in feature_counts]
lst1.sort()
lst1.reverse()


def word_in_sentence(word, sentence):
    if word in sentence.split():
        return True
    return False


i = 1

related_sentence = {}

print('\n The 5 most mentioned features are :')

for count, word in lst1[:10]:
    sentence_list = [];

    for sentence in input_sentences:
        if word_in_sentence(word, sentence):
            sentence_list.append(sentence)
    related_sentence[word] = sentence_list

    print('%2s. %4s %s' %(i, count, word))
    i += 1


def get_doc_from_list(list):
    return ".".join(list)


x = []
y = []

def calculate_sentiment_result():
    sentiment_score = {}
    total_score = 0.0

    for feature, sentence in related_sentence.items():
        sentiment_result = sentiment_analysis(get_doc_from_list(sentence))
        sentiment_score[feature] = sentiment_result
        print(feature, "   >>>  ", sentiment_result,"\n")
        total_score += sentiment_result

    s = []

    for feature, score in sentiment_score.items():
        score = score/total_score
        s.append(score)
        s.sort()
        sf = s[0] - 0.01
        sl = s[-1] + 0.01
        score = (9.0 / (sl - sf) * (score - sf)) + 1.0
        print(feature, " ------ ", (round(score, 1)), "/10")
        x.append(feature)
        y.append(score)


# Sentiment analysis
calculate_sentiment_result()


#Plot bar graph
Plot_Bar_Chart(x,y)
