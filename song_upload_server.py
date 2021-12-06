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
from pathlib import Path
import pydub
from pydub import AudioSegment
from IPython.display import Audio
import numpy as np
import scipy as sp
import soundfile as sf
import scipy.signal
from scipy.io.wavfile import write
import os.path
import time


# from spleeter.separator import Separator


app = Flask(__name__, static_folder='static')
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'pretty secret key'
UPLOAD_FOLDER = './static/audio_uploads'
STEMS_FOLDER = './static/stems'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STEMS_FOLDER'] = STEMS_FOLDER
dev_mode = 'TRUE'
#print("fn ",Flask(__name__))

@app.route("/")
def landing():
    return render_template("landing.html")
# @app.route('/api/<filepath>/')
# def api_get_filepath(filepath):
#     return json.jsonify({
#         'filepath': filepath
#     })

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

    # return render_template('play_audio.html',filename=filePath)



    # subprocessCommand = "spleeter separate -p spleeter:4stems -o output/ "
    # print(filePath)
    # print(subprocessCommand+filePath)
    # subprocess.run(subprocessCommand+filePath)

    # if __name__ == "__main__":   
    #     separator = Separator('spleeter:2stems')
    #     separator.separate_to_file(filePath, outputPath)
    #     print('sep is running')

    # print('subprocess is done now')
# @app.route("/change_audio")
# def change_audio(filePath, sample):
#     return filePath, sample

# @app.route('/<path:filename>')
@app.route('/audio_file_name')
def returnAudioFile(filename):
    path_to_audio_file = filename
    return send_file(
         path_to_audio_file, 
         mimetype="audio/wav", 
         as_attachment=True, 
         attachment_filename="test.wav")

@app.route('/audio_upload', methods=['GET', 'POST'])
def audio_upload():
    return render_template('upload.html')


@app.route("/")
def landing_load():
    return render_template("landing.html")


@app.route("/edu")
def edu():
    return render_template("edu.html")


@app.route('/<path:filename>')
def serve_static(filename):
    print("static serving filename:", filename)

    print('serving static')
    root_dir = app.root_path
    print("root ",root_dir,app.root_path,app.instance_path)
    filedir = os.path.join(root_dir, 'static/')
    print("filedir: ",filedir, " filename: ", filename)
    # convert the thing from dict if it is an audio file lol
    # return send_from_directory(os.path.join(root_dir, 'static/'), filename)
    # if "wav" in filename:
    #     print('hehe this is a wav file')
    #     return send_from_directory(app.static_folder,"static/bin_skiles_film_room.wav")

    print(app.static_folder)
    return send_from_directory(app.static_folder, filename)


# @app.route('/play_audio')
# def play_audio():
#     return render_template('play_audio.html')
@app.route('/submit_form', methods = ['POST','GET'])
def submitForm():
    selectedFreq = request.form.get('goals')
    print('selected a freq: ',selectedFreq)
    return selectedFreq

# def getGoals():
#     return("delta", "theta","alpha","beta","gamma")
# def template(text=""):
#     templateDate = {
#         'text': text,
#         'goals': getGoals(),
#         'selected_goal' : -1
#     }
#     return templateDate

x = None
@app.route('/goal_process', methods=['POST','GET'])
def goal_process(tf=True):
    global x
    band = 0
    print('i goal process ruan')
    if tf: 
        if request.method == 'POST':
            goal = (request.form['goals'])
            band=goal
            # band = request.form.get('goals')
            print("band: ", band)
            x = band
            return x
    else:
        return x
    
    

    # templateData = template(text="")
    # templateData['selected_goal'] = goal
    # band = request.form.get('goals')

    # print("band: ", band)
    # return band

@app.route('/save_audio', methods=['POST','GET'])
def save_audio():
    print("\nra",request.form,request.data,request.files,app.config)

    file_name = request.form.get('fname')
    band = goal_process(False)
    # if request.method == 'POST':
    #     goal = (request.form['goals'])
    #     band=goal
    #     # band = request.form.get('goals')
    #     print("band: ", band)
    # templateData = template(text="")
    # templateData['selected_goal'] = goal
    # # band = request.form.get('goals')

    print("band: ", band)
