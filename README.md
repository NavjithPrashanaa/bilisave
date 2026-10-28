# BijliSave (பிஜிலி சேவ்) ⚡
### Smart Home Electricity Bill Reduction & Tariff Forecasting Platform

BijliSave is a bilingual (Tamil and English), mobile-responsive full-stack application built for Indian households to track electricity bills, understand appliance-level power consumption, forecast future electricity board charges, enforce monthly budgets with threshold alerts, and adopt practical zero-risk energy reduction tips.

---

## 🌟 Key Features

1. **Bilingual Experience (English / தமிழ்)**: Complete interface localization with instant switching from navbar or settings.
2. **Transparent Data Tagging**: Every figure is explicitly tagged with a color-coded badge:
   - `ACTUAL` (Verified bill records)
   - `MANUALLY ENTERED` (User input)
   - `ESTIMATED` (Appliance consumption calculations)
   - `PREDICTED` (Statistical forecast)
   - `SIMULATED` (Virtual smart meter telemetry)
3. **Deterministic Tariff Calculator**:
   - Versioned demo tariffs for **Tamil Nadu (TNEB/TANGEDCO)** with the first 100 units free domestic subsidy, **Karnataka (BESCOM)**, **Maharashtra (MSEDCL)**, and **Delhi (BSES)**.
   - User-defined flat per-unit rate fallback when official tariffs are unavailable.
   - Transparent slab breakdowns showing tier units, rates, energy charges, fixed charges, and taxes.
4. **Baseline Bill Forecast**:
   - Weighted 3-period moving average with dampened trend slope (when $\ge 3$ bills are available).
   - Transparent "Insufficient history" baseline notices for 0, 1, or 2 bills.
   - Explicit disclaimer that mathematical forecasts are estimates, not guaranteed bills.
5. **Appliance Power Modeling**:
   - Deterministic bottom-up formula: $\text{kWh} = \frac{\text{Watts} \times \text{Qty} \times \text{Hours/Day} \times \text{Days/Month}}{1000}$.
   - Preset catalog of common Indian home appliances (Inverter AC, BLDC fans, LED tubelights, frost-free refrigerators, geysers, induction cooktops).
   - Real-time hours/day slider to preview monthly savings impact.
6. **Budget & Duplicate-Free Alerts**:
   - Monthly budget progress bar with color-coded status (Normal, 75%, 90%, Exceeded).
   - In-app alerts triggered only once per period and threshold to prevent duplicate spam.
7. **Zero-Risk Savings Tips**:
   - Habit-based recommendations (AC 24°C thermostat, vampire standby power cutoff, refrigerator coil maintenance, 15-minute geyser timer, washing machine cold cycles).
   - **Safety Mandate**: Strictly prohibits opening electrical panels, modifying mains equipment, or touching wiring.
8. **Bill Photo Scanning with OCR Fallback**:
   - Upload paper electricity bills (JPEG, PNG, WebP).
   - Uses local Tesseract OCR if installed, with regex extraction for units (kWh), amounts (₹), and dates.
   - If OCR is not installed or returns partial text, automatically provides an editable review form so users can review and confirm figures before saving.
9. **Simulated Smart Meter IoT Monitor**:
   - Built-in virtual smart meter displaying 24-hour diurnal residential consumption curves.
   - One-click "Simulate Live Meter Pulse" button to test real-time telemetry.
10. **Family Sharing & Privacy**:
    - Multi-tenant household isolation: users can only view households they belong to.
    - Family invite codes (e.g. `BIJLI888`) and direct email invitations.
    - One-click complete CSV export.

---

## 🏗️ Architecture & Stack

```
bijlisave/
├── start.py                   # Master unified development runner
├── .env.example               # Root configuration template
├── README.md                  # This file
├── antigravity_electricity_app_master_spec.md
├── backend/
│   ├── app/
│   │   ├── config.py          # App settings & editable display name
│   │   ├── database.py        # SQLAlchemy SQLite engine & session
│   │   ├── models.py          # Database schema (User, Household, Bill, Appliance, etc.)
│   │   ├── schemas.py         # Pydantic validation models
│   │   ├── auth.py            # PBKDF2-SHA256 hashing & JWT tokens
│   │   ├── permissions.py     # Household access control & isolation
│   │   ├── services/
│   │   │   ├── tariff_service.py         # Deterministic slab calculator
│   │   │   ├── forecast_service.py       # Baseline forecasting engine
│   │   │   ├── budget_service.py         # Budget evaluation & duplicate alert prevention
│   │   │   ├── recommendations_service.py# Zero-risk rules engine (EN & TA)
│   │   │   ├── ocr_service.py            # Tesseract adapter with manual fallback
│   │   │   └── device_simulator.py       # Virtual IoT smart meter
│   │   ├── routers/           # FastAPI REST endpoints
│   │   └── main.py            # FastAPI application & CORS
│   ├── seed_data.py           # Populates 6 months of demo bills & appliances
│   ├── tests/
│   │   └── test_backend.py    # 10 comprehensive Pytest test cases
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── config.ts          # App name ('BijliSave') & API endpoint
    │   ├── i18n/              # English & Tamil dictionaries
    │   ├── types/             # TypeScript interfaces
    │   ├── services/api.ts    # Typed API client with JWT bearer handling
    │   ├── context/           # Auth, Household & Language state providers
    │   ├── components/        # Badges, SVG Charts, Modals, StatCards, Navbar
    │   ├── pages/             # All 10 application views
    │   ├── index.css          # Modern navy & emerald responsive styling
    │   └── App.tsx            # Main layout & router
    ├── package.json
    └── vite.config.ts
```

