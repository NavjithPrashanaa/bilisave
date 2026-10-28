# ANTIGRAVITY MASTER BUILD SPECIFICATION
# Project: Smart Home Electricity Bill Reduction App
# App name: BijliSave (configurable)
# Purpose: Build a complete, runnable full-stack application from this single specification.

## 1. PRODUCT GOAL
Build a free, bilingual (Tamil and English), mobile-friendly electricity bill reduction application for Indian households. It must run as a responsive web app and be structured so it can later be packaged for mobile. It should help families record electricity bills, understand consumption, estimate appliance usage, predict future bills, set budgets, receive alerts, and follow practical savings recommendations.

Target users:
- Homeowners and apartment residents in India
- Families sharing one household dashboard
- College/hackathon demonstrators

Business model: free core application.
Community features: none.
App name: keep configurable; use “BijliSave” as a temporary display name and make it easy to rename.

## 2. IMPORTANT ENGINEERING RULES
1. Build a functional end-to-end app, not only a landing page.
2. Do not pretend estimates are actual meter readings.
3. Do not claim that a normal phone or electricity bill can identify exact appliance-level consumption.
4. Clearly label every reading as one of: actual, manually entered, estimated, predicted, or simulated.
5. Do not invent official Indian tariff values. Store tariffs as configurable, versioned data and include clearly labelled demo tariffs only. If no verified tariff exists for a selected provider/category, show an estimate based on user-provided assumptions and explain the limitation.
6. The bill calculator must be deterministic and separate from AI/forecast logic.
7. Use environment variables for secrets. Never commit credentials.
8. Validate inputs and protect household data by authorization checks on every protected API route.
9. Make core features work without paid AI services or physical hardware.
10. If a requested feature cannot be fully implemented due to missing credentials, implement an honest stub/demo mode and document the limitation.
11. Prefer readable, maintainable code with types and sensible error handling.
12. Include seed/demo data and a clear README with exact run instructions.
13. Never use unsafe electrical advice. Recommendations must be low-risk household efficiency tips, not instructions to open wiring or modify mains equipment.
14. Do not claim tests passed unless they were actually run.

## 3. RECOMMENDED STACK
- Frontend: React + TypeScript + Vite
- Styling: Responsive CSS / Tailwind
- Backend: Python FastAPI + SQLite + SQLAlchemy
- Validation: Pydantic on backend, TypeScript on frontend
- Authentication: Secure password hashing + JWT token bearer
- Testing: Pytest + Frontend component checks
- Language: English and Tamil translation dictionaries
