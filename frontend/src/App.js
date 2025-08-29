import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, useNavigate, useParams } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ================ LANGUAGE SERVICE ================
const LanguageService = {
  translations: {
    "hindi": {
      "welcome": "स्वागत है AgriSense Quantum में",
      "register_farmer": "किसान पंजीकरण",
      "dashboard": "डैशबोर्ड",
      "weather": "मौसम",
      "crop_recommendations": "फसल सिफारिशें",
      "alerts": "अलर्ट",
      "name": "नाम",
      "phone": "फोन नंबर",
      "farm_size": "खेत का आकार (एकड़)",
      "experience": "अनुभव (वर्ष)",
      "address": "पता",
      "register": "पंजीकरण करें",
      "current_weather": "वर्तमान मौसम",
      "temperature": "तापमान",
      "humidity": "नमी",
      "rainfall": "बारिश",
      "wind_speed": "हवा की गति",
      "recommendations": "सिफारिशें",
      "quantum_score": "क्वांटम स्कोर",
      "expected_yield": "अपेक्षित उत्पादन",
      "voice_command": "आवाज कमांड",
      "speak": "बोलें",
      "listening": "सुन रहा हूं...",
      "get_weather": "मौसम बताएं",
      "get_recommendations": "फसल सिफारिश दें",
      "high_temp_alert": "उच्च तापमान चेतावनी",
      "good_rain_alert": "अच्छी बारिश - बुआई का समय"
    },
    "marathi": {
      "welcome": "AgriSense Quantum मध्ये आपले स्वागत आहे",
      "register_farmer": "शेतकरी नोंदणी",
      "dashboard": "डॅशबोर्ड",
      "weather": "हवामान",
      "crop_recommendations": "पीक शिफारसी",
      "alerts": "इशारे",
      "name": "नाव",
      "phone": "फोन नंबर",
      "farm_size": "शेताचा आकार (एकर)",
      "experience": "अनुभव (वर्षे)",
      "address": "पत्ता",
      "register": "नोंदणी करा",
      "current_weather": "सध्याचे हवामान",
      "temperature": "तापमान",
      "humidity": "ओलावा",
      "rainfall": "पाऊस",
      "wind_speed": "वाऱ्याची गती",
      "recommendations": "शिफारसी",
      "quantum_score": "क्वांटम स्कोर",
      "expected_yield": "अपेक्षित उत्पादन",
      "voice_command": "आवाज आदेश",
      "speak": "बोला",
      "listening": "ऐकत आहे...",
      "get_weather": "हवामान सांगा",
      "get_recommendations": "पीक शिफारस द्या",
      "high_temp_alert": "उच्च तापमान इशारा",
      "good_rain_alert": "चांगला पाऊस - पेरणीची वेळ"
    }
  },
  
  get: function(key, language = 'hindi') {
    return this.translations[language]?.[key] || this.translations['hindi'][key] || key;
  },
  
  speak: function(text, language = 'hindi') {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = language === 'marathi' ? 'mr-IN' : 'hi-IN';
      utterance.rate = 0.8;
      speechSynthesis.speak(utterance);
    }
  }
};

