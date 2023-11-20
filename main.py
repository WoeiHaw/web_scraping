from tkinter import *
from coffee_price import Coffee
from shower_gel import Dettol
from shampoo import Shapoo
from facewash import Facewash
from toothpaste import Toothpaste
from sg_room import Sg_room
from data_science_job import Job_info
from house_price import House_price
from shoes import Shoes
from backup import Backup
from backup_drive import Backup_drive
from download_data import Download_data
from shoes_dashboard import Shoes_dashboard
from grocery_item_dashboard import Grocery_dashboard
from shoes_image import Shoes_image
from singapore_rental_dashboard import Sg_rental_dashboard
from processed_sg_rental import Process_data
import time
from dash import Dash, html

COLOR1 = "#FAF0E6"
COLOR2 = "#B9B4C7"
COLOR3 = "#5C5470"
COLOR4 = "352F44"
FONT_NAME = "Courier"


# ---------------------------- TRIGGER FOR WEB SCRAPPING ------------------------------- #
def skechers_shoes_my():
    Shoes("my", "../../data/skechers_shoes_MY.csv")


def skechers_shoes_sg():
    Shoes("sg", "../../data/skechers_shoes_SG.csv")


def kl_house():
    House_price("../../data/House Price kl.csv", "kuala+lumpur")


def jb_house():
    House_price("../../data/House Price JB.csv", "johor+bahru")


def sg_job():
    Job_info("../../data/Singapore Job.csv", "sg")


def my_job():
    Job_info("../../data/Malaysia Job.csv", "my")


def scrape_sg_room():
    Sg_room("../../data/sg rental.csv")
    Process_data("../../data/")


def scrape_coffee():
    Coffee("../../data/kopi o price.csv")


def scrape_shower_gel():
    Dettol("../../data/Dettol Shower Gel.csv")


def scrape_shampoo():
    Shapoo("../../data/shampoo price.csv")


def scrape_face_wash():
    Facewash("../../data/Nivea Man.csv")


def scrape_tooth_paste():
    Toothpaste("../../data/Darlie Toothpaste.csv")


def scrape_all():
    scrape_all_grocerries()

    scrape_sg_room()

    scrape_all_job()

    scrape_all_house()


def scrape_all_grocerries():
    scrape_coffee()
    scrape_shower_gel()
    scrape_shampoo()
    scrape_face_wash()
    scrape_tooth_paste()
    Shoes("my", "../../data/skechers_shoes_MY.csv")
    Shoes("sg", "../../data/skechers_shoes_SG.csv")


def scrape_all_job():
    sg_job()
    my_job()


def scrape_all_house():
    House_price("../../data/House Price kl.csv", "kuala+lumpur")
    House_price("../../data/House Price JB.csv", "johor+bahru")


def get_shoes_image():
    Shoes_image("my")
    Shoes_image("sg")


def back_up():
    file_location = [
        "../../data/kopi o price.csv",
        "../../data/Dettol Shower Gel.csv",
        "../../data/shampoo price.csv",
        "../../data/Nivea Man.csv",
        "../../data/Darlie Toothpaste.csv",
        "../../data/skechers_shoes_MY.csv",
        "../../data/skechers_shoes_SG.csv",
        "../../data/sg rental.csv",
        "../../data/Malaysia Job.csv",
        "../../data/Singapore Job.csv",
        "../../data/House Price kl.csv",
        "../../data/House Price JB.csv",
        "../../data/sg rental(processed).csv",
    ]
    backup_location = [
        "../../Data_back_up/kopi o price.csv",
        "../../Data_back_up/Dettol Shower Gel.csv",
        "../../Data_back_up/shampoo price.csv",
        "../../Data_back_up/Nivea Man.csv",
        "../../Data_back_up/Darlie Toothpaste.csv",
        "../../Data_back_up/skechers_shoes_MY.csv",
        "../../Data_back_up/skechers_shoes_SG.csv",
        "../../Data_back_up/sg rental.csv",
        "../../Data_back_up/Malaysia Job.csv",
        "../../Data_back_up/Singapore Job.csv",
        "../../Data_back_up/House Price kl.csv",
        "../../Data_back_up/House Price JB.csv",
        "../../Data_back_up/sg rental(processed).csv"
    ]
    Backup(file_location, backup_location)


