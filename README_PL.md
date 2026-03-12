<div align="center">

<img src="readme_assets/icon_polsoft.png" width="64" alt="polsoft.ITS Logo"/>

# 🔏 SignTool Suite — Narzędzia do podpisywania kodu

**Profesjonalne GUI dla signtool.exe i OpenSSL | polsoft.ITS™ Group**

*Autorstwa: Sebastian Januchowski*

---

</div>

Zestaw trzech aplikacji desktopowych dla Windows, które zamieniają skomplikowane polecenia wiersza poleceń w przejrzysty, intuicyjny interfejs graficzny. Każde narzędzie odpowiada na inne potrzeby — od szybkiego testowania podpisów, przez codzienną pracę z certyfikatami, aż po pełne środowisko produkcyjne z obsługą OpenSSL i generatorem certyfikatów.

---

## 1. PublicTester QuickDigital Signature GUI `v1.1.0`

<img src="readme_assets/icon_publictester.png" width="36" align="left" style="margin-right:12px"/>

**Lekkie narzędzie do szybkiego weryfikowania podpisów cyfrowych**

<br clear="left"/>

Zaprojektowane z myślą o testerach i programistach, którzy chcą w kilka sekund podpisać plik i sprawdzić, czy cały łańcuch działa prawidłowo — bez żadnej konfiguracji. Aplikacja automatycznie wykrywa `signtool.exe` (Windows SDK) oraz certyfikaty `.pfx` w pobliskich folderach.

<div align="center">
<img src="readme_assets/PublicTester_QuickDigitalSignature_GUI_v1_1.png" width="420" alt="PublicTester GUI Screenshot"/>
</div>

### ✅ Kluczowe funkcje

| Funkcja | Opis |
|---|---|
| 🔍 Auto-wykrywanie | Automatycznie lokalizuje `signtool.exe` i certyfikaty `.pfx` |
| ⚡ Jedno kliknięcie | Podpisanie pliku jednym przyciskiem **Sign File** |
| 🔄 Fallback timestamp | Automatyczny retry z zapasowym serwerem timestampów |
| 🧵 Wątek tła | Podpisywanie nie blokuje interfejsu |
| 📋 Logi | Szczegółowe pliki logów do diagnostyki |

**Dla kogo?** Testerzy QA, programiści weryfikujący pipeline CI/CD, osoby stawiające pierwsze kroki z podpisywaniem kodu.

---

## 2. Quick DigitalSignature GUI `v1.9`

<img src="readme_assets/icon_quickds.png" width="36" align="left" style="margin-right:12px"/>

**Kompletne narzędzie do codziennego podpisywania plików**

<br clear="left"/>

Rozbudowana wersja narzędzia z pełnym zestawem operacji: podpisywanie, weryfikacja z Policy Authority i serwerem timestampów, instalacja certyfikatów CA. Obsługuje tryb jasny i ciemny, zapis hasła przez DPAPI, a pliki można przeciągać bezpośrednio do okna (drag & drop).

<div align="center">
<img src="readme_assets/Quick_DigitalSignature_v1_9_GUI.png" width="440" alt="Quick DigitalSignature GUI Screenshot"/>
</div>

### ✅ Kluczowe funkcje

| Funkcja | Opis |
|---|---|
| 🖱️ Drag & Drop | Przeciągnij plik wprost do okna aplikacji |
| 🔐 Bezpieczne hasło | Szyfrowanie hasła PFX przez Windows DPAPI |
| ✔️ Verify PA / PA+TS | Weryfikacja podpisu z Policy Authority i Timestamp |
| 🏛️ Instalacja CA | Install Root CA / Intermediate CA jednym kliknięciem |
| 🌗 Tryb ciemny | Pełna obsługa motywu ciemnego i jasnego |
| 💾 Zapis sesji | Zapamiętuje ostatnio używane pliki i certyfikat |

**Dla kogo?** Deweloperzy i inżynierowie release, którzy regularnie podpisują wiele plików i potrzebują pełnej kontroli nad procesem.

---

## 3. SignTool's-ITS GUI `v2.0`

<img src="readme_assets/icon_signtools.png" width="36" align="left" style="margin-right:12px"/>

**Profesjonalne środowisko produkcyjne — Microsoft signtool + OpenSSL**

<br clear="left"/>

Najbardziej zaawansowane narzędzie z pakietu. Łączy `signtool.exe` (Microsoft) z `openssl` w jednym, wielozakładkowym interfejsie z obsługą języka polskiego i angielskiego. Umożliwia nie tylko podpisywanie i weryfikację, ale też generowanie własnych certyfikatów i przetwarzanie wsadowe (batch).

<div align="center">
<img src="readme_assets/SignTools-ITS_v2.png" width="600" alt="SignTools-ITS GUI v2.0 Screenshot"/>
</div>

### ✅ Kluczowe funkcje

| Funkcja | Opis |
|---|---|
| 📑 5 zakładek | Sign, Timestamp/Verify, CatDB/Remove, Batch, Generuj certyfikat |
| 🔑 Generator certyfikatów | Tworzenie certyfikatów self-signed przez OpenSSL |
| 📦 Tryb wsadowy | Podpisywanie wielu plików naraz (Batch) |
| 🌍 PL / EN | Wbudowana obsługa języka polskiego i angielskiego |
| 🔎 Auto-wykrywanie narzędzi | Skanuje dyski w poszukiwaniu `signtool.exe` i `openssl.exe` |
| 🛡️ SHA256 / RFC3161 | Nowoczesne algorytmy podpisywania i timestampów |
| 📋 Podgląd komend | Przycisk **Pokaż komendę** przed wykonaniem |
| 🗃️ CatDB | Obsługa katalogów certyfikatów Windows (.cat) |
| ⚙️ Cross-certification | Obsługa dodatkowych certyfikatów `/ac` |

**Dla kogo?** Firmy software'owe, release managerowie, administratorzy PKI — wszyscy, którzy potrzebują pełnego środowiska podpisywania kodu w jednym miejscu.

---

## 📦 Podsumowanie

| | PublicTester v1.1.0 | Quick DS v1.9 | SignTools-ITS v2.0 |
|---|:---:|:---:|:---:|
| Podpisywanie pliku | ✅ | ✅ | ✅ |
| Weryfikacja podpisu | — | ✅ | ✅ |
| Drag & Drop | — | ✅ | — |
| Tryb ciemny | — | ✅ | — |
| Generowanie certyfikatów | — | — | ✅ |
| Tryb wsadowy (Batch) | — | — | ✅ |
| Obsługa OpenSSL | — | — | ✅ |
| Język PL/EN | — | — | ✅ |
| Poziom trudności | 🟢 Prosty | 🟡 Średni | 🔴 Zaawansowany |

---

<div align="center">

**polsoft.ITS™ Group** • polsoft.its@fastservice.com • [github.com/seb07uk](https://github.com/seb07uk)

*Copyright © 2026 polsoft.ITS™. All rights reserved.*

<img src="readme_assets/icon_polsoft.png" width="32" alt="polsoft.ITS"/>

</div>
