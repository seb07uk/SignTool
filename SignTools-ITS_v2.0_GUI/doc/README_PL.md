<div align="center">

<img src="Ikona SignTool's-ITS2.ico" alt="SignTool's-ITS Logo" width="96"/>

# SignTool's-ITS GUI v2.0

**Graficzny interfejs podpisywania kodu i generowania certyfikatów**

*Microsoft SignTool & OpenSSL — Windows 7 / 8 / 10 / 11*

[![Wersja](https://img.shields.io/badge/wersja-2.0.0-0078D4?style=flat-square)](https://github.com/seb07uk)
[![Platforma](https://img.shields.io/badge/platforma-Windows-0078D4?style=flat-square&logo=windows)](https://github.com/seb07uk)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Licencja](https://img.shields.io/badge/licencja-Proprietary-c0392b?style=flat-square)](LICENSE)
[![Firma](https://img.shields.io/badge/polsoft.ITS™-Group-0a1a2e?style=flat-square)](https://github.com/seb07uk)
[![Język](https://img.shields.io/badge/UI-PL%20%2F%20EN-27ae60?style=flat-square)](#dwujęzyczny-interfejs-plen)

---

*Profesjonalny, przenośny plik EXE — pełna moc Microsoft SignTool i OpenSSL w przejrzystym, nowoczesnym interfejsie graficznym. Bez wiersza poleceń.*

</div>

---

## Spis treści

- [Przegląd](#przegląd)
- [Funkcje w skrócie](#funkcje-w-skrócie)
- [Wymagania systemowe](#wymagania-systemowe)
- [Instalacja i kompilacja](#instalacja-i-kompilacja)
- [Zakładki i moduły — pełny opis](#zakładki-i-moduły--pełny-opis)
  - [Sign — Podpisywanie kodu](#1--sign--podpisywanie-kodu)
  - [Timestamp / Verify — Znacznik czasu / Weryfikacja](#2--timestamp--verify)
  - [CatDB / Remove — Baza katalogów / Usuwanie podpisów](#3--catdb--remove)
  - [Batch — Plik odpowiedzi (wsadowy)](#4--batch--plik-odpowiedzi-wsadowy)
  - [Generuj certyfikat](#5--generuj-certyfikat)
- [Typy i metody podpisywania](#typy-i-metody-podpisywania)
- [Typy certyfikatów](#typy-certyfikatów)
- [Parametry kryptograficzne](#parametry-kryptograficzne)
- [Automatyczne wykrywanie narzędzi](#automatyczne-wykrywanie-narzędzi)
- [Konfiguracja i trwałość ustawień](#konfiguracja-i-trwałość-ustawień)
- [Dwujęzyczny interfejs PL/EN](#dwujęzyczny-interfejs-plen)
- [Struktura projektu](#struktura-projektu)
- [System budowania](#system-budowania)
- [Architektura i uwagi techniczne](#architektura-i-uwagi-techniczne)
- [Autor i kontakt](#autor-i-kontakt)
- [Licencja](#licencja)

---

## Przegląd

**SignTool's-ITS GUI v2.0** to kompleksowy graficzny front-end opracowany przez **polsoft.ITS™ Group** dla dwóch branżowych narzędzi:

- **Microsoft `signtool.exe`** — oficjalne narzędzie do podpisywania kodu w systemie Windows, wchodzące w skład Windows SDK
- **`openssl.exe`** — wieloplatformowy zestaw narzędzi kryptograficznych

Aplikacja eliminuje konieczność zapamiętywania złożonych flag wiersza poleceń, udostępniając wszystkie możliwości podpisywania, znacznikowania czasu, weryfikacji i generowania certyfikatów za pośrednictwem czytelnego interfejsu z zakładkami. Wszystkie operacje wykonywane są asynchronicznie — GUI pozostaje responsywne podczas pracy poleceń w tle, a wyniki są wyświetlane na bieżąco z kolorowaniem składni bezpośrednio w panelu wyniku.

Aplikacja dostarczana jest jako **pojedynczy przenośny plik `.exe`** — bez instalatora, bez zewnętrznych zależności, bez praw administratora.

> **Docelowi użytkownicy:** Deweloperzy oprogramowania, administratorzy IT, inżynierowie DevOps, oficerowie ds. podpisywania kodu i specjaliści ds. bezpieczeństwa, którzy na co dzień podpisują pliki binarne, sterowniki, instalatory, skrypty lub pliki katalogów w systemie Windows.

---

## Funkcje w skrócie

| Funkcja | Szczegóły |
|---|---|
| 🔎 **Automatyczne wykrywanie** | Skanuje wszystkie dyski w poszukiwaniu `signtool.exe` i `openssl.exe` przy starcie; wskaźniki LED statusu |
| 🖊️ **Podpisywanie kodu** | Pełna obsługa `signtool sign` — EXE, DLL, SYS, MSI, CAT, PS1 i każdy inny format |
| ⏱️ **Znacznikowanie czasu** | Protokoły RFC 3161 (`/tr`) i Authenticode (`/t`), wybieralne osobno dla każdej operacji |
| ✅ **Weryfikacja podpisów** | `signtool verify` z opcjami `/pa`, `/pg`, `/v` oraz plikiem katalogu (`/c`) |
| 🗂️ **Zarządzanie CatDB** | Dodawanie (`/u`) i usuwanie (`/r`) plików katalogów z bazy katalogów systemu Windows |
| 🗑️ **Usuwanie podpisów** | Usuwanie podpisów Authenticode z dowolnego podpisanego pliku (`signtool remove /s`) |
| 📦 **Tryb wsadowy** | Pełna obsługa `signtool @plik_odpowiedzi` z wbudowanym edytorem, wczytywaniem i zapisem |
| 🔑 **Generowanie certyfikatów** | Certyfikaty self-signed, Root CA i podpisane przez CA — przez OpenSSL lub PowerShell |
| 🌐 **Dwujęzyczny UI** | Polski i angielski z przełączaniem języka w czasie działania — bez restartu |
| 🔐 **Magazyn certyfikatów** | Podpisywanie z magazynu certyfikatów Windows (przez nazwę lub SHA1) lub z pliku PFX |
| 📋 **Cross-certification** | Obsługa dodatkowego certyfikatu (`/ac`) dla łańcuchów cross-certyfikacji |
| 🛑 **Przycisk Stop** | Natychmiastowe zatrzymanie dowolnego uruchomionego procesu `signtool`/`openssl`/`powershell` |
| 💾 **Trwałość ustawień** | Stan formularzy, ścieżki narzędzi i język zapisywane do pliku `SignToolGUI.json` |
| 🖥️ **DPI Aware** | Obsługa Per-Monitor DPI V2 — ostre renderowanie na ekranach HiDPI i 4K |
| 🚀 **Przenośny EXE** | Jednolikowy build PyInstallera — skopiuj i uruchom gdziekolwiek |
| 🔇 **Brak migania konsoli** | Manifest Windows + `CREATE_NO_WINDOW` eliminują miganie okna konsoli podprocesów |
| 🎨 **Kolorowanie wyniku** | Sukces (zielony), błąd (czerwony), ostrzeżenie (pomarańczowy), polecenie (błękitny) — ciemny motyw |
| ⚙️ **Dymki podpowiedzi** | 2-sekundowe tooltopy na każdej kontrolce, dynamicznie tłumaczone przy zmianie języka |

---

## Wymagania systemowe

| Komponent | Wymaganie |
|---|---|
| **System operacyjny** | Windows 7 SP1 / 8 / 8.1 / 10 / 11 (x64) |
| **Python** *(tylko do kompilacji ze źródeł)* | Python 3.8 lub nowszy |
| **PyInstaller** *(tylko do kompilacji ze źródeł)* | Instalowany automatycznie przez skrypt budowania |
| **signtool.exe** | Windows SDK — wykrywany automatycznie lub wskazywany ręcznie |
| **openssl.exe** | OpenSSL dla Windows — wykrywany automatycznie lub wskazywany ręcznie |
| **PowerShell** | Wymagany tylko dla metody generowania certyfikatów przez PowerShell |
| **Uprawnienia** | Zwykły użytkownik — **brak wymogu praw administratora** (admin potrzebny tylko do instalacji certyfikatu w magazynie komputera) |

> Skompilowany `SignTool.exe` **nie wymaga instalacji Pythona**. Python jest potrzebny tylko podczas budowania ze źródeł.

---

## Instalacja i kompilacja

### Wariant A — Użycie gotowego pliku EXE

Katalog `app/` zawiera plik gotowy do uruchomienia:

```
SignTools-ITS_v2.0_GUI/
└── app/
    └── SignTools-ITS v2.0 GUI.exe   ← uruchom bezpośrednio, bez instalacji
```

Skopiuj plik w dowolne miejsce i uruchom. Aplikacja automatycznie wykryje narzędzia przy pierwszym uruchomieniu.

### Wariant B — Kompilacja ze źródeł

**Warunek wstępny:** Python 3.8+ musi być dostępny w zmiennej `PATH`.

```batch
cd SignTools-ITS_v2.0_GUI
SignTool_GUI_v2.0_build.bat
```

Skrypt budowania wykonuje automatycznie sześć kroków:

```
[1/6]  Weryfikacja instalacji Pythona
[2/6]  Instalacja PyInstallera (jeśli brak)
[3/6]  Weryfikacja obecności wszystkich plików źródłowych
[4/6]  Czyszczenie poprzednich artefaktów (dist/, build/)
[5/6]  Kompilacja przy użyciu PyInstallera i pliku SignTool.spec
[6/6]  Sprzątanie po kompilacji → wynik: dist\SignTool.exe
```

Po pomyślnej kompilacji katalog `dist\` jest automatycznie otwierany w Eksploratorze.

> **Uwaga dotycząca oprogramowania antywirusowego:** Niektóre programy AV flagują świeżo skompilowane pliki EXE PyInstallera jako podejrzane. Przed kompilacją dodaj folder projektu do wyjątków AV.

---

## Zakładki i moduły — pełny opis

Aplikacja podzielona jest na pięć głównych zakładek, z których każda posiada wewnętrzną zakładkę **Opcje** (konfiguracja) oraz **Wynik** (live output polecenia).

---

### 1 · Sign — Podpisywanie kodu

Zakładka Sign udostępnia pełne polecenie `signtool sign` przez przewijalny formularz.

#### Pliki do podpisania

Wieloplikowy listbox obsługuje EXE, DLL, SYS, MSI, CAT, PS1 i każdy inny format. Pliki dodaje się przyciskiem **Dodaj pliki** (otwiera wielokrotny wybór) i można je usuwać pojedynczo lub wszystkie naraz.

#### Sekcja Certyfikat

Dwa wzajemnie wykluczające się źródła certyfikatu, wybierane przyciskami radio:

**Z magazynu certyfikatów Windows**

| Pole | Flaga SignTool | Opis |
|---|---|---|
| Nazwa certyfikatu | `/n` | Dopasowanie podciągu nazwy podmiotu w magazynie |
| SHA1 certyfikatu | `/sha1` | Dokładny 40-znakowy odcisk szesnastkowy |

Oba pola można wypełnić jednocześnie — SignTool użyje ich łącznie do zawężenia wyboru.

**Z pliku PFX**

| Pole | Flaga SignTool | Opis |
|---|---|---|
| Plik certyfikatu | `/f` | Ścieżka do pliku `.pfx` |
| Hasło | `/p` | Hasło klucza prywatnego PFX (maskowane, nigdy niezapisywane na dysk) |

**Dodatkowy certyfikat (Cross-certification)**

| Pole | Flaga SignTool | Opis |
|---|---|---|
| Dodatkowy cert | `/ac` | Ścieżka do dodatkowego pliku `.cer` lub `.crt` dla łańcuchów cross-certyfikacji |

#### Opcje podpisywania

| Opcja | Flaga SignTool | Opis |
|---|---|---|
| Algorytm hash | `/fd` | Algorytm skrótu pliku: SHA1, SHA256, SHA384, SHA512 |
| Opis | `/d` | Opis czytelny dla człowieka osadzony w podpisie |
| URL | `/du` | URL osadzony w podpisie (Authenticode description URL) |

#### Opcje znacznika czasu

| Opcja | Flaga SignTool | Opis |
|---|---|---|
| URL serwera timestamp | `/tr` lub `/t` | Adres URL serwera TSA |
| **RFC 3161** (radio) | `/tr` + `/td` | Nowoczesny protokół RFC 3161 — **zalecany do wszystkich nowych podpisań** |
| **Authenticode** (radio) | `/t` | Starszy protokół Authenticode — dla kompatybilności z Windows XP / Server 2003 |
| Hash znacznika czasu | `/td` | Algorytm skrótu znacznika (SHA1 / SHA256 / SHA384 / SHA512) — tylko RFC 3161 |

> **Najlepsza praktyka:** Zawsze używaj RFC 3161 (`/tr`), chyba że wymagana jest kompatybilność z systemami sprzed Vista. Znaczniki Authenticode (`/t`) używają SHA1 i nie obsługują opcji `/td`.

#### Dodatkowe flagi

| Pole wyboru | Flaga SignTool | Opis |
|---|---|---|
| Dołącz podpis | `/as` | Dodaje drugi podpis bez usuwania istniejącego (podwójne podpisywanie) |
| Tryb szczegółowy | `/v` | Wyświetla szczegółowe informacje o podpisaniu |
| Tryb debug | `/debug` | Wyświetla informacje diagnostyczne do rozwiązywania problemów |

#### Przyciski akcji

- **🔏 Podpisz** — Wykonuje `signtool sign` ze wszystkimi skonfigurowanymi opcjami; automatycznie przełącza na zakładkę Wynik
- **Pokaż komendę** — Wyświetla pełny ciąg polecenia w zakładce Wynik bez jego wykonywania

---

### 2 · Timestamp / Verify

Zakładka łączy dwie operacje w jednym pionie dzielonym panelu, każda z własnym obszarem wyniku.

#### Sekcja Timestamp

Dodaje znacznik czasu RFC 3161 lub Authenticode do już podpisanych plików (bez ponownego podpisywania).

| Pole | Flaga SignTool | Opis |
|---|---|---|
| Pliki | — | Listbox wieloplikowy (EXE, DLL, SYS) |
| Adres URL serwera | `/tr` lub `/t` | Adres serwera TSA |
| **RFC 3161** (radio) | `/tr` | Nowoczesny protokół znacznika czasu |
| **Authenticode** (radio) | `/t` | Starszy protokół znacznika czasu |
| Hash (`/td`) | `/td` | Skrót znacznika (tylko RFC 3161): SHA1, SHA256, SHA384, SHA512 |
| Tryb szczegółowy | `/v` | Szczegółowy wynik operacji |

**Akcja:** **Dodaj timestamp** — uruchamia `signtool timestamp` w wątku tła.

#### Sekcja Verify

Weryfikuje podpis cyfrowy na jednym lub wielu plikach.

| Pole | Flaga SignTool | Opis |
|---|---|---|
| Pliki | — | Listbox wieloplikowy |
| Weryfikuj wszystkie podpisy | `/pa` | Używa domyślnej polityki uwierzytelniania do weryfikacji wszystkich podpisów |
| Weryfikuj podpis strony | `/pg` | Weryfikuje skrót strony osadzony w podpisie |
| Tryb szczegółowy | `/v` | Wyświetla pełny łańcuch i szczegóły podpisu |
| Plik katalogu | `/c` | Wskazuje plik `.cat` do weryfikacji |

**Akcja:** **Weryfikuj** — uruchamia `signtool verify` i strumieniuje wynik do panelu Wynik Verify.

---

### 3 · CatDB / Remove

Kolejna zakładka łączona z dwiema niezależnymi sekcjami operacji.

#### Sekcja CatDB

Zarządza wpisami w bazie katalogów systemu Windows (`catdb`).

| Pole | Flaga SignTool | Opis |
|---|---|---|
| Plik katalogu | — | Ścieżka do pliku `.cat` |
| Akcja | `/u` lub `/r` | **Dodaj** (`/u` — przypisz unikalny ID) lub **Usuń** (`/r`) katalog |
| Tryb szczegółowy | `/v` | Szczegółowy wynik |
| Domyślna baza katalogów | `/d` | Zawsze dołączana — używa domyślnej systemowej bazy katalogów |

**Akcja:** **Wykonaj CatDB** — uruchamia `signtool catdb /d [/u|/r] <plik>`.

#### Sekcja Remove — Usuwanie podpisów

Usuwa wszystkie podpisy Authenticode z podpisanych plików.

| Pole | Flaga SignTool | Opis |
|---|---|---|
| Pliki | — | Listbox wieloplikowy |
| Usuń podpisy Authenticode | `/s` | **Zawsze aktywna** — flaga wymagana; `signtool remove` zawsze wymaga `/s` |
| Tryb szczegółowy | `/v` | Szczegółowy wynik |

> **Uwaga:** Flaga `/s` jest obowiązkowa i nie można jej odznaczyć — to wymaganie narzędzia `signtool`, nie ograniczenie GUI.

**Akcja:** **Usuń podpisy** — uruchamia `signtool remove /s [/v] <pliki>`.

---

### 4 · Batch — Plik odpowiedzi (wsadowy)

Wykonuje `signtool` przy użyciu pliku odpowiedzi (zwanego też „plikiem wsadowym"), w którym całe polecenie zdefiniowane jest jako jeden argument w każdej linii.

#### Format pliku odpowiedzi

```
sign
/n
Mój Certyfikat Podpisywania Kodu
/fd
SHA256
/tr
http://timestamp.digicert.com
/td
SHA256
MojaAplikacja.exe
```

Pierwsza linia to podpolecenie `signtool`; kolejne linie to jego argumenty w kolejności.

#### Funkcje

- **Wbudowany edytor tekstu** — Edytuj plik odpowiedzi bezpośrednio w GUI, czcionką monospace z poziomym przewijaniem
- **Wczytaj** — Importuj istniejący plik `.txt` z dysku
- **Zapisz** — Eksportuj bieżącą zawartość edytora do pliku `.txt`
- **Wyczyść** — Opróżnij edytor jednym kliknięciem
- **Wykonaj plik odpowiedzi** — Zapisuje zawartość edytora do pliku tymczasowego i uruchamia `signtool @<plik_tymcz>` w wątku tła; plik tymczasowy jest usuwany dopiero po zakończeniu procesu (bez wyścigu)

---

### 5 · Generuj certyfikat

Najbogatsza w funkcje zakładka — obsługuje trzy typy certyfikatów i dwa silniki generowania.

#### Metoda generowania

| Metoda | Opis |
|---|---|
| **OpenSSL** *(zalecana)* | Wieloplatformowa, pełna kontrola nad wszystkimi parametrami; obsługuje RSA i EC, rozszerzenia SAN i łańcuchy CA |
| **PowerShell** `New-SelfSignedCertificate` | Natywna dla Windows; generuje bezpośrednio do magazynu certyfikatów; eksportuje do PFX i CRT |

Po wyborze OpenSSL wyświetlana jest ścieżka do `openssl.exe` (wykrywana automatycznie z konfiguracji, folderu aplikacji, `_MEIPASS`, `PATH` i typowych lokalizacji instalacji).

#### Typ certyfikatu

| Typ | Opis |
|---|---|
| **Self-signed** (samopodpisany) | Samodzielny certyfikat; zawiera rozszerzenia `extendedKeyUsage=codeSigning` i `keyUsage=digitalSignature` |
| **Root CA** (urząd certyfikacji) | Certyfikat urzędu certyfikacji; zawiera `basicConstraints=critical,CA:TRUE` i `keyUsage=critical,keyCertSign,cRLSign` |
| **Podpisany przez CA** | Certyfikat końcowy podpisany przez istniejące Root CA; najpierw generuje CSR, następnie podpisuje go przy użyciu dostarczonego certyfikatu i klucza CA |

#### Dane certyfikatu (Subject)

| Pole | Flaga OpenSSL | Opis |
|---|---|---|
| Nazwa (CN) | `CN=` | Nazwa pospolita (Common Name) — wymagana |
| Organizacja (O) | `O=` | Nazwa organizacji |
| Kraj (C) | `C=` | Dwuliterowy kod kraju ISO (np. `PL`, `US`) — walidowany |
| Miejscowość (L) | `L=` | Miejscowość / miasto |
| Województwo (ST) | `ST=` | Stan lub województwo |
| E-mail | `emailAddress=` | Adres e-mail kontaktu — walidowany pod kątem obecności `@` |

#### Parametry kryptograficzne

| Parametr | Opcje | Opis |
|---|---|---|
| Algorytm klucza | RSA / EC | RSA używa stałego rozmiaru klucza; EC używa nazwanej krzywej |
| Rozmiar klucza RSA | 2048 / 3072 / 4096 | Bity; 2048 to aktualnie zalecane minimum |
| Krzywa EC | prime256v1 / secp384r1 / secp521r1 | NIST P-256, P-384, P-521 |
| Algorytm hash | sha256 / sha384 / sha512 | Algorytm skrótu podpisu |
| Ważność | 1 – N dni | Czas życia certyfikatu w dniach; walidowany jako dodatnia liczba całkowita |

#### Subject Alternative Names (SAN) — opcjonalne

| Pole | Rozszerzenie | Opis |
|---|---|---|
| Nazwy DNS | `DNS:` | Jedna nazwa hosta na linię (np. `localhost`, `mojapp.example.com`) |
| Adresy IP | `IP:` | Jeden adres IP na linię (np. `127.0.0.1`, `192.168.1.10`) |

Rozszerzenia SAN są zapisywane do pliku tymczasowego (kompatybilność z Windows; omija ograniczenie `/dev/stdin`).

#### Certyfikat CA (tylko tryb Podpisany przez CA)

| Pole | Flaga OpenSSL | Opis |
|---|---|---|
| Plik CA cert | `-CA` | Ścieżka do certyfikatu Root CA (`.crt`, `.pem`, `.cer`) |
| Plik CA klucza | `-CAkey` | Ścieżka do klucza prywatnego Root CA (`.key`, `.pem`) |
| Hasło klucza CA | `-passin pass:` | Hasło do klucza CA (maskowane, nigdy niezapisywane) |

#### Pliki wyjściowe

| Pole | Opis |
|---|---|
| Folder wyjściowy | Katalog, w którym zapisywane są wszystkie wygenerowane pliki; domyślnie `~\.polsoft\software\SignToolGUI\Certificates` |
| Nazwa bazowa plików | Prefiks wszystkich plików wyjściowych (np. `certyfikat` → `certyfikat.key`, `certyfikat.crt`, `certyfikat.pfx`) |
| Hasło do PFX | Hasło zabezpieczające eksportowany plik PFX (puste = brak hasła) |
| Eksportuj PFX | Uruchamia `openssl pkcs12 -export` — pakuje klucz + certyfikat do pliku `.pfx` |
| Zainstaluj w magazynie Windows | Importuje PFX do `Cert:\CurrentUser\My` przy użyciu PowerShell `Import-PfxCertificate` (admin wymagany dla magazynu komputera) |

#### Przyciski akcji

- **Generuj certyfikat** — Wykonuje sekwencyjnie wszystkie polecenia OpenSSL (lub skrypt PowerShell) w wątku tła z postępowym wyświetlaniem kroków
- **Pokaż komendy** — Wyświetla pełny zestaw poleceń OpenSSL lub skrypt PowerShell w panelu Wynik bez wykonywania; przydatne do podglądu lub ręcznego użycia

---

## Typy i metody podpisywania

### Protokoły znacznika czasu

| Protokół | Flaga | Standard | Kompatybilność | Uwagi |
|---|---|---|---|---|
| RFC 3161 | `/tr` + `/td` | IETF RFC 3161 | Windows Vista+ | **Zalecany.** Obsługuje znaczniki SHA-256, długoterminowa ważność |
| Authenticode | `/t` | Własny Microsoft | Windows XP+ | Tylko dla starszych systemów. Oparty na SHA1. Brak obsługi `/td` |

### Algorytmy hash dla podpisywania (`/fd`)

| Algorytm | Poziom bezpieczeństwa | Zalecany dla |
|---|---|---|
| SHA1 | Przestarzały | Tylko starsze systemy (Windows XP) |
| SHA256 | Aktualny standard | Wszystkie nowoczesne wersje Windows (**domyślny**) |
| SHA384 | Wysokie bezpieczeństwo | Aplikacje wymagające wysokiego bezpieczeństwa |
| SHA512 | Maksymalne | Wymagania maksymalnego bezpieczeństwa |

### Źródła certyfikatów

| Źródło | Jak wskazywane | Zastosowanie |
|---|---|---|
| Magazyn Windows — nazwa | `/n <NazwaPodmiotu>` | Certyfikat zapisany w lokalnym magazynie certyfikatów |
| Magazyn Windows — SHA1 | `/sha1 <odcisk>` | Precyzyjny wybór gdy wiele certyfikatów pasuje do nazwy |
| Plik PFX | `/f <ścieżka> /p <hasło>` | Certyfikat na dysku lub nośniku wymiennym |
| Dodatkowy certyfikat | `/ac <ścieżka>` | Cross-certyfikacja lub uzupełnienie łańcucha |

---

## Typy certyfikatów

| Typ | Rozszerzenia OpenSSL | Zastosowanie |
|---|---|---|
| Self-signed | `extendedKeyUsage=codeSigning`, `keyUsage=digitalSignature` | Programowanie, testowanie, podpisywanie wewnętrzne |
| Root CA | `basicConstraints=critical,CA:TRUE`, `keyUsage=critical,keyCertSign,cRLSign` | Budowa wewnętrznej hierarchii PKI |
| Podpisany przez CA | `extendedKeyUsage=codeSigning`, `keyUsage=digitalSignature`, opcjonalne SAN | Produkcyjne podpisywanie przez wewnętrzne CA |

---

## Parametry kryptograficzne

### Algorytmy klucza

| Algorytm | Rozmiary kluczy / krzywe | Uwagi |
|---|---|---|
| RSA | 2048, 3072, 4096 bitów | Powszechna kompatybilność; minimum 2048 bitów dla podpisywania kodu |
| EC (krzywa eliptyczna) | prime256v1, secp384r1, secp521r1 | Mniejsze klucze, równoważne lub lepsze bezpieczeństwo; nie wszędzie obsługiwany |

### Algorytmy hash

| Algorytm | Rozmiar wyjścia | Odpowiedni dla |
|---|---|---|
| sha256 | 256 bitów | Standard (**domyślny**) |
| sha384 | 384 bity | Aplikacje o podwyższonym bezpieczeństwie |
| sha512 | 512 bitów | Maksymalne wymagania bezpieczeństwa |

---

## Automatyczne wykrywanie narzędzi

Po uruchomieniu (200 ms po załadowaniu UI) aplikacja uruchamia skanowanie w tle w poszukiwaniu obu wymaganych narzędzi. Dialog wykrywania pokazuje:

- **signtool.exe** — przeszukiwane w: zapisana konfiguracja → folder aplikacji → `_MEIPASS` → systemowy `PATH` → ścieżki instalacji Windows SDK na wszystkich dyskach (`A:` do `Z:`)
- **openssl.exe** — przeszukiwane w: zapisana konfiguracja → folder aplikacji → `_MEIPASS` → systemowy `PATH` → typowe lokalizacje instalacji OpenSSL i dystrybucje Git

Wyniki wykrywania wyświetlane są ze wskaźnikami ✅ / ❌. Przycisk **Zastosuj i zamknij** zapisuje znalezione ścieżki i aktualizuje wskaźniki LED na pasku stanu. **Skanuj ponownie** uruchamia pełne skanowanie dysku ponownie.

### Wskaźniki LED na pasku stanu

Dwa kolorowe wskaźniki LED w prawym dolnym rogu informują o dostępności narzędzi:

- 🟢 **Zielony** — narzędzie znalezione i ścieżka zapisana
- 🔴 **Czerwony** — narzędzie nie znalezione

---

## Konfiguracja i trwałość ustawień

Wszystkie ustawienia przechowywane są w pliku `%USERPROFILE%\.polsoft\software\SignToolGUI\SignToolGUI.json`.

**Zapisywane przy zamknięciu:**

- Ścieżki narzędzi (`signtool_path`, `openssl_path`)
- Język UI (`"pl"` lub `"en"`)
- Wartości wszystkich pól formularzy (adresy URL serwerów, algorytmy hash, ścieżki certyfikatów, wpisy SAN, katalogi wyjściowe itd.)

**Nigdy niezapisywane (bezpieczeństwo):**

- `sign_cert_password` — hasło PFX do podpisywania
- `certgen_pfx_pass` — hasło do generowanego PFX
- `certgen_ca_key_pass` — hasło klucza CA

Certyfikaty generowane przez OpenSSL są domyślnie zapisywane w `%USERPROFILE%\.polsoft\software\SignToolGUI\Certificates\`.

---

## Dwujęzyczny interfejs PL/EN

Interfejs jest w pełni dwujęzyczny — wszystkie ciągi znaków zdefiniowane są w wewnętrznym słowniku tłumaczeń (`_TR`). Przełączenie języka następuje w czasie działania bez restartu:

1. Bieżący stan formularzy zostaje zapisany
2. Wszystkie zakładki zostają przebudowane w nowym języku
3. Stan formularzy zostaje przywrócony
4. Preferencja językowa zostaje zapisana do `SignToolGUI.json`

Przycisk przełączania języka (prawy dolny róg paska stanu) pokazuje język, **na który** zostanie przełączony (np. kliknięcie `EN` w trybie polskim przełącza na angielski).

Wszystkie dymki podpowiedzi są dynamicznie tłumaczone — zawsze odzwierciedlają bieżący język, nawet dla dymków na kontrolkach utworzonych przed przełączeniem.

---

## Struktura projektu

```
SignTools-ITS_v2.0_GUI/
│
├── main.py                    # Kod źródłowy aplikacji — 5 360 linii
├── SignTool.spec              # Specyfikacja budowania PyInstallera (one-file, windowed)
├── SignTool_GUI_v2.0_build.bat # Skrypt budowania (6-krokowy automatyczny build)
├── SignTool.manifest          # Manifest aplikacji Windows
│                              #   • Wymusza podsystem GUI Windows od bajtu 0
│                              #   • Obsługa DPI PerMonitorV2
│                              #   • Obsługa długich ścieżek (>260 znaków)
│                              #   • Kompatybilność: Windows 7 / 8 / 8.1 / 10 / 11
│                              #   • Poziom wykonania: asInvoker (bez monitu UAC)
├── version_info.txt           # Informacje o wersji PE (FileVersion 2.0.0.0)
├── hook_utf8.py               # Hook uruchamiany przez PyInstaller — wymusza kodowanie UTF-8
├── SignTool-ico.ico           # Ikona aplikacji (używana przez PyInstaller dla EXE)
├── Ikona SignTool's-ITS2.ico  # Źródłowy plik ikony
│
├── app/
│   └── SignTools-ITS v2.0 GUI.exe   # Gotowy przenośny plik EXE
│
└── doc/                       # Folder dokumentacji
```

---

## System budowania

Build jest sterowany przez `SignTool.spec` (plik spec PyInstallera) i `SignTool_GUI_v2.0_build.bat`:

| Ustawienie | Wartość |
|---|---|
| Tryb budowania | One-file (`onefile`) |
| Tryb okna | `windowed=True`, `console=False` |
| Ikona | `SignTool-ico.ico` (osadzona w EXE) |
| Runtime tmpdir | `None` (używa `%TEMP%` — eliminuje miganie konsoli) |
| Kompresja UPX | Wyłączona |
| Informacje o wersji | `version_info.txt` (metadane PE) |
| Manifest | `SignTool.manifest` (DPI + podsystem) |
| Hook uruchomieniowy | `hook_utf8.py` (kodowanie UTF-8) |
| Ukryte importy | `tkinter`, `tkinter.ttk`, `tkinter.filedialog`, `tkinter.messagebox`, `tkinter.scrolledtext`, `json`, `threading`, `subprocess`, `pathlib`, `tempfile`, `base64` |

Ikona aplikacji oraz logo PNG są osadzone jako ciągi Base64 wewnątrz `main.py` — plik EXE nie wymaga żadnych zewnętrznych plików zasobów podczas działania.

---

## Architektura i uwagi techniczne

- **Model wątkowania:** Każdy podproces `signtool`/`openssl`/`powershell` uruchamiany jest w wątku tła (`daemon=True`). Wynik jest strumieniowany linia po linii i przekazywany do głównego wątku przez `root.after(0, ...)`, aby uniknąć naruszeń wątkowania Tkinter.
- **Przycisk Stop:** Przechowuje referencję do `subprocess.Popen` w `self._current_process`; wywołuje `proc.kill()` na żądanie.
- **Brak migania konsoli:** `subprocess.Popen` jest monkey-patchowany na poziomie modułu w systemie Windows, aby zawsze dołączać `CREATE_NO_WINDOW` w `creationflags`.
- **Osadzanie ikony:** Ikona aplikacji jest dekodowana z Base64 w czasie działania, zapisywana do tymczasowego pliku `.ico`, ustawiana przez `root.iconbitmap()`, a następnie usuwana po 1 sekundzie.
- **Pliki tymczasowe SAN:** Przy generowaniu certyfikatów podpisanych przez CA pliki rozszerzeń OpenSSL są zapisywane do pliku tymczasowego w katalogu wyjściowym (Windows nie ma `/dev/stdin`). Plik jest usuwany po zakończeniu kroku podpisywania.
- **UTF-8 wszędzie:** `hook_utf8.py` rekonfiguruje `sys.stdout` i `sys.stderr`; `PYTHONIOENCODING=utf-8` jest ustawiany w środowisku; cały I/O plików używa `encoding='utf-8'`.
- **Bezpieczeństwo haseł:** Hasła PFX i klucza CA nigdy nie są zapisywane do pliku konfiguracji JSON, nawet podczas przełączania języka lub zamknięcia okna.

---

## Autor i kontakt

| Pole | Wartość |
|---|---|
| **Project Manager** | Sebastian Januchowski |
| **Firma** | polsoft.ITS™ Group |
| **E-mail** | polsoft.its@fastservice.com |
| **GitHub** | [github.com/seb07uk](https://github.com/seb07uk) |
| **Prawa autorskie** | 2026© polsoft.ITS™. Wszelkie prawa zastrzeżone. |

---

## Licencja

Niniejsze oprogramowanie jest **własnościowe**. Wszelkie prawa zastrzeżone przez polsoft.ITS™ Group.

Nieautoryzowane kopiowanie, modyfikowanie, dystrybucja lub użytkowanie niniejszego oprogramowania, w całości lub w części, bez wyraźnej pisemnej zgody polsoft.ITS™ Group jest surowo zabronione.

---

<div align="center">

*Stworzone z ❤️ przez polsoft.ITS™ Group — 2026©*

</div>
