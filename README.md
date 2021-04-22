# ProgettoWebSemantico

Prototipo di progetto web semantico, classificazione di testi e confronto su siti di rilevazione fake news.

**Input**: File con testo di fake news 

**Output**: eventuali errori grammaticali e prime 3 news più simili nei siti Butac e BufaleNet.

Tutto il codice è in _FileAnalysis.py_

## Procedura semplificata

- Rilevamento errori nel testo con **python_language_tool**
- Creazione bag of words dei testi
- Eliminazione stopwords
- Eliminazione parole con TF = 1
- Eliminazione delle ultime parole (cutoff = 30), solitamente parole meno importanti in un articolo
- Confronto dei bag of words, rilevamento similitudine con **spacy** (cosine similarity)

**Se la news è presente nei due siti, sicuramente comparirà tra le 3 news riportate.**

## Miglioramenti possibili
1. Non ho usato Stemming, Lemmatizzazione, POS tagging. Peggioravano gli indici di similarità, e il POS tagging in italiano è molto impreciso.
2. Il taglio delle parole con TF = 1 è stato fatto per ridurre le ridondanze nei testi, troppo lunghi altrimenti.
  Non è comunque preciso e le notizie troppo corte o con parole non ripetute vengono scartate
3. Python_language_tool è imperfetto, non coglie i neologismi o le sigle
4. Nel sito Butac ho preso gli articoli per intero. Sono presenti giudizi dell'autore, commenti, ironia fuorviante. Si potrebbe pensare di prendere solo la citazione 
(vera e propria fake news) dalla pagina, ma non tutte le notizie ce l'hanno.
