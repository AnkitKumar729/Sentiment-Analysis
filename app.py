"""Front page for the Opinion Summarization project.

Run:  streamlit run app.py
It uses the same steps as Opinion_Summarization.ipynb, but you type the reviews in yourself.
"""
import re
from collections import Counter
from pathlib import Path

import nltk
import pandas as pd
import streamlit as st
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Opinion Summarization", page_icon="🎧", layout="wide")

DATA_FILE = Path(__file__).parent / "data" / "headphone_reviews.csv"

NOT_FEATURES = {"headphone", "earbuds", "earbud", "headset", "earphone", "bud", "pair", "product",
                "set", "thing", "time", "work", "way", "year", "one", "day", "use", "bit", "lot",
                "review", "something", "month", "week", "people", "star", "end", "brand", "piece",
                "kid", "son", "wife", "daughter", "husband", "hour", "problem", "issue", "phone",
                "iphone", "device", "computer", "player", "music", "life", "feature", "amazon",
                "speaker", "purchase", "order", "item", "anything", "nothing", "everything",
                "reason", "money", "side", "head"}

SAMPLE_REVIEWS = """The sound is crisp and the bass is strong. Battery lasts the whole day easily.
Comfortable fit for long runs. The battery died completely after one month though.
Great sound for the price. The charging case feels cheap and the lid broke.
The bluetooth connection keeps dropping. The sound is good when it works.
Very comfortable fit and the battery life is amazing for the price."""


# ---------- same NLP steps as the notebook ----------

def clean_text(text):
    text = re.sub(r"<.*?>", " ", str(text))              # remove HTML tags like <br />
    text = re.sub(r"[^a-zA-Z0-9.,!?' ]", " ", text)     # keep letters, digits, basic punctuation
    text = re.sub(r"\s+", " ", text)                     # many spaces -> one space
    return text.strip()


@st.cache_resource(show_spinner="Training the sentiment model on 6,658 reviews...")
def train_model():
    for pkg in ["punkt", "punkt_tab", "stopwords", "wordnet",
                "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng"]:
        nltk.download(pkg, quiet=True)

    df = pd.read_csv(DATA_FILE)
    df["clean"] = df["review"].apply(clean_text)

    train_df = df[df["rating"] != 3].copy()
    train_df["label"] = (train_df["rating"] >= 4).astype(int)    # 1 = positive, 0 = negative
    X_train, X_test, y_train, y_test = train_test_split(
        train_df["clean"], train_df["label"], test_size=0.2, random_state=42,
        stratify=train_df["label"])

    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2)
    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(vectorizer.fit_transform(X_train), y_train)
    accuracy = accuracy_score(y_test, model.predict(vectorizer.transform(X_test)))
    return df, vectorizer, model, accuracy


df, vectorizer, model, accuracy = train_model()
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def score_sentences(reviews):
    rows = []
    for review_id, text in zip(reviews["review_id"], reviews["clean"]):
        for sentence in nltk.sent_tokenize(text):
            if len(sentence.split()) >= 4:
                rows.append({"review_id": review_id, "sentence": sentence})
    sents = pd.DataFrame(rows, columns=["review_id", "sentence"])
    if sents.empty:
        return sents
    sents["pos_prob"] = model.predict_proba(vectorizer.transform(sents["sentence"]))[:, 1]
    sents["sentiment"] = "neutral"
    sents.loc[sents["pos_prob"] >= 0.65, "sentiment"] = "positive"
    sents.loc[sents["pos_prob"] <= 0.35, "sentiment"] = "negative"
    return sents


def get_nouns(sentence):
    tagged = nltk.pos_tag(nltk.word_tokenize(sentence.lower()))
    nouns = set()
    for word, tag in tagged:
        if tag.startswith("NN") and word.isalpha() and len(word) > 2 and word not in stop_words:
            nouns.add(lemmatizer.lemmatize(word))
    return nouns - NOT_FEATURES


def feature_table(sents, top_k):
    counts = Counter(noun for nouns in sents["nouns"] for noun in nouns)
    rows = []
    for feature, mentions in counts.most_common(top_k):
        about = sents[sents["nouns"].apply(lambda nouns: feature in nouns)]
        pos = (about["sentiment"] == "positive").sum()
        neg = (about["sentiment"] == "negative").sum()
        rows.append({"feature": feature, "mentions": mentions, "positive": pos,
                     "negative": neg, "positive_%": round(100 * pos / max(pos + neg, 1))})
    return pd.DataFrame(rows, columns=["feature", "mentions", "positive", "negative",
                                       "positive_%"]).set_index("feature")


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


