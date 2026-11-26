# Builds Code_Explanation_Ankit_Kumar_500120442.html from the notebook's code cells.
# Every non-empty code line gets one explanation, in order. Print to PDF with headless Chrome afterwards.
import html
import nbformat

CELLS = [
("Install the libraries", [
 "Installs the four libraries the project needs. <code>%pip</code> is a notebook command that runs pip inside the notebook, and <code>-q</code> (quiet) hides the long install log. On a machine that already has them, nothing happens.",
]),
("Import the tools and download NLTK data", [
 "<code>re</code> is Python's regular expression module. I use it to clean text with patterns, e.g. \"remove anything that looks like &lt;...&gt;\".",
 "<code>Counter</code> counts things for me. <code>Counter(['ear','sound','ear'])</code> gives <code>{'ear': 2, 'sound': 1}</code>. I use it to find the most frequent nouns.",
 "pandas holds the reviews as a table (a DataFrame), like an Excel sheet in Python. <code>pd</code> is the usual short name.",
 "matplotlib draws charts; <code>pyplot</code> is its simple drawing interface, called <code>plt</code>.",
 "NLTK (Natural Language Toolkit) does the language work: splitting into sentences and words, and POS tagging.",
 "Loads NLTK's list of English stopwords: very common words like \"the\", \"is\", \"and\" that carry no meaning on their own.",
 "The WordNet lemmatizer turns a word into its dictionary form: \"batteries\" → \"battery\", \"ears\" → \"ear\".",
 "TfidfVectorizer converts text into numbers (TF-IDF scores), because a machine learning model can only work with numbers.",
 "Logistic Regression is the machine learning model that decides positive or negative.",
 "<code>train_test_split</code> splits the data into a training part and a testing part.",
 "Two ways to measure the model: <code>accuracy_score</code> (percent correct) and <code>classification_report</code> (precision, recall and F1 for each class).",
 "A loop over the names of the NLTK data packages I need: <code>punkt</code> for sentence splitting, <code>stopwords</code>, <code>wordnet</code> for the lemmatizer ...",
 "... and the POS tagger model. Two names are listed for some packages because newer NLTK versions renamed them (<code>punkt_tab</code>, <code>..._eng</code>); downloading both makes the code work on old and new NLTK.",
 "Downloads each package once. <code>quiet=True</code> stops it printing a message for every package.",
]),
("Step 1: Load the reviews", [
 "Reads the CSV file into a DataFrame called <code>df</code>. Each row is one review with columns review_id, product_id, rating, title and review.",
 "<code>len(df)</code> is the number of rows, so this prints how many reviews I have (6,658).",
 "<code>nunique()</code> counts different values in a column. Here: how many different products (4,397).",
 "Shows the first 5 rows of three columns so I can see what the data looks like.",
]),
("Step 1: Rating distribution chart", [
 "<code>value_counts()</code> counts how many reviews have each star rating; <code>sort_index()</code> puts them in order 1, 2, 3, 4, 5.",
 "Prints those counts (e.g. 5 stars: 3,774).",
 "pandas can draw a chart directly from the counts. <code>kind=\"bar\"</code> makes a bar chart; I give a colour and a title.",
 "Label for the x axis (bottom).",
 "Label for the y axis (side).",
 "Saves the chart as a PNG image into the outputs folder. <code>dpi=150</code> makes it sharp, <code>bbox_inches=\"tight\"</code> cuts away empty borders.",
 "Shows the chart in the notebook.",
]),
("Step 2: Clean the text", [
 "Defines my own function <code>clean_text</code> that takes one review and returns the cleaned version.",
 "<code>re.sub(pattern, replacement, text)</code> replaces every match of the pattern. <code>&lt;.*?&gt;</code> means \"a &lt;, then anything, then the nearest &gt;\", so HTML tags like <code>&lt;br /&gt;</code> become a space. <code>str(text)</code> makes sure the input is text even if a cell is empty.",
 "<code>[^...]</code> means \"any character NOT in this list\". The list is letters, digits and <code>. , ! ? '</code> and space. So emojis and symbols like # or * are replaced by a space. I keep full stops because sentence splitting needs them.",
 "<code>\\s+</code> means \"one or more spaces/tabs/newlines\". They are replaced by a single space, so \"good&nbsp;&nbsp;&nbsp;&nbsp;sound\" becomes \"good sound\".",
 "<code>strip()</code> removes spaces at the start and end, then the function gives back the clean text.",
 "<code>apply</code> runs <code>clean_text</code> on every review and stores the results in a new column called <code>clean</code>.",
 "A quick test on a made-up review to show the cleaning works. Output: <code>Great sound! Love it</code>.",
]),
("Step 3: Train the sentiment model", [
 "Keeps only reviews whose rating is NOT 3 (<code>!=</code> means \"not equal\"). 3-star reviews are mixed, so they would confuse the model. <code>.copy()</code> makes a separate table so I can add a column safely.",
 "Creates the label: <code>rating &gt;= 4</code> gives True/False, and <code>astype(int)</code> turns it into 1/0. So 4-5 stars = 1 (positive), 1-2 stars = 0 (negative).",
 "Splits the data into four parts: training texts, testing texts, training labels, testing labels ...",
 "... using the clean text as input and the label as answer. <code>test_size=0.2</code> keeps 20% for testing. <code>random_state=42</code> makes the split the same every time I run it. <code>stratify</code> keeps the same positive/negative ratio in both parts.",
 "Creates the TF-IDF converter. <code>lowercase=True</code>: \"Great\" and \"great\" are the same word. <code>ngram_range=(1, 2)</code>: use single words and pairs of words, so \"not good\" is one feature. <code>min_df=2</code>: ignore words that appear in only one review (mostly typos). I do NOT remove stopwords, because \"not\" and \"no\" change the meaning.",
 "<code>fit_transform</code> does two things on the training reviews: learns the vocabulary and IDF values (fit), then turns each review into a row of numbers (transform).",
 "For the test reviews I only <code>transform</code>, using the vocabulary learned from training. The test data must stay unseen, otherwise the accuracy would be cheating.",
 "Creates the model. <code>max_iter=1000</code> gives it enough steps to finish learning. <code>class_weight=\"balanced\"</code> gives more importance to the negative reviews because there are far fewer of them.",
 "<code>fit</code> is the actual training: the model learns one weight for every word/word pair.",
 "The trained model predicts 0 or 1 for every test review.",
 "Compares predictions with the true labels and prints the accuracy rounded to 3 decimals (0.916 = 91.6% correct).",
 "Prints precision, recall and F1 for each class. <code>target_names</code> just gives readable names to 0 and 1.",
]),
("Step 3: Which words did the model learn?", [
 "Gets the list of all words and word pairs the TF-IDF vectorizer knows, in the same order as the model's weights.",
 "<code>model.coef_[0]</code> is the list of learned weights. <code>argsort()</code> gives the positions sorted from smallest weight (most negative) to largest (most positive).",
 "The first 12 positions are the strongest negative words, e.g. \"not\", \"disappointed\", \"poor\".",
 "The last 12 positions (<code>[-12:]</code>) are the strongest positive words, e.g. \"great\", \"love\", \"easy\".",
]),
("Step 3: Test the model on my own sentences", [
 "A Python list of test sentences I wrote myself. The list continues over the next lines.",
 "Second sentence (should be negative).",
 "Third sentence: tests if the model understands \"not comfortable\".",
 "Fourth sentence, and the closing <code>]</code> ends the list.",
 "<code>predict_proba</code> returns two numbers per sentence: chance of negative and chance of positive. <code>[:, 1]</code> keeps only the chance of positive. <code>zip</code> pairs every sentence with its number so I can loop over both together.",
 "Prints the chance with 2 decimals, then the sentence. <code>f\"...\"</code> is an f-string: values inside <code>{}</code> are filled in.",
]),
("Step 4: Split into sentences and score each one", [
 "Defines a function that takes a table of reviews and returns a table of scored sentences. Making it a function lets me reuse it for one product or for my own reviews later.",
 "An empty list; I will add one small dictionary per sentence to it.",
 "Loops over every review, taking its id and its clean text together.",
 "<code>nltk.sent_tokenize</code> splits a review into sentences. It is smarter than splitting on \".\" because it knows \"Mr.\" or \"3.5\" are not sentence ends.",
 "<code>sentence.split()</code> gives the words; I only keep sentences with 4 or more words, so pieces like \"Wow.\" are skipped.",
 "Saves the sentence and which review it came from.",
 "Turns the list of dictionaries into a DataFrame (one row per sentence).",
 "Converts all sentences with the same TF-IDF vectorizer and asks the model for the chance of positive. Stored in column <code>pos_prob</code>.",
 "First marks every sentence as neutral ...",
 "... then <code>.loc[condition, column]</code> changes it to positive where the chance is 0.65 or more ...",
 "... and to negative where the chance is 0.35 or less. Everything in between stays neutral.",
 "Returns the finished sentence table.",
 "Runs the function on all 6,658 reviews.",
 "Prints the number of sentences (39,961).",
 "Prints how many are positive, negative and neutral.",
 "Shows the first 5 rows of the sentence table.",
]),
("Step 5: Find the features with POS tagging", [
 "Makes a set of English stopwords. A set is used because checking \"is this word in the set?\" is very fast.",
 "Creates the lemmatizer object once, so I can reuse it.",
 "My hand-made list of nouns that are common but are not product features: the product itself (headphone, earbuds) ...",
 "... general words like set, thing, time, way, year ...",
 "... words like review, month, people, star ...",
 "... people (son, wife) and words like problem/issue, which show a feeling but not which feature ...",
 "... other devices (iphone, computer) and words like music or life ...",
 "... shopping words like purchase, order, item ...",
 "... and the last few. The <code>}</code> closes the set. If I made this project for phones I would need a new list.",
 "Defines a function that returns the feature nouns in one sentence.",
 "First <code>lower()</code> the sentence, <code>word_tokenize</code> splits it into words, and <code>pos_tag</code> gives every word a part-of-speech tag, e.g. <code>('battery', 'NN')</code>.",
 "An empty set for the nouns. A set keeps each noun only once per sentence.",
 "Loops over every (word, tag) pair.",
 "Keeps the word only if: the tag starts with NN (noun: NN, NNS, NNP), it is only letters, it is longer than 2 letters, and it is not a stopword.",
 "Adds the lemma (dictionary form) of the noun, so \"batteries\" is saved as \"battery\".",
 "Returns the nouns minus (<code>-</code>) the not_features set, so \"headphone\" or \"time\" are removed.",
 "Runs <code>get_nouns</code> on every sentence and stores the result in a new column <code>nouns</code>.",
 "Shows the raw POS tags for one example sentence, so I can see what the tagger does: battery and sound get NN.",
 "Shows the result of my function on an example: <code>{'battery', 'sound'}</code>. \"batteries\" was turned into \"battery\".",
]),
("Step 6: Link each feature to its opinions", [
 "Defines a function that builds the feature table. <code>top_k=12</code> means \"use the 12 most common features\" unless I say otherwise.",
 "Counts in how many sentences each noun appears. The double loop goes over every sentence and every noun inside it.",
 "An empty list for the table rows.",
 "<code>most_common(top_k)</code> gives the top 12 nouns with their counts. These are the frequently discussed features.",
 "Selects all sentences whose noun set contains this feature. <code>apply(lambda ...)</code> runs a tiny function on every row; <code>lambda nouns: feature in nouns</code> returns True or False.",
 "Counts the positive sentences about this feature. <code>(... == \"positive\")</code> gives True/False, and <code>sum()</code> counts the Trues.",
 "Same for negative sentences.",
 "Adds one row with the feature name, mentions, positive and negative counts ...",
 "... and <code>positive_%</code> = positive / (positive + negative) × 100. <code>max(..., 1)</code> avoids dividing by zero when a feature has no opinions.",
 "Turns the rows into a DataFrame and uses the feature name as the row label.",
 "Runs the function on all the sentences.",
 "Displays the table in the notebook.",
]),
("Step 6: Chart of features", [
 "Takes only the positive and negative columns, sorts them so the biggest bar is at the top, and starts a chart ...",
 "... <code>barh</code> = horizontal bars, <code>stacked=True</code> puts negative on the end of positive, green and red colours, size 8 × 5 inches ...",
 "... and the chart title. The <code>)</code> closes the plot call.",
 "Label for the x axis.",
 "Saves the chart into the outputs folder.",
 "Shows it in the notebook.",
]),
("Step 7: Pick sentences and write the summary", [
 "Defines a function that picks one example sentence for each feature in a list.",
 "An empty list for the chosen sentences.",
 "Loops over the features one by one.",
 "Keeps only sentences that have the wanted sentiment (positive or negative) ...",
 "... AND (<code>&amp;</code>) mention this feature ...",
 "... AND have between 6 and 25 words, so the example is easy to read ...",
 "... AND were not already picked (<code>~</code> means NOT), so the summary never repeats a sentence.",
 "Only continues if at least one sentence is left.",
 "Sorts by <code>pos_prob</code>. For positive I want the highest chance first; for negative the lowest first. <code>ascending=(sentiment == \"negative\")</code> is True only for negative, which gives exactly that.",
 "Takes the first sentence after sorting (<code>iloc[0]</code>), which is the one the model is most sure about.",
 "Returns the list of chosen sentences.",
 "Defines the main function that puts everything together. It works on any table of reviews.",
 "Step 4 again: split the given reviews into sentences and score them.",
 "Step 5: find the nouns in each sentence.",
 "Step 6: build the feature table.",
 "Sorts the features from most liked to least liked (by <code>positive_%</code>) and keeps just the names. <code>kind=\"stable\"</code> keeps ties in their original order, so the result is the same every run.",
 "How many features go in each list: at most 4, and at most half of the features, so a feature can never be both liked and disliked.",
 "Liked features = the first <code>n</code> of the sorted list (highest positive_%).",
 "Disliked features = the last <code>n</code> (<code>[::-1]</code> reverses the list), but only if they really have at least one negative sentence.",
 "Prints how many reviews and sentences were used.",
 "Prints all the frequently discussed features, joined with commas.",
 "Prints the one-line overall summary built from a fixed sentence template, e.g. \"customers are happiest with the price, case ...\" <code>\\n</code> means a new line.",
 "... second part of the same sentence with the disliked features.",
 "Heading for the positive part.",
 "Gets the best positive sentence for each liked feature ...",
 "... and prints each one with a + in front.",
 "Heading for the negative part.",
 "Gets the best negative sentence for each disliked feature ...",
 "... and prints each with a - in front.",
 "Returns the feature table so it can also be shown as a table.",
]),
("Step 7: Summary of all reviews", [
 "Runs the whole pipeline on all 6,658 reviews and prints the summary.",
]),
("Step 7: Summary of one product", [
 "<code>value_counts()</code> sorts products by number of reviews; <code>index[0]</code> is the product with the most reviews.",
 "Keeps only the reviews of that product (101 reviews).",
 "Runs the same summarize function on them, with the top 8 features because there is less data.",
 "Shows that product's feature table.",
]),
("Step 7: Summary of my own reviews", [
 "A list of five short reviews I typed myself to test the system ...",
 "... second review ...",
 "... third review ...",
 "... fourth review ...",
 "... fifth review, and <code>]</code> closes the list.",
 "Puts them in a DataFrame with a <code>review_id</code> (0 to 4) and a <code>review</code> column, the same shape as the real data.",
 "Cleans them with the same <code>clean_text</code> function.",
 "Summarizes them with the top 6 features.",
 "Shows their feature table.",
]),
]

