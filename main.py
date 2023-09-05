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
import time

COLOR1 = "#FAF0E6"
COLOR2 = "#B9B4C7"
COLOR3 = "#5C5470"
COLOR4 = "352F44"
FONT_NAME = "Courier"


# ---------------------------- TRIGGER FOR WEB SCRAPPING ------------------------------- #
def skechers_shoes_my():
    Shoes("my", "../../skechers_shoes_MY.csv")


def skechers_shoes_sg():
    Shoes("sg", "../../skechers_shoes_SG.csv")


def kl_house():
    House_price("../../House Price kl.csv", "kuala+lumpur")


def jb_house():
    House_price("../../House Price JB.csv", "johor+bahru")


def sg_job():
    Job_info("../../Singapore Job.csv", "sg")


def my_job():
    Job_info("../../Malaysia Job.csv", "my")


def scrape_all():
    scrape_all_grocerries()

    Sg_room()

    scrape_all_job()

    scrape_all_house()


def scrape_all_grocerries():
    Coffee()
    Dettol()
    Shapoo()
    Facewash()
    Toothpaste()
    Shoes("my", "../../skechers_shoes_MY.csv")
    Shoes("sg", "../../skechers_shoes_SG.csv")


def scrape_all_job():
    sg_job()
    my_job()


def scrape_all_house():
    House_price("../../House Price kl.csv", "kuala+lumpur")
    House_price("../../House Price JB.csv", "johor+bahru")


def back_up():
    file_location = [
        "../../kopi o price.csv",
        "../../Dettol Shower Gel.csv",
        "../../shampoo price.csv",
        "../../Nivea Man.csv",
        "../../Darlie Toothpaste.csv",
        "../../skechers_shoes_MY.csv",
        "../../skechers_shoes_SG.csv",
        "../../sg rental.csv",
        "../../Malaysia Job.csv",
        "../../Singapore Job.csv",
        "../../House Price kl.csv",
        "../../House Price JB.csv",
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
    ]
    Backup(file_location, backup_location)
    pass


# ---------------------------- UI SETUP ------------------------------- #
window = None


def groceries_menu():
    global window
    window.destroy()
    window = new_window()

    title = Label(text="Grocerries Item", font=(FONT_NAME, 40), bg=COLOR1, fg=COLOR3)
    title.grid(row=0, column=1, columnspan=2)

    button_coffe = Button(text="Kluang Kopi O Kosong", font=(FONT_NAME, 20), bg=COLOR2, command=Coffee)
    button_coffe.grid(row=1, column=1, pady=5, columnspan=2)

    button_shower_gel = Button(text="Dettol Shower Gel", font=(FONT_NAME, 20), bg=COLOR2, command=Dettol)
    button_shower_gel.grid(row=2, column=1, pady=5, columnspan=2)

    button_shampoo = Button(text="Head and Shoulder Shampoo", font=(FONT_NAME, 20), bg=COLOR2, command=Shapoo)
    button_shampoo.grid(row=3, column=1, pady=5, columnspan=2)

    button_facewash = Button(text="Nivea Man Face-wash", font=(FONT_NAME, 20), bg=COLOR2, command=Facewash)
    button_facewash.grid(row=4, column=1, pady=5, columnspan=2)

    button_toothpaste = Button(text="Darlie Toothpaste", font=(FONT_NAME, 20), bg=COLOR2, command=Toothpaste)
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

    button_main_menu = Button(text="Main Menu", font=(FONT_NAME, 20), bg=COLOR3, command=go_main)
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

    button_main_menu = Button(text="Main Menu", font=(FONT_NAME, 20), bg=COLOR3, command=go_main)
    button_main_menu.grid(row=4, column=2, padx=20, pady=20, columnspan=2)


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

    button_main_menu = Button(text="Main Menu", font=(FONT_NAME, 20), bg=COLOR3, command=go_main)
    button_main_menu.grid(row=4, column=2, padx=20, pady=20, columnspan=2)


def go_main():
    global window
    window.destroy()
    main_gui()


def main_gui():
    global window
    window = new_window()
    title = Label(text="Web Scraping Programme", font=(FONT_NAME, 40), bg=COLOR1, fg=COLOR3)
    title.grid(row=0, column=0, )

    button_groceries = Button(text="Groceries Items", font=(FONT_NAME, 20), bg=COLOR2, command=groceries_menu)
    button_groceries.grid(row=1, column=0, pady=10)

    button_sg_room = Button(text="Singapore Room Rental Information ", font=(FONT_NAME, 20), bg=COLOR2,
                            command=Sg_room)
    button_sg_room.grid(row=2, column=0, pady=10)

    button_job = Button(text="Data Science Job Information ", font=(FONT_NAME, 20), bg=COLOR2,
                        command=data_science_job_gui)
    button_job.grid(row=3, column=0, pady=10)

    button_house_price = Button(text="Johor Bahru and Kuala Lumpur House Price", font=(FONT_NAME, 20), bg=COLOR2,
                                command=house_price_gui)
    button_house_price.grid(row=4, column=0, pady=10)

    button_run_all = Button(text="Scrape All", font=(FONT_NAME, 20), bg=COLOR2, command=scrape_all)
    button_run_all.grid(row=5, column=0, pady=10)

    button_backup = Button(text="Backup", font=(FONT_NAME, 20), bg=COLOR2, command=back_up)
    button_backup.grid(row=6, column=0, pady=10)

    button_exit = Button(text="Exit Programme", font=(FONT_NAME, 20), bg=COLOR3, command=window.destroy)
    button_exit.grid(row=7, column=0, pady=10)

    window.mainloop()


def new_window():
    window = Tk()
    window.title('Web Scraping')
    window.config(padx=100, pady=20, bg=COLOR1)
    window.minsize(width=500, height=300)
    return window


main_gui()
