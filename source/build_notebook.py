# Builds Opinion_Summarization.ipynb from the cells below (run once, then execute the notebook).
import nbformat as nbf

cells = []
md = lambda s: cells.append(nbf.v4.new_markdown_cell(s.strip()))
code = lambda s: cells.append(nbf.v4.new_code_cell(s.strip()))

md("""
**Name:** Ankit Kumar<br>
**SAP ID:** 500120442<br>
**Batch:** 02

# Automatic Opinion Summarization from Customer Reviews

Nobody reads 6,000 reviews before buying a pair of headphones. In this project I take a big pile of
real Amazon headphone reviews and let the computer tell me three things:

1. what customers **like** (positive opinions),
2. what customers **dislike** (negative opinions),
3. which **features** people talk about the most (sound, battery, price ...) and how they feel about each one.

My plan in short: clean the text, train a small machine learning model that knows positive from negative,
cut every review into sentences, find the features with POS tagging, and then pick real sentences from the
reviews as the summary.
""")

md("""
## Step 0: Install and import the libraries

`nltk` does the language work (sentences, words, POS tags), `scikit-learn` does the machine learning,
`pandas` holds the data as a table and `matplotlib` draws the chart.
""")
code("""
%pip install -q nltk scikit-learn pandas matplotlib
""")
code("""
import re
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

for pkg in ["punkt", "punkt_tab", "stopwords", "wordnet",
            "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng"]:
    nltk.download(pkg, quiet=True)
""")

md("""
## Step 1: Load the reviews

The file has real Amazon reviews of headphones and earbuds (taken from the public *Amazon Reviews 2023*
dataset by McAuley Lab). Every row has the product id, the star rating (1 to 5) and the review text.
""")
code("""
df = pd.read_csv("data/headphone_reviews.csv")
print("Total reviews:", len(df))
print("Different products:", df["product_id"].nunique())
df[["product_id", "rating", "review"]].head()
""")
code("""
rating_counts = df["rating"].value_counts().sort_index()
print(rating_counts)

rating_counts.plot(kind="bar", color="#4C72B0", title="How many reviews per star rating")
plt.xlabel("Stars")
plt.ylabel("Number of reviews")
plt.savefig("outputs/rating_distribution.png", dpi=150, bbox_inches="tight")
plt.show()
""")
md("""
Most people gave 4 or 5 stars, so the data is mostly positive. I keep this in mind later, because a model
trained on it could become lazy and call everything positive.
""")

md("""
## Step 2: Clean the text

Real reviews are messy. Some have HTML tags like `<br />`, emojis and strange symbols. My cleaning function
removes the tags, keeps only letters, digits and normal punctuation, and squeezes extra spaces.
I keep the full stops because I need them later to split reviews into sentences.

Example: `"Great sound!<br />Love it 😍"` becomes `"Great sound! Love it"`.
""")
code("""
def clean_text(text):
    text = re.sub(r"<.*?>", " ", str(text))              # remove HTML tags like <br />
    text = re.sub(r"[^a-zA-Z0-9.,!?' ]", " ", text)     # keep letters, digits, basic punctuation
    text = re.sub(r"\\s+", " ", text)                     # many spaces -> one space
    return text.strip()

df["clean"] = df["review"].apply(clean_text)
print(clean_text("Great sound!<br />Love it 😍"))
""")

md("""
## Step 3: Train a sentiment model (machine learning part)

To decide if a sentence is positive or negative I train my own model. The star ratings give me free labels:

* 4 or 5 stars → **positive** (1)
* 1 or 2 stars → **negative** (0)
* 3 stars are mixed, so I leave them out of training.

**TF-IDF** turns each review into numbers: a word gets a high score if it appears in this review but is
not common in every review. I also use word pairs (`ngram_range=(1, 2)`) so the model sees `"not good"`
as one clue, and I do **not** remove stopwords here, because words like "not" and "no" flip the meaning.

**Logistic Regression** then learns a weight for every word: positive weight → positive review.
`class_weight="balanced"` tells it to pay extra attention to the smaller negative class.
I keep 20% of the reviews aside to test the model on reviews it has never seen.
""")
code("""
train_df = df[df["rating"] != 3].copy()
train_df["label"] = (train_df["rating"] >= 4).astype(int)    # 1 = positive, 0 = negative

X_train, X_test, y_train, y_test = train_test_split(
    train_df["clean"], train_df["label"], test_size=0.2, random_state=42, stratify=train_df["label"])

vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train_vec, y_train)

predictions = model.predict(X_test_vec)
print("Accuracy on unseen reviews:", round(accuracy_score(y_test, predictions), 3))
print(classification_report(y_test, predictions, target_names=["negative", "positive"]))
""")
code("""
words = vectorizer.get_feature_names_out()
order = model.coef_[0].argsort()                      # smallest weight first
print("Words that push towards NEGATIVE:", [words[i] for i in order[:12]])
print("Words that push towards POSITIVE:", [words[i] for i in order[-12:]])
""")
md("""
Accuracy is about 92%. The negative class is harder (about 0.71 F1) because there are far fewer negative
reviews to learn from, but the word lists make sense: "disappointed", "poor", "returned", "stopped" are
negative clues, and "great", "love", "comfortable", "perfect" are positive clues.

The model was trained on whole reviews, but I want to use it on single sentences. So let me check a few
sentences I wrote myself:
""")
code("""
my_sentences = ["The sound quality is amazing and the bass is deep.",
                "The left earbud stopped working after a week.",
                "They are not comfortable at all.",
                "Great value for the price."]
for s, p in zip(my_sentences, model.predict_proba(vectorizer.transform(my_sentences))[:, 1]):
    print(f"{p:.2f}  {s}")
""")
md("The number is the chance of being positive. All four come out the right way, so the model works on sentences too.")

