import os
from os.path import basename
import shutil
from flask import Blueprint, request, current_app
from flask.helpers import url_for
from helpers import get_secure_filename_filepath
from werkzeug.utils import redirect
from PIL import Image
from datetime import datetime
from zipfile import ZipFile

bp = Blueprint('android', __name__, url_prefix='/android')


ICON_SIZES = [29, 40, 57, 58, 60, 80, 87, 114, 120, 180, 1024]

@bp.route('/', methods=["POST"])
def create_images():
    filename = request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename)

    tempfolder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp')
    os.makedirs(tempfolder)

    for size in ICON_SIZES:
        outfile = os.path.join(tempfolder, f'{size}.png')
        image = Image.open(filepath)
        out = image.resize((size, size))
        out.save(outfile, 'PNG')

    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).rsplit('.')[0]
    zipfilename = f'{timestamp}.zip'
    zipfilepath = os.path.join(current_app.config['UPLOAD_FOLDER'], zipfilename)

    with ZipFile(zipfilepath, 'w') as zipobj:
        for foldername, subfolders, filenames, in os.walk(tempfolder):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                zipobj.write(filepath, basename(filepath))
        shutil.rmtree(tempfolder)
        return redirect(url_for('download_file', name=zipfilename))






