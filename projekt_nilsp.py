from cryptography.fernet import Fernet, InvalidToken
import argparse
from colorama import init, Fore, Style


init()

val1_text1 = "Du valde " + Fore.YELLOW + "nyckel" + Style.RESET_ALL + "\n"
val1_text2 = "Använd -n eller --nyckel och sedan namnet på den fil du vill skapa som ska innehålla nyckeln - för att kunna generera en symmetrisk nyckel. \n" 
val1_text3 = Fore.RED + "Använd .key hos namnet på din nyckel" + Style.RESET_ALL + Fore.GREEN +" (nyckel_exempel.key)" + Style.RESET_ALL + "\n"
full_text1 = val1_text1 + val1_text2 + val1_text3

val2_text1 = "Du valde " + Fore.YELLOW + "kryptera" + Style.RESET_ALL + "\n"
val2_text2 = "Använd -tn eller --ta_nyckel och skriv in filnamnet där den genererade nyckeln finns. \n"
val2_text3 = "Använd sedan -kf eller --kry_fil och skriv in filnamnet på den fil du vill kryptera. \n"
val2_text4 = "Exempel: " + Fore.GREEN + "(-tn nyckel_exempel.key -kf fil_exempel.txt)" + Style.RESET_ALL + "\n"
full_text2 = val2_text1 + val2_text2 + val2_text3 + val2_text4

val3_text1 = "Du valde " + Fore.YELLOW + "dekryptera" + Style.RESET_ALL + "\n"
val3_text2 = "Använd -dn eller --din_nyckel och skriv in filnamnet på nycklen tillhörande den krypterade filen. \n"
val3_text3 = "Använd sedan -df eller --dek_fil och skriv in den fil som du vill dekryptera. \n"
val3_text4 = "Exempel: " + Fore.GREEN + "(-dn nyckel_exempel.key -df fil_exempel.txt)" + Style.RESET_ALL + "\n"
full_text3 = val3_text1 + val3_text2 + val3_text3 + val3_text4

def val1():
    return

def val2():
    return

def val3():
    return

def main_arguments():
    parser = argparse.ArgumentParser(prog="Krypteringsverktyg för filer:")
    subparser = parser.add_subparsers(title="Kommandon", description="nyckel, kryptera, dekryptera")

    parser1 = subparser.add_parser("nyckel", help="Genererar en symmetrisk nyckel och sparar den i en fil.")
    parser1.set_defaults(function=val1)
    parser1.add_argument("-n", "--nyckel", help="Skapar en symmetrisk nyckel.")

    parser2 = subparser.add_parser("kryptera", help="Krypterar en fil med en befintlig nyckel.")
    parser2.set_defaults(function=val2)
    parser2.add_argument("-tn", "--ta_nyckel", help="Hämtar den skapade nyckeln.")
    parser2.add_argument("-kf", "--kry_fil", help="Skriv in namnet på den fil du vill kryptera.")
    
    parser3 = subparser.add_parser("dekryptera", help="Dekrypterar en krypterad fil.")
    parser3.set_defaults(function=val3)
    parser3.add_argument("-dn", "--din_nyckel", help="Hämtar din nyckel.")
    parser3.add_argument("-df", "--dek_fil", help="Skriv in namnet på den fil du vill dekryptera (OBS du måste ha rätt nyckel).")


    key = Fernet.generate_key()
    args = parser.parse_args()


    try:
        args.function()

    except AttributeError:
        print(Fore.RED + "ERROR: Du angav inget kommando" + Style.RESET_ALL + "\nAnge ett av följande kommandon:"+ Fore.YELLOW +"\nnyckel\nkryptera\ndekryptera" + Style.RESET_ALL)
        print("För mer information använd -h eller --help")
    
    try:
        if args.nyckel:
            print("Du har skapat en " + Fore.YELLOW + "nyckel" + Style.RESET_ALL)
            with open(args.nyckel, "wb") as filekey:
                filekey.write(key)
            print(f"En nyckel är skapad och sparad i filen: {args.nyckel}")
        

        elif not args.nyckel:
            print(full_text1)
            print("För ytterligare information använd -h eller --help")

    except AttributeError:
        pass


    try:
        if args.ta_nyckel:
            with open(args.ta_nyckel, "rb") as filekey: 
                key = filekey.read()
            fernet = Fernet(key)

            if not args.ta_nyckel or not args.kry_fil:
                print(Fore.RED + "ERROR: Du måste ange namnet på din fil också" + Style.RESET_ALL)
                exit()
        
        if args.kry_fil:
            with open(args.kry_fil, "rb") as file:
                original = file.read()

            encrypted = fernet.encrypt(original)

            with open(args.kry_fil, "wb") as encrypted_file:
                encrypted_file.write(encrypted)
                print(f"Filen: {args.kry_fil} är " + Fore.YELLOW + "krypterad" + Style.RESET_ALL)


        elif not args.ta_nyckel or not args.kry_fil:
            print(full_text2)
            print("För ytterligare information använd -h eller --help")

    except AttributeError:
        pass
    except UnboundLocalError:
        print(Fore.RED + "ERROR: Du måste ange filnamnet på din nyckel först" + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + "ERROR: Filen existerar inte" + Style.RESET_ALL)


    try:
        if args.din_nyckel:
            with open(args.din_nyckel, "rb") as filekey: 
                key = filekey.read()
            fernet = Fernet(key)

            if not args.din_nyckel or not args.dek_fil:
                print(Fore.RED + "ERROR: Du måste ange namnet på din fil också" + Style.RESET_ALL)
                exit()


        if args.dek_fil:
            with open(args.dek_fil, "rb") as enc_file:
                encrypted = enc_file.read()

            decrypted = fernet.decrypt(encrypted)

            with open(args.dek_fil, "wb") as dec_file:
                dec_file.write(decrypted)
                print(f"Filen: {args.dek_fil} är " + Fore.YELLOW + "dekrypterad" + Style.RESET_ALL)


        elif not args.din_nyckel or not args.dek_fil:
            print(full_text3)
            print("För ytterligare information använd -h eller --help")

    except AttributeError:
        pass
    except UnboundLocalError:
        print(Fore.RED + "ERROR: Du måste ange filnamnet på din nyckel först" + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + "ERROR: Filen existerar inte" + Style.RESET_ALL)
    except InvalidToken:
        print(Fore.RED + f"ERROR: " + Fore.YELLOW + args.din_nyckel + Fore.RED + " är en ogiltig eller fel nyckel för filen " + Fore.YELLOW + args.dek_fil + Style.RESET_ALL)



if __name__ == "__main__":
    main_arguments()