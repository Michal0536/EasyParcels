# TBA:
# - mongoDB integration
# - PODs download
# - schedule a delivery 

from utils import *

class main:
    def __init__(self):
        isExist = os.path.exists('config.json')
        if isExist != True:
            log(Fore.RED+f"config.json missing!")

        with open('config.json',encoding='utf-8') as fetch_config_f:
            fetch_config = json.loads(fetch_config_f.read())
            licence_whop = fetch_config['config']['licence']
            
        #check licence 
        #update 'checkWhopLicence' with your data or leave it
        # self.valid = checkWhopLicence(licence_whop)
        self.valid = {"current_user":"Michal"}

        self.kurierzy_color = Fore.LIGHTCYAN_EX
        self.banner = pyfiglet.figlet_format('Kurierzy AIO', font = "chunky")
        
        with open("MyParcels.json",'r') as myParcels:
            self.MyParcels = json.loads(myParcels.read())

        


    def cli(self):
        if self.valid != False:
            self.current_user = self.valid.get('current_user')

            ###WELCOME BANNER
            os.system('cls')
            print(self.kurierzy_color + self.banner + Style.RESET_ALL)
            print(f"Welcome back {self.kurierzy_color}{self.current_user}{Style.RESET_ALL}!\n")
            
            menu_choices = [inquirer.List('first_menu_option',
                                        choices=['Track my parcels','Track any parcel','Schedule delivery','Download PODs','Exit']
            )]

            first_menu_choice = inquirer.prompt(menu_choices)
            
            try:
                ### TRACK MY PARCELS
                if first_menu_choice.get('first_menu_option') == "Track my parcels":
                    os.system('cls')
                    print(self.kurierzy_color + self.banner + Style.RESET_ALL)
                    
                    for parcel in self.MyParcels['myParcels']:
                        print(f"Tracking: {parcel['tracking']}")
                        print(f"Status: {parcel['status']}")
                        print(f"Shipment date: {parcel['shipment date']}")
                        print(f"Delivery Date: {parcel['delivery date']}")
                        

                    back = int(input("\nPress 0 to back to menu\n"))
                    if back == 0:
                        os.system('cls')
                        self.cli()

                ### TRACK ANY PARCEL
                if first_menu_choice.get('first_menu_option') == "Track any parcel":
                    os.system("cls")
                    print(Fore.LIGHTCYAN_EX + self.banner + Style.RESET_ALL)
                    second_menu_courier = [inquirer.List('second_menu_option',
                                            choices=['PL_Packages','PostNL']
                        )]
                    second_menu_choice = inquirer.prompt(second_menu_courier)

                    #epaka
                    if second_menu_choice.get("second_menu_option") == "PL_Packages":
                        
                        tracking = str(input('Paste number of your parcel: '))
                        for i in trackepaka(tracking)['AllSteps']:
                            temp = f"{i.get('time')} - {i.get('location')} - {i.get('status_code_desc')}"
                            print(temp)

                            
                
                    #PostNL 
                    if second_menu_choice.get('second_menu_option') == "PostNL":
                    
                        tracking = str(input('Paste number of your parcel: '))
                        print(PostNL_tracking(tracking))

                        
                    back = int(input("Press 0 to back to menu\n"))
                    if back == 0:
                        os.system('cls')
                        self.cli()

                ### SCHEDULE A DELIVERY      
                if first_menu_choice.get('first_menu_option') == "Schedule delivery":
                    print('TBA')
                    time.sleep(3)
                    self.cli()

                ### Download PODs
                if first_menu_choice.get('first_menu_option') == "Download PODs":
                    print('TBA')
                    time.sleep(3)
                    self.cli()
                ### EXIT
                if first_menu_choice.get('first_menu_option') == "Exit":
                    print("Bye!")
                    exit()

            except Exception as e:
                for i in range(3,0,-1):
                    print(f"{Fore.LIGHTRED_EX}Unexpected error occurred! Returning to menu in {i}{Style.RESET_ALL}")
                    time.sleep(1)
                logging.error(f"{datetime.now()} [{self.current_user}] {str(e)}")
                os.system('cls')
        


if __name__ == "__main__":
    main().cli()