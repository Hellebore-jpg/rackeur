from typing import TypedDict # Gère les types de variables, ce script est écrit avec des types stictes
from pathlib import Path # Gère les chemins de fichiers
import unicodedata # Gère les actions sur les caractères unicode
import math # Gère les fonctions mathématiques
import csv # Gère la lecture et l'écriture de fichiers CSV

class CSVTable(TypedDict):
    header: list[str]
    body: list[list[str]]
    
DATA_DIR: Path = Path('assets/data/') # Dossier des fichiers CSV

def CREATE_CSV(path: str | Path = 'catalogue.csv', header: list[str] | None = None, delimeter: str = ',', overwrite: bool = False) -> Path:
    """Crée un fichier CSV vide (avec l'entête si elle est fournie) dans "assets/data/".

    Args:
        path (str | Path, optional): Chemin du fichier dans "assets/data/". Defaults to 'catalogue.csv'.
        header (list[str] | None, optional): Entête du tableau, None crée un fichier totalement vide. Defaults to None.
        delimeter (str, optional): Délimitation utilisée par le fichier CSV. Defaults to ','.
        overwrite (bool, optional): Autorise l'écrasement d'un fichier existant. Defaults to False.

    Returns:
        Path: Chemin complet du fichier créé.

    Raises:
        FileExistsError: Si le fichier existe déjà et que overwrite vaut False.
    """
    full_path: Path = Path(DATA_DIR, path)
    full_path.parent.mkdir(parents=True, exist_ok=True) # Crée les dossiers manquants
    with open(full_path, 'w' if overwrite else 'x', newline='', encoding='utf-8') as f: # 'x' échoue si le fichier existe déjà
        if header:
            csv.writer(f, delimiter=delimeter).writerow(header)
    return full_path

class Catalogue:
    """Classe permetant d'importer et d'interagir facilement avec un fichier CSV.
    """
    def __init__(self, path: str | Path = 'catalogue.csv', delimeter: str = ','):
        """Importation d'un fichier CSV.

        Args:
            path (str | Path, optional): Chemin du fichier catalogue dans "assets/data/". Defaults to 'catalogue.csv'.
            delimeter (str, optional): Délimitation utilisée par le fichier CSV. Defaults to ','.
        """
        self.PATH: Path = Path(DATA_DIR, path)
        self.DELIMETER: str = delimeter
        _csv: CSVTable = self.import_csv()
        self.HEAD: list[str] = _csv['header']
        self.BODY: list[list[str]] = _csv['body']

    def import_csv(self) -> CSVTable:
        """Importe les valeurs du fichier CSV spécifié dans la classe.

        Returns:
            CSVTable: Dictionaire contenant l'entête et le corps du CSV.
        """
        with open(self.PATH, 'r', encoding='utf-8', newline='') as f:
            table: list[list[str]] = list(csv.reader(f, delimiter=self.DELIMETER))
            if not table: # Fichier totalement vide
                return {'header': [], 'body': []}
            return {'header': table[0], 'body': table[1:]}

    def SAVE_CSV(self):
        """Sauvegarde les modifications apportées dans la classe dans le fichier CSV.
        """
        with open(self.PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=self.DELIMETER)
            writer.writerow(self.HEAD)
            writer.writerows(self.BODY)

    # (C)RUD
    def CREATE(self, item: list[object], index: int = -1):
        """Crée une nouvelle ligne dans le fichier CSV et l'insère à un endroit précis si besoin.

        Args:
            item (list[object]): Ligne à ajouter.
            index (int, optional): Position de l'insertion, les valeurs négatives ajoute la ligne à la fin de la liste. Defaults to -1.
        """
        insert: list[str] = [str(i) for i in item]
        if index < 0:
            self.BODY.append(insert)
        else:
            self.BODY.insert(index, insert)

    # CR(U)D
    def UPDATE(self, item: object | list[object], coords: int | list[int] = 0):
        """Modifie la ou les valeurs séléctionnées du fichier CSV.

        Args:
            item (object | list[object]): Nouvelle valeur(s) à insérer.
            coords (int | list[int], optional): Index de la ligne à éditer, si cette valeur est une liste de 2 élément, le deuxième définit l'index de la colonne. Defaults to 0.
        """
        if isinstance(coords, int) and isinstance(item, list):
            self.BODY[coords] = [str(i) for i in item]
        elif isinstance(coords, list) and not isinstance(item, list):
            self.BODY[coords[0]][coords[1]] = str(item)
        else:
            print('Error : Cannot add a single item to replace an entire line.')

    def UPDATE_HEADER(self, item: str | list[str], index: int | None =  None) -> None:
        """Modifie l'entête ou une de ses valeurs.

        Args:
            item (str | list[str]): Valeur ou entête de remplacement.
            index (int | None, optional): Index d'une cellule spécifique. Defaults to None.
        """
        if isinstance(item, list) and index is None:
            self.HEAD = item
        elif isinstance(item, str) and isinstance(index, int):
            self.HEAD[index] = item
            
    # CRU(D)
    def DELETE(self, index: int = -1) -> list[str]:
        """Supprime et renvoit une ligne du fichier CSV.

        Args:
            index (int, optional): Index de la ligne. Defaults to -1.

        Returns:
            list[str]: Ligne supprimée.
        """
        return self.BODY.pop(index)