def summarize(reviews, top_k):
    reviews = reviews.copy()
    reviews["clean"] = reviews["review"].apply(clean_text)
    sents = score_sentences(reviews)
    if sents.empty:
        return None
    sents["nouns"] = sents["sentence"].apply(get_nouns)
    table = feature_table(sents, top_k)
    ranked = table.sort_values("positive_%", ascending=False, kind="stable").index.tolist()
    n = min(4, len(ranked) // 2)                       # at most 4, and never the same feature twice
    liked = ranked[:n]
    disliked = [f for f in ranked[::-1][:n] if table.loc[f, "negative"] > 0]
    return {"sents": sents, "table": table, "liked": liked, "disliked": disliked,
            "positive": best_sentences(sents, "positive", liked),
            "negative": best_sentences(sents, "negative", disliked)}


# ---------- the page ----------

st.title("🎧 Automatic Opinion Summarization from Customer Reviews")
st.caption("Ankit Kumar | SAP ID 500120442 | Batch 02")
st.markdown("**How it works:** reviews ➜ clean the text ➜ split into sentences ➜ "
            "score each sentence (TF-IDF + Logistic Regression) ➜ find features with POS tagging "
            "(nouns) ➜ pick the best real sentences as the summary")

with st.sidebar:
    st.header("The model")
    st.metric("Trained on", f"{len(df):,} reviews")
    st.metric("Accuracy on unseen reviews", f"{accuracy:.1%}")
    st.markdown("4-5 stars = positive, 1-2 stars = negative, 3 stars left out.\n\n"
                "A sentence is **positive** if P(positive) ≥ 0.65, **negative** if ≤ 0.35, "
                "otherwise neutral.")

st.header("1. Input")
mode = st.radio("Where do the reviews come from?",
                ["Type my own reviews", "Pick a product from the dataset"], horizontal=True)

if mode == "Type my own reviews":
    text = st.text_area("Write one review per line", value=SAMPLE_REVIEWS, height=180)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    reviews = pd.DataFrame({"review_id": range(len(lines)), "review": lines})
    top_k = 6
else:
    counts = df["product_id"].value_counts().head(20)
    labels = {f"{pid}  ({n} reviews)": pid for pid, n in counts.items()}
    product = labels[st.selectbox("Product (Amazon ID, most reviewed first)", list(labels))]
    reviews = df[df["product_id"] == product][["review_id", "rating", "review"]]
    with st.expander(f"See the {len(reviews)} input reviews"):
        st.dataframe(reviews, hide_index=True, use_container_width=True)
    top_k = 8

if st.button("Summarize", type="primary"):
    if reviews.empty:
        st.warning("Type at least one review first.")
        st.stop()
    with st.spinner("Scoring sentences and finding features..."):
        result = summarize(reviews, top_k)
    if result is None:
        st.warning("No sentence has 4 or more words, so there is nothing to score.")
        st.stop()

    sents, table = result["sents"], result["table"]
    st.header("2. Output")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reviews", len(reviews))
    c2.metric("Sentences scored", len(sents))
    c3.metric("Positive sentences", int((sents["sentiment"] == "positive").sum()))
    c4.metric("Negative sentences", int((sents["sentiment"] == "negative").sum()))

    st.subheader("Summary")
    if result["liked"]:
        line = "Customers are happiest with the **" + ", ".join(result["liked"]) + "**"
        if result["disliked"]:
            line += ", and complain most about the **" + ", ".join(result["disliked"]) + "**"
        st.info(line + ".")
    else:
        st.info("Too few features to split into liked and disliked (needs at least 2). "
                "The score of every sentence is in the table at the bottom.")
    left, right = st.columns(2)
    with left:
        st.markdown("#### 👍 Positive opinions")
        for s in result["positive"] or ["(none found)"]:
            st.success(s)
    with right:
        st.markdown("#### 👎 Negative opinions")
        for s in result["negative"] or ["(none found)"]:
            st.error(s)

    st.subheader("Frequently discussed features")
    if table.empty:
        st.write("No features (nouns) found.")
    else:
        left, right = st.columns([1, 1])
        left.dataframe(table, use_container_width=True)
        # names sort the same way as the colours: negative = red, positive = green
        right.bar_chart(table[["negative", "positive"]], color=["#C44E52", "#55A868"])

    st.subheader("Step by step: every sentence and its score")
    show = sents.assign(features=sents["nouns"].apply(lambda n: ", ".join(sorted(n))))
    show["sentiment"] = show["sentiment"].map(
        {"positive": "🟢 positive", "negative": "🔴 negative", "neutral": "⚪ neutral"})
    st.dataframe(
        show[["review_id", "sentence", "pos_prob", "sentiment", "features"]],
        hide_index=True, use_container_width=True,
        column_config={"pos_prob": st.column_config.ProgressColumn(
            "P(positive)", min_value=0.0, max_value=1.0, format="%.2f")})
