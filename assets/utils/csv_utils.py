from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctionsfrom contextlib import contextmanager #

from contextlib import contextmanager # Gère les blocs "with" personnalisés (utilisé pour la BDD temporaire)
from collections.abc import Generator # 
from typing import TypedDict # Gère les types de variables, ce script est écrit avec des types stictes
from pathlib import Path # Gère les chemins de fichiers
import unicodedata # Gère les actions sur les caractères unicode
import tempfile # Gère les fichiers et dossiers temporaires
import math # Gère les fonctions mathématiques
import csv # Gère la lecture et l'écriture de fichiers CSV

# Seuls ces classes sont exportés avec "from csv_utils import *", tout le reste est interne au script.
__all__ = [
    'CSVTable', 'IndexedRow', 'DATA_DIR',
    'CREATE_FILE', 'TEMP_DB',
    'Database', 'DB_Reader',
]

IndexedRow = tuple[int, list[str]] # (Index réel de la ligne dans la BDD, Ligne)

class CSVTable(TypedDict):
    header: list[str]
    body: list[list[str]]
    
DATA_DIR: Path = Path('assets/data/') # Dossier des fichiers CSV

def CREATE_FILE(path: str | Path = 'catalogue.csv', header: list[str] | None = None, delimeter: str = ',', overwrite: bool = False) -> Path:
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
    if full_path.exists() and not overwrite: # Arrête si le fichier existe déjà et que l'écrasement est désactivé
        return full_path
    full_path.parent.mkdir(parents=True, exist_ok=True) # Crée les dossiers manquants
    with open(full_path, 'w', newline='', encoding='utf-8') as f:
        if header:
            csv.writer(f, delimiter=delimeter).writerow(header)
    return full_path

@contextmanager
def TEMP_DB(header: list[str], rows: list[list[object]], delimeter: str = ',') -> Generator[Database]:
    """Crée un fichier CSV temporaire rempli avec {rows} et fournit la BDD correspondant. Le fichier est supprimé à la sortie du bloc "with".
 
    Exemple :
        with TEMP_DB(['nom', 'prix'], [['Pomme', 1.5]]) as db:
            print(db.READER().READ())
 
    Args:
        header (list[str]): Entête du tableau.
        rows (list[list[object]]): Lignes du corps du tableau.
        delimeter (str, optional): Délimitation utilisée par le fichier CSV. Defaults to ','.
 
    Yields:
        Catalogue: Catalogue lié au fichier temporaire.
    """
    with tempfile.TemporaryDirectory() as tmp_dir: # Le dossier (et son contenu) disparaît à la fin du with
        path: Path = CREATE_FILE(Path(tmp_dir, 'test.csv'), header, delimeter, overwrite=True)
        catalogue: Database = Database(path, delimeter)
        for row in rows:
            catalogue.CREATE(row)
        catalogue.SAVE_FILE()
        yield catalogue

class Database:
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
        _csv: CSVTable = self.__import_csv()
        self.HEAD: list[str] = _csv['header']
        self.BODY: list[list[str]] = _csv['body']

    def __import_csv(self) -> CSVTable:
        """Importe les valeurs du fichier CSV spécifié dans la classe.

        Returns:
            CSVTable: Dictionaire contenant l'entête et le corps du CSV.
        """
        with open(self.PATH, 'r', encoding='utf-8', newline='') as f:
            table: list[list[str]] = list(csv.reader(f, delimiter=self.DELIMETER))
            if not table: # Fichier totalement vide
                return {'header': [], 'body': []}
            return {'header': table[0], 'body': table[1:]}
        
    def READER(self, start: int = 0, end: int = 0) -> DB_Reader:
        """Raccourci pour créer un lecteur, ex : Catalogue('x.csv').READER().NUM_SORT(1).READ()
 
        Args:
            start (int, optional): Index de la première ligne du segment. Defaults to 0.
            end (int, optional): Index de fin du segment (exclu), 0 signifie jusqu'à la fin. Defaults to 0.
 
        Returns:
            Catalogue_Reader: Lecteur sur le segment demandé.
        """
        return DB_Reader(self, start, end)

    def SAVE_FILE(self):
        """Sauvegarde les modifications apportées dans la classe dans le fichier CSV.
        """
        with open(self.PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=self.DELIMETER)
            writer.writerow(self.HEAD)
            writer.writerows(self.BODY)

    # (C)RUD
    def CREATE(self, item: list[object], index: int = -1) -> None:
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
    def UPDATE(self, item: object | list[object], coords: int | list[int] = 0) -> None:
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

    def UPDATE_HEADER(self, item: str | list[str], index: int | None = None) -> None:
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

