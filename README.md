# 🎯 Mixwer - Advanced PDF Exam Shuffler

מערכת מתקדמת לערבוב מבחנים בפורמט PDF עם שימור פורמט מושלם ונוסחאות מתמטיות.

## 🚀 תכונות מתקדמות

### 🔍 טכנולוגיות מובילות
- **OCR מתקדם** - זיהוי טקסט מדויק עם pytesseract
- **עיבוד תמונות** - שימור פורמט ונוסחאות עם OpenCV
- **זיהוי חכם** - זיהוי אוטומטי של שאלות ותשובות
- **ממשק ידידותי** - תמיכה בעברית ואנגלית

### 📝 יכולות עיבוד
- זיהוי אוטומטי של דפוסי שאלות `[q1]`, `[q2]`, etc.
- חילוץ תשובות נכונות ולא נכונות
- ערבוב חכם עם שמירה על התבנית המקורית
- יצירת דף תשובות אוטומטי

## 🏗️ מבנה הפרויקט

```
project/
├── app.py                 # Flask server עיקרי
├── exam_processor.py      # Wrapper לbackend
├── backend/               # Backend מתקדם
│   ├── Main.py           # Logic עיקרי
│   ├── FunctionalScripts/ # פונקציות עזר
│   └── Logicalscripts/    # Logic עיבוד
├── templates/             # HTML templates
├── static/               # CSS, JS, images
└── requirements.txt      # Dependencies

```

## 🔧 התקנה והפעלה

### דרישות מערכת
- Python 3.8+
- Windows (לתמיכה ב-pytesseract)

### התקנת חבילות
```bash
pip install -r requirements.txt
```

### הפעלת השרת
```bash
python app.py
```

השרת יהיה זמין ב: `http://localhost:5000`

## 📋 חבילות נדרשות

- **Flask** - Web framework
- **PyMuPDF** - PDF processing
- **pdf2image** - PDF to image conversion
- **pytesseract** - OCR engine
- **opencv-python** - Image processing
- **Pillow** - Image manipulation
- **numpy** - Numerical operations
- **reportlab** - PDF generation

## 🎯 שימוש במערכת

1. **העלאת קובץ** - העלה קובץ PDF של מבחן
2. **עיבוד אוטומטי** - המערכת מזהה שאלות ותשובות
3. **ערבוב חכם** - ערבוב התשובות עם שמירה על פורמט
4. **הורדת תוצאה** - הורד את המבחן המעורבב עם דף תשובות

## 🔍 פורמט נתמך

המערכת תומכת במבחנים עם הפורמט הבא:
```
שאלה: טקסט השאלה
[q1]
תשובה נכונה
[a]
תשובה לא נכונה 1
[a]
תשובה לא נכונה 2
```

## 🌐 ממשק משתמש

- **עיצוב מודרני** - Dark/Light mode
- **תמיכה בעברית** - RTL layout מלא
- **Responsive** - מותאם לכל המכשירים
- **הודעות חכמות** - משוב למשתמש בזמן אמת

## 🔒 אבטחה ופרטיות

- קבצים זמניים נמחקים אוטומטית
- אין שמירה של מידע משתמש
- עיבוד מקומי ללא שליחה לשרתים חיצוניים

## 🛠️ פיתוח ותחזוקה

### הוספת תכונות חדשות
1. ערוך את הbackend ב`backend/`
2. עדכן את הwrapper ב`exam_processor.py`
3. הוסף routes חדשים ב`app.py`

### בדיקות
```bash
python -c "from exam_processor import process_exam_pdf; print('Test passed!')"
```

## 📄 לוג שינויים

### גרסה 2.0 (אוגוסט 2025)
- שילוב backend מתקדם עם OCR
- שיפור דיוק זיהוי השאלות
- תמיכה בנוסחאות מתמטיות
- ממשק משתמש משופר

### גרסה 1.0
- גרסה בסיסית עם חילוץ טקסט פשוט

## 🤝 תרומה לפרויקט

1. Fork את הפרויקט
2. צור branch חדש (`git checkout -b feature/amazing-feature`)
3. Commit את השינויים (`git commit -m 'Add amazing feature'`)
4. Push לbranch (`git push origin feature/amazing-feature`)
5. פתח Pull Request

## 📞 תמיכה

לשאלות ותמיכה, פנה אל צוות הפיתוח.

---

**Mixwer** - מערכת מתקדמת לערבוב מבחנים 🎓
