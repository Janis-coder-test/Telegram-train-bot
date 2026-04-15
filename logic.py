def calculate_plan(height, weight, goal_weight, activity_level):
    # Разница веса
    diff = goal_weight - weight

    # Базовый обмен (очень упрощённо)
    bmr = 24 * weight

    # Коэффициенты активности
    activity_multipliers = {
        "low": 1.2,
        "medium": 1.375,
        "high": 1.55
    }

    multiplier = activity_multipliers.get(activity_level, 1.2)

    # Поддержка калорий
    maintenance_calories = bmr * multiplier

    # Определяем цель
    if diff < 0:
        target = "похудение"
        calories = maintenance_calories - 400
        recommendation = "Старайся держать дефицит калорий и больше двигаться."
    elif diff > 0:
        target = "набор веса"
        calories = maintenance_calories + 300
        recommendation = "Добавь калории и следи за достаточным потреблением белка."
    else:
        target = "поддержание"
        calories = maintenance_calories
        recommendation = "Ты уже на цели. Поддерживай текущий образ жизни."

    return {
        "target": target,
        "calories": int(calories),
        "difference": diff,
        "recommendation": recommendation
    }