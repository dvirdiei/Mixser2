#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import tempfile
import shutil
from datetime import datetime
from exam_processor import process_exam_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max-limit
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching
app.secret_key = 'mixwer-advanced-exam-shuffler-2025'

# יצירת תיקיות נדרשות
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('outputs', exist_ok=True)
os.makedirs('temp', exist_ok=True)

@app.route('/')
def home():
    """
    עמוד הבית עם טופס העלאת PDF
    """
    return render_template('index.html')

@app.route('/shuffle_exam', methods=['POST'])
def shuffle_exam_route():
    """
    מסלול לערבוב מבחן עם הbackend המתקדם
    """
    if 'pdf_file' not in request.files:
        flash('לא נבחר קובץ PDF')
        return redirect(url_for('home'))
    
    file = request.files['pdf_file']
    if file.filename == '':
        flash('לא נבחר קובץ')
        return redirect(url_for('home'))
    
    if file and file.filename.lower().endswith('.pdf'):
        try:
            # שמירת הקובץ המועלה
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            input_filename = f"input_{timestamp}_{file.filename}"
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
            file.save(input_path)
            
            # יצירת שם קובץ פלט
            output_filename = f"shuffled_{timestamp}_{file.filename}"
            output_path = os.path.join('outputs', output_filename)
            
            # עיבוד הקובץ עם הbackend המתקדם
            flash('מעבד את הקובץ... זה עלול לקחת כמה דקות', 'info')
            
            success, result_path, error = process_exam_pdf(input_path, output_path)
            
            if success and result_path and os.path.exists(result_path):
                # שליחת הקובץ למשתמש
                return send_file(
                    result_path, 
                    as_attachment=True, 
                    download_name=f"מבחן_מעורבב_{file.filename}",
                    mimetype='application/pdf'
                )
            else:
                error_msg = error or "שגיאה לא ידועה בעיבוד הקובץ"
                flash(f'שגיאה בעיבוד הקובץ: {error_msg}')
                return redirect(url_for('home'))
                
        except Exception as e:
            flash(f'שגיאה בעיבוד הקובץ: {str(e)}')
            return redirect(url_for('home'))
        
        finally:
            # ניקוי קבצים זמניים
            try:
                if 'input_path' in locals() and os.path.exists(input_path):
                    os.remove(input_path)
            except:
                pass
    
    else:
        flash('יש להעלות קובץ PDF בלבד')
        return redirect(url_for('home'))

@app.route('/about')
def about():
    """
    עמוד מידע על המערכת
    """
    return render_template('about.html')

@app.route('/help')
def help_page():
    """
    עמוד עזרה
    """
    return render_template('help.html')

@app.route('/favicon.ico')
def favicon():
    """
    Favicon route
    """
    return send_file('static/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(413)
def too_large(e):
    flash('הקובץ גדול מדי. גודל מקסימלי: 50MB')
    return redirect(url_for('home'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# Cleanup function for temporary files
def cleanup_temp_files():
    """
    ניקוי קבצים זמניים ישנים
    """
    try:
        temp_dirs = ['uploads', 'outputs', 'temp', 'Local storage of images', 'Final PDFs']
        current_time = datetime.now().timestamp()
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for filename in os.listdir(temp_dir):
                    filepath = os.path.join(temp_dir, filename)
                    try:
                        # מחק קבצים ישנים יותר משעה
                        if os.path.isfile(filepath):
                            file_age = current_time - os.path.getctime(filepath)
                            if file_age > 3600:  # 1 hour
                                os.remove(filepath)
                        elif os.path.isdir(filepath):
                            dir_age = current_time - os.path.getctime(filepath)
                            if dir_age > 3600:
                                shutil.rmtree(filepath, ignore_errors=True)
                    except:
                        pass
    except:
        pass

if __name__ == '__main__':
    # ניקוי קבצים זמניים בהפעלה
    cleanup_temp_files()
    
    # הפעלת השרת
    app.run(debug=True, host='0.0.0.0', port=5000)
