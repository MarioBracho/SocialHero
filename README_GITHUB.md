# 🍹 Amity Drinks - Social Hero Dashboard

> Real-time influencer monitoring dashboard for Instagram & Facebook campaigns

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-Private-red?style=for-the-badge)](LICENSE)

## 📊 Overview

**Amity Social Hero** is a comprehensive web dashboard for tracking influencer campaigns across Instagram and Facebook. Built with Streamlit, it provides real-time monitoring, analytics, and reporting for your influencer marketing efforts.

### ✨ Key Features

- 🔐 **Secure Authentication** - Password-protected access
- 📱 **Multi-Platform** - Instagram & Facebook integration
- 📊 **Real-time Analytics** - Live tracking of posts, stories, and reels
- 🎯 **Goal Tracking** - Monitor influencer performance against targets
- 📈 **Visual Reports** - Beautiful charts and leaderboards
- 📧 **Email Notifications** - Automatic alerts for new content
- 📥 **Excel Export** - Monthly performance reports
- 🎨 **Brand Design** - Custom Amity Drinks styling

## 🚀 Quick Deployment

### Prerequisites

- GitHub account (free)
- Streamlit Cloud account (free) - [Sign up here](https://streamlit.io/cloud)
- Meta API credentials (optional - works without)

### Deploy in 5 Minutes

1. **Fork or Clone this Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/amity-social-hero.git
   cd amity-social-hero
   ```

2. **Push to Your GitHub**
   ```bash
   git remote set-url origin https://github.com/YOUR_USERNAME/amity-social-hero.git
   git push -u origin main
   ```

3. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Main file: `dashboard.py`
   - Click "Advanced settings" → "Secrets"
   - Copy-paste content from `.streamlit/secrets.toml.example`
   - Update with your credentials
   - Click "Deploy"!

4. **Access Your Dashboard**
   - Your app will be live at: `https://your-app.streamlit.app`
   - Login with credentials from secrets

## 🔐 Security Setup

### Creating secrets.toml for Streamlit Cloud

In Streamlit Cloud's Advanced Settings → Secrets, paste:

```toml
[passwords]
username = "your_username"
password = "your_secure_password"

# Meta API (optional - dashboard works without these)
META_APP_ID = "your_app_id"
META_APP_SECRET = "your_app_secret"
META_ACCESS_TOKEN = "your_access_token"
FACEBOOK_PAGE_ACCESS_TOKEN = "your_page_token"
INSTAGRAM_BUSINESS_ACCOUNT_ID = "your_ig_id"
FACEBOOK_PAGE_ID = "your_fb_page_id"

# Email notifications
EMAIL_TO = "your@email.com"
```

### ⚠️ Security Best Practices

- ✅ Keep your GitHub repository **PRIVATE**
- ✅ Never commit `.env` or `secrets.toml` files
- ✅ Use strong passwords for dashboard access
- ✅ Rotate Meta API tokens every 60 days
- ✅ Enable 2FA on GitHub and Streamlit Cloud

## 📱 Features in Detail

### Dashboard Sections

1. **Overview Metrics**
   - Total active influencers
   - Goal completion rates
   - Total posts and reach

2. **Performance Tracking**
   - Individual influencer statistics
   - Stories, posts, and reels breakdown
   - Progress vs. monthly targets

3. **Leaderboards**
   - Top performers by post count
   - Highest reach influencers

4. **Post Browser**
   - Filter by influencer
   - View all posts with details
   - Direct links to content

5. **Quick Actions**
   - Manual post addition
   - Instagram synchronization
   - Excel report generation

## 🛠️ Local Development

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/amity-social-hero.git
cd amity-social-hero

# Install dependencies
pip install -r requirements_web.txt

# Create .streamlit/secrets.toml
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml with your credentials

# Run dashboard
streamlit run dashboard.py
```

### Project Structure

```
amity-social-hero/
├── dashboard.py          # Main Streamlit app
├── src/
│   ├── api/             # Meta API client
│   ├── database/        # SQLite database manager
│   ├── monitoring/      # Background monitoring
│   ├── reporting/       # Excel report generation
│   └── utils/           # Config and helpers
├── .streamlit/
│   ├── config.toml      # Streamlit configuration
│   └── secrets.toml     # Credentials (gitignored)
├── requirements_web.txt # Production dependencies
└── README.md           # This file
```

## 📚 Documentation

- **[Deployment Guide](NASAZENI_NA_WEB.md)** - Detailed deployment instructions (Czech)
- **[Quick Start](QUICKSTART_NASAZENI.md)** - 15-minute deployment guide (Czech)
- **[Authentication Setup](PRIDANI_AUTENTIZACE.md)** - Adding password protection (Czech)
- **[Meta API Setup](Influencer%20boss/META_API_SETUP.md)** - Facebook/Instagram API configuration

## 🔄 Updating the App

When you make changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud will automatically redeploy your app!

## 🆘 Troubleshooting

### Common Issues

**"Invalid credentials"**
- Check that secrets are correctly set in Streamlit Cloud Settings
- Verify username and password match what you set

**"ModuleNotFoundError"**
- Ensure `requirements_web.txt` is in the repository root
- Check that all dependencies are listed

**"Meta API error"**
- Verify API tokens are current (60-day expiry)
- Dashboard works without Meta API - just shows empty data

**Dashboard not updating**
- Check Streamlit Cloud logs in App Settings
- Click "Reboot app" in Streamlit Cloud

## 🎨 Customization

### Changing Brand Colors

Edit `dashboard.py` CSS section (line ~105):

```python
# Primary color
#C8A43B → your hex color

# Background
#F5F0E8 → your background
```

### Changing Login Credentials

Update in Streamlit Cloud Settings → Secrets:

```toml
[passwords]
username = "new_username"
password = "new_password"
```

## 📊 Data Management

### Database

- SQLite database stores all posts and statistics
- Located at: `data/influencer_monitor.db`
- **Note**: Streamlit Cloud doesn't persist database between restarts
- For production, consider connecting PostgreSQL

### Backups

- Export monthly reports before major updates
- Download database via Streamlit if needed
- Keep influencer list backed up

## 🤝 Support

For issues or questions:
- 📧 Email: marian@amitydrinks.cz
- 📝 Create an issue in this repository

## 📄 License

This project is proprietary software for Amity Drinks s.r.o.
Unauthorized copying or distribution is prohibited.

---

<div align="center">

**Built with ❤️ for Amity Drinks**

🍹 *dobrota je uvnitř*

</div>
