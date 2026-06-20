# Resume Screening System

## Overview

This project automates resume analysis and candidate-job matching using Natural Language Processing (NLP) and machine learning techniques. It extracts information from resumes, compares candidate profiles with job descriptions, and provides similarity-based matching results through an interactive web application.

The project demonstrates the application of NLP, text processing, and machine learning in recruitment analytics.

## Features

* Resume text extraction and processing
* Job description matching
* NLP-based text analysis
* Similarity scoring between resumes and job descriptions
* Interactive Streamlit interface
* Automated candidate evaluation workflow

## Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* scikit-learn
* spaCy
* TF-IDF Vectorization

## How It Works

1. Resume and job description data are loaded into the system.
2. Text is cleaned and preprocessed.
3. Important keywords and features are extracted.
4. TF-IDF vectors are generated for resumes and job descriptions.
5. Similarity scores are calculated.
6. Matching results are displayed through the Streamlit interface.

## Project Structure

```text
Resume-Screening/
│
├── DataSet/
├── Model/
├── WebSite/
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd Resume-Screening

pip install -r requirements.txt
```

## Run the Project

```bash
streamlit run WebSite/app.py
```

The application will be available at:

```text
http://localhost:8501
```

## Example Use Cases

* Resume screening
* Candidate-job matching
* Recruitment analytics
* HR decision support
* Resume keyword analysis

## Learning Outcomes

Through this project, I learned:

* Natural Language Processing (NLP)
* Text preprocessing techniques
* TF-IDF vectorization
* Similarity-based recommendation systems
* Machine learning workflows
* Streamlit application development

## Future Improvements

* Resume ranking system
* Additional NLP models
* LinkedIn profile integration
* Recruiter dashboard
* Advanced candidate recommendations

## License

This project is based on open-source code released under the MIT License.
Original copyright belongs to the respective author.
I have used this project for learning, documentation, and portfolio-building purposes.