// ================ VOICE INTERFACE COMPONENT ================
const VoiceInterface = ({ language, onVoiceCommand }) => {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);

  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      recognitionInstance.lang = language === 'marathi' ? 'mr-IN' : 'hi-IN';
      
      recognitionInstance.onstart = () => setIsListening(true);
      recognitionInstance.onend = () => setIsListening(false);
      
      recognitionInstance.onresult = (event) => {
        const transcript = event.results[0][0].transcript.toLowerCase();
        onVoiceCommand(transcript);
      };
      
      setRecognition(recognitionInstance);
    }
  }, [language, onVoiceCommand]);

  const startListening = () => {
    if (recognition) {
      recognition.start();
    }
  };

  return (
    <div className="voice-interface bg-green-100 p-4 rounded-lg mb-4">
      <h3 className="text-lg font-semibold mb-2 text-green-800">
        🎤 {LanguageService.get('voice_command', language)}
      </h3>
      <button
        onClick={startListening}
        disabled={isListening}
        className={`px-6 py-2 rounded-lg font-semibold ${
          isListening 
            ? 'bg-red-500 text-white cursor-not-allowed' 
            : 'bg-green-600 text-white hover:bg-green-700'
        }`}
      >
        {isListening 
          ? LanguageService.get('listening', language)
          : LanguageService.get('speak', language)
        }
      </button>
      <div className="mt-2 text-sm text-green-700">
        <p>"{LanguageService.get('get_weather', language)}" या "{LanguageService.get('get_recommendations', language)}"</p>
      </div>
    </div>
  );
};

// ================ WEATHER COMPONENT ================
const WeatherCard = ({ weatherData, language }) => {
  if (!weatherData) return null;

  const getWeatherIcon = (temp, humidity, rainfall) => {
    if (rainfall > 50) return "🌧️";
    if (temp > 35) return "☀️";
    if (humidity > 80) return "🌫️";
    return "⛅";
  };

  return (
    <div className="bg-blue-50 p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-4 text-blue-800 flex items-center">
        {getWeatherIcon(weatherData.temperature, weatherData.humidity, weatherData.rainfall)}
        <span className="ml-2">{LanguageService.get('current_weather', language)}</span>
      </h3>
      
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white p-3 rounded">
          <div className="text-2xl font-bold text-red-600">{Math.round(weatherData.temperature)}°C</div>
          <div className="text-sm text-gray-600">{LanguageService.get('temperature', language)}</div>
        </div>
        
        <div className="bg-white p-3 rounded">
          <div className="text-2xl font-bold text-blue-600">{Math.round(weatherData.humidity)}%</div>
          <div className="text-sm text-gray-600">{LanguageService.get('humidity', language)}</div>
        </div>
        
        <div className="bg-white p-3 rounded">
          <div className="text-2xl font-bold text-green-600">{Math.round(weatherData.rainfall)}mm</div>
          <div className="text-sm text-gray-600">{LanguageService.get('rainfall', language)}</div>
        </div>
        
        <div className="bg-white p-3 rounded">
          <div className="text-2xl font-bold text-purple-600">{Math.round(weatherData.wind_speed)} km/h</div>
          <div className="text-sm text-gray-600">{LanguageService.get('wind_speed', language)}</div>
        </div>
      </div>
    </div>
  );
};

