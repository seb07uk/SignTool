#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
polsoft.ITS™ SignTool GUI
Autor: Seb / polsoft.ITS™

Standalone GUI wrapper dla Microsoft signtool.exe:
- wybór polecenia (sign, verify, timestamp, catdb, remove)
- dynamiczne opcje dla każdego polecenia (checkbox + pola tekstowe)
- wybór ścieżki do signtool.exe, certyfikatu, plików do podpisu/werifikacji
- podgląd wygenerowanej linii komend
- uruchamianie signtool i wyświetlanie stdout/stderr
"""

import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

# ---------------------- KONFIGURACJA OPCJI ----------------------

# Każda opcja: klucz = przełącznik, value = dict:
#   "label": opis w GUI
#   "has_value": czy wymaga wartości (np. /f <plik>)
#   "value_hint": podpowiedź dla pola tekstowego
#   "file_dialog": "file" / "dir" / None (jeśli ma otwierać dialog)
#   "multi": czy można podać wiele wartości (np. wiele plików)
SIGNTOOL_COMMANDS = {
    "sign": {
        "label": "sign – podpisywanie plików",
        "options": {
            "/a":  {"label": "Automatyczny wybór najlepszego certyfikatu", "has_value": False},
            "/ac": {"label": "Additional certificate", "has_value": True, "value_hint": "Ścieżka do dodatkowego certyfikatu", "file_dialog": "file"},
            "/as": {"label": "Dodaj podpis (nie zastępuj istniejącego)", "has_value": False},
            "/c":  {"label": "URL certyfikatu wydawcy", "has_value": True, "value_hint": "URL certyfikatu wydawcy"},
            "/d":  {"label": "Opis pliku", "has_value": True, "value_hint": "Opis"},
            "/du": {"label": "URL opisu", "has_value": True, "value_hint": "URL opisu"},
            "/f":  {"label": "Plik PFX z certyfikatem", "has_value": True, "value_hint": "Ścieżka do .pfx", "file_dialog": "file"},
            "/p":  {"label": "Hasło do PFX", "has_value": True, "value_hint": "Hasło"},
            "/n":  {"label": "Nazwa podmiotu (subject)", "has_value": True, "value_hint": "CN=..."},
            "/r":  {"label": "Issuer (wystawca)", "has_value": True, "value_hint": "CN=..."},
            "/s":  {"label": "Store name", "has_value": True, "value_hint": "np. My"},
            "/sha1": {"label": "SHA1 thumbprint certyfikatu", "has_value": True, "value_hint": "Thumbprint"},
            "/sm": {"label": "Store w maszynie (LocalMachine)", "has_value": False},
            "/fd": {"label": "File digest algorithm", "has_value": True, "value_hint": "np. sha256"},
            "/td": {"label": "Timestamp digest algorithm", "has_value": True, "value_hint": "np. sha256"},
            "/t":  {"label": "URL serwera timestamp (stary /t)", "has_value": True, "value_hint": "http://..."},
            "/tr": {"label": "RFC3161 timestamp server URL", "has_value": True, "value_hint": "http://..."},
            "/u":  {"label": "OID użycia certyfikatu", "has_value": True, "value_hint": "OID"},
            "/uw": {"label": "Użyj certyfikatu do podpisu Windows", "has_value": False},
            "/v":  {"label": "Verbose", "has_value": False},
            "/debug": {"label": "Debug output", "has_value": False},
            "/ph": {"label": "Podpisz hash (nie plik)", "has_value": False},
        },
    },
    "verify": {
        "label": "verify – weryfikacja podpisu",
        "options": {
            "/a":  {"label": "Użyj wszystkich certyfikatów", "has_value": False},
            "/ad": {"label": "Weryfikuj wszystkie podpisy w pliku", "has_value": False},
            "/all": {"label": "Weryfikuj wszystkie podpisy", "has_value": False},
            "/agile": {"label": "Weryfikuj podpisy agile", "has_value": False},
            "/pa": {"label": "Policy: Authenticode", "has_value": False},
            "/kp": {"label": "Key protection (kernel-mode)", "has_value": False},
            "/tw": {"label": "Sprawdź timestamp", "has_value": False},
            "/v":  {"label": "Verbose", "has_value": False},
            "/debug": {"label": "Debug output", "has_value": False},
        },
    },
    "timestamp": {
        "label": "timestamp – dodawanie znacznika czasu",
        "options": {
            "/t":  {"label": "URL serwera timestamp (stary /t)", "has_value": True, "value_hint": "http://..."},
            "/tr": {"label": "RFC3161 timestamp server URL", "has_value": True, "value_hint": "http://..."},
            "/td": {"label": "Timestamp digest algorithm", "has_value": True, "value_hint": "np. sha256"},
            "/v":  {"label": "Verbose", "has_value": False},
            "/debug": {"label": "Debug output", "has_value": False},
        },
    },
    "catdb": {
        "label": "catdb – zarządzanie katalogami (catalog database)",
        "options": {
            "/g": {"label": "Global catalog database", "has_value": False},
            "/r": {"label": "Remove katalog", "has_value": False},
            "/d": {"label": "Nazwa katalogu", "has_value": True, "value_hint": "Nazwa katalogu"},
            "/u": {"label": "Uninstall katalog", "has_value": False},
            "/v": {"label": "Verbose", "has_value": False},
            "/debug": {"label": "Debug output", "has_value": False},
        },
    },
    "remove": {
        "label": "remove – usuwanie podpisu",
        "options": {
            "/s": {"label": "Store name", "has_value": True, "value_hint": "np. My"},
            "/sha1": {"label": "SHA1 thumbprint certyfikatu", "has_value": True, "value_hint": "Thumbprint"},
            "/v": {"label": "Verbose", "has_value": False},
            "/debug": {"label": "Debug output", "has_value": False},
        },
    },
}

# ---------------------- GŁÓWNA KLASA GUI ----------------------

class SignToolGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("polsoft.ITS™ SignTool GUI")
        self.geometry("1000x700")
        self.minsize(900, 600)

        self.signtool_path_var = tk.StringVar()
        self.command_var = tk.StringVar(value="sign")
        self.files_var = tk.StringVar()
        self.extra_args_var = tk.StringVar()

        # dla dynamicznych opcji
        self.option_vars = {}   # switch -> tk.BooleanVar
        self.option_values = {} # switch -> tk.StringVar

        self._build_ui()
        self._refresh_options()

    # ---------------------- BUDOWA UI ----------------------

    def _build_ui(self):
        # Górny frame – ścieżka do signtool
        top = ttk.LabelFrame(self, text="Ścieżka do signtool.exe")
        top.pack(fill="x", padx=8, pady=4)

        entry = ttk.Entry(top, textvariable=self.signtool_path_var)
        entry.pack(side="left", fill="x", expand=True, padx=4, pady=4)

        btn_browse_signtool = ttk.Button(top, text="Wybierz...", command=self.browse_signtool)
        btn_browse_signtool.pack(side="left", padx=4, pady=4)

        # Środkowy frame – wybór komendy i plików
        mid = ttk.Frame(self)
        mid.pack(fill="x", padx=8, pady=4)

        # Komenda
        cmd_frame = ttk.LabelFrame(mid, text="Polecenie SignTool")
        cmd_frame.pack(side="left", fill="y", padx=4, pady=4)

        for cmd_key, cmd_info in SIGNTOOL_COMMANDS.items():
            rb = ttk.Radiobutton(
                cmd_frame,
                text=cmd_info["label"],
                value=cmd_key,
                variable=self.command_var,
                command=self._refresh_options
            )
            rb.pack(anchor="w", padx=4, pady=2)

        # Pliki
        files_frame = ttk.LabelFrame(mid, text="Pliki / katalogi docelowe")
        files_frame.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        files_entry = ttk.Entry(files_frame, textvariable=self.files_var)
        files_entry.pack(fill="x", padx=4, pady=4)

        btn_files = ttk.Button(files_frame, text="Dodaj pliki...", command=self.browse_files)
        btn_files.pack(side="left", padx=4, pady=4)

        btn_clear_files = ttk.Button(files_frame, text="Wyczyść", command=lambda: self.files_var.set(""))
        btn_clear_files.pack(side="left", padx=4, pady=4)

        # Dynamiczne opcje
        self.options_frame = ttk.LabelFrame(self, text="Opcje dla wybranego polecenia")
        self.options_frame.pack(fill="both", expand=False, padx=8, pady=4)

        # Extra args
        extra_frame = ttk.LabelFrame(self, text="Dodatkowe argumenty (ręcznie)")
        extra_frame.pack(fill="x", padx=8, pady=4)

        extra_entry = ttk.Entry(extra_frame, textvariable=self.extra_args_var)
        extra_entry.pack(fill="x", padx=4, pady=4)

        # Podgląd komendy + przycisk RUN
        cmd_preview_frame = ttk.Frame(self)
        cmd_preview_frame.pack(fill="x", padx=8, pady=4)

        self.cmd_preview_text = tk.StringVar()
        lbl_preview = ttk.Label(cmd_preview_frame, textvariable=self.cmd_preview_text, foreground="#00aa00", wraplength=900, justify="left")
        lbl_preview.pack(side="left", fill="x", expand=True, padx=4, pady=4)

        btn_run = ttk.Button(cmd_preview_frame, text="Uruchom signtool", command=self.run_signtool)
        btn_run.pack(side="right", padx=4, pady=4)

        # Output
        output_frame = ttk.LabelFrame(self, text="Wyjście signtool (stdout/stderr)")
        output_frame.pack(fill="both", expand=True, padx=8, pady=4)

        self.output_text = ScrolledText(output_frame, wrap="word")
        self.output_text.pack(fill="both", expand=True, padx=4, pady=4)

    # ---------------------- OBSŁUGA ŚCIEŻEK ----------------------

    def browse_signtool(self):
        path = filedialog.askopenfilename(
            title="Wybierz signtool.exe",
            filetypes=[("signtool.exe", "signtool.exe"), ("Wszystkie pliki", "*.*")]
        )
        if path:
            self.signtool_path_var.set(path)
            self._update_command_preview()

    def browse_files(self):
        files = filedialog.askopenfilenames(
            title="Wybierz pliki do podpisu/weryfikacji",
            filetypes=[("Wszystkie pliki", "*.*")]
        )
        if files:
            current = self.files_var.get().strip()
            new_list = list(filter(None, current.split(";"))) if current else []
            new_list.extend(files)
            self.files_var.set(";".join(new_list))
            self._update_command_preview()

    def browse_for_option_file(self, switch):
        path = filedialog.askopenfilename(
            title=f"Wybierz plik dla opcji {switch}",
            filetypes=[("Wszystkie pliki", "*.*")]
        )
        if path:
            self.option_values[switch].set(path)
            self._update_command_preview()

    # ---------------------- OPCJE DYNAMICZNE ----------------------

    def _clear_options_frame(self):
        for child in self.options_frame.winfo_children():
            child.destroy()
        self.option_vars.clear()
        self.option_values.clear()

    def _refresh_options(self):
        self._clear_options_frame()
        cmd_key = self.command_var.get()
        cmd_info = SIGNTOOL_COMMANDS.get(cmd_key, {})
        options = cmd_info.get("options", {})

        # siatka opcji
        row = 0
        for switch, opt in sorted(options.items()):
            var = tk.BooleanVar(value=False)
            self.option_vars[switch] = var

            chk = ttk.Checkbutton(
                self.options_frame,
                text=f"{switch} – {opt.get('label', '')}",
                variable=var,
                command=self._update_command_preview
            )
            chk.grid(row=row, column=0, sticky="w", padx=4, pady=2)

            if opt.get("has_value"):
                val_var = tk.StringVar()
                self.option_values[switch] = val_var
                entry = ttk.Entry(self.options_frame, textvariable=val_var, width=40)
                entry.grid(row=row, column=1, sticky="w", padx=4, pady=2)

                hint = opt.get("value_hint")
                if hint:
                    entry.insert(0, "")

                # przycisk "..." dla plików
                if opt.get("file_dialog") == "file":
                    btn = ttk.Button(
                        self.options_frame,
                        text="...",
                        width=3,
                        command=lambda s=switch: self.browse_for_option_file(s)
                    )
                    btn.grid(row=row, column=2, sticky="w", padx=2, pady=2)

                # aktualizacja podglądu przy zmianie
                entry.bind("<KeyRelease>", lambda e, s=switch: self._update_command_preview())
            row += 1

        self._update_command_preview()

    # ---------------------- BUDOWANIE KOMENDY ----------------------

    def build_command(self):
        signtool = self.signtool_path_var.get().strip() or "signtool.exe"
        cmd_key = self.command_var.get()

        cmd = [signtool, cmd_key]

        # opcje
        cmd_info = SIGNTOOL_COMMANDS.get(cmd_key, {})
        options = cmd_info.get("options", {})

        for switch, opt in options.items():
            if not self.option_vars.get(switch):
                continue
            if not self.option_vars[switch].get():
                continue

            cmd.append(switch)
            if opt.get("has_value"):
                val = self.option_values.get(switch, tk.StringVar()).get().strip()
                if val:
                    cmd.append(val)

        # dodatkowe argumenty
        extra = self.extra_args_var.get().strip()
        if extra:
            # proste split – jeśli chcesz bardziej zaawansowane parsowanie, można dodać shlex.split
            cmd.extend(extra.split())

        # pliki
        files_str = self.files_var.get().strip()
        if files_str:
            for f in files_str.split(";"):
                f = f.strip()
                if f:
                    cmd.append(f)

        return cmd

    def _update_command_preview(self):
        cmd = self.build_command()
        # ładny preview
        preview = " ".join(f'"{c}"' if " " in c and not c.startswith("/") else c for c in cmd)
        self.cmd_preview_text.set(preview)

    # ---------------------- URUCHAMIANIE SIGNTOOL ----------------------

    def run_signtool(self):
        cmd = self.build_command()
        self.output_text.delete("1.0", "end")

        if not cmd:
            messagebox.showerror("Błąd", "Brak komendy do uruchomienia.")
            return

        # prosta walidacja signtool
        signtool = cmd[0]
        if not shutil_which(signtool):
            # jeśli podano pełną ścieżkę, sprawdź istnienie
            if not os.path.isfile(signtool):
                messagebox.showerror("Błąd", f"Nie znaleziono signtool: {signtool}")
                return

        self.output_text.insert("end", f"Uruchamiam:\n{' '.join(cmd)}\n\n")
        self.output_text.see("end")
        self.update_idletasks()

        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
        except Exception as e:
            self.output_text.insert("end", f"Błąd uruchamiania signtool:\n{e}\n")
            self.output_text.see("end")
            return

        if proc.stdout:
            self.output_text.insert("end", "=== STDOUT ===\n")
            self.output_text.insert("end", proc.stdout + "\n")
        if proc.stderr:
            self.output_text.insert("end", "=== STDERR ===\n")
            self.output_text.insert("end", proc.stderr + "\n")

        self.output_text.see("end")


# ---------------------- POMOCNICZE ----------------------

def shutil_which(cmd):
    """Prosty odpowiednik shutil.which, żeby nie importować całego modułu."""
    # jeśli jest ścieżka bezpośrednia
    if os.path.isabs(cmd) or os.path.dirname(cmd):
        return cmd if os.path.exists(cmd) else None

    path = os.environ.get("PATH", "")
    exts = os.environ.get("PATHEXT", ".EXE;.BAT;.CMD").split(";")
    for p in path.split(os.pathsep):
        full = os.path.join(p, cmd)
        if os.path.isfile(full):
            return full
        for ext in exts:
            full_ext = full + ext
            if os.path.isfile(full_ext):
                return full_ext
    return None


# ---------------------- MAIN ----------------------

if __name__ == "__main__":
    app = SignToolGUI()
    app.mainloop()