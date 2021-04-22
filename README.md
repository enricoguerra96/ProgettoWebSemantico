# ProgettoWebSemantico

Prototipo di progetto web semantico, classificazione di testi e confronto su siti di rilevazione fake news.

**Input**: File con testo di fake news 

**Output**: eventuali errori grammaticali e prime 3 news più simili nei siti Butac e BufaleNet.

Tutto il codice è in _FileAnalysis.py_

## Procedura semplificata

- Rilevamento errori nel testo in input con **python_language_tool**
- Creazione bag of words dei testi, sia di input che dai siti Butac e Bufale.net
- Eliminazione stopwords
- Eliminazione parole con TF = 1
- Eliminazione delle ultime parole (cutoff = 30), solitamente parole meno importanti in un articolo
- Confronto dei bag of words testo in input-news del sito, rilevamento similitudine con **spacy** (cosine similarity)

**Se la news è presente nei due siti, probabilmente comparirà tra le 3 news riportate.**

## Spiegazione dettagliata metodi difficili

1. _bufale_scrap_download(url, index)_ : 
  Obiettivo: avere i BoW di tutte le news del sito già scaricate.
  - Questo metodo inizia con il download con la libreria **urllib** delle pagine indice di Bufale.net nella cartella Indici.
  - Con **BeautifulSoup** si selezionano i link ad ogni pagina (_hrefs_), salvandoli in una lista _in_hrefs_. Vengono salvati anche il corrispettivo titolo e il testo della pagina linkata salvandoli nella lista _in_links_. _in_links_ costituirà la lista dei BoW da confrontare con la news in input, _in_hrefs_ la lista dei link da riportare nel risultato.
  - I BoW dei testi in _in_links_ verranno salvati in files di testo nella cartella Pagine, ogni file avrà il nome del corrispondente _in_href_ appositamente modificato.
 
 2. _butac_scrap_download(url, index)_
  Obiettivo: avere i BoW di tutte le news del sito già scaricate.
  Il metodo segue la stessa logica del precedente. La complessità di Butac ha reso necessaria l'aggiunta della lista _whocares_hrefs_ per l'eliminazione di link inutili presenti in tutte le pagine di indicizzazione.
 
 3. _news_control(news, site)_
 Obiettivo: Calcolare l'indice di similarità di ogni file presente in Pagine con il testo fornito in input.
 - Viene prima creato il BoW del testo fornito in input
 - Per ogni file l'indice di similarità viene calcolato e salvato in _simil_records_, insieme al nome del file salvato in _simil_texts_.
 - Vengono poi mostrati i primi 3 files con indici di similarità maggiori sia per Butac che per Bufale.net. La similarità è approssimata alla seconda cifra decimale.


## Miglioramenti possibili
1. Non ho usato Stemming, Lemmatizzazione, POS tagging. Peggioravano gli indici di similarità, e il POS tagging in italiano è molto impreciso.
2. Il taglio delle parole con TF = 1 è stato fatto per ridurre le ridondanze nei testi, troppo lunghi altrimenti.
  Non è comunque preciso e le notizie troppo corte o con parole non ripetute vengono scartate
3. Python_language_tool è imperfetto, non coglie i neologismi o le sigle
4. La libreria nlp restituisce un errore se vengono inseriti SOLO input anomali(lettere casuali senza senso) dall'utente.
5. Nel sito Butac ho preso gli articoli per intero. Sono presenti giudizi dell'autore, commenti, ironia fuorviante. Si potrebbe pensare di prendere solo la citazione 
(vera e propria fake news) dalla pagina, ma non tutte le notizie ce l'hanno.
