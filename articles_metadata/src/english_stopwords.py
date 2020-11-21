import nltk

def write_stopwords():
    nltk.download('stopwords')
    stopwords = set(nltk.corpus.stopwords.words('english'))

    with open('../data/english_stopwords.csv', 'w', encoding='utf-8') as f:
        f.write(str(stopwords))

write_stopwords()