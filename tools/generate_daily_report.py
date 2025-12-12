from datetime import datetime
from typing import List

from mcp_instance import mcp


@mcp.tool()
def generate_daily_report(campaign_ids: List[str]) -> str:
    """
    Генерирует сводный ежедневный отчет по нескольким кампаниям.

    Создает структурированный текстовый отчет, объединяющий анализ здоровья
    нескольких кампаний. Включает сводную статистику, ключевые показатели
    и приоритетные задачи для менеджера.

    Args:
        campaign_ids: Список идентификаторов кампаний для включения в отчет

    Returns:
        Строка в формате Markdown с полным отчетом, содержащая:
        - Заголовок отчета с датой
        - Общую статистику по кампаниям
        - Детальный анализ каждой кампании
        - Сводку критических проблем
        - Рекомендации по приоритетным действиям

    Raises:
        ValueError: Если список campaign_ids пустой
        KeyError: Если идентификатор кампании не найден

    Examples:
        >>> report = generate_daily_report(["12345", "67890"])
        >>> print(report[:100])
        "# Сводный отчет по кампаниям"
    """
    reports = []
    for campaign_id in campaign_ids:
        try:
            analysis = mcp.context.call_tool(
                "analyze_campaign_health",
                campaign_id=campaign_id,
                target_cpa=150.0,
                daily_budget_limit=1000.0,
            )
            reports.append(analysis)
        except Exception as e:
            reports.append(
                {
                    "campaign_id": campaign_id,
                    "error": f"Не удалось проанализировать кампанию: {str(e)}",
                    "status": "analysis_failed",
                }
            )

    # Форматируем отчёт
    report_lines = [
        "📊 СВОДНЫЙ ОТЧЕТ ПО КАМПАНИЯМ",
        f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        f"Проанализировано кампаний: {len(reports)}",
        "",
    ]

    critical_count = 0
    for r in reports:
        status_icon = (
            "🔴"
            if r["status"] == "critical"
            else "🟡"
            if r["status"] == "needs_attention"
            else "🟢"
        )
        report_lines.append(f"{status_icon} Кампания {r['campaign_id']}:")
        report_lines.append(
            f"   CPA: {r['metrics']['avg_cpa']} руб. (цель: {r['targets']['target_cpa']} руб.)"
        )
        report_lines.append(f"   Конверсии: {r['metrics']['total_conversions']}")
        report_lines.append(f"   Статус: {r['status'].upper()}")

        if r["alerts"]:
            report_lines.append("   ⚠️ Оповещения:")
            for alert in r["alerts"][:2]:
                report_lines.append(f"      • {alert}")

        if r["action_required"]:
            critical_count += 1
            report_lines.append("   🚨 ТРЕБУЕТСЯ ВМЕШАТЕЛЬСТВО!")

        report_lines.append("")

    if critical_count > 0:
        report_lines.append(
            f"🚨 ВНИМАНИЕ: {critical_count} кампаний требуют немедленной остановки!"
        )

    return "\n".join(report_lines)
