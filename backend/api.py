
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
import logging
import requests
 
load_dotenv()
 
app = Flask(__name__)
CORS(app)
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
# Configuration
DYNATRACE_ENV_URL = os.getenv("DYNATRACE_ENVIRONMENT_URL")
DYNATRACE_API_TOKEN = os.getenv("DYNATRACE_API_TOKEN")
GCP_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
AGENT_ID = os.getenv("AGENT_ID")
 
# ============================================
# DYNATRACE CLIENT
# ============================================
 
class DynatraceMCPClient:
    def __init__(self, env_url, api_token):
        self.env_url = env_url
        self.api_token = api_token
        self.base_url = f"{env_url}/api/v2"
    
    def get_headers(self):
        return {
            "Authorization": f"Api-Token {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def list_problems(self, status="OPEN", limit=10):
        url = f"{self.base_url}/problems"
        params = {"status": status, "limit": limit}
        
        try:
            response = requests.get(url, headers=self.get_headers(), params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("problems", [])
        except Exception as e:
            logger.error(f"Error listing problems: {e}")
            return []
    
    def get_problem(self, problem_id):
        url = f"{self.base_url}/problems/{problem_id}"
        
        try:
            response = requests.get(url, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting problem: {e}")
            return None
    
    def query_logs(self, query, time_from="now-1h", time_to="now", limit=50):
        url = f"{self.base_url}/logs/query"
        payload = {"query": query, "timeFrom": time_from, "timeTo": time_to, "limit": limit}
        
        try:
            response = requests.post(url, headers=self.get_headers(), json=payload, timeout=10)
            response.raise_for_status()
            return response.json().get("records", [])
        except Exception as e:
            logger.error(f"Error querying logs: {e}")
            return []
 
# Initialize client
dt_client = DynatraceMCPClient(DYNATRACE_ENV_URL, DYNATRACE_API_TOKEN)
 
# ============================================
# API ENDPOINTS
# ============================================
 
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})
 
@app.route("/api/problems", methods=["GET"])
def get_problems():
    try:
        problems = dt_client.list_problems(status="OPEN")
        return jsonify({"count": len(problems), "problems": problems})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    problem_id = data.get("problemId")
    
    if not problem_id:
        return jsonify({"error": "problemId required"}), 400
    
    # Fetch problem from Dynatrace
    problem = dt_client.get_problem(problem_id)
    if not problem:
        return jsonify({"error": f"Problem {problem_id} not found"}), 404
    
    # Return demo analysis (in production, would call Gemini Agent)
    return jsonify({
        "thinking": "Analyzing the problem. Database connection pool is exhausted. Response times spiked. This correlates with v3.2.1 deployment.",
        "analysis": {
            "rootCause": "Database connection pool exhaustion due to connection leak in v3.2.1",
            "affectedServices": ["checkout-api", "payment-service"],
            "businessImpact": {
                "usersAffected": 4200,
                "estimatedRevenueLoss": "$12,000 per minute",
                "criticalityLevel": "P1 - Fan experience blocked"
            },
            "evidence": [
                "Connection pool at 95%",
                "Response time spiked from 200ms to 8000ms",
                "Spike started at v3.2.1 deployment"
            ],
            "recommendedActions": [
                "Roll back to v3.2.0",
                "OR increase connection pool to 200"
            ],
            "estimatedTTR": "12 minutes"
        }
    })
 
@app.route("/api/demo", methods=["POST"])
def demo_analysis():
    return jsonify({
        "thinking": "Database connection pool exhaustion detected. All 100 connections in use. Response times at 8000ms. Started after v3.2.1 deployment.",
        "analysis": {
            "rootCause": "Connection leak in v3.2.1 eager-loading implementation",
            "affectedServices": ["checkout-api"],
            "businessImpact": {
                "usersAffected": 4200,
                "estimatedRevenueLoss": "$12,000 per minute",
                "criticalityLevel": "P1"
            },
            "evidence": [
                "Connection pool full at 100/100",
                "Response time 200ms → 8000ms",
                "Correlates with v3.2.1 deploy"
            ],
            "recommendedActions": [
                "Roll back to v3.2.0 (5 min)"
            ],
            "estimatedTTR": "12 minutes"
        }
    })
 
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)