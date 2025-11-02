import streamlit as st
import requests
import datetime

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="🌾 Kisan Salah Demo", page_icon="🌱", layout="centered")

# ----------------------------
# Sidebar Menu
# ----------------------------
st.sidebar.header("🔍 Explore Features")
menu = st.sidebar.radio("Select a section:", ["Home", "Crop Suggestion", "Fertilizer Guide", "Weather Info", "About"])

# ----------------------------
# Function: Fetch Real-Time Weather
# ----------------------------
def get_weather(city, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# ----------------------------
# 1️⃣ Home Section
# ----------------------------
if menu == "Home":
    st.markdown(
        """
        <div style="background-color:#eafaf1;padding:20px;border-radius:10px">
        <h1 style="color:#2b7a0b;">🌾 Welcome to Kisan Salah</h1>
        <h4 style="color:#1f3c12;">Your Smart Farming Assistant</h4>
        <p>Get insights, suggestions, and live weather updates to boost your farm productivity!</p>
        </div>
        """, unsafe_allow_html=True
    )

    # Hero Image
    st.image("https://images.unsplash.com/photo-1595433562696-a8b1cb8b7a81", caption="Smart Farming for the Future", use_column_width=True)

    st.subheader("🌟 Key Features")
    col1, col2, col3 = st.columns(3)
    col1.metric("🌱 Crop Suggestions", "AI-based", "Improve yield")
    col2.metric("💧 Fertilizer Guide", "Optimized", "Reduce costs")
    col3.metric("☀️ Weather Advisory", "Live Data", "Plan irrigation")

    st.markdown("---")

    st.subheader("📊 Quick Demo")
    st.write("Try entering a crop, soil type, or city to see instant recommendations and weather info.")

    # Mini Input for quick demo
    demo_crop = st.text_input("Example Crop Input:")
    if demo_crop:
        st.success(f"✅ You entered: {demo_crop}")
        st.info("This is where suggestions will appear in the full app!")

    st.markdown(
        """
        <div style="background-color:#f0f8ff;padding:15px;border-radius:8px;margin-top:15px">
        💡 Tip: Use the sidebar to explore **Crop Suggestion**, **Fertilizer Guide**, and **Weather Info**.
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("---")
    st.write("Developed by: [sorrahasini](https://github.com/sorrahasini)")

# ----------------------------
# 2️⃣ Crop Suggestion Section
# ----------------------------
elif menu == "Crop Suggestion":
    st.header("🌱 Crop Suggestion System")

    soil_type = st.selectbox("Select your soil type:", ["Alluvial", "Black", "Red", "Laterite", "Arid"])
    rainfall = st.slider("Average rainfall (in mm):", 0, 500, 120)
    temperature = st.slider("Average temperature (°C):", 10, 45, 26)

    if st.button("Suggest Crop"):
        st.info(f"Soil Type: {soil_type}, Rainfall: {rainfall} mm, Temperature: {temperature}°C")
        if soil_type == "Alluvial":
            st.success("✅ Recommended Crops: Rice, Wheat, Sugarcane, Maize")
        elif soil_type == "Black":
            st.success("✅ Recommended Crops: Cotton, Soybean, Millets")
        elif soil_type == "Red":
            st.success("✅ Recommended Crops: Groundnut, Pulses, Tobacco")
        elif soil_type == "Laterite":
            st.success("✅ Recommended Crops: Tea, Coffee, Cashew")
        elif soil_type == "Arid":
            st.success("✅ Recommended Crops: Bajra, Jowar, Moong")
        else:
            st.warning("⚠️ No suitable crops found. Try different conditions.")

# ----------------------------
# 3️⃣ Fertilizer Guide Section
# ----------------------------
elif menu == "Fertilizer Guide":
    st.header("💧 Fertilizer Recommendation System")

    crop = st.text_input("Enter your crop name:")
    nitrogen = st.number_input("Nitrogen (N) level:", 0, 200, 40)
    phosphorus = st.number_input("Phosphorus (P) level:", 0, 200, 40)
    potassium = st.number_input("Potassium (K) level:", 0, 200, 40)

    if st.button("Get Fertilizer Advice"):
        if nitrogen < 50:
            st.success(f"🧪 For {crop}: Add Urea or Ammonium Sulphate to increase Nitrogen.")
        elif phosphorus < 50:
            st.success(f"🧪 For {crop}: Use DAP or SSP to boost Phosphorus.")
        elif potassium < 50:
            st.success(f"🧪 For {crop}: Apply MOP or Potash for better Potassium balance.")
        else:
            st.success("✅ Fertilizer levels are balanced! Maintain current practices.")

# ----------------------------
# 4️⃣ Weather Info Section (Live API)
# ----------------------------
elif menu == "Weather Info":
    st.header("☀️ Live Weather Advisory")

    city = st.text_input("Enter your city name:")
    api_key = "db90522fb0550840ee1e9393a0fa5928"  # 🔑 Replace this with your actual OpenWeatherMap API key

    if st.button("Get Live Weather"):
        if city:
            weather_data = get_weather(city, api_key)
            if weather_data:
                temp = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                description = weather_data['weather'][0]['description'].capitalize()
                wind_speed = weather_data['wind']['speed']

                st.success(f"✅ **Weather Report for {city.capitalize()}**")
                st.write(f"🌡️ Temperature: {temp} °C")
                st.write(f"💧 Humidity: {humidity}%")
                st.write(f"🌬️ Wind Speed: {wind_speed} m/s")
                st.write(f"☁️ Condition: {description}")

                # Simple tip based on condition
                if "rain" in description.lower():
                    st.info("💦 Tip: Rain expected — reduce irrigation and plan for drainage.")
                elif temp > 35:
                    st.warning("🔥 Tip: High temperature — ensure adequate irrigation and mulching.")
                elif temp < 15:
                    st.info("❄️ Tip: Cold conditions — consider protective cover for crops.")
                else:
                    st.success("🌿 Tip: Weather is favorable for most crops.")
            else:
                st.error("❌ Unable to fetch weather data. Check city name or API key.")
        else:
            st.warning("⚠️ Please enter a city name!")

# ----------------------------
# 5️⃣ About Section
# ----------------------------
elif menu == "About":
    st.header("ℹ️ About Kisan Salah")
    st.write("""
    **Kisan Salah** is a smart farming assistant that provides AI-driven insights to help farmers
    improve productivity, save costs, and adapt to weather changes.  

    **Built with:**
    - 🐍 Python  
    - 🎨 Streamlit  
    - ☁️ OpenWeatherMap API  
    - 💡 Smart Recommendation Logic  

    **Developer:** [sorrahasini](https://github.com/sorrahasini)
    """)


