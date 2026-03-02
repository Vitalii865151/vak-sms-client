# gui_sms.py
import tkinter as tk
from tkinter import ttk
import threading
import sms3


class VakSmsGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("VAK SMS Automation")
        self.root.geometry("800x420")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # ===== INPUT SECTION =====
        input_frame = ttk.LabelFrame(main_frame, text="Параметры", padding=15)
        input_frame.pack(fill="x", pady=10)

        ttk.Label(input_frame, text="API Key:").grid(row=0, column=0, sticky="w")
        self.api_entry = ttk.Entry(input_frame, width=65)
        self.api_entry.insert(0, "")   # значение по умолчанию
        self.api_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Service:").grid(row=1, column=0, sticky="w")
        self.service_entry = ttk.Entry(input_frame, width=65)
        self.service_entry.insert(0, "")  # пример
        self.service_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Country:").grid(row=2, column=0, sticky="w")
        self.country_entry = ttk.Entry(input_frame, width=65)
        self.country_entry.insert(0, "")
        self.country_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Operator:").grid(row=3, column=0, sticky="w")
        self.operator_entry = ttk.Entry(input_frame, width=65)
        self.operator_entry.insert(0, "")
        self.operator_entry.grid(row=3, column=1, padx=10, pady=5)

        # ===== BUTTON =====
        self.start_button = ttk.Button(
            main_frame,
            text="Получить и ждать",
            command=self.start_process
        )
        self.start_button.pack(pady=15)

        # ===== OUTPUT =====
        output_frame = ttk.LabelFrame(main_frame, text="Результат", padding=15)
        output_frame.pack(fill="both", expand=True)

        self.phone_label = tk.Label(
            output_frame,
            text="Телефон: ---",
            font=("Arial", 14),
            fg="blue",
            cursor="hand2"
        )
        self.phone_label.pack(pady=10)
        self.phone_label.bind("<Button-1>", self.copy_phone)

        self.sms_label = tk.Label(
            output_frame,
            text="SMS Code: ---",
            font=("Arial", 14),
            fg="green",
            cursor="hand2"
        )
        self.sms_label.pack(pady=10)
        self.sms_label.bind("<Button-1>", self.copy_sms)

        self.status_label = tk.Label(output_frame, text="", font=("Arial", 10))
        self.status_label.pack(pady=10)

    # ===== ОСНОВНОЙ ПРОЦЕСС =====

    def start_process(self):

        self.start_button.config(state="disabled")
        self.status_label.config(text="Начинаем процесс...")

        # Передаём данные в sms3
        sms3.apiKey = self.api_entry.get().strip()
        sms3.service = self.service_entry.get().strip()
        sms3.country = self.country_entry.get().strip()
        sms3.operator = self.operator_entry.get().strip()

        def task():

            success = sms3.send_get_request()

            if not success:
                self.status_label.config(text="Ошибка получения номера.")
                self.start_button.config(state="normal")
                return

            self.phone_label.config(text=f"Телефон: {sms3.tel}")
            self.status_label.config(text="Номер получен. Ожидаем SMS...")

            code = sms3.send_get_request2()

            if code:
                self.sms_label.config(text=f"SMS Code: {code}")
                self.status_label.config(text="Код получен.")
            else:
                self.status_label.config(text="Код не получен.")

            self.start_button.config(state="normal")

        threading.Thread(target=task).start()

    # ===== COPY =====

    def copy_phone(self, event):
        if sms3.tel:
            self.root.clipboard_clear()
            self.root.clipboard_append(sms3.tel)
            self.status_label.config(text="Телефон скопирован!")

    def copy_sms(self, event):
        if sms3.smsCode:
            self.root.clipboard_clear()
            self.root.clipboard_append(sms3.smsCode)
            self.status_label.config(text="Код скопирован!")


if __name__ == "__main__":
    root = tk.Tk()
    app = VakSmsGUI(root)
    root.mainloop()