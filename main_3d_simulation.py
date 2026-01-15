# -------------------------------------------------
# TSAS – Threat Severity Assessment System (3D)
# Multi-Threat + Distance-Based Alerts
# -------------------------------------------------

import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from vpython import *
from model.tsas_ann_model import TSASModel

# -------------------------------------------------
# LOAD ANN MODEL
# -------------------------------------------------
tsas_model = TSASModel()

# -------------------------------------------------
# SCENE SETUP
# -------------------------------------------------
scene.title = "TSAS – Multi-Threat Severity Assessment (3D)"
scene.width = 1000
scene.height = 600
scene.background = color.black

scene.camera.pos = vector(0, 0, 140)
scene.camera.axis = vector(0, 0, -140)

# -------------------------------------------------
# PROTECTED ZONE
# -------------------------------------------------
protected_zone_radius = 25
protected_zone = sphere(
    pos=vector(0, 0, 0),
    radius=protected_zone_radius,
    color=color.cyan,
    opacity=0.25
)

label(
    pos=vector(0, protected_zone_radius + 8, 0),
    text="PROTECTED ZONE",
    box=False,
    height=12
)

# -------------------------------------------------
# DISTANCE RINGS (RADAR ZONES) – FIXED ORIENTATION
# -------------------------------------------------

safe_ring = ring(
    pos=vector(0, 0, 0),
    axis=vector(0, 0, 1),   # ⬅️ Z-axis normal → XY plane
    radius=60,
    thickness=0.4,
    color=color.green,
    opacity=0.25
)

warning_ring = ring(
    pos=vector(0, 0, 0),
    axis=vector(0, 0, 1),
    radius=35,
    thickness=0.5,
    color=color.yellow,
    opacity=0.35
)

danger_ring = ring(
    pos=vector(0, 0, 0),
    axis=vector(0, 0, 1),
    radius=25,
    thickness=0.6,
    color=color.red,
    opacity=0.45
)

# -------------------------------------------------
# SEVERITY MAPPING
# -------------------------------------------------
severity_colors = {
    0: color.green,
    1: color.yellow,
    2: color.orange,
    3: color.red
}

severity_names = {
    0: "LOW",
    1: "MEDIUM",
    2: "HIGH",
    3: "CRITICAL"
}

# -------------------------------------------------
# DISTANCE ALERT LOGIC
# -------------------------------------------------
def distance_alert(distance):
    if distance > 60:
        return "SAFE"
    elif distance > 35:
        return "WARNING"
    elif distance > protected_zone_radius:
        return "DANGER"
    else:
        return "ZONE BREACH"

# -------------------------------------------------
# THREAT CLASS
# -------------------------------------------------
class Threat:
    def __init__(self, tid, start_pos, velocity, intent, signal):
        self.id = tid
        self.body = sphere(
            pos=start_pos,
            radius=3,
            color=color.green,
            make_trail=True,
            trail_radius=0.25
        )
        self.velocity = velocity
        self.intent = intent
        self.signal = signal
        self.active = True
        self.severity = 0

        self.label = label(
            pos=self.body.pos,
            text="",
            box=False,
            height=9,
            color=color.white
        )

    def update(self):
        if not self.active:
            return

        # Move threat
        self.body.pos += self.velocity

        # Distance from protected zone
        distance = mag(self.body.pos - protected_zone.pos)

        # ANN feature vector
        features = [
            min(distance / 100.0, 1.0),
            mag(self.velocity),
            1.0,
            self.intent,
            self.signal
        ]

        # ANN prediction
        self.severity, _ = tsas_model.predict(features)

        # Update color
        self.body.color = severity_colors[self.severity]

        # Distance-based alert
        alert = distance_alert(distance)

        # Update label above threat
        self.label.pos = self.body.pos + vector(0, 5, 0)
        self.label.text = (
            f"T{self.id} | {severity_names[self.severity]}\n"
            f"Dist: {distance:.1f}\n"
            f"{alert}"
        )

        # Stop if breached
        if distance <= protected_zone_radius:
            self.velocity = vector(0, 0, 0)
            self.active = False

# -------------------------------------------------
# CREATE MULTIPLE THREATS
# -------------------------------------------------
threats = [
    Threat(1, vector(80, 0, 0), vector(-0.6, 0, 0), 0.8, 0.9),
    Threat(2, vector(-90, 20, 10), vector(0.5, -0.1, -0.05), 0.4, 0.8),
    Threat(3, vector(0, -85, -20), vector(0, 0.6, 0.1), 0.6, 0.85)
]

# -------------------------------------------------
# GLOBAL STATUS
# -------------------------------------------------
status_label = label(
    pos=vector(0, -55, 0),
    text="TSAS ACTIVE – Monitoring Threats",
    box=False,
    height=12
)

# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
while True:
    rate(30)

    highest_severity = 0

    for threat in threats:
        threat.update()
        highest_severity = max(highest_severity, threat.severity)

    status_label.text = f"TSAS GLOBAL ALERT: {severity_names[highest_severity]}"
