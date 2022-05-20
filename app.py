import os
import shutil
import cv2
import matplotlib.pyplot as plt
from flask import Flask, redirect, url_for, request, flash
from flask import *
from flask import render_template
from flask import send_file
import numpy as np
from numpy import asarray
from numpy import savetxt
from matplotlib.path import Path


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "abc" 

@app.route('/',methods = ['GET', 'POST'])
def index():
    app.config["LABELS"] = []
    app.config["MASK"] = []
    app.config["HEAD"] = 0
    session['overlay_status'] = True
    if request.method == 'POST':
        try:
            shutil.rmtree('./images')
        except:
            pass
        os.mkdir('./images')
        try:
            shutil.rmtree('./download')
        except:
            pass
        os.mkdir('./download')
 
        files = request.files.getlist("file")
        if (files[0].filename == ''):
            flash('No files selected')
            return redirect('/') 
        for f in files:
            f.save(os.path.join('./images', f.filename))
        for (dirpath, dirnames, filenames) in os.walk(app.config["IMAGES"]):
            files = filenames
            break
        app.config["FILES"] = files
        '''
        try:
            shutil.rmtree('./overlays')
        except:
            pass
        os.mkdir('./overlays')
        
        overlays = request.files.getlist("ov_file")
        if(overlays[0].filename == ''):
            session['overlay_status'] = False

        if(session['overlay_status'] == True):
            for x in overlays:
                x.save(os.path.join('./overlays', x.filename))
            for (dirpath, dirnames, filenames) in os.walk(app.config["OVERLAYS"]):
                overlays = filenames
                break
            app.config["OV_FILES"] = overlays
    '''
        return redirect('/tagger',  code=302)
        #go to tagger after completing upload
    else:
        return render_template('index.html')




@app.route('/tagger')
def tagger():
 
    directory = app.config["FILES"]
    image = app.config["FILES"][app.config["HEAD"]]

    '''
    if(session['overlay_status'] == True):
        over_image = app.config["OV_FILES"][app.config["HEAD"]]
    else:
        over_image = image
    '''
    labels = app.config["LABELS"]
    masks = app.config["MASK"]
    not_end = not(app.config["HEAD"] == len(app.config["FILES"]) - 1)
    first = (app.config["HEAD"] == 0)
    

    #for buttons to determine if user is drawing box or custom shape
    is_box = True
    return render_template('tagger.html', overlay_status = session['overlay_status'],
    first=first, is_box = is_box, not_end=not_end,masks=masks, directory=directory, image=image, labels=labels, head=app.config["HEAD"] + 1, len=len(app.config["FILES"]))

@app.route('/next')
def next():
    app.config["HEAD"] = app.config["HEAD"] + 1
         
    #shutil.rmtree('./download')
    #os.mkdir('./download')
    app.config["LABELS"] = []
    app.config["MASK"] = []
    return redirect(url_for('tagger'))

@app.route('/prev')
def prev():
    app.config["HEAD"] = app.config["HEAD"] - 1
    app.config["LABELS"] = []
    app.config["MASK"] = []

    #shutil.rmtree('./download')
    #os.mkdir('./download')
    return redirect(url_for('tagger'))

def comma_separated_params_to_list(param):
    result = []
    pair = False
    for val in param.split(','):
        if val and pair:
            result.append((int(temp), int(val)))
            pair = False
        else:
            temp = val
            pair = True
        
    return result

@app.route('/addmask/<id>')
def addmask(id):
    ptList = request.args.getlist('ptList')
    app.config["WIDTH"] = request.args.get("Wid")
    app.config["HEIGHT"] = request.args.get("Hei")
    request_data = {}
    if len(ptList) == 1 and ',' in ptList[0]:
        request_data['status'] = comma_separated_params_to_list(ptList[0])
    else:
        request_data['status'] = ptList
    #arr = np.array(request_data["status"])
    #equivalent of label array
    app.config["MASK"].append({"id":id, "name":"", "arr": request_data["status"]})
    
    return redirect(url_for('tagger'))