def _normalize(text: str) -> str:
    """Renvoie les caractères en minuscules sans accents, ex :"Éclair" -> "eclair".

    Args:
        text (str): Texte d'entrée.

    Returns:
        str: Texte normalisé.
    """
    decomposed: str = unicodedata.normalize('NFD', text)
    return ''.join(c for c in decomposed if unicodedata.category(c) != 'Mn').casefold() # Le check ici permet de retirer les accents "NonSpacing Marks"

def _cell(row: list[str], column: int) -> str:
    """Renvoie la cellule d'une ligne ou si la colonne n'existe pas.

    Args:
        row (list[str]): Ligne.
        column (int): Index de la colonne.

    Returns:
        str: Valeur de la cellule en chaine de caractère ou ''.
    """
    return row[column] if -len(row) <= column < len(row) else ''

def _to_float(text: str) -> float | None:
    """Convertit un texte en nombre (accepte la virgule décimale), None si impossible.

    Args:
        text (str): Nombre au format texte.

    Returns:
        float | None: Texte converti en nombre décimal.
    """
    try:
        value: float = float(text.strip().replace(' ', '').replace(',', '.')) # Met le texte en forme pour une plus grande souplesse
    except ValueError:
        return None
    return None if math.isnan(value) else value # Check que la valeur renvoyée soit valide et pas NaN (Not a Number)

