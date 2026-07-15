# 🚀 Deploy Guide: Animated GitHub Profile README

This guide walks you through setting up and deploying your animated GitHub Profile README so that it updates automatically on your profile.

---

## 📋 Prerequisites

1. **Git** installed on your system.
2. A **GitHub account** (your username: `devendrarajsingh07`).
3. Your local photo is already saved as `assets/photo.jpg`.

---

## 🛠️ Step 1: Create a GitHub Profile Repository

1. Go to [github.com/new](https://github.com/new).
2. Enter your username `devendrarajsingh07` as the **Repository name**.
   > [!IMPORTANT]
   > The repository name must **exactly match** your GitHub username. This creates the special "Profile README" block on your GitHub home page.
3. Set the repository to **Public** (required for the profile README to display).
4. Do **NOT** initialize with a README, `.gitignore`, or License (we already have these files locally).
5. Click **Create repository**.

---

## 💻 Step 2: Push Your Code to GitHub

Open a terminal (Command Prompt, PowerShell, or Git Bash) inside the project folder `C:\Users\KIIT\.gemini\antigravity\scratch\github-profile-readme\` and run:

```bash
# Initialize git repository
git init -b main

# Add all files
git add .

# Create the initial commit
git commit -m "feat: initial commit for animated profile"

# Link your local repository to GitHub
git remote add origin https://github.com/devendrarajsingh07/devendrarajsingh07.git

# Push your code
git push -u origin main -f
```

---

## ⚙️ Step 3: Configure GitHub Actions Permissions

By default, GitHub Actions workflows do not have write access to your repository. You must enable it so the automated update workflow can commit the daily updated SVGs back to your repository:

1. Go to your repository page: `github.com/devendrarajsingh07/devendrarajsingh07`.
2. Click on **Settings** (gear icon at the top).
3. In the left sidebar, click **Actions** -> **General**.
4. Scroll down to the **Workflow permissions** section.
5. Select **Read and write permissions**.
6. Click **Save**.

---

## ⚡ Step 4: Run the Workflow Manually to Verify

1. Go to the **Actions** tab in your GitHub repository.
2. Select the **Update Profile README** workflow in the left sidebar.
3. Click the **Run workflow** dropdown on the right.
4. Click the green **Run workflow** button.
5. Once it completes, check your profile page (`github.com/devendrarajsingh07`)! You will see:
   - Your ASCII Portrait generated from your photo.
   - Your Neofetch-style info panel with a typing cursor.
   - Your contribution graph with staggered animation.
   - Live updated stats cards.

---

## 🎨 Customization

If you want to update your details, edit `config.yml` locally, commit, and push:
```bash
git add config.yml
git commit -m "chore: update config details"
git push
```
The GitHub Action will automatically detect the push and rebuild your README assets in seconds!
