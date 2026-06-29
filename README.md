# Rocketsim 🚀

A physics-based rocket flight simulator made in Python for fun and learning.

This project simulates the full flight of a rocket, from launch to landing, including realistic physics such as air resistance, changing air density, gravity variation, and engine efficiency loss at high altitudes.
<img width="1920" height="1080" alt="Screenshot 2026-06-29 122046" src="https://github.com/user-attachments/assets/46a1b559-0525-4329-bd4d-e8b75533ff51" />


## Features

- **One-stage rocket** with realistic thrust and fuel consumption
- **Two parachute** deployment system (different drag coefficients)
- **Air resistance** (quadratic drag model)
- **Air density** decreases exponentially with altitude
- **Gravity** gets weaker as you go higher
- **Engine efficiency** that drops when air density is low
- Multiple detailed graphs:
  - Height over time
  - Velocity
  - Acceleration
  - Thrust
  - Air density
  - Drag force
  - Net force
  - Efficiency


## Installation

```bash
# 1. Clone the project
git clone https://github.com/JOUW-GITHUB-NAAM/rocketsim.git
cd rocketsim

# 2. Install required packages
pip install matplotlib numpy
