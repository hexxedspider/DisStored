import os
import json
import base64
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, Response
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import webbrowser
import queue
import io
from config import Config

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = None  # No file size limit

# Configuration
WEBHOOK_URL = Config.DISCORD_WEBHOOK_URL
DATA_FILE = Config.DATA_FILE
MAX_FILE_SIZE = Config.MAX_FILE_SIZE
CHUNK_SIZE = Config.CHUNK_SIZE  # Use config value
MAX_TOTAL_FILE_SIZE = Config.MAX_TOTAL_FILE_SIZE  # Use config value
event_queue = queue.Queue()

class FileStorage:
    def __init__(self):
        self.files = self.load_files()
    
    def load_files(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {'files': [], 'folders': {}}
        return {'files': [], 'folders': {}}
    
    @app.route('/events')
    def events():
        def stream():
            while True:
                msg = event_queue.get()  # waits until a new event
                yield f"data: {msg}\n\n"
        return Response(stream(), mimetype="text/event-stream")

    def save_files(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.files, f, indent=2)
    
    def add_file(self, filename, file_data, folder='', discord_chunks=None, uploader_ip=None):
        file_info = {
            'id': len(self.files['files']) + 1,
            'name': filename,
            'folder': folder,
            'size': len(file_data),
            'uploaded_at': datetime.now().isoformat(),
            'data': base64.b64encode(file_data).decode('utf-8'),
            'discord_chunks': discord_chunks or [],
            'uploader_ip': uploader_ip or "unknown"
        }
        self.files['files'].append(file_info)
        self.save_files()
        return file_info
    
    def get_file(self, file_id):
        for file in self.files['files']:
            if file['id'] == file_id:
                return file
        return None
    
    def delete_file(self, file_id):
        self.files['files'] = [f for f in self.files['files'] if f['id'] != file_id]
        self.save_files()
    
    def get_files_in_folder(self, folder=''):
        return [f for f in self.files['files'] if f['folder'] == folder]
    
    def add_folder(self, folder_name):
        """Create a new empty folder"""
        if folder_name not in self.files['folders']:
            self.files['folders'][folder_name] = []
            self.save_files()
            return True
        return False

    def get_folders(self):
        """Return both explicit and implicit folders"""
        folders = set(self.files['folders'].keys())
        for file in self.files['files']:
            if file['folder']:
                folders.add(file['folder'])
        return sorted(list(folders))

file_storage = FileStorage()

def upload_chunk_to_discord(chunk_data, filename, chunk_number, total_chunks):
    """Upload a single chunk to Discord webhook"""
    if not WEBHOOK_URL:
        return None
    
    try:
        chunk_filename = f"{filename}.part{chunk_number:03d}of{total_chunks:03d}"
        
        temp_filename = f"temp_{chunk_filename}"
        with open(temp_filename, 'wb') as f:
            f.write(chunk_data)
        
        with open(temp_filename, 'rb') as f:
            files = {'file': (chunk_filename, f, 'application/octet-stream')}
            response = requests.post(WEBHOOK_URL, files=files)
        
        os.remove(temp_filename)
        
        if response.status_code == 200:
            response_data = response.json()
            if 'attachments' in response_data and len(response_data['attachments']) > 0:
                return response_data['attachments'][0]['url']
            return None
        else:
            return None
    except Exception as e:
        print(f"Error uploading chunk {chunk_number} to Discord: {e}")
        return None

def upload_to_discord(file_data, filename):
    """Upload file to Discord webhook (with chunking support, 3 at a time)"""
    if not WEBHOOK_URL:
        return None
    
    file_size = len(file_data)

    # Single-chunk file, just upload normally
    if file_size <= CHUNK_SIZE:
        try:
            temp_filename = f"temp_{filename}"
            with open(temp_filename, 'wb') as f:
                f.write(file_data)
            
            with open(temp_filename, 'rb') as f:
                files = {'file': (filename, f, 'application/octet-stream')}
                response = requests.post(WEBHOOK_URL, files=files)
            
            os.remove(temp_filename)
            
            if 200 <= response.status_code < 300:
                response_data = response.json()
                if 'attachments' in response_data and len(response_data['attachments']) > 0:
                    return [response_data['attachments'][0]['url']]
                return None
            else:
                return None
        except Exception as e:
            print(f"Error uploading to Discord: {e}")
            return None

    # Multi-chunk upload
    print(f"Splitting {filename} into chunks...")
    total_chunks = int((file_size + CHUNK_SIZE - 1) // CHUNK_SIZE)

    # Prepare tasks
    def task(i):
        start = i * CHUNK_SIZE
        end = min(start + CHUNK_SIZE, file_size)
        chunk_data = file_data[start:end]
        print(f"Uploading chunk {i+1}/{total_chunks} ({len(chunk_data)} bytes)...")
        return (i, upload_chunk_to_discord(chunk_data, filename, i+1, total_chunks))

    chunks = [None] * total_chunks
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(task, i) for i in range(total_chunks)]
        for future in as_completed(futures):
            i, url = future.result()
            if url:
                chunks[i] = url
            else:
                print(f"Failed to upload chunk {i+1}")
                return None

    if all(chunks):
        print(f"Successfully uploaded {len(chunks)} chunks for {filename}")
        return chunks
    else:
        print(f"Some chunks failed for {filename}")
        return None

@app.route('/')
def index():
    folder = request.args.get('folder', '')
    files = file_storage.get_files_in_folder(folder)
    folders = file_storage.get_folders()
    return render_template('index.html', files=files, folders=folders, current_folder=folder)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    folder = request.form.get('folder', '')
    uploader_ip = request.remote_addr  # 👈 get client IP

    if not file.filename or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    file_data = file.read()
    
    discord_chunks = upload_to_discord(file_data, filename)

    # Store file locally (with uploader_ip)
    file_info = file_storage.add_file(filename, file_data, folder, discord_chunks)
    file_info['uploader_ip'] = uploader_ip
    file_storage.save_files()

    event_queue.put(json.dumps({
        "event": "new_file",
        "file_id": file_info["id"],
        "name": file_info["name"],
        "uploader_ip": file_info.get("uploader_ip", "unknown")
    }))

    return jsonify({
        'success': True,
        'file': file_info,
        'discord_uploaded': discord_chunks is not None and len(discord_chunks) > 0,
        'chunks_uploaded': len(discord_chunks) if discord_chunks else 0
    })

def download_from_discord_chunks(chunk_urls):
    """Download and reassemble file from Discord chunks"""
    if not chunk_urls:
        return None
    
    try:
        file_data = b''
        for i, chunk_url in enumerate(chunk_urls):
            print(f"Downloading chunk {i+1}/{len(chunk_urls)} from Discord...")
            response = requests.get(chunk_url)
            if response.status_code == 200:
                file_data += response.content
            else:
                print(f"Failed to download chunk {i+1}")
                return None
        
        print(f"Successfully reassembled file from {len(chunk_urls)} chunks")
        return file_data
    except Exception as e:
        print(f"Error downloading from Discord chunks: {e}")
        return None

@app.route('/download/<int:file_id>')
def download_file(file_id):
    file_info = file_storage.get_file(file_id)
    if not file_info:
        return jsonify({'error': 'File not found'}), 404
    
    if file_info.get('discord_chunks') and len(file_info['discord_chunks']) > 0:
        if not file_info.get('data') or len(file_info['data']) == 0:
            print(f"Reconstructing {file_info['name']} from Discord chunks...")
            file_data = download_from_discord_chunks(file_info['discord_chunks'])
            if file_data:
                file_info['data'] = base64.b64encode(file_data).decode('utf-8')
                file_storage.save_files()
            else:
                return jsonify({'error': 'Failed to reconstruct file from Discord chunks'}), 500
        else:
            file_data = base64.b64decode(file_info['data'])
    else:
        file_data = base64.b64decode(file_info['data'])
    
    return send_file(
        io.BytesIO(file_data),
        as_attachment=True,
        download_name=file_info['name']
    )

@app.route('/delete/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    file_storage.delete_file(file_id)
    return jsonify({'success': True})

@app.route('/folders')
def get_folders():
    folders = file_storage.get_folders()
    return jsonify({'folders': folders})

@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.json.get('folder') # type: ignore
    if not folder_name:
        return jsonify({'error': 'Folder name required'}), 400

    success = file_storage.add_folder(folder_name)
    if not success:
        return jsonify({'error': 'Folder already exists'}), 400

    event_queue.put(json.dumps({
        "event": "new_folder",
        "name": folder_name
    }))

    return jsonify({'success': True, 'folder': folder_name})

def open_browser():
    webbrowser.open('http://10.0.0.7:26435')

if __name__ == '__main__':
    # Print configuration
    Config.print_config()
    Config.validate_config()
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print(f"\nStarting DisStored file storage server...")
    print(f"Web UI opened in tab at: http://{Config.HOST}:{Config.PORT}")
    
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