# ---------------------------- UI SETUP FOR WEB SCRAPING ------------------------------- #
window = None


def groceries_menu():
    global window
    window.destroy()
    window = new_window()

    title = Label(text="Grocerries Item", font=(FONT_NAME, 40), bg=COLOR1, fg=COLOR3)
    title.grid(row=0, column=1, columnspan=2)

    button_coffe = Button(text="Kluang Kopi O Kosong", font=(FONT_NAME, 20), bg=COLOR2, command=scrape_coffee)
    button_coffe.grid(row=1, column=1, pady=5, columnspan=2)

    button_shower_gel = Button(text="Dettol Shower Gel", font=(FONT_NAME, 20), bg=COLOR2, command=scrape_shower_gel)
    button_shower_gel.grid(row=2, column=1, pady=5, columnspan=2)

    button_shampoo = Button(text="Head and Shoulder Shampoo", font=(FONT_NAME, 20), bg=COLOR2, command=scrape_shampoo)
    button_shampoo.grid(row=3, column=1, pady=5, columnspan=2)

    button_facewash = Button(text="Nivea Man Face-wash", font=(FONT_NAME, 20), bg=COLOR2, command=scrape_face_wash)
    button_facewash.grid(row=4, column=1, pady=5, columnspan=2)

    button_toothpaste = Button(text="Darlie Toothpaste", font=(FONT_NAME, 20), bg=COLOR2, command=scrape_tooth_paste)
    button_toothpaste.grid(row=5, column=1, pady=5, columnspan=2)

    button_skechers_shoes_my = Button(text="Skechers Shoes (Malaysia)", font=(FONT_NAME, 20), bg=COLOR2,
                                      command=skechers_shoes_my)
    button_skechers_shoes_my.grid(row=6, column=1, pady=5, columnspan=2)

    button_skechers_shoes_sg = Button(text="Skechers Shoes (Singapore)", font=(FONT_NAME, 20), bg=COLOR2,
                                      command=skechers_shoes_sg)
    button_skechers_shoes_sg.grid(row=7, column=1, pady=5, columnspan=2)

    button_scrape_all = Button(text="Scrape All", font=(FONT_NAME, 20), bg=COLOR2,
                               command=scrape_all_grocerries)
    button_scrape_all.grid(row=8, column=1, pady=5, columnspan=2)

    button_exit_grocerries = Button(text="Exit Programme", font=(FONT_NAME, 20), bg=COLOR3, command=window.destroy)
    button_exit_grocerries.grid(row=9, column=0, padx=20, pady=10, columnspan=2)

    button_main_menu = Button(text="Go Back", font=(FONT_NAME, 20), bg=COLOR3, command=go_web_scrape_main_gui)
    button_main_menu.grid(row=9, column=2, padx=20, pady=10, columnspan=2)


def data_science_job_gui():
    global window
    window.destroy()
    window = new_window()
    title = Label(text="Data Science Job", font=(FONT_NAME, 40), bg=COLOR1, fg=COLOR3)
    title.grid(row=0, column=1, pady=10, columnspan=2)

    button_sg_job = Button(text="Data Science Job(Singapore)", font=(FONT_NAME, 20), bg=COLOR2, command=sg_job)
    button_sg_job.grid(row=1, column=1, pady=10, columnspan=2)

    button_sg_job = Button(text="Data Science Job(Malaysia)", font=(FONT_NAME, 20), bg=COLOR2, command=my_job)
    button_sg_job.grid(row=2, column=1, pady=10, columnspan=2)

    button_scrape_all = Button(text="Scrape All", font=(FONT_NAME, 20), bg=COLOR2,
                               command=scrape_all_job)
    button_scrape_all.grid(row=3, column=1, pady=10, columnspan=2)

    button_exit_grocerries = Button(text="Exit Programme", font=(FONT_NAME, 20), bg=COLOR3, command=window.destroy)
    button_exit_grocerries.grid(row=4, column=0, padx=20, columnspan=2)

    button_main_menu = Button(text="GO BACK", font=(FONT_NAME, 20), bg=COLOR3, command=go_web_scrape_main_gui)
    button_main_menu.grid(row=4, column=2, padx=20, pady=20, columnspan=2)


