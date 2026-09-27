import tkinter as tk
from tkinter import ttk, messagebox
import csv


# ==========================================
# LOAD MEDICINE DATABASE
# ==========================================

try:
    with open("medicine_safety_starter.csv", "r", encoding="utf-8") as file:
        medicines = list(csv.DictReader(file))

except FileNotFoundError:
    medicines = []
    print("ERROR: medicine_safety_starter.csv was not found.")


# ==========================================
# CHECK MEDICINE
# ==========================================

def check_medicine():

    medicine_name = medicine_entry.get().strip().lower()

    if medicine_name == "":
        messagebox.showwarning(
            "Missing information",
            "Please enter a medicine name."
        )
        return

    # Find medicine
    medicine = None

    for item in medicines:

        name = item["medicine"].lower()
        aliases = item["aliases"].lower()

        if medicine_name == name or medicine_name == aliases:
            medicine = item
            break

    # Medicine not found
    if medicine is None:

        result_text.delete("1.0", tk.END)

        result_text.insert(
            tk.END,
            "❓ MEDICINE NOT FOUND\n\n"
            "This medicine is not currently in the database.\n\n"
            "Try another medicine or add it to the CSV database."
        )

        status_label.config(
            text="Medicine not found",
            foreground="gray"
        )

        return

    # Get user conditions
    has_diabetes = diabetes_var.get()
    has_high_bp = blood_pressure_var.get()
    has_kidney = kidney_var.get()

    warnings = []

    # Diabetes
    if has_diabetes == "Yes":

        if medicine["diabetes"] == "high_caution":
            warnings.append("⚠ Diabetes: HIGH CAUTION")

        elif medicine["diabetes"] == "caution":
            warnings.append("⚠ Diabetes: CAUTION")

    # Blood pressure
    if has_high_bp == "Yes":

        if medicine["high_blood_pressure"] == "high_caution":
            warnings.append("⚠ Blood pressure: HIGH CAUTION")

        elif medicine["high_blood_pressure"] == "caution":
            warnings.append("⚠ Blood pressure: CAUTION")

    # Kidney disease
    if has_kidney == "Yes":

        if medicine["kidney_disease"] == "high_caution":
            warnings.append("⚠ Kidney disease: HIGH CAUTION")

        elif medicine["kidney_disease"] == "caution":
            warnings.append("⚠ Kidney disease: CAUTION")

    # ==========================================
    # DISPLAY RESULT
    # ==========================================

    result_text.delete("1.0", tk.END)

    result_text.insert(
        tk.END,
        "MEDICINE SAFETY CHECK\n"
        "========================================\n\n"
    )

    result_text.insert(
        tk.END,
        f"Medicine: {medicine['medicine']}\n"
    )

    result_text.insert(
        tk.END,
        f"Class: {medicine['class']}\n\n"
    )

    # Determine status
    if any("HIGH CAUTION" in warning for warning in warnings):

        status = "🔴 HIGH CAUTION"

        status_label.config(
            text=status,
            foreground="red"
        )

    elif warnings:

        status = "🟡 CAUTION"

        status_label.config(
            text=status,
            foreground="orange"
        )

    else:

        status = "🟢 NO SPECIFIC WARNING FOUND"

        status_label.config(
            text=status,
            foreground="green"
        )

    result_text.insert(
        tk.END,
        f"Status: {status}\n\n"
    )

    # Warnings
    if warnings:

        result_text.insert(
            tk.END,
            "Warnings:\n"
        )

        for warning in warnings:

            result_text.insert(
                tk.END,
                f"  {warning}\n"
            )

        result_text.insert(tk.END, "\n")

    else:

        result_text.insert(
            tk.END,
            "No specific warning was found for the conditions\n"
            "you entered in this starter database.\n\n"
        )

    # Notes
    result_text.insert(
        tk.END,
        "Notes:\n"
        f"{medicine['notes']}\n\n"
    )

    # Action
    result_text.insert(
        tk.END,
        "Recommended action:\n"
        f"{medicine['action']}\n\n"
    )

    result_text.insert(
        tk.END,
        "----------------------------------------\n"
        "IMPORTANT:\n"
        "This is an educational tool and does NOT\n"
        "determine whether a medicine is medically\n"
        "safe for a specific person.\n"
        "Always check with a doctor or pharmacist\n"
        "when appropriate."
    )


