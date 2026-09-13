# SatyaHarit — GreenWash Guard

Final hackathon prototype combining AI-assisted analysis, cybersecurity URL signals, and sustainability claim analysis.

## Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Important
- The scoring engine is deterministic and independent of language.
- The same input produces the same score in English, Hindi, and Hinglish.
- The current offline prototype analyzes pasted product/packaging text and URL structure.
- Packaging images are displayed for the demo; OCR and live certification verification are not claimed.