def data_management():
    global window
    window.destroy()
    window = new_window()

    title = Label(text="Data Management", font=(FONT_NAME, 40), bg=COLOR1, fg=COLOR3)
    title.grid(row=0, column=0, pady=10, columnspan=3)

    download_data = Button(text="Download Data", font=(FONT_NAME, 20), bg=COLOR2, command=Download_data)
    download_data.grid(row=1, column=0, pady=10, columnspan=3)

    back_up_local = Button(text="Back Up Locally", font=(FONT_NAME, 20), bg=COLOR2, command=back_up)
    back_up_local.grid(row=2, column=0, pady=10, columnspan=3)

    back_up_drive = Button(text="Back Up - Google Drive", font=(FONT_NAME, 20), bg=COLOR2, command=Backup_drive)
    back_up_drive.grid(row=3, column=0, pady=10, columnspan=3)

    skechers_shoes_image = Button(text="Get Skeacher Shoes Image", font=(FONT_NAME, 20), bg=COLOR2,
                                  command=get_shoes_image)
    skechers_shoes_image.grid(row=4, column=0, pady=10, columnspan=3)

    button_exit_grocerries = Button(text="Exit Programme", font=(FONT_NAME, 20), bg=COLOR3, command=window.destroy)
    button_exit_grocerries.grid(row=5, column=0, padx=20, columnspan=1)

    button_main_menu = Button(text="GO BACK", font=(FONT_NAME, 20), bg=COLOR3, command=go_web_scrape_main_gui)
    button_main_menu.grid(row=5, column=2, padx=20, pady=20, columnspan=1)


def house_price_gui():
    global window
    window.destroy()
    window = new_window()

    title = Label(text="House Price", font=(FONT_NAME, 40), bg=COLOR1, fg=COLOR3)
    title.grid(row=0, column=0, pady=10, columnspan=4)

    button_kl_house = Button(text="Kuala Lumpur", font=(FONT_NAME, 20), bg=COLOR2, command=kl_house)
    button_kl_house.grid(row=1, column=1, pady=10, columnspan=2)

    button_jb_house = Button(text="Johor Bahru", font=(FONT_NAME, 20), bg=COLOR2, command=jb_house)
    button_jb_house.grid(row=2, column=1, pady=10, columnspan=2)

    button_scrape_all = Button(text="Scrape All", font=(FONT_NAME, 20), bg=COLOR2,
                               command=scrape_all_house)
    button_scrape_all.grid(row=3, column=1, pady=10, columnspan=2)

    button_exit_grocerries = Button(text="Exit Programme", font=(FONT_NAME, 20), bg=COLOR3, command=window.destroy)
    button_exit_grocerries.grid(row=4, column=0, padx=20, columnspan=2)

    button_main_menu = Button(text="GO BACK", font=(FONT_NAME, 20), bg=COLOR3, command=go_web_scrape_main_gui)
    button_main_menu.grid(row=4, column=2, padx=20, pady=20, columnspan=2)


def go_web_scrape_main_gui():
    global window
    # window.destroy()
    web_scrape_main_gui()


def go_main_menu():
    global window
    window.destroy()
    main_gui()


