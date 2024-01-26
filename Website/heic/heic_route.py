from flask import Blueprint, redirect, render_template, request, flash
from werkzeug.utils import secure_filename
from PIL import Image
from pillow_heif import register_heif_opener
from glob import glob
import os
import uuid
import shutil
from flask import send_file

register_heif_opener()

# setting blueprint and assigning the file path for the temp files
heic_route = Blueprint("heic_route", __name__)
file_storage_path = "C:/Users/mkiley/OneDrive - neuco.com/Documents/VS code/Heic flask - Test/files/"


# assigns each user a unique session id and redirects them to the main page
@heic_route.route('/')
def unique_ip_handler():
    global unique_id

    # assigning variables
    client_ip = str(request.environ['REMOTE_ADDR'])
    unique_id = uuid.uuid4().hex

    # Clearing duplicate dir 
    try:
        stored_files = glob(str(file_storage_path) + "*")
        for file in stored_files:
            formated_file = file.replace("\\", "/")
            if formated_file == str(file_storage_path) + str(client_ip):
                print("Duplicate Detected")
                shutil.rmtree(formated_file)
    except:
        print("Temp file clear failed")

    return redirect(unique_id, code=302)

# Main page
@heic_route.route('/<unique_id>', methods=['GET','POST'])
def heic_coverter(unique_id):
    global redirect_unique_id
    global zip_location_path
    global client_location_path
    global download_ready
    global client_ip
    

    # assigning variables
    flash = ""
    client_ip = str(request.environ['REMOTE_ADDR'])
    client_location_path = file_storage_path + client_ip + "/"
    temp_location_path = client_location_path + "temp_files/"
    redirect_unique_id = '/redirect/' + unique_id
    zip_location_path = client_location_path + "Converted_images.zip"


    # if data is posted
    if request.method == 'POST':
        print("Data Posted!")
        download_ready = False
        file_counter = 0

        # making directories for files
        try:
            os.mkdir(client_location_path)
            os.mkdir(temp_location_path)
        except:
            pass


        # pulling files and checking for empty post requests
        heic_file = request.files.getlist('file')
        for file in heic_file:
            if str(file).split("'")[1] == "":
                print('Empty post request detected. Skipping list item.')
                del heic_file[int(file_counter)]

            file_counter += 1

        # converting files
        for file in heic_file:

            # sorting variables
            file_type = str(secure_filename(file.filename)).split(".")[-1]
            file_name = str(secure_filename(file.filename)).split(".")[0]

            # filtering accepted file types
            if file_type.lower() == "heic" or file_type.lower() == "heif" and len(heic_file) >= 1:
                print('File Accepted!')

                # downloading current file/s
                heic_download = str(temp_location_path) + str(file_name) + str(file_type)
                file.save(heic_download)

                # converting file/s to jpg format
                image = Image.open(file)
                image.convert("RGB").save(str(temp_location_path) + str(file_name) + ".jpg")
                os.remove(heic_download)

                flash = "Files uploaded"

            # error catcher for unsupported file types
            else:
                print("no supported file types recognized")
                pass

        # compressing files and saving them as a zip file
        shutil.make_archive("files/" + str(client_ip) + "/Converted_Images", 'zip', temp_location_path)
        download_ready = True

    return render_template("Index.html", unique_id=unique_id, redirect_unique_id=redirect_unique_id, flash=flash)


#redirecting user to download page
@heic_route.route("/redirect/<unique_id>")
def redirect_page(unique_id):
    global download_unique_id
    download_unique_id = '/send-file/' + unique_id
    return render_template("Redirect.html", download_unique_id=download_unique_id)


# Download page
@heic_route.route('/send-file/<unique_id>', methods=['GET','POST'])
def send_files(unique_id):
    print("Sent to download Page!")

    if request.method == 'POST':
        submit = request.form.get('convert')

        # if download button was clicked
        if submit == 'download':
            try:
                #checking to see if download is ready
                while download_ready == False:
                    pass

                # sending files to client
                print("Files Downloaded!")
                return send_file(zip_location_path, as_attachment=True)
            
            # if no files have been uploaded it redirects to the main page
            except:
                return redirect("/", code=302)

        # if Convert more button is clicked    
        if submit == "convert":
            # sending client back to home page
            return redirect("/", code=302)
    
    return render_template('Download_file.html', download_unique_id=download_unique_id)
