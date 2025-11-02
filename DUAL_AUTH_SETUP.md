# 🎉 DUAL DATABASE AUTHENTICATION - COMPLETE SETUP GUIDE

## ✅ IMPLEMENTATION STATUS: **FULLY WORKING**

---

## 📋 Overview

Successfully implemented a dual database authentication system for the LSC Portal that supports:
1. **Admin Users**: Authenticated from `online_edu.lsc_admins` table
2. **LSC Center Users**: Authenticated from `lsc_portal_db.lsc_auth_lscuser` table

Both user types receive JWT tokens and can access the portal with their respective permissions.

---

## 🏗️ Architecture

### Database Configuration

**Two MySQL Databases:**

1. **online_edu** (Existing database)
   - Table: `lsc_admins`
   - Purpose: Admin/LSC center administrator authentication
   - Connection: Host: localhost, Port: 3306

2. **lsc_portal_db** (New database)
   - Table: `lsc_auth_lscuser`
   - Purpose: LSC center user authentication
   - Connection: Host: localhost, Port: 3306

### Database Router

**File**: `backend/backend/db_router.py`

Routes queries to appropriate database:
- `LSCAdmin` model → `online_edu` database
- `LSCUser` model → `default` (lsc_portal_db) database
- All other models → `default` database

---

## 🔐 Authentication Flow

### 1. User Login Request

```
POST /api/auth/login/
{
  "lscNumber": "LC2101-CDOE",  // or "LC3001"
  "password": "admin123"        // or "user123"
}
```

### 2. Backend Processing

**File**: `backend/lsc_auth/auth_backend.py` - `DualDatabaseAuthBackend`

```python
1. Try to authenticate as LSCAdmin (online_edu.lsc_admins)
2. If not found, try LSCUser (lsc_portal_db.lsc_auth_lscuser)
3. Mark authenticated user with _user_type and _database attributes
```

### 3. JWT Token Generation

**File**: `backend/lsc_auth/views.py` - `LSCLoginView`

```python
# For LSCAdmin
refresh = RefreshToken()
refresh['user_id'] = user.id
refresh['lsc_code'] = user.lsc_code
refresh['user_type'] = 'admin'
refresh['database'] = 'online_edu'

# For LSCUser
refresh = RefreshToken()
refresh['user_id'] = user.id
refresh['lsc_number'] = user.lsc_number
refresh['user_type'] = 'user'
refresh['database'] = 'default'
```

### 4. Response Format

**Admin Login Response:**
```json
{
  "access": "eyJhbGci...",
  "refresh": "eyJhbGci...",
  "user": {
    "id": 1,
    "lsc_code": "LC2101-CDOE",
    "lsc_number": "LC2101-CDOE",
    "lsc_name": "Centre for Distance and Online Education",
    "email": "cdoe@periyar.edu",
    "is_admin": true,
    "user_type": "admin",
    "database": "online_edu"
  },
  "message": "Welcome Admin! Logged in as LSC Admin."
}
```

**LSC User Login Response:**
```json
{
  "access": "eyJhbGci...",
  "refresh": "eyJhbGci...",
  "user": {
    "id": 2,
    "lsc_number": "LC3001",
    "lsc_code": "LC3001",
    "lsc_name": "Salem LSC Center",
    "email": "salem@lsc.periyar.edu",
    "is_active": true,
    "user_type": "user",
    "database": "lsc_portal_db"
  },
  "message": "Welcome Salem LSC Center! Logged in as LSC User."
}
```

---

## 🧪 Testing

### Test Credentials

**Admin User:**
- LSC Code: `LC2101-CDOE`
- Password: `admin123`
- Database: `online_edu.lsc_admins`

**LSC Center User:**
- LSC Number: `LC3001`
- Password: `user123`
- Database: `lsc_portal_db.lsc_auth_lscuser`

### Test Scripts

1. **test_both_logins.py** - Test both authentication types
```bash
python test_both_logins.py
```

2. **test_lsc_user_login.py** - Test LSC user login with full details
```bash
python test_lsc_user_login.py
```

3. **create_test_lsc_user.py** - Create additional test LSC users
```bash
python create_test_lsc_user.py
```

---

## 📁 Modified Files

### Backend Files

1. **backend/backend/settings.py**
   - Added dual database configuration
   - Configured DATABASE_ROUTERS

2. **backend/backend/db_router.py** (New)
   - Custom database router for query routing

3. **backend/lsc_auth/models.py**
   - Updated `LSCAdmin` with `managed=False`, explicit `db_table`
   - Updated `LSCUser` with explicit `db_table`

