from flask_restful import Resource
import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask import session, render_template, request
import re

class WatsonSpeechToText(Resource):
    
    STT_API_KEY_ID = ""
    STT_URL = ""

    def __init__(self):
        try:
            with open('static/credentials/speechtotext.json', 'r') as credentialsFile:
                credentials1 = json.loads(credentialsFile.read())
                self.STT_API_KEY_ID = credentials1.get('apikey')
                self.STT_URL = credentials1.get('url')
        except json.decoder.JSONDecodeError:
            print("Speech to text credentials file is empty, please enter the credentials and try again.")
            exit()

        authenticator = IAMAuthenticator(self.STT_API_KEY_ID)
        speech_to_text = SpeechToTextV1(authenticator=authenticator)
        speech_to_text.set_service_url(self.STT_URL)

        ''' Methods for IBM Watson Speech-To-Text '''
        try:
            language_models = speech_to_text.list_language_models().get_result()
            lite = {"name": "Lite version", "customization_id": "lite"}
            language_models["customizations"].insert(0, lite)
        except:
            language_models = {"customizations":[{"name": "Lite version", "customization_id": "lite"}]}

        try:
            acoustic_models = speech_to_text.list_acoustic_models().get_result()
            lite = {"name": "Lite version", "customization_id": "lite"}
            acoustic_models["customizations"].insert(0, lite)
        except:
            acoustic_models = {"customizations":[{"name": "Lite version", "customization_id": "lite"}]}

        self.acousticModel = acoustic_models
        self.languageModel = language_models
        self.speech_to_text = speech_to_text
    
    def get(self, model):
        if model == "acoustic":
            return self.acousticModel
        elif model == "language":
            return self.languageModel
        elif model == "stt":
            toChunk = request.args.get('toChunk')
            langModelId = request.args.get('langModelId')
            acoModelId = request.args.get('acoModelId')
            if toChunk == "True":
                filepath = "static/chunks/"+request.args.get('filename')
            else:
                filepath = "static/audios/"+request.args.get('filename')

            return self.transcribe(filepath, langModelId, acoModelId)
    
    def transcribe(self, audiofilepath, langModelId, acoModelId):
        transcript = ''
        speakerOutput = ''
        finalOutput = []

        try:
            if langModelId == "lite" or acoModelId == "lite":
                speech_recognition_results = self.transcribeLite(audiofilepath)
            else:
                speech_recognition_results = self.transcribePaid(audiofilepath, langModelId, acoModelId)
            
            for chunks in speech_recognition_results['results']:
                print(chunks)
                if 'alternatives' in chunks.keys():
                    alternatives = chunks['alternatives'][0]
                    end_of_utterance = chunks['end_of_utterance']
                    if 'transcript' in alternatives:
                        transcript += alternatives['transcript']
                    
                    if end_of_utterance == "full_stop": 
                        transcript += ".\n"
                    elif end_of_utterance == "silence":
                        transcript += ","
                    elif end_of_utterance == "question_mark":
                        transcript += "?"
                    elif end_of_utterance == "exclamation_mark":
                        transcript += "!"
                    elif end_of_utterance == "end_of_data":
                        transcript += ".\n\n"   

            speakerLabels = speech_recognition_results["speaker_labels"]
            
            extractedData = []
            for i in speech_recognition_results["results"]:
                if i["word_alternatives"]:
                    mydict = {'from': i["word_alternatives"][0]["start_time"], 'transcript': i["alternatives"]
                                [0]["transcript"].replace("%HESITATION", ""), 'to': i["word_alternatives"][0]["end_time"]}
                    mydict["transcript"] = mydict["transcript"] + "."
                    extractedData.append(mydict)

            for i in extractedData:
                for j in speakerLabels:
                    if i["from"] == j["from"] and i["to"] == j["to"]:
                        mydictTemp = {"from": i["from"],
                                        "to": i["to"],
                                        "transcript": i["transcript"],
                                        "speaker": j["speaker"],
                                        "confidence": j["confidence"],
                                        "final": j["final"],
                                        }
                        finalOutput.append(mydictTemp)
            transcript = transcript.replace("%HESITATION", "")
            transcript = transcript.replace(" .", ".")
            transcript = re.sub("(^|[.?!])\s*([a-zA-Z])", lambda p: p.group(0).upper(), transcript)

            for i in finalOutput:
                speakerOutput += "<strong>Speaker {} ({} to {}) </strong>: {}".format(i["speaker"],i["from"], i["to"], i["transcript"])
                speakerOutput += '<br>'
                speakerOutput = speakerOutput.replace(" .", ".")
            return {"transcript": transcript, "speaker": speakerOutput}
        except Exception as e:
            print(e)
            return {"error": "Something went wrong, please try again."}

    def transcribeLite(self, audiofilepath):
        print("Transcribing using lite version")
        with open(audiofilepath, 'rb') as audio_file:
            speech_recognition_results = self.speech_to_text.recognize(
                    audio=audio_file,
                    content_type='audio/wav',
                    model='en-US_NarrowbandModel',
                    keywords=['redhat', 'data and AI', 'Linux', 'Kubernetes'],
                    keywords_threshold=0.5,
                    timestamps=True,
                    speaker_labels=True,
                    word_alternatives_threshold=0.5,
                    end_of_phrase_silence_time=1.0,
                    split_transcript_at_phrase_end=True,
                    smart_formatting=True
                ).get_result()
            
        return speech_recognition_results

    def transcribePaid(self, audiofilepath, langModelId, acoModelId):
        print("Transcribing using Language model {} and Acoustic model {}".format(langModelId, acoModelId))
        with open(audiofilepath, 'rb') as audio_file:
            speech_recognition_results = self.speech_to_text.recognize(
                    audio=audio_file,
                    content_type='audio/wav',
                    model='en-US_NarrowbandModel',
                    keywords=['redhat', 'data and AI', 'Linux', 'Kubernetes'],
                    keywords_threshold=0.5,
                    timestamps=True,
                    speaker_labels=True,
                    customization_id= langModelId,
                    acoustic_customization_id= acoModelId,
                    word_alternatives_threshold=0.9,
                    end_of_phrase_silence_time=1.8,
                    split_transcript_at_phrase_end=True,
                    smart_formatting=True
                ).get_result()
            
        return speech_recognition_results