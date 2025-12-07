def generate_recommendations(study_time, absences, health, failures):
    suggestions = []

    if study_time < 2:
        suggestions.append("Increase your daily study hours to at least 2–3 hours.")
    if absences > 10:
        suggestions.append("Try to reduce absences for better performance.")
    if health < 3:
        suggestions.append("Focus on health — it strongly influences learning quality.")
    if failures > 0:
        suggestions.append("Seek academic support to understand previous subjects better.")

    if not suggestions:
        suggestions.append("You're on track! Keep maintaining your study habits.")

    return suggestions
