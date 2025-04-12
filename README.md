# 🤖 Caregiver Support Chatbot 

Welcome to the **Caregiver Chatbot**: a Streamlit-based intelligent assistant designed to support caregivers emotionally and functionally. 
This chatbot helps caregivers manage stress, track care-related tasks like medication and appointments, and offers compassionate conversation based on the user's emotional state.

---

## Overview

This project combines conversational AI with a lightweight task manager to:

- Provide emotional support to caregivers using tone-aware responses.
- Allow users to log care tasks (e.g., giving medication, attending appointments).
- Display all scheduled tasks with a simple checkbox toggle.
- Create a safe, intuitive space for caregivers to feel heard and organized.

---

## Features

### 🗣️ Emotion-Aware Chatbot
- Responds with either a **soft** or **directive** tone.
- Uses sentiment triggers like "tired", "overwhelmed", or "lonely".
- Offers empathetic or solution-driven replies accordingly.

### ✅ Task Management
- Add care tasks via a sidebar (task type, name, time, date).
- View all scheduled tasks by toggling a checkbox.
- Tasks are stored using `st.session_state` (in-memory).

### 🖼️ Clean Streamlit Interface
- Sidebar for adding tasks and choosing chatbot tone.
- Main section for chatting with the assistant and viewing scheduled care tasks.
