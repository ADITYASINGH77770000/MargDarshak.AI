# MargDarshak.AI



MargDarshak.AI is an AI-powered personalized learning assistant that helps students choose the right courses, skills, and projects based on their career goals. It provides AI-driven study plans, resume-building tools, and career guidance to enhance the learning experience.

## Features 🚀
- **AI Mentor**: Personalized learning recommendations
- **Roadmap Generator**: Career-based learning paths
- **Career Guidance**: Explore career options and prospects
- **Resume Builder**: AI-generated resumes and project highlights
- **Feedback System**: Share experiences and suggestions

## Installation 🛠️
### **Prerequisites**
Ensure you have Python installed. Then, install the required dependencies using:
```bash
pip install -r requirements.txt
```

## How to Run 💻
Run the Streamlit app using:
```bash
streamlit run app.py
```

## Project Structure 📂
```
MargDarshak.AI/
│── app.py               # Main Streamlit application
│── config.yaml          # Configuration file for authentication
│── push_data.py         # Data storage in MongoDB
│── test.py              # User progress dashboard
│── test_mongodb.py      # MongoDB connection test
│── requirements.txt     # Project dependencies
│── user_data.csv        # Sample user data
│── .gitignore           # Ignore unnecessary files
└── README.md            # Project documentation
```

## MongoDB Configuration 🗄️
- The app stores user data in **MongoDB Atlas**.
- Update the MongoDB connection string in `config.yaml` and `push_data.py`.

## Usage 🏆
1. Run `app.py` to start the application.
2. Navigate through the AI-driven course recommendations.
3. Use features like Roadmap Generator and Career Guidance.

## License 📜
This project is licensed under the MIT License.

---
🚀 **MargDarshak.AI** - Empowering students with AI-driven learning!

