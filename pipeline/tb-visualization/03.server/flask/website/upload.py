from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from os import path
from website import app
import os
from website import pySQL
import time
import subprocess


@app.route('/upload_data')
def index():
    if pySQL.existRunning():
        run_id= pySQL.existRunning()
        basepath = '/root/pipeline/tb-visualization/04.variant_calling/05.sample_proprocessing/'
        for id in run_id:
            status_dir = basepath+str(id[0])+'/status'
            if os.path.exists(status_dir):
                f = open(status_dir, 'r')
                status = f.read()
                if status =='error\n':
                    pySQL.updatetable(id[0],'error')
                elif status =='finished\n':
                    pySQL.updatetable(id[0],'finished')
    data=pySQL.table2output()
    return render_template('select_sample.html', data=data)


@app.route("/", methods=['GET', 'POST'])
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        sample_id = request.form.get('sample_id')
        left_file = request.files['left_file']
        right_file = request.files['right_file']
        left_name = secure_filename(left_file.filename)
        right_name = secure_filename(right_file.filename)
        if (len(sample_id) == 0 or secure_filename(left_file.filename) == '' or secure_filename(left_file.filename) == ''):
            return render_template('index.html', msg='Missing necessary information!  Please re-upload.')
        elif (left_name.rsplit('.', 1)[1] not in ['gz', 'fq']) or (right_name.rsplit('.', 1)[1] not in ['gz', 'fq']):
            return render_template('index.html', msg='File extension is limited to ".gz" or "fq"')
        elif pySQL.isrepeatSampleid(sample_id):
            return render_template('index.html', msg='File corresponding to this sample-iD has been uploaded ! ')
        else:
            basepath = '/root/pipeline/tb-visualization/02.data'
            left_file.save(os.path.join(basepath, left_name))
            right_file.save(os.path.join(basepath, right_name))
            pySQL.input2mysql(sample_id, left_name,right_name, 'submitted')
            return redirect(url_for('index'))
    return render_template('index.html', msg='Please wait after submision ')





@app.route('/analysis', methods=['POST'])
def analysis():
    data = pySQL.table2output()
    idlist = (request.form.getlist('check'))
    if idlist == []:
        return render_template('select_sample.html',msg='Please input at least one item !',data=data)
    else:
        sampleID = []
        leftfile_name = []
        rightfile_name = []
        for id in idlist:
            if pySQL.isrepeatID(id):
                return render_template('select_sample.html', data=data, msg='Selected sample has been analyzed,!  Please select another ' )
            input = pySQL.select_info(id)  
            sampleID.append(input[0])
            leftfile_name.append(input[1][0][0])
            rightfile_name.append(input[1][0][1])
            pySQL.updatetable(id,'running')
            # time.sleep(5)
            # pySQL.updatetable(id,'finished')
            # for i in ['X', 'Y', 'Z']:
            #     pySQL.inputmysql(id, i, 'A')
        a=str(idlist).replace('[','').replace(']','').replace("'",'')
        b=str(leftfile_name).replace('[','').replace(']','').replace("'",'')
        c=str(rightfile_name).replace('[','').replace(']','').replace("'",'')
        subprocess.Popen(["/bin/bash","/root/pipeline/tb-visualization/04.variant_calling/wgs_to_format_data.sh",a,b,c])
        data = pySQL.table2output()
        return render_template('select_sample.html', data=data)

@app.route('/delete_sample',methods=['POST'])
def delete():
    data = pySQL.table2output()
    idlist = (request.form.getlist('check'))
    if idlist == []:
        return render_template('select_sample.html', msg=' No sample selected! ', data=data)
    else:
        for id in idlist:
            pySQL.delete_sample(id)
    data = pySQL.table2output()
    return render_template('select_sample.html', msg='Complete deletion ', data=data)


@app.route('/result')
def result():
    id = request.args.get('sn')
    sample_id = pySQL.ID2SampleID(id)
    #data = pySQL.table2outputByID(id)
    data = []
    file_path = '/root/pipeline/tb-visualization/05.drug_resistance_prediction/'+id
    if (os.path.exists(file_path)):
        with open(file_path,'rt',encoding='utf-8') as f:
            lines = f.readlines()
        for i in lines:
            data.append(i.strip().split(','))
    return render_template('tables.html', data=data,sample_id=sample_id)


