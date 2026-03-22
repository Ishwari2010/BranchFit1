import requests

session = requests.Session()
base_url = "http://localhost:5000"

# Register/Login
res = session.post(f"{base_url}/register", data={
    "username": "tester",
    "email": "tester@example.com",
    "password": "password123"
}, allow_redirects=True)

# Start test
res = session.get(f"{base_url}/general-test", allow_redirects=True)

# Go to question
res = session.get(f"{base_url}/question")
print(f"Status: {res.status_code}")
print(f"Content Length: {len(res.text)}")
print("HTML Snapshot (first 500 chars):")
print(res.text[:500])

# Check for question text
if "Question 1" in res.text:
    print("✅ Question text found")
else:
    print("❌ Question text NOT found")
