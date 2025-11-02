from flask import Flask, request, jsonify, render_template_string, send_file
import requests, os, random, tempfile, pyttsx3, speech_recognition as sr

# ------------------ Flask App ------------------
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------ Weather API ------------------
@app.route('/get_weather')
def get_weather():
    city = request.args.get('city', 'Hyderabad')
    api_key = "db90522fb0550840ee1e9393a0fa5928"  # replace with your key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    data = requests.get(url).json()
    if data.get("cod") != 200:
        return jsonify({"error": "Failed to fetch weather", "details": data})
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return jsonify({"city": city, "temperature": temp, "description": desc})

# ------------------ AI Crop Doctor ------------------
@app.route('/predict_disease', methods=['POST'])
def predict_disease():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"})
    image = request.files['image']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    possible_diseases = {
        "Tomato": ["Leaf Curl Virus", "Late Blight", "Healthy"],
        "Paddy": ["Bacterial Blight", "Blast", "Healthy"],
        "Cotton": ["Wilt", "Bollworm Attack", "Healthy"]
    }
    crop = random.choice(list(possible_diseases.keys()))
    disease = random.choice(possible_diseases[crop])

    treatments = {
        "Leaf Curl Virus": "Spray neem oil and remove infected leaves.",
        "Late Blight": "Use Mancozeb fungicide every 7–10 days.",
        "Bacterial Blight": "Apply copper-based fungicides.",
        "Blast": "Use Tricyclazole and maintain proper spacing.",
        "Wilt": "Apply Carbendazim and improve soil drainage.",
        "Bollworm Attack": "Use pheromone traps and safe insecticides.",
        "Healthy": "No disease detected. Keep regular irrigation."
    }

    return jsonify({
        "crop": crop,
        "disease": disease,
        "treatment": treatments[disease]
    })

# ------------------ Test Crop ------------------
@app.route('/test-crop', methods=['POST'])
def test_crop():
    crop_name = request.form.get('crop_name')
    if crop_name:
        return f"Crop '{crop_name}' tested successfully!"
    else:
        return "Please enter a crop name."

# ------------------ Voice Advisory ------------------
@app.route('/voice-advisory', methods=['POST'])
def voice_advisory():
    if 'audio' not in request.files:
        return {"error": "No audio file uploaded"}, 400

    audio_file = request.files['audio']
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, audio_file.filename)
    audio_file.save(audio_path)

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        print("User said:", text)
    except sr.UnknownValueError:
        return {"error": "Could not understand audio"}, 400
    except sr.RequestError:
        return {"error": "Speech recognition service failed"}, 500

    if "weather" in text.lower():
        reply_text = "The weather in Hyderabad is 30 degrees Celsius."
    elif "crop" in text.lower():
        reply_text = "The crop seems healthy. Keep regular irrigation."
    else:
        reply_text = "Sorry, I can only give weather or crop advice for now."

    engine = pyttsx3.init()
    tts_path = os.path.join(temp_dir, "reply.wav")
    engine.save_to_file(reply_text, tts_path)
    engine.runAndWait()

    return send_file(tts_path, mimetype="audio/wav", as_attachment=False, download_name="reply.wav")

# ------------------ Dashboard (Single Page) ------------------
@app.route('/')
def home():
    html = """
    <h1>Kisan Salah - All-in-One Demo</h1>
    
    <hr>
    <h2>Weather Query</h2>
    <input type="text" id="city" placeholder="Enter city">
    <button onclick="getWeather()">Get Weather</button>
    <p id="weatherResult"></p>

    <hr>
    <h2>Crop Doctor</h2>
    <input type="file" id="cropImage" accept="image/*">
    <button onclick="predictCrop()">Predict Disease</button>
    <p id="cropResult"></p>

    <hr>
    <h2>Test Crop</h2>
    <input type="text" id="cropName" placeholder="Enter crop name">
    <button onclick="testCrop()">Test Crop</button>
    <p id="testCropResult"></p>

    <hr>
    <h2>Voice Advisory</h2>
    <input type="file" id="voiceFile" accept="audio/wav">
    <button onclick="voiceAdvisory()">Send Voice</button>
    <audio id="voiceReply" controls></audio>

    <script>
    async function getWeather() {
        const city = document.getElementById('city').value;
        const res = await fetch(`/get_weather?city=${city}`);
        const data = await res.json();
        if(data.error){
            document.getElementById('weatherResult').innerText = data.error;
        } else {
            document.getElementById('weatherResult').innerText =
                `City: ${data.city}, Temp: ${data.temperature}°C, Description: ${data.description}`;
        }
    }

    async function predictCrop() {
        const fileInput = document.getElementById('cropImage');
        const data = new FormData();
        data.append('image', fileInput.files[0]);
        const res = await fetch('/predict_disease', {method: 'POST', body: data});
        const result = await res.json();
        document.getElementById('cropResult').innerText =
            `Crop: ${result.crop}, Disease: ${result.disease}, Treatment: ${result.treatment}`;
    }

    async function testCrop() {
        const cropName = document.getElementById('cropName').value;
        const data = new FormData();
        data.append('crop_name', cropName);
        const res = await fetch('/test-crop', {method: 'POST', body: data});
        const text = await res.text();
        document.getElementById('testCropResult').innerHTML = text;
    }

    async function voiceAdvisory() {
        const fileInput = document.getElementById('voiceFile');
        const data = new FormData();
        data.append('audio', fileInput.files[0]);

        const res = await fetch('/voice-advisory', {method: 'POST', body: data});
        if(res.ok){
            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            const audio = document.getElementById('voiceReply');
            audio.src = url;
            audio.play();
        } else {
            const err = await res.json();
            alert(err.error);
        }
    }
    </script>
    """
    return render_template_string(html)

# ------------------ Run Server ------------------
if __name__ == '__main__':
    app.run(debug=True)
