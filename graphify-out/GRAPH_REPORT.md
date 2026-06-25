# Graph Report - .  (2026-06-25)

## Corpus Check
- Corpus is ~1,847 words - fits in a single context window. You may not need a graph.

## Summary
- 96 nodes · 218 edges · 16 communities (9 shown, 7 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 46 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Weather Forecasting & Ledger Infrastructure|Weather Forecasting & Ledger Infrastructure]]
- [[_COMMUNITY_Core Domain Interfaces & Questionnaire Flow|Core Domain Interfaces & Questionnaire Flow]]
- [[_COMMUNITY_Attire Recording & Completion Flow|Attire Recording & Completion Flow]]
- [[_COMMUNITY_Telegram Messaging Infrastructure|Telegram Messaging Infrastructure]]
- [[_COMMUNITY_API Entrypoints & Webhook Handlers|API Entrypoints & Webhook Handlers]]
- [[_COMMUNITY_Environment Configuration & Errors|Environment Configuration & Errors]]
- [[_COMMUNITY_Project Metadata & FlaskTelegram Dependencies|Project Metadata & Flask/Telegram Dependencies]]
- [[_COMMUNITY_Vercel Deployment Settings|Vercel Deployment Settings]]
- [[_COMMUNITY_Graphify Knowledge Graph Guidelines|Graphify Knowledge Graph Guidelines]]
- [[_COMMUNITY_Package Version Config|Package Version Config]]
- [[_COMMUNITY_Initial Changelog|Initial Changelog]]
- [[_COMMUNITY_Minor Changelog Updates|Minor Changelog Updates]]
- [[_COMMUNITY_Vercel Hobby Plan Cron Changelog|Vercel Hobby Plan Cron Changelog]]
- [[_COMMUNITY_Google Sheets Dependency|Google Sheets Dependency]]
- [[_COMMUNITY_Dotenv Dependency|Dotenv Dependency]]
- [[_COMMUNITY_Pytz Timezone Dependency|Pytz Timezone Dependency]]

## God Nodes (most connected - your core abstractions)
1. `OpenMeteoForecaster` - 17 edges
2. `GoogleSheetsLedger` - 17 edges
3. `TelegramSender` - 17 edges
4. `MessageSender` - 16 edges
5. `FinalizeRecordUseCase` - 16 edges
6. `WardrobeLedger` - 15 edges
7. `DailyAttire` - 14 edges
8. `AdvanceQuestionnaireUseCase` - 14 edges
9. `WardrobeRecommendation` - 12 edges
10. `WeatherForecaster` - 12 edges

## Surprising Connections (you probably didn't know these)
- `TelegramSender` --uses--> `WeatherFetchError`  [INFERRED]
  infrastructure.py → domain.py
- `TelegramSender` --uses--> `LedgerError`  [INFERRED]
  infrastructure.py → domain.py
- `GoogleSheetsLedger` --uses--> `MessagingError`  [INFERRED]
  infrastructure.py → domain.py
- `OpenMeteoForecaster` --uses--> `MessagingError`  [INFERRED]
  infrastructure.py → domain.py
- `TelegramSender` --uses--> `WeatherForecast`  [INFERRED]
  infrastructure.py → domain.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Graphify Integration and Guidelines** — rules_graphify_rule_query, rules_graphify_rule_wiki, rules_graphify_rule_update, workflows_graphify_workflow [INFERRED 0.85]
- **Yoan's Chamberlain Core Dependencies** — requirements_python_telegram_bot, requirements_requests, requirements_gspread, requirements_pytz, requirements_python_dotenv, requirements_flask [EXTRACTED 1.00]

## Communities (16 total, 7 thin omitted)

### Community 0 - "Weather Forecasting & Ledger Infrastructure"
Cohesion: 0.19
Nodes (7): LedgerError, WardrobeRecommendation, WeatherFetchError, WeatherForecast, GoogleSheetsLedger, OpenMeteoForecaster, Response

### Community 1 - "Core Domain Interfaces & Questionnaire Flow"
Cohesion: 0.19
Nodes (5): ABC, MessageSender, WardrobeLedger, WeatherForecaster, AdvanceQuestionnaireUseCase

### Community 2 - "Attire Recording & Completion Flow"
Cohesion: 0.41
Nodes (3): date, DailyAttire, FinalizeRecordUseCase

### Community 3 - "Telegram Messaging Infrastructure"
Cohesion: 0.43
Nodes (3): MessagingError, TelegramSender, InlineKeyboardMarkup

### Community 4 - "API Entrypoints & Webhook Handlers"
Cohesion: 0.48
Nodes (5): get_use_cases(), _handle_webhook_payload(), run_daily_cron(), telegram_webhook(), InitiateQuestionnaireUseCase

### Community 5 - "Environment Configuration & Errors"
Cohesion: 0.57
Nodes (3): EnvironmentConfig, ConfigurationError, Exception

### Community 6 - "Project Metadata & Flask/Telegram Dependencies"
Cohesion: 0.33
Nodes (6): Changelog v1.0.2, Changelog v1.0.4, Yoan's Chamberlain README, Flask Dependency, python-telegram-bot Dependency, requests Dependency

### Community 7 - "Vercel Deployment Settings"
Cohesion: 0.40
Nodes (4): builds, crons, routes, version

### Community 8 - "Graphify Knowledge Graph Guidelines"
Cohesion: 0.50
Nodes (4): Graphify Query Rule, Graphify Update Rule, Graphify Wiki Navigation Rule, Graphify Workflow

## Knowledge Gaps
- **17 isolated node(s):** `version`, `version`, `builds`, `routes`, `crons` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TelegramSender` connect `Telegram Messaging Infrastructure` to `Weather Forecasting & Ledger Infrastructure`, `Core Domain Interfaces & Questionnaire Flow`, `Attire Recording & Completion Flow`, `API Entrypoints & Webhook Handlers`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `OpenMeteoForecaster` connect `Weather Forecasting & Ledger Infrastructure` to `Core Domain Interfaces & Questionnaire Flow`, `Attire Recording & Completion Flow`, `Telegram Messaging Infrastructure`, `API Entrypoints & Webhook Handlers`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `AdvanceQuestionnaireUseCase` connect `Core Domain Interfaces & Questionnaire Flow` to `Weather Forecasting & Ledger Infrastructure`, `Attire Recording & Completion Flow`, `API Entrypoints & Webhook Handlers`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `OpenMeteoForecaster` (e.g. with `DailyAttire` and `LedgerError`) actually correct?**
  _`OpenMeteoForecaster` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `GoogleSheetsLedger` (e.g. with `DailyAttire` and `LedgerError`) actually correct?**
  _`GoogleSheetsLedger` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `TelegramSender` (e.g. with `DailyAttire` and `LedgerError`) actually correct?**
  _`TelegramSender` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `MessageSender` (e.g. with `GoogleSheetsLedger` and `OpenMeteoForecaster`) actually correct?**
  _`MessageSender` has 6 INFERRED edges - model-reasoned connections that need verification._