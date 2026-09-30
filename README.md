# 10 Domain Study Chatbots (Gemini + Flask)

1. 01-astronomy-space-science-chatbot: Astronomy & Space Science
2. 02-agritech-chatbot: Agricultural Technology (AgriTech)
3. 03-marine-technology-chatbot: Marine Technology
4. 04-construction-technology-chatbot: Construction Technology
5. 05-railway-technology-chatbot: Railway Technology
6. 06-smart-city-technology-chatbot: Smart City Technology
7. 07-environmental-technology-chatbot: Environmental Technology
8. 08-battery-energy-storage-chatbot: Battery & Energy Storage
9. 09-document-ocr-technology-chatbot: Document & OCR Technology
10. 10-nlp-chatbot: Natural Language Processing (NLP)

## Run one chatbot
```bash
cd 01-astronomy-space-science-chatbot
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
# put your key in .env  ->  GEMINI_API_KEY=...
python app.py            # http://localhost:5000
gunicorn app:app         # production
```
Change the subject any time in `chatbot_config.py` (CHATBOT_TITLE, CHATBOT_TOPICS).
