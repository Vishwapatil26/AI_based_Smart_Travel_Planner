import streamlit as st
import google.generativeai as genai
import requests

# Set up API keys
GOOGLE_GENAI_API_KEY = "XXXXXXXXXXXXXXXXXXXXXX"
WEATHER_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXX"

# Configure GenAI
genai.configure(api_key=GOOGLE_GENAI_API_KEY)

# Function to fetch weather data
def get_weather(city):
    """Fetch current weather details for the city."""
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    response = requests.get(url).json()
    if "current" in response:
        return f"{response['current']['temp_c']}°C, {response['current']['condition']['text']}"
    return "Weather data unavailable"

# Function to generate travel options
def get_travel_options(source, destination, budget):
    """Generate travel options using Google GenAI."""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Ensure correct model usage
        prompt = (f"Suggest travel options from {source} to {destination}, including flights, trains, buses, and cabs, "
                  f"with estimated costs in Indian Rupees (INR). Provide recommendations for a budget of ₹{budget}.")
        response = model.generate_content(prompt)
        return response.text if hasattr(response, "text") else "No options found."
    except Exception as e:
        return f"Error: {str(e)}"

# Custom Background Styling
st.markdown(
    """
    <style>
        body {
            
            background-size: cover;
        }
        .main {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 15px;
        }
        h1 {
            color: #ff5733;
            text-align: center;
        }
        .stButton>button {
            background-color: #ff5733;
            color: white;
            font-size: 18px;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI Layout
st.markdown("<div class='main'>", unsafe_allow_html=True)
st.title("✈️ AI-Powered Travel Planner")
st.markdown(
    """<h6 style="text-align: center;">
        Plan your perfect trip with real-time travel insights! 🌍
    </h6>""",
        unsafe_allow_html=True
    )

# Sidebar for input fields
st.sidebar.header("📍 Plan Your Trip")
source = st.sidebar.text_input("🏙️ Source City")
destination = st.sidebar.text_input("🌆 Destination City")
budget = st.sidebar.number_input("💰 Budget (INR)", min_value=500, max_value=100000, value=5000)

if st.sidebar.button("🔍 Find Travel Options"):
    if source and destination:
        st.subheader("🚆 Travel Options")
        travel_options = get_travel_options(source, destination, budget)
        st.success(travel_options)

        # Show weather updates
        st.subheader("🌦 Weather Updates")
        st.info(f"📍 {source}: {get_weather(source)}")
        st.info(f"📍 {destination}: {get_weather(destination)}")
    else:
        st.warning("⚠️ Please enter both source and destination.")

st.markdown("</div>", unsafe_allow_html=True)
