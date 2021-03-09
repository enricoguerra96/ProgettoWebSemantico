import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import language_tool_python
import csv
import urllib.request
from datetime import datetime
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import os
import ast
import spacy

nlp = spacy.load("it_core_news_lg")


def count_frequencies(input_text: list):
    # Create BoW
    frequency = {}
    for item in input_text:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1

    correct_frequency = {}

    # Eliminate less frequency words
    for key, value in frequency.items():
        if value > 1:
            correct_frequency[key] = value

    # Re-create string
    correct_str = ""
    for key, value in correct_frequency.items():
        for i in range(0, value):
            correct_str += str(key) + " "

    return correct_str


def is_correct(input_text: str, lang: str):
    try:
        tool = language_tool_python.LanguageTool(lang)
        matches = tool.check(input_text)

        if len(matches) == 0:
            return "Correct"
        else:
            result = ''
            result += str(len(matches)) + " possible errors found: "
        for m in matches:
            result += m.matchedText + " "
        return result

    except ValueError:
        return "Language not supported."


def stemming(input_words: list):
    snow_stemmer = SnowballStemmer(language='italian')
    stem_words = []
    for w in input_words:
        x = snow_stemmer.stem(w)
        stem_words.append(x)

    return stem_words


def lemmatize(input_words: list):
    lemmas = []
    for word in input_words:
        lemma = nlp(word)
        for tok in lemma:
            lemmas.append(tok.lemma_)
    return lemmas


def text_analysis(input_text: str):

    # Tokenization
    text_toked = word_tokenize(input_text)

    # Stopwords/punctuation elimination
    stop_words = set(stopwords.words('italian'))
    filtered_text = []

    punc = '''!()-[–]{};:'’"“”\, <>./?^&amp;*_~'''

    for tok in text_toked:
        if tok.lower() not in stop_words and tok.lower() not in punc and len(tok) != 1:
            with open("./BufaleNet/banned_words", 'r') as f:
                content = f.read()
                if tok not in content:
                    filtered_text.append(tok)
    return filtered_text


def count_words(input_text: str):
    strip_str = input_text.strip()
    count = 1
    for c in strip_str:
        if c == " ":
            count += 1
    return count


def bufale_scrap_download(url: str, index: str):
    # save as local HTML (Indici)
    time_obj = datetime.now()
    filename = "./BufaleNet/Indici/" + str(index) + "_" + str(time_obj) + ".html"
    urllib.request.urlretrieve(url, filename)

    # Scrap HTML files with BS
    with open(filename, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

    # Move links(titles) and texts to in_links
    in_links = []
    in_hrefs = []
    for element in soup.select('a'):
        href = element.get('href')
        if str(href) is not None and str(href) != '' and '-' in str(href):
            text = element.text
            if str(text) is not None and str(text) != '' and str(text).find('\n'):
                if count_words(str(text)) > 3:
                    page = requests.get(str(href))
                    text_soup = BeautifulSoup(page.text, "lxml")
                    for t in text_soup.find_all(class_="text-article"):
                        in_links.append(str(text + " " + t.text))
                        in_hrefs.append(str(href))

    # Divide all in files and save (Pagine)
    ind = 0
    for text in in_links:
        if ind != len(in_links):
            time_obj = datetime.now()
            new_href = in_hrefs[ind].replace('https://www.bufale.net/', '')[:-1]
            filename = "./BufaleNet/Pagine/" + new_href + ".txt"
            with open(filename, 'w') as w:
                w.write(str(count_frequencies(text_analysis(text))))
            ind += 1


def bufale_checkupdates():
    basic_url = "https://www.bufale.net/bufala/page/"
    bufale_scrap_download("https://www.bufale.net/bufala/", str(1))
    for i in range(4, 10):
        new_url = basic_url
        new_url += str(i)
        bufale_scrap_download(new_url, str(i))


def simil_spacy(input1: str, input2: str):
    main = nlp(input1)
    new = nlp(input2)
    return round(main.similarity(new), 2)


def news_control(news: str):
    input1_string = count_frequencies(text_analysis(news))
    directory = "./BufaleNet/Pagine/"
    simil_records = []
    simil_texts = []
    for filename in os.listdir(directory):
        with open(directory + filename, 'r') as f:
            input2 = f.read()
            simil_records.append(simil_spacy(input1_string, input2))
            simil_texts.append(str(filename))
    m = max(simil_records)
    print(simil_texts[simil_records.index(m)] + " : " + str(m))


# bufale_checkupdates()
news_control("Gli esperti infatti raccomandano non solo che il vaccino vaccino vaccino deve essere somministrato in ambienti che "
             "dispongono di scorte, inclusi ossigeno e adrenalina, proprio per gestire le reazioni reazioni anafilattiche, "
             "ma anche defibrillatore per una sorte di rianimazione immediata a seguito dell’inoculazione di queste "
             "“oscure sostanze” capaci di manipolare il DNA creando in futuro qualsiasi tipo di reazione avversa o "
             "patologia potenzialmente mortale mortale.")
