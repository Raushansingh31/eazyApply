from flask import Flask, request, jsonify
from flask_cors import CORS
from src.libs.resume_and_cover_builder import ResumeFacade, ResumeGenerator, StyleManager
import yaml
from pathlib import Path

app = Flask(_name_)
CORS(app)  # Enable CORS for all routes

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.json
        
        # Load resume data from yaml
        with open('data_folder/plain_text_resume.yaml', 'r') as file:
            resume_data = yaml.safe_load(file)
            
        # Update resume data with form data
        resume_data.update({
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'linkedin': data.get('linkedin'),
            'github': data.get('github')
        })
        
        # Initialize components
        resume_generator = ResumeGenerator()
        resume_generator.set_resume_object(resume_data)
        
        # Generate resume with selected style
        style = data.get('style', 'style_josylad_grey')
        style_path = f"src/libs/resume_and_cover_builder/resume_style/{style}.css"
        
        resume_html = resume_generator.create_resume(style_path)
        
        return jsonify({'html': resume_html})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    try:
        data = request.json
        
        # Load resume data
        with open('data_folder/plain_text_resume.yaml', 'r') as file:
            resume_data = yaml.safe_load(file)
            
        # Update resume data with form data
        resume_data.update({
            'name': data.get('name'),
            'email': data.get('email')
        })
        
        # Initialize components
        resume_generator = ResumeGenerator()
        resume_generator.set_resume_object(resume_data)
        
        # Generate cover letter
        style = data.get('style', 'style_josylad_grey')
        style_path = f"src/libs/resume_and_cover_builder/resume_style/{style}.css"
        job_description = data.get('jobDescription', '')
        
        cover_letter = resume_generator.create_cover_letter_job_description(
            style_path,
            job_description
        )
        
        return jsonify({'html': cover_letter})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True, port=5001)