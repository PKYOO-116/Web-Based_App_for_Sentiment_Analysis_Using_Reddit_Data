# Web-Based Sentiment Analysis System on Reddit for U.S. Presidential Election

## Project Overview

This project presents a full-stack web application that collects, stores, and analyzes Reddit posts and comments related to the U.S. presidential election. The application performs sentiment analysis to assess public opinion trends and predicts support levels for major political candidates and parties.

As part of the DSCI 551 course (Foundations of Data Management) at the University of Southern California in Spring 2024, the project emphasizes distributed data management using Firebase Realtime Database, scalable CRUD operations, and a user-interactive front-end built with React.

---

## Features

- Scrapes Reddit data using the PRAW API in Python
- Performs sentiment analysis using NLTK's VADER analyzer
- Calculates sentiment scores for keywords (Trump, Biden, Republican, Democrat)
- Predicts leading candidate and support ratio based on sentiment aggregation
- Distributes data across four Firebase databases via a hash-based partitioning scheme
- Provides real-time CRUD (Create, Read, Update, Delete) functionality via frontend
- Implements RESTful API using Flask for backend communication

---

## Technology Stack

- **Frontend:** React.js
- **Backend:** Python (Flask)
- **Database:** Firebase Realtime Database (NoSQL)
- **Scraping & Analysis:** PRAW (Reddit API), NLTK (VADER sentiment analysis)

---

## Repository Structure

This repository is organized as follows:

### `web/`

Frontend directory containing the React application.

- Interactive interface for displaying Reddit post data
- Includes buttons for inserting, editing, deleting, and filtering content
- Sentiment results and predictions are shown on the homepage

### `api/`

Python backend implemented with Flask.

- Handles all Reddit data collection, preprocessing, and Firebase interactions
- Includes scripts like:
  - `extract_data.py`: Scrapes Reddit content using keyword filters
  - `score_parse.py`: Performs sentiment analysis and support prediction

### `data/`

Contains JSON-formatted Reddit post and comment data used for testing and validation.

---

## How to Run the App Locally (Terminal/MacOS)

1. Navigate to the frontend directory:

   ```bash
   cd web
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm start
   ```

4. Visit http://localhost:3000 in your browser
   The Flask backend and Firebase database must be active and properly configured for full functionality.

---

## Author

**Paul Yoo**  
M.S. in Applied Data Science  
University of Southern California, Spring 2024  
Model implementation, training optimization, performance evaluation, and report documentation  
[LinkedIn](https://www.linkedin.com/in/pkyoo) | [GitHub](https://github.com/PKYOO-116)
