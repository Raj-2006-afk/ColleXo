# ColleXo Setup Guide

## Complete Setup Instructions

### Prerequisites

1. **Python 3.8+** installed
2. **Node.js 16+** and npm installed
3. **XAMPP** installed with MySQL
4. **Git** (optional, for version control)

---

## Step-by-Step Setup

### 1. Start MySQL Database

1. Open **XAMPP Control Panel**
2. Click **Start** next to MySQL
3. Ensure MySQL is running on port 3306 (default)

> **Note**: The application will automatically create the database and tables on first run!

---

### 2. Backend Setup

Open a terminal and navigate to the backend directory:

```powershell
cd backend
```

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Start the Flask server:

```powershell
python app.py
```

**Expected Output:**

```
============================================================
🚀 ColleXo Backend Starting...
============================================================
📍 Server: http://localhost:5000
📊 Database: MySQL (localhost:3306)
============================================================
🔧 Initializing Database...
✅ Database 'collexo' ready
✅ Table 'users' ready
✅ Table 'societies' ready
✅ Table 'forms' ready
✅ Table 'applications' ready
✅ Seed data inserted successfully!

=== DEFAULT CREDENTIALS ===
Admin: admin@csms.local / admin123
Tech Head: tech.head@csms.local / head123
Arts Head: arts.head@csms.local / head123
Student: student@csms.local / student123
===========================
```

The backend is now running at **http://localhost:5000**

---

### 3. Frontend Setup

Open a **NEW** terminal window and navigate to the frontend directory:

```powershell
cd frontend
```

Install Node.js dependencies:

```powershell
npm install
```

Start the Vite development server:

```powershell
npm run dev
```

**Expected Output:**

```
  VITE v5.0.8  ready in 324 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

The frontend is now running at **http://localhost:5173**

---

## 4. Access the Application

Open your browser and go to:

```
http://localhost:5173
```

### Login with Demo Accounts

| Role             | Email                | Password   |
| ---------------- | -------------------- | ---------- |
| **Student**      | student@csms.local   | student123 |
| **Society Head** | tech.head@csms.local | head123    |
| **Admin**        | admin@csms.local     | admin123   |

---

## Troubleshooting

### Backend Issues

#### Error: `mysql.connector.errors.DatabaseError: 2003`

- **Solution**: MySQL is not running. Start MySQL in XAMPP.

#### Error: `ModuleNotFoundError: No module named 'flask'`

- **Solution**: Install dependencies again:
  ```powershell
  pip install -r requirements.txt
  ```

#### Error: `Port 5000 is already in use`

- **Solution**: Kill the process using port 5000 or change the port in `app.py`.

---

### Frontend Issues

#### Error: `Cannot find module 'react'`

- **Solution**: Delete node_modules and reinstall:
  ```powershell
  Remove-Item -Recurse -Force node_modules
  npm install
  ```

#### Error: `Failed to fetch` or API errors

- **Solution**: Ensure the backend is running on http://localhost:5000

#### Blank page after login

- **Solution**: Clear browser cache and local storage, then refresh.

---

## Project Structure

```
ColleXo/
├── backend/               # Flask API
│   ├── app.py            # Main entrypoint
│   ├── config/           # Database configuration
│   ├── models/           # Data models
│   ├── controllers/      # Business logic
│   ├── routes/           # API endpoints
│   ├── middleware/       # Auth middleware
│   └── requirements.txt  # Python dependencies
│
├── frontend/             # React app
│   ├── src/
│   │   ├── main.jsx     # Entry point
│   │   ├── App.jsx      # Root component
│   │   ├── api/         # API client
│   │   ├── context/     # Auth context
│   │   ├── router/      # Routing
│   │   ├── components/  # Reusable components
│   │   ├── pages/       # Page components
│   │   └── styles/      # Global styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## Testing the Application

### As a Student

1. Login with: `student@csms.local / student123`
2. Browse societies
3. View your applications

### As a Society Head

1. Login with: `tech.head@csms.local / head123`
2. Manage your society
3. Create forms
4. View and manage applications

### As an Admin

1. Login with: `admin@csms.local / admin123`
2. View all societies
3. Manage users
4. View system statistics

---

## Next Steps

- Create new student accounts via the Register page
- Society heads can update their society profiles
- Admins can approve/disable societies
- Students can apply to open societies

---

## Development Commands

### Backend

```powershell
# Run backend
python app.py

# Install new package
pip install package_name
pip freeze > requirements.txt
```

### Frontend

```powershell
# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Ensure all prerequisites are installed
3. Verify MySQL is running
4. Check terminal output for error messages

---

**Happy coding! 🚀**
