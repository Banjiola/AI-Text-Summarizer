# 💼 Project Title: AI Text Summarizer + Named Entity Recognition Web App

> *"An AI-powered web application that summarizes long-form text and highlights key entities like people, organizations, and locations for improved reading comprehension and insight extraction."*

---

## 📌 Table of Contents
- [Overview](#overview)
- [Business Objective](#business-objective)
- [Dataset](#dataset)
- [Tools & Techniques](#tools--techniques)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Feature Engineering](#feature-engineering)
- [Modeling](#modeling)
- [Results & Insights](#results--insights)
- [Dashboard / Visuals](#dashboard--visuals)
- [Conclusion](#conclusion)
- [Next Steps](#next-steps)
- [Author](#author)

---

## 🧩 Overview

This application combines Natural Language Processing models for:
- Generating concise summaries from large text using `facebook/bart-large-cnn`
- Identifying named entities like people, organizations, and locations using `dslim/bert-base-NER`

It's built with Gradio and hosted on Hugging Face Spaces, allowing users to test text analysis capabilities interactively through a simple web interface.

---

## 🎯 Business Objective

> Designed for:
- Researchers, journalists, analysts, and students
- Anyone needing to digest long-form content quickly while retaining key information

> Value:
- Saves time by summarizing text
- Enhances understanding by highlighting important named entities

---

## 📊 Dataset

- **Input Type**: Any user-provided long-form English text (100+ words)
- **Examples**: News articles, research summaries, policy briefs, blog content
- **No external dataset**: The app processes user inputs in real time

---

## 🛠️ Tools & Techniques

| **Category**       | **Tools**                         |
|--------------------|-----------------------------------|
| Language           | Python                            |
| Models             | `bart-large-cnn`, `bert-base-NER` |
| App Framework      | Gradio                            |
| Hosting            | Hugging Face Spaces               |
| Visualization      | Gradio HighlightedText            |

---

## 🔎 Exploratory Data Analysis

As this is a text-based app using dynamic user inputs, there's no static dataset to analyze. However:
- Word count is validated to ensure input suitability
- Entity groups include PERSON, ORG, LOC, and MISC

---

## 🏗️ Feature Engineering

- Preprocessing: Token merging for consistent entity display
- NER: Token-level merging logic to stitch multi-token entities (e.g., "New York City")
- Summary → NER: Summarization precedes entity recognition for cleaner results

---

## 🤖 Modeling

| **Function**           | **Model Used**          |
|------------------------|-------------------------|
| Text Summarization     | `facebook/bart-large-cnn` |
| Named Entity Recognition | `dslim/bert-base-NER`     |

- Evaluation metrics: qualitative review (highlight accuracy, summary clarity)
- Summary generation is followed by entity extraction to improve focus

---

## 📈 Results & Insights

> Example output:
- Summarized a 250-word article to 70 words
- Highlighted 4 organizations and 2 persons
- Displayed structured text with highlights for quick scanning

- **Insight**: This helps users identify the "who", "what", and "where" of a document in seconds.

---

## 📊 Dashboard / Visuals

The application is hosted here:  
🌐 **[AI Summarizer + NER Web App](https://huggingface.co/spaces/banjiola/text_summarization)**

Visual interface powered by **Gradio**  
- Example inputs provided
- Color-coded entity highlights

---

## 🧾 Conclusion

- The app successfully integrates two state-of-the-art models for a seamless user experience.
- Helps various audiences process and understand content faster.
- Real-time feedback via Hugging Face Spaces makes it instantly usable.

---

## 🔄 Next Steps

- Add support for more languages
- Include export feature (PDF/CSV)
- Evaluate and fine-tune models on domain-specific datasets (e.g., legal, medical)

---

## 👨‍💻 Author

**Olabanji Olaniyan**  
Data Scientist & Machine Learning Engineer  

📫 [LinkedIn](https://www.linkedin.com/in/olabanji-olaniyan-59a6b0198/)  
🌐 [Portfolio](https://banjiola.github.io/Olabanji-Olaniyan/)