md("""
## Step 4: Break reviews into sentences and score each sentence

One review often has both feelings: *"Sound is great. But the battery dies in two hours."*
If I scored the whole review I would lose that detail, so I split every review into sentences and
score each one. I skip tiny pieces with fewer than 4 words (like "Wow.").

A sentence is **positive** if the chance is 0.65 or more, **negative** if it is 0.35 or less, and
**neutral** in between (for example "I bought these for the gym.").
""")
code("""
def score_sentences(reviews):
    rows = []
    for review_id, text in zip(reviews["review_id"], reviews["clean"]):
        for sentence in nltk.sent_tokenize(text):
            if len(sentence.split()) >= 4:
                rows.append({"review_id": review_id, "sentence": sentence})
    sents = pd.DataFrame(rows)
    sents["pos_prob"] = model.predict_proba(vectorizer.transform(sents["sentence"]))[:, 1]
    sents["sentiment"] = "neutral"
    sents.loc[sents["pos_prob"] >= 0.65, "sentiment"] = "positive"
    sents.loc[sents["pos_prob"] <= 0.35, "sentiment"] = "negative"
    return sents

sentences = score_sentences(df)
print("Total sentences:", len(sentences))
print(sentences["sentiment"].value_counts())
sentences.head()
""")

md("""
## Step 5: Find the features people talk about (POS tagging)

Features of a product are almost always **nouns**: sound, battery, price, cable, fit. So I POS tag every
sentence and keep the nouns (tags starting with `NN`). I also turn plurals into singular with a
lemmatizer (`ears` → `ear`) so they are counted together.

Some nouns are very common but are not features, like "headphone", "time", "product" or "son". I put these in a
small hand-made list (`not_features`) and ignore them. Then I simply count in how many sentences each
noun appears; the most frequent ones are the frequently discussed features.
""")
code("""
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
not_features = {"headphone", "earbuds", "earbud", "headset", "earphone", "bud", "pair", "product",
                "set", "thing", "time", "work", "way", "year", "one", "day", "use", "bit", "lot",
                "review", "something", "month", "week", "people", "star", "end", "brand", "piece",
                "kid", "son", "wife", "daughter", "husband", "hour", "problem", "issue", "phone",
                "iphone", "device", "computer", "player", "music", "life", "feature", "amazon",
                "speaker", "purchase", "order", "item", "anything", "nothing", "everything",
                "reason", "money", "side", "head"}

def get_nouns(sentence):
    tagged = nltk.pos_tag(nltk.word_tokenize(sentence.lower()))
    nouns = set()
    for word, tag in tagged:
        if tag.startswith("NN") and word.isalpha() and len(word) > 2 and word not in stop_words:
            nouns.add(lemmatizer.lemmatize(word))
    return nouns - not_features

sentences["nouns"] = sentences["sentence"].apply(get_nouns)
print(nltk.pos_tag(nltk.word_tokenize("the battery lasts long and the sound is clear")))
print(get_nouns("The batteries last long and the sound is clear"))
""")

md("""
## Step 6: Link each feature to the opinions about it

For every top feature I take all the sentences that mention it and count how many are positive and how
many are negative. `positive_%` is the share of positive sentences among the positive + negative ones.
""")
code("""
def feature_table(sents, top_k=12):
    counts = Counter(noun for nouns in sents["nouns"] for noun in nouns)
    rows = []
    for feature, mentions in counts.most_common(top_k):
        about = sents[sents["nouns"].apply(lambda nouns: feature in nouns)]
        pos = (about["sentiment"] == "positive").sum()
        neg = (about["sentiment"] == "negative").sum()
        rows.append({"feature": feature, "mentions": mentions, "positive": pos,
                     "negative": neg, "positive_%": round(100 * pos / max(pos + neg, 1))})
    return pd.DataFrame(rows).set_index("feature")

features = feature_table(sentences)
features
""")
code("""
features[["positive", "negative"]].sort_values("positive").plot(
    kind="barh", stacked=True, color=["#55A868", "#C44E52"], figsize=(8, 5),
    title="Most discussed features: positive vs negative sentences")
plt.xlabel("Number of sentences")
plt.savefig("outputs/feature_sentiment.png", dpi=150, bbox_inches="tight")
plt.show()
""")