// ================ CROP RECOMMENDATIONS COMPONENT ================
const CropRecommendations = ({ recommendations, language }) => {
  if (!recommendations || recommendations.length === 0) return null;

  const getCropIcon = (cropName) => {
    const icons = {
      rice: "🌾",
      wheat: "🌾", 
      sugarcane: "🎋",
      cotton: "🌸",
      soybean: "🫘"
    };
    return icons[cropName] || "🌱";
  };

  return (
    <div className="bg-green-50 p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-4 text-green-800">
        🧬 {LanguageService.get('recommendations', language)}
      </h3>
      
      <div className="space-y-4">
        {recommendations.slice(0, 3).map((rec, index) => (
          <div key={index} className="bg-white p-4 rounded-lg border-l-4 border-green-500">
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-lg font-semibold text-green-800 flex items-center">
                {getCropIcon(rec.crop_name)}
                <span className="ml-2">{rec.crop_name.toUpperCase()}</span>
              </h4>
              <div className="text-right">
                <div className="text-sm text-gray-600">{LanguageService.get('quantum_score', language)}</div>
                <div className="text-lg font-bold text-purple-600">{rec.quantum_resilience_score}%</div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-semibold">Confidence:</span> {rec.confidence_score}%
              </div>
              <div>
                <span className="font-semibold">{LanguageService.get('expected_yield', language)}:</span> {rec.expected_yield} tons/acre
              </div>
              <div>
                <span className="font-semibold">Water Need:</span> {Math.round(rec.water_requirement)} liters
              </div>
              <div>
                <span className="font-semibold">Market Price:</span> ₹{Math.round(rec.market_price_prediction)}/ton
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ================ ALERTS COMPONENT ================
const AlertsPanel = ({ alerts, language }) => {
  if (!alerts || alerts.length === 0) return null;

  const getAlertIcon = (type, severity) => {
    if (severity === 'critical') return "🚨";
    if (type === 'weather') return "🌤️";
    if (type === 'pest') return "🐛";
    return "📢";
  };

  const getAlertColor = (severity) => {
    const colors = {
      low: "border-blue-500 bg-blue-50",
      medium: "border-yellow-500 bg-yellow-50", 
      high: "border-orange-500 bg-orange-50",
      critical: "border-red-500 bg-red-50"
    };
    return colors[severity] || colors.medium;
  };

  return (
    <div className="bg-yellow-50 p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-4 text-yellow-800">
        🔔 {LanguageService.get('alerts', language)}
      </h3>
      
      <div className="space-y-3">
        {alerts.slice(0, 3).map((alert, index) => (
          <div key={index} className={`p-4 rounded-lg border-l-4 ${getAlertColor(alert.severity)}`}>
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-2">{getAlertIcon(alert.type, alert.severity)}</span>
              <h4 className="font-semibold">
                {language === 'marathi' ? alert.title_mr : alert.title_hi}
              </h4>
            </div>
            <p className="text-sm">
              {language === 'marathi' ? alert.message_mr : alert.message_hi}
            </p>
            <div className="mt-2 text-xs text-gray-600">
              Action: {alert.action_required}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ================ FARMER REGISTRATION ================
const FarmerRegistration = ({ onRegistered, language, setLanguage }) => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    language: language,
    location: {
      latitude: 19.7515,
      longitude: 75.7139,
      address: '',
      district: '',
      state: 'Maharashtra',
      country: 'India'
    },
    farm_size_acres: '',
    experience_years: '',
    preferred_crops: []
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/farmers`, formData);
      LanguageService.speak(
        language === 'marathi' 
          ? "नोंदणी यशस्वी झाली" 
          : "पंजीकरण सफल हुआ", 
        language
      );
      onRegistered(response.data);
    } catch (error) {
      console.error('Registration failed:', error);
      alert('Registration failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-green-800 mb-2">
            🌾 AgriSense Quantum
          </h1>
          <p className="text-green-600">{LanguageService.get('welcome', language)}</p>
          
          {/* Language Selector */}
          <div className="mt-4 flex justify-center space-x-4">
            <button
              onClick={() => setLanguage('hindi')}
              className={`px-4 py-2 rounded ${language === 'hindi' ? 'bg-green-600 text-white' : 'bg-gray-200'}`}
            >
              हिंदी
            </button>
            <button
              onClick={() => setLanguage('marathi')}
              className={`px-4 py-2 rounded ${language === 'marathi' ? 'bg-green-600 text-white' : 'bg-gray-200'}`}
            >
              मराठी
            </button>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              {LanguageService.get('name', language)}
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              {LanguageService.get('phone', language)}
            </label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              {LanguageService.get('address', language)}
            </label>
            <input
              type="text"
              value={formData.location.address}
              onChange={(e) => setFormData({
                ...formData, 
                location: {...formData.location, address: e.target.value}
              })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                {LanguageService.get('farm_size', language)}
              </label>
              <input
                type="number"
                value={formData.farm_size_acres}
                onChange={(e) => setFormData({...formData, farm_size_acres: parseFloat(e.target.value)})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                {LanguageService.get('experience', language)}
              </label>
              <input
                type="number"
                value={formData.experience_years}
                onChange={(e) => setFormData({...formData, experience_years: parseInt(e.target.value)})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-green-600 to-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:shadow-lg transition-all duration-300"
          >
            {LanguageService.get('register', language)}
          </button>
        </form>
      </div>
    </div>
  );
};

// ================ FARMER DASHBOARD ================
const FarmerDashboard = ({ farmer, language, setLanguage }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, [farmer.id]);

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get(`${API}/dashboard/${farmer.id}`);
      setDashboardData(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceCommand = async (command) => {
    if (command.includes('मौसम') || command.includes('weather') || command.includes('हवामान')) {
      const weatherText = language === 'marathi' 
        ? `तापमान ${Math.round(dashboardData?.current_weather?.temperature)} अंश आणि ओलावा ${Math.round(dashboardData?.current_weather?.humidity)} टक्के आहे`
        : `तापमान ${Math.round(dashboardData?.current_weather?.temperature)} डिग्री और नमी ${Math.round(dashboardData?.current_weather?.humidity)} प्रतिशत है`;
      
      LanguageService.speak(weatherText, language);
    } else if (command.includes('फसल') || command.includes('crop') || command.includes('पीक')) {
      const recommendations = dashboardData?.recommendations || [];
      if (recommendations.length > 0) {
        const cropText = language === 'marathi' 
          ? `आपल्यासाठी सर्वोत्तम पीक ${recommendations[0].crop_name} आहे`
          : `आपके लिए सबसे अच्छी फसल ${recommendations[0].crop_name} है`;
        
        LanguageService.speak(cropText, language);
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-500 mx-auto mb-4"></div>
          <p className="text-xl text-green-800">Loading Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <header className="bg-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-green-800">
              🌾 AgriSense Quantum
            </h1>
            
            <div className="flex items-center space-x-4">
              <div className="flex space-x-2">
                <button
                  onClick={() => setLanguage('hindi')}
                  className={`px-3 py-1 rounded ${language === 'hindi' ? 'bg-green-600 text-white' : 'bg-gray-200'}`}
                >
                  हिंदी
                </button>
                <button
                  onClick={() => setLanguage('marathi')}
                  className={`px-3 py-1 rounded ${language === 'marathi' ? 'bg-green-600 text-white' : 'bg-gray-200'}`}
                >
                  मराठी
                </button>
              </div>
              
              <div className="text-right">
                <p className="font-semibold text-green-800">{farmer.name}</p>
                <p className="text-sm text-gray-600">{farmer.location.address}</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <VoiceInterface 
          language={language} 
          onVoiceCommand={handleVoiceCommand}
        />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <WeatherCard 
            weatherData={dashboardData?.current_weather} 
            language={language}
          />
          
          <AlertsPanel 
            alerts={dashboardData?.alerts} 
            language={language}
          />
        </div>

        <CropRecommendations 
          recommendations={dashboardData?.recommendations} 
          language={language}
        />

        <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">
            📊 Quantum Analysis Overview
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-3xl font-bold text-purple-600">
                {dashboardData?.recommendations?.[0]?.quantum_resilience_score || 0}%
              </div>
              <div className="text-sm text-gray-600">Quantum Resilience</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-3xl font-bold text-green-600">
                {dashboardData?.recommendations?.length || 0}
              </div>
              <div className="text-sm text-gray-600">Crop Options</div>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-3xl font-bold text-blue-600">
                {Math.round(dashboardData?.current_weather?.temperature || 0)}°C
              </div>
              <div className="text-sm text-gray-600">Current Temp</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

// ================ MAIN APP COMPONENT ================
function App() {
  const [farmer, setFarmer] = useState(null);
  const [language, setLanguage] = useState('hindi');

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={
            farmer ? (
              <FarmerDashboard 
                farmer={farmer} 
                language={language} 
                setLanguage={setLanguage}
              />
            ) : (
              <FarmerRegistration 
                onRegistered={setFarmer} 
                language={language} 
                setLanguage={setLanguage}
              />
            )
          } />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;