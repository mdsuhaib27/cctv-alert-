def detect_behavior(classes):
    print(f"[DEBUG] Detected classes: {classes}")  # <-- Add this for debugging
    if 'gun' in classes or 'knife' in classes or 'weapon' in classes:
        return "threat"
    return "safe"
