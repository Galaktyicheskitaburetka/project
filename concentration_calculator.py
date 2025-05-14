import tkinter as tk
from tkinter import ttk
from math import log10


def show_ph_calculator():
    clear_inputs()
    method_var.set("H+")

    tk.Label(input_frame, text="Выберите метод расчёта pH:").pack()

    methods = [
        ("По концентрации [H⁺]", "H+"),
        ("По концентрации [OH⁻]", "OH-"),
        ("По Ka и концентрации слабой кислоты", "Ka"),
    ]

    for text, mode in methods:
        tk.Radiobutton(input_frame, text=text, variable=method_var, value=mode).pack()

    tk.Button(input_frame, text="Далее →", command=calculate_ph).pack(pady=10)


def show_concentration_calculator():
    clear_inputs()
    conc_type_var.set("molar")

    tk.Label(input_frame, text="Выберите тип концентрации:").pack()

    types = [
        ("Молярная (Cм, моль/л)", "molar"),
        ("Нормальная (Cн, экв/л)", "normal"),
        ("Моляльная (Cm, моль/кг)", "molal"),
        ("Титр (T, г/мл)", "titer"),
        ("Мольная доля (χ)", "mole_fraction"),
    ]

    for text, conc_type in types:
        tk.Radiobutton(input_frame, text=text, variable=conc_type_var, value=conc_type).pack()

    tk.Button(input_frame, text="Далее →", command=setup_concentration_inputs).pack(pady=10)


def calculate_ph():
    clear_inputs()
    method = method_var.get()

    if method == "H+":
        tk.Label(input_frame, text="Введите [H⁺] (моль/л):").pack()
        entry = tk.Entry(input_frame)
        entry.pack()

        def compute():
            try:
                h_conc = float(entry.get())
                if h_conc <= 0:
                    show_error("Концентрация должна быть > 0!")
                    return
                ph = -log10(h_conc)
                show_result(f"pH = {ph:.2f}")
            except ValueError:
                show_error("Введите число!")

        tk.Button(input_frame, text="Рассчитать", command=compute).pack()

    elif method == "OH-":
        tk.Label(input_frame, text="Введите [OH⁻] (моль/л):").pack()
        entry = tk.Entry(input_frame)
        entry.pack()

        def compute():
            try:
                oh_conc = float(entry.get())
                if oh_conc <= 0:
                    show_error("Концентрация должна быть > 0!")
                    return
                poh = -log10(oh_conc)
                ph = 14 - poh
                show_result(f"pH = {ph:.2f}")
            except ValueError:
                show_error("Введите число!")

        tk.Button(input_frame, text="Рассчитать", command=compute).pack()

    elif method == "Ka":
        tk.Label(input_frame, text="Константа кислотности (Ka):").pack()
        ka_entry = tk.Entry(input_frame)
        ka_entry.pack()

        tk.Label(input_frame, text="Концентрация кислоты (моль/л):").pack()
        c_entry = tk.Entry(input_frame)
        c_entry.pack()

        def compute():
            try:
                ka = float(ka_entry.get())
                c = float(c_entry.get())
                if ka <= 0 or c <= 0:
                    show_error("Значения должны быть > 0!")
                    return
                h_conc = (ka * c) ** 0.5
                ph = -log10(h_conc)
                show_result(f"pH = {ph:.2f}")
            except ValueError:
                show_error("Введите числа!")

        tk.Button(input_frame, text="Рассчитать", command=compute).pack()


