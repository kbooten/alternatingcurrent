
import sklearn
import numpy as np
from bs4 import BeautifulSoup as soup
import html
import string
import unidecode

## classification stuff
from nltk import classify,tokenize,ngrams,FreqDist
from sklearn.svm import LinearSVC ### could also try SVC but very slow
from sklearn.linear_model import LogisticRegression
from nltk import SklearnClassifier


## loading
import pickle,json

with open('maxent_model_pos_vs_neg.pkl','rb') as f:
    model = pickle.load(f)

with open('top_words.json','r') as f:
    top_words = json.load(f)


ok_chars= string.ascii_letters + "?.!,' "


class ACevaluator:


    def clean_text(self,astring):
        text = soup(astring,'html5lib').text
        text = html.unescape(text)
        text = unidecode.unidecode(text)
        
        ## remove weird characters
        for i in range(len(text)):
            if text[i] not in ok_chars:
                text = text.replace(text[i]," ")
        text = text.strip(' ')
        text = text.replace("  "," ") ## should use regex but probably doesn't matter
                
        return text


    def word_feats(self,words):
        words = [w.lower() for w in tokenize.word_tokenize(words)]
        words_pop = [w for w in words if w in top_words]
        for i in range(len(words)):
            if words[i] not in words_pop:
                words[i]="<UNK>"
        words = ["<BEG>"]+ words + ["<END>"]
        bigrams = [str(i) for i in ngrams(words,2)]
        trigrams = [str(i) for i in ngrams(words,3)]
        allfeatures = words_pop+bigrams+trigrams
        allfeatures = words_pop+bigrams
        return dict([(word, True) for word in allfeatures])


    def predict_sentence_affect(self,asentence):
        features = word_feats(asentence)
        prediction = model.prob_classify(features)
        return prediction.prob('pos')


    def sentiment_analysis(self,asentence):
        features = self.word_feats(self.clean_text(asentence))
        prediction = model.prob_classify(features).prob('pos')
        return prediction-.5


    def score(self,sent_sentiment_tuples):
        score = 0
        pairs = list(ngrams(sent_sentiment_tuples,2))
        for x,y in pairs:
            difference = max(x - y, y - x) #https://stackoverflow.com/a/40075059
            score+=difference
        return score
            

    def evaluate(self,poem):
        sents = tokenize.sent_tokenize(poem)
        sent_sentiment_tuples = [(s,self.sentiment_analysis(s)) for s in sents]
        score = self.score([affect for sentence,affect in sent_sentiment_tuples])
        yvals = [self.sentiment_analysis(s) for s in sents]
        return {"yvals":yvals,"sents":sents,"score":score}



if __name__ == "__main__":
    t = ACevaluator()
    print(t.evaluate("You can run through the valley. You are true of life.  I have wasted my life."))
