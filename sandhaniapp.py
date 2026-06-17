import os
import sys
import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class MedicalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sandhani Medical Record System")
        self.root.geometry("850x700")
        
        self.style = ttk.Style()
        self.style.theme_use('clam') 
        self.style.configure('.', font=('Helvetica', 11)) 
        self.style.configure('TLabelframe.Label', font=('Helvetica', 12, 'bold'), foreground="#1a5276")
        self.style.configure('TLabelframe', padding=15)
        self.style.configure('Action.TButton', font=('Helvetica', 13, 'bold'), padding=15)
        
        self.vcmd_digits = (self.root.register(self.validate_digits_only), '%S')
        self.vcmd_decimal = (self.root.register(self.validate_decimal_only), '%P')
        
        self.form_type = tk.StringVar(value="screening")
        
        self.var_name = tk.StringVar()
        self.var_age = tk.StringVar()
        self.var_sex = tk.StringVar(value="Male")
        self.var_phone = tk.StringVar()
        self.var_date = tk.StringVar(value=datetime.now().strftime("%d-%b-%Y"))
        
        self.var_r_name = tk.StringVar()
        self.var_r_age = tk.StringVar()
        self.var_r_sex = tk.StringVar(value="Male")
        self.var_r_phone = tk.StringVar()
        
        self.var_bag_no = tk.StringVar()
        self.var_abo = tk.StringVar(value="O")
        self.var_rh = tk.StringVar(value="Positive (+)")
        self.var_compat = tk.StringVar(value="Compatible")
        
        self.tests = {
            "hbsag": tk.StringVar(value="N/A"),
            "hcv": tk.StringVar(value="N/A"),
            "hiv": tk.StringVar(value="N/A"),
            "malaria": tk.StringVar(value="N/A"),
            "vdrl": tk.StringVar(value="N/A")
        }
        
        self.var_glucose_val = tk.StringVar()
        self.var_glucose_type = tk.StringVar(value="Random")
        
        self.create_search_bar()
        self.create_form_selector()
        self.create_action_buttons()
        
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, padding=10)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.build_screening_form()

    def validate_digits_only(self, char_typed):
        return char_typed.isdigit()

    def validate_decimal_only(self, current_full_text):
        if current_full_text == "":
            return True
        try:
            float(current_full_text)
            return True
        except ValueError:
            return False

    def create_search_bar(self):
        search_frame = ttk.LabelFrame(self.root, text=" 🔍 Search Existing Records ")
        search_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.var_search = tk.StringVar()
        ttk.Label(search_frame, text="Enter Phone Number:").pack(side=tk.LEFT, padx=10)
        
        ttk.Entry(search_frame, textvariable=self.var_search, width=25, 
                  validate="key", validatecommand=self.vcmd_digits).pack(side=tk.LEFT, padx=10)
        ttk.Button(search_frame, text="Search System", command=self.search_record).pack(side=tk.LEFT, padx=10)

    def create_form_selector(self):
        selector_frame = ttk.Frame(self.root, padding=10)
        selector_frame.pack(fill=tk.X, padx=15)
        
        ttk.Radiobutton(selector_frame, text="Option 1: Blood Screening Report", 
                        variable=self.form_type, value="screening", command=self.toggle_forms).pack(side=tk.LEFT, padx=20)
        ttk.Radiobutton(selector_frame, text="Option 2: Blood Donation & Cross-Matching", 
                        variable=self.form_type, value="donation", command=self.toggle_forms).pack(side=tk.LEFT, padx=20)

    def toggle_forms(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        if self.form_type.get() == "screening":
            self.build_screening_form()
        else:
            self.build_donation_form()

    def build_screening_form(self):
        info_box = ttk.LabelFrame(self.scrollable_frame, text=" Patient Information ")
        info_box.pack(fill=tk.X, pady=5)
        
        self.setup_patient_grid(info_box, self.var_name, self.var_age, self.var_sex, self.var_phone, self.var_date)
        
        test_box = ttk.LabelFrame(self.scrollable_frame, text=" Rapid Screening Tests (Defaults to N/A) ")
        test_box.pack(fill=tk.X, pady=15)
        
        options = ["N/A", "Negative", "Positive"]
        row = 0
        for test_name, var in self.tests.items():
            ttk.Label(test_box, text=f"{test_name.upper()}:").grid(row=row, column=0, sticky=tk.W, pady=5, padx=10)
            ttk.Combobox(test_box, textvariable=var, values=options, state="readonly", width=15).grid(row=row, column=1, sticky=tk.W, pady=5, padx=10)
            row += 1
            
        ttk.Label(test_box, text="Blood Glucose (mmol/L):").grid(row=row, column=0, sticky=tk.W, pady=15, padx=10)
        ttk.Entry(test_box, textvariable=self.var_glucose_val, width=15,
                  validate="key", validatecommand=self.vcmd_decimal).grid(row=row, column=1, sticky=tk.W, pady=15, padx=10)
        ttk.Combobox(test_box, textvariable=self.var_glucose_type, values=["Fasting", "2hours", "Random"], state="readonly", width=15).grid(row=row, column=2, sticky=tk.W, pady=15, padx=10)

    def build_donation_form(self):
        dual_frame = ttk.Frame(self.scrollable_frame)
        dual_frame.pack(fill=tk.X, pady=5)
        
        donor_box = ttk.LabelFrame(dual_frame, text=" Donor Information ")
        donor_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.setup_patient_grid(donor_box, self.var_name, self.var_age, self.var_sex, self.var_phone, self.var_date)
        
        recip_box = ttk.LabelFrame(dual_frame, text=" Recipient Information ")
        recip_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        self.setup_patient_grid(recip_box, self.var_r_name, self.var_r_age, self.var_r_sex, self.var_r_phone, None)
        
        match_box = ttk.LabelFrame(self.scrollable_frame, text=" Verification & Cross-Match ")
        match_box.pack(fill=tk.X, pady=15)
        
        ttk.Label(match_box, text="Blood Bag Number:").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        ttk.Entry(match_box, textvariable=self.var_bag_no, width=20).grid(row=0, column=1, sticky=tk.W, pady=10, padx=10)
        
        ttk.Label(match_box, text="ABO Group:").grid(row=0, column=2, sticky=tk.W, pady=10, padx=15)
        ttk.Combobox(match_box, textvariable=self.var_abo, values=["A", "B", "AB", "O"], state="readonly", width=10).grid(row=0, column=3, sticky=tk.W, pady=10, padx=5)
        
        ttk.Label(match_box, text="Rh Factor:").grid(row=0, column=4, sticky=tk.W, pady=10, padx=15)
        ttk.Combobox(match_box, textvariable=self.var_rh, values=["Positive (+)", "Negative (-)"], state="readonly", width=15).grid(row=0, column=5, sticky=tk.W, pady=10, padx=5)
        
        ttk.Label(match_box, text="Cross-Match Decision:").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        ttk.Combobox(match_box, textvariable=self.var_compat, values=["Compatible", "Incompatible"], state="readonly", width=20).grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=10, padx=10)

        donor_test_box = ttk.LabelFrame(self.scrollable_frame, text=" Donor Rapid Screening Tests ")
        donor_test_box.pack(fill=tk.X, pady=5)
        
        options = ["N/A", "Negative", "Positive"]
        row = 0
        for test_name, var in self.tests.items():
            ttk.Label(donor_test_box, text=f"Donor {test_name.upper()}:").grid(row=row, column=0, sticky=tk.W, pady=5, padx=10)
            ttk.Combobox(donor_test_box, textvariable=var, values=options, state="readonly", width=15).grid(row=row, column=1, sticky=tk.W, pady=5, padx=10)
            row += 1

    def setup_patient_grid(self, master, name, age, sex, phone, date_var):
        ttk.Label(master, text="Full Name:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=10)
        ttk.Entry(master, textvariable=name, width=25).grid(row=0, column=1, sticky=tk.W, pady=5, padx=10)
        
        ttk.Label(master, text="Age:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=10)
        ttk.Entry(master, textvariable=age, width=12, 
                  validate="key", validatecommand=self.vcmd_digits).grid(row=1, column=1, sticky=tk.W, pady=5, padx=10)
        
        ttk.Label(master, text="Sex:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=10)
        ttk.Combobox(master, textvariable=sex, values=["Male", "Female", "Other"], state="readonly", width=12).grid(row=2, column=1, sticky=tk.W, pady=5, padx=10)
        
        ttk.Label(master, text="Phone No:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=10)
        ttk.Entry(master, textvariable=phone, width=25, 
                  validate="key", validatecommand=self.vcmd_digits).grid(row=3, column=1, sticky=tk.W, pady=5, padx=10)
        
        if date_var:
            ttk.Label(master, text="Date:").grid(row=4, column=0, sticky=tk.W, pady=5, padx=10)
            ttk.Entry(master, textvariable=date_var, width=25).grid(row=4, column=1, sticky=tk.W, pady=5, padx=10)

    def create_action_buttons(self):
        btn_frame = ttk.Frame(self.root, padding=15)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        ttk.Button(btn_frame, text="👁️ Generate & Preview PDF", command=self.process_submission, style='Action.TButton').pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)
        ttk.Button(btn_frame, text="🧹 Clear Screen", command=self.clear_fields, style='Action.TButton').pack(side=tk.RIGHT, padx=20, expand=True, fill=tk.X)

    def process_submission(self):
        self.var_name.set(self.var_name.get().upper().strip())
        self.var_r_name.set(self.var_r_name.get().upper().strip())
        
        phone = self.var_phone.get().strip()
        if not phone or not self.var_name.get():
            messagebox.showerror("Missing Data", "Primary Patient Name and Phone Number are strictly required.")
            return
            
        filename = f"{phone}_{self.form_type.get()}.pdf"
        self.generate_medical_pdf(filename)
        self.save_to_csv()
        
        try:
            os.startfile(filename)
        except Exception:
            messagebox.showinfo("PDF Saved", f"Report saved successfully as {filename} inside your application folder.")

    def generate_medical_pdf(self, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        
        # --- THE FIX: ADDED SECTION TITLES AND UNDERLINES ---
        c.setFont("Helvetica-Bold", 12)
        if self.form_type.get() == "screening":
            c.drawString(80, 545, "Patient Information")
            c.line(80, 540, 200, 540)
        else:
            c.drawString(80, 545, "Donor Information")
            c.line(80, 540, 195, 540)
            
        c.setFont("Helvetica", 11)
        c.drawString(80, 520, f"Date: {self.var_date.get()}")
        c.drawString(80, 500, f"Name: {self.var_name.get()}")
        c.drawString(80, 480, f"Phone No: {self.var_phone.get()}")
        
        c.drawString(400, 500, f"Age: {self.var_age.get()} Y")
        c.drawString(400, 480, f"Sex: {self.var_sex.get()}")
        
        if self.form_type.get() == "screening":
            c.setFont("Helvetica-Bold", 12)
            c.drawString(80, 430, "Blood Screening Report")
            c.line(80, 425, 230, 425)
            
            y_pos = 390
            c.setFont("Helvetica-Bold", 11)
            
            for test_name, var in self.tests.items():
                val = var.get()
                if val != "N/A":
                    c.drawString(80, y_pos, f"► {test_name.upper()}")
                    c.drawString(300, y_pos, f": {val}")
                    y_pos -= 25 
                    
            g_val = self.var_glucose_val.get().strip()
            if g_val:
                c.drawString(80, y_pos, "► BLOOD GLUCOSE")
                c.drawString(300, y_pos, f": {g_val} mmol/L ({self.var_glucose_type.get()})")
                
        else:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(80, 440, f"Blood Bag No: {self.var_bag_no.get().strip()}")
            
            c.setFont("Helvetica-Bold", 16)
            c.drawString(80, 415, f"DONOR BLOOD TYPE: {self.var_abo.get()} {self.var_rh.get()}")
            
            c.setFont("Helvetica-Bold", 14)
            c.drawString(80, 390, f"CROSS-MATCH EVALUATION: {self.var_compat.get().upper()}")
            
            # --- THE FIX: ADDED RECIPIENT TITLE & CLEANED LABELS ---
            c.setFont("Helvetica-Bold", 12)
            c.drawString(80, 355, "Recipient Information")
            c.line(80, 350, 215, 350)
            
            c.setFont("Helvetica", 11)
            # The redundant "Recipient" words are completely gone
            c.drawString(80, 330, f"Name: {self.var_r_name.get()}")
            c.drawString(80, 310, f"Phone No: {self.var_r_phone.get()}")
            c.drawString(400, 330, f"Age: {self.var_r_age.get()} Y")
            c.drawString(400, 310, f"Sex: {self.var_r_sex.get()}")
            
            c.setFont("Helvetica-Bold", 11)
            c.drawString(80, 270, "Donor Compulsory Screening Results:")
            y_pos = 250
            
            for test_name, var in self.tests.items():
                c.drawString(80, y_pos, f"► Donor {test_name.upper()}")
                c.drawString(300, y_pos, f": {var.get()}")
                y_pos -= 22

        c.setFont("Helvetica", 11)
        c.drawString(430, 160, "Signature: __________________")
        c.drawString(430, 140, "Date: _______________________")
        
        c.save()

    def save_to_csv(self):
        file_exists = os.path.isfile("medical_records.csv")
        with open("medical_records.csv", mode="a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "FormType", "PrimaryPhone", "PrimaryName", "Age", "Sex", "PayloadDetails"])
            
            details = f"Bag:{self.var_bag_no.get()}|ABO:{self.var_abo.get()}|Compat:{self.var_compat.get()}" if self.form_type.get() == "donation" else f"Glucose:{self.var_glucose_val.get()}"
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.form_type.get(),
                self.var_phone.get(),
                self.var_name.get(),
                self.var_age.get(),
                self.var_sex.get(),
                details
            ])

    def search_record(self):
        target = self.var_search.get().strip()
        if not target:
            return
            
        if not os.path.isfile("medical_records.csv"):
            messagebox.showinfo("Empty System", "No saved databases found yet.")
            return
            
        with open("medical_records.csv", mode="r") as f:
            reader = csv.DictReader(f)
            for row in reversed(list(reader)):
                if row["PrimaryPhone"] == target:
                    self.form_type.set(row["FormType"])
                    self.toggle_forms()
                    self.var_phone.set(row["PrimaryPhone"])
                    self.var_name.set(row["PrimaryName"])
                    self.var_age.set(row["Age"])
                    self.var_sex.set(row["Sex"])
                    messagebox.showinfo("Found Record", f"Patient profile for {row['PrimaryName']} loaded successfully!")
                    return
            messagebox.showwarning("Not Found", "No local entry matches that phone number.")

    def clear_fields(self):
        self.var_name.set("")
        self.var_age.set("")
        self.var_phone.set("")
        self.var_r_name.set("")
        self.var_r_age.set("")
        self.var_r_phone.set("")
        self.var_bag_no.set("")
        self.var_glucose_val.set("")
        self.var_search.set("")
        for var in self.tests.values():
            var.set("N/A")

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalApp(root)
    root.mainloop()
