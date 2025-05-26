import logging
import re
import json
from typing import List, Dict, Any

import spacy
from spacy.matcher import PhraseMatcher
import nltk
from nltk.corpus import stopwords
from collections import Counter

# Ensure NLTK stopwords are downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Load spaCy English model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    raise ImportError('spaCy English model not found. Run: python -m spacy download en_core_web_sm')

logger = logging.getLogger(__name__)

# Example skill/action verb lists (should be expanded or loaded from a config/db)
SKILLS = [
    'python', 'java', 'c++', 'sql', 'javascript', 'aws', 'docker', 'kubernetes', 'react', 'node',
    'machine learning', 'deep learning', 'nlp', 'data analysis', 'project management', 'excel',
    'communication', 'leadership', 'git', 'linux', 'tensorflow', 'pytorch', 'flask', 'django'
]
ACTION_VERBS = [
    'developed', 'managed', 'designed', 'implemented', 'created', 'led', 'analyzed', 'built',
    'deployed', 'optimized', 'improved', 'collaborated', 'coordinated', 'executed', 'delivered'
]

# Precompile matchers for efficiency
skill_matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
skill_matcher.add('SKILL', [nlp.make_doc(skill) for skill in SKILLS])
action_matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
action_matcher.add('ACTION', [nlp.make_doc(verb) for verb in ACTION_VERBS])

STOPWORDS = set(stopwords.words('english'))


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    try:
        text = text.lower()
        text = re.sub(r'[^\w\s\-.,;:()\[\]{}\'\"?!@#$%^&*+=]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    except Exception as e:
        logger.error(f"Error cleaning text: {e}")
        return text


def extract_skills(text: str) -> List[str]:
    """Extract skills from text using spaCy PhraseMatcher."""
    try:
        doc = nlp(text)
        matches = skill_matcher(doc)
        found = set()
        for match_id, start, end in matches:
            found.add(doc[start:end].text.lower())
        return sorted(found)
    except Exception as e:
        logger.error(f"Error extracting skills: {e}")
        return []


def extract_action_verbs(text: str) -> List[str]:
    """Extract action verbs from text using spaCy PhraseMatcher."""
    try:
        doc = nlp(text)
        matches = action_matcher(doc)
        found = set()
        for match_id, start, end in matches:
            found.add(doc[start:end].text.lower())
        return sorted(found)
    except Exception as e:
        logger.error(f"Error extracting action verbs: {e}")
        return []


def extract_keywords(text: str, top_n: int = 15) -> List[str]:
    """Extract top keywords (excluding stopwords)."""
    try:
        words = [w for w in re.findall(r'\b\w+\b', text.lower()) if w not in STOPWORDS]
        freq = Counter(words)
        return [w for w, _ in freq.most_common(top_n)]
    except Exception as e:
        logger.error(f"Error extracting keywords: {e}")
        return []


def analyze_job_description(jd_text: str) -> Dict[str, Any]:
    """Extract key requirements, skills, and keywords from job description."""
    try:
        cleaned = clean_text(jd_text)
        skills = extract_skills(cleaned)
        keywords = extract_keywords(cleaned)
        return {
            'skills': skills,
            'keywords': keywords
        }
    except Exception as e:
        logger.error(f"Error analyzing job description: {e}")
        return {'skills': [], 'keywords': []}


def analyze_resume(resume_text: str) -> Dict[str, Any]:
    """Extract skills, action verbs, and keywords from resume."""
    try:
        cleaned = clean_text(resume_text)
        skills = extract_skills(cleaned)
        actions = extract_action_verbs(cleaned)
        keywords = extract_keywords(cleaned)
        return {
            'skills': skills,
            'action_verbs': actions,
            'keywords': keywords
        }
    except Exception as e:
        logger.error(f"Error analyzing resume: {e}")
        return {'skills': [], 'action_verbs': [], 'keywords': []}


def match_resume_to_job(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """Match resume to job description and return structured analysis."""
    try:
        resume_data = analyze_resume(resume_text)
        job_data = analyze_job_description(jd_text)
        resume_skills = set(resume_data['skills'])
        job_skills = set(job_data['skills'])
        matched_skills = sorted(resume_skills & job_skills)
        missing_skills = sorted(job_skills - resume_skills)
        match_score = round(len(matched_skills) / max(len(job_skills), 1), 2)
        recommendations = []
        if missing_skills:
            recommendations.append(f"Consider adding or improving: {', '.join(missing_skills)}.")
        if match_score < 0.7:
            recommendations.append("Your resume could be better tailored to this job description.")
        return {
            'match_score': match_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'recommendations': recommendations
        }
    except Exception as e:
        logger.error(f"Error matching resume to job: {e}")
        return {
            'match_score': 0.0,
            'matched_skills': [],
            'missing_skills': [],
            'recommendations': [f'Error during analysis: {e}']
        } 