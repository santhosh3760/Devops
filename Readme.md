# Signup/Login Flask App

A simple Flask web application that allows users to sign up, log in, and access a dashboard with a welcome message.

## 🛠 Tech Stack

- Python 3.11 (Slim)
- Flask
- PostgreSQL
- HTML/CSS

---

## 🚀 Getting Started

Follow the steps below to set up and run the app locally.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/signupapp.git
cd signupapp
```

### 2. Create a Virtual Environment & Activate

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the root directory and add the following:

```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/your_db_name
```

> ⚠️ Make sure your PostgreSQL server is running, and you’ve created the database mentioned in the `DATABASE_URL`.

### 5. Initialize the Database

```bash
python create_tables.py
```

### 6. Run the Application

```bash
python app.py
```

The app will be accessible at [http://localhost:5000](http://localhost:5000)

---

## 📁 Project Structure

```
signupapp/
├── __pycache__/
├── flask_session/
├── static/
│   └── style.css
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   └── signup.html
├── .env
├── .gitignore
├── app.py
├── create_tables.py
├── app.log*
├── requirements.txt
└── Readme.md
```

---

## 📝 Notes

- This app is for educational/demo purposes.
- You can host it using platforms like Render, Railway, or deploy on your own VM.
- If you want to switch to SQLite for easier testing, let me know and I can help adjust the code.

---

## 📬 Contact

Built with ❤️ by Santhosh  
Feel free to reach out for any feedback or questions.
