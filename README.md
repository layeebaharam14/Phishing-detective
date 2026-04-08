# 🛡️ Phishing Detective

An interactive web-based simulation that helps users identify and classify phishing emails in real-world scenarios.

## 🚀 Problem Statement

Phishing attacks are one of the most common cybersecurity threats. Many users fail to recognize suspicious emails, leading to data breaches and financial loss.

## 💡 Solution

This project simulates real-world email scenarios where users must classify emails as **Phishing** or **Safe**.

## 🎮 Features

- Easy, Medium, Hard difficulty levels
- Realistic email examples
- Score tracking system
- Round-based gameplay
- Instant feedback with explanation
- Restart game functionality

## 🧠 How It Works

- User clicks **Start**
- Email is displayed
- User selects:
  - Phishing ❌
  - Safe ✅
- System gives:
  - Reward
  - Explanation
- Game continues for 10 rounds
- Final score is displayed

## ⚙️ Tech Stack

- HTML
- CSS
- JavaScript
- Backend (Flask / API-based logic)

## 🔁 OpenEnv Structure
.
- `reset()` → Starts the game
- `step(action)` → Processes user input
- `state()` → Returns current email state

## 📊 Sample API Response

```json
{
  "email": {...},
  "reward": 1.0,
  "correct": true,
  "done": false
}
```
