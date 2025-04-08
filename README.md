# Discord PDF Assistant Bot

This bot allows users to upload one or more PDF files to Discord and perform the following actions:

- ✅ **Summarize entire PDFs or a specific page range**
- ✅ **Ask questions about the content of the PDFs using a built-in Q&A system**

---

## 🚀 Features

### 1️⃣ Summarize PDFs
- Upload 1 or more PDFs.
- Choose to summarize **all pages** or a **specific page range** (e.g., `5-10`).

### 2️⃣ Q&A Mode
- Ask questions about the content of the uploaded PDFs.
- The bot will return context-aware answers based on the combined content of all uploaded PDFs.

---

## 🧠 Powered By

- `class_summarize.py` — your custom module for handling:
  - PDF reading: `ReadFile`
  - Summarization: `FullSummarize`, `UserRangeSummarize`
  - Retrieval-based QA: `Questions_and_Answers`

---

## 📦 Requirements

Make sure the following libraries are installed:

```bash
pip install -r requirements.txt
```

## 🛠 Setup

Clone the repository.

Replace the bot token in client.run("YOUR_BOT_TOKEN") with your actual bot token.

Run the bot:

```bash
python main.py
```

## Example Interaction

In order to add discord bot to the server.

https://discord.com/oauth2/authorize?client_id=1358443923802030190 -> click this 

and ![image](https://github.com/user-attachments/assets/50435d1c-c76d-4712-9b32-f3b85cbc83ff)

click to add server. Now you can use DocuGenie.

![image](https://github.com/user-attachments/assets/d29fb50c-665e-4473-9d05-ba5da57d52bd)

Testing with only one pdf and summarize all.

![image](https://github.com/user-attachments/assets/fc239354-ccdf-4543-b660-e0fb27c54c3e)

The range would be pdf file pages.

![image](https://github.com/user-attachments/assets/2957d4b5-02f4-4d5d-88ea-357e297f9960)

I uploaded the fulfilling dataskills pdf file and generating images pdf file. If you do not want to ask anymore type "exit" or "done".

Author: Ye Bhone Lin