# C(R)UD
class Catalogue_Reader:
    """Classe regroupant toutes les fonctions permettant d'afficher, de trier ou de rechercher les données d'un tableau CSV.
    """
    def __init__(self, catalogue: Catalogue, start: int = 0, end: int = 0) -> None:
        """Importe un morceau du fichier CSV contenu dans le Catalogue utilisé pour pouvoir y extraire des informations.

        Args:
            catalogue (Catalogue): Catalogue CSV.
            start (int, optional): Index de la première ligne du segment utilisé. Defaults to 0.
            end (int, optional): Index de la dernière ligne du segment utilisé. Defaults to 0.
        """
        if end == 0:
            end = len(catalogue.BODY)
        self.HEAD: list[str] = catalogue.HEAD
        self.BODY: list[list[str]] = catalogue.BODY[start:end]
        
    def SELECT(self, index: int) -> list[str]:
        """Séléctionne une seule ligne parmi le segment utilisé du fichier CSV et supprime les autres du corps du lecteur.

        Args:
            index (int): Index relatif au premier index du segment (considéré comme 0).

        Returns:
            list[str]: Ligne séléctionnée.
        """
        self.BODY = [self.BODY[index]]
        return self.BODY[0]
    
    def ALPHA_SORT(self, column: int = 0, reverse: bool = False) -> list[list[str]]:
        """Renvoie le segment du fichier CSV séléctionné trié dans l'ordre alphabétique par la colonne {column} et met à jour le corp du lecteur.

        Args:
            column (int, optional): Index de la colonne sur laquelle se baser. Defaults to 0.
            reverse (bool, optional): Inverse l'ordre. Defaults to False.

        Returns:
            list[list[str]]: Segment séléctionné trié.
        """
        self.BODY = sorted(self.BODY, key=lambda r: _normalize(_cell(r, column)), reverse=reverse)
        # Note & Mémo :
        # Lambda est une fonction anonyme, elle ne s'appelle pas et est écrite sur une seule ligne pour symboliser une expression.
        # Dans sorted() elle sert à déterminer la manière de trier les éléments.
        return self.BODY
        
    def NUM_SORT(self, column: int = 0, reverse: bool = False) -> list[list[str]]:
        """Renvoie le segment du fichier CSV séléctionné trié dans l'ordre croissant par la colonne {column} et met à jour le corp du lecteur.
    
        Args:
            column (int, optional): Index de la colonne sur laquelle se baser. Defaults to 0.
            reverse (bool, optional): Trie dans l'ordre décroissant. Defaults to False.

        Returns:
            list[list[str]]: Segment séléctionné trié.
        """
        numeric: list[tuple[float, list[str]]] = []
        others: list[list[str]] = []
        for row in self.BODY:
            value: float | None = _to_float(_cell(row, column))
            if value is None:
                others.append(row) # Ajoute les valeurs non numériques à la fin de la liste triée
            else:
                numeric.append((value, row)) # Ajoute les valeurs détéctée comme numérique malgrès le format non conventionel à la liste
        numeric.sort(key=lambda pair: pair[0], reverse=reverse)
        # Note & Mémo :
        # Lambda est une fonction anonyme, elle ne s'appelle pas et est écrite sur une seule ligne pour symboliser une expression.
        # Dans .sort() elle sert à trier la liste "numeric" par sa première colonne, celle qui contient la valeur numérique à utiliser.
        self.BODY = [row for _, row in numeric] + others # Retire la colonne de la valeur numérique des lignes du résultat pour les reformater
        return self.BODY
        
    def SEARCH(self, query: str, columns: list[int] = [-1]) -> list[list[str]]:
        """Renvoie une partie du segment du fichier CSV séléctionné qui correspond à la recherche entrée sur la colonne {column} et met à jour le corp du lecteur.

        Args:
            query (str): Recherche.
            columns (list[int], optional): Index de la colonne sur laquelle appliquer la recherche, -1 signifie toutes les colonnes. Defaults to [-1].

        Returns:
            list[list[str]]: Segment séléctionné correspondant à la recherche.
        """
        needle: str = _normalize(query)
        all_columns: bool = -1 in columns

        def matches(row: list[str]) -> bool:
            """Renvoie si la ligne correspond à la recherche.

            Args:
                row (list[str]): Ligne du fichier CSV.

            Returns:
                bool: Correspondance.
            """
            cells: list[str] = row if all_columns else [_cell(row, c) for c in columns]
            return any(needle in _normalize(cell) for cell in cells) # Renvoie vrai si n'importe quelle case observée de la ligne correspond.

        self.BODY = [row for row in self.BODY if matches(row)]
        return self.BODY

    def READ(self, types: list[type] = [str]) -> list[object] | list[list[object]]:
        """Renvoie la section séléctionnée du fichier CSV avec types par colonnes.

        Args:
            types (list[type]): Types utilisés par chaque colonne, se répète en boucle. Defaults to [str].

        Returns:
            list[list[object]] | list[object]: Ligne ou liste de lignes avec les valeurs converties.
        """
        
        def to_type(item: str, rtype: type = str) -> object:
            """Converti une chaîne de caractères en valeur d'un autre type.

            Args:
                item (str): Chaine de caractères.
                rtype (type | None): Type de la valeur de sortie.

            Returns:
                object: Valeur convertie.
            """
            if rtype is str:
                return item
            if rtype is bool: # Cas particulier : bool("False") vaut True, car pour les chaines de caractères la fonction ne regarde que si la chaine est vide ou pas.
                return item.strip().lower() in ('true', '1', 'yes', 'oui', 'vrai')
            return rtype(item)
                
        types = types or [str]
        converted = [[to_type(cell, types[i % len(types)]) for i, cell in enumerate(row)] for row in self.BODY]
        if len(converted) == 1:
            return converted[0] # Ligne simple
        return converted # Liste de lignes
    
    def PRINT_CSV(self, pretty: bool = True) -> None:
        """Affiche une entête et un corps dans le terminal comme un tableau CSV.

        Args:
            pretty (bool, optional): Améliore l'affichage avec du padding. Defaults to True.
        """
        header: list[str] = [str(h) for h in self.HEAD]

       # Transforme toutes les valeurs en texte
        rows: list[list[str]] = [[str(c) for c in r] for r in self.BODY if isinstance(r, list)]

       # Padding : Calcul de la largeur maximum des éléments de chaque colonnes
        n_cols: int = max([len(header)] + [len(r) for r in rows])
        widths: list[int] = [0] * n_cols
        if pretty:
            for row in [header, *rows]:
                for i, cell in enumerate(row):
                    widths[i] = max(widths[i], len(cell))

        def frmat(row: list[str]) -> str:
            """Formate une liste en texte.

            Args:
                row (list[str]): Liste de valeurs.

            Returns:
                str: Ligne CSV séparée par "|" et avec padding.
            """
            return ' | '.join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip()

        print(frmat(header))
        if pretty:
            print('-+-'.join('-' * w for w in widths)) # Ligne de séparation décorative sous l'entête
        for row in rows:
            print(frmat(row))
            
def TESTING():
    pass

if __name__ == '__main__':
    TESTING()