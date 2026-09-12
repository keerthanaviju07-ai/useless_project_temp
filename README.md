# Thalayattam Technologies — What Did Your Nod Say? 🎯

## Basic Details

### Team Name
**miki**

### Team Members

- **Keerthana V** — Jawaharlal College of Engineering and Technology — Team Lead
- **Meenakshi Jayaraj** — Jawaharlal College of Engineering and Technology — Member

---

## Project Description

**Thalayattam Technologies** is an AI-powered computer vision system that interprets predefined Malayali-style head movement patterns through a webcam.

Instead of speaking or typing, users can simply move their heads and let the system recognize the movement and respond with predefined Malayalam expressions such as **ATHE, SHERI, VENDA, NOKKAM, and ARIYILLA**.

### Live Demo

**[Thalayattam Technologies — What Did Your Nod Say?](https://thalayattam-nod-detect.lovable.app/)**

---

# The Problem (that doesn't exist)

What if saying **"Athe", "Sheri", "Venda", "Nokkam", or "Ariyilla"** became too much effort?

Why use words when your head is already doing the talking?

We decided to solve this completely unnecessary but surprisingly fun problem.

---

# The Solution (that nobody asked for)

We created **Thalayattam Technologies**, an AI system that watches your head movements and attempts to understand what you are communicating.

The user simply:

1. Opens the Nod Detector.
2. Allows camera access.
3. Calibrates their neutral head position.
4. Performs a head movement.
5. The AI analyses the movement.
6. The system predicts the corresponding predefined response.

Because sometimes a nod is all you need.

---

# Technical Details

## Technologies / Components Used

### Software

**Languages**
- Python
- TypeScript
- JavaScript

**Frontend**
- React
- Vite
- TypeScript
- Tailwind CSS
- Lovable

**Backend**
- FastAPI
- Uvicorn
- WebSocket

**Computer Vision**
- MediaPipe Face Landmarker
- OpenCV
- OpenCV `solvePnP`

**Machine Learning**
- Scikit-learn
- Random Forest Classifier
- NumPy
- Pandas
- Joblib

**Development Tools**
- VS Code
- GitHub
- Lovable
- Vercel

### Hardware

- Laptop / Desktop
- Webcam

---

# System Architecture

```text
                    WEBCAM
                       │
                       ▼
              ┌─────────────────┐
              │ React Frontend  │
              │   Lovable UI    │
              └────────┬────────┘
                       │
                    WebSocket
                       │
                       ▼
              ┌─────────────────┐
              │ FastAPI Backend │
              └────────┬────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │ MediaPipe Face          │
          │ Landmarker              │
          └───────────┬─────────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │ Head Pose Estimation    │
          │ Yaw / Pitch / Roll      │
          └───────────┬─────────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │ Temporal Feature        │
          │ Extraction              │
          └───────────┬─────────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │ Random Forest           │
          │ Classifier              │
          └───────────┬─────────────┘
                      │
                      ▼
             Gesture + Confidence
                      │
                      ▼
              ┌─────────────────┐
              │ Frontend Result │
              └─────────────────┘