TERMS = [
("NLP", "Natural Language Processing: making computers work with human language, e.g. splitting text, tagging words, finding opinions."),
("Opinion summarization", "Reading many reviews and giving a short summary of what people like, dislike and talk about."),
("Tokenization", "Cutting text into pieces. Sentence tokenization gives sentences, word tokenization gives words."),
("Stopwords", "Very common words (the, is, and). I remove them when looking for features, but NOT when training the model, because \"not\" is a stopword and it flips meaning."),
("POS tagging", "Part-of-speech tagging: labelling each word as noun (NN), verb (VB), adjective (JJ) and so on. I use it to find nouns, because features are nouns."),
("Lemmatization", "Turning a word into its dictionary form: batteries → battery. Different from stemming, which just chops endings (batteries → batteri)."),
("TF-IDF", "Term Frequency × Inverse Document Frequency. A word gets a high score if it appears often in this review (TF) but rarely in other reviews (IDF). \"the\" is everywhere, so it gets a low score; \"crackling\" is rare, so it gets a high score."),
("N-grams", "Groups of N words in a row. 1-gram: \"good\"; 2-gram (bigram): \"not good\"."),
("Logistic Regression", "A simple classification model. It adds up word weights and squeezes the total into a number between 0 and 1 (the chance of positive) using the sigmoid function."),
("Train/test split", "Training data teaches the model; test data checks it on reviews it has never seen, like a surprise exam."),
("Accuracy", "Correct predictions ÷ all predictions. Mine is 91.6%."),
("Precision", "Of the reviews the model CALLED negative, how many really were negative (0.72)."),
("Recall", "Of the reviews that really ARE negative, how many the model found (0.70)."),
("F1 score", "One number that balances precision and recall (their harmonic mean)."),
("Class imbalance", "One class has far more examples (here 5,107 positive vs 872 negative). class_weight=\"balanced\" fixes this a bit."),
("Extractive summary", "A summary made by picking real sentences from the text. The other type, abstractive, writes new sentences (like ChatGPT)."),
("Aspect / feature", "The part of the product an opinion is about: sound, battery, price."),
]

