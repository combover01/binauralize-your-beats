from __future__ import unicode_literals
from flask import Flask, jsonify, render_template, request,json,send_from_directory, flash, url_for, redirect, session,send_file,redirect
from flask_wtf import FlaskForm
from wtforms import SelectField,HiddenField,SubmitField,FieldList,FormField
import pretty_midi
import librosa
import os
import subprocess
from functools import wraps
from wtforms import Form, BooleanField, TextField, PasswordField, validators,RadioField
import gc
import requests
import sys,traceback


midipitches = ['C','C#','D','Eb','E','F','F#','G','G#','A','Bb','B']
 

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'pretty secret key'
UPLOAD_FOLDER = './static/audio_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
dev_mode = 'TRUE'
#print("fn ",Flask(__name__))

@app.route('/audio_upload')
def midi_upload():
    song_id = request.args.get('song_id')
    return render_template('audio_upload.html',song_id=song_id)
@app.route('/<path:filename>')
def serve_static(filename):
    root_dir = app.root_path
    print("root ",root_dir,app.root_path,app.instance_path)
    print(os.path.join(root_dir, 'static/'), filename)
    return send_from_directory(os.path.join(root_dir, 'static/'), filename)
@app.route('/play_audio')
def play_audio():
    return render_template('play_audio.html')
@app.route('/save_audio',methods=['GET','POST'])
def save_audio():
    print("ra",request.form,request.data,request.files,app.config)
    save_fn = 'test.mid'
    file_name = request.form.get('fname')
    
    if file_name is None:
        audio_file = request.files['audio']
        print("path",os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename))
        audio_file.save(os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename))
    
    #nbr_parts = len(midi_stream.getElementsByClass(music21.stream.Part)) 
    return render_template('play_audio.html',filename=os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename))
    

if __name__ == '__main__':
    #app = Flask(__name__)
    #sess = Session()
    if dev_mode == 'TRUE':
        app.run(host='0.0.0.0',port=8000,debug=True)
    else:
        app.run()
        
   

            