# ==========================================
# CLEAR BUTTON
# ==========================================

def clear_form():

    medicine_entry.delete(0, tk.END)

    diabetes_var.set("No")
    blood_pressure_var.set("No")
    kidney_var.set("No")

    result_text.delete("1.0", tk.END)

    status_label.config(
        text="Ready",
        foreground="black"
    )


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title("Medicine Safety Checker")

root.geometry("700x650")

root.resizable(False, False)


# ==========================================
# TITLE
# ==========================================

title_label = tk.Label(
    root,
    text="Medicine Safety Checker",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=20)


subtitle_label = tk.Label(
    root,
    text="Educational medicine-condition checker",
    font=("Arial", 11)
)

subtitle_label.pack()


# ==========================================
# MEDICINE INPUT
# ==========================================

medicine_frame = tk.Frame(root)

medicine_frame.pack(pady=20)

medicine_label = tk.Label(
    medicine_frame,
    text="Medicine name:",
    font=("Arial", 12)
)

medicine_label.pack(side=tk.LEFT, padx=10)


medicine_entry = tk.Entry(
    medicine_frame,
    width=35,
    font=("Arial", 12)
)

medicine_entry.pack(side=tk.LEFT)


# ==========================================
# CONDITIONS
# ==========================================

conditions_frame = tk.LabelFrame(
    root,
    text="Health conditions",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=15
)

conditions_frame.pack(
    padx=30,
    fill="x"
)


diabetes_var = tk.StringVar(value="No")

blood_pressure_var = tk.StringVar(value="No")

kidney_var = tk.StringVar(value="No")


# Diabetes
tk.Label(
    conditions_frame,
    text="Diabetes:"
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=10,
    pady=5
)

ttk.Combobox(
    conditions_frame,
    textvariable=diabetes_var,
    values=["No", "Yes"],
    state="readonly",
    width=12
).grid(
    row=0,
    column=1,
    padx=10
)


# Blood pressure
tk.Label(
    conditions_frame,
    text="High blood pressure:"
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=10,
    pady=5
)

ttk.Combobox(
    conditions_frame,
    textvariable=blood_pressure_var,
    values=["No", "Yes"],
    state="readonly",
    width=12
).grid(
    row=1,
    column=1,
    padx=10
)


# Kidney
tk.Label(
    conditions_frame,
    text="Kidney disease:"
).grid(
    row=2,
    column=0,
    sticky="w",
    padx=10,
    pady=5
)

ttk.Combobox(
    conditions_frame,
    textvariable=kidney_var,
    values=["No", "Yes"],
    state="readonly",
    width=12
).grid(
    row=2,
    column=1,
    padx=10
)


# ==========================================
# BUTTONS
# ==========================================

button_frame = tk.Frame(root)

button_frame.pack(pady=20)


check_button = tk.Button(
    button_frame,
    text="Check Medicine",
    command=check_medicine,
    font=("Arial", 12, "bold"),
    width=18
)

check_button.pack(side=tk.LEFT, padx=10)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_form,
    font=("Arial", 12),
    width=10
)

clear_button.pack(side=tk.LEFT, padx=10)


# ==========================================
# STATUS
# ==========================================

status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 14, "bold")
)

status_label.pack(pady=5)


# ==========================================
# RESULT BOX
# ==========================================

result_frame = tk.LabelFrame(
    root,
    text="Result",
    font=("Arial", 11, "bold")
)

result_frame.pack(
    padx=30,
    pady=10,
    fill="both",
    expand=True
)


result_text = tk.Text(
    result_frame,
    height=15,
    width=75,
    font=("Consolas", 10),
    wrap=tk.WORD
)

result_text.pack(
    padx=10,
    pady=10,
    fill="both",
    expand=True
)


# ==========================================
# START APP
# ==========================================

root.mainloop()