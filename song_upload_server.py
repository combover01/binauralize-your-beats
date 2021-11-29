from __future__ import unicode_literals
from flask import Flask, jsonify, render_template, request,json,send_from_directory, flash, url_for, redirect, session,send_file,redirect
from flask_wtf import FlaskForm
from wtforms import SelectField,HiddenField,SubmitField,FieldList,FormField
import librosa
import ffmpeg
import os
import subprocess
from functools import wraps
from wtforms import Form, BooleanField, TextField, PasswordField, validators,RadioField
import gc
import math
import requests
import sys,traceback
# import spleeter
import pydub
from pydub import AudioSegment
# from spleeter.separator import Separator


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'pretty secret key'
UPLOAD_FOLDER = './static/audio_uploads'
STEMS_FOLDER = './static/stems'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STEMS_FOLDER'] = STEMS_FOLDER
dev_mode = 'TRUE'
#print("fn ",Flask(__name__))


def separate_stems(filePath,fileName):
    print("\nseparating stems")
    # sep = Separator('spleeter:2stems')
    print("separator ran")
    # sep.separate_to_file(file_path,output_path,codec='mp3')
    print("we do be having issues if this doesnt show")

    outputPath = "static/stems/" + fileName

    print(filePath)

    # WE USE SUBPROCESS NOW::

    demucsCommand = "demucs -d cpu -n mdx_q "

    subprocess.run(demucsCommand+filePath)




    # subprocessCommand = "spleeter separate -p spleeter:4stems -o output/ "
    # print(filePath)
    # print(subprocessCommand+filePath)
    # subprocess.run(subprocessCommand+filePath)

    # if __name__ == "__main__":   
    #     separator = Separator('spleeter:2stems')
    #     separator.separate_to_file(filePath, outputPath)
    #     print('sep is running')

    # print('subprocess is done now')

@app.route('/audio_upload')
def midi_upload():
    song_id = request.args.get('song_id')
    # song_id = song_id.replace(" ","_")
    return render_template('audio_upload.html',song_id=song_id)
@app.route('/<path:filename>')
def serve_static(filename):
    print('serving static')
    root_dir = app.root_path
    print("root ",root_dir,app.root_path,app.instance_path)
    filedir = os.path.join(root_dir, 'static/')
    print(filedir,filename)
    return send_from_directory(os.path.join(root_dir, 'static/'), filename)


@app.route('/play_audio')
def play_audio():
    return render_template('play_audio.html')

@app.route('/save_audio',methods=['GET','POST'])
def save_audio():
    print("\nra",request.form,request.data,request.files,app.config)
    # save_fn = 'test.mid'
    # dict = request.files
    
    # print('\nrequestfiles: ', dict['audio'])
    # print('\nrequestfilesget: ', dict['audio'])
    file_name = request.form.get('fname')
    
    if file_name is None:
        # this saves audio files into the "audio_uploads" folder. we will need to delete these in a cache on the webhosting possibly but for now it works fine
        audio_file = request.files['audio']
        print('audiofile: ', audio_file.filename)
        print('newaudiofile: ', audio_file.filename.replace(" ","_"))

        file_id=audio_file.filename.replace(" ","_")
        # file_path = UPLOAD_FOLDER + "/" + file_id
        # output_path = STEMS_FOLDER + "/" + file_id
        file_path = "static/audio_uploads/"+file_id

        print("file path: ", file_path)
        # print("output path", output_path)
        audio_file.save(file_path)   

        separate_stems(file_path, file_id)

        # separate the audio into 1 minute chunks to send to spleeter to avoid memory errors.
        # FOR MP3:

        # if (file_id[-3:] == "mp3"):
        #     originalFile = AudioSegment.from_mp3(file_path)
        #     length = len(originalFile)
        #     print(length)
            
            # get number of minutes rounded up to loop the audio file splitter and then spleeter
        #     numMinLoops = math.ceil(length/60000)
        #     print(numMinLoops)
        #     for n in range(numMinLoops):
        #         # t1 = n*60000
        #         t1 = n*60000
        #         t2 = t1+60000
        #         print("hello "+ str(n))
        #         newAudio = originalFile[t1:t2]
        #         newAudio.export("static/segments/section" + str(n) + ".wav", format="wav")
        #         cur_file_path = "static/segments/section" + str(n) + ".wav"
        #         separate_stems(cur_file_path,"section" + str(n)+".wav")






        # if (file_id[-3:] == "wav"):
        #     originalFile = AudioSegment.from_wav(file_path)
        #     length = len(originalFile)
        #     print(length)
            
        #     # get number of minutes rounded up to loop the audio file splitter and then spleeter
        #     numMinLoops = math.ceil(length/60000)
        #     print(numMinLoops)
        #     for n in range(numMinLoops):
        #         t1 = n*60000
        #         t2 = t1+60000
        #         print("hello "+ str(n))
        #         newAudio = originalFile[t1:t2]
        #         newAudio.export("static/segments/section" + str(n) + ".wav", format="wav")
        #         cur_file_path = "static/segments/section" + str(n) + ".wav"
        #         separate_stems(cur_file_path,"section" + str(n)+".wav")
        
        # separate_stems(file_path,file_id)


    return render_template('play_audio.html',filename='/static/audio_uploads/hooch.wav')


if __name__ == '__main__':
    #app = Flask(__name__)
    #sess = Session()
    if dev_mode == 'TRUE':
        app.run(host='0.0.0.0',port=8100,debug=True)
    else:
        app.run()
        
   

            
