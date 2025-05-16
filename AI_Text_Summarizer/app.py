# An AI web application for Text Summarization and Named Entity Recognition
# Developer: Olabanji Olaniyan

# Import Necessary Libraries
import requests, json
import os
from dotenv import load_dotenv, find_dotenv
import gradio as gr



# reads local .env file
_ = load_dotenv(find_dotenv())

# load api key and endpoints
hf_api_key = os.environ['HUGGINGFACEHUB_API_TOKEN'] # This should not be hardcoded
sum_endpoint = os.environ["API_URL_SUMMARIZE"] # summarization endpoint
ner_endpoint = os.environ["API_URL_NER"] # named entity recognization endpoint



# Examples for app
example_1 = '''Andrew Yan-Tak Ng (Chinese: 吳恩達; born April 18, 1976[2]) is a British-American computer scientist and technology entrepreneur focusing on machine learning and artificial intelligence (AI).Ng was a cofounder and head of Google Brain and was the former Chief Scientist at Baidu, building the company's Artificial Intelligence Group into a team of several thousand people. Ng is an adjunct professor at Stanford University (formerly associate professor and Director of its Stanford AI Lab or SAIL). Ng has also worked in the field of online education, cofounding Coursera and DeepLearning.AI. He has spearheaded many efforts to "democratize deep learning" teaching over 8 million students through his online courses. Ng is renowned globally in computer science, recognized in Time magazine's 100 Most Influential People in 2012 and Fast Company's Most Creative People in 2014. His influence extends to being named in the Time100 AI Most Influential People in 2023. In 2018, he launched and currently heads the AI Fund, initially a $175-million investment fund for backing artificial intelligence startups. He has founded Landing AI, which provides AI-powered SaaS products. On April 11, 2024, Amazon announced the appointment of Ng to its board of directors.'''
example_2 = """Lionel Andrés "Leo" Messi; born 24 June 1987) is an Argentine professional footballer who plays as a forward for and captains both Major League Soccer club Inter Miami and the Argentina national team. Widely regarded as one of the greatest players of all time, Messi set numerous records for individual accolades won throughout his professional footballing career such as eight Ballon d'Or awards and eight times being named the world's best player by FIFA. He is the most decorated player in the history of professional football having won 45 team trophies, including twelve Big Five league titles, four UEFA Champions Leagues, two Copa Américas, and one FIFA World Cup. Messi holds the records for most European Golden Shoes (6), most goals in a calendar year (91), most goals for a single club (672, with Barcelona), most goals (474), hat-tricks (36) and assists (192) in La Liga, most assists (18) and goal contributions (32) in the Copa América, most goal contributions (21) in the World Cup, most international appearances (191) and international goals (112) by a South American male, and the second-most in the latter category outright. A prolific goalscorer and creative playmaker, Messi has scored over 850 senior career goals and has provided over 380 assists for club and country"""

# function to get a response from our endpoint. The default is summarization endpoint
def get_completion(inputs, parameters=None,ENDPOINT_URL=sum_endpoint): 
    """
    This function sends a POST request to a Hugging Face Inference API endpoint and returns the model's output.

    Args:
        inputs (str): The input text to be processed by the model (e.g., for summarization, translation, etc.)
        
        parameters (dict, optional): Additional generation parameters for the model, such as: ### Although it was not used in this program ###
            - max_length (int): Maximum length of the generated text.
            - min_length (int): Minimum length of the generated text.
            - do_sample (bool): Whether or not to use sampling; use greedy decoding otherwise.

        ENDPOINT_URL (str, optional):The URL of the Hugging Face model API endpoint. Defaults to `sum_endpoint`.

    Returns:
        dict: A dictionary parsed from the JSON response of the API. This is our selected model's output.
        For example: if our `ENDPOINT_URL` is a summarization endpoint then the output is:
        summarization [{summary_text: "The summary of your text"}]
        
    """


    headers = {
      "Authorization": f"Bearer {hf_api_key}",
      "Content-Type": "application/json"
    }
    data = { "inputs": inputs }
    if parameters is not None:
        data.update({"parameters": parameters})
    response = requests.request("POST",
                                ENDPOINT_URL, headers=headers,
                                data=json.dumps(data)
                               )
    return json.loads(response.content.decode("utf-8"))


# for named entity recognition
def merge_tokens(tokens):
    """
    This function is to clean the inside token of an entity group
    """
    merged_tokens = []
    for token in tokens:
        # entity_group
        if merged_tokens and token['entity_group'].startswith('I-') and merged_tokens[-1]['entity_group'].endswith(token['entity_group'][2:]):
            # If current token continues the entity of the last one, merge them
            last_token = merged_tokens[-1]
            last_token['word'] += token['word'].replace('##', '')
            last_token['end'] = token['end']
            last_token['score'] = (last_token['score'] + token['score']) / 2
        else:
            # Otherwise, add the token to the list
            merged_tokens.append(token)

    return merged_tokens

# for named input recognition
def ner(input):
    output = get_completion(input, parameters=None, ENDPOINT_URL=ner_endpoint)
    merged_tokens = merge_tokens(output)
    return {"text": input, "entities": merged_tokens}


# This function combines the named entity recognition and summarization pipeline
def summarize_ner(text): # I implemented the validation step here because the model behaves weirdly for text of smaller words
    """
    This function receives a text. It ensures the text is greater than 100 in length then passes our summarization and ner functions.

    Args:
        text (str): Text.

    Returns:
        str: Summarized text with named entity group.
    """
    word_count = len(text.split())
    if word_count <100:
        return "⚠️ Please enter at least 100 words."
    else:
        summarized = get_completion(text)
        # remember I don't have to define a summarization function because the default mode is summarization
        summarized = summarized[0]['summary_text']
        # let's perform ner on the summarized text
        output = ner(summarized)
        return output



demo = gr.Interface(fn=summarize_ner,
                    inputs=[gr.Textbox(label="Text to Summarize and find entities",
                                        lines=10,
                                        placeholder= "Enter or Paste Text here"
                                        )],
                    outputs=[gr.HighlightedText(label="Text with entities",
                                                show_legend=True,
                                                color_map={"PER": "#ff9aa2", "ORG": "#ffdac1", "LOC": "#e2f0cb", 'MISC': "#b5ead7"}
        
                                                )],
                    title="AI Text Summarizer",
                    description= """<div class="header-text">
                    <h3>Generate concise summaries and highlight key entities</h3>
                    <p>This tool helps you generate quick summaries from long-form text and highlights named entities such as <mark>people</mark>, <mark>organisations</mark>, and <mark>locations</mark>. The following models were used: the <code>bart-large-cnn</code> model for text summarisation and the <code>dslim/bert-base-NER</code> model for named entity recognition.</p></div>
                    
                    <p>This web application is an implementation of Text Summarization and Named Entity Recognition. <b><i>Click the example below to see it in action or paste your text.</b></i></p>
                    """,
                    flagging_mode="never",
                    examples= [example_1, example_2],    
                    theme= 'soft',
                    article="""<p style='text-align: center'><i>Developed by <a href="https://banjiola.github.io/Olabanji-Olaniyan/" 
                    target="_blank">Olabaji Olaniyan</a> © 2025</i></p>"""
                    )

if __name__ == "__main__":
    demo.launch()
