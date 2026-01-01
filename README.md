# 🤖 takzenai/omni-operator-v1

**Autonomiczna fabryka dystrybucji treści. Od surowego MP4 do dominacji w social mediach.**

![STATUS-OPERACYJNY](https://img.shields.io/badge/STATUS-OPERACYJNY-FF0000?style=for-the-badge)
![HACKATHON](https://img.shields.io/badge/HACKATHON-GEMINI_API_COMPETITION-blue?style=for-the-badge&logo=google)
![PYTHON](https://img.shields.io/badge/PYTHON-3.12-003366?style=for-the-badge&logo=python&logoColor=white)
![MODEL](https://img.shields.io/badge/MODEL-GEMINI_3_FLASH_PREVIEW-0047AB?style=for-the-badge&logo=google-gemini&logoColor=white)

> 🏆 **Zgłoszenie konkursowe**: [Gemini API Developer Competition](https://gemini3.devpost.com/)

---

## 🎯 PROBLEM, KTÓRY ROZWIĄZUJEMY

Content creatorzy tracą **godziny** na żmudną, manualną pracę:

- 🎬 Oglądanie długich nagrań w poszukiwaniu "viralnych momentów" (tzw. hooks).
- ✂️ Cięcie i formatowanie pod wymogi różnych platform.
- ✍️ Pisanie unikalnych opisów, strategii i dobieranie hashtagów.
- 📁 Organizację i fizyczną dystrybucję plików.

**Nasza wizja**: Jeden upload → Pełna automatyzacja agentyczna → Wygenerowane Shortsy i posty gotowe do publikacji w interfejsie klasy premium.

---

## 💡 NASZE ROZWIĄZANIE

**Omni-Operator v1** to suwerenny system AI, który wykorzystuje **Gemini 3 Flash Preview** jako multimodalny procesor decyzyjny do:

- **Multimodalnej analizy (Native Vision)** - Gemini "ogląda" wideo przez nowe SDK `google-genai` i rozumie kontekst wizualny + audio bez żadnych pośrednich narzędzi.
- **Inteligentnego montażu** - Automatyczne wykrywanie najlepszych momentów i generowanie instrukcji dla silnika montażowego.
- **Agentury Copywriterskiej** - Tworzenie unikalnych postów na TikTok, YouTube i LinkedIn zwalidowanych przez PydanticAI.
- **Tactical HUD Interface** - Nowoczesny, agentyczny interfejs użytkownika w stylu "Mission Control" z efektami scanlines, CRT i szklanymi panelami.

---

## 🏗️ ARCHITEKTURA SYSTEMU

```mermaid
graph TD
    User([👤 Operator/User]) -->|Upload MP4| API[🎯 FastAPI Conductor]
    UI[🖥️ Tactical HUD Frontend] <--> API

    subgraph Brain["🧠 Mózg Agentyczny (Gemini 3 Flash Preview + PydanticAI)"]
        API -->|Trigger| Analyst[📊 Agent Analityk]
        Analyst -->|Extract Hooks JSON| Copywriter[✍️ Agent Copywriter]
        Copywriter -->|Generate Posts| Memory[(🗄️ Qdrant Vector DB)]
    end

    subgraph Factory["🎬 Fabryka Mediów"]
        Copywriter -->|Instructions| VideoEngine[⚙️ MoviePy / FFmpeg]
        VideoEngine -->|Render Clips| Storage[💾 Local File System]
    end

    API -.->|Tracing & Costs| Langfuse[(📈 Langfuse v2)]

    classDef userNode fill:#e1f5ff,stroke:#01579b,stroke-width:3px,color:#000
    classDef uiNode fill:#ffebee,stroke:#c21d1d,stroke-width:2px,color:#000
    classDef agentNode fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef storageNode fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000

    class User userNode
    class UI uiNode
    class Analyst,Copywriter agentNode
    class Memory,Storage,Langfuse storageNode
```

## � MISSION VISUALS (TACTICAL HUD)

### FAZA 01: GOTOWOŚĆ_OPERACYJNA (MISSION_READY)
> *Stan gotowości systemu przed przesłaniem materiału źródłowego.*
![Mission Ready](./docs/image/before.webp)

### FAZA 02: HANGAR_ZASOBÓW (ASSET_HANGAR)
> *Podgląd wygenerowanych treści, strategii social media i zmontowanych klipów.*
![Asset Hangar](./docs/image/before.webp)

---

## 🚀 DLACZEGO GEMINI 3 FLASH PREVIEW?

- ✅ **Szybkość**: Błyskawiczna analiza multimodalna.
- ✅ **Native Video Grounding**: Precyzyjne łączenie treści z czasem (sekundy).
- ✅ **Google Cloud Integration**: Wykorzystanie najnowszego SDK `google-genai` dla bezpiecznego przetwarzania plików.

---

## 🛠️ STOS TECHNOLOGICZNY

| Komponent          | Technologia          | Rola                                        |
20. | ------------------ | -------------------- | ------------------------------------------- |
103. | **Mózg AI**        | Gemini 3 Flash Prev  | Multimodalna analiza i reasoning            |
104. | **Agentura**       | PydanticAI           | Logika agentyczna i typowane wyjścia danych |
105. | **Frontend**       | Next.js 16 + Tailwind 4 | Interfejs Tactical HUD                    |
106. | **Infrastruktura** | Docker & uv          | Zarządzanie kontenerami i pakietami         |
107. | **Monitoring**     | Langfuse v2          | Lokalny tracing i kontrola kosztów          |
108. | **Baza Wektorowa** | Qdrant               | Pamięć doświadczeń                          |
109. | **Serwer API**     | FastAPI              | Dyrygent całego workflowu                   |

---

## 🚀 JAK URUCHOMIĆ

### 1. Przygotowanie Backend (API)
```bash
# Wejdź do folderu głównego
uv sync
docker-compose up -d
# Skonfiguruj .env (GOOGLE_API_KEY, LANGFUSE_*)
uv run src/api/main.py
```

### 2. Przygotowanie Frontend (Web)
```bash
cd web
pnpm install
pnpm dev
# Otwórz http://localhost:4000
```

---

## 🏆 GEMINI API DEVELOPER COMPETITION

Projekt udowadnia, że **Gemini 3 Flash Preview** jest gotowy do roli autonomicznego "Operatora" w najnowocześniejszych systemach Media-Ops.

**Zbudowane z 🔥 przez KUŹNIĘ OPERATORÓW**

