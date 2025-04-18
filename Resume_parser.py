#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop = stopwords.words('english')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
import spacy
import en_core_web_sm
from spacy.matcher import Matcher


# In[2]:


import os
import re
from PyPDF2 import PdfReader
import pandas as pd
import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)


# In[3]:


def pdftotext(filepath):
    if filepath.lower().endswith('.pdf'):
        with open(filepath, 'rb') as pdfFileObj:
            pdfReader = PdfReader(pdfFileObj)
            num_pages = len(pdfReader.pages)
            text = ''
            for i in range(num_pages):
                pdfPage = pdfReader.pages[i]
                text += pdfPage.extract_text()
            return text
    else:
        return None

def extract_name(text):
    pattern = r'Name\s*:\s*(\w+)\s*'
    match = re.search(pattern, text)
    return match.group(1) if match else None

def extract_email_addresses(text):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    emails = r.findall(text)
    cleaned_emails = [re.sub(r'[^\w\s@.-]', '', email) for email in emails]
    return cleaned_emails

def extract_phone_number(text):
    r = re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?')
    match = r.findall(text)
    if match:
        cleaned_numbers = []
        for m in match[0]:
            if m:
                cleaned_numbers.append(''.join([c for c in m if c.isdigit()]))
        return '-'.join(cleaned_numbers)
    else:
        return None

def extract_qualification(text):
    pattern = r'Qualification:\s*(.*?)Skills\s*:'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None

def extract_skills(text):
    pattern = r'Skills\s*:\s*(.*?)Personal details\s*:'
    match = re.search(pattern, text, re.DOTALL)
    return [skill.strip() for skill in match.group(1).split('\n') if skill.strip()] if match else None


# In[5]:


if __name__ == '__main__':
    resume_paths = ["resume.1.pdf", "resume.2.pdf", "resume.3.pdf", "resume.4.pdf", "resume.5.pdf"]
    data = []
    for file_name in resume_paths:
        if file_name.lower().endswith('.pdf'):
            text_input = pdftotext(file_name)
            if text_input:
                name = extract_name(text_input)
                email = extract_email_addresses(text_input)
                phone = extract_phone_number(text_input)
                education = extract_qualification(text_input)
                skills = extract_skills(text_input)
                data.append({
                    'File Name': file_name,
                    'Name': name,
                    'Email': email,
                    'Phone': phone,
                    'Education': education,
                    'Skills': skills,
                })


    df = pd.DataFrame(data)
    df.to_csv('output.csv', index=False)


# In[6]:


resume = pd.read_csv('output.csv')


# In[7]:


resume['Education'] = resume['Education'].apply(lambda x: re.sub(r'[^\x00-\x7F]+', ' ', x) if isinstance(x, str) else None)


# In[8]:


resume.head()

