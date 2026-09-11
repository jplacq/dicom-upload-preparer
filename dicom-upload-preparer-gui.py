#!/usr/bin/env python3

import os
import subprocess
import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText


APP_TITLE = "DICOM Upload Preparer"
DEFAULT_MAX_ZIP_MB = 430


class DicomUploadPreparerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("820x650")
        self.minsize(720, 560)

        self.source_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.anonymize_var = tk.BooleanVar(value=True)
        self.create_zip_var = tk.BooleanVar(value=True)
        self.max_zip_var = tk.StringVar(value=str(DEFAULT_MAX_ZIP_MB))
        self.status_var = tk.StringVar(value="Ready")

        self._process = None
        self._build_ui()
        self._update_controls()

    def _build_ui(self):
        root = ttk.Frame(self, padding=18)
        root.pack(fill="both", expand=True)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(8, weight=1)

        title = ttk.Label(root, text=APP_TITLE, font=("TkDefaultFont", 18, "bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 4))

        subtitle = ttk.Label(
            root,
            text="Prepare DICOM studies for review, transfer, or upload.",
        )
        subtitle.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 18))

        ttk.Label(root, text="DICOM source folder").grid(row=2, column=0, sticky="w", pady=6)
        source_entry = ttk.Entry(root, textvariable=self.source_var)
        source_entry.grid(row=2, column=1, sticky="ew", padx=(12, 8), pady=6)
        ttk.Button(root, text="Browse…", command=self._choose_source).grid(row=2, column=2, pady=6)

        ttk.Label(root, text="Output folder").grid(row=3, column=0, sticky="w", pady=6)
        output_entry = ttk.Entry(root, textvariable=self.output_var)
        output_entry.grid(row=3, column=1, sticky="ew", padx=(12, 8), pady=6)
        ttk.Button(root, text="Browse…", command=self._choose_output).grid(row=3, column=2, pady=6)

        options = ttk.LabelFrame(root, text="Options", padding=12)
        options.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(14, 10))
        options.columnconfigure(2, weight=1)

        ttk.Checkbutton(
            options,
            text="Anonymize DICOM files before writing them",
            variable=self.anonymize_var,
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        ttk.Checkbutton(
            options,
            text="Create ZIP archives",
            variable=self.create_zip_var,
            command=self._update_controls,
        ).grid(row=1, column=0, sticky="w")

        ttk.Label(options, text="Maximum ZIP size (MB)").grid(row=1, column=1, sticky="e", padx=(24, 8))
        self.max_zip_entry = ttk.Entry(options, textvariable=self.max_zip_var, width=8)
        self.max_zip_entry.grid(row=1, column=2, sticky="w")

        privacy = ttk.Label(
            root,
            text=(
                "Privacy: DICOM files can contain personal medical information. "
                "Anonymization is enabled by default in this graphical interface."
            ),
            wraplength=760,
        )
        privacy.grid(row=5, column=0, columnspan=3, sticky="w", pady=(0, 12))

        actions = ttk.Frame(root)
        actions.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        actions.columnconfigure(0, weight=1)

        self.prepare_button = ttk.Button(
            actions,
            text="Prepare DICOM files",
            command=self._start_processing,
        )
        self.prepare_button.grid(row=0, column=0, sticky="w")

        self.open_button = ttk.Button(
            actions,
            text="Open output folder",
            command=self._open_output,
            state="disabled",
        )
        self.open_button.grid(row=0, column=1, sticky="e")

        self.progress = ttk.Progressbar(root, mode="indeterminate")
        self.progress.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(0, 8))

        log_frame = ttk.LabelFrame(root, text="Processing log", padding=8)
        log_frame.grid(row=8, column=0, columnspan=3, sticky="nsew")
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

        self.log = ScrolledText(log_frame, height=16, wrap="word", state="disabled")
        self.log.grid(row=0, column=0, sticky="nsew")

        status = ttk.Label(root, textvariable=self.status_var, anchor="w")
        status.grid(row=9, column=0, columnspan=3, sticky="ew", pady=(8, 0))

    def _choose_source(self):
        folder = filedialog.askdirectory(title="Select the folder containing the DICOM study")
        if not folder:
            return

        source = Path(folder).expanduser().resolve()
        self.source_var.set(str(source))

        if not self.output_var.get().strip():
            self.output_var.set(str(source.parent / "dicom-prepared"))

    def _choose_output(self):
        folder = filedialog.askdirectory(title="Select the output folder")
        if folder:
            self.output_var.set(str(Path(folder).expanduser().resolve()))

    def _update_controls(self):
        self.max_zip_entry.configure(state="normal" if self.create_zip_var.get() else "disabled")

    def _append_log(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _validate(self):
        source_text = self.source_var.get().strip()
        output_text = self.output_var.get().strip()

        if not source_text:
            messagebox.showerror(APP_TITLE, "Select the folder containing the DICOM study.")
            return None

        source = Path(source_text).expanduser().resolve()
        if not source.is_dir():
            messagebox.showerror(APP_TITLE, "The selected DICOM source folder does not exist.")
            return None

        if not output_text:
            output = source.parent / "dicom-prepared"
            self.output_var.set(str(output))
        else:
            output = Path(output_text).expanduser().resolve()

        if output == source:
            messagebox.showerror(APP_TITLE, "The output folder cannot be the same as the source folder.")
            return None

        try:
            output.relative_to(source)
        except ValueError:
            pass
        else:
            messagebox.showerror(
                APP_TITLE,
                "Choose an output folder outside the DICOM source folder.\n\n"
                "This prevents generated files from being scanned again on a later run.",
            )
            return None

        try:
            max_zip = int(self.max_zip_var.get())
            if max_zip <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(APP_TITLE, "Maximum ZIP size must be a positive whole number.")
            return None

        return source, output, max_zip

    def _engine_path(self):
        candidates = [
            Path(__file__).resolve().parent / "prepare-dicom-upload",
            Path.cwd() / "prepare-dicom-upload",
        ]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        return None

    def _start_processing(self):
        validated = self._validate()
        if not validated:
            return

        engine = self._engine_path()
        if engine is None:
            messagebox.showerror(
                APP_TITLE,
                "Cannot find 'prepare-dicom-upload'.\n\n"
                "Keep dicom-upload-preparer-gui.py in the same folder as prepare-dicom-upload.",
            )
            return

        source, output, max_zip = validated

        command = [
            sys.executable,
            "-u",
            str(engine),
            str(source),
            "-o",
            str(output),
            "--max-zip-mb",
            str(max_zip),
        ]

        if self.anonymize_var.get():
            command.append("--anonymize")

        if not self.create_zip_var.get():
            command.append("--no-zip")

        self._clear_log()
        self._append_log("Starting DICOM preparation…\n\n")
        self.status_var.set("Processing…")
        self.prepare_button.configure(state="disabled")
        self.open_button.configure(state="disabled")
        self.progress.start(10)

        thread = threading.Thread(
            target=self._run_process,
            args=(command, output),
            daemon=True,
        )
        thread.start()

    def _run_process(self, command, output):
        try:
            creationflags = 0
            if os.name == "nt" and hasattr(subprocess, "CREATE_NO_WINDOW"):
                creationflags = subprocess.CREATE_NO_WINDOW

            self._process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                creationflags=creationflags,
            )

            assert self._process.stdout is not None
            for line in self._process.stdout:
                self.after(0, self._append_log, line)

            return_code = self._process.wait()
            self.after(0, self._processing_finished, return_code, output)

        except Exception as exc:
            self.after(0, self._processing_failed, str(exc))
        finally:
            self._process = None

    def _processing_finished(self, return_code, output):
        self.progress.stop()
        self.prepare_button.configure(state="normal")

        if return_code == 0:
            self.status_var.set("Finished successfully")
            if output.exists():
                self.open_button.configure(state="normal")
            self._append_log("\nFinished successfully.\n")
            messagebox.showinfo(
                APP_TITLE,
                "DICOM preparation finished successfully.\n\n"
                "Open README.txt in the output folder to see the prepared series.",
            )
        else:
            self.status_var.set(f"Failed (exit code {return_code})")
            self._append_log(f"\nProcessing failed with exit code {return_code}.\n")
            messagebox.showerror(
                APP_TITLE,
                "DICOM preparation failed.\n\nCheck the processing log for details.",
            )

    def _processing_failed(self, error):
        self.progress.stop()
        self.prepare_button.configure(state="normal")
        self.status_var.set("Failed")
        self._append_log(f"\nError: {error}\n")
        messagebox.showerror(APP_TITLE, f"Unable to start DICOM preparation.\n\n{error}")

    def _open_output(self):
        output_text = self.output_var.get().strip()
        if not output_text:
            return

        output = Path(output_text).expanduser().resolve()
        if not output.exists():
            messagebox.showerror(APP_TITLE, "The output folder does not exist yet.")
            return

        try:
            if sys.platform == "win32":
                os.startfile(output)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(output)])
            else:
                subprocess.Popen(["xdg-open", str(output)])
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"Unable to open the output folder.\n\n{exc}")


def main():
    app = DicomUploadPreparerGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
