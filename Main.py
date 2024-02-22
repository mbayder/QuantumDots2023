import tkinter as tk
import math
import tkinter.messagebox
from PIL import Image, ImageTk
import numpy as np
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tensorflow
from tensorflow import keras
import molmass
from molmass import Formula
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Defining theme
customtkinter.set_default_color_theme("dark-blue")
model2 = keras.models.load_model('Network')




h = 6.62607015 * (10 ** -34)  # J*s
m0 = 9.1093837e-31 #kg
c = 299792458. #m / s
#Creating class
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__(fg_color="black")
        #Initialize window and some values
        self.title("Quantum Dots Simulation")
        self.active_button = None
        self.geometry(f"{1}x{1}")
        self.switch_state = "off"
        self.after(0, lambda: self.attributes("-fullscreen", True))
        self.slider_value = tk.StringVar(value='6.00')
        self.slider_value_display = tk.StringVar(value='6.00 nm')
        self.slider_value.trace_add('write', self.slider_value_changed)
        self.current_material = "CdS"
        self.wave_length = "NA"
        self.colour = "NA"
        self.hexcolour = "#ffffff"
        self.material_name = tk.StringVar(value="CdS")
        self.material_name.set(self.current_material)
        self.wave = tk.StringVar(value="NA")
        self.wave.set(self.wave_length)
        self.colour = tk.StringVar(value="NA")
        self.colour.set(self.wave_length)
        self.atomic_radius = 6.00
        self.energy_var = tk.StringVar()
        self.from_search_event = False
        self.color_label = customtkinter.CTkLabel(self, textvariable=self.colour)
        #Configure the rows & columns
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        #Create the sidebars
        self.sidebar_frame = customtkinter.CTkFrame(self, width=250, fg_color="#111112", corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)  # Allow the column to expand
        #Create top label
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Quantum Dots", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))


        tiny_image = Image.open("images/Logo.png")
        tiny_image = tiny_image.resize((55, 55))
        tiny_photo_image = ImageTk.PhotoImage(tiny_image)
        self.tiny_image_label = customtkinter.CTkLabel(self.sidebar_frame, image=tiny_photo_image, width=10, height=10, text="")
        self.tiny_image_label.image = tiny_photo_image
        self.tiny_image_label.grid(row=0, column=0, sticky="w", padx=(20,0), pady=(5,0))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,
                                                        text="Quantum Dot (QD)",
                                                        command=self.sidebar_button_event,
                                                        fg_color="#383735",
                                                        hover_color="gray",
                                                        font=customtkinter.CTkFont(size=25, weight="bold"),
                                                        width=250,
                                                        height=50)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,
                                                        text= "QD Energy Diagram",
                                                        command=self.sidebar_button_event2,
                                                        fg_color="#383735",
                                                        font=customtkinter.CTkFont(size=25, weight="bold"),
                                                        hover_color="gray",
                                                        width=250,
                                                        height=50)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.search_entry = customtkinter.CTkEntry(self.sidebar_frame,

                                                   placeholder_text="Enter your compound...",
                                                   width=200,
                                                   height=30)
        self.search_entry.grid(row=3, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.search_button = customtkinter.CTkButton(self.sidebar_frame,
                                                     text="Find Compound",
                                                     command=self.search_event,
                                                     font=customtkinter.CTkFont(size=18, weight="bold"),
                                                     fg_color="#383735",
                                                     hover_color="gray",
                                                     width=200,
                                                     height=30)
        self.search_button.grid(row=4, column=0, padx=20, pady=(5, 10), sticky="ew")

        #Create top label of slider, slider & tracking slider value
        self.slider_label_top = customtkinter.CTkLabel(self.sidebar_frame,
                                                       text="QD Radius",
                                                       font=customtkinter.CTkFont(size=12, weight="bold"),
                                                       fg_color="#111112",
                                                       text_color="#ffffff")
        self.slider_label_top.grid(row=4, column=0, padx=(30, 0), pady=(60, 0), sticky="wn"
                                   )
        self.slider = customtkinter.CTkSlider(self.sidebar_frame,
                                              from_=1,
                                              to=8,
                                              command=self.slider_event,
                                              orientation="vertical",
                                              width=28,
                                              height=500)
        self.slider.grid(row=5, column=0, pady=(0,75), padx=(0,160), sticky="ns")
        self.slider_label_bottom = customtkinter.CTkLabel(self.sidebar_frame,
                                                          textvariable=self.slider_value_display,
                                                          fg_color="transparent",
                                                          text_color="#ffffff",
                                                          font=customtkinter.CTkFont(size=18, weight="bold"))
        self.sidebar_frame.grid_rowconfigure(6, weight=0)
        self.slider_label_bottom.grid(row=5, column=0, padx=(0, 159), pady=(470, 0),
                                   )

        # Side buttons

        #Define images
        CdS = ImageTk.PhotoImage(Image.open("images/CdS.png").resize((100,100),))
        CdSe = ImageTk.PhotoImage(Image.open("images/CdSe.png").resize((100,100),))
        GaAs = ImageTk.PhotoImage(Image.open("images/GaAs.png").resize((100,100),))
        Ge = ImageTk.PhotoImage(Image.open("images/Ge.png").resize((100,100),))
        InAs = ImageTk.PhotoImage(Image.open("images/InAs.png").resize((100,100),))
        Si = ImageTk.PhotoImage(Image.open("images/Si.png").resize((100, 100), ))
        self.sidebar_button_CdS = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="",
                                                             command=self.set_material_CdS,
                                                             fg_color="#383735",
                                                             hover_color="gray",
                                                             image=CdS,
                                                             compound = 'bottom',
                                                             width=150,
                                                             height=30)

        self.sidebar_button_CdS.grid(row=5, column=0, padx=(110,0), sticky="nw")
        self.sidebar_button_CdSe = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="",
                                                             command=self.set_material_CdSe,
                                                             fg_color="#383735",
                                                             hover_color="gray",
                                                             image=CdSe,
                                                             compound='bottom',
                                                             width=150,
                                                             height=30)

        self.sidebar_button_CdSe.grid(row=5, column=0, padx=(110, 0), pady=(120, 0), sticky="nw")
        self.sidebar_button_GaAs = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="",
                                                             command=self.set_material_GaAs,
                                                             fg_color="#383735",
                                                             hover_color="gray",
                                                             image=GaAs,
                                                             compound='bottom',
                                                             width=150,
                                                             height=30)
        self.sidebar_button_GaAs.grid(row=5, column=0, padx=(110, 0), pady=(240, 0), sticky="nw")
        self.sidebar_button_Ge = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="",
                                                             command=self.set_material_Ge,
                                                             fg_color="#383735",
                                                             hover_color="gray",
                                                             image=Ge,
                                                             compound='bottom',
                                                             width=150,
                                                             height=30)
        self.sidebar_button_Ge.grid(row=5, column=0, padx=(110, 0), pady=(360, 0), sticky="nw")
        self.sidebar_button_InAs = customtkinter.CTkButton(self.sidebar_frame,
                                                             text="",
                                                             command=self.set_material_InAs,
                                                             fg_color="#383735",
                                                             hover_color="gray",
                                                             image=InAs,
                                                             compound='bottom',
                                                             width=150,
                                                             height=30)
        self.sidebar_button_InAs.grid(row=5, column=0, padx=(110, 0), pady=(480, 0), sticky="nw")

    def slider_event(self, value):
        rounded_value = round(float(value), 3)
        self.slider_value.set(rounded_value)
        self.atomic_radius = rounded_value
        self.slider_value_display.set(f"{rounded_value} nm")
        self.update_energy_label()

    def search_event(self):
        self.active_button = None
        self.from_search_event = True
        self.reset_sidebar_button_colors()
        self.slider_value_changed()

    def update_energy_label(self):
        energy = self.dot_energy(self.current_material, self.atomic_radius)
        energy = round(float(energy), 22)
        self.energy_var.set(f"{energy}J")

    def reset_sidebar_button_colors(self):
        buttons = [self.sidebar_button_1, self.sidebar_button_2, self.sidebar_button_CdS, self.sidebar_button_CdSe,
                   self.sidebar_button_GaAs, self.sidebar_button_Ge, self.sidebar_button_InAs]
        for button in buttons:
            button.configure(fg_color="#383735")






    def change_button_color(self, button, color):
        button.configure(fg_color=color)

    def dot_energy_general(self, material, inf_array, r):
        E_bg = inf_array[0][2]
        me_m0 = inf_array[0][1]
        mh_m0 = inf_array[0][0]

        if material == "CdS":
            E_bg = 2.42
            me_m0 = 0.21
            mh_m0 = 0.8
            m_e = me_m0 * m0
            m_h = mh_m0 * m0
            radius = r * 10 ** -9
            E_dot = (E_bg / 6.242e+18) + (h ** 2 / (8 * radius ** 2)) * (1 / m_e + 1 / m_h)
            return E_dot
        if material == "CdSe":
            E_bg = 1.73
            me_m0 = 0.13
            mh_m0 = 0.45
            m_e = me_m0 * m0
            m_h = mh_m0 * m0
            radius = r * 10 ** -9
            E_dot = (E_bg / 6.242e+18) + (h ** 2 / (8 * radius ** 2)) * (1 / m_e + 1 / m_h)
            return E_dot
        if material == "GaAs":
            E_bg = 1.42
            me_m0 = 0.067
            mh_m0 = 0.082
            m_e = me_m0 * m0
            m_h = mh_m0 * m0
            radius = r * 10 ** -9
            E_dot = (E_bg / 6.242e+18) + (h ** 2 / (8 * radius ** 2)) * (1 / m_e + 1 / m_h)
            return E_dot
        if material == "InAs":
            E_bg = 0.36
            me_m0 = 0.023
            mh_m0 = 0.4
            m_e = me_m0 * m0
            m_h = mh_m0 * m0
            radius = r * 10 ** -9
            E_dot = (E_bg / 6.242e+18) + (h ** 2 / (8 * radius ** 2)) * (1 / m_e + 1 / m_h)
            return E_dot
        if material == "Si":
            E_bg = 1.11
            me_m0 = 0.19
            mh_m0 = 0.49
            m_e = me_m0 * m0
            m_h = mh_m0 * m0
            radius = r * 10 ** -9
            E_dot = (E_bg / 6.242e+18) + (h ** 2 / (8 * radius ** 2)) * (1 / m_e + 1 / m_h)
            return E_dot
        if material == "Ge":
            E_bg = 0.67
            me_m0 = 0.082
            mh_m0 = 0.28
            m_e = me_m0 * m0
            m_h = mh_m0 * m0
            radius = r * 10 ** -9
            E_dot = (E_bg / 6.242e+18) + (h ** 2 / (8 * radius ** 2)) * (1 / m_e + 1 / m_h)
            return E_dot
        else:
            if E_bg < 0.1 or E_bg > 6.5:
                return False
            elif me_m0 < 0.01 or me_m0 > 10:
                return False
            elif mh_m0 < 0.01 or mh_m0 > 10:
                return False
            else:
                m_e = me_m0 * m0
                m_h = mh_m0 * m0
                radius = r * 10 ** -9
                E_dot = (E_bg / 6.242e+18) + (h ** 2 / (8 * radius ** 2)) * (1 / m_e + 1 / m_h)
                return E_dot

    def set_material_CdS(self):
        self.from_search_event = False
        self.current_material = "CdS"
        self.slider_value_changed()
        print(self.current_material)
        self.handle_button_click(self.sidebar_button_CdS)
        self.update_energy_label()

    def set_material_CdSe(self):
        self.from_search_event = False
        self.current_material = "CdSe"
        self.slider_value_changed()
        print(self.current_material)
        self.handle_button_click(self.sidebar_button_CdSe)
        self.update_energy_label()


    def set_material_GaAs(self):
        self.from_search_event = False
        self.current_material = "GaAs"
        self.slider_value_changed()
        print(self.current_material)
        self.handle_button_click(self.sidebar_button_GaAs)
        self.update_energy_label()

    def set_material_Ge(self):
        self.from_search_event = False
        self.current_material = "Ge"
        self.slider_value_changed()
        print(self.current_material)
        self.handle_button_click(self.sidebar_button_Ge)
        self.update_energy_label()

    def set_material_InAs(self):
        self.from_search_event = False
        self.current_material = "InAs"
        self.slider_value_changed()
        print(self.current_material)
        self.handle_button_click(self.sidebar_button_InAs)
        self.update_energy_label()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def new_button_event(self):
        print("New Button Clicked")

    def sidebar_button_event(self):
        print("sidebar_button click")
        self.sidebar_button_1.configure(command=lambda: self.sidebar_button_event(1))

    def sidebar_button_event2(self):
        print("sidebar_button click")
        self.sidebar_button_2.configure(command=lambda: self.sidebar_button_event(2))
        self.slider_value_changed()


    def setup_pages(self):
        # Create frames for each page
        self.page1 = customtkinter.CTkFrame(self, fg_color="#000000")
        self.page2 = customtkinter.CTkFrame(self, fg_color="#000000")
        image = Image.open("images/dot.png")  # Change "dot.jpg" to the actual image file path
        image = image.convert("RGBA")
        r2 = 255
        g2 = 255
        b2 = 255
        color = (r2, g2, b2, 255)
        brus = ImageTk.PhotoImage(Image.open("images/Brus Eqn.png").resize((600, 100)))
        formula = customtkinter.CTkLabel(self.page2, text="", image=brus)
        formula.place(x=300, y=550)
        equal = ImageTk.PhotoImage(Image.open("images/equal sign.png").resize((20, 20)))
        sign = customtkinter.CTkLabel(self.page2, text="", image=equal)
        sign.place(x=600, y=700)
        bond_e = customtkinter.CTkLabel(self.page2, textvariable=self.energy_var)
        custom_font = customtkinter.CTkFont(size=60, weight="bold")
        bond_e.configure(font=custom_font)
        bond_e.place(x=400, y=770)
        Wavelength = ImageTk.PhotoImage(Image.open("images/_Wavelength_.png").resize((300, 100)))
        WavelengthTitle = customtkinter.CTkLabel(self.page1, text="", image=Wavelength)
        WavelengthTitle.place(x=800,y=80, anchor="center")
        Wavelength = ImageTk.PhotoImage(Image.open("images/Wavelength-Equation.png").resize((220, 100)))
        WavelengthTitle = customtkinter.CTkLabel(self.page1, text="", image=Wavelength)
        WavelengthTitle.place(x=700, y=200, anchor="center")
        self.WaveR = customtkinter.CTkLabel(self.page1, text="", textvariable=self.wave, text_color="#ffffff",
                                       font=customtkinter.CTkFont(size=40, weight="bold"))
        self.WaveR.place(x=900, y=200, anchor="center")
        self.ColourWord = customtkinter.CTkLabel(self.page1, textvariable=self.colour,text_color=self.hexcolour,
                                       font=customtkinter.CTkFont(size=40, weight="bold"))
        self.ColourWord.place(x=800, y=300, anchor="center")
        Plank = ImageTk.PhotoImage(Image.open("images/_h- Plank Constant_.png").resize((300, 40)))
        PlankTitle = customtkinter.CTkLabel(self.page1, text="", image=Plank)
        PlankTitle.place(x=800, y=370, anchor="center")
        C = ImageTk.PhotoImage(Image.open("images/c- speed of light.png").resize((300, 45)))
        CT = customtkinter.CTkLabel(self.page1, text="", image=C)
        CT.place(x=800, y=450, anchor="center")






        for x in range(image.width):
            for y in range(image.height):
                r, g, b, a = image.getpixel((x, y))
                if r != 0 or g != 0 or b != 0:  # Check if the pixel is white
                    image.putpixel((x, y), color)

        image.save("images/dot.png")
        self.flask_photo_image = ImageTk.PhotoImage(image)

        self.image_label = customtkinter.CTkLabel(self.page1, image=self.flask_photo_image, text='')

        self.image_label.pack(anchor='w')
        self.Labal = customtkinter.CTkLabel(self.page1, text="", textvariable=self.material_name, text_color=self.hexcolour,
                                       font=customtkinter.CTkFont(size=30, weight="bold"))
        self.Labal.place(x=232, y=44, anchor="center")


        #Old code, no longer in use.
        '''image = Image.open("flash.png").resize((150,300), Image.Resampling.LANCZOS)
        light = ImageTk.PhotoImage(image)
        image_label = customtkinter.CTkLabel(self.page1, image=light, text='')
        image_label.pack(anchor='sw', padx="144", pady=(0,0))
        # image 3
        image = Image.open("light.png").resize((150, 300), Image.Resampling.LANCZOS)
        flash = ImageTk.PhotoImage(image)
        image_label = customtkinter.CTkLabel(self.page1, image=flash, text='')
        image_label.pack(anchor='sw', padx="144", pady=(0, 0))'''



    def handle_button_click(self, clicked_button):
        if self.active_button is not None:
            self.active_button.configure(fg_color="#383735")  # Set this to your default button color
        clicked_button.configure(fg_color="gray")
        self.active_button = clicked_button

    def add_switch_for_light(self):

        flash_image = Image.open("images/flash.png").resize((150, 300), Image.Resampling.LANCZOS)
        light_image = Image.open("images/light.png").resize((150, 300), Image.Resampling.LANCZOS)
        switch_var = customtkinter.StringVar(value="off")

        flash_ctk_image = ImageTk.PhotoImage(image=flash_image)
        light_ctk_image = ImageTk.PhotoImage(image=light_image)
        flash = customtkinter.CTkLabel(self.page1, text="", image=flash_ctk_image)
        light = customtkinter.CTkLabel(self.page1, text="", image=light_ctk_image)
        flash.pack(anchor='sw', padx="144", pady=(0, 0))
        def switch_event():
            self.switch_state = switch_var.get()
            if switch_var.get() == "on":
                light.pack(anchor='sw', padx="144", pady=(0,0))
                flash.pack_forget()

            if switch_var.get() == "on":

                light.pack(anchor='sw', padx="144", pady=(0, 0))

                flash.pack_forget()

                self.update_flask_image()

            elif switch_var.get() == "off":
                self.wave.set("NA")
                self.colour.set("NA")
                self.hexcolour = "#ffffff"
                self.ColourWord.configure(text_color=self.hexcolour)
                self.Labal.configure(text_color=self.hexcolour)
                flash.pack(anchor='sw', padx="144", pady=(0, 0))

                light.pack_forget()

                self.set_flask_white()


        switch = customtkinter.CTkSwitch(self.page1, text="Red/UV Lightswitch", command=switch_event, variable=switch_var, onvalue="on",
                                         offvalue="off")
        switch.place(x=0, y=850)













        # Place frames on top of each other
        self.page1.grid(row=0, column=1, sticky="nsew")
        self.page2.grid(row=0, column=1, sticky="nsew")

        # Initially raise page 1 to the top
        self.page1.lift()

    def show_page(self, page):
        page.lift()
        if page == self.page2:
            self.update_energy_label()
            self.display_functions_one_by_one()

    def func1(self):
        plt.close()
        fig, ax = plt.subplots()
        fig.set_facecolor("black")
        #   ax.set_ylim(-5, 5)
        r = self.atomic_radius

        X = np.arange(0.0, 10.0)

        #    plt.figure(facecolor='black', figsize=(14.0,10.0)) #change figure size

        line_count = 0.0  # initialize
        E_lvl = self.Band(self.current_material, self.atomic_radius) / 2

        def graph_two_vertical_lines_first(x, E_lvl):
            plt.plot(x, np.full(X.shape, E_lvl), color='orange')  # colors changeable
            plt.plot(x, np.full(X.shape, - E_lvl), color='red')

        def graph_two_vertical_lines(x, E_lvl):
            plt.plot(x, np.full(X.shape, E_lvl), color='orange')  # colors changeable
            plt.plot(x, np.full(X.shape, - E_lvl), color='red')
            plt.scatter(6.0, - E_lvl, s=100, color='yellow')
            plt.scatter(3.0, - E_lvl, s=100, color='yellow')

        plt.annotate('Valence Band', (8.0, - self.Band(self.current_material, self.atomic_radius) / 2 - 0.4),
                     color="red")
        plt.annotate('Conduction Band', (8.0, self.Band(self.current_material, self.atomic_radius) / 2 + 0.2),
                     color="orange")

        if line_count == 0.0:
            graph_two_vertical_lines_first(X, E_lvl)
            line_count += 1
            E_lvl += (10 - self.Band(self.current_material, self.atomic_radius)) / r * (1 / 1.2 ** (-line_count))

        while line_count >= 0.0 and line_count <= r:
            graph_two_vertical_lines(X, E_lvl)
            line_count += 1
            E_lvl += (10 - self.Band(self.current_material, self.atomic_radius)) / r * (1 / 1.2 ** (-line_count))  # tbc

        plt.axis('off')
        plt.ylim(-5, 5)

        plt.scatter(4.5, - self.Band(self.current_material, self.atomic_radius) / 2, s=100, color='yellow')
        plt.annotate('Electron', (4.65, - self.Band(self.current_material, self.atomic_radius) / 2 + 0.2),
                     color="yellow")

        x_wave = np.arange(0.0, 4.3, 0.05)
        plt.plot(x_wave,
                 0.4 * np.sin(6 * x_wave) - (self.Band(self.current_material, self.atomic_radius) / 10) * x_wave,
                 label='UV', color='royalblue')
        plt.annotate('UV Light', (2.0, - self.Band(self.current_material, self.atomic_radius) / 2 + 0.2), color="aqua")

        canvas = FigureCanvasTkAgg(fig, master=self.page2)
        canvas.get_tk_widget().place(x=50, y=50)

    def func2(self):
        plt.close()

        fig, ax = plt.subplots()
        fig.set_facecolor("black")
        E_bg = self.Band(self.current_material, self.atomic_radius)

        X = np.arange(0.0, 10.0)
        r = self.atomic_radius

        #    plt.figure(facecolor='black', figsize=(14.0,10.0)) #change figure size

        line_count = 0.0  # initialize
        E_lvl = E_bg / 2

        def graph_two_vertical_lines_first(x, E_lvl):
            plt.plot(x, np.full(X.shape, E_lvl), color='orange')  # colors changeable
            plt.plot(x, np.full(X.shape, - E_lvl), color='red', alpha=0.3)

        def graph_two_vertical_lines(x, E_lvl):
            plt.plot(x, np.full(X.shape, E_lvl), color='orange')  # colors changeable
            plt.plot(x, np.full(X.shape, - E_lvl), color='red')
            plt.scatter(6.0, - E_lvl, s=100, color='yellow')
            plt.scatter(3.0, - E_lvl, s=100, color='yellow')

        plt.annotate('Valence Band', (8.0, - self.Band(self.current_material, self.atomic_radius) / 2 - 0.4),
                     color="red")
        plt.annotate('Conduction Band', (8.0, self.Band(self.current_material, self.atomic_radius) / 2 + 0.2),
                     color="orange")

        if line_count == 0.0:
            graph_two_vertical_lines_first(X, E_lvl)
            line_count += 1
            E_lvl += (10 - self.Band(self.current_material, self.atomic_radius)) / r * (1 / 1.2 ** (-line_count))

        while line_count >= 0.0 and line_count <= r:
            graph_two_vertical_lines(X, E_lvl)
            line_count += 1
            E_lvl += (10 - self.Band(self.current_material, self.atomic_radius)) / r * (1 / 1.2 ** (-line_count))  # tbc

        plt.axis('off')
        plt.ylim(-5, 5)

        plt.scatter(4.5, self.Band(self.current_material, self.atomic_radius) / 2, s=100, color='yellow')
        plt.annotate('Electron', (4.65, self.Band(self.current_material, self.atomic_radius) / 2 + 0.2), color="yellow")

        canvas = FigureCanvasTkAgg(fig, master=self.page2)
        canvas.get_tk_widget().place(x=50, y=50)


    def func3(self):
        plt.close()
        fig, ax = plt.subplots()
        fig.set_facecolor("black")
        #   ax.set_ylim(-5, 5)

        X = np.arange(0.0, 10.0)
        r = self.atomic_radius

        #    plt.figure(facecolor='black', figsize=(14.0,10.0)) #change figure size

        line_count = 0.0  # initialize
        E_lvl = self.Band(self.current_material, self.atomic_radius) / 2

        def graph_two_vertical_lines_first(x, E_lvl):
            plt.plot(x, np.full(X.shape, E_lvl), color='orange')  # colors changeable
            plt.plot(x, np.full(X.shape, - E_lvl), color='red')  # colors changeable

        def graph_two_vertical_lines(x, E_lvl):
            plt.plot(x, np.full(X.shape, E_lvl), color='orange')  # colors changeable
            plt.plot(x, np.full(X.shape, - E_lvl), color='red')
            plt.scatter(6.0, - E_lvl, s=100, color='yellow')
            plt.scatter(3.0, - E_lvl, s=100, color='yellow')

        plt.annotate('Valence Band', (8.0, - self.Band(self.current_material, self.atomic_radius) / 2 - 0.4),
                     color="red")
        plt.annotate('Conduction Band', (8.0, self.Band(self.current_material, self.atomic_radius) / 2 + 0.2),
                     color="orange")

        if line_count == 0.0:
            graph_two_vertical_lines_first(X, E_lvl)
            line_count += 1
            E_lvl += (10 - self.Band(self.current_material, self.atomic_radius)) / r * (1 / 1.2 ** (-line_count))

        while line_count >= 0.0 and line_count <= r:
            graph_two_vertical_lines(X, E_lvl)
            line_count += 1
            E_lvl += (10 - self.Band(self.current_material, self.atomic_radius)) / r * (1 / 1.2 ** (-line_count))  # tbc

        #  plt.axis('off')
        plt.axis('off')
        plt.ylim(-5, 5)

        plt.scatter(4.5, - self.Band(self.current_material, self.atomic_radius) / 2, s=100, color='yellow')
        plt.annotate('Electron', (4.65, - self.Band(self.current_material, self.atomic_radius) / 2 + 0.2),
                     color="yellow")

        x_wave = np.arange(5.5, 8.7, 0.05)
        plt.plot(x_wave, 0.4 * np.sin(7 * x_wave), color='white')
        plt.annotate('Emits Photon', (8.8, 0.0), color='white')
        canvas = FigureCanvasTkAgg(fig, master=self.page2)
        canvas.get_tk_widget().place(x=50, y=50)
        self.after(1500, self.display_functions_one_by_one)


    def display_functions_one_by_one(self):

        self.func1()

        self.after(500, self.func2)  # Schedule func2 to run 0.5 seconds (500 milliseconds) after func1

        self.after(1000, self.func3)  # Schedule func3 to run 1 second (1000 milliseconds) after func


    def set_flask_white(self):
        image_path = "images/dot.png"  # Updated path to the uploaded image
        image = Image.open(image_path)  # Change "dot.jpg" to the actual image file path
        image = image.convert("RGBA")
        data = np.array(image)
        # Set all non-black pixels to the new color
        non_black_pixels_mask = np.any(data[:, :, :3] != 0, axis=-1)
        data[non_black_pixels_mask] = [255, 255, 255, 255]  # Use the new color
        new_image = Image.fromarray(data)

        # Now create a PhotoImage from the new_image
        self.flask_photo_image = ImageTk.PhotoImage(new_image)

        # Refresh the label that displays the image
        self.image_label.configure(image=self.flask_photo_image)

        # Keep a reference to avoid garbage collection
        self.image_label.image = self.flask_photo_image


    def update_flask_image(self):
        # This method should be called to update the flask image based on the slider value
        self.slider_value_changed()


    def sidebar_button_event(self, page_number):
        print(f"Sidebar button {page_number} clicked")
        if page_number == 1:
            self.show_page(self.page1)
        elif page_number == 2:
            self.show_page(self.page2)
        elif page_number == 3:
            self.show_page(self.page3)

    def Band(self, material, r):
        E_bg = 0  # eV
        # me_m0 = 1  # relative - no units
        # mh_m0 = 1  # relative - no units

        if material == "CdS":
            E_bg = 2.42  # eV
            # me_m0 = 0.21  # relative - no units
            # mh_m0 = 0.8  # relative - no units
        if material == "CdSe":
            E_bg = 1.73  # eV
            # me_m0 = 0.13  # relative - no units
            # mh_m0 = 0.45  # relative - no units
        if material == "GaAs":
            E_bg = 1.42  # eV
            # me_m0 = 0.067  # relative - no units
            # mh_m0 = 0.082  # relative - no units
        if material == "InAs":
            E_bg = 0.36  # eV
            # me_m0 = 0.023  # relative - no units
            # mh_m0 = 0.4  # relative - no units
        if material == "Si":
            E_bg = 1.11  # eV
            # me_m0 = 0.19  # relative - no units
            # mh_m0 = 0.49  # relative - no units
        if material == "Ge":
            E_bg = 0.67  # eV
            # me_m0 = 0.082  # relative - no units
            # mh_m0 = 0.28  # relative - no units

        # Effective masses of electron and hole (in kg)
        # m_e = me_m0 * m0
        # m_h = mh_m0 * m0
        # Converting radius to meters
        # radius = r * 10 ** -9

        return E_bg

    def dot_energy(self, material, r):
        E_bg = 0  # eV
        me_m0 = 1  # relative - no units
        mh_m0 = 1  # relative - no units

        if material == "CdS":
            E_bg = 2.42  # eV
            me_m0 = 0.21  # relative - no units
            mh_m0 = 0.8  # relative - no units
        if material == "CdSe":
            E_bg = 1.73  # eV
            me_m0 = 0.13  # relative - no units
            mh_m0 = 0.45  # relative - no units
        if material == "GaAs":
            E_bg = 1.42  # eV
            me_m0 = 0.067  # relative - no units
            mh_m0 = 0.082  # relative - no units
        if material == "InAs":
            E_bg = 0.36  # eV
            me_m0 = 0.023  # relative - no units
            mh_m0 = 0.4  # relative - no units
        if material == "Si":
            E_bg = 1.11  # eV
            me_m0 = 0.19  # relative - no units
            mh_m0 = 0.49  # relative - no units
        if material == "Ge":
            E_bg = 0.67  # eV
            me_m0 = 0.082  # relative - no units
            mh_m0 = 0.28  # relative - no units

        # Effective masses of electron and hole (in kg)
        m_e = me_m0 * m0
        m_h = mh_m0 * m0
        # Converting radius to meters
        radius = r * 10 ** -9

        # Brus equation for quantum dots (in J)
        E_dot = (E_bg / 6.242e+18) + (h ** 2 / (8 * radius ** 2)) * (1 / m_e + 1 / m_h)

        return E_dot

    def wavelength(self, dot_e):
        return int(((h * c) / dot_e) * (10 ** 9))

    def written_colour(self, wavelen):
        if wavelen > 781:
            return "Infrared - Not visible"
        if 625 < wavelen <= 781:
            return "Red"
        if 590 < wavelen <= 625:
            return "Orange"
        if 565 < wavelen <= 590:
            return "Yellow"
        if 500 < wavelen <= 565:
            return "Green"
        if 485 < wavelen <= 500:
            return "Cyan"
        if 450 < wavelen <= 485:
            return "Blue"
        if 380 < wavelen <= 450:
            return "Violet"
        else:
            return "Ultraviolet - Not visible"

    # Determining what colour is quantum dot emitting:

    def rgbhex(self, rgb_tuple):
        def toHex(number):
            hexa = str(hex(number)).replace("0x", "")
            if len(hexa) < 2:
                hexa = "0" + hexa
            return hexa

        hexstring = '#'
        for x in range(len(rgb_tuple)):
            hexstring += toHex((rgb_tuple[x]))

        return hexstring

    def dot_colour(self, wavelen):
        gamma = 0.8
        IntensityMax = 255
        if 380 <= wavelen < 440:
            red = -(wavelen - 440) / (440 - 380)
            green = 0.0
            blue = 1.0
        elif 440 <= wavelen < 490:
            red = 0.0
            green = (wavelen - 440) / (490 - 440)
            blue = 1.0
        elif 490 <= wavelen < 510:
            red = 0.0
            green = 1.0
            blue = -(wavelen - 510) / (510 - 490)
        elif 510 <= wavelen < 580:
            red = (wavelen - 510) / (580 - 510)
            green = 1.0
            blue = 0.0
        elif 580 <= wavelen < 645:
            red = 1.0
            green = -(wavelen - 645) / (645 - 580)
            blue = 0.0
        elif 645 <= wavelen < 781:
            red = 1.0
            green = 0.0
            blue = 0.0
        else:
            red = 0.0
            green = 0.0
            blue = 0.0

        if 380 <= wavelen < 420:
            factor = 0.3 + 0.7 * (wavelen - 380) / (420 - 380)
        elif 420 <= wavelen < 701:
            factor = 1.0
        elif 701 <= wavelen < 781:
            factor = 0.3 + 0.7 * (780 - wavelen) / (780 - 700)
        else:
            factor = 0.0
        if red != 0:
            red = round((IntensityMax * (red * factor) ** gamma))
        if green != 0:
            green = round((IntensityMax * (green * factor) ** gamma))
        if blue != 0:
            blue = round((IntensityMax * (blue * factor) ** gamma))

        if wavelen < 380:
            red = 118
            green = 91
            blue = 255
        if wavelen > 781:
            red = 134
            green = 19
            blue = 19

        return int(red), int(green), int(blue)


    def slider_value_changed(self, *args):
        # ... your code for calculations ...
        if self.switch_state == "on":
            # This function will be called whenever the slider_value changes
            new_value = self.slider_value.get()
            self.atomic_radius = float(new_value)
            if self.from_search_event:
                self.material_name.set(self.search_entry.get())
                x = self.search_entry.get()

                molecule = Formula(x)
                input_to_neuralnet = [molecule.isotope.mass]
                model = model2.predict(input_to_neuralnet)
                print(model)
                print(x)
                print(input_to_neuralnet)
                energy = self.dot_energy_general(x, model, self.atomic_radius)
                self.wave_length = self.wavelength(energy)
                self.wave.set(f"{self.wave_length} nm")
                current_colour = self.written_colour(self.wave_length)
                self.colour.set(current_colour)



            else:
                self.material_name.set(self.current_material)
                energy = self.dot_energy(self.current_material, self.atomic_radius)
            self.wave_length = self.wavelength(energy)
            self.wave.set(f"{self.wave_length} nm")
            current_colour = self.written_colour(self.wave_length)
            self.colour.set(current_colour)
            dot_colour = self.dot_colour(self.wave_length)

            r2, g2, b2 = dot_colour
            self.hexcolour = self.rgbhex(dot_colour)
            self.ColourWord.configure(text_color=self.hexcolour)
            self.Labal.configure(text_color=self.hexcolour)

            # Now we directly create a PhotoImage from the altered image data
            image_path = "images/dot.png"  # Updated path to the uploaded image
            image = Image.open(image_path)  # Change "dot.jpg" to the actual image file path
            image = image.convert("RGBA")
            data = np.array(image)
            # Set all non-black pixels to the new color
            non_black_pixels_mask = np.any(data[:, :, :3] != 0, axis=-1)
            data[non_black_pixels_mask] = [r2, g2, b2, 255]  # Use the new color
            new_image = Image.fromarray(data)

            # Now create a PhotoImage from the new_image
            self.flask_photo_image = ImageTk.PhotoImage(new_image)

            # Refresh the label that displays the image
            self.image_label.configure(image=self.flask_photo_image)

            # Keep a reference to avoid garbage collection
            self.image_label.image = self.flask_photo_image

        else:
            self.wave.set("NA")
            self.colour.set("NA")
            if self.from_search_event:
                self.material_name.set(self.search_entry.get())
            else:
                self.material_name.set(self.current_material)



if __name__ == "__main__":
    app = App()
    app.setup_pages()
    app.sidebar_button_1.configure(command=lambda: app.sidebar_button_event(1))
    app.sidebar_button_2.configure(command=lambda: app.sidebar_button_event(2))
    app.add_switch_for_light()
    app.mainloop()
