import os
import random
from typing import Any, Dict

from dotenv import load_dotenv

from mcp_instance import mcp

load_dotenv()


YANDEX_API_TOKEN = os.getenv("YANDEX_API_TOKEN", "")
YANDEX_API_URL = os.getenv("YANDEX_API_URL", "")

# Функция с генерацией фейковых данных, поскольку в АПИ данные не доступны
@mcp.tool()
def get_campaign_performance(campaign_id: str, days: int = 7) -> Dict[str, Any]:
    """
    Получает и анализирует отчет по эффективности рекламной кампании.

    Извлекает ключевые метрики кампании Яндекс.Директ за указанный период,
    включая расходы, конверсии, клики, показы и расчетные показатели (CPA, CTR, CPC).
    Для демонстрационных целей генерирует реалистичные синтетические данные.

    Args:
        campaign_id: Уникальный идентификатор кампании в Яндекс.Директ
        days: Количество дней для анализа (по умолчанию 7)

    Returns:
        Словарь с результатами анализа, содержащий:
        - status: Статус выполнения ('success', 'no_data', 'api_error', 'exception')
        - campaign_id: Идентификатор анализируемой кампании
        - period_days: Анализируемый период в днях
        - data_trend: Тренд данных ('improving', 'stable', 'worsening')
        - metrics: Основные метрики кампании
        - note: Примечания или предупреждения

    Raises:
        ValueError: Если campaign_id пустой или некорректный
        ConnectionError: При проблемах с подключением к API

    Examples:
        >>> result = get_campaign_performance("12345", days=7)
        >>> print(result["status"])
        "success"
        >>> print(result["metrics"]["avg_cpa"])
        150.75
    """
    # Генерация данных
    base_cost = random.uniform(30000, 80000)
    base_conversions = random.randint(50, 200)

    trend = random.choice(["improving", "stable", "worsening"])

    if trend == "improving":
        total_cost = base_cost * 0.85
        total_conversions = int(base_conversions * 1.15)
    elif trend == "worsening":
        total_cost = base_cost * 1.3
        total_conversions = int(base_conversions * 0.7)
    else:
        total_cost = base_cost
        total_conversions = base_conversions

    total_clicks = int(total_conversions * random.uniform(8, 12))
    total_impressions = total_clicks * random.randint(10, 15)

    avg_cpa = total_cost / total_conversions if total_conversions > 0 else 0
    avg_ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0
    avg_cpc = total_cost / total_clicks if total_clicks > 0 else 0

    return {
        "status": "success",
        "source": "demo_data",
        "campaign_id": campaign_id,
        "period_days": days,
        "data_trend": trend,
        "metrics": {
            "total_cost": round(total_cost, 2),
            "total_conversions": total_conversions,
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "avg_cpa": round(avg_cpa, 2),
            "avg_ctr": round(avg_ctr, 2),
            "avg_cpc": round(avg_cpc, 2),
            "days_analyzed": days,
        },
        "note": "⚠️ ДЕМО-ДАННЫЕ. Для реальных данных нужен токен Яндекс.Директ API.",
    }

# Функция с реальным доступом к АПИ
# @mcp.tool()
# def get_campaign_performance(campaign_id: str, days: int = 7) -> Dict[str, Any]:
#     """
#     Получает и анализирует отчет по эффективности рекламной кампании.

#     Извлекает ключевые метрики кампании Яндекс.Директ за указанный период,
#     включая расходы, конверсии, клики, показы и расчетные показатели (CPA, CTR, CPC).
#     Для демонстрационных целей генерирует реалистичные синтетические данные.

#     Args:
#         campaign_id: Уникальный идентификатор кампании в Яндекс.Директ
#         days: Количество дней для анализа (по умолчанию 7)

#     Returns:
#         Словарь с результатами анализа, содержащий:
#         - status: Статус выполнения ('success', 'no_data', 'api_error', 'exception')
#         - campaign_id: Идентификатор анализируемой кампании
#         - period_days: Анализируемый период в днях
#         - data_trend: Тренд данных ('improving', 'stable', 'worsening')
#         - metrics: Основные метрики кампании
#         - note: Примечания или предупреждения

#     Raises:
#         ValueError: Если campaign_id пустой или некорректный
#         ConnectionError: При проблемах с подключением к API

#     Examples:
#         >>> result = get_campaign_performance("12345", days=7)
#         >>> print(result["status"])
#         "success"
#         >>> print(result["metrics"]["avg_cpa"])
#         150.75
#     """
#     # Формируем запрос к API Яндекс.Директ
#     date_to = datetime.now().strftime("%Y-%m-%d")
#     date_from = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
#     headers = {
#         "Authorization": f"Bearer {YANDEX_API_TOKEN}",
#         "Accept-Language": "ru",
#         "skipReportHeader": "true",
#         "skipColumnHeader": "false",
#         "skipReportSummary": "true",
#     }

#     body = {
#         "params": {
#             "SelectionCriteria": {
#                 "Filter": [
#                     {
#                         "Field": "CampaignId",
#                         "Operator": "EQUALS",
#                         "Values": [campaign_id],
#                     }
#                 ],
#                 "DateFrom": date_from,
#                 "DateTo": date_to,
#             },
#             "FieldNames": ["Date", "Clicks", "Cost", "Impressions", "Conversions"],
#             "ReportName": f"Campaign_{campaign_id}_{date_from}_{date_to}",
#             "ReportType": "CAMPAIGN_PERFORMANCE_REPORT",
#             "DateRangeType": "CUSTOM_DATE",
#             "Format": "TSV",
#             "IncludeVAT": "NO",
#             "IncludeDiscount": "NO",
#         }
#     }

#     try:
#         response = requests.post(YANDEX_API_URL, headers=headers, json=body)

#         if response.status_code == 200:
#             # Парсим TSV
#             lines = response.text.strip().split("\n")
#             if len(lines) > 1:
#                 headers = lines[0].split("\t")
#                 data_lines = lines[1:]

#                 # Агрегируем данные
#                 total_clicks = 0
#                 total_cost = 0
#                 total_conversions = 0

#                 for line in data_lines:
#                     values = line.split("\t")
#                     row = dict(zip(headers, values))
#                     total_clicks += int(row.get("Clicks", 0))
#                     total_cost += float(row.get("Cost", 0))
#                     total_conversions += int(row.get("Conversions", 0))

#                 # Рассчитываем метрики
#                 cpa = total_cost / total_conversions if total_conversions > 0 else 0
#                 ctr = (total_clicks / len(data_lines)) * 100 if data_lines else 0

#                 return {
#                     "status": "success",
#                     "campaign_id": campaign_id,
#                     "period": f"{date_from} - {date_to}",
#                     "metrics": {
#                         "total_cost": round(total_cost, 2),
#                         "total_clicks": total_clicks,
#                         "total_conversions": total_conversions,
#                         "avg_cpa": round(cpa, 2),
#                         "avg_ctr": round(ctr, 2),
#                         "days_analyzed": len(data_lines),
#                     },
#                     "raw_data_available": True,
#                 }
#             else:
#                 return {
#                     "status": "no_data",
#                     "campaign_id": campaign_id,
#                     "period": f"{date_from} - {date_to}",
#                     "note": "Нет данных за указанный период",
#                 }
#         else:
#             return {
#                 "status": "api_error",
#                 "campaign_id": campaign_id,
#                 "error": f"API вернул {response.status_code}",
#                 "response": response.text[:200],
#             }

#     except Exception as e:
#         return {"status": "exception", "campaign_id": campaign_id, "error": str(e)}
