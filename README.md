# 🤖 takzenai/omni-operator-v1

**Autonomiczna fabryka dystrybucji treści. Od surowego MP4 do dominacji w social mediach.**

![STATUS-OPERACYJNY](https://img.shields.io/badge/STATUS-OPERACYJNY-006400?style=for-the-badge)
![HACKATHON](https://img.shields.io/badge/HACKATHON-GEMINI_API_COMPETITION-blue?style=for-the-badge&logo=google)
![PYTHON](https://img.shields.io/badge/PYTHON-3.12-003366?style=for-the-badge&logo=python&logoColor=white)
![MODEL](https://img.shields.io/badge/MODEL-GEMINI_2.5_FLASH-0047AB?style=for-the-badge&logo=google-gemini&logoColor=white)

---

## 📜 MANIFEST

Budujemy **suwerenny stos technologiczny**, który eliminuje potrzebę korzystania z SaaS-ów do edycji i dystrybucji wideo. Wykorzystujemy natywną multimodalność **Gemini 2.5 Flash**, aby stworzyć system, który widzi, myśli i operuje bezpośrednio na plikach.

---

## 🗺️ ROADMAPA OPERACYJNA (HACKATHON EDITION)

### [ETAP 0] Mobilizacja i Poligon

- **Sovereign Stack Setup**: Konfiguracja Python 3.12 z menedżerem `uv` ✅ **ZAKOŃCZONO**
- **Definicja Infrastruktury**: `docker-compose.yml` dla Qdrant, Postgres i Langfuse v2 ✅ **ZAKOŃCZONO**
- **Uruchomienie Węzłów**: Start kontenerów i weryfikacja połączenia ✅ **ZAKOŃCZONO**

### [ETAP 1] Multimodalna Analiza (Native Gemini Vision)

- **Analiza Video-to-JSON**: Wykorzystanie Gemini 2.5 Flash do zrozumienia obrazu i dźwięku bez transkrypcji ✅ **ZAKOŃCZONO**
- **Ekstrakcja Planu Cięć**: Generowanie raportu `VideoAnalysisReport` ze znacznikami czasu ✅ **ZAKOŃCZONO**

### [ETAP 2] Agent Strategii i Copywritingu

- **Personalizacja Stylu**: Generowanie opisów pod TikTok, Reels, Shorts i LinkedIn w oparciu o PydanticAI ✅ **ZAKOŃCZONO**
- **Inżynieria Hashtagów**: System dobierania tagów pod viralowe zasięgi ✅ **ZAKOŃCZONO**

### [ETAP 3] Automatyczna Fabryka Wideo (FFmpeg Core) ✅ **ZAKOŃCZONO**

- **Precyzyjny Silnik Cięcia**: Skryptowe wycinanie fragmentów MP4 przez FFmpeg na podstawie instrukcji JSON od Agenta
- **Branding & Overlay**: Automatyczne napisy, logo i formatowanie do pionu (9:16) bezpośrednio przez kod

### [ETAP 4] Pamięć Długotrwała (Qdrant RAG) ✅ **ZAKOŃCZONO**

- **Baza Wiedzy o Contentcie**: Zapisywanie analiz i wyników w lokalnej bazie Qdrant
- **Pętla Optymalizacji**: Uczenie systemu stylu twórcy na podstawie historycznych sukcesów (RAG na metadanych)

### [ETAP 5] Dyrygent (FastAPI & Agentic Workers) ✅ **ZAKOŃCZONO**

- **Orkiestracja Workflows**: Budowa asynchronicznego API zarządzającego procesem: UPLOAD → ANALYZE → EDIT → QC
- **Agentic Quality Control**: Gemini 2.5 Flash weryfikuje zmontowany materiał przed publikacją

### [ETAP 6] Protokół Dystrybucji (MCP Integration) ✅ **ZAKOŃCZONO**

- **Model Context Protocol**: Użycie MCP, aby Gemini mogło zarządzać lokalnym systemem plików i dystrybucją
- **Omnipresence**: Automatyczna wysyłka na platformy social media i powiadomienie Operatora na Telegramie

---

## 🛠️ STOS TECHNOLOGICZNY (SOVEREIGN STACK)

| Komponent          | Technologia          | Rola                                        |
| ------------------ | -------------------- | ------------------------------------------- |
| **Mózg AI**        | Gemini 2.5 Flash     | Multimodalna analiza i rozumowanie          |
| **Agentura**       | PydanticAI (v1.39.0) | Logika agentyczna i typowane wyjścia danych |
| **Infrastruktura** | Docker & uv          | Zarządzanie kontenerami i pakietami         |
| **Monitoring**     | Langfuse v2          | Lokalny tracing i kontrola kosztów          |
| **Pamięć**         | Qdrant               | Wektorowa baza doświadczeń                  |
| **Media**          | FFmpeg / MoviePy     | Programowy montaż wideo                     |

---

## 🚀 DLACZEGO GEMINI 2.5 FLASH?

W ramach hackathonu udowadniamy, że **Gemini 2.5 Flash** to najlepszy model do zadań typu Media-Ops:

1. **Szybkość**: Błyskawiczna analiza klatek wideo pod kątem "hooków"
2. **Multimodalność**: Brak konieczności używania zewnętrznych modeli do transkrypcji (Whisper). Gemini widzi emocje i dynamikę obrazu
3. **Context**: Możliwość wrzucenia długich nagrań (podcastów) i pocięcia ich na dziesiątki Shortsów w jednej sesji

---

**Zbudowane z 🔥 dla Gemini API Developer Competition**