@app.route('/add/<id>')
def add(id):
    xMin = request.args.get("xMin")
    xMax = request.args.get("xMax")
    yMin = request.args.get("yMin")
    yMax = request.args.get("yMax")
    app.config["LABELS"].append({"id":id, "name":"", "xMin":xMin, "xMax":xMax, "yMin":yMin, "yMax":yMax})
    
    #app.config["LABELS_SINGLE"][id].append({"id":id, "name":"", "xMin":xMin, "xMax":xMax, "yMin":yMin, "yMax":yMax})
    return redirect(url_for('tagger'))

@app.route('/remove/<id>')
def remove(id):
    index = int(id) - 1
    del app.config["LABELS"][index]
    for label in app.config["LABELS"][index:]:
        label["id"] = str(int(label["id"]) - 1)
    return redirect(url_for('tagger'))

@app.route('/removemask/<id>')
def removemask(id):
    index = int(id) - 1
    del app.config["MASK"][index]
    if len(app.config["MASK"]) > 0:
        for x in app.config["MASK"][index:]:
            x["id"] = str(int(x["id"]) - 1)
    return redirect(url_for('tagger'))

@app.route('/label/<id>')
def label(id):
    name = request.args.get("name")
    app.config["LABELS"][int(id) - 1]["name"] = name
    return redirect(url_for('tagger'))

@app.route('/mask/<id>')
def mask(id):
    name = request.args.get("name")
    app.config["MASK"][int(id) - 1]["name"] = name
    return redirect(url_for('tagger'))

@app.route('/image/<f>')
def images(f):
    images = app.config["IMAGES"]
    return send_file(images +'/'+f)

@app.route('/overlay/<f>')
def overlays(f):
    overlays = app.config["OVERLAYS"]
    return send_file(overlays +'/'+f)

@app.route('/download')
def download():
    image = app.config["FILES"][app.config["HEAD"]]
    with open(app.config["OUT"],'a') as f:
        for label in app.config["LABELS"]:
            f.write(image + "," +
            label["id"] + "," +
            label["name"] + "," +
            str(round(float(label["xMin"]))) + "," +
            str(round(float(label["xMax"]))) + "," +
            str(round(float(label["yMin"]))) + "," +
            str(round(float(label["yMax"]))) + "\n")
    '''
    x, y = np.meshgrid(np.arange(int(app.config["HEIGHT"])), np.arange(int(app.config["WIDTH"])))
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x,y)).T 
    p = Path(app.config["MASK"]) # make a polygon
    grid = p.contains_points(points)
    '''
    if(len(app.config["MASK"]) > 0):
        mask = np.zeros((int(app.config["HEIGHT"]), int(app.config["WIDTH"])), dtype=np.int8)
        for x in app.config["MASK"]:
            cv2.fillConvexPoly(mask, np.array(x["arr"]), 1)
        savetxt('data.csv', mask, delimiter=',')
    
    #plt.imsave('filename.jpeg', mask)
    if(len(app.config["MASK"]) > 0 and len(app.config["LABELS"]) > 0):
        shutil.copyfile('data.csv', 'download/mask.csv')
        shutil.copyfile('out.csv', 'download/boxes.csv')
        shutil.make_archive(image + '_annotations', 'zip', 'download')
        return send_file( image + '_annotations.zip',
                     mimetype='text/csv',
                     attachment_filename=image + '_annotations.zip',
                     as_attachment=True)
    elif(len(app.config["MASK"]) == 0 and len(app.config["LABELS"]) != 0):
        shutil.copyfile('out.csv', 'download/' + image + '_boxes.csv')
        return send_file('download/' + image + '_boxes.csv',
                     mimetype='text/csv',
                     attachment_filename=image + '_boxes.csv',
                     as_attachment=True)
    elif(len(app.config["LABELS"]) == 0 and len(app.config["MASK"]) != 0):
        shutil.copyfile('out.csv', 'download/' + image + '_mask.csv')
        return send_file( 'download/' + image + '_mask.csv',
                     mimetype='text/csv',
                     attachment_filename=image + '_mask.csv',
                     as_attachment=True)
    else:
        return
        


if __name__ == "__main__":
    app.config["OVERLAYS"] = 'overlays'
    app.config["IMAGES"] = 'images'
    app.config["LABELS"] = []
    app.config["MASK"] = []
    app.config["HEAD"] = 0
    app.config["OUT"] = "out.csv"
    with open("out.csv",'w') as f:
        f.write("image,id,name,xMin,xMax,yMin,yMax\n")
    app.run(debug="True")
