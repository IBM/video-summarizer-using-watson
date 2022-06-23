from flask_restful import Resource
import json
from flask import request
from summarizer import Summarizer,TransformerSummarizer
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from keybert import KeyBERT

class Summarizer(Resource):

    def __init__(self):
        print('Inside Summarizer Class')

    def get(self):
        pass

    '''Get the summary of the text'''

    def get_summary(self, text, pct):
        summary = summarize(text,ratio=pct,split=True)
        return summary

    '''Get the keywords of the text'''

    def get_keywords(self, text):
        res = keywords(text, ratio=0.1, words=None, split=False, scores=False, pos_filter=None, lemmatize=False, deacc=False)
        res = res.split('\n')
        return res

    def post(self):
        
        if request.method == 'POST':
            text = request.get_json().get('text')

            # Gensim Summarizer
            summary = self.get_summary(text, 0.1)
            keywords = self.get_keywords(text)

            # GPT2 Summarizer
            GPT2_model = TransformerSummarizer(transformer_type="GPT2",transformer_model_key="gpt2-medium")
            GPT2_summary = ''.join(GPT2_model(text, ratio=0.1))

            # XLNET Summarizer
            XLNET_model = TransformerSummarizer(transformer_type="XLNet",transformer_model_key="xlnet-base-cased")
            XLNET_summary = ''.join(XLNET_model(text, ratio=0.1))

            # BERT Summarizer
            kw_model = KeyBERT()
            Bert_keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words=None)
            
            BertNgrams = []
            AdditionalKeywords = []
            
            for keyword in Bert_keywords:
                BertNgrams.append(keyword[0])

            # Additional Insights & Key phrases
            insights = kw_model.extract_keywords(text, keyphrase_ngram_range=(3, 3), stop_words='english', 
                              use_maxsum=True, nr_candidates=20, top_n=10)
            
            for keyword in insights:
                AdditionalKeywords.append(keyword[0])

            keyphrase = kw_model.extract_keywords(text, keyphrase_ngram_range=(3, 3), stop_words='english', 
                              use_mmr=True, diversity=0.8, top_n=10)

            for keyword in keyphrase:
                AdditionalKeywords.append(keyword[0])
            

            return {
                "gensimsSummary":summary,
                "gensimKeywords":keywords,
                "gpt2Summary":GPT2_summary,
                "xlnetSummary":XLNET_summary,
                "bertKeywords":BertNgrams,
                "additionalKeywords": AdditionalKeywords
                }, 200