def web_scrape_main_gui():
    global window
    window.destroy()
    window = new_window()
    title = Label(text="Web Scraping Programme", font=(FONT_NAME, 40), bg=COLOR1, fg=COLOR3)
    title.grid(row=0, column=0, columnspan=2)

    button_groceries = Button(text="Groceries Items", font=(FONT_NAME, 20), bg=COLOR2, command=groceries_menu)
    button_groceries.grid(row=1, column=0, pady=10, columnspan=2)

    button_sg_room = Button(text="Singapore Room Rental Information ", font=(FONT_NAME, 20), bg=COLOR2,
                            command=scrape_sg_room)
    button_sg_room.grid(row=2, column=0, pady=10, columnspan=2)

    button_job = Button(text="Data Science Job Information ", font=(FONT_NAME, 20), bg=COLOR2,
                        command=data_science_job_gui)
    button_job.grid(row=3, column=0, pady=10, columnspan=2)

    button_house_price = Button(text="Johor Bahru and Kuala Lumpur House Price", font=(FONT_NAME, 20), bg=COLOR2,
                                command=house_price_gui)
    button_house_price.grid(row=4, column=0, pady=10, columnspan=2)

    button_run_all = Button(text="Scrape All", font=(FONT_NAME, 20), bg=COLOR2, command=scrape_all)
    button_run_all.grid(row=5, column=0, pady=10, columnspan=2)

    button_backup = Button(text="Data Management", font=(FONT_NAME, 20), bg=COLOR2, command=data_management)
    button_backup.grid(row=6, column=0, pady=10, columnspan=2)

    button_exit = Button(text="Exit Programme", font=(FONT_NAME, 20), bg=COLOR3, command=window.destroy)
    button_exit.grid(row=8, column=0, pady=10)

    button_main = Button(text="Main Menu", font=(FONT_NAME, 20), bg=COLOR3, command=go_main_menu)
    button_main.grid(row=8, column=1, pady=10)


# ---------------------------- UI SETUP FOR DASHBOARD ------------------------------- #

def get_shoes_dashboard():
    shoes_dashboard = Shoes_dashboard("../../data/")
    shoes_dashboard.run()
    # time.sleep(30)


def get_grocery_dashboard():
    grocery_dashboard = Grocery_dashboard("../../data/")
    grocery_dashboard.run()


def get_sg_rental_dashboard():
    Sg_rental_dashboard("../../data/")


def dashboard_menu():
    global window
    window.destroy()
    window = new_window()

    title = Label(text="Dashboard Menu", font=(FONT_NAME, 40), bg=COLOR1, fg=COLOR3)
    title.grid(row=0, column=0, columnspan=2)

    button_shoes_dashboard = Button(text="Skeachers Shoes Dashboard", font=(FONT_NAME, 20), bg=COLOR2,
                                    command=get_shoes_dashboard)
    button_shoes_dashboard.grid(row=1, column=0, pady=10, columnspan=2)

    button_grocery_dashboard = Button(text="Grocery Item Dashboard", font=(FONT_NAME, 20), bg=COLOR2,
                                      command=get_grocery_dashboard
                                      )
    button_grocery_dashboard.grid(row=2, column=0, pady=10, columnspan=2)

    button_sg_rental_dashboard = Button(text="Singapore Room Rental Dashboard", font=(FONT_NAME, 20), bg=COLOR2,
                                        command=get_sg_rental_dashboard
                                        )
    button_sg_rental_dashboard.grid(row=3, column=0, pady=10, columnspan=2)

    button_exit = Button(text="Exit Programme", font=(FONT_NAME, 20), bg=COLOR3, command=window.destroy)
    button_exit.grid(row=8, column=0, pady=10)

    button_main = Button(text="Main Menu", font=(FONT_NAME, 20), bg=COLOR3, command=go_main_menu)
    button_main.grid(row=8, column=1, pady=10)


def main_gui():
    global window
    window = new_window()
    title = Label(text="Web Scraping & Dashboard Programme", font=(FONT_NAME, 40), bg=COLOR1, fg=COLOR3)
    title.grid(row=0, column=0, )

    button_web_scraping = Button(text="Web Scraping Programme", font=(FONT_NAME, 20), bg=COLOR2,
                                 command=web_scrape_main_gui)
    button_web_scraping.grid(row=1, column=0, pady=10)

    button_dashboard = Button(text="Dashboard", font=(FONT_NAME, 20), bg=COLOR2,
                              command=dashboard_menu)
    button_dashboard.grid(row=2, column=0, )

    button_exit = Button(text="Exit Programme", font=(FONT_NAME, 20), bg=COLOR3, command=window.destroy)
    button_exit.grid(row=8, column=0, pady=10)

    window.mainloop()


def new_window():
    window = Tk()
    window.title('Web Scraping')
    window.config(padx=100, pady=20, bg=COLOR1)
    window.minsize(width=500, height=300)
    return window


# web_scrape_main_gui()
main_gui()
