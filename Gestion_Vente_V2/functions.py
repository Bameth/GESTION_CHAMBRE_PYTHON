import os
import shutil
from views import *
from datetime import *
from const import *
from fpdf import FPDF


def get_file_content(file_path: str) -> list:
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = [line.strip().split(',') for line in f.readlines()]
        return content
    except FileNotFoundError:
        print(f"Fichier introuvable : {file_path}")
        return []



def get_available_rooms(list_rooms: list) -> list:
    available_rooms = []
    available_rooms.insert(0, list_rooms[0])
    for room in list_rooms[1:]:
        if int(room[3]) > 0:
            available_rooms.append(room)
    return available_rooms


def get_room_by_id(list_room: list, IdP: int) -> list:
    for room in list_room[1:]:
        if IdP == int(room[0]):
            return room
    return None

def get_all_id_from_available(list_available: list) ->list:
    id_list = []
    for p in list_available[1:]:
        id_list.append(str(p[0]))
    return id_list



def get_id(list_room: list) -> int:
    id_put = ""
    while not (id_put.isdigit() and (id_put in get_all_id_from_available(list_room) or id_put == "0")):
        display_room(list_room)
        id_put = input("Entrez l'ID du chambre que vous voulez reserver : ")
        os.system("cls")
    return int(id_put)

def get_quantity(room_choosen: list) -> int:
    while True:
        print(f"Chambre choisi  : {room_choosen[1]}")
        qte = input("Pour combien de personne voulez-vous reserver? :")
        if not qte.isdigit():
            print("Veuillez entrer un nombre entier.")
            continue
        qte = int(qte)
        stock_quantity = int(room_choosen[3])

        if qte > stock_quantity:
            print(f"La quantité ne doit pas dépasser {stock_quantity}.")
        else:
            return qte

def ajouter_au_panier(panier, list_room, id_room, quantite):
    room = get_room_by_id(list_room, id_room)
    total = int(quantite) * int(room[2])
    description = room[4]
    panier.append([id_room, room[1], quantite, room[2],description, total])
    print("Chambre reserver avec succés!!")

    

def supprimer_du_panier(panier, id_room):
    for room in panier[1:len(panier)-1]:
        if int(room[0]) == id_room:
            panier.remove(room)
            print("Reservation supprimer du panier!")
            return
    print("L'ID de chambre n'a pas été trouvé dans le panier.")

def vider_panier(panier: list) -> list:
    panier = panier[:1]  # L'en-tête du panier
    return panier

def modifier_reservation(panier: list, list_room: list, rep: int):
    match(rep):
        case 1:
            id = get_id(list_room)
            qte = get_quantity(get_room_by_id(list_room, id))
            ajouter_au_panier(panier, list_room, id, qte)
        case 2:
            print("Voici votre reservation actuelle : ")
            id_room = get_id(panier)
            print(type(panier[0][0]))
            supprimer_du_panier(panier, id_room)
        case 3:
            panier = vider_panier(panier)

def annuler_reservation(panier):
    print("Voici votre réservation actuelle : ")
    display_room(panier)

    choix = input("Voulez-vous annuler une réservation ? [oui/non] ")

    if choix.lower() == "oui":
        id_room = input("Entrez l'ID de la chambre dont vous voulez annuler sa reservation : ")

        for room in panier:
            if str(room[0]) == id_room:
                panier.remove(room)
                print("La réservation a été annulée.")
                facture_file = f'fact_{id_room}.txt'
                if os.path.exists(facture_file):
                    destination = os.path.join('Gestion_Vente_V2', 'Factures', facture_file)
                    shutil.move(facture_file, destination)
                    print(f"Facture déplacée vers {destination}")
                else:
                    print(f"La facture {facture_file} n'existe pas.")

                return None

        print("L'ID de la chambre n'a pas été trouvé dans la réservation.")
    
    elif choix.lower() == "non":
        print("Aucune réservation n'a été annulée. Continuer avec la réservation actuelle.")

    else:
        print("Réponse invalide. Veuillez répondre 'oui' ou 'non'.")


def get_answer():
    while True:
        reponse = input("->")
        if not reponse.isdigit():
            continue
        else:
            return int(reponse) 


def get_answer_2(min: int, max :int):
    while True:
        reponse = get_answer()
        if reponse < min or reponse > max:
            continue
        else:
            return reponse
        
