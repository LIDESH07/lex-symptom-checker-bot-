# Symptom Checker Chatbot – Amazon Lex + AWS Lambda

This is a basic health symptom checker chatbot built using *Amazon Lex* and *AWS Lambda*.

### 🔍 Features:
- Users can input symptoms like headache, fever, dizziness, etc.
- The bot asks:
  - How long the symptom has lasted
  - Severity: Mild, Moderate, or Severe
- Based on input, it suggests:
  - Booking a doctor
  - Talking to an expert
  - Other follow-up actions

### ⚙ Tech Stack:
- Amazon Lex (v2)
- AWS Lambda (Node.js/Python)
- JSON Bot Configuration
- Deployed and tested in AWS Console

### 📁 Files Included:
- lambda_function.py: Custom logic for symptom evaluation
- bot_configuration.json: Lex Bot structure (exported)
- README.md: Project overview

### 🚀 How to Use:
1. Import bot_configuration.json into Amazon Lex.
2. Deploy your lambda_function.py in AWS Lambda.
3. Connect the bot to Lambda and start testing in the Lex console.

---

### 🤝 Created By:
[Lidesh Chevvakula] – Aspiring Cloud/AI Developer
