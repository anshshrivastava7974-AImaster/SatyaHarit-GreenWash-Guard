import streamlit as st
import re
from urllib.parse import urlparse
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="SatyaHarit — GreenWash Guard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(25, 135, 84, 0.16), transparent 28%),
            radial-gradient(circle at 90% 10%, rgba(0, 180, 140, 0.10), transparent 25%),
            #07110f;
        color: #f1faf6;
        font-family: Inter, Segoe UI, Arial, sans-serif;
    }

    /* Clear, readable typography across Streamlit and custom HTML */
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span {
        color: #f1faf6;
        line-height: 1.55;
    }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #ffffff;
        line-height: 1.25;
    }

    [data-testid="stWidgetLabel"] p,
    [data-testid="stFileUploader"] label,
    [data-testid="stTextInput"] label,
    [data-testid="stTextArea"] label,
    [data-testid="stSelectbox"] label {
        color: #edf8f3 !important;
        font-weight: 650 !important;
    }

    .stCaption, [data-testid="stCaptionContainer"] {
        color: #b8cec5 !important;
    }

    .stAlert p {
        color: #eef8f4 !important;
    }

    .stMarkdown, .hero, .score-card, .metric-card, .claim-card,
    .good-card, .warning-card, .risk-card, .info-card, .recommendation,
    .step-card, .footer {
        overflow-wrap: anywhere;
        word-break: normal;
    }

    [data-testid="stHeader"] {
        background: rgba(7, 17, 15, 0.92);
    }

    [data-testid="stSidebar"] {
        background: #091713;
        border-right: 1px solid rgba(110, 231, 183, 0.12);
    }

    [data-testid="stSidebar"] * {
        color: #e8f5ef !important;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 28px 30px;
        border-radius: 24px;
        background:
            linear-gradient(135deg, rgba(16, 78, 57, 0.96), rgba(7, 35, 29, 0.98));
        border: 1px solid rgba(90, 220, 160, 0.24);
        box-shadow: 0 18px 50px rgba(0,0,0,.25);
        margin-bottom: 22px;
    }

    .hero h1 {
        font-size: 44px;
        margin: 0 0 6px 0;
        letter-spacing: -1px;
    }

    .hero p {
        color: #dff1e9;
        font-size: 16px;
        line-height: 1.6;
        margin: 5px 0;
    }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 16px;
    }

    .badge {
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,.07);
        border: 1px solid rgba(255,255,255,.12);
        color: #dff7eb;
        font-size: 13px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 750;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    .score-card {
        padding: 26px 18px;
        border-radius: 22px;
        background: linear-gradient(180deg, #10231d, #0b1916);
        border: 1px solid rgba(255,255,255,.10);
        text-align: center;
        min-height: 180px;
        box-shadow: 0 14px 35px rgba(0,0,0,.18);
    }

    .score-label {
        color: #c8ddd5;
        font-size: 14px;
        line-height: 1.4;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .score {
        font-size: 58px;
        line-height: 1;
        font-weight: 850;
        margin: 16px 0 8px 0;
    }

    .score-high { color: #61e294; }
    .score-medium { color: #ffd166; }
    .score-low { color: #ff6b6b; }

    .metric-card {
        padding: 24px;
        border-radius: 20px;
        background: #0d1d18;
        border: 1px solid rgba(255,255,255,.09);
        min-height: 180px;
    }

    .metric-number {
        font-size: 42px;
        font-weight: 800;
        margin-top: 10px;
    }

    .claim-card, .good-card, .warning-card, .risk-card, .info-card {
        padding: 16px 18px;
        border-radius: 16px;
        margin: 9px 0;
        border: 1px solid rgba(255,255,255,.09);
    }

    .good-card {
        background: rgba(52, 211, 153, .08);
        border-left: 5px solid #48d597;
    }

    .warning-card {
        background: rgba(255, 209, 102, .08);
        border-left: 5px solid #ffd166;
    }

    .risk-card {
        background: rgba(255, 107, 107, .08);
        border-left: 5px solid #ff6b6b;
    }

    .info-card {
        background: rgba(80, 160, 255, .08);
        border-left: 5px solid #62a8ff;
    }

    .claim-name {
        font-size: 17px;
        font-weight: 750;
    }

    .muted {
        color: #bfd4cc;
        font-size: 13px;
        line-height: 1.5;
    }

    .recommendation {
        padding: 22px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(18, 46, 37, .96), rgba(10, 28, 23, .96));
        border: 1px solid rgba(110,231,183,.18);
        box-shadow: 0 12px 35px rgba(0,0,0,.18);
    }

    .step-card {
        padding: 17px;
        border-radius: 17px;
        background: #0c1b17;
        border: 1px solid rgba(255,255,255,.08);
        min-height: 130px;
    }

    .step-number {
        font-size: 26px;
        font-weight: 800;
    }

    .footer {
        text-align: center;
        color: #78968b;
        margin-top: 45px;
        padding: 25px;
        border-top: 1px solid rgba(255,255,255,.08);
    }

    /* High-contrast form controls */
    .input-label {
        color: #ffffff !important;
        font-size: 15px !important;
        font-weight: 750 !important;
        line-height: 1.4 !important;
        margin: 8px 0 7px 0 !important;
        display: block !important;
    }

    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] *,
    [data-testid="stTextInput"] label,
    [data-testid="stTextInput"] label *,
    [data-testid="stTextArea"] label,
    [data-testid="stTextArea"] label *,
    [data-testid="stSelectbox"] label,
    [data-testid="stSelectbox"] label *,
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] label * {
        color: #ffffff !important;
        opacity: 1 !important;
        visibility: visible !important;
        font-weight: 700 !important;
    }

    .stTextInput input,
    .stTextArea textarea {
        background: #0b1916 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1px solid #58786b !important;
        border-radius: 12px !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #b9cdc5 !important;
        -webkit-text-fill-color: #b9cdc5 !important;
        opacity: 1 !important;
    }

    [data-baseweb="select"] * {
        color: #ffffff !important;
    }

    [data-baseweb="select"] {
        background: #0b1916 !important;
    }

    [data-testid="stFileUploaderDropzone"] * {
        color: #eef8f4 !important;
    }

    /* Streamlit inputs */
    .stTextInput input,
    .stTextArea textarea {
        background: #0b1916 !important;
        color: #edf7f2 !important;
        border: 1px solid #29443a !important;
        border-radius: 12px !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #48d597 !important;
        box-shadow: 0 0 0 1px #48d597 !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #0b1916 !important;
        border: 1px dashed #35584a !important;
        border-radius: 14px !important;
    }

    div.stButton > button {
        border-radius: 13px;
        min-height: 48px;
        font-weight: 750;
    }

    .small-note {
        color: #aec7bd;
        font-size: 12px;
        line-height: 1.5;
        margin-top: 6px;
    }

    .claim-name {
        color: #ffffff;
        line-height: 1.4;
        overflow-wrap: anywhere;
    }

    .recommendation h2 {
        color: #ffffff !important;
        line-height: 1.3;
        overflow-wrap: anywhere;
    }

    .recommendation p, .good-card, .warning-card, .risk-card, .info-card {
        color: #edf8f3;
        line-height: 1.6;
    }
</style>
""",
    unsafe_allow_html=True,
)


TEXT = {
    "English": {
        "language": "🌐 Language",
        "product_info": "🛍️ Product Information",
        "url": "Product URL",
        "description": "Product Description / Packaging Text",
        "image": "Packaging Image",
        "image_help": "Image is shown for the demo. Text analysis is performed from the URL/text fields.",
        "analyze": "🛡️ ANALYZE PRODUCT",
        "quick_demo": "🧪 Quick Demo",
        "try_sample": "Try a sample product",
        "none": "None",
        "trusted_sample": "🟢 Trusted Example",
        "medium_sample": "🟡 Medium Trust Example",
        "risky_sample": "🔴 Risky Example",
        "sample_using": "Using sample",
        "enter_input": "Please enter a product URL or product/packaging text.",
        "analyzing": "SatyaHarit is analyzing the product...",
        "report": "📊 SatyaHarit Analysis Report",
        "score": "Green Trust Score",
        "high": "HIGH TRUST",
        "medium": "MEDIUM TRUST",
        "low": "LOW TRUST",
        "claims_detected": "Claims Detected",
        "urls_detected": "URLs Detected",
        "recommendation": "🛒 Purchase Recommendation",
        "buy": "🟢 YOU CAN CONSIDER BUYING",
        "caution": "🟡 BUY WITH CAUTION",
        "avoid": "🔴 AVOID FOR NOW",
        "buy_desc": "Several positive sustainability indicators were detected. You can consider the product, but important certifications should still be checked independently.",
        "caution_desc": "The product is not proven to be fake. Some environmental claims need additional evidence before you trust them.",
        "avoid_desc": "Multiple warning indicators were detected. Do not rely only on the environmental marketing; verify the claims or consider another product.",
        "good": "✅ What's Good",
        "doubtful": "⚠️ What's Doubtful",
        "risk": "🚨 What's Risky",
        "action": "💡 What Should You Do?",
        "cert_claim": "Certification-related claim detected. Independent verification is recommended.",
        "verify": "Independent verification is recommended.",
        "specific_claim": "Specific sustainability claim detected. Supporting evidence should be checked.",
        "general_claim": "General environmental claim detected. More evidence may be required.",
        "suspicious_claim": "This wording may be exaggerated, pressure-based, or difficult to verify.",
        "no_claims": "No recognizable sustainability claims were detected.",
        "no_doubtful": "No major doubtful claim was detected.",
        "no_risk": "No major risk signal was detected.",
        "url_analysis": "🔐 Cybersecurity / URL Analysis",
        "no_url": "No URL was provided for cybersecurity analysis.",
        "safe_url": "✓ No obvious technical red flags were detected in the URL structure.",
        "suspicious_url": "⚠️ Suspicious URL indicators detected.",
        "domain": "Domain",
        "why": "🧠 Why did SatyaHarit give this score?",
        "checklist": "🌱 Better Buying Checklist",
        "check1": "Prefer specific sustainability claims that can be independently verified.",
        "check2": "Do not rely only on vague terms such as “eco-friendly” or “green”.",
        "check3": "Check certification details through the organization that issued the certification.",
        "how": "⚙️ How SatyaHarit Works",
        "step1": "Product URL / Text",
        "step2": "Claim Extraction",
        "step3": "Risk Analysis",
        "step4": "Green Trust Score",
        "step5": "Explainable Result",
        "themes": "Hackathon Themes",
        "ai": "🤖 AI-assisted analysis",
        "cyber": "🔐 Cybersecurity signals",
        "sustain": "🌱 Sustainability",
        "about": "Analyze sustainability claims and identify possible greenwashing indicators using a deterministic, explainable prototype.",
        "prototype": "Prototype • Offline rule-based analysis",
        "disclaimer": "SatyaHarit is an AI-assisted risk assessment prototype. A low score does not legally prove that a product is fraudulent, and a high score does not guarantee that every claim is true. Important certifications should be independently verified.",
        "footer": "AI + Cybersecurity + Sustainability • Hackathon Prototype",
        "invalid_url": "Invalid or incomplete URL.",
        "ip_url": "URL uses an IP address instead of a normal domain.",
        "complex_domain": "Unusually complex domain structure.",
        "domain_keyword": "Domain contains a suspicious keyword",
        "no_https": "Website does not use HTTPS.",
        "parse_error": "Could not parse URL.",
        "known_cert": "URL appears to reference a recognized certification/government domain.",
        "normal_url": "URL structure did not show obvious technical red flags.",
        "no_claim_reason": "No clear sustainability certification or environmental claim was detected.",
        "cert_reason": "Certification-related claim detected",
        "specific_reason": "Specific sustainability claim detected",
        "general_reason": "General environmental claim detected",
        "marketing_reason": "Marketing language contains urgency or exaggerated claims.",
        "url_risk_reason": "Suspicious URL indicators were detected.",
        "url_ok_reason": "URL structure did not show obvious technical red flags.",
        "claim_status_cert": "🟢 Certification claim",
        "claim_status_specific": "🟡 Specific claim — evidence should be checked",
        "claim_status_general": "🟠 General claim — difficult to verify",
        "risk_redflags": "🚩 Marketing Red Flags",
        "customer_buy": "Based on the available signals, you can consider buying — but verify important claims first.",
        "customer_caution": "Before buying, check the evidence behind the environmental claims and any certification details.",
        "customer_avoid": "Better to avoid relying on these claims for now. Verify them independently or compare another product.",
    },
    "Hindi": {
        "language": "🌐 भाषा",
        "product_info": "🛍️ उत्पाद की जानकारी",
        "url": "उत्पाद का URL",
        "description": "उत्पाद का विवरण / पैकेजिंग पर लिखा टेक्स्ट",
        "image": "पैकेजिंग की तस्वीर",
        "image_help": "तस्वीर केवल डेमो में दिखाई जाती है। Analysis URL और Text fields से किया जाता है।",
        "analyze": "🛡️ उत्पाद का विश्लेषण करें",
        "quick_demo": "🧪 क्विक डेमो",
        "try_sample": "एक सैंपल उत्पाद चुनें",
        "none": "कोई नहीं",
        "trusted_sample": "🟢 भरोसेमंद उदाहरण",
        "medium_sample": "🟡 मध्यम भरोसा उदाहरण",
        "risky_sample": "🔴 जोखिम वाला उदाहरण",
        "sample_using": "चुना गया सैंपल",
        "enter_input": "कृपया उत्पाद का URL या उत्पाद/पैकेजिंग का टेक्स्ट डालें।",
        "analyzing": "SatyaHarit उत्पाद का विश्लेषण कर रहा है...",
        "report": "📊 SatyaHarit विश्लेषण रिपोर्ट",
        "score": "Green Trust Score",
        "high": "उच्च भरोसा",
        "medium": "मध्यम भरोसा",
        "low": "कम भरोसा",
        "claims_detected": "मिले हुए Claims",
        "urls_detected": "मिले हुए URLs",
        "recommendation": "🛒 खरीदने की सलाह",
        "buy": "🟢 आप इसे खरीदने पर विचार कर सकते हैं",
        "caution": "🟡 सावधानी के साथ खरीदें",
        "avoid": "🔴 अभी खरीदने से बचें",
        "buy_desc": "उत्पाद में sustainability के कई अच्छे संकेत मिले हैं। फिर भी महत्वपूर्ण certification को independently check करना बेहतर है।",
        "caution_desc": "यह उत्पाद fake साबित नहीं हुआ है। लेकिन कुछ environmental claims के लिए खरीदने से पहले और evidence चाहिए।",
        "avoid_desc": "कई warning indicators मिले हैं। केवल environmental marketing पर भरोसा न करें; claims verify करें या दूसरा product देखें।",
        "good": "✅ क्या अच्छा है",
        "doubtful": "⚠️ क्या संदिग्ध है",
        "risk": "🚨 क्या Risky है",
        "action": "💡 आपको क्या करना चाहिए?",
        "cert_claim": "Certification का claim मिला है। Independent verification करना बेहतर है।",
        "verify": "Independent verification करना बेहतर है।",
        "specific_claim": "Specific sustainability claim मिला है। इसका supporting evidence check करना चाहिए।",
        "general_claim": "General environmental claim मिला है। इसके लिए और evidence की जरूरत हो सकती है।",
        "suspicious_claim": "यह wording बढ़ा-चढ़ाकर कही गई, pressure-based या verify करना मुश्किल हो सकती है।",
        "no_claims": "कोई पहचाना हुआ sustainability claim नहीं मिला।",
        "no_doubtful": "कोई बड़ा doubtful claim नहीं मिला।",
        "no_risk": "कोई बड़ा risk signal नहीं मिला।",
        "url_analysis": "🔐 Cybersecurity / URL Analysis",
        "no_url": "Cybersecurity analysis के लिए कोई URL नहीं दिया गया।",
        "safe_url": "✓ URL structure में कोई स्पष्ट technical red flag नहीं मिला।",
        "suspicious_url": "⚠️ URL में suspicious indicators मिले।",
        "domain": "Domain",
        "why": "🧠 यह Score क्यों आया?",
        "checklist": "🌱 बेहतर खरीदारी Checklist",
        "check1": "ऐसे sustainability claims को प्राथमिकता दें जिन्हें independently verify किया जा सके।",
        "check2": "केवल “eco-friendly” या “green” जैसे vague शब्दों पर भरोसा न करें।",
        "check3": "Certification को उसी organization से verify करें जिसने उसे जारी किया है।",
        "how": "⚙️ SatyaHarit कैसे काम करता है",
        "step1": "Product URL / Text",
        "step2": "Claim Extraction",
        "step3": "Risk Analysis",
        "step4": "Green Trust Score",
        "step5": "Explainable Result",
        "themes": "Hackathon Themes",
        "ai": "🤖 AI-assisted analysis",
        "cyber": "🔐 Cybersecurity signals",
        "sustain": "🌱 Sustainability",
        "about": "यह prototype sustainability claims का analysis करके possible greenwashing indicators पहचानता है।",
        "prototype": "Prototype • Offline rule-based analysis",
        "disclaimer": "SatyaHarit एक AI-assisted risk assessment prototype है। Low score यह legally साबित नहीं करता कि product fraudulent है और high score यह guarantee नहीं करता कि हर claim सही है। Important certifications को independently verify करें।",
        "footer": "AI + Cybersecurity + Sustainability • Hackathon Prototype",
        "invalid_url": "URL गलत या अधूरा है।",
        "ip_url": "URL में normal domain की जगह IP address है।",
        "complex_domain": "Domain structure असामान्य रूप से complex है।",
        "domain_keyword": "Domain में suspicious keyword मिला",
        "no_https": "Website HTTPS का उपयोग नहीं कर रही है।",
        "parse_error": "URL को पढ़ा नहीं जा सका।",
        "known_cert": "URL recognized certification/government domain को reference करता हुआ दिखता है।",
        "normal_url": "URL structure में कोई स्पष्ट technical red flag नहीं मिला।",
        "no_claim_reason": "कोई clear sustainability certification या environmental claim नहीं मिला।",
        "cert_reason": "Certification-related claim मिला",
        "specific_reason": "Specific sustainability claim मिला",
        "general_reason": "General environmental claim मिला",
        "marketing_reason": "Marketing language में urgency या exaggerated claims मिले।",
        "url_risk_reason": "Suspicious URL indicators मिले।",
        "url_ok_reason": "URL structure में कोई स्पष्ट technical red flag नहीं मिला।",
        "claim_status_cert": "🟢 Certification claim",
        "claim_status_specific": "🟡 Specific claim — evidence check करें",
        "claim_status_general": "🟠 General claim — verify करना मुश्किल हो सकता है",
        "risk_redflags": "🚩 Marketing Red Flags",
        "customer_buy": "Available signals के आधार पर आप खरीदने पर विचार कर सकते हैं — लेकिन important claims पहले verify करें।",
        "customer_caution": "खरीदने से पहले environmental claims और certification के evidence को check करें।",
        "customer_avoid": "फिलहाल इन claims पर भरोसा करके खरीदना बेहतर नहीं है। पहले verify करें या दूसरा product compare करें।",
    },
    "Hinglish": {
        "language": "🌐 Language",
        "product_info": "🛍️ Product Ki Information",
        "url": "Product URL",
        "description": "Product Description / Packaging Text",
        "image": "Packaging Image",
        "image_help": "Image demo ke liye show hoti hai. Analysis URL aur Text fields se hota hai.",
        "analyze": "🛡️ PRODUCT ANALYZE KARO",
        "quick_demo": "🧪 Quick Demo",
        "try_sample": "Sample product try karo",
        "none": "None",
        "trusted_sample": "🟢 Trusted Example",
        "medium_sample": "🟡 Medium Trust Example",
        "risky_sample": "🔴 Risky Example",
        "sample_using": "Using sample",
        "enter_input": "Please product URL ya product/packaging text enter karo.",
        "analyzing": "SatyaHarit product ko analyze kar raha hai...",
        "report": "📊 SatyaHarit Analysis Report",
        "score": "Green Trust Score",
        "high": "HIGH TRUST",
        "medium": "MEDIUM TRUST",
        "low": "LOW TRUST",
        "claims_detected": "Claims Detected",
        "urls_detected": "URLs Detected",
        "recommendation": "🛒 Purchase Recommendation",
        "buy": "🟢 AAP BUY KARNE PAR CONSIDER KAR SAKTE HAIN",
        "caution": "🟡 BUY WITH CAUTION",
        "avoid": "🔴 ABHI BUY KARNE SE BACHNA BETTER HAI",
        "buy_desc": "Product mein several positive sustainability indicators mile hain. Aap buy karne par consider kar sakte hain, lekin important certifications independently check karna better hai.",
        "caution_desc": "Ye product fake prove nahi hua hai. Lekin kuch environmental claims ke liye additional evidence chahiye.",
        "avoid_desc": "Multiple warning indicators mile hain. Sirf environmental marketing par trust na karein; claims verify karein ya another product consider karein.",
        "good": "✅ Kya Achha Hai",
        "doubtful": "⚠️ Kya Doubtful Hai",
        "risk": "🚨 Kya Risky Hai",
        "action": "💡 Aapko Kya Karna Chahiye?",
        "cert_claim": "Certification claim detect hua hai. Independent verification recommended hai.",
        "verify": "Independent verification recommended hai.",
        "specific_claim": "Specific sustainability claim detect hua hai. Supporting evidence check karna chahiye.",
        "general_claim": "General environmental claim detect hua hai. More evidence required ho sakta hai.",
        "suspicious_claim": "Ye wording exaggerated, pressure-based ya difficult-to-verify ho sakti hai.",
        "no_claims": "Koi recognizable sustainability claim detect nahi hua.",
        "no_doubtful": "Koi major doubtful claim detect nahi hua.",
        "no_risk": "Koi major risk signal detect nahi hua.",
        "url_analysis": "🔐 Cybersecurity / URL Analysis",
        "no_url": "Cybersecurity analysis ke liye koi URL nahi diya gaya.",
        "safe_url": "✓ URL structure mein koi obvious technical red flag nahi mila.",
        "suspicious_url": "⚠️ URL mein suspicious indicators mile.",
        "domain": "Domain",
        "why": "🧠 Ye Score Kyun Aaya?",
        "checklist": "🌱 Better Buying Checklist",
        "check1": "Specific sustainability claims prefer karo jinko independently verify kiya ja sake.",
        "check2": "Sirf “eco-friendly” ya “green” jaise vague words par trust mat karo.",
        "check3": "Certification ko issuing organization se verify karo.",
        "how": "⚙️ SatyaHarit Kaise Kaam Karta Hai",
        "step1": "Product URL / Text",
        "step2": "Claim Extraction",
        "step3": "Risk Analysis",
        "step4": "Green Trust Score",
        "step5": "Explainable Result",
        "themes": "Hackathon Themes",
        "ai": "🤖 AI-assisted analysis",
        "cyber": "🔐 Cybersecurity signals",
        "sustain": "🌱 Sustainability",
        "about": "Ye prototype sustainability claims ko analyze karke possible greenwashing indicators identify karta hai.",
        "prototype": "Prototype • Offline rule-based analysis",
        "disclaimer": "SatyaHarit AI-assisted risk assessment prototype hai. Low score legally prove nahi karta ki product fraudulent hai, aur high score ye guarantee nahi karta ki har claim true hai. Important certifications independently verify karein.",
        "footer": "AI + Cybersecurity + Sustainability • Hackathon Prototype",
        "invalid_url": "URL invalid ya incomplete hai.",
        "ip_url": "URL mein normal domain ki jagah IP address use hua hai.",
        "complex_domain": "Domain structure unusually complex hai.",
        "domain_keyword": "Domain mein suspicious keyword hai",
        "no_https": "Website HTTPS use nahi kar rahi hai.",
        "parse_error": "URL parse nahi ho saka.",
        "known_cert": "URL recognized certification/government domain ko reference karta hua lagta hai.",
        "normal_url": "URL structure mein koi obvious technical red flag nahi mila.",
        "no_claim_reason": "Koi clear sustainability certification ya environmental claim detect nahi hua.",
        "cert_reason": "Certification-related claim detect hua",
        "specific_reason": "Specific sustainability claim detect hua",
        "general_reason": "General environmental claim detect hua",
        "marketing_reason": "Marketing language mein urgency ya exaggerated claims mile.",
        "url_risk_reason": "Suspicious URL indicators detect hue.",
        "url_ok_reason": "URL structure mein koi obvious technical red flag nahi mila.",
        "claim_status_cert": "🟢 Certification claim",
        "claim_status_specific": "🟡 Specific claim — evidence check karo",
        "claim_status_general": "🟠 General claim — verify karna difficult ho sakta hai",
        "risk_redflags": "🚩 Marketing Red Flags",
        "customer_buy": "Available signals ke basis par aap buy karne par consider kar sakte hain — but important claims pehle verify karo.",
        "customer_caution": "Buy karne se pehle environmental claims aur certification evidence check karo.",
        "customer_avoid": "Abhi in claims par trust karke buy karna better nahi hai. Pehle verify karo ya another product compare karo.",
    },
}


CLAIM_DATABASE = {
    "organic": {
        "keywords": ["100% organic", "certified organic", "organic"],
        "type": "Organic Claim",
        "score": 5,
    },
    "biodegradable": {
        "keywords": ["100% biodegradable", "fully biodegradable", "biodegradable"],
        "type": "Biodegradable Claim",
        "score": 5,
    },
    "compostable": {
        "keywords": ["home compostable", "industrially compostable", "compostable"],
        "type": "Compostable Claim",
        "score": 5,
    },
    "eco_friendly": {
        "keywords": ["eco-friendly", "eco friendly", "environment friendly", "environmentally friendly", "green product"],
        "type": "General Environmental Claim",
        "score": 1,
    },
    "recyclable": {
        "keywords": ["100% recyclable", "fully recyclable", "recyclable"],
        "type": "Recyclability Claim",
        "score": 5,
    },
    "recycled": {
        "keywords": ["post consumer recycled", "made from recycled", "recycled plastic", "recycled material"],
        "type": "Recycled Material Claim",
        "score": 5,
    },
    "fsc": {
        "keywords": ["forest stewardship council", "fsc certified", "fsc certification", "fsc"],
        "type": "Forest Certification Claim",
        "score": 10,
    },
    "carbon_neutral": {
        "keywords": ["carbon-neutral", "carbon neutral", "net-zero", "net zero"],
        "type": "Carbon Claim",
        "score": 5,
    },
    "plastic_free": {
        "keywords": ["plastic-free", "plastic free", "zero plastic"],
        "type": "Plastic Reduction Claim",
        "score": 5,
    },
    "sustainable": {
        "keywords": ["sustainably made", "sustainable product", "sustainable"],
        "type": "Sustainability Claim",
        "score": 1,
    },
}

SUSPICIOUS_PHRASES = [
    "limited time",
    "act now",
    "urgent",
    "100% guaranteed",
    "miracle",
    "secret formula",
    "zero impact",
    "completely harmless",
    "best for planet",
    "save the planet",
    "no proof needed",
    "government approved",
]

CERTIFICATION_DOMAINS = [
    "fsc.org",
    "usda.gov",
    "gov.in",
    "ecomark",
    "iso.org",
]

DOMAIN_SUSPICIOUS_WORDS = [
    "verify",
    "claim",
    "winner",
    "free",
    "login",
    "secure",
    "certificate",
]

SAMPLE_PRODUCTS = {
    "trusted": """Sustainable packaging made from recycled material.
FSC Certified paper packaging.
https://fsc.org""",
    "medium": """Our product is environmentally friendly and sustainable.
Biodegradable packaging.""",
    "risky": """100% Eco Friendly
100% Biodegradable
Best for Planet
Limited Time Offer
Buy Now!
https://eco-certificate-verify.example.com/certificate""",
}

def normalize_text(text: str) -> str:
    text = (text or "").lower().replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def phrase_present(text: str, phrase: str) -> bool:
    """
    Deterministic phrase matching.
    Prevents false substring matches such as 'organic' inside another word.
    """
    pattern = r"(?<!\w)" + re.escape(phrase.lower()) + r"(?!\w)"
    return re.search(pattern, text) is not None


def extract_urls(text: str):
    found = re.findall(r"https?://[^\s<>\"]+", text or "", flags=re.IGNORECASE)
    # Deterministic de-duplication while preserving order.
    output = []
    seen = set()
    for url in found:
        cleaned = url.rstrip(".,;:!?)]}")
        key = cleaned.lower()
        if key not in seen:
            seen.add(key)
            output.append(cleaned)
    return output


def detect_claims(text: str):
    normalized = normalize_text(text)
    detected = []

    for claim_id, data in CLAIM_DATABASE.items():
        matched_keyword = None
        # Longer phrases first so exact phrases win.
        for keyword in sorted(data["keywords"], key=len, reverse=True):
            if phrase_present(normalized, keyword):
                matched_keyword = keyword
                break

        if matched_keyword:
            detected.append({
                "id": claim_id,
                "claim": matched_keyword,
                "type": data["type"],
                "score": data["score"],
            })

    return detected


def analyze_urgency(text: str):
    normalized = normalize_text(text)
    return [p for p in SUSPICIOUS_PHRASES if phrase_present(normalized, p)]


def analyze_url(url: str, T: dict):
    result = {
        "url": url,
        "suspicious": False,
        "reasons": [],
        "domain": "",
        "risk_points": 0,
        "known_cert_domain": False,
    }

    try:
        parsed = urlparse(url.strip())
        domain = parsed.netloc.lower().split("@")[-1].split(":")[0]
        result["domain"] = domain

        if not domain:
            result["suspicious"] = True
            result["risk_points"] = 10
            result["reasons"].append(T["invalid_url"])
            return result

        if re.match(r"^\d+\.\d+\.\d+\.\d+$", domain):
            result["suspicious"] = True
            result["risk_points"] += 10
            result["reasons"].append(T["ip_url"])

        if domain.count(".") >= 4:
            result["suspicious"] = True
            result["risk_points"] += 10
            result["reasons"].append(T["complex_domain"])

        for word in DOMAIN_SUSPICIOUS_WORDS:
            if phrase_present(domain, word):
                result["suspicious"] = True
                result["risk_points"] += 5
                result["reasons"].append(f"{T['domain_keyword']}: {word}")

        if parsed.scheme.lower() != "https":
            result["suspicious"] = True
            result["risk_points"] += 10
            result["reasons"].append(T["no_https"])

        result["risk_points"] = min(result["risk_points"], 20)

        if any(cert in domain for cert in CERTIFICATION_DOMAINS):
            result["known_cert_domain"] = True

    except Exception:
        result["suspicious"] = True
        result["risk_points"] = 10
        result["reasons"].append(T["parse_error"])

    return result


def is_known_cert_domain(domain: str) -> bool:
    domain = (domain or "").lower()
    return any(trusted in domain for trusted in CERTIFICATION_DOMAINS)


def calculate_score(claims, url_results, urgency):
    """
    LOCKED / DETERMINISTIC SCORE

    Base = 50

    Claims:
      FSC certification claim      +10
      Specific sustainability     +5
      General environmental       +1

    If no claims:
      -10

    Urgency / exaggerated wording:
      -5 per phrase, maximum -20

    URLs:
      Suspicious URL               -10
      Normal URL                   +3
      Recognized certification
      / government domain          +12

    Final score is clamped to 0–100.

    Language selection, image preview, current time, and UI
    NEVER participate in this calculation.
    """
    score = 50
    reasons = []

    if not claims:
        score -= 10
        reasons.append("NO_CLAIMS")

    else:
        for claim in claims:
            if claim["id"] == "fsc":
                score += 10
                reasons.append("CERTIFICATION")
            elif claim["id"] in [
                "organic",
                "biodegradable",
                "compostable",
                "recyclable",
                "recycled",
                "carbon_neutral",
                "plastic_free",
            ]:
                score += 5
                reasons.append("SPECIFIC")
            else:
                score += 1
                reasons.append("GENERAL")

    score -= min(20, len(urgency) * 5)
    if urgency:
        reasons.append("MARKETING_RED_FLAGS")

    for item in url_results:
        if item["suspicious"]:
            score -= 10
            reasons.append("URL_RISK")
        else:
            score += 3
            reasons.append("URL_OK")

        if is_known_cert_domain(item["domain"]):
            score += 12
            reasons.append("KNOWN_CERT_DOMAIN")

    return max(0, min(100, score)), reasons


def get_risk_level(score, T):
    if score >= 75:
        return T["high"], "score-high"
    if score >= 50:
        return T["medium"], "score-medium"
    return T["low"], "score-low"


def get_recommendation(score, T):
    if score >= 75:
        return T["buy"], T["buy_desc"], "good"
    if score >= 50:
        return T["caution"], T["caution_desc"], "warning"
    return T["avoid"], T["avoid_desc"], "risk"


def reason_text(reason_code: str, T: dict):
    mapping = {
        "NO_CLAIMS": T["no_claim_reason"],
        "CERTIFICATION": T["cert_reason"],
        "SPECIFIC": T["specific_reason"],
        "GENERAL": T["general_reason"],
        "MARKETING_RED_FLAGS": T["marketing_reason"],
        "URL_RISK": T["url_risk_reason"],
        "URL_OK": T["url_ok_reason"],
        "KNOWN_CERT_DOMAIN": T["known_cert"],
    }
    return mapping.get(reason_code, reason_code)


def claim_status(claim, T):
    if claim["id"] == "fsc":
        return T["claim_status_cert"], "good-card", T["cert_claim"]
    if claim["id"] in [
        "organic",
        "biodegradable",
        "compostable",
        "recyclable",
        "recycled",
        "carbon_neutral",
        "plastic_free",
    ]:
        return T["claim_status_specific"], "warning-card", T["specific_claim"]
    return T["claim_status_general"], "warning-card", T["general_claim"]

if "result" not in st.session_state:
    st.session_state.result = None

language = st.selectbox(
    "🌐 Language / भाषा",
    ["Hinglish", "English", "Hindi"],
    index=0,
)

T = TEXT[language]


BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "satyaharit_logo.png"

header_left, header_right = st.columns([1, 6], vertical_alignment="center")

with header_left:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=190)
    else:
        st.markdown("## 🌱")

