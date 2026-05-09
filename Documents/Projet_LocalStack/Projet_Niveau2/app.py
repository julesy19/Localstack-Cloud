from flask import Flask, render_template, request, redirect, send_file
import boto3
import os

app = Flask(__name__)

BUCKET_NAME = "babadiamas3"

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4666',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

@app.route('/')
def index():

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    files = []

    if 'Contents' in response:

        for obj in response['Contents']:

            filename = obj['Key']

            files.append({
                "name": filename,
                "is_image": filename.lower().endswith(
                    ('.png', '.jpg', '.jpeg', '.gif')
                )
            })

    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():

    files = request.files.getlist("file")

    for file in files:

        if file.filename != '':
            s3.upload_fileobj(file, BUCKET_NAME, file.filename)

    return redirect('/')

@app.route('/download/<filename>')
def download(filename):

    local_path = f"/tmp/{filename}"

    s3.download_file(BUCKET_NAME, filename, local_path)

    return send_file(local_path, as_attachment=True)

@app.route('/delete/<filename>')
def delete(filename):

    s3.delete_object(Bucket=BUCKET_NAME, Key=filename)

    return redirect('/')

@app.route('/image/<filename>')
def image(filename):

    local_path = f"/tmp/{filename}"

    s3.download_file(BUCKET_NAME, filename, local_path)

    return send_file(local_path)

if __name__ == '__main__':
    app.run(debug=True)
