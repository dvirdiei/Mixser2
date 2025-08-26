# 🔧 מדריך התקנת Tesseract OCR

המערכת דורשת Tesseract OCR להפעלה תקינה. 

## 📥 הורדה והתקנה

### Windows:
1. הורד מ: https://github.com/UB-Mannheim/tesseract/wiki
2. התקן את הקובץ המוריד
3. הוסף לPATH: `C:\Program Files\Tesseract-OCR`
4. הורד חבילת עברית: https://github.com/tesseract-ocr/tessdata/raw/main/heb.traineddata
5. שים את heb.traineddata ב: `C:\Program Files\Tesseract-OCR\tessdata\`

### מדריך מהיר:
```bash
# הורד את Tesseract
# התקן אותו ב C:\Program Files\Tesseract-OCR
# הוסף למשתני סביבה:
set TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata
```

## ✅ בדיקה
לאחר ההתקנה, הרץ:
```python
import pytesseract
print(pytesseract.get_tesseract_version())
```

אם זה עובד - המערכת מוכנה לפעולה מלאה! 🎯
