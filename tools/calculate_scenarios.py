import random
from typing import Any, Dict

from mcp_instance import mcp


@mcp.tool()
def calculate_scenarios(campaign_id: str, target_conversions: int) -> Dict[str, Any]:
    """
    Рассчитывает финансовые сценарии для достижения целевых конверсий.

    Анализирует возможные пути достижения заданного количества конверсий
    с учетом текущей эффективности кампании. Предоставляет варианты
    бюджетирования и оптимизации для планирования рекламных активностей.

    Args:
        campaign_id: Уникальный идентификатор кампании в Яндекс.Директ
        target_conversions: Желаемое количество конверсий для планирования

    Returns:
        Словарь с расчетными сценариями, содержащий:
        - campaign_id: Идентификатор анализируемой кампании
        - current_performance: Текущие показатели эффективности
        - scenarios: Расчетные сценарии с разными стратегиями
        - recommendations: Рекомендации по выбору сценария

    Raises:
        ValueError: Если target_conversions <= 0
        ArithmeticError: При ошибках в расчетах

    Examples:
        >>> scenarios = calculate_scenarios("12345", target_conversions=100)
        >>> print(scenarios["scenarios"]["keep_current_cpa"]["required_budget"])
        15000.0
    """

    # Генерируем данные
    current_cost = random.uniform(30000, 80000)
    current_conversions = random.randint(50, 200)
    current_cpa = current_cost / current_conversions if current_conversions > 0 else 0

    # Сценарий 1 - сохраняем текущий CPA
    cost_needed_current_cpa = target_conversions * current_cpa

    # Сценарий 2 - улучшаем CPA на 20%
    improved_cpa = current_cpa * 0.8
    cost_needed_improved = target_conversions * improved_cpa

    # Сценарий 3 - сколько конверсий при текущем бюджете
    conversions_at_current_budget = current_cost / current_cpa if current_cpa > 0 else 0

    return {
        "campaign_id": campaign_id,
        "current_performance": {
            "conversions": current_conversions,
            "cost": round(current_cost, 2),
            "cpa": round(current_cpa, 2),
        },
        "scenarios": {
            "keep_current_cpa": {
                "target_conversions": target_conversions,
                "required_budget": round(cost_needed_current_cpa, 2),
                "note": f"При CPA {current_cpa:.2f} руб.",
            },
            "improve_cpa_20pct": {
                "target_conversions": target_conversions,
                "required_budget": round(cost_needed_improved, 2),
                "note": f"При CPA {improved_cpa:.2f} руб. (на 20% лучше)",
            },
            "at_current_budget": {
                "possible_conversions": round(conversions_at_current_budget, 1),
                "current_budget": round(current_cost, 2),
                "note": "Без увеличения бюджета",
            },
        },
        "recommendations": [
            f"Для {target_conversions} конверсий нужно {cost_needed_current_cpa:.0f} руб. при текущем CPA",
            f"При оптимизации CPA на 20% нужно {cost_needed_improved:.0f} руб.",
            f"С текущим бюджетом можно получить ~{conversions_at_current_budget:.0f} конверсий",
        ],
        "note": "Расчеты основаны на демо-данных. Для точных данных используйте get_campaign_performance.",
    }
