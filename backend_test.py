import requests
import sys
import json
from datetime import datetime

class AgriSenseAPITester:
    def __init__(self, base_url="https://task-helper-14.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.farmer_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else f"{self.api_url}/"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test basic API health check"""
        return self.run_test("API Health Check", "GET", "", 200)

    def test_farmer_registration(self):
        """Test farmer registration"""
        farmer_data = {
            "name": "राज पाटील",
            "phone": "+91-9876543210",
            "language": "hindi",
            "location": {
                "latitude": 19.7515,
                "longitude": 75.7139,
                "address": "Aurangabad Maharashtra",
                "district": "Aurangabad",
                "state": "Maharashtra",
                "country": "India"
            },
            "farm_size_acres": 5.5,
            "experience_years": 15,
            "preferred_crops": ["rice", "wheat", "cotton"]
        }
        
        success, response = self.run_test(
            "Farmer Registration",
            "POST",
            "farmers",
            200,
            data=farmer_data
        )
        
        if success and 'id' in response:
            self.farmer_id = response['id']
            print(f"   Farmer ID: {self.farmer_id}")
            return True
        return False

    def test_get_farmer(self):
        """Test getting farmer details"""
        if not self.farmer_id:
            print("❌ Skipping - No farmer ID available")
            return False
            
        return self.run_test(
            "Get Farmer Details",
            "GET",
            f"farmers/{self.farmer_id}",
            200
        )[0]

    def test_crop_recommendations(self):
        """Test quantum crop recommendations"""
        if not self.farmer_id:
            print("❌ Skipping - No farmer ID available")
            return False
            
        success, response = self.run_test(
            "Quantum Crop Recommendations",
            "POST",
            f"crops/recommend/{self.farmer_id}",
            200
        )
        
        if success and isinstance(response, list) and len(response) > 0:
            print(f"   Found {len(response)} recommendations")
            for i, rec in enumerate(response[:2]):
                print(f"   Crop {i+1}: {rec.get('crop_name', 'Unknown')} - Quantum Score: {rec.get('quantum_resilience_score', 0)}%")
            return True
        return False

    def test_dashboard_data(self):
        """Test farmer dashboard data"""
        if not self.farmer_id:
            print("❌ Skipping - No farmer ID available")
            return False
            
        success, response = self.run_test(
            "Farmer Dashboard",
            "GET",
            f"dashboard/{self.farmer_id}",
            200
        )
        
        if success:
            # Check if dashboard has required components
            has_farmer = 'farmer' in response
            has_weather = 'current_weather' in response
            has_recommendations = 'recommendations' in response
            has_alerts = 'alerts' in response
            
            print(f"   Dashboard components - Farmer: {has_farmer}, Weather: {has_weather}, Recommendations: {has_recommendations}, Alerts: {has_alerts}")
            return has_farmer and has_weather
        return False

    def test_create_alert(self):
        """Test creating agricultural alerts"""
        if not self.farmer_id:
            print("❌ Skipping - No farmer ID available")
            return False
            
        # Test high temperature alert
        success1, _ = self.run_test(
            "Create High Temperature Alert",
            "POST",
            f"alerts/create?farmer_id={self.farmer_id}&alert_type=high_temperature&severity=high",
            200
        )
        
        # Test good rainfall alert
        success2, _ = self.run_test(
            "Create Good Rainfall Alert", 
            "POST",
            f"alerts/create?farmer_id={self.farmer_id}&alert_type=good_rainfall&severity=medium",
            200
        )
        
        return success1 and success2

    def test_get_alerts(self):
        """Test getting farmer alerts"""
        if not self.farmer_id:
            print("❌ Skipping - No farmer ID available")
            return False
            
        success, response = self.run_test(
            "Get Farmer Alerts",
            "GET",
            f"alerts/{self.farmer_id}",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} alerts")
            return True
        return False

    def test_translations(self):
        """Test language translations"""
        # Test Hindi translations
        success1, response1 = self.run_test(
            "Hindi Translations",
            "GET",
            "translations/hindi",
            200
        )
        
        # Test Marathi translations
        success2, response2 = self.run_test(
            "Marathi Translations",
            "GET",
            "translations/marathi", 
            200
        )
        
        if success1 and success2:
            print(f"   Hindi keys: {len(response1) if response1 else 0}")
            print(f"   Marathi keys: {len(response2) if response2 else 0}")
            return True
        return False

    def test_weather_endpoints(self):
        """Test weather-related endpoints"""
        location_data = {
            "latitude": 19.7515,
            "longitude": 75.7139,
            "address": "Aurangabad Maharashtra",
            "district": "Aurangabad", 
            "state": "Maharashtra",
            "country": "India"
        }
        
        # Test current weather
        success1, _ = self.run_test(
            "Current Weather",
            "POST",
            "weather/current",
            200,
            data=location_data
        )
        
        # Test weather forecast
        success2, _ = self.run_test(
            "Weather Forecast",
            "POST", 
            "weather/forecast",
            200,
            data=location_data
        )
        
        return success1 and success2

def main():
    print("🌾 AgriSense Quantum API Testing Suite")
    print("=" * 50)
    
    tester = AgriSenseAPITester()
    
    # Run all tests in sequence
    test_results = []
    
    # Basic API tests
    test_results.append(("Health Check", tester.test_health_check()))
    
    # Farmer management tests
    test_results.append(("Farmer Registration", tester.test_farmer_registration()))
    test_results.append(("Get Farmer Details", tester.test_get_farmer()))
    
    # Core functionality tests
    test_results.append(("Crop Recommendations", tester.test_crop_recommendations()))
    test_results.append(("Dashboard Data", tester.test_dashboard_data()))
    
    # Alert system tests
    test_results.append(("Create Alerts", tester.test_create_alert()))
    test_results.append(("Get Alerts", tester.test_get_alerts()))
    
    # Language and weather tests
    test_results.append(("Translations", tester.test_translations()))
    test_results.append(("Weather Endpoints", tester.test_weather_endpoints()))
    
    # Print final results
    print("\n" + "=" * 50)
    print("📊 FINAL TEST RESULTS")
    print("=" * 50)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_tests = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    
    print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")
    print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if tester.farmer_id:
        print(f"🆔 Test Farmer ID: {tester.farmer_id}")
    
    return 0 if passed_tests == total_tests else 1

if __name__ == "__main__":
    sys.exit(main())