def update_room_database(room_id, quantity_sold, all_rooms_file, file_name: str):
    updated_rooms = []

    # Mettre à jour la quantité en stock du produit dans la liste de tous les produits
    for room in all_rooms_file:
        if room[0] == str(room_id):
            updated_quantity = int(room[3]) - quantity_sold
            room[3] = str(updated_quantity)
        updated_rooms.append(','.join(room))

    # Maintenant, écrire la liste mise à jour dans le fichier de tous les produits
    with open(file_name, "w", encoding="utf-8") as file:
        file.write('\n'.join(updated_rooms))



def main_loop(file_name: str, all_rooms: list, panier, available_rooms: list, somme: int = 0):
    while True:
        os.system("cls")
        print("-"*5, "BIENVENUE DANS NOTRE BREUKHI HOTEL", "-"*5)
        id = get_id(available_rooms)
        room = get_room_by_id(available_rooms, id)
        if not room == None:
            qte = get_quantity(room)
            if qte == 0:
                continue
            total = int(qte) * int(room[2])
            panier.append([id, room[1], qte, room[2], room[4],total])
            somme += total
            rep = input("Voulez-vous ajouter une autre chambre? [oui/non] ")
            if rep.upper() == "NON":
                return panier
            elif rep.upper() == "OUI":
                id_room = get_id(available_rooms)
                quantite = get_quantity(get_room_by_id(available_rooms, id_room))
                ajouter_au_panier(panier, available_rooms, id_room, quantite)

            

def input_choice(data: str) -> str:
    while True:
        display_menu(menu)
        choice = input("-> ")
        if choice not in data:
            continue
        else:
            return choice


def sauvegarder_reservation(file_name: str, data: list):
    with open(file_name, 'a') as file:
        for item in data:
            str_item = [str(i) for i in item]
            file.write(','.join(str_item) + '\n')

def generer_numero_vente():
    return datetime.now().strftime("%d%m%Y%H%M%S")

def enregistrer_reservation(reservation_file: str, numero_reservation: str, data: list):
    with open(reservation_file, 'a') as file:
        for item in data:
            str_item = [str(i) for i in item]
            file.write(f"{numero_reservation},{','.join(str_item)}\n")

def generer_facture(numero_commande: str, panier: list):
    with open(f"Fact_{numero_commande}.txt", "w") as facture:
        # name = "**********************FACTURE***********************\n"
        # facture.write(name)
        header = "Id,Type,Nombre de personne,PVu,Total\n"
        facture.write(header)
        somme = 0
        for item in panier:
            item.pop(4)
            somme += item[4]
            str_item = [str(i) for i in item]
            somme_str = ["-", "-", "-", "Total", str(somme)]
            facture.write(f"{','.join(str_item)}\n")
        facture.write(f"{','.join(somme_str)}")
    


def valider_panier(file_name_command: str, panier: list, all_rooms: list, file_name: str, shopping_cart_file: str, vente_file: str):
    numero_vente = generer_numero_vente()
    sauvegarder_reservation(shopping_cart_file, panier)
    sauvegarder_reservation(file_name_command, panier)
    for cmd in panier:
        id_room = cmd[0]
        qte_commandee = int(cmd[2])
        update_room_database(id_room, qte_commandee, all_rooms, file_name)
    enregistrer_reservation(vente_file, numero_vente, panier)
    generer_facture(numero_vente, panier)
    
    
def generer_facture_pdf(numero_commande: str, panier: list):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Facture", ln=True, align='C')

    pdf.ln(10)  # saut de ligne

    # En-tête du tableau
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(20, 10, txt="Id", border=1)
    pdf.cell(60, 10, txt="Type", border=1)
    pdf.cell(45, 10, txt="Nombre de personne", border=1)
    pdf.cell(20, 10, txt="PVu", border=1)
    pdf.cell(40, 10, txt="Total", border=1)
    pdf.ln()

    # Contenu du tableau
    pdf.set_font("Arial", size=12)
    somme = 0
    for item in panier:
        somme += int(item[3])
        pdf.cell(20, 10, txt=str(item[0]), border=1)
        pdf.cell(60, 10, txt=str(item[1]), border=1)
        pdf.cell(45, 10, txt=str(item[2]), border=1)
        pdf.cell(20, 10, txt=str(item[3]), border=1)
        pdf.cell(40, 10, txt=str(item[4]), border=1)
        pdf.ln()

    # Total
    pdf.cell(145, 10, txt="Total", border=1)
    pdf.cell(40, 10, txt=str(somme), border=1)

    pdf_file = f"Gestion_Vente_V2/Factures/Facture_{numero_commande}.pdf"
    pdf.output(pdf_file)

    print(f"Facture générée avec succès : {pdf_file}")



