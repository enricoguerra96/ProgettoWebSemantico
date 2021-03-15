import os
import urllib.request
from datetime import datetime

import language_tool_python
import requests
import spacy
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from translate import Translator

nlp = spacy.load("it_core_news_lg")


def text_translation(text: str):
    translator = Translator(to_lang="Italian")
    translation = translator.translate(text)
    return translation


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
        ok_words = ["Covid-19", "Covid", "COVID-19", "Coronavirus", "coronavirus", "SARS", "sars"]

        if len(matches) == 0:
            return print("Grammar: correct")
        else:
            print(str(len(matches)) + " possible error(s) found: ")
            for m in matches:
                if m not in ok_words:
                    print(m.matchedText + " : " + m.ruleId)
    except ValueError:
        return print("Language not supported.")


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
                    filtered_text.append(tok.lower())
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
            new_href = in_hrefs[ind].replace('https://www.bufale.net/', '')[:-1]
            filename = "./BufaleNet/Pagine/" + new_href + ".txt"
            with open(filename, 'w') as w:
                w.write(str(count_frequencies(text_analysis(text))))
            ind += 1


def butac_scrap_download(url: str, index: str):
    # save as local HTML (Indici)
    time_obj = datetime.now()
    filename = "./Butac/Indici/" + str(index) + "_" + str(time_obj) + ".html"
    urllib.request.urlretrieve(url, filename)

    # Scrap HTML files with BS
    with open(filename, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

    # Move links(titles) to in_links
    whocares_hrefs = ['https://www.butac.it/guida-2/', 'https://www.butac.it/fake-news/',
                      'https://www.butac.it/notizia-vera/',
                      'https://www.butac.it/speciale-coronavirus-covid-19/', 'https://www.butac.it/ambiente-e-animali/',
                      'https://www.butac.it/giornalismo-pseudogiornalismo/',
                      'https://www.butac.it/scienza-e-tecnologia/',
                      'https://www.butac.it/teorie-del-complotto/', 'https://www.butac.it/xenofobia-2/',
                      'https://www.butac.it/the-black-list/', 'https://www.butac.it/chi-siamo/',
                      'https://www.butac.it/parlano-di-noi/',
                      'https://www.butac.it/citazioni-e-leggende-urbane/']

    in_links = []
    in_hrefs = []
    in_hrefs_ok = []
    in_texts_href = []
    in_texts_href_ok = []
    for element in soup.find_all('a'):
        href = element.get('href')
        if str(href) is not None and str(href) != '' and str(href) not in whocares_hrefs \
                and 'https://www.butac.it/' in str(href) and '-' in str(href):
            text = element.text
            in_texts_href.append(text)
            in_hrefs.append(str(href))

    # Remove duplicate hrefs
    [in_hrefs_ok.append(x) for x in in_hrefs if x not in in_hrefs_ok]
    [in_texts_href_ok.append(x) for x in in_texts_href if x not in in_texts_href_ok]

    # Scrap texts from pages
    for ok_link in in_hrefs_ok:
        page = requests.get(ok_link)
        text_soup = BeautifulSoup(page.text, "lxml")
        temp = ""
        for t in text_soup.find_all(class_="textArticle"):
            temp += t.text
        in_links.append(temp)

    # Divide in files and save
    for ind in range(0, len(in_links)):
        new_href = in_hrefs[ind].replace('https://www.butac.it/', '')[:-1]
        filename = "./Butac/Pagine/" + new_href + ".txt"
        with open(filename, 'w') as w:
            w.write(str(count_frequencies(text_analysis(in_links[ind]))))


def butac_checkupdates():
    basic_url = "https://www.butac.it/bufala/page/"
    butac_scrap_download("https://www.butac.it/bufala", str(1))
    for i in range(2, 20):
        new_url = basic_url
        new_url += str(i)
        butac_scrap_download(new_url, str(i))


def bufale_checkupdates():
    basic_url = "https://www.bufale.net/bufala/page/"
    # bufale_scrap_download("https://www.bufale.net/bufala", str(1))
    for i in range(10, 20):
        new_url = basic_url
        new_url += str(i)
        bufale_scrap_download(new_url, str(i))


def simil_spacy(input1: str, input2: str):
    main = nlp(input1)
    new = nlp(input2)
    return round(main.similarity(new), 2)


def news_control(news: str, site: str):
    # Retrieve the maximum similarity index for each news in the directory
    try:
        input1_string = count_frequencies(text_analysis(news))
        directory = "./" + site + "/Pagine/"
        simil_records = []
        simil_texts = []
        for filename in os.listdir(directory):
            with open(directory + filename, 'r') as f:
                input2 = f.read()
                simil_records.append(simil_spacy(input1_string, input2))
                simil_texts.append(str(filename))

        for _ in range(0, 3):
            m = max(simil_records)
            if site == "BufaleNet":
                print("https://www.bufale.net/" + simil_texts[simil_records.index(m)][:-4] + " : " + str(m))
                simil_records.remove(m)
            else:
                print("https://www.butac.it/" + simil_texts[simil_records.index(m)][:-4] + " : " + str(m))
                simil_records.remove(m)

    except FileNotFoundError:
        print("No directory with this name.")
    except ValueError:
        print("Maybe there are no pages in this directory.")


def analyze_news():
    it_text = ""
    print("Insert text:\n")
    text = input()
    print("\n")
    is_correct(text, "it")
    print("\n Similarities:")
    news_control(text, "BufaleNet")
    news_control(text, "Butac")


#analyze_news()

bufale_checkupdates()

butac_checkupdates()


"""
news_control("Pillon Pillon Pillon atleti atleti atleti transessuali transessuali transessuali askdfbasdk", "BufaleNet")
"""
