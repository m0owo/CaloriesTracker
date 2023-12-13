from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import *
from tkcalendar import *
from datetime import date
from tkmacosx import *
import pickle
import os
import turtle as t
from PIL import Image, ImageTk
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'


class MealAlreadyInIndex(Exception):
    pass
class PositiveNumbersOnly(Exception):
    pass
class NoGoal(Exception):
    pass
class EmptyBox(Exception):
    pass
class NumbersOnly(Exception):
    pass
class LettersOnly(Exception):
    pass

class BMR:
    def __init__(self, age, weight, height, gender):
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
    def calculate_BMR(self):
        self.base = (10.0 * self.weight) + ((6.25 * self.height) - (5.0 * self.age))
        if self.gender == "male":
            return self.base + 5
        elif self.gender == "female":
            return self.base - 161

class CalorieGoal(BMR):
    def __init__(self, age, weight, height, gender, objective):
        super().__init__(age, weight, height, gender)
        self.objective = objective

    def calculate_calorie_goal(self):
        if self.objective == "gain":
            return (super().calculate_BMR() * 1.2) + 500.0
        elif self.objective == "lose":
            return (super().calculate_BMR() * 1.2) - 500.0
        elif self.objective == "maintain":
            return super().calculate_BMR() * 1.2

class CalorieProgram:
    def __init__(self):
        #formatting
        self.window1 = Tk()
        self.window1.config(bg = "#fcf4dd")
        self.window1.title("My Progress")
        self.window1.geometry("800x800")
        self.window1.resizable(False, False)
        style = ttk.Style(self.window1)
        style.theme_use('clam') 
        self.window1.option_add( "*Font", "TimesNewRoman 14" )

        #frame for saving, loading, and resetting progress
        self.load_save_progress_frame = Frame(self.window1, bg = "#fcf4dd")
        self.load_save_progress_frame.pack(side = TOP, pady = 10)
        self.load_progress_button = Button(
                                    self.load_save_progress_frame, borderless = True, text = "Load Progress", 
                                    command = self.load_progress, activebackground= "#ddedea", activeforeground= 'black',
                                    font= "TimesNewRoman 14", bg = 'white')
        self.load_progress_button.pack(side = LEFT, fill= X, padx = 10)
        self.reset_progress_button = Button(
                                    self.load_save_progress_frame, activebackground= "#ddedea", activeforeground= 'black', 
                                    borderless = True, text = "Reset Progress", command = self.reset_progress,
                                    font= "TimesNewRoman 14", bg = 'white')
        self.reset_progress_button.pack(side = LEFT, fill = X, padx = (0,10))
        self.save_progress_button = Button(
                                    self.load_save_progress_frame, borderless = True, text = "Save Progress", 
                                    command = self.save_progress, font= "TimesNewRoman 14", bg = 'white',
                                    activebackground= "#ddedea", activeforeground= 'black')
        self.save_progress_button.pack(side = LEFT, fill = X, padx = (0,10))

        #frame for calendar
        self.calendar_frame = Frame(self.window1, bg = "#fcf4dd")
        self.calendar_frame.pack(expand = True, fill = BOTH, pady = (0, 10))
        today = date.today()
        self.cal = Calendar(
                        self.calendar_frame, background = 'black', borderless = True, selectmode = 'day', year = today.year,
                        month = today.month, day = today.day, font = "TimesNewRoman 16 bold", showweeknumbers = False, locale="en_US")
        self.cal.pack(padx = 100, pady = (20, 0), side = TOP, expand = True, fill = BOTH)
        self.date = self.cal.get_date()
        
        #retrieving saves from last use
        self.save_directory = "Calorie_Program_Saves"
        self.save_parent_dir = os.getcwd()
        print(self.save_parent_dir)
        self.save_path = os.path.join(self.save_parent_dir, self.save_directory) 
        self.images_folder = os.path.join(self.save_path, "Meal_Images")
        if os.path.exists(self.save_path):
            print(self.save_path)
            self.meal_index_auto_save = os.path.join(self.save_path, "Meal_Index")
            self.meal_record_auto_save = os.path.join(self.save_path, "My_Progress")
            self.cal_goal_auto_save = os.path.join(self.save_path, "Calories_Goal")
            # print(os.getcwd())
            # print(self.meal_index_auto_save)
            # print(self.images_folder)
            self.meal_index_save_file = open(self.meal_index_auto_save, "rb")
            self.meal_record_save_file = open(self.meal_record_auto_save, "rb")
            self.cal_goal_save_file = open(self.cal_goal_auto_save, "rb")

            self.meal_index_dict = pickle.load(self.meal_index_save_file)
            self.meal_record_dict = pickle.load(self.meal_record_save_file)
            self.calories_today = pickle.load(self.meal_record_save_file)
            self.cal_goal = pickle.load(self.cal_goal_save_file)

            self.meal_index_save_file.close()
            self.meal_record_save_file.close()
            self.cal_goal_save_file.close() 
        else:
            os.mkdir(self.save_path)
            os.mkdir(self.images_folder)
            self.meal_index_dict = {
                                "Steak(100g)":271, "Omelette Curry Rice": 560, "ข้าวมันไก่ทอด":693,
                                "ข้าวขาหมู":790, "Watermelon(100g)":30, "Boba Milk Tea":350, "Blended Cocoa":250}
            self.meal_record_dict = {}
            self.calories_today = {}
            self.cal_goal = 0.0
            self.meal_index_auto_save = os.path.join(self.save_path, "Meal_Index")
            self.meal_record_auto_save = os.path.join(self.save_path, "My_Progress")
            self.cal_goal_auto_save = os.path.join(self.save_path, "Calories_Goal")

            self.meal_index_save_file = open(self.meal_index_auto_save, "wb")
            self.meal_record_save_file = open(self.meal_record_auto_save, "wb")
            self.cal_goal_save_file = open(self.cal_goal_auto_save, "wb")

            pickle.dump(self.meal_index_dict, self.meal_index_save_file)
            pickle.dump(self.meal_record_dict, self.meal_record_save_file)
            pickle.dump(self.calories_today, self.meal_record_save_file)
            pickle.dump(self.cal_goal, self.cal_goal_save_file)

            self.meal_index_save_file.close()
            self.meal_record_save_file.close()
            self.cal_goal_save_file.close() 

            
        # print(f"{self.meal_record_dict}\n{self.meal_index_dict}\n{self.calories_today}\n{self.cal_goal}")
        
        self.meal_record_frame = Frame(self.window1, width= 100, height = 100, bg = "#fcf4dd")
        self.meal_record_frame.pack(side = TOP, fill = X, pady = 20)
        self.meal_record_button = Button(
                                    self.meal_record_frame,  borderless = True, height = 50,
                                    text="S h o w  M e a l s", command = self.show_meal, font= "TimesNewRoman 18 bold",
                                    activebackground= "#ddedea", activeforeground= 'black')
        self.meal_record_button.pack(side = TOP, fill = X, padx = 200, expand = True)
        self.meal_record = Label(self.meal_record_frame,  text="", bg = "#fcf4dd", fg = 'black', font = "timesnewroman 12 bold")
        self.meal_record.pack(pady = (0, 10), side = TOP, expand = True)

        self.record_meal_frame = Frame(self.window1, bg = "#fcf4dd")
        self.record_meal_frame.pack(side = TOP,  pady = (0,20), fill = X)
        self.record_meal_button = Button(
                                    self.record_meal_frame, height = 50,  borderless = True,
                                    text = "R e c o r d  M e a l", command = self.record_meal, font= "TimesNewRoman 18 bold",
                                    activebackground= "#ddedea", activeforeground= 'black')
        self.record_meal_button.pack(padx = 200, side = TOP, fill = X, expand = True)
        self.record_meal_label = Label(self.record_meal_frame, text = "\n")

        self.main_menu = Menu(self.window1)
        self.window1.config(menu = self.main_menu)
        # self.cal_goal_label1 = Label(self.goal_frame)
        # self.cal_goal_label1.pack(side= TOP)
        self.goal = Menu(self.main_menu)
        self.main_menu.add_cascade(label = "Goal", menu = self.goal)
        self.goal.add_command(label = "Create A New Goal", command = self.open_goal_window)

        self.meal_index_menu = Menu(self.main_menu)
        self.main_menu.add_cascade(label = "Meal Index", menu = self.meal_index_menu)
        self.meal_index_menu.add_command(label = "Record Meal", command = self.record_meal)

        self.analytics_menu = Menu(self.main_menu)
        self.main_menu.add_cascade(label = "Analytics", menu= self.analytics_menu)
        self.analytics_menu.add_command(label = "Analyze My Data", command = self.analyze_data)
        
        self.quit = Menu(self.main_menu)
        self.main_menu.add_cascade(label = "Quit", menu = self.quit )
        self.quit.add_command(label = "Quit", command = self.quit_program)

        self.window1.mainloop()
    
    def auto_save(self):
        self.meal_index_save_file = open(self.meal_index_auto_save, "wb")
        self.meal_record_save_file = open(self.meal_record_auto_save, "wb")
        self.cal_goal_save_file = open(self.cal_goal_auto_save, "wb")

        pickle.dump(self.meal_index_dict, self.meal_index_save_file)
        pickle.dump(self.meal_record_dict, self.meal_record_save_file)
        pickle.dump(self.calories_today, self.meal_record_save_file)
        pickle.dump(self.cal_goal, self.cal_goal_save_file)

        self.meal_index_save_file.close()
        self.meal_record_save_file.close()
        self.cal_goal_save_file.close()
    
    def load_meal_index(self):
        try:
            self.meal_index_file = askopenfilename()
            self.meal_index_file = open(self.meal_index_file, "rb")
            self.meal_index_dict = pickle.load(self.meal_index_file)
            self.meal_index_dict.close()
            self.add_meal_label.config(text = "Meal Index Loaded")
        except:
            #self.add_meal_label.config(text = "Failed to Load Meal Index. Please Try Again.")
            ans = messagebox.askretrycancel("Failed to Load Index", "Failed to Load Index.")
            if ans == True:
                self.load_meal_index()
        
    def save_meal_index(self):
        try:
            self.meal_record_file = asksaveasfilename()
            self.meal_record_file = open(self.meal_record_file, "wb")
            pickle.dump(self.meal_record_dict, self.meal_record_file)
            self.meal_record_file.close()
            self.add_meal_label.config(text = "Meal Index Saved")
            self.auto_save()
        except:
            ans = messagebox.askretrycancel("Failed to Save Meal Index", "Failed to Save Meal Index.")
            if ans == True:
                self.save_meal_index()

    def load_progress(self):
        try:
            self.progress_file = askopenfilename()
            self.progress_file = open(self.progress_file, "rb")
            self.meal_record_dict = pickle.load(self.progress_file)
            self.calories_today = pickle.load(self.progress_file)
            self.progress_file.close()
            self.meal_record.config(text = "Progress Loaded")
            self.auto_save()
        except:
            ans = messagebox.askretrycancel("Failed to Load Progress", "Failed to Load Meal Index.")
            if ans == True:
                self.load_progress()
    
    def save_progress(self):
        try:
            self.meal_record_file = asksaveasfilename()
            self.meal_record_file = open(self.meal_record_file, "wb")
            pickle.dump(self.meal_record_dict, self.meal_record_file)
            pickle.dump(self.calories_today, self.meal_record_file)
            self.meal_record_file.close()
            self.meal_record.config(text = "Progress Saved")
            self.autosave()
        except:
            ans = messagebox.askretrycancel("Failed to Save Progress", "Failed to Save Progress.")
            if ans == True:
                self.save_progress()
    
    def reset_progress(self):
        ans = messagebox.askyesno("Are You Sure?", "Are You Sure You Want to Reset Your Progress?")
        if ans == True:
            self.meal_record_dict.clear()
            self.calories_today.clear()
            self.meal_record.config(text = "Your Progress Has Been Reset", font= "TimesNewRoman 14")
        self.auto_save()

    def quit_program(self):
        self.window1.destroy()

    def record_meal(self):
        self.meal_index = Toplevel(self.window1, bg = "#ddedea")
        self.meal_index.title("Meal Index")
        self.meal_index.geometry("400x500")
        self.meal_index.minsize(400, 400)
        self.meal_index.maxsize(400, 500)

        self.meal_combo_frame = Frame(self.meal_index, bg = "#ddedea")
        self.meal_combo_frame.pack(side = TOP, pady = (10, 0))
        self.meal_combo_label = Label(
                                self.meal_combo_frame, text = "Select a Meal\n", font= "TimesNewRoman 14 bold", 
                                bg = "#ddedea", foreground="black")
        self.meal_combo_label.pack(side = TOP)
        self.meal = StringVar()
        self.meal_combo = ttk.Combobox(
                                self.meal_combo_frame, textvariable= self.meal, values= list(self.meal_index_dict.keys()),
                                font= "TimesNewRoman 14")
        self.meal_combo.current(0)
        self.meal_combo.bind("<<ComboboxSelected>>", self.get_meal_image)
        self.meal_combo.pack()
        self.meal_combo_button = Button(
                                self.meal_combo_frame, text = "Record Meal", command = self.pick_meal, font= "TimesNewRoman 14",
                                activebackground= "#ddedea", activeforeground= 'black', borderless = True)
        self.meal_combo_button.pack(side= TOP)
        self.add_image_for_meal_button = Button(self.meal_combo_frame, text = "Add Image",
                                activebackground= "#ddedea", activeforeground= 'black', borderless = True,
                                command = self.add_image_for_meal)
        self.add_image_for_meal_button.pack(side = TOP)
        self.meal_image_label = Label(self.meal_combo_frame, bg = "#ddedea")
        self.meal_image_label.pack(side = TOP)
        # self.meal_index_delete_button = Button(self.meal_combo_frame, text = "Delete Meal From Index", command = self.delete_meal)
        # self.meal_index_delete_button.pack(side = TOP)

        self.add_meal_name_frame = Frame(self.meal_index, bg = "#ddedea")
        self.add_meal_name_frame.pack(side = TOP, pady = 10, padx = 20)
        self.add_meal_label1 = Label(
                                    self.add_meal_name_frame, text = "OR Add a New Meal\n", font= "TimesNewRoman 14 bold", bg = "#ddedea",
                                    foreground = 'black')
        self.add_meal_label1.pack(side = TOP)
        self.new_meal_name_input = StringVar()
        self.new_meal_calories_input = DoubleVar()
        self.new_meal_name_label = Label(
                                        self.add_meal_name_frame, text = "Enter a Meal Name: ", font= "TimesNewRoman 14", bg = "#ddedea",
                                        foreground = 'black')
        self.new_meal_name_label.pack(side = LEFT)
        self.new_meal_name = Entry(
                                    self.add_meal_name_frame, textvariable= self.new_meal_name_input, bg = "#ddedea", foreground = 'black',
                                    highlightthickness= 0)
        self.new_meal_name.pack(side = RIGHT)

        self.add_meal_calories_frame = Frame(self.meal_index, bg = "#ddedea")
        self.add_meal_calories_frame.pack(side = TOP, padx= 10)
        self.new_meal_calories = Entry(
                                        self.add_meal_calories_frame, textvariable = self.new_meal_calories_input, bg = "#ddedea", 
                                        foreground= 'black', highlightthickness= 0)
        self.new_meal_calories.pack(side = RIGHT)
        self.new_meal_calories_label = Label(
                                            self.add_meal_calories_frame, text = "Calories: ", font= "TimesNewRoman 14", bg = "#ddedea",
                                            foreground = 'black')
        self.new_meal_calories_label.pack(side = LEFT)
        self.add_meal_button = Button(
                                    self.meal_index, text = "Add", command = self.add_meal, font= "TimesNewRoman 14", bg = "white",
                                    borderless = True, activebackground = '#ddedea', activeforeground= 'black')
        self.add_meal_button.pack(side = TOP)
        self.add_meal_label = Label(self.meal_index, text = "", bg = "#ddedea")
        self.add_meal_label.pack(side = TOP)
    
    # def delete_meal(self):
    #     if self.meal.get() in self.meal_index_dict:
    #         self.meal_index_dict.pop(self.meal.get())
    #         self.meal_combo = ttk.Combobox(self.meal_combo_frame, textvariable= self.meal, values= list(self.meal_index_dict.keys()),
    #                                         font= "TimesNewRoman 14")
    #         self.meal_combo.current(0)
    #         self.auto_save()
    def add_image_for_meal(self):
        try:
            self.selected_meal = self.meal.get().replace(" ", "")
            self.image_import_file = askopenfilename()
            self.image_open = Image.open(self.image_import_file)
            self.image_photo = ImageTk.PhotoImage(self.image_open)
            self.meal_image_label.config(image = self.image_photo)
            self.image_save_path = os.path.join(self.images_folder, f"{self.selected_meal}.png")
            self.image_open = self.image_open.save(self.image_save_path)
        except:
            ans = messagebox.askretrycancel("Image Import Failed", "Import Failed.")
            if ans == True:
                self.add_image_for_meal()
        # self.selected_meal = self.meal.get().replace(" ", "_")
        # self.image_import_file = askopenfilename()
        # self.image_open = Image.open(self.image_import_file)
        # self.image_photo = ImageTk.PhotoImage(self.image_open)
        # self.meal_image_label.config(image = self.image_photo)
        # self.image_save_path = os.path.join(self.images_folder, f"{self.selected_meal}.png")
        # self.image_open = self.image_open.save(self.image_save_path)

    def get_meal_image(self, event):
        self.selected_meal = self.meal.get().replace(" ", "")
        self.image_import_file = os.path.join(self.images_folder, f"{self.selected_meal}.png")
        if os.path.exists(self.image_import_file):
            self.image_open = Image.open(self.image_import_file)
            self.image_photo = ImageTk.PhotoImage(self.image_open)
            self.meal_image_label.config(image = self.image_photo)
        else:
            self.meal_image_label.config(image = '')

    def add_meal(self):
        try:
            if self.new_meal_name_input.get() in self.meal_index_dict:
                raise MealAlreadyInIndex
            if self.new_meal_name_input.get() == "":
                raise EmptyBox
            if self.new_meal_calories_input.get() <= 0.0:
                raise PositiveNumbersOnly
            if type(self.new_meal_name_input.get()) != str:
                raise LettersOnly
            else:
                self.meal_index_dict[self.new_meal_name_input.get()] = self.new_meal_calories_input.get()
            self.add_meal_label.config(text = "Meal Added", font= "TimesNewRoman 14")
            self.auto_save()
            self.meal_index.destroy()
        except MealAlreadyInIndex:
            ans = messagebox.askyesno("Meal Already Exists", f"\'{self.new_meal_name_input.get()}\' already exists. Replace It?")
            if ans == True:
                self.meal_index_dict[self.new_meal_name_input.get()] = self.new_meal_calories_input.get()
                self.add_meal_label.config(text = "Meal Added", font= "TimesNewRoman 14")
                self.auto_save()
                self.meal_index.destroy()
        except PositiveNumbersOnly:
            messagebox.showerror("Invalid Input", "Please Input Positive Numbers Only")
        except EmptyBox:
            messagebox.showerror("Invalid Input", "Please Fill In Blank Boxes")
        except LettersOnly:
            messagebox.showerror("Invalid Input", "Please Enter a Valid Name")
        except:
            messagebox.showerror("Invalid Input", "Please Enter a Valid Number")
    
    def pick_meal(self):
        self.date = self.cal.get_date()
        if self.date in self.meal_record_dict.keys():
            self.meal_record_dict[self.date].append(self.meal.get())
        else:
            self.meal_record_dict[self.date] = [self.meal.get()]
        self.auto_save()
        try:
            if self.date in self.calories_today.keys():
                self.calories_today[self.date] += self.meal_index_dict[self.meal.get()]
            else:
                self.calories_today[self.date] = self.meal_index_dict[self.meal.get()]
            self.auto_save()
            self.show_meal()
        except:
            messagebox.showerror("Invalid Meal Index", "Please Use A Valid Meal Index")
        self.meal_index.destroy()
    
    def show_meal(self):
        self.date = self.cal.get_date()
        try:
            self.meal_record.config(text = f"{self.cal.get_date()} Meals:" )
            for x in self.meal_record_dict[self.date]:
                self.meal_record.config(text = self.meal_record.cget("text") + "\n" + x + " ("  + str(self.meal_index_dict[x]) + 
                                        " Calories)")
        except:
            self.meal_record.config(text = "No Meals to Show")
        if self.date in self.calories_today.keys():
            if self.cal_goal != 0.0:
                self.meal_record.config(text = self.meal_record.cget("text") + "\n\nCalories Consumed: " + 
                                        str(self.calories_today[self.date]) + "/" + str(self.cal_goal))
            else:
                self.meal_record.config(text = self.meal_record.cget("text") + "\n\nCalories Consumed: " 
                                        + str(self.calories_today[self.date]) + "/" + " - ")
        
    def open_goal_window(self):
        self.goal = Toplevel(self.window1, bg = "#e8dff5")
        self.goal.title("Set a Goal")
        self.goal.geometry("800x600")
        self.goal.resizable(False, False)
        self.goal.option_add("*font", "timesnewroman 16 bold")
        
        self.gender_frame = Frame(self.goal, bg = "#e8dff5")
        self.gender_frame.pack(side = TOP, expand = True)
        self.gender_input = StringVar(self.gender_frame, value = "male")
        self.gender_M = Radiobutton(
                            self.gender_frame, text = "Male", variable = self.gender_input, value = "male", 
                            bg = "#e8dff5", fg = "black")
        self.gender_M.pack(side = LEFT, expand = True, fill = X, padx = 5)
        self.gender_F = Radiobutton(
                            self.gender_frame, text = "Female", variable = self.gender_input, value = "female",
                            bg = "#e8dff5", fg = "black")
        self.gender_F.pack(side = RIGHT, expand = True, fill = X, padx = 5)

        self.age_frame = Frame(self.goal, bg = "#e8dff5")
        self.age_frame.pack(side = TOP, expand = True, fill= X)
        self.age_input = IntVar()
        self.age_label = Label(self.age_frame, text= "Enter your age: ", bg = "#e8dff5", foreground= 'black')
        self.age_label.pack(side = LEFT, expand = True, fill= X)
        self.age = Entry(self.age_frame, textvariable= self.age_input, highlightthickness=0, fg = 'white')
        self.age.pack(side = RIGHT, expand = True)

        self.weight_frame = Frame(self.goal, bg = "#e8dff5")
        self.weight_frame.pack(side = TOP, expand = True, fill= X)
        self.weight_label = Label(self.weight_frame, text = "Enter your weight in KG: ", bg = "#e8dff5", foreground='black')
        self.weight_label.pack(side = LEFT, expand = True, fill= X)
        self.weight_input = DoubleVar()
        self.weight = Entry(self.weight_frame, textvariable = self.weight_input, highlightthickness = 0, fg = 'white')
        self.weight.pack(side = RIGHT, expand = True)

        self.height_frame = Frame(self.goal, bg = "#e8dff5")
        self.height_frame.pack(side = TOP, expand = True, fill= X)
        self.height_label = Label(self.height_frame, text = "Enter your height in CM: ", bg = "#e8dff5", foreground= 'black')
        self.height_label.pack(side = LEFT, expand = True, fill= X)
        self.height_input = IntVar()
        self.height = Entry(self.height_frame, text = "Enter your height in CM: ", textvariable = self.height_input, highlightthickness=0, fg = 'white')
        self.height.pack(side = RIGHT, expand = True)

        self.goal_frame = Frame(self.goal, bg = "#e8dff5")
        self.goal_frame.pack(side = TOP, expand = True)
        self.goal_input = StringVar(self.goal_frame, value = "maintain")
        self.goal_M = Radiobutton(
                        self.goal_frame, text = "Maintain Weight", variable = self.goal_input, value = "maintain", bg = "#e8dff5",
                        foreground = "black")
        self.goal_M.pack(side = LEFT, expand = True, padx = 20)
        self.goal_L = Radiobutton(
                        self.goal_frame, text = "Lose Weight", variable = self.goal_input, value = "lose", bg = "#e8dff5",
                        foreground = "black")
        self.goal_L.pack(side = LEFT, expand = True)
        self.goal_G = Radiobutton(
                        self.goal_frame, text = "Gain Weight", variable = self.goal_input, value = "gain", bg = "#e8dff5",
                        foreground = "black")
        self.goal_G.pack(side = LEFT, expand = True, padx = 20)

        self.bmr = DoubleVar()
        self.bmr_frame = Frame(self.goal, bg = "#e8dff5")
        self.bmr_frame.pack(side = TOP, expand = True, fill = X)
        self.bmr_button = Button(self.bmr_frame, text = "Calculate", command = self.process_bmr, borderless = True, activebackground= 'black',
                            activeforeground = 'white', )
        self.bmr_button.pack(side = LEFT, expand = True)
        self.goal_label = Label(self.bmr_frame, text = "", bg = "#e8dff5")
        self.goal_label.pack(side = RIGHT, expand = True, fill = X)

        self.save_goal_frame = Frame(self.goal, bg = "#e8dff5")
        self.save_goal_frame.pack(side = TOP, expand = True, fill = X)
        self.save_goal_file_button = Button(
                                        self.save_goal_frame, text = "Save Goal", command = self.save_goal_file, bg = "white", 
                                        borderless = True, activebackground= 'black', activeforeground= 'white')
        self.save_goal_file_button.pack(side = RIGHT, expand = True)
        self.load_goal_file_button = Button(
                                        self.save_goal_frame, text = "Load Goal", command = self.load_goal_file, bg = "white", 
                                        borderless = True, activebackground= 'black', activeforeground= 'white')
        self.load_goal_file_button.pack(side = LEFT, expand = True)
        self.save_load_label = Label(self.save_goal_frame, text = "", bg = "#e8dff5")
        self.save_load_label.pack(side = TOP, expand = True)
           
    def process_bmr(self):
        try:
            if (self.weight_input.get() <= 0) or (self.age_input.get() <= 0) or (self.height_input.get() <= 0):
                raise PositiveNumbersOnly()
            else: 
                user_BMR = BMR(self.age_input.get(), self.weight_input.get(), self.height_input.get(), self.gender_input.get())
                cal_goal = CalorieGoal(
                                self.age_input.get(), self.weight_input.get(), self.height_input.get(), self.gender_input.get(),
                                self.goal_input.get())
                if cal_goal == 0.0:
                    raise NoGoal
                self.bmr = user_BMR.calculate_BMR()
                self.cal_goal = cal_goal.calculate_calorie_goal()
                if self.cal_goal <= 1500.0 and self.gender_input.get() == "male":
                    self.cal_goal = 1500.0
                    self.goal_label.config(
                                    text = "Your BMR is " + str(self.bmr) + "\nYour Goal Will Be " + str(self.cal_goal) +
                                    " Calories/day (Minimum)")
                elif self.cal_goal <= 1200.0 and self.gender_input.get() == "female":
                    self.cal_goal = 1200.0
                    self.goal_label.config(
                                    text = "Your BMR is " + str(self.bmr) + "\nYour Goal Will Be " + str(self.cal_goal) + 
                                    " Calories/day (Minimum)")
                else:
                    self.goal_label.config(
                                    text = "Your BMR is " + str(self.bmr) + "\nYour Goal Will Be " + str(self.cal_goal) + 
                                    " Calories/day")
                self.auto_save()
        except PositiveNumbersOnly:
            messagebox.showerror("Invalid Input", "Please Input Positive Numbers Only")
        except NoGoal:
            self.goal_label.config("Please Create a New Goal")
        except:
            messagebox.showerror("Invalid Input", "Please Input Numbers Only")

    def save_goal_file(self):
        try:
            if self.cal_goal == 0.0:
                raise NoGoal
            filenameforWriting = asksaveasfilename()
            self.goal_file = open(filenameforWriting, "wb")
            pickle.dump(self.cal_goal, self.goal_file)
            self.goal_file.close()
            self.save_load_label.config(text = "Goal Saved")
            self.goal_label.config(text = "Your Goal is " + str(self.cal_goal) + " Calories/day")
            #self.cal_goal_label1.config(text = f"Goal: {str(self.cal_goal)} Calories/day")
        except NoGoal:
            self.goal_label.config("Please Create a New Goal.")
        except:
            ans = messagebox.askretrycancel("Failed to Save", "Failed to Save Goal.")
            if ans == True:
                self.save_goal_file()

    def load_goal_file(self):
        try:
            filenameforReading = askopenfilename()
            filenameforReading = open(filenameforReading, "rb")
            self.cal_goal = pickle.load(filenameforReading)
            filenameforReading.close()
            if self.cal_goal == 0.0:
                raise NoGoal
            self.save_load_label.config(text = "Goal Loaded")
            self.goal_label.config(text = "Your Goal is " + str(self.cal_goal) + " Calories/day")
            #self.cal_goal_label1.config(text = f"Goal: {str(self.cal_goal)} Calories/day")
        except NoGoal:
            ans = messagebox.showinfo("No Existing Goal", "No Existing Goal. Please Create a New Goal")
        except:
            ans = messagebox.askretrycancel("Failed to Load Goal", "Failed to Load Goal.")
            if ans == True:
                self.load_goal_file()

    def analyze_data(self):
        data_window = Analytics(parent = self.window1, meal_index= self.meal_index_dict, meal_record = self.meal_record_dict, 
                                calories_today=self.calories_today, cal_goal=self.cal_goal)
        data_window.find_least_most_calories()
        data_window.find_mean_calories()
        data_window.find_goal_reached()
        data_window.find_fav_meal()

