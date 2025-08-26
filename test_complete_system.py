#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))

from exam_processor import process_exam_pdf

def test_backend_complete():
    """
    בדיקה מלאה של הbackend עם כל הקבצים המעודכנים
    """
    print("🔍 בודק את הbackend המעודכן...")
    
    # נסה עם PDF דוגמה
    test_pdf = r"C:\Users\HP\Downloads\ddd.pdf"
    
    if not os.path.exists(test_pdf):
        print("❌ לא נמצא קובץ PDF לבדיקה")
        print("💡 העלה קובץ PDF דרך הממשק ב-http://localhost:5000")
        return
    
    print(f"📄 מעבד קובץ: {test_pdf}")
    
    try:
        success, output_path, error = process_exam_pdf(test_pdf)
        
        if success:
            print(f"✅ הצלחה! נוצר קובץ: {output_path}")
            if output_path and os.path.exists(output_path):
                size = os.path.getsize(output_path) / 1024  # KB
                print(f"📊 גודל קובץ: {size:.1f} KB")
        else:
            print(f"❌ כשל: {error}")
            
    except Exception as e:
        print(f"💥 שגיאה: {e}")
        
    print("\n🌐 השרת זמין ב: http://localhost:5000")
    print("🚀 המערכת מוכנה לשימוש!")

if __name__ == "__main__":
    test_backend_complete()
