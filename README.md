# Streamlit MCQ Generator App 📝

Welcome to the **Streamlit MCQ Generator App**, a web-based tool built with Python and Streamlit that allows users to generate multiple-choice questions (MCQs) from any input text using the OpenAI GPT model.

---

## 🌟 Features

- Generate multiple-choice questions (MCQs) from any input text.
- Simple and user-friendly interface built with Streamlit.
- Integrates with OpenAI's GPT API to generate intelligent questions.
- Automatically evaluates the complexity of the questions.
- Real-time output of generated MCQs.
- Deployed using AWS EC2 and GitHub Actions for CI/CD.

---

## 🚀 Demo Images

(https://github.com/natashapashupathi/mcqgen/images/1.png)

(https://github.com/natashapashupathi/mcqgen/images/2.png)

(https://github.com/natashapashupathi/mcqgen/images/3.png)


---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.11 or above
- Streamlit
- OpenAI API Key (You can obtain one from [OpenAI](https://beta.openai.com/signup/))
- AWS EC2 instance (if deploying using AWS)
- GitHub repository for CI/CD integration

### Step 1: Clone the Repository

```bash
git clone https://github.com/natashapashupathi/mcqgen.git
cd mcqgen
```

### Step 2: Set Up a Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\\Scripts\\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory with the following content:

```plaintext
OPENAI_API_KEY=your-openai-api-key
```

### Step 5: Run the App Locally

To start the Streamlit app locally:

```bash
streamlit run StreamlitAPP.py
```

Your app should now be running on `http://localhost:8501`.

---

## 🌐 Deployment

### Deploying to AWS EC2

1. **Launch an EC2 instance** (Amazon Linux 2 or Amazon Linux 2023).
2. **SSH into the instance**:
   ```bash
   ssh -i "your-key.pem" ec2-user@ec2-<your-instance-public-ip>.compute-1.amazonaws.com
   ```
3. **Install necessary software**:
   ```bash
   sudo yum update -y
   sudo yum install git python3 -y
   git clone https://github.com/natashapashupathi/mcqgen.git
   cd mcqgen
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Run the app** on the EC2 instance:
   ```bash
   streamlit run StreamlitAPP.py --server.port 8501 --server.address 0.0.0.0
   ```

Your app should now be accessible via the public IP of your EC2 instance on port 8501.

---

## 📖 Usage

1. **Upload a PDF or text file** from which you'd like to generate MCQs.
2. **Set the number of MCQs**, the subject, and the tone of the questions.
3. Click the **"Create MCQs"** button to generate the questions.


## 📦 CI/CD with GitHub Actions

This project uses GitHub Actions for continuous deployment to an AWS EC2 instance. The `deploy.yml` file in the `.github/workflows/` folder defines the CI/CD pipeline that triggers on each push to the `main` branch.

### Key Steps:
1. **GitHub Actions** checks out the latest code.
2. The workflow sets up SSH using the EC2 private key stored in GitHub Secrets.
3. The workflow logs into the EC2 instance, pulls the latest code, and restarts the Streamlit app.

---

## 🛠️ Tech Stack

- **Backend**: Python, OpenAI GPT
- **Frontend**: Streamlit
- **Deployment**: AWS EC2, GitHub Actions (CI/CD)

---

---

## 📞 Contact

If you have any questions or feedback, feel free to reach out at:

- **Email**: natasha.pashu@gmail.com

