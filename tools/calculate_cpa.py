from typing import Any, Dict

from mcp_instance import mcp


@mcp.tool()
def calculate_cpa(cost: float, conversions: int) -> Dict[str, Any]:
    """
    Рассчитывает стоимость привлечения клиента (CPA) на основе расходов и конверсий.

    Выполняет базовый расчет эффективности рекламных инвестиций.
    Полезен для быстрой оценки эффективности кампаний или отдельных активностей.

    Args:
        cost: Общие расходы на рекламную активность (в рублях), должно быть положительным
        conversions: Количество достигнутых конверсий, должно быть неотрицательным

    Returns:
        Словарь с результатами расчета, содержащий:
        - cost: Входные расходы
        - conversions: Входное количество конверсий
        - calculated_cpa: Рассчитанное значение CPA
        - efficiency_note: Оценка эффективности (низкая/средняя/высокая)

    Raises:
        ValueError: Если cost < 0 или conversions < 0
        ZeroDivisionError: При conversions = 0

    Examples:
        >>> result = calculate_cpa(cost=10000.0, conversions=50)
        >>> print(result["calculated_cpa"])
        200.0
        >>> print(result["efficiency_note"])
        "CPA в пределах нормы"
    """
    if cost < 0:
        raise ValueError("Расходы не могут быть отрицательными")
    if conversions < 0:
        raise ValueError("Количество конверсий не может быть отрицательным")
    if conversions == 0:
        raise ZeroDivisionError("Невозможно рассчитать CPA при нулевых конверсиях")

    # Расчет CPA
    calculated_cpa = cost / conversions

    # Оценка эффективности
    if calculated_cpa < 100:
        efficiency_note = "Отличная эффективность, CPA низкий"
        efficiency_level = "high"
    elif calculated_cpa < 500:
        efficiency_note = "CPA в пределах нормы"
        efficiency_level = "medium"
    else:
        efficiency_note = "CPA высокий, требуется оптимизация"
        efficiency_level = "low"

    return {
        "status": "success",
        "input_parameters": {"cost": cost, "conversions": conversions},
        "calculated_cpa": round(calculated_cpa, 2),
        "efficiency_note": efficiency_note,
        "efficiency_level": efficiency_level,
        "interpretation": {
            "cost_per_conversion": f"{calculated_cpa:.2f} руб.",
            "conversions_per_cost": f"{conversions / cost:.4f}" if cost > 0 else "N/A",
            "recommendation": "Снижайте стоимость клика"
            if calculated_cpa > 500
            else "Оптимизируйте конверсию"
            if calculated_cpa > 100
            else "Масштабируйте успешную кампанию",
        },
    }
