import requests, os, shutil, json
from bs4 import BeautifulSoup
from tqdm import tqdm
from colorama import Fore, Style

def printHeader(text:str):
    print(f"{Fore.BLUE}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def printOption(number:int, text:str):
    print(f"[{Fore.RED}{Style.BRIGHT}{number}{Style.RESET_ALL}] {text}")

def printError(text:str):
    return print(f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def downloadMangaMenu(message:str=None, messageType:int=None):
    while True:
        os.system("cls")

        """
        MessageType code and meaning:
        0 = Success
        1 = Error
        """

        if not message == None:
            if messageType == 0:
                print(f"{Fore.GREEN}{Style.BRIGHT}{message} is saved to Downloads folder.{Style.RESET_ALL}\n")
                print("Download Success!")
                print("Download Again!\n")
            if messageType == 1:
                printError(message)
                print("\nDownload Failed!\n")

        printHeader("========== NHentai Downloader By Charlzk (Download Manga) ==========\n")
        print(f"{Fore.GREEN}{Style.BRIGHT}How to use?{Style.RESET_ALL}")
        print(f"1. Copy the URL or ID of the {Fore.RED}{Style.BRIGHT}nhentai.net{Style.RESET_ALL} manga you want to download.")
        print(f"2. Paste it into the input below.")
        print(f"{Fore.GREEN}{Style.BRIGHT}Important Note:{Style.RESET_ALL} make sure the Cookies and Headers are working or else it won't work.")

        choice = input("\nInput (Enter '<' to return to Main Menu): ")

        cookies = {}
        headers = {}

        with open("./Cookies.json", "r", encoding="utf-8") as file:
            jsons =json.loads(file.read())
            cookies = {
                'cf_clearance': jsons["cf_clearance"],
                'csrftoken': jsons["csrftoken"],
            }
        with open("./Headers.json", "r", encoding="utf-8") as file:
            jsons =json.loads(file.read())
            headers = {
                'user-agent': jsons["user-agent"],
            }

        if choice == "<":
            return mainMenu()
        else:
            return downloadManga(url=choice, cookies=cookies, headers=headers)

class listDownloads:
    def __init__(self) -> None:
        pass

    def main(self):
        while True:
            os.system("cls")
            printHeader("========== NHentai Downloader By Charlzk (Downloads) ==========\n")
            print(f"Your downloaded manga can be found on the {Fore.GREEN}{Style.BRIGHT}Downloads{Style.RESET_ALL} folder\n")

            if not len(os.listdir("./Downloads")) == 0:
                for i in os.listdir("./Downloads"):
                    if os.path.isdir("./Downloads"):
                        print(f"{Fore.GREEN}{Style.BRIGHT}{i}{Style.RESET_ALL}")
            else:
                printError("You don't have any downloaded manga.")

            options = {
                1: "Open Download",
                2: "Delete Download",
                3: "Return",
            }

            print("")
            for i, o in options.items():
                printOption(i, o)

            try:
                choice = int(input("\nChoice: "))
            except Exception as error:
                print("Error: " + str(error))

            if choice == 1:
                return self.openManga()
            elif choice == 2:
                return self.deleteManga()
            elif choice == 3:
                return mainMenu()
            else:
                print("Hello world")

    def openManga(self):
        os.system("cls")
        printHeader("========== NHentai Downloader By Charlzk (Downloads) (Open) ==========\n")

        if not len(os.listdir("./Downloads")) == 0:
            for i in os.listdir("./Downloads"):
                if os.path.isdir("./Downloads"):
                    print(f"{Fore.GREEN}{Style.BRIGHT}{i}{Style.RESET_ALL}")
        else:
            printError("You don't have any downloaded manga.")
        
        choice = input("\nInput (Enter '<' to return to Main Menu): ")

        for i in os.listdir("./Downloads"): 
            if choice == i: os.system(f"explorer Downloads/{choice}")
            
        return self.main()
    
    def deleteManga(self):
        os.system("cls")
        printHeader("========== NHentai Downloader By Charlzk (Downloads) (Open) ==========\n")

        if not len(os.listdir("./Downloads")) == 0:
            for i in os.listdir("./Downloads"):
                if os.path.isdir("./Downloads"):
                    print(f"{Fore.GREEN}{Style.BRIGHT}{i}{Style.RESET_ALL}")
        else:
            printError("You don't have any downloaded manga.")
        
        choice = input("\nInput (Enter '<' to return to Main Menu): ")

        for i in os.listdir("./Downloads"): 
            if choice == i: shutil.rmtree(f"./Downloads/{i}")
            
        return self.main()

def openCookies():
    return os.system("Cookies.json")

def openHeaders():
    return os.system("Headers.json")

def mainMenu():
    downloads = listDownloads()

    while True:
        os.system("cls")

        if not os.path.exists("./Cookies.json"):
            with open("./Cookies.json", "w", encoding="utf-8") as file: file.write(json.dumps({"cf_clearance": "", "csrftoken": ""}, indent=4))
        if not os.path.exists("./Headers.json"):
            with open("./Headers.json", "w", encoding="utf-8") as file: file.write(json.dumps({"user-agent": ""}, indent=4))

        printHeader("========== NHentai Downloader By Charlzk ==========\n")
    
        options = {
            1: "Download Manga",
            2: "Downloads",
            3: "Open Cookies",
            4: "Open Headers",
        }

        for i, j in options.items():
            printOption(i, j)

        try:
            choice = int(input("\nChoice: "))
        except Exception as error:
            return printError("Error: " + str(error))

        if choice == 1:
            return downloadMangaMenu()
        elif choice == 2:
            return downloads.main()
        elif choice == 3:
            openCookies()
        elif choice == 4:
            openHeaders()
        else:
            print("Hello world")

def main():
    mainMenu()
    return

def downloadManga(url:str, cookies:object, headers:object):
    print(f"\n{Fore.GREEN}Now downloading...{Style.RESET_ALL}\n")

    if not os.path.exists("./Downloads"): os.mkdir("./Downloads")

    if "https://nhentai.net/g/" in url:
        res = requests.get(url, headers=headers, cookies=cookies)
    else:
        res = requests.get("https://nhentai.net/g/" + url, headers=headers, cookies=cookies)
    
    if cookies["cf_clearance"] == "" or cookies["csrftoken"] == "":
        return downloadMangaMenu("One of the element in Cookies.json is empty.", 1)
    if headers["user-agent"] == "":
        return downloadMangaMenu("user-agent in Headers.json is empty.", 1)
    
    if not res.status_code == 200:
        return downloadMangaMenu(f"HTTP Error: " + str(res.status_code), 1)
    
    soup = BeautifulSoup(res.text, "html.parser")
    gallerythumb = soup.find_all("a", { "class": "gallerythumb" })

    for i in gallerythumb:
        res = requests.get("https://nhentai.net" + i["href"], headers=headers, cookies=cookies)
        foldername = i["href"].split("/")[2]
        filename = i["href"].split("/")[3] + ".jpg"
        soup = BeautifulSoup(res.text, "html.parser")
        img_src = soup.find_all("img")[1]["src"]

        if os.path.exists("./Downloads/" + foldername):
            res = requests.get(img_src, cookies=cookies, headers=headers)
            total_size = int(res.headers.get("content-length", 0))
            progress = tqdm(total=total_size, unit="B", unit_scale=True, desc=filename)

            with open(f"./Downloads/{foldername}/{filename}", "wb") as file:
                for data in res.iter_content(chunk_size=1024):
                    progress.update(len(data))
                    file.write(data)
            progress.close()
        else:
            os.mkdir("./Downloads/" + foldername)

    return downloadMangaMenu(url, 0)

if __name__ == "__main__":
    main()