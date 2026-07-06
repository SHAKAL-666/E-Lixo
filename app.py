import os
import sqlite3
from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import imagehash
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'data', 'images.db')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

app = Flask(__name__, root_path=BASE_DIR, instance_path=BASE_DIR)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-for-local')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', '1') == '1'

# Simple admin credentials (override via env vars in production)
ADMIN_USER = os.environ.get('E_LIXO_ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('E_LIXO_ADMIN_PASS', 'password')

# Predefined explanations for each category
CATEGORY_EXPLANATIONS = {
    'Equipamentos de informática': 'Computadores, notebooks, monitores, impressoras e acessórios relacionados ao processamento de dados.',
    'Dispositivos de comunicação': 'Celulares, modems, roteadores e outros dispositivos usados para comunicação de voz e dados.',
    'Equipamentos de áudio e vídeo': 'Televisores, caixas de som, câmeras, aparelhos de som e similares.',
    'Pilhas e baterias': 'Pilhas alcalinas, baterias recarregáveis e baterias de lítio usadas em equipamentos eletrônicos.',
    'Carregadores e cabos': 'Carregadores, cabos USB, cabos de energia e adaptadores associados a dispositivos eletrônicos.',
    'Eletrodomésticos eletrônicos': 'Aparelhos domésticos com componentes eletrônicos, como micro-ondas, liquidificadores e ferros elétricos.',
    'Equipamentos de iluminação': 'Lâmpadas, luminárias e lâmpadas LED contendo componentes eletrônicos ou materiais recicláveis especiais.',
    'Componentes eletrônicos': 'Placas, resistores, capacitores, chips, e outros componentes usados em circuitos eletrônicos.'
}

# Mapping of common ImageNet labels to the waste categories in this app.
LABEL_TO_CATEGORY = {
    'computer': 'Equipamentos de informática',
    'laptop': 'Equipamentos de informática',
    'desktop computer': 'Equipamentos de informática',
    'notebook': 'Equipamentos de informática',
    'monitor': 'Equipamentos de informática',
    'keyboard': 'Equipamentos de informática',
    'mouse': 'Equipamentos de informática',
    'cellular telephone': 'Dispositivos de comunicação',
    'mobile phone': 'Dispositivos de comunicação',
    'radio': 'Dispositivos de comunicação',
    'telephone': 'Dispositivos de comunicação',
    'modem': 'Dispositivos de comunicação',
    'router': 'Dispositivos de comunicação',
    'television': 'Equipamentos de áudio e vídeo',
    'speaker': 'Equipamentos de áudio e vídeo',
    'headphone': 'Equipamentos de áudio e vídeo',
    'camera': 'Equipamentos de áudio e vídeo',
    'microphone': 'Equipamentos de áudio e vídeo',
    'battery': 'Pilhas e baterias',
    'coin cell': 'Pilhas e baterias',
    'charger': 'Carregadores e cabos',
    'cable': 'Carregadores e cabos',
    'power cord': 'Carregadores e cabos',
    'adapter': 'Carregadores e cabos',
    'microwave': 'Eletrodomésticos eletrônicos',
    'toaster': 'Eletrodomésticos eletrônicos',
    'blender': 'Eletrodomésticos eletrônicos',
    'vacuum': 'Eletrodomésticos eletrônicos',
    'lamp': 'Equipamentos de iluminação',
    'light bulb': 'Equipamentos de iluminação',
    'candle': 'Equipamentos de iluminação',
    'circuit board': 'Componentes eletrônicos',
    'printed circuit board': 'Componentes eletrônicos',
    'resistor': 'Componentes eletrônicos',
    'capacitor': 'Componentes eletrônicos',
    'semiconductor': 'Componentes eletrônicos'
}


def map_label_to_category(label):
    label_text = label.lower()
    if label_text in LABEL_TO_CATEGORY:
        return LABEL_TO_CATEGORY[label_text]

    for key, category in LABEL_TO_CATEGORY.items():
        if key in label_text:
            return category
    return None


def ensure_google_credentials():
    def validate_credentials_file(candidate):
        try:
            with open(candidate, 'r', encoding='utf-8') as f:
                payload = json.load(f)
        except Exception as exc:
            print(f'[Vision API Error] Could not parse credentials JSON at {candidate}: {exc}')
            return None

        required_fields = ['type', 'project_id', 'private_key', 'client_email', 'token_uri']
        missing = [field for field in required_fields if not payload.get(field)]
        if payload.get('type') != 'service_account':
            print(f'[Vision API Error] Unsupported credentials type in {candidate}: {payload.get("type")}')
            return None
        if missing:
            print(f'[Vision API Error] Credentials file {candidate} is missing required fields: {", ".join(missing)}')
            return None
        return candidate

    # The app can discover credentials in three ways:
    # 1) GOOGLE_APPLICATION_CREDENTIALS pointing to a JSON key file
    # 2) GOOGLE_APPLICATION_CREDENTIALS containing the JSON payload itself
    # 3) GOOGLE_CLOUD_KEY_JSON or GOOGLE_APPLICATION_CREDENTIALS_JSON containing the JSON payload
    creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if creds:
        creds = creds.strip()
        if creds.startswith('{') and 'private_key' in creds and 'client_email' in creds:
            try:
                credentials_path = os.path.join(BASE_DIR, 'google_service_account.json')
                with open(credentials_path, 'w', encoding='utf-8') as f:
                    f.write(creds)
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
                print(f'[Vision API] Loaded credentials from GOOGLE_APPLICATION_CREDENTIALS JSON payload into {credentials_path}')
                return credentials_path
            except Exception as e:
                print(f'[Vision API Error] could not write GOOGLE_APPLICATION_CREDENTIALS JSON payload to file: {e}')
                return None

        candidate_path = os.path.expanduser(creds.strip('"\''))
        if os.path.exists(candidate_path):
            print(f'[Vision API] Using GOOGLE_APPLICATION_CREDENTIALS={candidate_path}')
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = candidate_path
            return candidate_path
        print(f'[Vision API] GOOGLE_APPLICATION_CREDENTIALS is set but file not found: {candidate_path}. Trying alternate sources.')

    json_payload = os.environ.get('GOOGLE_CLOUD_KEY_JSON') or os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if json_payload:
        try:
            credentials_path = os.path.join(BASE_DIR, 'google_service_account.json')
            with open(credentials_path, 'w', encoding='utf-8') as f:
                f.write(json_payload)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            print(f'[Vision API] Loaded credentials from JSON environment variable into {credentials_path}')
            return credentials_path
        except Exception as e:
            print(f'[Vision API Error] could not write JSON env var to file: {e}')
            return None

    # Fallback: look for a downloaded service account JSON in the project root or data folder
    search_paths = [BASE_DIR, os.path.join(BASE_DIR, 'data')]
    for search_path in search_paths:
        if not os.path.isdir(search_path):
            continue
        for filename in os.listdir(search_path):
            if filename.lower().endswith('.json'):
                candidate = os.path.join(search_path, filename)
                if os.path.isfile(candidate):
                    validated = validate_credentials_file(candidate)
                    if validated:
                        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = validated
                        print(f'[Vision API] Found service account JSON at {validated}')
                        return validated
    return None


def classify_with_vision_api(image_path):
    """
    Classify image using Google Cloud Vision API.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable pointing to service account JSON.
    Returns a dict with category, explanation, label, and confidence, or an error dict when unavailable.
    """
    creds_path = ensure_google_credentials()
    if not creds_path:
        return {
            'error': 'missing_credentials',
            'message': 'Credencial do Google Vision não encontrada. Defina GOOGLE_APPLICATION_CREDENTIALS com um arquivo JSON válido do service account.'
        }
    try:
        from google.cloud import vision
    except ImportError:
        return {
            'error': 'missing_dependency',
            'message': 'O pacote google-cloud-vision não está instalado. Instale-o para habilitar a classificação automática.'
        }

    try:
        # Initialize Vision API client
        client = vision.ImageAnnotatorClient()

        # Read image file
        with open(image_path, 'rb') as f:
            image_content = f.read()

        image = vision.Image(content=image_content)

        # Perform label detection (object recognition)
        response = client.label_detection(image=image)
        if response.error and response.error.message:
            return {'error': 'vision_api_error', 'message': response.error.message}

        labels = response.label_annotations
        if not labels:
            return {'error': 'no_labels', 'message': 'A imagem não retornou rótulos suficientes para sugestão automática.'}

        # Extract top labels and try to map to our categories
        detected_objects = [label.description.lower() for label in labels[:10]]
        confidences = [float(label.score) for label in labels[:10]]

        result = None
        best_confidence = 0

        # Find best matching category from detected objects
        for i, obj_label in enumerate(detected_objects):
            category = map_label_to_category(obj_label)
            if category and confidences[i] > best_confidence:
                best_confidence = confidences[i]
                result = {
                    'label': obj_label,
                    'confidence': round(best_confidence, 3),
                    'category': category,
                    'explanation': CATEGORY_EXPLANATIONS.get(category),
                    'detected_objects': detected_objects[:5]
                }

        # If no direct match, try common keywords
        if result is None:
            keywords_to_check = {
                'computer': 'Equipamentos de informática',
                'phone': 'Dispositivos de comunicação',
                'mobile': 'Dispositivos de comunicação',
                'tv': 'Equipamentos de áudio e vídeo',
                'television': 'Equipamentos de áudio e vídeo',
                'speaker': 'Equipamentos de áudio e vídeo',
                'battery': 'Pilhas e baterias',
                'charger': 'Carregadores e cabos',
                'cable': 'Carregadores e cabos',
                'lamp': 'Equipamentos de iluminação',
                'light': 'Equipamentos de iluminação',
                'circuit': 'Componentes eletrônicos',
                'electronic': 'Componentes eletrônicos',
                'microwave': 'Eletrodomésticos eletrônicos',
                'oven': 'Eletrodomésticos eletrônicos',
                'blender': 'Eletrodomésticos eletrônicos',
            }

            for i, obj_label in enumerate(detected_objects):
                for keyword, category in keywords_to_check.items():
                    if keyword in obj_label:
                        result = {
                            'label': obj_label,
                            'confidence': round(confidences[i], 3),
                            'category': category,
                            'explanation': CATEGORY_EXPLANATIONS.get(category),
                            'detected_objects': detected_objects[:5]
                        }
                        break
                if result:
                    break

        return result

    except Exception as e:
        error_message = str(e).lower()
        if 'credentials' in error_message or 'service account' in error_message or 'token_uri' in error_message:
            return {
                'error': 'invalid_credentials',
                'message': 'A credencial do Google Vision está inválida ou incompleta. Verifique o arquivo JSON exportado do Google Cloud Console.'
            }
        return {'error': 'vision_api_error', 'message': f'Erro ao chamar o Google Vision: {e}'}


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            phash TEXT NOT NULL,
            category TEXT,
            explanation TEXT
        )
    ''')
    conn.commit()
    conn.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def compute_phash(path):
    img = Image.open(path).convert('RGB')
    return str(imagehash.phash(img))


def find_similar(phash_hex, threshold=6):
    # Return the closest match within threshold hamming distance
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT id, filename, phash, category, explanation FROM images')
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return None

    new_hash = imagehash.hex_to_hash(phash_hex)
    best = None
    best_dist = None
    for r in rows:
        try:
            existing = imagehash.hex_to_hash(r['phash'])
        except Exception:
            continue
        dist = new_hash - existing
        if best is None or dist < best_dist:
            best = r
            best_dist = dist

    if best_dist is not None and best_dist <= threshold:
        return dict(id=best['id'], filename=best['filename'], category=best['category'], explanation=best['explanation'], distance=int(best_dist))
    return None


def find_nearest_k(phash_hex, k=3):
    """Return up to k nearest rows sorted by hamming distance (no threshold)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT id, filename, phash, category, explanation FROM images')
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return []

    new_hash = imagehash.hex_to_hash(phash_hex)
    neighbors = []
    for r in rows:
        try:
            existing = imagehash.hex_to_hash(r['phash'])
        except Exception:
            continue
        dist = new_hash - existing
        neighbors.append((int(dist), dict(id=r['id'], filename=r['filename'], category=r['category'], explanation=r['explanation'])))

    neighbors.sort(key=lambda x: x[0])
    return [{'distance': d, **info} for d, info in neighbors[:k]]


def try_classify(image_path):
    """
    ML classification with fallback chain:
    1. Google Cloud Vision API (if credentials available)
    2. TensorFlow MobileNetV2 (if available)
    3. Returns None if both unavailable
    
    Returns a dict with category, explanation, label and confidence.
    """
    # Try Google Vision API first. If it returns an error dict, continue to fallbacks.
    vision_result = classify_with_vision_api(image_path)
    if vision_result and not (isinstance(vision_result, dict) and vision_result.get('error')):
        return vision_result
    if isinstance(vision_result, dict) and vision_result.get('error'):
        print(f"[ML] Vision API unavailable, reason={vision_result.get('error')}: {vision_result.get('message')}")

    # Fallback to TensorFlow
    try:
        from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
        from tensorflow.keras.preprocessing import image
        import numpy as np
    except Exception:
        return None

    try:
        model = MobileNetV2(weights='imagenet')
        img = image.load_img(image_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        decoded = decode_predictions(preds, top=3)[0]

        best_label = decoded[0][1]
        confidence = float(decoded[0][2])
        category = map_label_to_category(best_label)
        explanation = CATEGORY_EXPLANATIONS.get(category)

        result = {
            'label': best_label,
            'confidence': round(confidence, 3),
            'category': category,
            'explanation': explanation
        }

        if category is None and len(decoded) > 1:
            for item in decoded[1:]:
                candidate = map_label_to_category(item[1])
                if candidate:
                    result['category'] = candidate
                    result['explanation'] = CATEGORY_EXPLANATIONS.get(candidate)
                    break

        return result
    except Exception:
        return None


@app.route('/')
def index():
    return render_template('index.html', is_admin=session.get('admin', False))


@app.route('/healthz')
def healthz():
    return jsonify({'status': 'ok'})


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/catalogs')
def catalogs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT id, filename, phash, category, explanation FROM images ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return render_template('catalogs.html', items=rows, explanations=CATEGORY_EXPLANATIONS, is_admin=session.get('admin', False))


def admin_required(fn):
    def wrapper(*a, **kw):
        if not session.get('admin'):
            flash('Acesso restrito. Faça login como administrador.','warning')
            return redirect(url_for('login'))
        return fn(*a, **kw)
    wrapper.__name__ = fn.__name__
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            flash('Login realizado com sucesso.','success')
            return redirect(url_for('admin'))
        flash('Credenciais inválidas.','danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Logout efetuado.','info')
    return redirect(url_for('index'))


@app.route('/admin')
@admin_required
def admin():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT id, filename, phash, category, explanation FROM images ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return render_template('admin.html', items=rows)


@app.route('/admin/delete/<int:id>', methods=['POST'])
@admin_required
def admin_delete(id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT filename FROM images WHERE id = ?', (id,))
    row = cur.fetchone()
    if row:
        filename = row[0]
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception:
            pass
    cur.execute('DELETE FROM images WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Item removido do catálogo.','success')
    return redirect(url_for('admin'))


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'no file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'no selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'invalid file type'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # ensure unique filename
    base, ext = os.path.splitext(filename)
    i = 1
    while os.path.exists(save_path):
        filename = f"{base}_{i}{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        i += 1
    file.save(save_path)

    phash = compute_phash(save_path)
    similar = find_similar(phash)
    if similar:
        return jsonify({'matched': True, 'match': similar, 'filename': filename})

    # not matched — prepare suggestions from nearest neighbors
    neighbors = find_nearest_k(phash, k=5)
    suggested = None
    if neighbors:
        # pick majority category among neighbors (if any)
        from collections import Counter
        cats = [n['category'] for n in neighbors if n.get('category')]
        if cats:
            most = Counter(cats).most_common(1)[0]
            # compute a simple confidence from the best neighbor distance
            best_dist = neighbors[0]['distance']
            confidence = max(0.0, 1.0 - (best_dist / 16.0))
            suggested = {'category': most[0], 'confidence': round(confidence, 2), 'neighbors': neighbors}

    # optional ML classification
    ml = try_classify(save_path)
    return jsonify({'matched': False, 'phash': phash, 'filename': filename, 'suggested': suggested, 'ml_suggestion': ml})


@app.route('/catalog', methods=['POST'])
def catalog():
    data = request.json or request.form
    filename = data.get('filename')
    category = data.get('category')
    explanation = data.get('explanation', '')
    phash = data.get('phash')
    if not filename or not category or not phash:
        return jsonify({'error': 'missing fields (filename, category, phash required)'}), 400

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO images (filename, phash, category, explanation) VALUES (?, ?, ?, ?)', (filename, phash, category, explanation))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({'ok': True, 'id': new_id})


if __name__ == '__main__':
    init_db()
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '8000'))
    app.run(host=host, port=port, debug=app.config['DEBUG'])
