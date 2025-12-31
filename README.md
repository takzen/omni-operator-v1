# OMNI-OPERATOR-V1 // AUTONOMICZNA FABRYKA DYSTRYBUCJI TREŚCI

![Status](https://img.shields.io/badge/STATUS-W_BUDOWIE-8B0000?style=for-the-badge)
![Python](https://img.shields.io/badge/PYTHON-3.12-003366?style=for-the-badge&logo=python&logoColor=white)
![Model](https://img.shields.io/badge/MODEL-GEMINI_2.5_FLASH-0047AB?style=for-the-badge&logo=google-gemini&logoColor=white)
![Framework](https://img.shields.io/badge/FRAMEWORK-PYDANTIC--AI_v1.39.0-006400?style=for-the-badge)
![Vector DB](https://img.shields.io/badge/VECTOR_DB-QDRANT_v1.16.2-8B4513?style=for-the-badge)
![Monitoring](https://img.shields.io/badge/MONITORING-LANGFUSE_v2.60.10-4B0082?style=for-the-badge)
![Backend](https://img.shields.io/badge/BACKEND-FASTAPI_v0.128.0-008B8B?style=for-the-badge)
![Media](https://img.shields.io/badge/MEDIA-MOVIEPY_v2.2.1-2F4F4F?style=for-the-badge)
![Compute](https://img.shields.io/badge/COMPUTE-CUDA_13.0_v2.9.1-800020?style=for-the-badge)

> "SUWERENNOŚĆ INŻYNIERYJNA ZACZYNA SIĘ TAM, GDZIE KOŃCZĄ SIĘ SUBSKRYPCJE SaaS. BUDUJEMY WŁASNY STOS TECHNOLOGICZNY."

---

## 00 // MANIFEST JEDNOSTKI

**OMNI-OPERATOR-V1** to system klasy **Modern AI Engineering** stworzony w ramach **KUŹNI OPERATORÓW**. Projekt służy do całkowitej automatyzacji procesu produkcji i dystrybucji wideo przy użyciu natywnego stosu technologicznego (Local-First/Sovereign AI).

**KLUCZOWE PARAMETRY:**

- **SILNIK:** Gemini 2.5 Flash (Multimodal Reasoning & Analysis).
- **LOGIKA:** PydanticAI (Typowani Agenci o wysokiej gęstości danych).
- **PAMIĘĆ:** Qdrant (Wektorowa baza doświadczeń i stylu).
- **OBSERWOWALNOŚĆ:** LangFuse
- **INFRASTRUKTURA:** Python 3.12 + uv + CUDA 13.0.

---

## 01 // ARCHITEKTURA SYSTEMU (CLEAN STACK)

Projekt realizuje wytyczne z sylabusa **TakzenAI HUB**:

1. **ANALIZA (M_05):** Multimodalne przetwarzanie obrazu i dźwięku przez SDK Gemini.
2. **AGENCJA (M_06):** Zarządzanie procesem przez agentów PydanticAI.
3. **MONTAŻ (M_02):** Automatyczna edycja wideo przez FFmpeg/MoviePy (Python Core).
4. **PAMIĘĆ (M_09):** RAG w bazie Qdrant do optymalizacji strategii treści.
5. **DYSTRYBUCJA (M_11):** Protokół MCP do zarządzania lokalnymi plikami i publikacją.

---

## 02 // PROTOKÓŁ INSTALACJI (UV + VS CODE)

Zalecane podejście inżynierskie przy użyciu menedżera **uv**.

### 1. KLONOWANIE REPOZYTORIUM

```bash
git clone https://github.com/takzen/omni-operator-v1.git
cd omni-operator-v1
```

### 2. SYNCHRONIZACJA ŚRODOWISKA

```bash
# uv stworzy .venv i zainstaluje zależności z uv.lock
uv sync
```

### 3. AKTYWACJA JEDNOSTKI

```bash
# Windows:
.\.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate
```

---

## 03 // KONFIGURACJA CUDA 13.0 (GPU ACCELERATION)

System wykorzystuje CUDA 13.0 do lokalnych operacji wideo i modeli embeddingowych. Konfiguracja znajduje się w `pyproject.toml`.

| WERSJA    | URL INDEKSU (UV)                         | KOMPATYBILNOŚĆ     |
| --------- | ---------------------------------------- | ------------------ |
| CUDA 13.0 | `https://download.pytorch.org/whl/cu130` | RTX 30xx/40xx/50xx |
| CPU (MAC) | `https://download.pytorch.org/whl/cpu`   | MacBook M1/M2/M3   |

Po zmianie w `pyproject.toml` uruchom: `uv sync`.

---

## 04 // STRUKTURA KATALOGÓW

```
OMNI-OPERATOR-V1/
├── src/                    # Kod źródłowy systemu
│   ├── agents/             # Definicje agentów PydanticAI (Gemini 2.5 Flash)
│   ├── core/               # Schematy danych (Pydantic) i konfiguracja globalna
│   ├── services/           # Integracje: FFmpeg, Qdrant, Langfuse
│   └── api/                # Serwery Model Context Protocol (dostęp do plików)
├── docker/                 #
├── notebooks/              #
├── pyproject.toml          # Konfiguracja projektu, zależności i indeksy CUDA
├── uv.lock                 # Zamrożone wersje bibliotek (generowane przez uv)
└── docker-compose.yml      # Kontenery infrastruktury (Qdrant, Langfuse, Postgres)
```

---

## 05 // Harmonogram operacji (Build-in-Public)

- [x] **Odcinek 0:** Setup infrastruktury (uv, Docker, CUDA 13.0).
- [x] **Odcinek 1:** Multimodalny wywiad – Gemini 2.5 Flash analizuje wideo.
- [x] **Odcinek 2:** Agentura typowana – PydanticAI (v1.39.0) w praktyce.
- [ ] **Odcinek 3:** Kod zamiast CapCuta – Automatyczny montaż przez Python.
- [ ] **Odcinek 4:** Pamięć długotrwała – Budowa strategii treści w Qdrant.
- [ ] **Odcinek 5:** Protokół dystrybucji – Automatyzacja "Omnipresence".

---

## STATUS: JEDNOSTKA_GOTOWA // DO_DZIAŁANIA

**ORGANIZACJA: KUŹNIA OPERATORÓW**

---

## PLIK `pyproject.toml` (KLUCZOWY DLA UV)

To jest serce Twojego setupu. Stwórz go w głównym folderze `omni-operator-v1/`.

```toml
[project]
name = "omni-operator-v1"
version = "0.1.0"
description = "Autonomiczna fabryka dystrybucji treści - Projekt z Kuźni Operatorów"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pydantic-ai>=0.0.18",
    "google-generativeai>=0.8.3",
    "fastapi>=0.115.0",
    "uvicorn>=0.30.0",
    "qdrant-client>=1.12.0",
    "langfuse<3.0.0",
    "moviepy>=1.0.3",
    "python-dotenv>=1.0.1",
    "torch",
    "torchvision",
    "torchaudio",
]

[tool.uv]
managed = true

[[tool.uv.index]]
name = "pytorch-cu130"
url = "https://download.pytorch.org/whl/cu130"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch-cu130" }
torchvision = { index = "pytorch-cu130" }
torchaudio = { index = "pytorch-cu130" }

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```
