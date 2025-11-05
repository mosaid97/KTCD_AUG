# 🎓 KTCD_Aug - Knowledge Tracing & Cognitive Diagnosis Platform

**An intelligent educational platform powered by Knowledge Graphs and AI**

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.12-blue)]()
[![Flask](https://img.shields.io/badge/flask-latest-lightgrey)]()
[![Neo4j](https://img.shields.io/badge/neo4j-graph%20database-green)]()

> 📖 **Complete Documentation**: See [`ULTIMATE_PROJECT_SUMMARY.md`](ULTIMATE_PROJECT_SUMMARY.md) for comprehensive project details, architecture, and technical specifications.

---

## 🚀 Quick Start

### **1. Start the System**
```bash
# Start Neo4j database
docker-compose up -d

# Run the application
python3 nexus_app.py
```

### **2. Access the Platform**
```
URL: http://127.0.0.1:8084/student/login

Test Student:
Email: roma@example.com
Password: roma123

Debugger PIN: 475-321-601
```

### **3. Explore Features**
- 📚 Browse 5 topics in Big Data Analysis
- 📹 Watch educational videos
- 🧪 Complete interactive labs
- ❓ Take graded quizzes
- 📊 Track your progress

---

## ✨ Features

### **For Students**:
- ✅ **Personalized Learning** - AI-powered content adaptation
- ✅ **Interactive Labs** - Jupyter-style coding notebooks
- ✅ **Video Lectures** - 15 educational videos
- ✅ **Graded Assessments** - Quizzes and exams
- ✅ **Progress Tracking** - Real-time analytics dashboard
- ✅ **AI Chatbot** - 24/7 learning assistance
- ✅ **Cognitive Diagnosis** - Concept-level mastery tracking

### **For Educators**:
- ✅ **Knowledge Graph** - Structured content organization
- ✅ **Analytics** - Student performance insights
- ✅ **Adaptive Assessments** - Dynamic question generation
- ✅ **Progress Monitoring** - Real-time tracking

### **NEW: Theory-Based Blog Scraper**:
- ✅ **Automatic Content Discovery** - Scrapes 8 trusted sources
- ✅ **Relevance Evaluation** - 5-metric evaluation system
- ✅ **Quality Filtering** - Threshold-based filtering
- ✅ **Hybrid Content** - Generated + scraped blogs
- ✅ **Trusted Sources** - arXiv, Wikipedia, GitHub, Dev.to, Medium, Coursera, edX, Hashnode

---

## 📊 System Overview

### **Knowledge Graph**:
- **310 Nodes**: Classes, Topics, Concepts, Videos, Labs, Quizzes
- **935 Relationships**: Structured learning paths
- **47 Concepts**: Comprehensive coverage
- **15 Videos**: 3 per topic
- **21 Labs**: Interactive practice
- **5 Quizzes**: Graded assessments

### **Technology Stack**:
- **Backend**: Python 3.12, Flask
- **Database**: Neo4j (Graph Database)
- **Frontend**: HTML5, JavaScript, Tailwind CSS
- **AI**: OpenAI API (Chatbot & Content Generation)
- **Visualization**: Chart.js

---

## 📁 Project Structure

```
KTCD_Aug/
├── routes/          # Flask blueprints (API endpoints)
├── services/        # Business logic (14 services)
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── utilities/       # Utility scripts and tools
├── docs/            # Documentation (22 files)
├── data/            # Data files
├── logs/            # Application logs
└── nexus_app.py     # Main application
```

---

## 📖 Documentation

- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete project guide
- **[FINAL_PROJECT_SUMMARY.md](FINAL_PROJECT_SUMMARY.md)** - Summary & status
- **[utilities/README.md](utilities/README.md)** - Utility scripts guide
- **[docs/](docs/)** - Technical documentation

---

## 🛠️ Installation

### **Prerequisites**:
- Python 3.12+
- Docker & Docker Compose
- Neo4j (via Docker)

### **Setup**:
```bash
# 1. Clone repository
git clone git clone https://github.com/mosaid97/KTCD_AUG.git
cd KTCD_Aug

# 2. Start Neo4j
docker-compose up -d

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create test student
python3 utilities/create_demo_students.py

# 5. Run application
python3 nexus_app.py
```

---

## 🔧 Maintenance

### **View Knowledge Graph**:
```bash
python3 utilities/visualize_knowledge_graph.py
```

### **Clean Up Database**:
```bash
python3 utilities/cleanup_knowledge_graph.py
```

### **Verify System**:
```bash
python3 utilities/verify_and_test_pipelines.py
```

---

## 📊 Current Status

✅ **Production Ready**
✅ **All Features Working**
✅ **Clean & Organized Code**
✅ **Comprehensive Documentation**
✅ **Test Data Available**

---

## 🎯 Key Features Explained

### **1. Interactive Labs**
- Jupyter-style notebook interface
- Python code execution in browser
- Theory section with concepts
- Automatic grading
- Hobby-based personalized backgrounds

### **2. Progress Dashboard**
- Performance trend chart (14 days)
- Skill mastery radar chart
- Learning velocity metrics
- Cognitive profile (G-CDM)
- AI-generated insights
- Complete grades history

### **3. Assessment System**
- Pre-topic assessments
- Class-wide assessments
- Dynamic question generation
- Concept-level evaluation
- Automatic mastery tracking

### **4. AI Chatbot**
- Learning assistance
- Concept explanations
- Progress queries
- Personalized recommendations

---

## 🔗 Quick Links

- **Login**: http://127.0.0.1:8084/student/login
- **Register**: http://127.0.0.1:8084/student/register
- **Teacher Dashboard**: http://127.0.0.1:8084/teacher/dashboard
- **Neo4j Browser**: http://localhost:7474
- **Documentation**: [docs/](docs/)
- **Utilities**: [utilities/](utilities/)

---

## 📝 License

MIT License

---

## 🙏 Acknowledgments

- **Neo4j** - Graph database platform
- **Flask** - Web framework
- **OpenAI** - AI capabilities
- **Tailwind CSS** - UI framework
- **Chart.js** - Data visualization

---

**Version**: 2.0
**Last Updated**: November 3, 2025
**Status**: ✅ Production Ready
**Port**: 8084 (Auto-detected)

🎓 **Empowering personalized learning with AI and Knowledge Graphs!** 🚀
# KTCD_AUG
# KTCD_AUG
# KTCD_AUG
