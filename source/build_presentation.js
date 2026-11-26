// Builds Presentation/Opinion_Summarization_Presentation.pptx
// Run from the project folder:  node source/build_presentation.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const { applyTheme } = require(process.env.APPLY_THEME);

const THEME = {
  name: "Opinion Summary",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F2A30", lt1: "FFFFFF", dk2: "4A5A63", lt2: "EEF3F1",
    accent1: "2E8B57", accent2: "C8483F", accent3: "E8A33D",
    accent4: "3B6E8F", accent5: "8A9BA3", accent6: "6B4E9B",
    hlink: "3B6E8F", folHlink: "6B4E9B",
  },
};
const HEX = THEME.colors;
const OUT = path.join("Presentation", "Opinion_Summarization_Presentation.pptx");

async function icon(Comp, color) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: 256 }));
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
  pres.title = "Automatic Opinion Summarization from Customer Reviews";
  pres.author = "Ankit Kumar";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;

  pres.defineSlideMaster({
    title: "DARK",
    background: { color: C.text1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.0, w: 11.7, h: 1.8,
          fontSize: 44, bold: true, color: C.background1, valign: "bottom", align: "left" }, text: "" } },
      { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.0, w: 11.7, h: 1.0,
          fontSize: 20, color: C.background2, valign: "top", align: "left" }, text: "" } },
    ],
  });
  pres.defineSlideMaster({
    title: "CONTENT",
    background: { color: C.background1 },
    margin: [0.5, 0.6, 0.6, 0.6],
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.9,
          fontSize: 34, bold: true, color: C.text1, valign: "middle", align: "left" }, text: "" } },
      { text: { text: "Opinion Summarization  |  Ankit Kumar", options: {
          x: 0.6, y: 7.0, w: 6, h: 0.3, fontSize: 10, color: C.text2, margin: 0 } } },
    ],
    slideNumber: { x: 12.2, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: C.text2, align: "right" },
  });

  const ic = {};
  for (const [k, comp, col] of [
    ["comments", fa.FaComments, "FFFFFF"], ["up", fa.FaThumbsUp, "FFFFFF"], ["down", fa.FaThumbsDown, "FFFFFF"],
    ["tags", fa.FaTags, "FFFFFF"], ["broom", fa.FaBroom, "FFFFFF"], ["brain", fa.FaBrain, "FFFFFF"],
    ["cut", fa.FaCut, "FFFFFF"], ["link", fa.FaLink, "FFFFFF"], ["file", fa.FaFileAlt, "FFFFFF"],
    ["star", fa.FaStar, HEX.accent3], ["head", fa.FaHeadphones, HEX.accent3], ["user", fa.FaUserEdit, "FFFFFF"],
    ["warn", fa.FaExclamationTriangle, "FFFFFF"], ["rocket", fa.FaRocket, "FFFFFF"], ["box", fa.FaBox, "FFFFFF"],
  ]) ic[k] = await icon(comp, col);

  const circleIcon = (s, key, x, y, d, fill, name) => {
    s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" }, objectName: name + " circle" });
    const p = d * 0.25;
    s.addImage({ data: ic[key], x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, objectName: name + " icon" });
  };
  const card = (s, x, y, w, h, name, fill) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.12, fill: { color: fill || C.background2 }, line: { type: "none" }, objectName: name });
  const txt = (s, text, o) => s.addText(text, Object.assign({ isTextBox: true, fontSize: 16, color: C.text1, valign: "top" }, o));
  const content = (title, section) => {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
    s.addText(title, { placeholder: "title" });
    return s;
  };

  // 1. Title ---------------------------------------------------------------
  pres.addSection({ title: "Introduction" });
  let s = pres.addSlide({ masterName: "DARK", sectionTitle: "Introduction" });
  s.addImage({ data: ic.head, x: 0.8, y: 1.0, w: 0.8, h: 0.8, objectName: "headphones icon" });
  s.addText("Automatic Opinion Summarization from Customer Reviews", { placeholder: "title" });
  s.addText("What do 6,658 headphone buyers like, dislike and talk about most?", { placeholder: "body" });
  txt(s, [
    { text: "Ankit Kumar", options: { bold: true, breakLine: true } },
    { text: "SAP ID: 500120442   |   Batch: 02", options: { breakLine: true } },
    { text: "Natural Language Processing Project" },
  ], { x: 0.8, y: 5.4, w: 8, h: 1.2, fontSize: 16, color: C.background1 });
  s.addNotes("Good morning. My project is about automatically summarizing what customers say in product reviews. I used real Amazon headphone reviews.");

  // 2. Problem ---------------------------------------------------------------
  s = content("Too many reviews, too little time", "Introduction");
  txt(s, "6,658", { x: 0.6, y: 1.6, w: 4.6, h: 1.4, fontSize: 72, bold: true, color: C.accent2, fontFace: "Cambria", margin: 0 });
  txt(s, "headphone reviews in my dataset. Nobody reads all of them before buying.", {
    x: 0.6, y: 3.0, w: 4.4, h: 1.0, fontSize: 18, color: C.text2, margin: 0 });
  txt(s, "Goal: let the computer read them and answer three questions", {
    x: 0.6, y: 4.5, w: 4.4, h: 1.0, fontSize: 18, bold: true, margin: 0 });
  const goals = [
    ["up", C.accent1, "What do customers like?", "A summary of positive opinions"],
    ["down", C.accent2, "What do they dislike?", "A summary of negative opinions"],
    ["tags", C.accent4, "Which features come up most?", "Sound, battery, price ... and the feeling about each"],
  ];
  goals.forEach(([k, col, h, d], i) => {
    const y = 1.55 + i * 1.75;
    card(s, 5.7, y, 7.0, 1.45, "goal card " + (i + 1));
    circleIcon(s, k, 5.95, y + 0.3, 0.85, col, "goal " + (i + 1));
    txt(s, h, { x: 7.05, y: y + 0.25, w: 5.4, h: 0.5, fontSize: 20, bold: true, margin: 0 });
    txt(s, d, { x: 7.05, y: y + 0.75, w: 5.4, h: 0.5, fontSize: 15, color: C.text2, margin: 0 });
  });
  s.addNotes("Online products have thousands of reviews. Reading them all is impossible, so the aim is a short summary: what people like, what they dislike, and which features they talk about.");

  // 3. Dataset ---------------------------------------------------------------
  pres.addSection({ title: "Method" });
  s = content("The data: real Amazon headphone reviews", "Method");
  const stats = [["6,658", "reviews"], ["4,397", "different products"], ["1 to 5", "star rating on each review"]];
  stats.forEach(([n, l], i) => {
    const y = 1.5 + i * 1.65;
    card(s, 0.6, y, 4.3, 1.4, "stat card " + (i + 1));
    txt(s, n, { x: 0.85, y: y + 0.15, w: 3.9, h: 0.7, fontSize: 36, bold: true, color: C.accent4, fontFace: "Cambria", margin: 0 });
    txt(s, l, { x: 0.85, y: y + 0.85, w: 3.9, h: 0.4, fontSize: 15, color: C.text2, margin: 0 });
  });
  // Keynote does not draw native PowerPoint charts, so the charts are images (source/make_slide_charts.py)
  s.addImage({ path: "outputs/slide_ratings.png", x: 5.4, y: 1.4, w: 7.3, h: 4.6, objectName: "rating chart",
    altText: "Bar chart: 477 one-star, 395 two-star, 679 three-star, 1333 four-star and 3774 five-star reviews" });
  txt(s, "Source: Amazon Reviews 2023 (McAuley Lab), Electronics category, reviews that mention headphones or earbuds.", {
    x: 5.4, y: 6.15, w: 7.3, h: 0.6, fontSize: 12, color: C.text2, margin: 0 });
  s.addNotes("I took real reviews from the public Amazon Reviews 2023 dataset and kept the ones about headphones and earbuds. Most reviews are 4 or 5 stars, so the data is mostly positive. This matters later.");

  // 4. Pipeline ---------------------------------------------------------------
  s = content("How it works: six simple steps", "Method");
  const steps = [
    ["broom", "Clean", "Remove HTML tags, emojis and extra spaces"],
    ["brain", "Train model", "TF-IDF + Logistic Regression learns positive vs negative"],
    ["cut", "Split sentences", "Score every sentence on its own"],
    ["tags", "Find features", "POS tagging keeps the nouns, count the most frequent"],
    ["link", "Link opinions", "Count positive and negative sentences per feature"],
    ["file", "Summarize", "Pick the best real sentences for likes and dislikes"],
  ];
  steps.forEach(([k, h, d], i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.6 + col * 4.1, y = 1.5 + row * 2.7;
    card(s, x, y, 3.8, 2.4, "step card " + (i + 1));
    circleIcon(s, k, x + 0.3, y + 0.3, 0.8, i === 1 ? C.accent3 : C.accent4, "step " + (i + 1));
    txt(s, String(i + 1), { x: x + 2.9, y: y + 0.25, w: 0.6, h: 0.6, fontSize: 28, bold: true, color: C.accent5, align: "right", margin: 0, fontFace: "Cambria" });
    txt(s, h, { x: x + 0.3, y: y + 1.2, w: 3.2, h: 0.45, fontSize: 20, bold: true, margin: 0 });
    txt(s, d, { x: x + 0.3, y: y + 1.65, w: 3.2, h: 0.7, fontSize: 14, color: C.text2, margin: 0 });
  });
  s.addNotes("The whole project is six steps. Step 2, the yellow one, is the machine learning part. The rest are classic NLP steps from NLTK.");

  // 5. Cleaning + labels ---------------------------------------------------------------
  s = content("Steps 1 and 2: clean text and free labels", "Method");
  card(s, 0.6, 1.5, 5.9, 4.9, "cleaning card");
  txt(s, "Cleaning with regular expressions", { x: 0.9, y: 1.75, w: 5.3, h: 0.5, fontSize: 20, bold: true, margin: 0 });
  txt(s, "Before", { x: 0.9, y: 2.5, w: 5.3, h: 0.35, fontSize: 14, bold: true, color: C.accent2, margin: 0 });
  txt(s, "Great sound!<br />Love it 😍", { x: 0.9, y: 2.85, w: 5.3, h: 0.5, fontSize: 16, fontFace: "Courier New", margin: 0 });
  txt(s, "After", { x: 0.9, y: 3.55, w: 5.3, h: 0.35, fontSize: 14, bold: true, color: C.accent1, margin: 0 });
  txt(s, "Great sound! Love it", { x: 0.9, y: 3.9, w: 5.3, h: 0.5, fontSize: 16, fontFace: "Courier New", margin: 0 });
  txt(s, "Full stops are kept, because the next steps need them to split sentences.", {
    x: 0.9, y: 4.8, w: 5.3, h: 0.9, fontSize: 15, color: C.text2, margin: 0 });

  txt(s, "Star ratings become labels", { x: 7.1, y: 1.6, w: 5.6, h: 0.5, fontSize: 20, bold: true, margin: 0 });
  const labels = [["4 or 5 stars", "positive (1)", C.accent1], ["1 or 2 stars", "negative (0)", C.accent2], ["3 stars", "mixed, left out of training", C.accent5]];
  labels.forEach(([a, b, col], i) => {
    const y = 2.35 + i * 1.15;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.1, y, w: 2.2, h: 0.85, rectRadius: 0.1, fill: { color: col }, line: { type: "none" }, objectName: "label chip " + (i + 1) });
    txt(s, a, { x: 7.1, y, w: 2.2, h: 0.85, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0 });
    txt(s, "→  " + b, { x: 9.5, y, w: 3.2, h: 0.85, fontSize: 16, valign: "middle", margin: 0 });
  });
  txt(s, "No manual labelling needed: customers already labelled their own reviews.", {
    x: 7.1, y: 5.85, w: 5.6, h: 0.6, fontSize: 15, italic: true, color: C.text2, margin: 0 });
  s.addNotes("Cleaning uses three regular expressions. For labels I used the stars: 4-5 is positive, 1-2 is negative, 3 is mixed so I skip it for training.");

  // 6. Model ---------------------------------------------------------------
  s = content("Step 2: the sentiment model", "Method");
  const model = [
    ["TF-IDF", "Turns text into numbers. A word scores high when it is frequent in this review but rare across all reviews.",
      "Uses single words and word pairs, so \"not good\" is one clue. Stopwords are kept, because \"not\" and \"no\" flip the meaning."],
    ["Logistic Regression", "Learns one weight per word. Positive weights push towards positive, negative weights towards negative.",
      "class_weight = \"balanced\" makes it pay more attention to the smaller negative class."],
  ];
  model.forEach(([h, a, b], i) => {
    const x = 0.6 + i * 6.15;
    card(s, x, 1.5, 5.95, 3.7, "model card " + (i + 1));
    txt(s, h, { x: x + 0.35, y: 1.75, w: 5.3, h: 0.55, fontSize: 24, bold: true, color: C.accent4, fontFace: "Cambria", margin: 0 });
    txt(s, a, { x: x + 0.35, y: 2.45, w: 5.3, h: 1.2, fontSize: 16, margin: 0 });
    txt(s, b, { x: x + 0.35, y: 3.75, w: 5.3, h: 1.2, fontSize: 15, color: C.text2, margin: 0 });
  });
  txt(s, "80% of the reviews train the model, 20% are kept aside to test it on reviews it has never seen.", {
    x: 0.6, y: 5.6, w: 12.1, h: 0.6, fontSize: 18, bold: true, margin: 0 });
  s.addNotes("TF-IDF converts text into numbers, Logistic Regression learns which words mean positive or negative. I keep 20 percent aside for testing.");

  // 7. Results ---------------------------------------------------------------
  pres.addSection({ title: "Results" });
  s = content("The model is right 92% of the time", "Results");
  txt(s, "91.6%", { x: 0.6, y: 1.5, w: 4.4, h: 1.3, fontSize: 72, bold: true, color: C.accent1, fontFace: "Cambria", margin: 0 });
  txt(s, "accuracy on 1,196 unseen reviews", { x: 0.6, y: 2.8, w: 4.4, h: 0.5, fontSize: 16, color: C.text2, margin: 0 });
  const hdr = { bold: true, color: C.background1, fill: { color: C.text1 }, fontSize: 14 };
  s.addTable([
    [{ text: "Class", options: hdr }, { text: "Precision", options: hdr }, { text: "Recall", options: hdr }, { text: "F1", options: hdr }],
    ["Negative", "0.72", "0.70", "0.71"], ["Positive", "0.95", "0.95", "0.95"],
  ], { x: 0.6, y: 3.6, w: 4.4, colW: [1.4, 1.1, 0.95, 0.95], fontSize: 14, color: C.text1,
    border: { type: "solid", pt: 0.5, color: "DDE3E1" }, rowH: 0.45, objectName: "metrics table" });
  txt(s, "Negative is harder: far fewer negative reviews to learn from.", { x: 0.6, y: 5.15, w: 4.4, h: 0.8, fontSize: 14, color: C.text2, margin: 0 });

  const wordsBox = (x, title, col, words) => {
    card(s, x, 1.5, 3.55, 4.9, title + " card");
    txt(s, title, { x: x + 0.3, y: 1.7, w: 3.0, h: 0.5, fontSize: 18, bold: true, color: col, margin: 0 });
    txt(s, words.map((w, i) => ({ text: w, options: { breakLine: i < words.length - 1 } })),
      { x: x + 0.3, y: 2.3, w: 3.0, h: 3.9, fontSize: 16, margin: 0, paraSpaceAfter: 4 });
  };
  wordsBox(5.5, "Top negative words", C.accent2, ["not", "disappointed", "poor", "return / returned", "horrible", "stopped", "useless", "disappointing"]);
  wordsBox(9.15, "Top positive words", C.accent1, ["great", "love", "easy", "good", "works well", "nice", "excellent", "comfortable"]);
  s.addNotes("On reviews the model never saw, it is right 91.6 percent of the time. The words it learned make sense, which shows it learned real opinion words.");

  // 8. Sentences ---------------------------------------------------------------
  s = content("Step 3: one review, many opinions", "Results");
  txt(s, "A review often praises one thing and attacks another, so every sentence gets its own score.", {
    x: 0.6, y: 1.35, w: 12.1, h: 0.5, fontSize: 18, color: C.text2, margin: 0 });
  const ex = [["The sound quality is amazing and the bass is deep.", "0.73", "positive", C.accent1],
              ["They are not comfortable at all.", "0.24", "negative", C.accent2],
              ["The left earbud stopped working after a week.", "0.03", "negative", C.accent2],
              ["Great value for the price.", "0.95", "positive", C.accent1]];
  ex.forEach(([t, p, l, col], i) => {
    const y = 2.1 + i * 0.85;
    card(s, 0.6, y, 8.2, 0.7, "sentence card " + (i + 1));
    txt(s, t, { x: 0.85, y, w: 5.9, h: 0.7, fontSize: 15, valign: "middle", margin: 0 });
    txt(s, p, { x: 6.8, y, w: 0.8, h: 0.7, fontSize: 16, bold: true, valign: "middle", align: "right", margin: 0 });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.75, y: y + 0.15, w: 0.9, h: 0.4, rectRadius: 0.08, fill: { color: col }, line: { type: "none" }, objectName: "tag " + (i + 1) });
    txt(s, l, { x: 7.75, y: y + 0.15, w: 0.9, h: 0.4, fontSize: 11, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0 });
  });
  txt(s, "Number = chance the sentence is positive", { x: 0.6, y: 5.55, w: 8.2, h: 0.4, fontSize: 13, italic: true, color: C.text2, margin: 0 });
  card(s, 9.3, 2.1, 3.4, 4.0, "threshold card");
  txt(s, [
    { text: "≥ 0.65  positive", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "≤ 0.35  negative", options: { bold: true, color: C.accent2, breakLine: true } },
    { text: "in between  neutral", options: { bold: true, color: C.text2, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "39,961 sentences: 15,415 positive, 3,326 negative, 21,220 neutral", options: { fontSize: 14, color: C.text2 } },
  ], { x: 9.55, y: 2.35, w: 2.95, h: 3.6, fontSize: 17, margin: 0, paraSpaceAfter: 6 });
  s.addNotes("I split reviews into sentences with NLTK and score each one. Neutral sentences like 'I bought these for the gym' are ignored in the summary.");

  // 9. Features ---------------------------------------------------------------
  s = content("Step 4: features are nouns", "Results");
  txt(s, "POS tagging labels every word. Product features are nearly always nouns (NN).", {
    x: 0.6, y: 1.35, w: 12.1, h: 0.5, fontSize: 18, color: C.text2, margin: 0 });
  const tags = [["the", "DT"], ["battery", "NN"], ["lasts", "VBZ"], ["long", "RB"], ["and", "CC"], ["the", "DT"], ["sound", "NN"], ["is", "VBZ"], ["clear", "JJ"]];
  let tx = 0.6;
  tags.forEach(([w, t], i) => {
    const wd = 0.45 + w.length * 0.13, noun = t === "NN";
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: tx, y: 2.2, w: wd, h: 1.1, rectRadius: 0.08,
      fill: { color: noun ? C.accent3 : C.background2 }, line: { type: "none" }, objectName: "token " + (i + 1) });
    txt(s, [{ text: w, options: { bold: true, breakLine: true } }, { text: t, options: { fontSize: 12, color: C.text2 } }],
      { x: tx, y: 2.2, w: wd, h: 1.1, fontSize: 16, align: "center", valign: "middle", margin: 0 });
    tx += wd + 0.15;
  });
  const fsteps = [["Keep nouns", "Tags starting with NN, longer than 2 letters, not a stopword"],
                  ["Lemmatize", "ears → ear, batteries → battery, so they count together"],
                  ["Drop non-features", "A small hand-made list: headphone, time, product, son ..."],
                  ["Count", "The most frequent nouns are the most discussed features"]];
  fsteps.forEach(([h, d], i) => {
    const x = 0.6 + i * 3.08;
    card(s, x, 3.85, 2.85, 2.5, "feature step " + (i + 1));
    txt(s, (i + 1) + ". " + h, { x: x + 0.25, y: 4.05, w: 2.4, h: 0.5, fontSize: 18, bold: true, margin: 0 });
    txt(s, d, { x: x + 0.25, y: 4.6, w: 2.4, h: 1.6, fontSize: 14, color: C.text2, margin: 0 });
  });
  s.addNotes("This is the frequent-noun method from Hu and Liu, 2004. Features are nouns, so I keep the nouns, merge plurals, drop generic words, and count.");

  // 10. Feature chart ---------------------------------------------------------------
  s = content("Step 5: what people say about each feature", "Results");
  s.addImage({ path: "outputs/slide_features.png", x: 0.6, y: 1.35, w: 7.6, h: 5.5, objectName: "feature chart",
    altText: "Stacked bars of positive and negative sentences for sound, quality, price, ear, case, noise, battery, fit, bass, cable, cord and volume" });
  const callouts = [["98%", "price", "of opinions are positive: the best liked feature", C.accent1],
                    ["77%", "volume", "positive: the most complained-about feature", C.accent2]];
  callouts.forEach(([n, f, d, col], i) => {
    const y = 1.5 + i * 2.6;
    card(s, 8.6, y, 4.1, 2.3, "callout " + (i + 1));
    txt(s, n, { x: 8.85, y: y + 0.2, w: 1.9, h: 0.9, fontSize: 40, bold: true, color: col, fontFace: "Cambria", margin: 0 });
    txt(s, f, { x: 10.7, y: y + 0.35, w: 1.8, h: 0.6, fontSize: 22, bold: true, margin: 0 });
    txt(s, d, { x: 8.85, y: y + 1.2, w: 3.6, h: 0.9, fontSize: 15, color: C.text2, margin: 0 });
  });
  s.addNotes("Sound and quality are talked about the most. Price is almost always positive. Volume, ear and cord collect the most complaints, usually one side stopping or the cord wearing out.");

  // 11. Summary ---------------------------------------------------------------
  s = content("Step 6: the final summary", "Results");
  txt(s, "Extractive summary: real customer sentences, one per feature, picked where the model is most confident.", {
    x: 0.6, y: 1.3, w: 12.1, h: 0.5, fontSize: 16, color: C.text2, margin: 0 });
  const sumCol = (x, key, col, head, feat, lines) => {
    card(s, x, 2.0, 5.95, 4.75, head + " card");
    circleIcon(s, key, x + 0.3, 2.25, 0.7, col, head);
    txt(s, head, { x: x + 1.2, y: 2.25, w: 4.5, h: 0.4, fontSize: 20, bold: true, margin: 0 });
    txt(s, feat, { x: x + 1.2, y: 2.65, w: 4.5, h: 0.35, fontSize: 14, color: col, bold: true, margin: 0 });
    txt(s, lines.map((l, i) => ({ text: "“" + l + "”", options: { breakLine: i < lines.length - 1 } })),
      { x: x + 0.3, y: 3.25, w: 5.35, h: 3.35, fontSize: 14, margin: 0, paraSpaceAfter: 8 });
  };
  sumCol(0.6, "up", C.accent1, "What customers like", "price · case · cable · fit", [
    "These are great for the price.", "This is a great carry case for my Sony earbuds and charger.",
    "They are easy to charge with just a USB cable.", "This is a nice set of earbuds, with good sound quality and a comfortable fit."]);
  sumCol(6.75, "down", C.accent2, "What customers dislike", "volume · ear · cord · bass", [
    "Right side earphone doesn't produce the same volume of sound as left side.",
    "Just two months after I recieced them, the right ear completely stopped working.",
    "After a few months the cord was getting worn and my left earbud was flickering.",
    "The sound out of the one side that work is loud, but not clear at all, and absolutely no bass at all."]);
  s.addNotes("This is the output for all 6,658 reviews. Liked features have the highest positive percentage, disliked the lowest. Sentences are copied exactly from reviews, typos included, so nothing is invented.");

  // 12. Any input ---------------------------------------------------------------
  s = content("Same function, any set of reviews", "Results");
  const demos = [
    ["box", C.accent4, "One product", "101 reviews of the most reviewed earbuds", [
      ["Liked", "price, sound, charge, battery", C.accent1], ["Disliked", "noise, volume, ear, quality", C.accent2],
      ["Example", "“There is no bass or noise canceling at all.”", C.text2]]],
    ["user", C.accent3, "My own 5 reviews", "Typed by me to test the system", [
      ["Liked", "sound, fit, price", C.accent1], ["Disliked", "battery", C.accent2],
      ["Example", "“The battery died completely after one month though.”", C.text2]]],
  ];
  demos.forEach(([k, col, h, d, rows], i) => {
    const x = 0.6 + i * 6.15;
    card(s, x, 1.5, 5.95, 5.0, h + " card");
    circleIcon(s, k, x + 0.35, 1.8, 0.85, col, h);
    txt(s, h, { x: x + 1.4, y: 1.8, w: 4.3, h: 0.45, fontSize: 22, bold: true, margin: 0 });
    txt(s, d, { x: x + 1.4, y: 2.25, w: 4.3, h: 0.4, fontSize: 14, color: C.text2, margin: 0 });
    rows.forEach(([a, b, c2], j) => {
      const y = 3.05 + j * 1.1;
      txt(s, a, { x: x + 0.35, y, w: 5.2, h: 0.35, fontSize: 13, bold: true, color: c2, margin: 0 });
      txt(s, b, { x: x + 0.35, y: y + 0.35, w: 5.2, h: 0.65, fontSize: 16, margin: 0 });
    });
  });
  s.addNotes("The summarize function takes any table of reviews. It works for one product with 101 reviews and even for five reviews I typed myself.");

  // 13. Limits ---------------------------------------------------------------
  pres.addSection({ title: "Conclusion" });
  s = content("Limitations and future scope", "Conclusion");
  const lim = ["Data is mostly positive, so \"disliked\" means less liked than the others, not hated",
               "A sentence counts for every feature it names: \"great sound, bad battery\" counts for both",
               "The model can miss sarcasm and words it never saw in training",
               "The list of non-feature nouns is hand-made for headphones"];
  const fut = ["Link each opinion word to its nearest feature instead of the whole sentence",
               "Group synonyms like cord and cable into one feature",
               "Try a pretrained model such as BERT for sentence sentiment",
               "A small web page where a user pastes reviews and gets the summary"];
  [[lim, "warn", C.accent2, "Limitations"], [fut, "rocket", C.accent4, "Future scope"]].forEach(([items, k, col, h], i) => {
    const x = 0.6 + i * 6.15;
    card(s, x, 1.5, 5.95, 5.0, h + " card");
    circleIcon(s, k, x + 0.35, 1.75, 0.75, col, h);
    txt(s, h, { x: x + 1.3, y: 1.85, w: 4.3, h: 0.55, fontSize: 22, bold: true, margin: 0 });
    txt(s, items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1 } })),
      { x: x + 0.35, y: 2.8, w: 5.3, h: 3.5, fontSize: 16, margin: 0, paraSpaceAfter: 10 });
  });
  s.addNotes("I want to be honest about the limits. Each one has a matching improvement on the right.");

  // 14. Thank you ---------------------------------------------------------------
  s = pres.addSlide({ masterName: "DARK", sectionTitle: "Conclusion" });
  s.addText("Thank you. Questions?", { placeholder: "title" });
  s.addText("Clean → Train → Split → Find features → Link → Summarize", { placeholder: "body" });
  txt(s, [
    { text: "References", options: { bold: true, breakLine: true } },
    { text: "Hu, M. and Liu, B. (2004). Mining and Summarizing Customer Reviews. KDD.", options: { breakLine: true } },
    { text: "Hou, Y. et al. (2024). Amazon Reviews 2023 dataset, McAuley Lab, UC San Diego.", options: { breakLine: true } },
    { text: "Libraries: NLTK, scikit-learn, pandas, matplotlib." },
  ], { x: 0.8, y: 5.2, w: 11.7, h: 1.5, fontSize: 14, color: C.background2, margin: 0 });
  s.addNotes("To sum up: with simple NLP and one small machine learning model, thousands of reviews become a one-screen summary. Thank you.");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
