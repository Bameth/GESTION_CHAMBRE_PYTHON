from tabulate import tabulate

def display_room(list_room: list) -> None:
    data = [p for p in list_room]
    print(tabulate(data, tablefmt="rounded_grid"))

def display_menu(msg: str):
    print(msg)

def test_menu() -> None:
    print("1{:.>20}".format("Produit1")) # aligner à droite
    print("1{:.<20}".format("Produit1")) # aligner à gauche
    print("1{:.^20}".format("Produit1"))

def make_title(titres: list, symb: str = "*", screen_width: int = 75) -> None:
    print(symb*screen_width)
    for titre in titres:
        print("{:^75}".format(titre))
    print(symb*screen_width)

