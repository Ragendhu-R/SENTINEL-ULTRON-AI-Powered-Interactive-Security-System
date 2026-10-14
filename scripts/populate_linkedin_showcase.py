"""
ULTRON LinkedIn Showcase Telemetry Generator
============================================
Generates high-definition, authentic tactical surveillance frames with YOLO
bounding boxes, HUD telemetry, and security incident dialogues, then injects
them into the ULTRON Monitor Station for high-impact LinkedIn post captures.
"""

import base64
import json
import time
from pathlib import Path
import cv2
import numpy as np
import requests

SERVER_URL = "http://127.0.0.1:8000"


def create_surveillance_frame(title: str, subtitle: str, subject_boxes: list, alert_color=(0, 255, 120), is_critical=False):
    """
    Renders a realistic 640x480 high-tech tactical CCTV surveillance frame.
    If webcam is available, blends live optical feed with military HUD graphics.
    """
    frame = None
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, cam_frame = cap.read()
            if ret and cam_frame is not None:
                frame = cv2.resize(cam_frame, (640, 480))
            cap.release()
    except Exception:
        pass

    if frame is None:
        # Create ultra-cool dark CCTV surveillance background with grid
        frame = np.full((480, 640, 3), 18, dtype=np.uint8)
        # Add surveillance scanlines
        for y in range(0, 480, 4):
            frame[y : y + 1, :] = (26, 30, 36)
        # Add perimeter boundary grid lines
        cv2.line(frame, (60, 400), (580, 400), (45, 55, 70), 1)
        cv2.line(frame, (60, 400), (200, 150), (40, 50, 65), 1)
        cv2.line(frame, (580, 400), (440, 150), (40, 50, 65), 1)
        cv2.putText(frame, "CCTV CAM-01 [EAST PERIMETER GATE]", (20, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (90, 115, 140), 1, cv2.LINE_AA)

    # 1. Overlay HUD Vignette & Dark Tint
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (640, 480), (10, 14, 20), -1)
    cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)

    # 2. Draw HUD Corner Brackets
    c_len = 25
    hud_c = (0, 229, 255) if not is_critical else (0, 30, 255)
    # TL
    cv2.line(frame, (15, 15), (15 + c_len, 15), hud_c, 2)
    cv2.line(frame, (15, 15), (15, 15 + c_len), hud_c, 2)
    # TR
    cv2.line(frame, (625, 15), (625 - c_len, 15), hud_c, 2)
    cv2.line(frame, (625, 15), (625, 15 + c_len), hud_c, 2)
    # BL
    cv2.line(frame, (15, 465), (15 + c_len, 465), hud_c, 2)
    cv2.line(frame, (15, 465), (15, 465 - c_len), hud_c, 2)
    # BR
    cv2.line(frame, (625, 465), (625 - c_len, 465), hud_c, 2)
    cv2.line(frame, (625, 465), (625, 465 - c_len), hud_c, 2)

    # 3. Draw Subject / Threat Bounding Boxes
    for box in subject_boxes:
        bx1, by1, bx2, by2 = box["bbox"]
        bcolor = box["color"]
        label = box["label"]
        tag = box.get("tag", "")

        # Box rectangle
        cv2.rectangle(frame, (bx1, by1), (bx2, by2), bcolor, 2)
        # Corner brackets on bbox
        blen = 12
        cv2.line(frame, (bx1, by1), (bx1 + blen, by1), bcolor, 3)
        cv2.line(frame, (bx1, by1), (bx1, by1 + blen), bcolor, 3)
        cv2.line(frame, (bx2, by1), (bx2 - blen, by1), bcolor, 3)
        cv2.line(frame, (bx2, by1), (bx2, by1 + blen), bcolor, 3)
        cv2.line(frame, (bx1, by2), (bx1 + blen, by2), bcolor, 3)
        cv2.line(frame, (bx1, by2), (bx1, by2 - blen), bcolor, 3)
        cv2.line(frame, (bx2, by2), (bx2 - blen, by2), bcolor, 3)
        cv2.line(frame, (bx2, by2), (bx2, by2 - blen), bcolor, 3)

        # Header tag background
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.42, 1)
        cv2.rectangle(frame, (bx1, max(0, by1 - 22)), (bx1 + tw + 14, by1), bcolor, -1)
        text_color = (0, 0, 0) if bcolor != (0, 0, 255) else (255, 255, 255)
        cv2.putText(frame, label, (bx1 + 6, max(14, by1 - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.42, text_color, 1, cv2.LINE_AA)

        if tag:
            (tw2, th2), _ = cv2.getTextSize(tag, cv2.FONT_HERSHEY_SIMPLEX, 0.38, 1)
            cv2.rectangle(frame, (bx1, by2), (bx1 + tw2 + 10, by2 + 18), (20, 24, 30), -1)
            cv2.putText(frame, tag, (bx1 + 4, by2 + 13), cv2.FONT_HERSHEY_SIMPLEX, 0.38, bcolor, 1, cv2.LINE_AA)

    # 4. Top Tactical HUD Banner
    banner_bg = frame.copy()
    cv2.rectangle(banner_bg, (0, 0), (640, 36), (12, 15, 22), -1)
    cv2.addWeighted(banner_bg, 0.88, frame, 0.12, 0, frame)
    cv2.line(frame, (0, 36), (640, 36), (36, 48, 68), 1)

    cv2.putText(frame, title, (20, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S UTC")
    cv2.putText(frame, time_str, (430, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 229, 255), 1, cv2.LINE_AA)

    # 5. Bottom Status Strip
    cv2.rectangle(frame, (0, 452), (640, 480), (10, 14, 20), -1)
    cv2.line(frame, (0, 452), (640, 452), (36, 48, 68), 1)
    cv2.putText(frame, subtitle, (20, 471), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (140, 160, 185), 1, cv2.LINE_AA)
    cv2.putText(frame, "OPTICAL SENSOR: 30 FPS // AI TRACKING: ACTIVE", (320, 471), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 230, 118), 1, cv2.LINE_AA)

    # Encode to JPEG Base64
    _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    b64 = "data:image/jpeg;base64," + base64.b64encode(buf).decode("utf-8")
    return b64


def inject(topic: str, payload: dict):
    """Sends telemetry payload to server."""
    res = requests.post(f"{SERVER_URL}/api/inject_event", json={"topic": topic, "payload": payload}, timeout=5)
    return res.status_code == 200


def populate_critical_intrusion():
    print("[SHOWCASE] Ingesting Critical Intrusion Scenario...")

    # 1. Generate 3 Diverse Forensic Snapshots
    # Snap 1: Armed Threat in Sector 4
    snap1_b64 = create_surveillance_frame(
        title="[ALERT] SECTOR 04: ARMED INTRUSION DETECTED",
        subtitle="YOLO11s PERSON #07 + WEAPON DETECTED (KNIFE)",
        subject_boxes=[
            {
                "bbox": (170, 75, 410, 410),
                "label": "PERSON ID:07 [94.6%]",
                "tag": "DWELL: 154s // LOITERING",
                "color": (0, 230, 118),
            },
            {
                "bbox": (330, 230, 420, 320),
                "label": "CRITICAL: KNIFE [91.4%]",
                "tag": "ARMED THREAT",
                "color": (0, 0, 255),
            },
        ],
        is_critical=True,
    )

    # Snap 2: Phone Recording & Surveillance
    snap2_b64 = create_surveillance_frame(
        title="[NOTICE] SECTOR 02: COVERT RECORDING DEVICE",
        subtitle="YOLO11s PERSON #03 HOLDING SMARTPHONE",
        subject_boxes=[
            {
                "bbox": (140, 90, 350, 415),
                "label": "PERSON ID:03 [89.2%]",
                "tag": "DWELL: 48s // TRANSIT",
                "color": (0, 230, 118),
            },
            {
                "bbox": (245, 175, 305, 260),
                "label": "PHONE DETECTED [88.7%]",
                "tag": "RECORDING LENS",
                "color": (255, 140, 0),
            },
        ],
        is_critical=False,
    )

    # Snap 3: Optical Tamper Alert
    snap3_b64 = create_surveillance_frame(
        title="[TAMPER] OPTICAL SENSOR CH-01 LENS COVERED",
        subtitle="TAMPER DETECTOR: SUDDEN ILLUMINANCE BLACKOUT",
        subject_boxes=[
            {
                "bbox": (90, 50, 550, 430),
                "label": "SENSOR OBSTRUCTION DETECTED",
                "tag": "CONF: 99.1% // DEBOUNCED",
                "color": (0, 0, 255),
            }
        ],
        is_critical=True,
    )

    # Send State Telemetry
    inject("ultron/state", {
        "security_state": "CRITICAL",
        "person_count": 2,
        "persons": [
            {
                "track_id": 7,
                "dwell_time": 154.2,
                "phone": False,
                "weapon": "KNIFE",
                "first_seen": time.time() - 154.2,
            },
            {
                "track_id": 3,
                "dwell_time": 48.6,
                "phone": True,
                "weapon": None,
                "first_seen": time.time() - 48.6,
            },
        ],
    })

    # Send Snapshots in reverse chronological order
    inject("ultron/snapshot", {
        "base64": snap3_b64,
        "filename": "snap_tamper.jpg",
        "trigger": "CAMERA TAMPER DETECTED",
        "threat_level": "CRITICAL",
        "has_weapon": False,
        "timestamp": time.time() - 120,
        "description": "Optical sensor lens obstruction debounced",
    })

    inject("ultron/snapshot", {
        "base64": snap2_b64,
        "filename": "snap_phone.jpg",
        "trigger": "PHONE RECORDING DETECTED",
        "threat_level": "NOMINAL",
        "has_weapon": False,
        "timestamp": time.time() - 60,
        "description": "Visitor holding active mobile recording device",
    })

    inject("ultron/snapshot", {
        "base64": snap1_b64,
        "filename": "snap_armed.jpg",
        "trigger": "ARMED INTRUDER: KNIFE BRANDISHED",
        "threat_level": "CRITICAL",
        "has_weapon": True,
        "timestamp": time.time(),
        "description": "Subject #07 drew weapon in Sector 4 perimeter",
    })

    # Send Dialogue Stream
    chats = [
        {"role": "visitor", "text": "Is someone there? Who is recording this area?", "timestamp": time.time() - 45},
        {"role": "ultron", "text": "Perimeter defense active. Sector 4 is under 24/7 autonomous optical and acoustic surveillance.", "timestamp": time.time() - 40},
        {"role": "visitor", "text": "Shut off that camera right now or I'll smash it!", "timestamp": time.time() - 25},
        {"role": "ultron", "text": "Critical warning: Concealed weapon detected in your right hand. Dwell time: 154s. Vacate perimeter immediately.", "timestamp": time.time() - 18},
        {"role": "ultron", "text": "Dispatching emergency law enforcement telemetry over HiveMQ Cloud. Audio siren arming in 5 seconds.", "timestamp": time.time() - 5},
    ]

    for c in chats:
        inject("ultron/chat", c)

    # Send Critical Incident Alert Banner
    inject("ultron/alerts", {
        "severity": "CRITICAL",
        "alert_type": "PERIMETER_BREACH_ARMED",
        "message": "CRITICAL INCIDENT: ARMED SUBJECT IN SECTOR 4 — CODE RED DISPATCHED",
    })

    print("[SHOWCASE] Telemetry injected successfully!")


if __name__ == "__main__":
    populate_critical_intrusion()