# do a lil switch statement here
    freqShift = 0
    if band == "Sleep":
        freqShift = 2
    elif band == "Meditation":
        freqShift = 6
    elif band =="Stress":
        freqShift=10
    elif band=="Focus":
        freqShift=20
    elif band=="Memory":
        freqShift=30
    else:
        freqShift = 2

    print(freqShift)

    if file_name is None:
        # this saves audio files into the "audio_uploads" folder. we will need to delete these in a cache on the webhosting possibly but for now it works fine
        audio_file = request.files['audio']
        print('audiofile: ', audio_file.filename)
        print('newaudiofile: ', audio_file.filename.replace(" ","_").replace(".","_",audio_file.filename.count(".")-1))

        file_id=audio_file.filename.replace(" ","_").replace(".","_",audio_file.filename.count(".")-1)

        # file_path = UPLOAD_FOLDER + "/" + file_id
        # output_path = STEMS_FOLDER + "/" + file_id
        # orig_file_path = "static/audio_uploads/"+file_id
        orig_file_path = "static/"+file_id

        print("file path: ", orig_file_path)
        # print("output path", output_path)
        audio_file.save(orig_file_path)   

        # convert file to wav for future use
        if ".mp3" in orig_file_path:
            print('yes there is mp3 here')
            sound = AudioSegment.from_mp3(orig_file_path)
            sound.export(orig_file_path.replace(".mp3",".wav"), format="wav")
            file_id = file_id.replace(".mp3",".wav")
            orig_file_path = orig_file_path.replace(".mp3",".wav")


        separate_stems(orig_file_path, file_id)
        name_of_file=file_id.split(".")[0]
        bass_path = 'separated/mdx_q/'+ name_of_file + '/bass.wav'

        binauralized_file_id = "bin_"+file_id
        print("binauralized file id: ", binauralized_file_id)
        stereo,sr=binauralizer(freqShift,high,bass_path,orig_file_path)
        binauralized_file_path = 'static/' + binauralized_file_id

        sf.write(binauralized_file_path,stereo,sr)

        time.sleep(10)
        # renders template with file id and not file path because they are all in static and otherwise it gets messy
        return render_template('play_audio.html', file_path=binauralized_file_id)         
        

    
    # return render_template('play_audio.html', file_path=binauralized_file_path)





#reading in stems from demucs separation

def binauralizer_definitions(path_to_bass,path_to_orig):
    [stem,sr1] = librosa.load(path_to_bass)        #### path for bass stem
    [original,sr2] = librosa.load(path_to_orig)                #### path for whole song

    #lowpass filter to remove extraneous signal noise
    lowpass = scipy.signal.butter(2, 5000, 'lowpass', fs=sr1, output='sos')
    filtered = scipy.signal.sosfilt(lowpass, stem)
    return filtered, original,sr1

#freq shift
def nextpow2(x):
    return int(np.ceil(np.log2(np.abs(x))))            #### for zero padding inside freq_shift function

def freq_shift(x, f_shift, dt):                        #### frequency shifting function
    print("f_shift: ", f_shift)
    N_orig = len(x)
    N_padded = 2**nextpow2(N_orig)                     #### zero padding
    t = np.arange(0, N_padded)
    return (scipy.signal.hilbert(np.hstack((x, np.zeros(N_padded-N_orig, x.dtype))))*np.exp(2j*np.pi*f_shift*dt*t))[:N_orig].real

dt = 1/44100
fs = 1/dt
T = 1.0
t = np.arange(0, T, dt)
N = len(t)


# individual frequency bands
delta = 2
theta = 6
alpha = 10
beta = 20
gamma = 30

# volume levels
low = 0.6
medium = 0.9
high = 1.2


def binauralizer(band,gain=1, path_to_bass=1, path_to_orig=1):           #### creates stereo signal, each channel mixed with original audio for sound quality
    stem,original,sr = binauralizer_definitions(path_to_bass,path_to_orig)
    leftear = stem * gain
    leftear = original + leftear
    shift = freq_shift(stem,band,dt)
    rightear = shift * gain
    rightear = original + rightear
    stereo = np.vstack([leftear,rightear])
    stereo = np.transpose(stereo)
    return stereo,sr

#testcase   
# stereo,sr=binauralizer(alpha,high,path_to_bass,path_to_orig)
# write("stereo.wav",sr,stereo)






if __name__ == '__main__':
    #app = Flask(__name__)
    #sess = Session()
    if dev_mode == 'TRUE':
        app.run(host='0.0.0.0',port=8100,debug=True)
    else:
        app.run()
        
   

            
