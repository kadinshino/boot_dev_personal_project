# Framework detection patterns (absorbed from security scanner)
FRAMEWORK_PATTERNS = {
    'django': [
        'from django.', 'django.conf', 'models.Model', 'INSTALLED_APPS',
        'django.urls', 'manage.py', 'settings.py'
    ],
    'flask': [
        'from flask import', 'Flask(__name__)', '@app.route', 'app.run()',
        'flask.request', 'Blueprint'
    ],
    'fastapi': [
        'from fastapi import', 'FastAPI()', '@app.get', '@app.post',
        'from pydantic import', 'uvicorn'
    ],
    'streamlit': [
        'import streamlit', 'st.', 'streamlit run', 'st.write', 'st.sidebar'
    ],
    'tkinter': [
        'import tkinter', 'from tkinter import', 'Tk()', 'mainloop()', 'ttk.'
    ],
    'pygame': [
        'import pygame', 'pygame.init', 'pygame.display', 'pygame.sprite'
    ],
    'requests': [
        'import requests', 'requests.get', 'requests.post', 'session()'
    ],
    'pandas': [
        'import pandas', 'pd.DataFrame', 'pd.read_csv', 'pd.', '.groupby'
    ],
    'numpy': [
        'import numpy', 'np.array', 'np.', 'numpy.array'
    ],
    'machine_learning': [
        'sklearn', 'tensorflow', 'pytorch', 'keras', 'from transformers'
    ]
}

# Business logic patterns (absorbed from security scanner)  
BUSINESS_PATTERNS = {
    'user_authentication': ['login', 'logout', 'authenticate', 'session', 'password', 'auth'],
    'payment_processing': ['stripe', 'paypal', 'payment', 'billing', 'charge', 'invoice'],
    'email_system': ['send_email', 'smtp', 'mail', 'email', 'sendmail'],
    'file_operations': ['file_upload', 'download', 'save_file', 'read_file', 'storage'],
    'api_service': ['@app.route', 'jsonify', 'request.json', 'api', 'endpoint'],
    'data_analysis': ['pandas', 'numpy', 'matplotlib', 'analysis', 'statistics'],
    'web_scraping': ['beautifulsoup', 'selenium', 'scrape', 'crawl', 'parse_html'],
    'database_operations': ['sqlite', 'postgresql', 'mysql', 'database', 'query', 'orm'],
    'gui_application': ['tkinter', 'qt', 'gui', 'window', 'dialog', 'mainloop'],
    'automation': ['schedule', 'cron', 'automation', 'bot', 'script']
}

# External service patterns
EXTERNAL_SERVICE_PATTERNS = {
    'aws': ['boto3', 'aws_', 's3', 'ec2', 'lambda'],
    'google_cloud': ['google.cloud', 'gcp'],
    'azure': ['azure.', 'microsoft.azure'],
    'stripe': ['stripe.', 'stripe_'],
    'redis': ['redis.Redis', 'redis.'],
    'postgresql': ['psycopg2', 'postgresql'],
    'mongodb': ['pymongo', 'mongodb'],
    'docker': ['docker', 'dockerfile'],
    'github': ['github', 'pygithub'],
    'slack': ['slack', 'slackbot']
}