class Analytics(Toplevel):
    def __init__(self, parent, meal_index, meal_record, calories_today, cal_goal):
        super().__init__(parent)
        self.meal_index = meal_index
        self.meal_record = meal_record
        self.calories_today = calories_today
        self.cal_goal = cal_goal
        self.days_goal_reached = {}
        self.meal_occurences = {}

        self.config(bg = "#daeaf6")
        self.title("My History")
        self.geometry("500x400")
        self.resizable(False, False)
        style = ttk.Style(self)
        style.theme_use('clam') 
        self.option_add("*font", "TimesNewRoman 14 bold")
        self.option_add("*foreground", "black")

        self.data_frame = Frame(self, bg = "#daeaf6")
        self.data_frame.pack(side = TOP)
        self.cal_goal_label = Label(self.data_frame, text = f"Current Goal: {str(self.cal_goal)} Calories/day", bg = "#daeaf6")
        self.cal_goal_label.pack(side = TOP, pady = 10)
        self.days_recorded_label = Label(self.data_frame, text = f"Days Recorded: {str(len(self.meal_record))} day(s)", bg = "#daeaf6")
        self.days_recorded_label.pack(side = TOP, pady = 10)

        self.least_most_calories_frame = Frame(self, bg = "#daeaf6")
        self.least_most_calories_frame.pack(side = TOP)
        self.least_most_calories_label = Label(
                                    self.least_most_calories_frame,
                                    text = "Least Calories in One Day = *Not Enough Data*\n\nMost Calories in One Day = *Not Enough Data*",
                                    bg = "#daeaf6")
        self.least_most_calories_label.pack(side = TOP, pady = 10)

        self.mean_calories_frame = Frame(self, bg = "#daeaf6")
        self.mean_calories_frame.pack(side = TOP)
        self.mean_calories_label = Label(self.mean_calories_frame, text = "Average Calories per Day =  *Not Enough Data*", bg = "#daeaf6")
        self.mean_calories_label.pack(side = TOP, pady=10)

        self.goal_reached_frame = Frame(self, bg = "#daeaf6")
        self.goal_reached_frame.pack(side = TOP)
        self.goal_reached_label = Label(self.goal_reached_frame, text = "Days Goal Reached = *Not Enough Data*", bg = "#daeaf6")
        self.goal_reached_label.pack(side = TOP, pady = 10)

        self.fav_meal_frame = Frame(self, bg = "#daeaf6")
        self.fav_meal_frame.pack(side = TOP)
        self.fav_meal_label = Label(self.fav_meal_frame, text = "Favorite Meal = *Not Enough Data*", bg = "#daeaf6")
        self.fav_meal_label.pack(side = TOP, pady = 10)
        self.fav_meal_button = Button(self.fav_meal_frame, text = "Show Meal Record", background = "white", foreground= 'black',
                                activebackground = "#daeaf6", activeforeground = 'black', borderless = True,
                                font = "Timesnewroman 14 bold", command = self.fav_meal_graphic)
        self.fav_meal_button.pack(side = TOP, pady = 10)


    def find_least_most_calories(self):
        #print(self.calories_today)
        self.least_calories = 0.0
        self.most_calories = 0.0
        self.least_calories_dict = {}
        self.most_calories_dict = {}
        if self.calories_today != {}:
            for x, y in self.calories_today.items():
                if y < self.least_calories:
                    self.least_calories = y
                    self.least_calories_dict[x] = y
                if y > self.most_calories:
                    self.most_calories = y 
                    self.most_calories_dict[x] = y
            self.least_most_calories_label.config(
                                                    text = "Least Calories in One Day = " + str(self.least_calories) 
                                                    + " Calories\nMost Calories in One Day = " + str(self.most_calories) + " Calories")
        
    def find_mean_calories(self):
        # print(self.calories_today)
        self.mean_calories = 0.0
        sum = 0.0
        try:
            for x in self.calories_today:
                sum += self.calories_today[x]
            self.mean_calories = sum / len(self.calories_today)
            self.mean_calories_label.config(text = "Average Calories per Day = " + str(round(self.mean_calories,2)) + " Calories")
        except:
            pass

    def find_goal_reached(self):
        if self.calories_today != {}:
            for x, y in self.calories_today.items():
                if y <= self.cal_goal:
                    self.days_goal_reached[x] = y
            self.days_goal_reached_percentage = len(self.days_goal_reached)/len(self.meal_record)
            self.days_goal_reached_percentage *= 100
            self.goal_reached_label.config(
                                            text = f"Days Goals Reached = {len(self.days_goal_reached)} day(s) out of {len(self.meal_record)} day(s) "
                                            + f"({round(self.days_goal_reached_percentage, 2)}%)")
    
    def find_fav_meal(self):
        self.most_occurences = 0
        self.most_occurences_dict = {}
        if self.meal_record != {}:
            for meals in self.meal_record.values():
                for y in meals:
                    if y in self.meal_occurences:
                        self.meal_occurences[y] += 1
                    else:
                        self.meal_occurences[y] = 1
            for x, y in self.meal_occurences.items():
                if y >= self.most_occurences:
                    self.most_occurences = y 
                    if y in self.most_occurences_dict:
                        self.most_occurences_dict[y].append(x)
                    else:
                        self.most_occurences_dict[y] = [x]
            self.fav_meal_label.config(
                                text = f"Favorite Meal(s) = {self.most_occurences_dict[self.most_occurences]}\n" +
                                f"Had = {self.most_occurences} time(s) in {len(self.meal_record)} day(s)")
    
    def fav_meal_graphic(self):
        try:
        #print(self.most_occurences)
            if len(self.meal_record) == 0:
                raise EmptyBox
            t.tracer(False)
            t.penup()
            t.goto(-200, 0)
            t.pendown()
            t.left(90)
            t.stamp()
            t.right(180)
            t.forward(self.most_occurences * 20)
            t.left(90)
            for x, y in self.meal_occurences.items():
                t.forward(20)
                t.write(y)
                t.forward(10)
                for i in range(2):
                    t.left(90)
                    t.forward(20*y)
                    t.left(90)
                    t.forward(15)
            t.forward(30)
            t.stamp()
            t.penup()
            t.goto(-200, -(self.most_occurences * 40))
            t.write(f"Domain: {list(self.meal_occurences.keys())}")
            t.exitonclick()
        except EmptyBox:
            messagebox.showerror("Not Enough Data", "Not Enough Data")
CalorieProgram()