# Fonctions internes (préfixe "__" + absentes de __all__ : invisibles avec "import *")

def _normalize(text: str) -> str:
    """Renvoie les caractères en minuscules sans accents, ex :"Guitare" -> "guitare".

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

def _to_type(item: str, rtype: type) -> object:
    """Converti une chaîne de caractères en valeur d'un autre type.
 
    Args:
        item (str): Chaine de caractères.
        rtype (type): Type de la valeur de sortie.
 
    Returns:
        object: Valeur convertie.
 
    Raises:
        ValueError: Si la conversion en float est impossible.
    """
    if rtype is str:
        return item
    if rtype is bool: # Cas particulier : bool("False") vaut True, car pour les chaines de caractères la fonction ne regarde que si la chaine est vide ou pas.
        return item.strip().lower() in ('true', '1', 'yes', 'oui', 'vrai')
    if rtype is float: # Cas particulier : Check plus souple.
        number: float | None = _to_float(item)
        if number is None:
            raise ValueError(f'Impossible de convertir {item!r} en flotant !') # !r force la chaine de caractère à afficher tout les caractères cachés également en appellant repr() au lieu de str().
        return number
    return rtype(item)

# C(R)UD
class DB_Reader:
    """Classe regroupant toutes les fonctions permettant d'afficher, de trier ou de rechercher les données d'un tableau CSV.
    """
    def __init__(self, database: Database, start: int = 0, end: int = 0) -> None:
        """Importe un morceau du fichier CSV contenu dans le Catalogue utilisé pour pouvoir y extraire des informations.

        Args:
            database (DataBase): Base de données CSV.
            start (int, optional): Index de la première ligne du segment utilisé. Defaults to 0.
            end (int, optional): Index de la dernière ligne du segment utilisé. Defaults to 0.
        """
        real_ids: range = range(*slice(start, end or None).indices(len(database.BODY))) # Les index restent ceux du Catalogue (ne repartent pas de 0)
        # Cette expression est divisée en plusieurs parties :
        # 1. "slice" découpe le morceau désiré du tableau pour renvoyer les lignes comprises entre "start" et "end" exclu.
        # 2. ".indices" renvoie la liste des indices des lignes que l'on vient d'extraire.
        # 3. Le "*" devant "slice" permet de renvoyer la liste comme si il sagissait de plusieurs arguments, ex : f(*[p1, p2, p3]) = f(p1, p2, p3)
        # 4. "range" crée une listes itérable de nombres entiers.
        self.HEAD: list[str] = database.HEAD
        self.BODY: list[IndexedRow] = [(i, database.BODY[i]) for i in real_ids]
        
    def SELECT(self, index: int) -> DB_Reader:
        """Séléctionne une seule ligne parmi le segment utilisé du fichier CSV et supprime les autres du corps du lecteur.

        Args:
            index (int): Index relatif au premier index du segment (considéré comme 0).

        Returns:
            DB_Reader: Le lecteur, pour enchaîner.
        """
        self.BODY = [self.BODY[index]]
        return self
    
    def ALPHA_SORT(self, column: int = 0, reverse: bool = False) -> DB_Reader:
        """Renvoie le segment du fichier CSV séléctionné trié dans l'ordre alphabétique par la colonne {column} et met à jour le corp du lecteur.

        Args:
            column (int, optional): Index de la colonne sur laquelle se baser. Defaults to 0.
            reverse (bool, optional): Inverse l'ordre. Defaults to False.

        Returns:
            DB_Reader: Le lecteur, pour enchaîner.
        """
        self.BODY = sorted(self.BODY, key=lambda pair: _normalize(_cell(pair[1], column)), reverse=reverse)
        # Note & Mémo :
        # Lambda est une fonction anonyme, elle ne s'appelle pas et est écrite sur une seule ligne pour symboliser une expression.
        # Dans sorted() elle sert à déterminer la manière de trier les éléments.
        return self
        
    def NUM_SORT(self, column: int = 0, reverse: bool = False) -> DB_Reader:
        """Renvoie le segment du fichier CSV séléctionné trié dans l'ordre croissant par la colonne {column} et met à jour le corp du lecteur.
    
        Args:
            column (int, optional): Index de la colonne sur laquelle se baser. Defaults to 0.
            reverse (bool, optional): Trie dans l'ordre décroissant. Defaults to False.

        Returns:
            DB_Reader: Le lecteur, pour enchaîner.
        """
        numeric: list[tuple[float, IndexedRow]] = []
        others: list[IndexedRow] = []
        for pair in self.BODY:
            value: float | None = _to_float(_cell(pair[1], column))
            if value is None:
                others.append(pair) # Ajoute les valeurs non numériques à la fin de la liste triée
            else:
                numeric.append((value, pair)) # Ajoute les valeurs détéctée comme numérique malgrès le format non conventionel à la liste
        numeric.sort(key=lambda item: item[0], reverse=reverse)
        # Note & Mémo :
        # Dans .sort() la lambda sert à trier la liste "numeric" par sa première colonne, celle qui contient la valeur numérique à utiliser.
        self.BODY = [pair for _, pair in numeric] + others # Retire la valeur numérique secondaire pour ne garder que (index réel, ligne)
        return self
        
    def SEARCH(self, query: str, columns: list[int] | None = None, exact: bool = False) -> DB_Reader:
        """Ne garde que les lignes du segment qui correspondent à la recherche (sans accents ni majuscules) sur les colonnes {columns}.
 
        Args:
            query (str): Recherche.
            columns (list[int] | None, optional): Index des colonnes sur lesquelles appliquer la recherche, None ou -1 signifie toutes les colonnes. Defaults to None.
            exact (bool, optional): Si vrai, TOUTES les cellules observées doivent contenir la recherche (sinon une seule suffit). Defaults to False.
 
        Returns:
            DB_Reader: Le lecteur, pour enchaîner.
        """
        needle: str = _normalize(query)
        wanted: list[int] = columns if columns is not None else [-1]
        all_columns: bool = -1 in wanted
 
        def matches(row: list[str]) -> bool:
            """Renvoie si la ligne correspond à la recherche.
 
            Args:
                row (list[str]): Ligne du fichier CSV.
 
            Returns:
                bool: Correspondance.
            """
            cells: list[str] = row if all_columns else [_cell(row, c) for c in wanted]
            if exact: return all(needle == _normalize(cell) for cell in cells)
            return any(needle in _normalize(cell) for cell in cells) # Renvoie vrai si n'importe quelle case observée de la ligne correspond.
 
        self.BODY = [pair for pair in self.BODY if matches(pair[1])]
        return self

    def READ(self, types: list[type] | None = None) -> list[object] | list[list[object]]:
        """Renvoie la section séléctionnée du fichier CSV avec les types par colonnes.
 
        Args:
            types (list[type] | None, optional): Types utilisés par chaque colonne, se répète en boucle. None équivaut à [str]. Defaults to None.
 
        Returns:
            list[object] | list[list[object]]:
                - Une seule ligne : [valeurs]
                - Plusieurs lignes (ou aucune) : [[valeurs], [valeurs], ...]
        """
        kinds: list[type] = types or [str]
        lines: list[list[object]] = [[_to_type(cell, kinds[i % len(kinds)]) for i, cell in enumerate(row)] for _, row in self.BODY]
        if len(lines) == 1:
            return lines[0] # Ligne simple
        return lines # Liste de lignes
    
    def READ_WITH_ID(self, types: list[type] | None = None) -> list[object] | list[list[object]]:
            """Renvoie la section séléctionnée du fichier CSV avec les types par colonnes et l'index réel de chaque ligne.
     
            Args:
                types (list[type] | None, optional): Types utilisés par chaque colonne, se répète en boucle. None équivaut à [str]. Defaults to None.
     
            Returns:
                list[object] | list[list[object]]:
                    - Une seule ligne : [index, [valeurs]]
                    - Plusieurs lignes (ou aucune) : [[index, [valeurs]], [index, [valeurs]], ...]
            """
            kinds: list[type] = types or [str]
            lines: list[list[object]] = []
            for real_id, row in self.BODY:
                items: list[object] = [_to_type(cell, kinds[i % len(kinds)]) for i, cell in enumerate(row)]
                lines.append([real_id, items])
            if len(lines) == 1:
                return lines[0] # Ligne simple
            return lines # Liste de lignes
    
    def PRINT_TABLE(self, pretty: bool = True) -> None:
        """Affiche une entête et un corps dans le terminal comme un tableau CSV, avec l'index réel de chaque ligne en première colonne.
 
        Args:
            pretty (bool, optional): Améliore l'affichage avec du padding. Defaults to True.
        """
        header: list[str] = ['id'] + [str(h) for h in self.HEAD]
 
        # Transforme toutes les valeurs en texte
        rows: list[list[str]] = [[str(real_id)] + [str(c) for c in row] for real_id, row in self.BODY]
 
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
            
# --------------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------------

def TESTING() -> None:
    """Teste la librairie sur un fichier CSV temporaire. Lève une AssertionError au premier test qui échoue.
    """
    header: list[str] = ['nom', 'prix', 'qte', 'actif']
    rows: list[list[object]] = [
        ['Guitare',             '2.50', 10, True],   # index réel 0
        ['Basse',               '1,20', 5,  False],  # index réel 1 (virgule décimale)
        ['Flûte à bec',         5,      0,  'oui'],  # index réel 2
        ['Platine',             'abc',  7,  True],   # index réel 3 (prix non numérique)
        ['Guitare éléctrique', '3.10', 4,  True],   # index réel 4
    ]
    types: list[type] = [str, float, int, bool]
    passed: int = 0
 
    def check(name: str, got: object, expected: object) -> None:
        nonlocal passed
        assert got == expected, f'[FAIL] {name}\n  obtenu  : {got!r}\n  attendu : {expected!r}'
        passed += 1
        print(f'[ OK ] {name}')
 
    def ids(reader: DB_Reader) -> list[int]:
        return [real_id for real_id, _ in reader.BODY]
 
    with TEMP_DB(header, rows) as db:
        path: Path = db.PATH
        check('le fichier temporaire existe', path.exists(), True)
 
        # 1. Les chaînes : tri -> recherche -> sélection -> lecture
        check('chaîne complète ALPHA_SORT().SEARCH().SELECT().READ_WITH_ID()',
              DB_Reader(db).ALPHA_SORT().SEARCH('guitare').SELECT(0).READ_WITH_ID(types),
              [0, ['Guitare', 2.5, 10, True]])
        check('chaîne via Database.READER() + NUM_SORT',
              db.READER().NUM_SORT(1).SEARCH('guitare').SELECT(-1).READ_WITH_ID(types),
              [4, ['Guitare éléctrique', 3.1, 4, True]])
        check('chaîne complète sans ID via READ()',
            DB_Reader(db).ALPHA_SORT().SEARCH('guitare').SELECT(0).READ(types),
            ['Guitare', 2.5, 10, True])
 
        # 2. Format de sortie : une ligne vs plusieurs lignes
        check('plusieurs lignes -> [[id, [..]], ...]',
              db.READER().SEARCH('guitare').READ_WITH_ID(),
              [[0, ['Guitare', '2.50', '10', 'True']], [4, ['Guitare éléctrique', '3.10', '4', 'True']]])
        check('aucun résultat -> []', db.READER().SEARCH('zzz').READ_WITH_ID(), [])
 
        # 3. Index réels conservés
        check('segment [2:5] garde les index réels', ids(DB_Reader(db, 2, 5)), [2, 3, 4])
        check('segment + recherche -> id réel 4',
              DB_Reader(db, 1).SEARCH('guitare').READ_WITH_ID(types),
              [4, ['Guitare éléctrique', 3.1, 4, True]])
        check('ALPHA_SORT garde les index réels', ids(db.READER().ALPHA_SORT()), [1, 2, 0, 4, 3])
        check('ALPHA_SORT inversé', ids(db.READER().ALPHA_SORT(reverse=True)), [3, 4, 0, 2, 1])
        check('NUM_SORT (non numériques à la fin)', ids(db.READER().NUM_SORT(1)), [1, 0, 4, 2, 3])
        check('NUM_SORT décroissant', ids(db.READER().NUM_SORT(1, reverse=True)), [2, 4, 0, 1, 3])
 
        # 4. Recherche
        check('SEARCH sur une colonne précise', ids(db.READER().SEARCH('Flûte à bec', [0])), [2])
        check('SEARCH ignore accents et majuscules', ids(db.READER().SEARCH('Guitare', [0])), [0, 4])
 
        # 5. Conversion de types
        check('virgule décimale convertie en float', db.READER().SELECT(1).READ_WITH_ID(types), [1, ['Basse', 1.2, 5, False]])
 
        # 6. Écriture puis relecture du fichier
        db.CREATE(['Rat', 3, 1, 'non'])
        db.SAVE_FILE()
        reloaded: Database = Database(path)
        check('CREATE + SAVE_FILE + rechargement', reloaded.BODY[-1], ['Rat', '3', '1', 'non'])
        check('le rechargement garde 6 lignes', len(reloaded.BODY), 6)
 
    check('le fichier temporaire est supprimé', path.exists(), False)
 
    # 7. Autre délimiteur
    with TEMP_DB(header, rows[:1], ';') as semi:
        check('délimiteur ";" dans le fichier', semi.PATH.read_text(encoding='utf-8').splitlines()[0], 'nom;prix;qte;actif')
        check('délimiteur ";" relu correctement', semi.READER().READ_WITH_ID(), [0, ['Guitare', '2.50', '10', 'True']])
 
    print(f'\n{passed} tests réussis.')
    with TEMP_DB(header, rows) as demo:
        demo.READER().NUM_SORT(1).PRINT_TABLE()

if __name__ == '__main__':
    TESTING()