4. **backend/lsc_auth/auth_backend.py** (New)
   - `DualDatabaseAuthBackend` class
   - Sequential authentication checking

5. **backend/lsc_auth/views.py**
   - Updated `LSCLoginView` for dual authentication
   - Custom JWT token generation for both user types

6. **backend/lsc_auth/urls.py**
   - Registered login/logout endpoints

### Database Setup

7. **create_auth_user_table.py** (New)
   - Creates `auth_user` table in `lsc_portal_db`
   - Required for Django's JWT authentication

---

## 🚀 Deployment Steps

### 1. Database Setup

```bash
# Create lsc_portal_db database
mysql -u root -p
CREATE DATABASE lsc_portal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# Run migrations
cd backend
python manage.py migrate
python create_auth_user_table.py
```

### 2. Create Test Users

```bash
# Create LSC test user
python create_test_lsc_user.py
```

### 3. Start Backend Server

```bash
python manage.py runserver
```

### 4. Start Frontend (if needed)

```bash
cd ../frontend
npm install
npm run dev
```

---

## 🔍 JWT Token Claims

### Admin Token Claims:
```json
{
  "token_type": "access",
  "user_id": 1,
  "lsc_code": "LC2101-CDOE",
  "lsc_name": "Centre for Distance and Online Education",
  "is_admin": true,
  "email": "cdoe@periyar.edu",
  "user_type": "admin",
  "database": "online_edu"
}
```

### LSC User Token Claims:
```json
{
  "token_type": "access",
  "user_id": 2,
  "lsc_number": "LC3001",
  "lsc_name": "Salem LSC Center",
  "email": "salem@lsc.periyar.edu",
  "user_type": "user",
  "database": "default"
}
```

---

## 🎯 Frontend Integration

### Stored in localStorage:

```javascript
// After successful login:
localStorage.setItem('access_token', access);
localStorage.setItem('refresh_token', refresh);
localStorage.setItem('user_info', JSON.stringify(user));

// User info includes:
{
  "user_type": "admin" | "user",
  "database": "online_edu" | "lsc_portal_db",
  "lsc_code" | "lsc_number": "...",
  "lsc_name": "...",
  // ... other user fields
}
```

### Permission-Based UI:

```javascript
// Check user type
const userInfo = JSON.parse(localStorage.getItem('user_info'));
if (userInfo.user_type === 'admin') {
  // Show admin features
} else {
  // Show regular user features
}
```

---

## 🛠️ Troubleshooting

### Issue: "Table 'lsc_portal_db.auth_user' doesn't exist"

**Solution:**
```bash
python create_auth_user_table.py
```

### Issue: Admin login works but user login fails

**Check:**
1. Is `lsc_portal_db` database created?
2. Are migrations run?
3. Is `auth_user` table present?
4. Is `DualDatabaseAuthBackend` in `AUTHENTICATION_BACKENDS`?

### Issue: JWT tokens not generated

**Check:**
1. Is `rest_framework_simplejwt` installed?
2. Is `SECRET_KEY` set in settings.py?
3. Are custom token claims properly set?

---

## ✅ Verification Checklist

- [x] Dual database configuration working
- [x] Database router routing queries correctly
- [x] Admin authentication from `online_edu.lsc_admins`
- [x] LSC user authentication from `lsc_portal_db.lsc_auth_lscuser`
- [x] JWT tokens generated for both user types
- [x] User type identified in token claims
- [x] Frontend storing user info in localStorage
- [x] Both login types tested and working
- [x] Test scripts created and validated

---

## 📊 Performance Notes

- Database router adds minimal overhead
- Queries are routed to correct database automatically
- No cross-database queries needed
- Each authentication check is isolated
- JWT tokens are stateless and efficient

---

## 🔮 Future Enhancements

1. **Role-Based Access Control (RBAC)**
   - Define roles beyond admin/user
   - Implement permission checks in views

2. **Audit Logging**
   - Track login attempts
   - Log authentication failures

3. **Password Policies**
   - Enforce password complexity
   - Implement password expiration

4. **Multi-Factor Authentication (MFA)**
   - Add SMS/Email OTP
   - Support authenticator apps

---

## 📞 Support

For issues or questions:
1. Check test scripts for working examples
2. Verify database connections
3. Check Django logs for detailed errors
4. Ensure all migrations are applied

---

**Last Updated:** January 2025
**Status:** ✅ Production Ready
**Version:** 1.0.0
