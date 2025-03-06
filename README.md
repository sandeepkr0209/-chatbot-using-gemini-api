# -chatbot-using-gemini-api
🤖 AI Chatbot with Chat History
A smart AI chatbot built with Flask (Python) and MongoDB, featuring user authentication (email/password & Google Login), "Remember Me" session persistence, and chat history storage.

🚀 Features
✅ User Authentication (Email/Password & Google OAuth)
✅ "Remember Me" Session Persistence
✅ Chat History (Stored & Retrieved from MongoDB)
✅ Voice Input (Speech-to-Text)
✅ File Attachments
✅ Offline Responses (Predefined AI replies when offline)

🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Flask (Python), Flask-Session, Flask-CORS
Database: MongoDB (Stores user & chat data)
Authentication: Google OAuth + bcrypt for password hashing
📌 Installation & Setup
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/chatbot.git
cd chatbot
2️⃣ Install Dependencies
bash
Copy
Edit
pip install flask flask-cors pymongo bcrypt flask-session google-auth-oauthlib google-auth google-auth-httplib2
3️⃣ Set Up MongoDB
Install MongoDB & start the server
Create a database: chatbot_db
4️⃣ Run the Backend
bash
Copy
Edit
python server.py
5️⃣ Run the Frontend
Simply open index.html in your browser.

🌍 Deployment
Deploy Backend on Render/Vercel
Push your code to GitHub
Connect GitHub repo to Render/Vercel
Add environment variables
Deploy 🚀
📸 Screenshots
(Add chatbot UI screenshots here)

📧 Contact & Contributions
Contributions are welcome! Feel free to submit a PR.
