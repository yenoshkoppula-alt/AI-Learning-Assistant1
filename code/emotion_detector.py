def detect_emotion(text: str) -> dict:
    """
    Analyzes user text to classify keyword frequency for target academic emotions.
    Returns a dictionary containing the detected 'emotion' and 'confidence' score.
    """
    if not text:
        return {"emotion": "Neutral", "confidence": 0.5}

    normalized = text.lower()
    
    # Core learning-context keyword mapping
    emotion_keywords = {
        "Happy": ["happy", "joy", "excited", "glad", "wonderful", "great", "awesome", "cheerful", "pleased", "celebrate"],
        "Sad": ["sad", "unhappy", "depressed", "cry", "lonely", "down", "disappointed", "gloom", "sorrow"],
        "Angry": ["angry", "mad", "frustrated", "annoyed", "furious", "hate", "pissed", "rage", "irritated"],
        "Stressed": ["stressed", "overwhelmed", "pressure", "burnout", "tired", "exhausted", "heavy", "load", "struggling"],
        "Anxious": ["anxious", "nervous", "worried", "scared", "fear", "panic", "dread", "uneasy"],
        "Motivated": ["motivated", "inspired", "ready", "eager", "focused", "determined", "ambitious", "hype", "excited to learn"],
        "Confused": ["confused", "lost", "stuck", "puzzled", "uncertain", "clueless", "unclear", "dont understand", "don't understand"]
    }

    matches = {}
    total_matches = 0

    for emotion, keywords in emotion_keywords.items():
        count = 0
        for keyword in keywords:
            count += normalized.count(keyword)
        if count > 0:
            matches[emotion] = count
            total_matches += count

    # Handle Neutral fallback
    if total_matches == 0:
        return {"emotion": "Neutral", "confidence": 0.5}

    # Find emotion with the most keyword matches
    detected_emotion = max(matches, key=matches.get)
    max_count = matches[detected_emotion]

    # Calculate confidence based on distribution density
    base_confidence = 0.6
    match_ratio = max_count / total_matches
    confidence = min(0.95, base_confidence + match_ratio * 0.3)

    return {
        "emotion": detected_emotion,
        "confidence": round(confidence, 2)
    }