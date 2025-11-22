# 🚀 ColleXo - Quick Start Guide

## Prerequisites Check

- [ ] Python 3.8+ installed
- [ ] XAMPP installed
- [ ] Virtual environment created (already done: `venv/`)

---

## 🏃 3-Step Launch

### Step 1: Start MySQL

1. Open **XAMPP Control Panel**
2. Click **Start** next to **MySQL**
3. Verify it's running (green background)

### Step 2: Install Dependencies

```bash
# Double-click setup.bat
# OR run manually:
cd backend
pip install -r requirements.txt
```

### Step 3: Start Application

```bash
# Double-click run.bat
# OR run manually:
python backend\app.py
```

**That's it!** 🎉

---

## 🌐 Access the Application

Open your browser and visit:

- **Homepage:** http://localhost:5000
- **Login:** http://localhost:5000/login
- **Register:** http://localhost:5000/register
- **Browse Societies:** http://localhost:5000/api/societies/browse

---

## 🔑 Login Credentials

### Test as Admin

```
Email: admin@collexo.com
Password: admin123
```

### Test as Student

```
Email: student@collexo.com
Password: student123
```

### Test as Society Head

```
Email: john@collexo.com
Password: head123
```

---

## ✅ What Happens on First Run?

The application automatically:

1. ✅ Connects to MySQL
2. ✅ Creates `collexo` database
3. ✅ Creates 4 tables (USERS, SOCIETIES, FORMS, APPLICATIONS)
4. ✅ Inserts sample data:
   - 4 users (1 admin, 2 society heads, 1 student)
   - 2 societies (Tech Club, Drama Society)
   - 1 recruitment form
5. ✅ Starts server on port 5000

**Zero manual database setup required!**

---

## 📝 Quick Feature Test

### As Student:

1. Login with `student@collexo.com`
2. Browse societies
3. Apply to Tech Club
4. Check application status

### As Society Head:

1. Login with `john@collexo.com`
2. View your society (Tech Club)
3. Check applications
4. Update application status (Accept/Reject)

### As Admin:

1. Login with `admin@collexo.com`
2. View all users
3. View all societies
4. Check platform statistics

---

## 🧪 Test the API

### Using Browser:

- GET http://localhost:5000/api/societies/browse
- GET http://localhost:5000/api/forms/published

### Using Postman:

1. Import `docs/postman.json`
2. Login to get token
3. Set token in collection variable
4. Test all 23 endpoints

---

## 🐛 Troubleshooting

### Problem: Can't connect to database

**Solution:**

- Ensure XAMPP MySQL is running
- Check port 3306 is not blocked
- Verify MySQL is on localhost

### Problem: Import errors

**Solution:**

```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

### Problem: Port 5000 in use

**Solution:** Edit `backend/app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Problem: Module not found

**Solution:** Activate virtual environment:

```bash
venv\Scripts\activate
```

---

## 📚 Next Steps

1. **Read Documentation:**

   - `README.md` - Full project documentation
   - `docs/schema.md` - Database schema
   - `docs/PROJECT_SUMMARY.md` - Complete feature list

2. **Explore Code:**

   - `backend/models/` - Database operations
   - `backend/routes/` - API endpoints
   - `frontend/templates/` - Web pages

3. **Test APIs:**

   - Import Postman collection
   - Test all endpoints
   - Check response formats

4. **Customize:**
   - Add your own societies
   - Create new forms
   - Test application workflow

---

## 🎯 Verify Installation

Run these checks:

```python
# Check Python
python --version  # Should be 3.8+

# Check packages
pip list | findstr Flask  # Should show Flask 3.0.0

# Check database (in MySQL)
SHOW DATABASES;  # Should show 'collexo'
USE collexo;
SHOW TABLES;  # Should show 4 tables
```

---

## 💡 Tips

- Keep XAMPP running while using the app
- Use Chrome/Firefox DevTools to see API calls
- Check terminal for application logs
- Database auto-resets on each run (seed data)

---

## 🆘 Need Help?

1. Check `README.md` for detailed docs
2. Review `docs/schema.md` for database info
3. Import `docs/postman.json` for API examples
4. Check terminal logs for error messages

---

## 🎉 Success Indicators

You'll know everything is working when:

- ✅ No errors in terminal
- ✅ Can access http://localhost:5000
- ✅ Can login with test credentials
- ✅ Can see societies list
- ✅ Dashboards load correctly

---

**Enjoy ColleXo!** 🚀

_If you see the homepage and can login, you're all set!_
