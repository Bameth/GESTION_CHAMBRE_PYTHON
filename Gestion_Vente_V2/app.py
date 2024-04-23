from const import *
from functions import *
from views import *
from datetime import *
import shutil

# os.mkdir("./FacturesPDF")
rep = "OUI"
panier = []
# somme = 0
all_rooms = get_file_content(ROOM_FILE)
all_sale = get_file_content(SALE_FILE)
available_rooms = get_available_rooms(all_rooms)
my_cart = get_file_content(PANIER)
line_command = get_file_content(COMMAND_LINE)
main_loop(ROOM_FILE, all_rooms, panier, available_rooms)

# Menu principal
choice = input_choice('abc')

if choice == 'a':
    valider_panier(COMMAND_LINE, panier, all_rooms, ROOM_FILE, PANIER, SALE_FILE)
    print("Reservation validée avec succès!!!")
elif choice == 'b':
    annuler_reservation(panier)
else:
    display_menu(menu2)
    answer = get_answer_2(1, 3)
    modifier_reservation(panier, available_rooms, answer)
    valider_panier(COMMAND_LINE, panier, all_rooms, ROOM_FILE, PANIER, SALE_FILE)
    print("Commande validée avec succès!!!")

FACTURE_PATH = f'fact_{generer_numero_vente()}.txt'
facture = get_file_content(FACTURE_PATH)
display_room(facture)

# le chemin actuel du fichier
source = f'fact_{generer_numero_vente()}.txt'
# le chemin du dossier de destination
destination = 'Gestion_Vente_V2/Factures/'

# Vérifier si le fichier existe avant de le déplacer
if os.path.exists(source):
    try:
        # Déplacement du fichier vers le dossier de destination
        shutil.move(source, destination)
        print(f"Facture déplacée vers {destination}")
        
        # Générer la facture PDF après le déplacement
        generer_facture_pdf(generer_numero_vente(), panier)
        
    except Exception as e:
        print(f"Erreur lors du déplacement de la facture : {e}")