QA = [
("Why did you use machine learning and not just a list of good and bad words?",
 "A word list (like VADER) cannot learn headphone language. My model learned from 6,000 real reviews that words like \"returned\" or \"stopped\" are negative, which a general list may not know. It also gives a probability, which I use to pick the most confident sentences."),
("Where did your labels come from?", "From the star ratings: 4-5 stars = positive, 1-2 stars = negative. 3 stars are mixed, so I left them out of training. No manual labelling was needed."),
("Why Logistic Regression and not Naive Bayes or SVM?", "All three work on TF-IDF. I chose Logistic Regression because it is simple, fast, gives probabilities directly, and its weights show which words it learned, so I can explain its decisions."),
("Why did you keep stopwords in TF-IDF?", "Because negation words like \"not\" and \"no\" are in the stopword list. Removing them would turn \"not good\" into \"good\"."),
("Why bigrams?", "So \"not good\" or \"stopped working\" becomes one clue instead of two separate words."),
("Your model was trained on reviews but used on sentences. Is that OK?", "Yes, sentences use the same words. I checked it on my own sentences: \"They are not comfortable at all\" scored 0.24 (negative) and \"Great value for the price\" scored 0.95 (positive)."),
("Why work at sentence level?", "Because one review can have both opinions: \"Great sound. Battery died in a week.\" Sentence level puts each opinion with the right feature."),
("Why 0.65 and 0.35 as limits?", "To leave a neutral zone. Sentences like \"I bought these for the gym\" are not opinions, so they get about 0.5 and are ignored. I picked the values by looking at examples; they can be tuned."),
("How do you find features?", "POS tag every sentence, keep the nouns, lemmatize them, drop a small list of nouns that are not features, and count. The most frequent nouns are the features. This idea is from Hu and Liu (2004)."),
("Why is the negative F1 lower than positive?", "There are only 872 negative reviews against 5,107 positive ones, so the model has fewer negative examples to learn from. I used class_weight=\"balanced\" to reduce this effect."),
("Why is positive_% high for every feature?", "Because about 77% of the reviews are 4-5 stars. So \"disliked\" means \"less liked than the other features\", not hated. That is why I compare features with each other."),
("What is extractive vs abstractive summarization?", "Extractive picks real sentences from the reviews (what I did). Abstractive writes new sentences, like a large language model would. Extractive cannot invent anything, so it is safer and easy to check."),
("What would you improve?", "Link each opinion to its nearest feature instead of the whole sentence, merge synonyms (cord/cable), try a pretrained model like BERT, and build a small web page for live use."),
("Where is your data from?", "The public Amazon Reviews 2023 dataset (McAuley Lab, UC San Diego), Electronics category. I kept reviews that mention headphones, earbuds or earphones and removed ones about headphone jacks or adapters."),
]

