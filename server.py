import os

from dotenv import load_dotenv

from mcp_instance import mcp
from tools.analyze_campaign_health import analyze_campaign_health
from tools.calculate_cpa import calculate_cpa
from tools.calculate_scenarios import calculate_scenarios
from tools.generate_daily_report import generate_daily_report
from tools.get_campaign_performance import get_campaign_performance
from tools.test_connection import test_connection

load_dotenv()


PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")


# Регистрация инструментов
mcp.add_tool(get_campaign_performance)
mcp.add_tool(analyze_campaign_health)
mcp.add_tool(generate_daily_report)
mcp.add_tool(calculate_scenarios)
mcp.add_tool(calculate_cpa)
mcp.add_tool(test_connection)

if __name__ == "__main__":
    print("=" * 65)
    print("🤖 MCP СЕРВЕР: Яндекс.Директ Монитор")
    print("=" * 65)
    print("Стратегия: Анализ отчётов + рекомендации (без прямого управления)")
    print("")
    print("📊 ИНСТРУМЕНТЫ:")
    print("   1. get_campaign_performance - Получить данные по кампании")
    print("   2. analyze_campaign_health  - Анализ по правилам (CPA, бюджет)")
    print("   3. generate_daily_report    - Сводный отчёт по кампаниям")
    print("   4. calculate_scenarios      - Расчёт сценариев")
    print("   5. calculate_cpa            - Рассчитать CPA по стоимости и конверсиям")
    print("   6. test_connection          - Проверить подключение к серверу")
    print("")
    print("🔧 Конфигурация:")
    print("   • Транспорт: streamable-http")
    print("   • Статус: stateless")
    print("=" * 65)

    mcp.run(transport="streamable-http", host=HOST, port=PORT)
