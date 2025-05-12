Backend Setup
mkdir backend
cd backend
python -m venv venv
.\venv\Scripts\activate


uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --ssl-keyfile=certs/key.pem --ssl-certfile=certs/cert.pem


Frontend setup
mkdir frontend
npm install
npm run dev


CURL

curl -X POST https://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"testuser\", \"password\": \"testpass\"}" -k



curl -X POST https://localhost:8000/recommend \
  -H "Authorization: Bearer *******" \
  -H "Content-Type: application/json" \
  -d "{\"spends\": {\"dining\": 1200, \"travel\": 2000, \"groceries\": 2500}}" -k


curl https://localhost:8000/last_parsed -k


