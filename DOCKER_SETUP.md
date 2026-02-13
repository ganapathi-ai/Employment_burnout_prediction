# Docker Hub Setup Guide

## 🐳 Get Docker Hub Username & Password

### Option 1: If You Already Have Docker Hub Account

**Username**: Your Docker Hub username (e.g., `ganapathi18`)

**Password**: Create an Access Token (recommended) instead of using your password

#### Get Access Token:
1. Go to: https://hub.docker.com/settings/security
2. Click **New Access Token**
3. Description: `GitHub Actions`
4. Access permissions: `Read, Write, Delete`
5. Click **Generate**
6. **Copy the token immediately** (you won't see it again!)
7. Use this token as `DOCKER_PASSWORD` in GitHub Secrets

---

### Option 2: Create New Docker Hub Account (2 minutes)

#### Step 1: Sign Up
1. Go to: https://hub.docker.com/signup
2. Fill in:
   - **Docker ID**: Choose a username (e.g., `yourname123`)
   - **Email**: Your email address
   - **Password**: Create a strong password
3. Click **Sign Up**
4. Verify your email

#### Step 2: Create Access Token
1. Log in to Docker Hub
2. Go to: https://hub.docker.com/settings/security
3. Click **New Access Token**
4. Description: `GitHub Actions`
5. Access permissions: `Read, Write, Delete`
6. Click **Generate**
7. **Copy the token** (save it somewhere safe!)

---

## 📝 Add to GitHub Secrets

### Go to GitHub Repository:
https://github.com/ganapathi-ai/Employment_burnout_prediction/settings/secrets/actions

### Add Secret 1: DOCKER_USERNAME
1. Click **New repository secret**
2. Name: `DOCKER_USERNAME`
3. Value: Your Docker Hub username (e.g., `ganapathi18`)
4. Click **Add secret**

### Add Secret 2: DOCKER_PASSWORD
1. Click **New repository secret**
2. Name: `DOCKER_PASSWORD`
3. Value: Your access token (the long string you copied)
4. Click **Add secret**

---

## ✅ Quick Links

- **Docker Hub Sign Up**: https://hub.docker.com/signup
- **Docker Hub Login**: https://hub.docker.com/
- **Create Access Token**: https://hub.docker.com/settings/security
- **GitHub Secrets**: https://github.com/ganapathi-ai/Employment_burnout_prediction/settings/secrets/actions

---

## 🔒 Security Note

**Never use your actual Docker Hub password in GitHub Secrets!**
Always use an Access Token instead. You can revoke tokens anytime without changing your password.

---

## ❓ Troubleshooting

### "Invalid credentials" error
- Make sure you're using an access token, not your password
- Check the token has Read, Write, Delete permissions
- Verify username is correct (case-sensitive)

### Can't find Security settings
- Make sure you're logged in to Docker Hub
- Direct link: https://hub.docker.com/settings/security

---

**After adding both secrets, your GitHub Actions will be able to push Docker images!** 🚀