nb = nbformat.read("Opinion_Summarization.ipynb", 4)
code_cells = [c.source for c in nb.cells if c.cell_type == "code"]
assert len(code_cells) == len(CELLS), (len(code_cells), len(CELLS))

esc = html.escape
parts = []
total = 0
for k, (src, (title, notes)) in enumerate(zip(code_cells, CELLS), 1):
    lines = [l for l in src.split("\n") if l.strip()]
    assert len(lines) == len(notes), (k, title, len(lines), len(notes))
    rows = []
    for line, note in zip(lines, notes):
        total += 1
        rows.append(f'<tr><td class="n">{total}</td><td><pre>{esc(line)}</pre><div class="ex">{note}</div></td></tr>')
    parts.append(f'<h3>Cell {k}: {esc(title)}</h3><table class="code">{"".join(rows)}</table>')

terms = "".join(f"<tr><td><b>{esc(t)}</b></td><td>{esc(d)}</td></tr>" for t, d in TERMS)
qa = "".join(f"<p class='q'>Q{i}. {esc(q)}</p><p class='a'>{esc(a)}</p>" for i, (q, a) in enumerate(QA, 1))

page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Code Explanation</title>
<style>
@page {{ size: A4; margin: 16mm 14mm; }}
body {{ font-family: Calibri, "Segoe UI", Arial, sans-serif; font-size: 11pt; color: #1F2A30; line-height: 1.45; }}
h1 {{ font-family: Cambria, Georgia, serif; font-size: 22pt; margin: 6px 0 4px; }}
h2 {{ font-family: Cambria, Georgia, serif; font-size: 16pt; margin-top: 22px; break-after: avoid; }}
h3 {{ font-size: 12.5pt; margin: 18px 0 6px; color: #3B6E8F; break-after: avoid; }}
.hdr {{ color: #4A5A63; margin-bottom: 10px; }}
table {{ border-collapse: collapse; width: 100%; }}
table.code td {{ border-bottom: 1px solid #DDE3E1; padding: 5px 6px; vertical-align: top; }}
table.code tr {{ break-inside: avoid; }}
td.n {{ width: 26px; color: #8A9BA3; font-size: 9pt; text-align: right; padding-top: 7px; }}
pre {{ margin: 0 0 3px; padding: 4px 6px; background: #EEF3F1; border-radius: 4px; font-family: Menlo, Consolas, monospace;
      font-size: 8.6pt; white-space: pre-wrap; overflow-wrap: anywhere; }}
.ex {{ font-size: 10.5pt; }}
code {{ font-family: Menlo, Consolas, monospace; font-size: 9pt; background: #EEF3F1; padding: 0 3px; border-radius: 3px; }}
.terms td {{ border-bottom: 1px solid #DDE3E1; padding: 5px 6px; vertical-align: top; }}
.terms td:first-child {{ width: 26%; }}
.q {{ font-weight: bold; margin: 12px 0 2px; break-after: avoid; }} .a {{ margin: 0; }}
.flow {{ background: #EEF3F1; padding: 8px 10px; border-radius: 6px; }}
</style></head><body>
<div class="hdr">Name: Ankit Kumar<br>SAP ID: 500120442<br>Batch: 02</div>
<h1>Automatic Opinion Summarization from Customer Reviews</h1>
<div class="hdr">Line-by-line explanation of the code in <code>Opinion_Summarization.ipynb</code></div>

<h2>The project in one paragraph</h2>
<p>I take 6,658 real Amazon headphone reviews. I clean them, train a TF-IDF + Logistic Regression model that tells
positive from negative (using the star ratings as labels), split every review into sentences and score each sentence,
find the product features as the most frequent nouns (POS tagging), count the positive and negative sentences for
each feature, and finally pick real sentences from the reviews as the summary of what customers like and dislike.</p>
<p class="flow"><b>Flow:</b> load CSV → clean text → train model → split into sentences → score sentences →
find nouns (features) → feature table → pick best sentences → print summary</p>

<h2>Key terms in plain words</h2>
<table class="terms">{terms}</table>

<h2>Every line of code</h2>
<p>Each grey box is one line of code from the notebook, in the same order. Blank lines are left out. Some long
statements continue over two or three lines; those lines are explained as \"...\" parts of one idea.</p>
{"".join(parts)}

<h2>Likely viva questions</h2>
{qa}
</body></html>"""
open("Code_Explanation_Ankit_Kumar_500120442.html", "w").write(page)
print("explained", total, "lines")
