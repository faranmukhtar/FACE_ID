import tkinter as tk
from tkinter import font as tkfont
import Register

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Face ID")
        self.root.geometry("420x560")
        self.root.configure(bg="#0F0F0F")
        self.root.resizable(False, False)

        self._confirm_result = 'N'

        self.BG         = "#0F0F0F"
        self.SURFACE    = "#1A1A1A"
        self.BORDER     = "#2A2A2A"
        self.ACCENT     = "#00C98D"
        self.ACCENT_DIM = "#009E6F"
        self.DANGER     = "#E24B4A"
        self.TEXT       = "#F0F0F0"
        self.MUTED      = "#888880"

        self.title_font   = tkfont.Font(family="Helvetica Neue", size=22, weight="bold")
        self.sub_font     = tkfont.Font(family="Helvetica Neue", size=11)
        self.btn_font     = tkfont.Font(family="Helvetica Neue", size=13, weight="bold")
        self.label_font   = tkfont.Font(family="Helvetica Neue", size=10)
        self.status_font  = tkfont.Font(family="Helvetica Neue", size=12)

        self.build_home()

    def build_home(self):
        for w in self.root.winfo_children():
            w.destroy()

        outer = tk.Frame(self.root, bg=self.BG)
        outer.place(relwidth=1, relheight=1)

        tk.Frame(outer, bg=self.BG, height=60).pack()

        icon_canvas = tk.Canvas(outer, width=80, height=80,
                                bg=self.BG, highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_oval(4, 4, 76, 76, fill=self.SURFACE,
                                outline=self.ACCENT, width=2)
        icon_canvas.create_oval(28, 24, 52, 48, fill="", outline=self.ACCENT, width=1.5)
        icon_canvas.create_arc(18, 44, 62, 70, start=0, extent=180,
                               style="arc", outline=self.ACCENT, width=1.5)

        tk.Frame(outer, bg=self.BG, height=20).pack()

        tk.Label(outer, text="Face ID", font=self.title_font,
                 bg=self.BG, fg=self.TEXT).pack()

        tk.Label(outer, text="Secure biometric access control",
                 font=self.sub_font, bg=self.BG, fg=self.MUTED).pack(pady=(4, 0))

        tk.Frame(outer, bg=self.BG, height=48).pack()

        card = tk.Frame(outer, bg=self.SURFACE,
                        highlightbackground=self.BORDER,
                        highlightthickness=1)
        card.pack(padx=40, fill="x")

        self._action_btn(card, "Login with Face", self.ACCENT, "#0F0F0F",
                         self.do_login).pack(padx=24, pady=(24, 12), fill="x")

        divider_row = tk.Frame(card, bg=self.SURFACE)
        divider_row.pack(padx=24, fill="x", pady=4)
        tk.Frame(divider_row, bg=self.BORDER, height=1).pack(
            side="left", fill="x", expand=True)
        tk.Label(divider_row, text="  or  ", font=self.label_font,
                 bg=self.SURFACE, fg=self.MUTED).pack(side="left")
        tk.Frame(divider_row, bg=self.BORDER, height=1).pack(
            side="left", fill="x", expand=True)

        self._action_btn(card, "Register New Face", self.SURFACE, self.TEXT,
                         self.open_register, border_color=self.BORDER).pack(
            padx=24, pady=(12, 24), fill="x")

        tk.Frame(outer, bg=self.BG, height=32).pack()

        self.status_var = tk.StringVar(value="")
        self.status_label = tk.Label(outer, textvariable=self.status_var,
                                     font=self.status_font, bg=self.BG,
                                     fg=self.MUTED, wraplength=340)
        self.status_label.pack()

        tk.Frame(outer, bg=self.BG, height=20).pack()
        tk.Label(outer, text="Powered by face_recognition",
                 font=self.label_font, bg=self.BG, fg="#3A3A38").pack()

    def _action_btn(self, parent, text, bg, fg, command, border_color=None):
        bc = border_color or bg
        f = tk.Frame(parent, bg=bc, highlightbackground=bc, highlightthickness=1)
        btn = tk.Label(f, text=text, font=self.btn_font,
                       bg=bg, fg=fg, cursor="hand2",
                       padx=0, pady=13)
        btn.pack(fill="x")
        btn.bind("<Button-1>", lambda e: command())
        btn.bind("<Enter>",  lambda e: btn.config(bg=self._lighten(bg)))
        btn.bind("<Leave>",  lambda e: btn.config(bg=bg))
        return f

    def _lighten(self, hex_color):
        mapping = {
            self.ACCENT:  self.ACCENT_DIM,
            self.SURFACE: "#222222",
        }
        return mapping.get(hex_color, hex_color)

    def do_login(self):
        self.set_status("Scanning...", self.MUTED)
        self.root.update()
        result = Register.predict()
        if result != "Unknown":
            self.set_status(f"Access granted — welcome, {result}!", self.ACCENT)
            self.show_granted(result)
        else:
            self.set_status("Face not recognised. Try again or register.", self.DANGER)

    def show_granted(self, name):
        popup = tk.Toplevel(self.root)
        popup.title("Access Granted")
        popup.geometry("300x220")
        popup.configure(bg=self.BG)
        popup.resizable(False, False)
        popup.grab_set()

        c = tk.Canvas(popup, width=60, height=60, bg=self.BG, highlightthickness=0)
        c.pack(pady=(28, 8))
        c.create_oval(2, 2, 58, 58, fill=self.SURFACE, outline=self.ACCENT, width=2)
        c.create_line(16, 30, 26, 42, fill=self.ACCENT, width=3)
        c.create_line(26, 42, 46, 18, fill=self.ACCENT, width=3)

        tk.Label(popup, text="Access Granted", font=self.btn_font,
                 bg=self.BG, fg=self.ACCENT).pack()
        tk.Label(popup, text=f"Welcome, {name}", font=self.sub_font,
                 bg=self.BG, fg=self.MUTED).pack(pady=4)

        tk.Label(popup, text="Close", font=self.label_font,
                 bg=self.BG, fg=self.MUTED, cursor="hand2").pack(pady=12)
        popup.bind("<Button-1>", lambda e: popup.destroy())

    def open_register(self):
        popup = tk.Toplevel(self.root)
        popup.title("Register")
        popup.geometry("320x220")
        popup.configure(bg=self.BG)
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text="Register your face", font=self.btn_font,
                 bg=self.BG, fg=self.TEXT).pack(pady=(28, 4))
        tk.Label(popup, text="Enter your name to begin capture",
                 font=self.sub_font, bg=self.BG, fg=self.MUTED).pack()

        tk.Frame(popup, bg=self.BG, height=16).pack()

        entry_frame = tk.Frame(popup, bg=self.BORDER, highlightthickness=0)
        entry_frame.pack(padx=32, fill="x")
        entry = tk.Entry(entry_frame, font=self.status_font,
                         bg=self.SURFACE, fg=self.TEXT,
                         insertbackground=self.TEXT,
                         relief="flat", bd=8)
        entry.pack(fill="x")
        entry.focus_set()

        tk.Frame(popup, bg=self.BG, height=16).pack()

        def do_register():
            name = entry.get().strip()
            if not name:
                return
            popup.destroy()
            self.set_status(f"Registering {name}... follow on-screen prompts.", self.MUTED)
            self.root.update()
            Register.Registerface(name, self.get_confirmation)
            self.set_status(f"Registration complete for {name}.", self.ACCENT)

        self._action_btn(popup, "Start Capture", self.ACCENT, "#0F0F0F",
                         do_register).pack(padx=32, fill="x")
        entry.bind("<Return>", lambda e: do_register())

    def get_confirmation(self, fname):
        popup = tk.Toplevel(self.root)
        popup.title("Confirm identity")
        popup.geometry("320x220")
        popup.configure(bg=self.BG)
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text="Face already on file",
                 font=self.btn_font, bg=self.BG, fg=self.TEXT).pack(pady=(28, 4))
        tk.Label(popup, text=f"Is this person  \"{fname}\"?",
                 font=self.sub_font, bg=self.BG, fg=self.MUTED).pack()

        tk.Frame(popup, bg=self.BG, height=20).pack()

        btn_row = tk.Frame(popup, bg=self.BG)
        btn_row.pack(padx=32, fill="x")

        self._confirm_result = 'N'

        def yes():
            self._confirm_result = 'Y'
            popup.destroy()

        def no():
            self._confirm_result = 'N'
            popup.destroy()

        yes_f = tk.Frame(btn_row, bg=self.ACCENT)
        yes_l = tk.Label(yes_f, text="Yes, merge", font=self.label_font,
                         bg=self.ACCENT, fg="#0F0F0F", padx=0, pady=10, cursor="hand2")
        yes_l.pack(fill="x", padx=1, pady=1)
        yes_l.bind("<Button-1>", lambda e: yes())
        yes_f.pack(side="left", expand=True, fill="x", padx=(0, 6))

        no_f = tk.Frame(btn_row, bg=self.BORDER)
        no_l = tk.Label(no_f, text="No, new person", font=self.label_font,
                        bg=self.SURFACE, fg=self.TEXT, padx=0, pady=10, cursor="hand2")
        no_l.pack(fill="x", padx=1, pady=1)
        no_l.bind("<Button-1>", lambda e: no())
        no_f.pack(side="left", expand=True, fill="x")

        self.root.wait_window(popup)
        return self._confirm_result

    def set_status(self, msg, color):
        self.status_var.set(msg)
        self.status_label.config(fg=color)
        self.root.update()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()