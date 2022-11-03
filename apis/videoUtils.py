from flask_restful import Resource
import logging as logger
from flask import request, flash, redirect
import os
import json
from moviepy.editor import VideoFileClip

class VideoUitls(Resource):
    ALLOWED_EXTENSIONS = {'mp4','mov', 'mp3', 'wav'}
    SttModel = {}
    toChunk = False

    def __init__(self):
        print('Inside Video Utils Class')
    
    def get(self):
        ''' Method to handle GET request '''
        
        if "extract" in request.args:
            filename = request.args.get('filename')

            if filename.split('.')[1] == 'wav':
                return {"flag": 1, "filename": filename}
            
            fileformat = '.wav'
            videofilepath = 'static/videos/' + filename
            audiofilepath =  'static/audios/' + filename.split('.')[0] + fileformat
            try:
                video = VideoFileClip(videofilepath)
                audio = video.audio
                rate = video.fps
                audio.write_audiofile(audiofilepath)
                return {"flag": 1, "filename": filename.split('.')[0] + fileformat}
            except Exception as e:
                print(e)
                return {"flag": 0}
        
        elif "chunk" in request.args:
            try:
                from pydub import AudioSegment
                from pydub.silence import split_on_silence
                audiofilepath = 'static/audios/'+request.args.get('filename')
                audio = AudioSegment.from_wav(audiofilepath)
                dBFS = audio.dBFS
                chunks = split_on_silence(audio, min_silence_len = 500, silence_thresh = dBFS-16,keep_silence = 250)
                
                target_length = 300 * 1000 
                output_chunks = [chunks[0]]
                for chunk in chunks[1:]:
                    if len(output_chunks[-1]) < target_length:
                        output_chunks[-1] += chunk
                    else:
                        output_chunks.append(chunk)
                
                for i, chunk in enumerate(output_chunks):
                    chunk.export(
                        "static/chunks/chunk{0}.wav".format(i),
                        bitrate = "192k",
                        format = "wav"
                    )
                totalChunks = i
                return {"flag": 1, "pauses": totalChunks}
            
            except Exception as e:
                print(e)
                return {"flag": 0}

    def post(self):
        ''' Method to handle POST upload '''
        if request.method == 'POST':
            if 'video' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['video']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and self.allowed_file(file.filename):
                print("Filename=>",file.filename)
                filename_converted = file.filename.replace(
                    " ", "-").replace("'", "").lower()
                file.save(os.path.join('static/videos/', filename_converted))
                print("FILE SAVED!")
            
            sttopt = request.form
            self.SttModel = json.loads(sttopt['SttModel'])
            self.toChunk = sttopt['toChunk']
            print(self.SttModel)
            print("Chunk: ", self.toChunk)
            return {"flag": 1, "filename": filename_converted}

        return {"flag": 0}

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