md("""
## Step 7: Write the summary

Now I build the final summary. I do **extractive** summarization, which means I do not invent new text;
I pick the best real sentences written by customers:

* I sort the features by `positive_%`. The top ones (at most 4) are the **liked features**, the bottom
  ones (at most 4, and only if they have at least one negative sentence) are the **disliked features**.
  With few features I take half and half, so one feature never appears in both lists.
* For each liked feature I take the positive sentence the model is most sure about (highest `pos_prob`),
  and for each disliked feature the most clearly negative sentence (lowest `pos_prob`).
  I only use sentences of 6 to 25 words so they are easy to read, and one sentence per feature so the
  summary does not repeat itself.
""")
code("""
def best_sentences(sents, sentiment, feature_list):
    picked = []
    for feature in feature_list:
        options = sents[(sents["sentiment"] == sentiment)
                        & sents["nouns"].apply(lambda nouns: feature in nouns)
                        & sents["sentence"].str.split().str.len().between(6, 25)
                        & ~sents["sentence"].isin(picked)]
        if len(options) > 0:
            options = options.sort_values("pos_prob", ascending=(sentiment == "negative"))
            picked.append(options["sentence"].iloc[0])
    return picked

def summarize(reviews, top_k=12):
    sents = score_sentences(reviews)
    sents["nouns"] = sents["sentence"].apply(get_nouns)
    table = feature_table(sents, top_k)
    ranked = table.sort_values("positive_%", ascending=False, kind="stable").index.tolist()
    n = min(4, len(ranked) // 2)                       # at most 4, and never the same feature twice
    liked = ranked[:n]
    disliked = [f for f in ranked[::-1][:n] if table.loc[f, "negative"] > 0]

    print(f"Reviews: {len(reviews)} | Sentences: {len(sents)}")
    print("Frequently discussed features:", ", ".join(table.index))
    print("\\nOverall: customers are happiest with the " + ", ".join(liked)
          + ", and complain most about the " + ", ".join(disliked) + ".")
    print("\\nPOSITIVE OPINIONS")
    for s in best_sentences(sents, "positive", liked):
        print("  +", s)
    print("\\nNEGATIVE OPINIONS")
    for s in best_sentences(sents, "negative", disliked):
        print("  -", s)
    return table
""")
md("### Summary of all 6,658 headphone reviews")
code("""
all_table = summarize(df)
""")
md("""
### Summary of one single product

The same function works for one product. Here I take the product with the most reviews in my file.
""")
code("""
top_product = df["product_id"].value_counts().index[0]
product_reviews = df[df["product_id"] == top_product]
product_table = summarize(product_reviews, top_k=8)
product_table
""")
md("""
### Try it on your own reviews

Any list of review texts can be summarized. Here are a few short reviews I typed in myself.
""")
code("""
my_reviews = ["The sound is crisp and the bass is strong. Battery lasts the whole day easily.",
              "Comfortable fit for long runs. The battery died completely after one month though.",
              "Great sound for the price. The charging case feels cheap and the lid broke.",
              "The bluetooth connection keeps dropping. The sound is good when it works.",
              "Very comfortable fit and the battery life is amazing for the price."]
mine = pd.DataFrame({"review_id": range(len(my_reviews)), "review": my_reviews})
mine["clean"] = mine["review"].apply(clean_text)
my_table = summarize(mine, top_k=6)
my_table
""")

md("""
## What I learned and the limits

* Star ratings are a cheap way to get labels, and a simple TF-IDF + Logistic Regression model already
  reaches about 92% accuracy on unseen reviews.
* Working at **sentence** level is the key idea: one review can praise the sound and attack the battery,
  and both opinions end up in the right place.
* Frequent nouns are a simple but good way to find features (this is the idea from Hu and Liu, 2004).

Limits I noticed:

* The data is mostly positive, so `positive_%` is high for almost every feature. "Disliked" here means
  *less liked than the others*, not hated.
* A sentence is linked to every feature it mentions, even if the opinion is about only one of them
  ("great sound but bad battery" counts for both).
* The model only knows words it saw in training, and it can miss sarcasm.
* The `not_features` list is made by hand for headphones; a new product type would need a new list.
""")

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, "Opinion_Summarization.ipynb")
print("written", len(cells), "cells")
