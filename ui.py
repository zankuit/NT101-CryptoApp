import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ast
import random
import string
import math
from datetime import datetime

from algorithms.playfair import encrypt as pf_encrypt, decrypt as pf_decrypt, generate_matrix as pf_generate_matrix
from algorithms.rsa import generate_keys, encrypt as rsa_encrypt, decrypt as rsa_decrypt, is_prime


class CryptoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Crypto App")
        self.root.geometry("800x600")

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        self.playfair_tab = ttk.Frame(notebook)
        self.rsa_tab = ttk.Frame(notebook)
        self.aboutUs_tab = ttk.Frame(notebook)

        notebook.add(self.playfair_tab, text="Playfair")
        notebook.add(self.rsa_tab, text="RSA")
        notebook.add(self.aboutUs_tab, text="Giới thiệu")

        self.build_playfair()
        self.build_rsa()
        self.build_about_us()
        self.pf_last_result = None
        self.rsa_last_result = None

    def show_help(self, title, content):
        messagebox.showinfo(f"Hướng dẫn: {title}", content)

    def copy_entry_value(self, entry, label):
        value = entry.get().strip()
        if not value:
            messagebox.showwarning("Copy", f"Ô {label} đang trống")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.root.update()
        messagebox.showinfo("Copy", f"Đã copy {label} vào clipboard")

    def add_input_row(self, parent, label, help_text, width=45, with_copy=False):
        row = tk.Frame(parent)
        row.pack(fill="x", pady=4)

        tk.Label(row, text=label, width=28, anchor="w").pack(side="left")
        entry = tk.Entry(row, width=width)
        entry.pack(side="left", padx=(0, 6), fill="x", expand=True)
        tk.Button(
            row,
            text="?",
            width=3,
            command=lambda: self.show_help(label, help_text),
        ).pack(side="left")
        if with_copy:
            tk.Button(
                row,
                text="Sao chép",
                command=lambda: self.copy_entry_value(entry, label),
            ).pack(side="left", padx=(6, 0))

        return entry

    def set_entry_state(self, entry, enabled):
        entry.configure(state=tk.NORMAL if enabled else tk.DISABLED)

    def set_entry_value(self, entry, value):
        old_state = str(entry.cget("state"))
        entry.configure(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.insert(0, value)
        if old_state == tk.DISABLED:
            entry.configure(state=tk.DISABLED)

    def set_result_display(self, entry, label_var, value):
        self.set_entry_value(entry, value)
        label_var.set(value if value else "(chưa có kết quả)")

    def add_field_action_row(self, parent, actions):
        row = tk.Frame(parent)
        row.pack(fill="x", pady=(0, 6))
        tk.Label(row, text="", width=28, anchor="w").pack(side="left")
        for text, command in actions:
            tk.Button(row, text=text, command=command).pack(side="left", padx=(0, 8))
        return row

    def read_text_file_to_entry(self, entry, label):
        path = filedialog.askopenfilename(
            title=f"Chọn file cho {label}",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            self.set_entry_value(entry, content)
            messagebox.showinfo("Đọc file", f"Đã nạp dữ liệu cho {label}")
        except Exception as ex:
            messagebox.showerror("Lỗi đọc file", str(ex))

    def save_entry_to_text_file(self, entry, label, default_name):
        value = entry.get().strip()
        if not value:
            messagebox.showwarning("Ghi file", f"Ô {label} đang trống")
            return

        path = filedialog.asksaveasfilename(
            title=f"Lưu {label}",
            initialfile=default_name,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(value)
            messagebox.showinfo("Ghi file", f"Đã lưu {label} thành công")
        except Exception as ex:
            messagebox.showerror("Lỗi ghi file", str(ex))

    def save_text_report(self, content, default_name):
        path = filedialog.asksaveasfilename(
            title="Xuất báo cáo kết quả",
            initialfile=default_name,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Xuất báo cáo", "Đã xuất báo cáo kết quả")
        except Exception as ex:
            messagebox.showerror("Lỗi Xuất báo cáo", str(ex))

    def random_alpha_text(self, min_len=6, max_len=12):
        length = random.randint(min_len, max_len)
        return "".join(random.choice(string.ascii_uppercase) for _ in range(length))

    def random_prime(self, min_value=17, max_value=97):
        candidates = [n for n in range(min_value, max_value + 1) if is_prime(n)]
        return random.choice(candidates)

    def random_rsa_params(self):
        p = self.random_prime()
        q = self.random_prime()
        while q == p:
            q = self.random_prime()

        phi = (p - 1) * (q - 1)
        e_candidates = [n for n in range(3, phi) if math.gcd(n, phi) == 1]
        e = random.choice(e_candidates)
        return p, q, e

    # ================= PLAYFAIR =================
    def build_playfair(self):
        container = tk.Frame(self.playfair_tab, padx=12, pady=10)
        container.pack(fill="both", expand=True)

        desc = (
            "Playfair là thuật toán mã hóa thay thế theo cặp ký tự (digraph). "
            "Khóa được đưa vào ma trận 5x5 (I/J gộp chung), và mỗi cặp ký tự "
            "được biến đổi theo quy tắc cùng hàng, cùng cột, hoặc hình chữ nhật."
        )
        tk.Label(container, text=desc, justify="left", wraplength=760).pack(anchor="w", pady=(0, 10))

        self.pf_input = self.add_input_row(
            container,
            "Plaintext / Ciphertext",
            "Nhập chuỗi chỉ gồm chữ cái A-Z. Hệ thống sẽ tự động chuyển về IN HOA và J -> I.",
        )
        self.add_field_action_row(
            container,
            [
                (
                    "Đọc từ file",
                    lambda: self.read_text_file_to_entry(self.pf_input, "Plaintext / Ciphertext"),
                ),
                (
                    "Lưu ra file",
                    lambda: self.save_entry_to_text_file(
                        self.pf_input,
                        "Plaintext / Ciphertext",
                        "playfair_input.txt",
                    ),
                ),
            ],
        )
        self.pf_key = self.add_input_row(
            container,
            "Khóa",
            "Nhập khóa Playfair chỉ gồm chữ cái. Ký tự trùng sẽ được loại bỏ khi tạo ma trận.",
            width=30,
        )

        button_row = tk.Frame(container)
        button_row.pack(fill="x", pady=6)
        tk.Button(button_row, text="Mã hóa", command=self.handle_pf_encrypt).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Giải mã", command=self.handle_pf_decrypt).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Ngẫu nhiên", command=self.random_pf_data).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Xóa", command=self.clear_pf_data).pack(side="left")

        self.pf_output = self.add_input_row(
            container,
            "Kết quả",
            "Kết quả mã hóa hoặc giải mã.",
            with_copy=True,
        )
        self.set_entry_state(self.pf_output, False)
        self.add_field_action_row(
            container,
            [
                (
                    "Lưu Result ra file",
                    lambda: self.save_entry_to_text_file(self.pf_output, "Kết quả", "playfair_result.txt"),
                ),
                ("Xuất báo cáo", self.export_playfair_result),
            ],
        )
        self.pf_result_var = tk.StringVar(value="(chưa có kết quả)")
        tk.Label(
            container,
            textvariable=self.pf_result_var,
            justify="left",
            anchor="w",
            wraplength=760,
            fg="#1f2937",
        ).pack(fill="x", pady=(2, 8))

        tk.Label(container, text="Bảng khóa (Keysquare) 5x5").pack(pady=(10, 4))
        self.pf_keysquare_frame = tk.Frame(container, bd=1, relief=tk.GROOVE, padx=6, pady=6)
        self.pf_keysquare_frame.pack(pady=(0, 4))
        self.pf_keysquare_cells = []
        for r in range(5):
            row_cells = []
            for c in range(5):
                cell = tk.Label(
                    self.pf_keysquare_frame,
                    text="",
                    width=3,
                    height=1,
                    font=("Courier", 12, "bold"),
                    relief=tk.RIDGE,
                    bd=1,
                    anchor="center",
                )
                cell.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                row_cells.append(cell)
            self.pf_keysquare_cells.append(row_cells)

        for i in range(5):
            self.pf_keysquare_frame.grid_columnconfigure(i, weight=1)

    def validate_pf(self, text, key):
        if not text or not key:
            messagebox.showerror("Error", "Không được để trống")
            return False
        if not text.isalpha() or not key.isalpha():
            messagebox.showerror("Error", "Chỉ nhập chữ cái")
            return False
        return True

    def render_pf_keysquare(self, key):
        matrix = pf_generate_matrix(key)
        for r in range(5):
            for c in range(5):
                self.pf_keysquare_cells[r][c].configure(text=matrix[r][c])

    def clear_pf_data(self):
        self.pf_input.delete(0, tk.END)
        self.pf_key.delete(0, tk.END)
        self.set_result_display(self.pf_output, self.pf_result_var, "")
        self.pf_last_result = None
        for row in self.pf_keysquare_cells:
            for cell in row:
                cell.configure(text="")

    def random_pf_data(self):
        self.set_entry_value(self.pf_input, self.random_alpha_text())
        self.set_entry_value(self.pf_key, self.random_alpha_text(5, 9))
        self.set_result_display(self.pf_output, self.pf_result_var, "")
        self.pf_last_result = None
        for row in self.pf_keysquare_cells:
            for cell in row:
                cell.configure(text="")

    def handle_pf_encrypt(self):
        text = self.pf_input.get()
        key = self.pf_key.get()

        if not self.validate_pf(text, key):
            return

        try:
            result = pf_encrypt(text, key)
            self.set_result_display(self.pf_output, self.pf_result_var, result)
            self.render_pf_keysquare(key)
            self.pf_last_result = {
                "mode": "Encrypt",
                "plaintext": text,
                "ciphertext": result,
                "keyword": key,
            }
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def handle_pf_decrypt(self):
        text = self.pf_input.get()
        key = self.pf_key.get()

        if not self.validate_pf(text, key):
            return

        try:
            result = pf_decrypt(text, key)
            self.set_result_display(self.pf_output, self.pf_result_var, result)
            self.render_pf_keysquare(key)
            self.pf_last_result = {
                "mode": "Decrypt",
                "plaintext": result,
                "ciphertext": text,
                "keyword": key,
            }
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def export_playfair_result(self):
        if not self.pf_last_result:
            messagebox.showwarning("Xuất", "Chưa có kết quả Playfair để xuất")
            return

        matrix = pf_generate_matrix(self.pf_last_result["keyword"])
        matrix_text = "\n".join(" ".join(row) for row in matrix)
        exported_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        content = (
            "=== PLAYFAIR EXPORT ===\n"
            f"Thời gian xuất: {exported_at}\n"
            f"Chế độ: {self.pf_last_result['mode']}\n"
            f"Keyword: {self.pf_last_result['keyword']}\n"
            f"Plaintext: {self.pf_last_result['plaintext']}\n"
            f"Ciphertext: {self.pf_last_result['ciphertext']}\n"
            "\nKeysquare (5x5):\n"
            f"{matrix_text}\n"
        )
        self.save_text_report(content, "playfair_export.txt")

    # ================= RSA =================
    def build_rsa(self):
        container = tk.Frame(self.rsa_tab, padx=12, pady=10)
        container.pack(fill="both", expand=True)

        desc = (
            "RSA là thuật toán mã hóa bất đối xứng. Encrypt dùng public key (e, n), "
            "Decrypt dùng private key (d, n). Đây là bản minh họa học tập, không sử dụng "
            "padding bảo mật như OAEP."
        )
        tk.Label(container, text=desc, justify="left", wraplength=760).pack(anchor="w", pady=(0, 10))

        self.rsa_mode = tk.StringVar(value="encrypt")
        mode_row = tk.Frame(container)
        mode_row.pack(fill="x", pady=(0, 8))
        tk.Label(mode_row, text="Chế độ", width=28, anchor="w").pack(side="left")
        tk.Radiobutton(
            mode_row,
            text="Mã hóa",
            variable=self.rsa_mode,
            value="encrypt",
            command=self.update_rsa_mode,
        ).pack(side="left", padx=(0, 10))
        tk.Radiobutton(
            mode_row,
            text="Giải mã",
            variable=self.rsa_mode,
            value="decrypt",
            command=self.update_rsa_mode,
        ).pack(side="left")

        self.rsa_p = self.add_input_row(
            container,
            "p",
            "Nhập số nguyên tố p. Nên chọn số lớn hơn để tránh n quá nhỏ.",
            width=20,
        )
        self.rsa_q = self.add_input_row(
            container,
            "q",
            "Nhập số nguyên tố q, khác p.",
            width=20,
        )
        self.rsa_e = self.add_input_row(
            container,
            "e",
            "Nhập e sao cho 1 < e < phi và gcd(e, phi) = 1.",
            width=20,
        )
        self.rsa_plain_input = self.add_input_row(
            container,
            "Plaintext",
            "Nhập chuỗi bản rõ để mã hóa.",
            with_copy=True,
        )
        self.add_field_action_row(
            container,
            [
                (
                    "Đọc Plaintext từ file",
                    lambda: self.read_text_file_to_entry(self.rsa_plain_input, "Plaintext"),
                ),
                (
                    "Lưu Plaintext ra file",
                    lambda: self.save_entry_to_text_file(self.rsa_plain_input, "Plaintext", "rsa_plaintext.txt"),
                ),
            ],
        )
        self.rsa_cipher_input = self.add_input_row(
            container,
            "Ciphertext",
            "Nhập danh sách số nguyên, ví dụ: [2790, 102, 88]",
            with_copy=True,
        )
        self.add_field_action_row(
            container,
            [
                (
                    "Đọc Ciphertext từ file",
                    lambda: self.read_text_file_to_entry(self.rsa_cipher_input, "Ciphertext"),
                ),
                (
                    "Lưu Ciphertext ra file",
                    lambda: self.save_entry_to_text_file(self.rsa_cipher_input, "Ciphertext", "rsa_ciphertext.txt"),
                ),
            ],
        )
        self.rsa_d = self.add_input_row(
            container,
            "Khóa bí mật d",
            "Nhập giá trị d của private key.",
            width=20,
        )
        self.rsa_n = self.add_input_row(
            container,
            "Khóa bí mật n",
            "Nhập giá trị n của private key.",
            width=20,
        )

        button_row = tk.Frame(container)
        button_row.pack(fill="x", pady=6)
        self.rsa_action_button = tk.Button(button_row, text="Mã hóa", command=self.handle_rsa_action)
        self.rsa_action_button.pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Ngẫu nhiên", command=self.random_rsa_data).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Xóa", command=self.clear_rsa_data).pack(side="left")

        self.rsa_output = self.add_input_row(
            container,
            "Kết quả",
            "Kết quả mã hóa hoặc giải mã.",
            with_copy=True,
        )
        self.set_entry_state(self.rsa_output, False)
        self.add_field_action_row(
            container,
            [
                (
                    "Lưu Result ra file",
                    lambda: self.save_entry_to_text_file(self.rsa_output, "Kết quả", "rsa_result.txt"),
                ),
                ("Xuất báo cáo", self.export_rsa_result),
            ],
        )
        self.rsa_result_var = tk.StringVar(value="(chưa có kết quả)")
        tk.Label(
            container,
            textvariable=self.rsa_result_var,
            justify="left",
            anchor="w",
            wraplength=760,
            fg="#1f2937",
        ).pack(fill="x", pady=(2, 8))

        self.update_rsa_mode()

    def update_rsa_mode(self):
        mode = self.rsa_mode.get()
        is_encrypt = mode == "encrypt"

        self.set_entry_state(self.rsa_p, is_encrypt)
        self.set_entry_state(self.rsa_q, is_encrypt)
        self.set_entry_state(self.rsa_e, is_encrypt)
        self.set_entry_state(self.rsa_plain_input, is_encrypt)

        self.set_entry_state(self.rsa_cipher_input, not is_encrypt)
        self.set_entry_state(self.rsa_d, not is_encrypt)
        self.set_entry_state(self.rsa_n, not is_encrypt)

        self.rsa_action_button.configure(text="Mã hóa" if is_encrypt else "Giải mã")

    def clear_rsa_data(self):
        entries = [
            self.rsa_p,
            self.rsa_q,
            self.rsa_e,
            self.rsa_plain_input,
            self.rsa_cipher_input,
            self.rsa_d,
            self.rsa_n,
            self.rsa_output,
        ]
        for entry in entries:
            old_state = str(entry.cget("state"))
            entry.configure(state=tk.NORMAL)
            entry.delete(0, tk.END)
            if old_state == tk.DISABLED:
                entry.configure(state=tk.DISABLED)
        self.rsa_result_var.set("(chưa có kết quả)")
        self.rsa_last_result = None

    def random_rsa_data(self):
        try:
            p, q, e = self.random_rsa_params()
            message = self.random_alpha_text(5, 10)
            pub, priv = generate_keys(p, q, e)
            cipher = rsa_encrypt(message, pub)

            if self.rsa_mode.get() == "encrypt":
                self.set_entry_value(self.rsa_p, str(p))
                self.set_entry_value(self.rsa_q, str(q))
                self.set_entry_value(self.rsa_e, str(e))
                self.set_entry_value(self.rsa_plain_input, message)
                self.set_entry_value(self.rsa_cipher_input, "")
                self.set_entry_value(self.rsa_d, "")
                self.set_entry_value(self.rsa_n, "")
                self.set_result_display(self.rsa_output, self.rsa_result_var, "")
            else:
                self.set_entry_value(self.rsa_cipher_input, str(cipher))
                self.set_entry_value(self.rsa_d, str(priv[0]))
                self.set_entry_value(self.rsa_n, str(priv[1]))
                self.set_result_display(self.rsa_output, self.rsa_result_var, "")
            self.rsa_last_result = None
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def handle_rsa_action(self):
        if self.rsa_mode.get() == "encrypt":
            self.handle_rsa_encrypt()
        else:
            self.handle_rsa_decrypt()

    def validate_rsa(self, p, q, e):
        try:
            p, q, e = int(p), int(q), int(e)
            return p, q, e
        except ValueError:
            messagebox.showerror("Error", "p, q, e phải là số")
            return None

    def parse_cipher(self, text):
        try:
            value = ast.literal_eval(text)
        except (ValueError, SyntaxError):
            raise ValueError("Cipher phải là danh sách số nguyên, ví dụ: [72, 101]")

        if not isinstance(value, list) or not all(isinstance(x, int) for x in value):
            raise ValueError("Cipher phải là danh sách số nguyên, ví dụ: [72, 101]")
        return value

    def read_privkey(self):
        d_raw = self.rsa_d.get().strip()
        n_raw = self.rsa_n.get().strip()
        if not d_raw or not n_raw:
            raise ValueError("Vui lòng nhập private key d và n")

        try:
            d = int(d_raw)
            n = int(n_raw)
        except ValueError:
            raise ValueError("d và n phải là số nguyên")

        if d <= 0 or n <= 0:
            raise ValueError("d và n phải lớn hơn 0")

        return d, n

    def handle_rsa_encrypt(self):
        values = self.validate_rsa(self.rsa_p.get(), self.rsa_q.get(), self.rsa_e.get())
        if not values:
            return

        p, q, e = values
        msg = self.rsa_plain_input.get()
        if not msg:
            messagebox.showerror("Error", "Không được để trống Plaintext")
            return

        try:
            pub, priv = generate_keys(p, q, e)
            cipher = rsa_encrypt(msg, pub)

            self.set_entry_value(self.rsa_cipher_input, str(cipher))
            self.set_entry_value(self.rsa_d, str(priv[0]))
            self.set_entry_value(self.rsa_n, str(priv[1]))

            self.set_result_display(self.rsa_output, self.rsa_result_var, str(cipher))
            self.rsa_last_result = {
                "mode": "Encrypt",
                "plaintext": msg,
                "ciphertext": str(cipher),
                "p": p,
                "q": q,
                "e": e,
                "d": priv[0],
                "n": priv[1],
            }
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def handle_rsa_decrypt(self):
        try:
            cipher = self.parse_cipher(self.rsa_cipher_input.get())
            priv = self.read_privkey()
            result = rsa_decrypt(cipher, priv)

            self.set_result_display(self.rsa_output, self.rsa_result_var, result)
            p_val = self.rsa_p.get().strip() or "N/A"
            q_val = self.rsa_q.get().strip() or "N/A"
            e_val = self.rsa_e.get().strip() or "N/A"
            self.rsa_last_result = {
                "mode": "Decrypt",
                "plaintext": result,
                "ciphertext": str(cipher),
                "p": p_val,
                "q": q_val,
                "e": e_val,
                "d": priv[0],
                "n": priv[1],
            }
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def export_rsa_result(self):
        if not self.rsa_last_result:
            messagebox.showwarning("Xuất báo cáo", "Chưa có kết quả RSA để xuất")
            return

        exported_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = (
            "=== RSA EXPORT ===\n"
            f"Thời gian export: {exported_at}\n"
            f"Chế độ: {self.rsa_last_result['mode']}\n"
            f"Plaintext: {self.rsa_last_result['plaintext']}\n"
            f"Ciphertext: {self.rsa_last_result['ciphertext']}\n"
            f"p: {self.rsa_last_result['p']}\n"
            f"q: {self.rsa_last_result['q']}\n"
            f"e: {self.rsa_last_result['e']}\n"
            f"d: {self.rsa_last_result['d']}\n"
            f"n: {self.rsa_last_result['n']}\n"
        )
        self.save_text_report(content, "rsa_export.txt")

    # ================= ABOUT US =================
    def build_about_us(self):
        container = tk.Frame(self.aboutUs_tab, padx=16, pady=14)
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="THÔNG TIN ĐỒ ÁN",
            font=("TkDefaultFont", 13, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        info_text = (
            "Môn học: An toàn mạng máy tính - NT101.Q22\n"
            "Giảng viên phụ trách: Tô Nguyễn Nhật Quang\n"
            "Niên khóa: Học kỳ 2, 2025-2026\n"
            "Thành viên nhóm:\n"
            "1. Mai Nguyễn Bình Tân\n"
            "2. Lê Huy Hiếu\n"
            "3. Phạm Thành Danh"
        )
        tk.Label(
            container,
            text=info_text,
            justify="left",
            anchor="w",
            wraplength=760,
        ).pack(fill="x", pady=(0, 12))

        tk.Label(
            container,
            text="MÔ TẢ SƠ LƯỢC ỨNG DỤNG",
            font=("TkDefaultFont", 11, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 8))

        app_desc = (
            "Đây là ứng dụng desktop minh họa hai thuật toán mật mã cơ bản: "
            "Playfair và RSA.\n\n"
            "- Tab Playfair hỗ trợ mã hóa/giải mã văn bản theo mô hình bảng khóa 5x5, "
            "đồng thời hiển thị trực quan Keysquare để người học dễ theo dõi cơ chế biến đổi ký tự.\n"
            "- Tab RSA hỗ trợ hai chế độ Encrypt/Decrypt, kiểm tra dữ liệu đầu vào, sinh khóa từ p, q, e, "
            "và cho phép thao tác với ciphertext/private key để quan sát toàn bộ quy trình.\n"
            "- Ứng dụng có các tiện ích học tập như nút hướng dẫn (?), tạo dữ liệu ngẫu nhiên, xóa nhanh dữ liệu, "
            "và sao chép kết quả để thuận tiện khi thực hành.\n\n"
            "Mục tiêu chính của ứng dụng là phục vụ học tập, giúp sinh viên nắm được nguyên lý hoạt động của thuật toán "
            "thông qua thao tác trực tiếp trên giao diện." 
        )
        tk.Label(
            container,
            text=app_desc,
            justify="left",
            anchor="nw",
            wraplength=760,
        ).pack(fill="x")

    def run(self):
        self.root.mainloop()

