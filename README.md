# 📊 Petkit Dashboard

A **local dashboard** for visualizing and analyzing data collected from Petkit smart devices.  
Built with **PostgreSQL, and Pandas**, the dashboard provides clear insights into pet health trends such as **feeding, drinking, and weight**.

---

## 📖 Overview
Petkit devices generate valuable IoT data, but the official app offers limited visibility and customization.  
This project provides a **custom analytics dashboard** that integrates with the **Petkit Logger** database and surfaces **actionable insights**.  

The dashboard is used to feed into **DAKboard displays** for at-a-glance monitoring in the home.

---

## 🚀 Features
 ✅ Visualize long-term pet trends (feeding, water intake, weight)  
 ✅ Filter data by pet, device, and time range  
 ✅ Interactive charts built with Plotly 
 ✅ Configurable to run locally or on a home server   
 ✅ Integrates with DAKboard for smart-home display  
 ✅ Modular design for adding new visualizations  

---

## 🛠 Tech Stack
- **Languages**: Python 3.11  
- **Data**: PostgreSQL, Pandas, SQLAlchemy  
- **Visualization**: Plotly  
- **Infra**: Docker, GitHub Actions  

---

## ⚙️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/williewu-projects/Petkit_Dashboard.git
   cd Petkit_Dashboard
2. Create a virtual environment & install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
3. Configure environment variables in .env:
   ```
   DB_HOST=localhost
   DB_PORT=5433
   DB_USER=[youruser]
   DB_PASS=[yourpassword]
   DB_NAME=[petkit]
   GITHUB_REPO=[your repo]
   GITHUB_PAT=[your github personal access token]
   GITHUB_USERNAME=[github username]
   GIT_AUTHOR_NAME=[author name]
   GIT_AUTHOR_EMAIL=[author email]
4. Run with Docker   
   ###Build the Image
   ```bash
   docker build -t Petkit_Dashboard

   ###Run the Container
   ```bash
   docker run -d \
  --name Petkit_Dashboard \
  --env-file .env \
  <Petkit_Dashboard

## 📊 Screenshots

<img width="1043" height="322" alt="image" src="https://github.com/user-attachments/assets/28d1c38b-e031-47ef-aca6-ae5a4d6385cd" />

## 📜 License
MIT License © 2025 Willie Wu
