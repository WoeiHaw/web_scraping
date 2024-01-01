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
from job_dashboard import JobDashboard
from house_price_dashboard import HousePriceDashBoard

COLOR1 = "#FAF0E6"
COLOR2 = "#B9B4C7"
COLOR3 = "#5C5470"
COLOR4 = "352F44"
FONT_NAME = "Courier"

data_path = "data/"
backup_path = "Data_back_up/"
# ---------------------------- TRIGGER FOR WEB SCRAPPING ------------------------------- #
def skechers_shoes_my():
    Shoes("my", f"{data_path}skechers_shoes_MY.csv")


def skechers_shoes_sg():
    Shoes("sg", f"{data_path}skechers_shoes_SG.csv")


def kl_house():
    House_price(f"{data_path}House Price kl.csv", "kuala+lumpur")


def jb_house():
    House_price(f"{data_path}/House Price JB.csv", "johor+bahru")


def sg_job():
    Job_info(f"{data_path}/Singapore Job.csv", "sg")


def my_job():
    Job_info(f"{data_path}Malaysia Job.csv", "my")


def scrape_sg_room():
    Sg_room(f"{data_path}sg rental.csv")
    Process_data(data_path)


def scrape_coffee():
    Coffee(f"{data_path}kopi o price.csv")


def scrape_shower_gel():
    Dettol(f"{data_path}Dettol Shower Gel.csv")


def scrape_shampoo():
    Shapoo(f"{data_path}shampoo price.csv")


def scrape_face_wash():
    Facewash(f"{data_path}Nivea Man.csv")


def scrape_tooth_paste():
    Toothpaste(f"{data_path}Darlie Toothpaste.csv")


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
    Shoes("my", f"{data_path}skechers_shoes_MY.csv")
    Shoes("sg", f"{data_path}skechers_shoes_SG.csv")


def scrape_all_job():
    sg_job()
    my_job()


def scrape_all_house():
    House_price(f"{data_path}House Price kl.csv", "kuala+lumpur")
    House_price(f"{data_path}House Price JB.csv", "johor+bahru")


def get_shoes_image():
    Shoes_image("my")
    Shoes_image("sg")

def back_up_google_drive():
    Backup_drive(data_path)
def back_up():
    file_location = [
        f"{data_path}kopi o price.csv",
        f"{data_path}Dettol Shower Gel.csv",
        f"{data_path}shampoo price.csv",
        f"{data_path}Nivea Man.csv",
        f"{data_path}Darlie Toothpaste.csv",
        f"{data_path}skechers_shoes_MY.csv",
        f"{data_path}skechers_shoes_SG.csv",
        f"{data_path}sg rental.csv",
        f"{data_path}Malaysia Job.csv",
        f"{data_path}Singapore Job.csv",
        f"{data_path}House Price kl.csv",
        f"{data_path}House Price JB.csv",
        f"{data_path}sg rental(processed).csv",
        f"{data_path}Singapore Job(Processed).csv",
        f"{data_path}Malaysia Job(Processed).csv",
        f"{data_path}House Price kl(Processed).csv",
        f"{data_path}House Price JB(Processed).csv"
    ]
    backup_location = [
        f"{backup_path}kopi o price.csv",
        f"{backup_path}Dettol Shower Gel.csv",
        f"{backup_path}shampoo price.csv",
        f"{backup_path}Nivea Man.csv",
        f"{backup_path}Darlie Toothpaste.csv",
        f"{backup_path}skechers_shoes_MY.csv",
        f"{backup_path}skechers_shoes_SG.csv",
        f"{backup_path}sg rental.csv",
        f"{backup_path}Malaysia Job.csv",
        f"{backup_path}Singapore Job.csv",
        f"{backup_path}House Price kl.csv",
        f"{backup_path}House Price JB.csv",
        f"{backup_path}sg rental(processed).csv",
        f"{backup_path}Singapore Job(Processed).csv",
        f"{backup_path}Malaysia Job(Processed).csv",
        f"{backup_path}House Price kl(Processed).csv",
        f"{backup_path}House Price JB(Processed).csv"
    ]
    Backup(file_location, backup_location)

def download_data_drive():
    Download_data(data_path)
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

    download_data = Button(text="Download Data", font=(FONT_NAME, 20), bg=COLOR2, command=download_data_drive)
    download_data.grid(row=1, column=0, pady=10, columnspan=3)

    back_up_local = Button(text="Back Up Locally", font=(FONT_NAME, 20), bg=COLOR2, command=back_up)
    back_up_local.grid(row=2, column=0, pady=10, columnspan=3)

    back_up_drive = Button(text="Back Up - Google Drive", font=(FONT_NAME, 20), bg=COLOR2, command=back_up_google_drive)
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
    shoes_dashboard = Shoes_dashboard(data_path)
    shoes_dashboard.run()
    # time.sleep(30)


def get_grocery_dashboard():
    grocery_dashboard = Grocery_dashboard(data_path)
    grocery_dashboard.run()


def get_sg_rental_dashboard():
    Sg_rental_dashboard(f"{data_path}")


def get_job_dashboard():
    JobDashboard(data_path)


def get_house_price_dashboard():
    HousePriceDashBoard(data_path)


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

    job_dashboard = Button(text="Data Science Job Dashboard", font=(FONT_NAME, 20), bg=COLOR2,
                           command=get_job_dashboard
                           )
    job_dashboard.grid(row=4, column=0, pady=10, columnspan=2)

    houae_dashboard = Button(text="House Price Dashboard", font=(FONT_NAME, 20), bg=COLOR2,
                             command=get_house_price_dashboard
                             )
    houae_dashboard.grid(row=5, column=0, pady=10, columnspan=2)

    button_exit = Button(text="Exit Programme", font=(FONT_NAME, 20), bg=COLOR3, command=window.destroy)
    button_exit.grid(row=8, column=0, pady=10)

    button_main = Button(text="Main Menu", font=(FONT_NAME, 20), bg=COLOR3, command=go_main_menu)
    button_main.grid(row=8, column=1, pady=10)


def main_gui():
    global window
    window = new_window()
    title = Label(text="Web Scraping &\n Dashboard Programme", font=(FONT_NAME, 40), bg=COLOR1, fg=COLOR3)
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
