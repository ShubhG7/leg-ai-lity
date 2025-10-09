# Security Guidelines

## 🔒 Environment Variables & Secrets

### Current Setup

All sensitive credentials are stored in environment variables, **NOT** hardcoded in the source code:

1. **Google Gemini API Key** (`GEMINI_API_KEY`)
2. **JWT Secret Key** (`JWT_SECRET_KEY`)
3. **Demo User Credentials** (`DEMO_USER_EMAIL`, `DEMO_USER_PASSWORD`, `DEMO_USER_NAME`)

### ✅ What's Protected

- `.env` files are in `.gitignore` and **will NOT be committed to git**
- `.env.example` provides a template with placeholder values
- All secrets should be set via environment variables in production

### 🚨 Important: GitGuardian Alert

If you received a GitGuardian alert about hardcoded credentials:

1. **The credentials have been moved to environment variables** ✅
2. **The .env file is NOT tracked by git** ✅
3. **Change your demo password** in the `.env` file immediately
4. **For production deployment**, use different, secure credentials

## 🔐 Production Deployment Checklist

### Backend (.env file)

```bash
# REQUIRED: Change ALL of these in production!

# Google Gemini API Key (get from https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your_production_gemini_api_key

# JWT Secret (generate a secure random string)
JWT_SECRET_KEY=$(openssl rand -hex 32)

# Demo User (CHANGE THESE!)
DEMO_USER_EMAIL=admin@yourdomain.com
DEMO_USER_PASSWORD=$(openssl rand -base64 16)
DEMO_USER_NAME=Admin User
```

### Generate Secure Secrets

```bash
# Generate a secure JWT secret
openssl rand -hex 32

# Generate a secure password
openssl rand -base64 16

# Or use Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 📋 Deployment Steps

### 1. Vercel (Frontend)

No secrets needed for frontend deployment.

### 2. Render/Railway (Backend)

Set these environment variables in your deployment platform:

```
GEMINI_API_KEY=<your-production-key>
JWT_SECRET_KEY=<generated-secure-secret>
DEMO_USER_EMAIL=<your-admin-email>
DEMO_USER_PASSWORD=<generated-secure-password>
DEMO_USER_NAME=<your-admin-name>
```

### 3. Other Platforms (Heroku, AWS, etc.)

Use the platform's environment variable configuration:

- Heroku: `heroku config:set KEY=value`
- AWS: Use Parameter Store or Secrets Manager
- Docker: Use docker-compose.yml with env_file or secrets

## 🛡️ Security Best Practices

### Current Implementation (Development/Demo)

✅ Environment variables for all secrets
✅ .gitignore properly configured
✅ .env.example for reference
✅ Simple password hashing (SHA256)

### Production Recommendations

1. **Use a proper database** instead of in-memory storage
2. **Implement bcrypt** for password hashing (commented in code)
3. **Enable HTTPS** for all production traffic
4. **Use rate limiting** on API endpoints
5. **Implement refresh tokens** for better security
6. **Add input validation** and sanitization
7. **Use environment-specific configs** (dev/staging/prod)
8. **Monitor for security vulnerabilities** regularly
9. **Implement proper user roles** and permissions
10. **Use secrets management services** (AWS Secrets Manager, HashiCorp Vault)

## 🔍 How to Verify Security

### Check if .env is tracked by git:

```bash
git ls-files | grep .env
# Should only show .env.example, NOT .env
```

### Check .gitignore:

```bash
cat .gitignore | grep .env
# Should show .env patterns
```

### Verify environment variables are loaded:

```bash
cd backend
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('JWT Key:', os.getenv('JWT_SECRET_KEY')[:10] + '...')"
```

## 📝 User Management

### Current System

- **In-memory storage** (for demo purposes)
- **Demo user** created from environment variables
- **New users** can register (stored in memory during runtime)
- **Users are lost** when server restarts (by design for demo)

### For Production

Replace with:
- PostgreSQL/MySQL database
- Proper user tables with indexes
- Password reset functionality
- Email verification
- Two-factor authentication (2FA)
- OAuth integration (Google, GitHub, etc.)

## 🚀 Quick Start for New Developers

1. Copy `.env.example` to `.env`:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Get a Gemini API key:
   - Visit: https://aistudio.google.com/app/apikey
   - Create a new API key
   - Add to `.env`: `GEMINI_API_KEY=your_key_here`

3. Generate a JWT secret:
   ```bash
   openssl rand -hex 32
   # Add to .env: JWT_SECRET_KEY=<generated_secret>
   ```

4. Set demo credentials:
   ```bash
   # Edit .env file
   DEMO_USER_EMAIL=demo@lexsy.ai
   DEMO_USER_PASSWORD=your_secure_password
   DEMO_USER_NAME=Demo User
   ```

5. Never commit `.env` file to git!

## 🆘 If You Accidentally Committed Secrets

1. **Immediately rotate all secrets** (new API keys, new JWT secret)
2. **Remove from git history**:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch backend/.env" \
     --prune-empty --tag-name-filter cat -- --all
   ```
3. **Force push** (CAREFULLY):
   ```bash
   git push origin --force --all
   ```
4. **Update all deployment environments** with new secrets

## 📞 Security Contacts

For security concerns or vulnerabilities:
- Create a private issue in the repository
- Contact the maintainers directly
- Do not disclose vulnerabilities publicly

---

**Last Updated**: October 2024
**Status**: ✅ All secrets are environment-based and secure

