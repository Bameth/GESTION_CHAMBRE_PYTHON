ROOM_FILE = r'./Gestion_Vente_V2/db/Rooms.txt'
SALE_FILE = r'./Gestion_Vente_V2/db/reservation.txt'
COMMAND_LINE = r'./Gestion_Vente_V2/db/ligneCommande.txt'
PANIER = r'./Gestion_Vente_V2/db/panier.txt'



# constantes pour les menus

menu = """-------> Menu <--------
a.......Valider la reservation
b.......Annuler la reservation
c.......Modifier la reservation
"""
menu2 = """-------> Sous-Menu <--------
1.......Ajouter une nouvelle chambre
2......Retirer une chambre de la reservation
3.....Annuler toute la reservation
"""

en_tete_panier = ["Id", "Type", "Nombre de personne", "PVu", "Total"]
en_tete_vente = ["Numero_Vente","Id", "Type", "Nombre de personne", "PVu", "Total"]