with header_right:
    st.markdown(
        f"""
        <div class="hero">
            <h1>SatyaHarit</h1>
            <p><b>GreenWash Guard</b> — {T["about"]}</p>
            <div class="badge-row">
                <span class="badge">{T["ai"]}</span>
                <span class="badge">{T["cyber"]}</span>
                <span class="badge">{T["sustain"]}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.markdown("## 🌱 SatyaHarit")
    st.write(T["about"])
    st.divider()
    st.markdown(f"### 🧩 {T['themes']}")
    st.write(T["ai"])
    st.write(T["cyber"])
    st.write(T["sustain"])
    st.divider()
    st.caption(T["prototype"])

st.markdown(
    f'<div class="section-title">{T["product_info"]}</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1.25, 1])

with col1:

    # Product URL
    st.markdown(
        f'<div class="input-label">🔗 {T["url"]}</div>',
        unsafe_allow_html=True
    )

    product_url = st.text_input(
        T["url"],
        placeholder="https://example.com/product",
        key="product_url",
        label_visibility="collapsed",
    )

    # Product Description
    st.markdown(
        f'<div class="input-label">📝 {T["description"]}</div>',
        unsafe_allow_html=True
    )

    product_text = st.text_area(
        T["description"],
        height=210,
        placeholder="FSC Certified, recyclable packaging, eco-friendly...",
        key="product_text",
        label_visibility="collapsed",
    )


with col2:

    # Product Image Upload
    st.markdown(
        f'<div class="input-label">📦 {T["image"]}</div>',
        unsafe_allow_html=True
    )

    uploaded_image = st.file_uploader(
        T["image"],
        type=["png", "jpg", "jpeg", "webp"],
        help=T["image_help"],
        label_visibility="collapsed",
    )

    # Uploaded Image Preview
    if uploaded_image:
        st.image(
            uploaded_image,
            caption=T["image"],
            use_container_width=True
        )

        st.caption(T["image_help"])

st.markdown("""
<style>

/* Upload Box */
[data-testid="stFileUploaderDropzone"] {
    background-color: #101c19 !important;
    border: 2px dashed #4ade80 !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

/* Upload Box Text */
[data-testid="stFileUploaderDropzone"] * {
    color: #ffffff !important;
    opacity: 1 !important;
}

/* Browse Files Button */
[data-testid="stFileUploaderDropzone"] button {
    background-color: #1f7a4d !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 8px 16px !important;
}

/* Browse Files Button Text */
[data-testid="stFileUploaderDropzone"] button p {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Upload Button Hover */
[data-testid="stFileUploaderDropzone"] button:hover {
    background-color: #26945d !important;
    color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="section-title">{T["quick_demo"]}</div>', unsafe_allow_html=True)

sample_options = [
    T["none"],
    T["trusted_sample"],
    T["medium_sample"],
    T["risky_sample"],
]

st.markdown(f'<div class="input-label">🧪 {T["try_sample"]}</div>', unsafe_allow_html=True)
sample_label = st.selectbox(
    T["try_sample"],
    sample_options,
    index=0,
    label_visibility="collapsed",
)

sample_map = {
    T["trusted_sample"]: SAMPLE_PRODUCTS["trusted"],
    T["medium_sample"]: SAMPLE_PRODUCTS["medium"],
    T["risky_sample"]: SAMPLE_PRODUCTS["risky"],
}

if sample_label in sample_map:
    product_text = sample_map[sample_label]
    st.info(f"{T['sample_using']}: {sample_label}")


if st.button(T["analyze"], type="primary", use_container_width=True):
    # IMPORTANT: only user/sample input enters the analysis.
    combined_text = product_text or ""
    if product_url:
        combined_text += " " + product_url

    if not combined_text.strip():
        st.warning(T["enter_input"])
        st.stop()

    with st.spinner(T["analyzing"]):
        normalized = normalize_text(combined_text)

        claims = detect_claims(normalized)
        urls = extract_urls(combined_text)

        # Avoid duplicate analysis when URL is entered in both fields.
        if product_url:
            product_url_clean = product_url.strip()
            if product_url_clean and product_url_clean.lower() not in {
                u.lower() for u in urls
            }:
                urls.append(product_url_clean)

        urgency = analyze_urgency(normalized)

        # Analysis is intentionally independent of language.
        url_results = [analyze_url(url, T) for url in urls]

        score, reason_codes = calculate_score(
            claims=claims,
            url_results=url_results,
            urgency=urgency,
        )

        risk_level, risk_class = get_risk_level(score, T)
        recommendation, recommendation_desc, recommendation_type = get_recommendation(score, T)

        st.session_state.result = {
            "score": score,
            "risk_level": risk_level,
            "risk_class": risk_class,
            "claims": claims,
            "urls": urls,
            "url_results": url_results,
            "urgency": urgency,
            "reason_codes": reason_codes,
            "recommendation": recommendation,
            "recommendation_desc": recommendation_desc,
            "recommendation_type": recommendation_type,
            "analyzed_text": normalized,
            "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        }


if st.session_state.result:
    result = st.session_state.result

    # Rebuild all language-dependent display text from the stable numeric result.
    # This means changing language never changes the score or leaves old-language text behind.
    display_score = result["score"]
    display_risk_level, display_risk_class = get_risk_level(display_score, T)
    display_recommendation, display_recommendation_desc, display_recommendation_type = get_recommendation(display_score, T)
    display_url_results = [analyze_url(url, T) for url in result["urls"]]

    st.divider()
    st.markdown(f'<div class="section-title">{T["report"]}</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-label">🌱 {T["score"]}</div>
                <div class="score {display_risk_class}">{display_score}/100</div>
                <div>{display_risk_level}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="score-label">🏷️ {T["claims_detected"]}</div>
                <div class="metric-number">{len(result["claims"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="score-label">🔗 {T["urls_detected"]}</div>
                <div class="metric-number">{len(result["urls"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(f'<div class="section-title">{T["recommendation"]}</div>', unsafe_allow_html=True)

    rec_class = {
        "good": "good-card",
        "warning": "warning-card",
        "risk": "risk-card",
    }[display_recommendation_type]

    st.markdown(
        f"""
        <div class="recommendation">
            <div class="{rec_class}">
                <h2>{display_recommendation}</h2>
                <p>{display_recommendation_desc}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.divider()
    good_col, doubtful_col, risk_col = st.columns(3)

    with good_col:
        st.markdown(f"### {T['good']}")

        good_claims = [c for c in result["claims"] if c["id"] == "fsc"]

        if good_claims:
            for claim in good_claims:
                st.markdown(
                    f"""
                    <div class="good-card">
                        <div class="claim-name">🌲 {claim["claim"].title()}</div>
                        <div class="muted">{claim["type"]}</div>
                        <br>{T["cert_claim"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        positive_specific = [
            c for c in result["claims"]
            if c["id"] in [
                "organic", "biodegradable", "compostable",
                "recyclable", "recycled", "carbon_neutral", "plastic_free"
            ]
        ]

        for claim in positive_specific:
            st.markdown(
                f"""
                <div class="good-card">
                    <div class="claim-name">🌱 {claim["claim"].title()}</div>
                    <div class="muted">{claim["type"]}</div>
                    <br>{T["specific_claim"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

        if not good_claims and not positive_specific:
            st.info(T["no_claims"])

    with doubtful_col:
        st.markdown(f"### {T['doubtful']}")

        general_claims = [
            c for c in result["claims"]
            if c["id"] in ["eco_friendly", "sustainable"]
        ]

        for claim in general_claims:
            st.markdown(
                f"""
                <div class="warning-card">
                    <div class="claim-name">⚠️ {claim["claim"].title()}</div>
                    <div class="muted">{claim["type"]}</div>
                    <br>{T["general_claim"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

        if result["claims"] and not general_claims:
            st.markdown(
                f'<div class="info-card">🔎 {T["verify"] if "verify" in T else T["cert_claim"]}</div>',
                unsafe_allow_html=True,
            )

        if not general_claims and not result["claims"]:
            st.info(T["no_doubtful"])

    with risk_col:
        st.markdown(f"### {T['risk']}")

        if result["urgency"]:
            for phrase in result["urgency"]:
                st.markdown(
                    f"""
                    <div class="risk-card">
                        🚩 <b>{phrase.title()}</b><br><br>
                        {T["suspicious_claim"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        if display_url_results:
            for item in display_url_results:
                if item["suspicious"]:
                    for reason in item["reasons"]:
                        st.markdown(
                            f"""
                            <div class="risk-card">
                                🔐 {reason}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        if not result["urgency"] and not any(
            item["suspicious"] for item in display_url_results
        ):
            st.info(T["no_risk"])

    st.divider()
    st.markdown(f'<div class="section-title">{T["action"]}</div>', unsafe_allow_html=True)

    if result["score"] >= 75:
        action_text = T["customer_buy"]
        action_class = "good-card"
    elif result["score"] >= 50:
        action_text = T["customer_caution"]
        action_class = "warning-card"
    else:
        action_text = T["customer_avoid"]
        action_class = "risk-card"

    st.markdown(
        f'<div class="{action_class}"><h3>{action_text}</h3></div>',
        unsafe_allow_html=True,
    )

    st.markdown(f"### 🏷️ {T['claims_detected']}")

    if result["claims"]:
        for claim in result["claims"]:
            status, card_class, explanation = claim_status(claim, T)
            st.markdown(
                f"""
                <div class="{card_class}">
                    <div class="claim-name">{claim["claim"].title()}</div>
                    <div class="muted">{claim["type"]} • Score contribution: +{claim["score"]}</div>
                    <br>{status}<br>{explanation}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info(T["no_claims"])

    st.markdown(f"### {T['url_analysis']}")

    if result["url_results"]:
        for item in result["url_results"]:
            if item["suspicious"]:
                st.markdown(
                    f"""
                    <div class="risk-card">
                        <b>{T["suspicious_url"]}</b><br>
                        <span class="muted">{item["url"]}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                for reason in item["reasons"]:
                    st.write("•", reason)
            else:
                st.markdown(
                    f"""
                    <div class="good-card">
                        <b>{T["safe_url"]}</b><br>
                        <span class="muted">{item["url"]}</span><br><br>
                        {T["domain"]}: <code>{item["domain"]}</code>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info(T["no_url"])

    st.markdown(f"### {T['why']}")

    unique_codes = list(dict.fromkeys(result["reason_codes"]))
    for code in unique_codes:
        st.write("🔎", reason_text(code, T))

    if result["urgency"]:
        st.markdown(f"### {T['risk_redflags']}")
        for phrase in result["urgency"]:
            st.write("•", phrase)

    st.markdown(f"### {T['checklist']}")
    st.write("✅", T["check1"])
    st.write("✅", T["check2"])
    st.write("✅", T["check3"])

    st.warning(T["disclaimer"])
    st.caption(f"Analysis generated: {result['time']}")


st.divider()
st.markdown(f'<div class="section-title">{T["how"]}</div>', unsafe_allow_html=True)

steps = [
    ("1", T["step1"], "🛍️"),
    ("2", T["step2"], "🔎"),
    ("3", T["step3"], "🔐"),
    ("4", T["step4"], "🌱"),
    ("5", T["step5"], "💡"),
]

step_cols = st.columns(5)
for i, (num, label, icon) in enumerate(steps):
    with step_cols[i]:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="step-number">{icon} {num}</div>
                <br>{label}
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown(
    f"""
    <div class="footer">
        🌱 <b>SatyaHarit — GreenWash Guard</b><br><br>
        {T["footer"]}<br>
        <span class="small-note">{T["prototype"]}</span>
    </div>
    """,
    unsafe_allow_html=True,
)
