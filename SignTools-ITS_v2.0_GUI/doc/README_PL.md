# SignTool's-ITS GUI v2.0

> **Graficzny interfejs podpisywania kodu i generowania certyfikatów**  
> Microsoft SignTool & OpenSSL — Windows | v2.0

---

![SignTool's-ITS GUI](https://raw.githubusercontent.com/seb07uk/seb07uk/main/signtool_preview.png)

> *Zrzut ekranu: Główne okno aplikacji — zakładka Sign z wyborem certyfikatu i opcjami podpisywania*

---

## Opis

**SignTool's-ITS GUI** to profesjonalny graficzny interfejs dla `signtool.exe` (Microsoft) i `openssl.exe`, zapewniający kompletny przepływ pracy podpisywania kodu przez przejrzysty, dwujęzyczny (PL/EN) interfejs zbudowany na Python Tkinter.

Nie jest wymagana znajomość wiersza poleceń — wszystkie operacje podpisywania, znacznikowania czasu, weryfikacji i obsługi certyfikatów są dostępne przez intuicyjne zakładki i pola formularzy.

---

## Funkcjonalności

| Kategoria | Możliwości |
|---|---|
| **Sign** | Podpisywanie EXE, DLL, skryptów; plik PFX lub magazyn certyfikatów Windows; algorytmy SHA-256/SHA-512 |
| **Timestamp** | Serwery znaczników czasu RFC3161 (nowoczesny) i Authenticode (legacy) |
| **Verify** | Weryfikacja wszystkich podpisów (`/pa`), podpisów strony (`/pg`), opcjonalny plik katalogu |
| **CatDB** | Dodawanie/usuwanie plików katalogu do/z bazy katalogów Windows |
| **Remove** | Usuwanie podpisów Authenticode z plików binarnych |
| **Batch** | Edytor plików odpowiedzi — wykonywanie plików odpowiedzi signtool bezpośrednio z GUI |
| **Generator certyfikatów** | Generowanie certyfikatów samopodpisanych, Root CA lub podpisanych przez CA via OpenSSL lub PowerShell |
| **Język** | Pełny dwujęzyczny interfejs PL / EN przełączany w czasie działania |

---

## Wymagania

- **System:** Windows 10 / 11 (64-bit)
- **Python:** 3.9+ (tylko biblioteka standardowa — brak zewnętrznych pakietów)
- **signtool.exe:** Część Windows SDK — automatycznie wykrywany przy starcie
- **openssl.exe:** Wymagany do generowania certyfikatów — automatycznie wykrywany przy starcie

> Aplikacja skanuje wszystkie dyski przy uruchomieniu i raportuje, które narzędzia zostały znalezione. Brakujące narzędzia można wskazać ręcznie przez okno dialogowe.

---

## Instalacja i uruchomienie

```bash
# Sklonuj lub pobierz main.py
git clone https://github.com/seb07uk/signtool-its-gui

# Uruchom bezpośrednio — instalacja niepotrzebna
python main.py
```

Lub zbuduj samodzielny plik EXE:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile main.py
```

---

## Zakładki aplikacji

### Sign
Wybierz pliki do podpisania, certyfikat (z magazynu Windows po nazwie/SHA1 lub z pliku PFX z hasłem), skonfiguruj algorytm hash, opis, URL i serwer znaczników czasu. Obsługiwane jest podwójne podpisywanie (dołącz `/as`) i tryb debugowania.

### Timestamp / Verify
Dodaj znacznik czasu do już podpisanych plików lub zweryfikuj istniejące podpisy względem katalogu.

### CatDB / Remove
Zarządzaj bazą katalogów Windows i usuwaj podpisy z plików binarnych.

### Batch
Wczytaj, edytuj i wykonuj pliki odpowiedzi signtool. Każdy argument w osobnej linii; pierwsza linia to komenda (`sign`, `verify` itp.).

### 🔑 Generuj certyfikat
Generuj certyfikaty za pomocą OpenSSL lub PowerShell `New-SelfSignedCertificate`. Obsługuje:
- **Samopodpisany** — do testów
- **Root CA** — urząd certyfikacji
- **Podpisany przez CA** — wymaga istniejących plików Root CA

Konfigurowalne: algorytm klucza (RSA / EC), rozmiar klucza, algorytm hash, okres ważności, pola Subject (CN, O, C, L, ST, email), SAN (DNS + IP), eksport PFX, instalacja w magazynie Windows.

### Opcje
Przełącznik języka (Polski / English) i konfiguracja ścieżek narzędzi.

---

## Automatyczne wykrywanie narzędzi

Przy uruchomieniu SignTool's-ITS GUI przeszukuje wszystkie dostępne dyski w poszukiwaniu `signtool.exe` i `openssl.exe`. Dialog podsumowania raportuje:

- ✅ Znaleziono — wyświetlana ścieżka
- ⚠️ Nie znaleziono — opcja ręcznego wskazania

---

## Informacje architektoniczne

- **Aplikacja jednoplikowa** — cała logika w `main.py` (~5 500 linii)
- **Wbudowany system tłumaczeń** — słownik `_TR` z kluczami `pl`/`en`; brak zewnętrznej biblioteki i18n
- **Wymuszanie UTF-8** — stdout/stderr rekonfigurowane przy starcie; flaga `CREATE_NO_WINDOW` stosowana globalnie do wszystkich wywołań subprocess na Windows, aby zapobiec błyskaniu konsoli
- **Wątki** — wszystkie wywołania subprocess działają w wątkach-demonach; wyniki są przesyłane strumieniowo linia po linii do widgetu tekstowego GUI z kolorowymi znacznikami (sukces / błąd / komenda / info)
- **Wbudowane zasoby** — ikony i obrazy przechowywane jako ciągi Base64

---

## Autor i licencja

| Pole | Wartość |
|---|---|
| **Autor** | Sebastian Januchowski |
| **Firma** | polsoft.ITS™ Group |
| **Kontakt** | polsoft.its@fastservice.com |
| **GitHub** | https://github.com/seb07uk |
| **Copyright** | 2026© polsoft.ITS™. Wszelkie prawa zastrzeżone. |
| **Licencja** | Własnościowa |

---

> © 2026 polsoft.ITS™ Group. Wszelkie prawa zastrzeżone. Nieautoryzowana dystrybucja zabroniona.
