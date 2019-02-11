import nltk.data
from nltk.corpus import stopwords
import pandas as pd
import string
import pickle
import io

def doc2sent(file_name):
    '''
    changes a text document into a list of entences
    '''
    nltk.download('punkt')
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    # open and read the file
    ff = io.open(file_name, encoding="utf-8")
    txt = ff.read()
    text = '\n-----\n'.join(tokenizer.tokenize(txt))
    text = text.split('\n-----\n')
    return pd.DataFrame( data=text, columns=["quote"])


def preprocess(sentences):
    '''
    gets a Series containing sentences and preprocesses 
    them for NLP processes
    '''
    # Convert text to lowercase
    sentences = sentences.str.lower()
    
    # Remove numbers. Here numbers do not carry any importance to our analysis
    sentences = sentences.str.replace(r'\d+','')
    ## remove between square brackets and anything in between them
    sentences = sentences.str.replace(r'<[^>]+>', '')
    ## remove \n
    sentences = sentences.str.replace(r'\n', '')
    ## remove with less than 30 characters
    #df_train = df_train[df_train['quote'].str.len()>30]
    # removing stop words
    nltk.download("stopwords")
    stop = stopwords.words('english')
    pat = r'\b(?:{})\b'.format('|'.join(stop))
    sentences = sentences.str.replace(pat, '')
    sentences = sentences.str.replace(r'\s+', ' ')
    # remove punctuation
    sentences = sentences.str.replace(r'[^\w\s]','')
    sentences = sentences.to_frame('quote')
    return sentences
    

def model_1(corpus):
    '''
    corpus is a list containing preprocessed sentences.
    Using a pretrained Countvectorizer it creates a sparse
    matrix for the corpus
    '''
    filename = 'flaskexample/data/CountVec_1.pkl'
    cv = pickle.load(open(filename, 'rb'))
    X = cv.transform(corpus)
    
    # Now putting into the regression model to predict y
    model_file = 'flaskexample/data/model_1.pkl'
    logistreg = pickle.load(open(model_file, 'rb'))
    Y = logistreg.predict(X)

    # Now putting them in a dataframe
    result = pd.DataFrame({'point': Y, 'quote': corpus})
    return result