
import os
import sys
from dotenv import load_dotenv
import requests
 
load_dotenv()
 
DYNATRACE_ENV_URL = os.getenv("DYNATRACE_ENVIRONMENT_URL")
DYNATRACE_API_TOKEN = os.getenv("DYNATRACE_API_TOKEN")
 
if not DYNATRACE_ENV_URL or not DYNATRACE_API_TOKEN:
    print("❌ Missing Dynatrace credentials in .env")
    sys.exit(1)
 
url = f"{DYNATRACE_ENV_URL}/api/v2/problems"
headers = {
    "Authorization": f"Api-Token {DYNATRACE_API_TOKEN}",
    "Content-Type": "application/json"
}
 
print(f"Testing Dynatrace connection...")
print(f"URL: {DYNATRACE_ENV_URL}")
 
try:
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ SUCCESS! Connected to Dynatrace")
        print(f"  Problems found: {len(data.get('problems', []))}")
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(f"  Response: {response.text}")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)