---

## 🚀 Quick Start (Single Command)

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Launch Everything
From the `bijlisave` root directory:
```bash
python start.py
```
This script will automatically:
1. Verify and seed `backend/bijlisave.db` with demo household data.
2. Start the FastAPI backend at **http://localhost:8000** (API docs at `/docs`).
3. Start the React + Vite frontend at **http://localhost:5173**.

---

## 🔑 Demo Accounts (Evaluation Ready)

The database is pre-seeded with realistic 6-month seasonal data for a Chennai household under the TNEB tariff structure:

| Role | Email | Password | Details |
|---|---|---|---|
| **Household Owner** | `demo@bijlisave.in` | `Bijli@2026` | Anand Sundaram (Default Tamil UI, 6 bills, 7 appliances) |
| **Family Member** | `family@bijlisave.in` | `Bijli@2026` | Kavitha Anand (Member permissions) |

**Household Invite Code:** `BIJLI888`

You can also click the **"Quick Demo"** buttons directly on the login screen to sign in with 1 click.

---

## 🧪 Running the Automated Test Suite

BijliSave includes automated tests covering authentication, household isolation, deterministic slab math, forecasting, bill duplicate prevention, and CSV export.

From the `backend` directory:
```bash
cd backend
python -m pytest -v
```

**Results:**
- `test_password_hashing`: PBKDF2-HMAC-SHA256 salt & verification: **PASSED**
- `test_user_registration_and_login`: Token creation & validation: **PASSED**
- `test_household_authorization_blocked`: Unauthorized user blocked (403): **PASSED**
- `test_appliance_kwh_formula`: $\frac{\text{Watts} \times \text{Qty} \times \text{Hours} \times \text{Days}}{1000}$: **PASSED**
- `test_bill_validation_and_duplicate`: Date checks & duplicate handling: **PASSED**
- `test_tariff_calculator`: TNEB domestic free slab & fallback rates: **PASSED**
- `test_forecast_baseline`: 0 bills, 1 bill, and 3 bills trend extrapolation: **PASSED**
- `test_budget_and_duplicate_alerts`: Alert triggered once without duplication: **PASSED**
- `test_ocr_fallback`: Graceful fallback when OCR binary is missing: **PASSED**
- `test_csv_export`: Complete CSV output generation: **PASSED**

---

## ⚙️ Manual / Independent Server Startup

### Backend
```bash
cd backend
pip install -r requirements.txt
python seed_data.py
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev -- --port 5173
```

---

## 🛠️ Customization & Extensibility

### Changing the App Name
- Backend: Change `APP_NAME` in `backend/app/config.py` or pass `APP_NAME=MyAppName` in `.env`.
- Frontend: Change `APP_NAME` in `frontend/src/config.ts`.

### Adding Verified Tariffs Safely
To add verified DISCOM tariffs (e.g. WBSEDCL or TPDDL), edit `DEFAULT_DEMO_TARIFFS` in `backend/app/services/tariff_service.py`. Follow the format:
```python
"West Bengal": {
    "provider": "WBSEDCL",
    "consumer_category": "Domestic",
    "source_label": "Official WBSEDCL Tariff Order 2026",
    "is_demo": False,
    "slabs": [
        {"min": 0, "max": 102, "rate": 5.30, "name": "1-102 units"},
        {"min": 102, "max": 180, "rate": 5.97, "name": "103-180 units"},
        {"min": 180, "max": float("inf"), "rate": 6.97, "name": "Above 180 units"},
    ],
    "fixed_charges": 15.0,
    "duty_percent": 10.0,
    "notes": "State regulated domestic tariff schedule."
}
```

### Optical Character Recognition (OCR) Setup
- The app checks for `pytesseract` and system binary `tesseract`.
- On Windows: Download the installer from UB-Mannheim Tesseract OCR and add it to system `PATH`.
- **Fallback**: If Tesseract is not installed, the app reports `OCR unavailable` and presents the manual review form pre-filled with candidate fields.

### Physical Smart Meter Roadmap
The `backend/app/services/device_simulator.py` defines the software adapter interface for smart meter telemetry. To connect real hardware in production:
1. Replace `DeviceSimulator` with a MQTT / Webhook receiver parsing DLMS/COSEM HDLC frames or ESP32 Modbus RTU readings from PZEM-004T / CT clamp sensors.
2. Authenticate the smart meter device using per-device HMAC API keys stored in `Device.config_json`.
3. Switch `Device.mode` from `"simulated"` to `"real"`.
