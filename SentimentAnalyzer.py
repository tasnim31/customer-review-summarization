import nltk
from nltk.corpus import sentiwordnet as swn


def sentiment_analysis(doc):
    sentences = nltk.sent_tokenize(doc)
    stokens = [nltk.word_tokenize(sent) for sent in sentences]
    taggedlist = []
    for stoken in stokens:
        taggedlist.append(nltk.pos_tag(stoken))

    print(taggedlist)

    wnl = nltk.WordNetLemmatizer()

    score_list = []

# The enumerate() function adds a counter to an iterable.
    for idx1, taggedsent in enumerate(taggedlist):
        score_list.append([])
        for idx2, t in enumerate(taggedsent):
            lemmatized = wnl.lemmatize(t[0])

            if t[1].startswith('NN'):
                newtag = 'n'
            elif t[1].startswith('JJ'):
                newtag = 'a'
            elif t[1].startswith('V'):
                newtag = 'v'
            elif t[1].startswith('R'):
                newtag = 'r'
            else:
                newtag = ''
            if (newtag != ''):
                synsets = list(swn.senti_synsets(lemmatized, newtag))

                # Getting average of all possible sentiments
                score = 0.0
                if (len(synsets) > 0):
                    for syn in synsets:
                        p = syn.pos_score()
                        n = syn.neg_score()
                        score += p - n
                    score_list[idx1].append(score / len(synsets))

    #print(score_list)
    sentence_sentiment = []

    for score_sent in score_list:
        total = sum([word_score for word_score in score_sent]) / len(score_sent)
        sentence_sentiment.append(total)
    print("Sentiment for each sentence for:" + doc)
    print(sentence_sentiment)
    return sum(sentence_sentiment)/ len(sentence_sentiment)