def setup_concentration_inputs():
    clear_inputs()
    conc_type = conc_type_var.get()

    if conc_type == "molar":
        tk.Label(input_frame, text="Количество вещества (моль):").pack()
        n_entry = tk.Entry(input_frame)
        n_entry.pack()

        tk.Label(input_frame, text="Объём раствора (л):").pack()
        v_entry = tk.Entry(input_frame)
        v_entry.pack()

        def compute():
            try:
                n = float(n_entry.get())
                v = float(v_entry.get())
                if v == 0:
                    show_error("Объём не может быть 0!")
                    return
                c = n / v
                show_result(f"Cм = {c:.4f} моль/л")
            except ValueError:
                show_error("Введите числа!")

        tk.Button(input_frame, text="Рассчитать", command=compute).pack()

    elif conc_type == "normal":
        tk.Label(input_frame, text="Количество эквивалентов (моль):").pack()
        n_entry = tk.Entry(input_frame)
        n_entry.pack()

        tk.Label(input_frame, text="Объём раствора (л):").pack()
        v_entry = tk.Entry(input_frame)
        v_entry.pack()

        def compute():
            try:
                n = float(n_entry.get())
                v = float(v_entry.get())
                if v == 0:
                    show_error("Объём не может быть 0!")
                    return
                cn = n / v
                show_result(f"Cн = {cn:.4f} экв/л")
            except ValueError:
                show_error("Введите числа!")

        tk.Button(input_frame, text="Рассчитать", command=compute).pack()

    elif conc_type == "molal":
        tk.Label(input_frame, text="Количество вещества (моль):").pack()
        n_entry = tk.Entry(input_frame)
        n_entry.pack()

        tk.Label(input_frame, text="Масса растворителя (кг):").pack()
        m_entry = tk.Entry(input_frame)
        m_entry.pack()

        def compute():
            try:
                n = float(n_entry.get())
                m = float(m_entry.get())
                if m == 0:
                    show_error("Масса не может быть 0!")
                    return
                b = n / m
                show_result(f"Cm = {b:.4f} моль/кг")
            except ValueError:
                show_error("Введите числа!")

        tk.Button(input_frame, text="Рассчитать", command=compute).pack()

    elif conc_type == "titer":
        tk.Label(input_frame, text="Масса вещества (г):").pack()
        m_entry = tk.Entry(input_frame)
        m_entry.pack()

        tk.Label(input_frame, text="Объём раствора (мл):").pack()
        v_entry = tk.Entry(input_frame)
        v_entry.pack()

        def compute():
            try:
                m = float(m_entry.get())
                v = float(v_entry.get())
                if v == 0:
                    show_error("Объём не может быть 0!")
                    return
                t = m / v
                show_result(f"T = {t:.4f} г/мл")
            except ValueError:
                show_error("Введите числа!")

        tk.Button(input_frame, text="Рассчитать", command=compute).pack()

    elif conc_type == "mole_fraction":
        tk.Label(input_frame, text="Количество вещества (моль):").pack()
        n_solute_entry = tk.Entry(input_frame)
        n_solute_entry.pack()

        tk.Label(input_frame, text="Количество растворителя (моль):").pack()
        n_solvent_entry = tk.Entry(input_frame)
        n_solvent_entry.pack()

        def compute():
            try:
                n_solute = float(n_solute_entry.get())
                n_solvent = float(n_solvent_entry.get())
                total = n_solute + n_solvent
                if total == 0:
                    show_error("Сумма количеств не может быть 0!")
                    return
                x = n_solute / total
                show_result(f"χ = {x:.4f}")
            except ValueError:
                show_error("Введите числа!")

        tk.Button(input_frame, text="Рассчитать", command=compute).pack()


def clear_inputs():
    for widget in input_frame.winfo_children():
        widget.destroy()
    result_label.config(text="")


def show_result(text):
    result_label.config(text=text)


def show_error(message):
    tk.messagebox.showerror("Ошибка", message)


# Основное окно
root = tk.Tk()
root.title("pH/Concentration Calculator")
root.geometry("500x500")

# Переменные
method_var = tk.StringVar(value="H+")
conc_type_var = tk.StringVar(value="molar")

# Главное меню
tk.Label(root, text="Выберите режим:", font=("Arial", 14)).pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

# Увеличиваем ширину кнопок
tk.Button(button_frame, text="Расчёт pH", command=show_ph_calculator, width=20).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Расчёт концентрации", command=show_concentration_calculator, width=20).pack(side=tk.LEFT,
                                                                                                          padx=10)

# Фрейм для ввода
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

# Фрейм для результата
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()