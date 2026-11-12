from __future__ import annotations

import math
import sqlite3
import tempfile
import unicodedata
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import TypeAlias

__all__ = [
    'IndexedRow',
    'CREATE_FILE', 'TEMP_DB',
    'Database', 'DB_Reader',
]

IndexedRow: TypeAlias = tuple[int, list[str]]
DATA_DIR = Path('assets/data')
DEFAULT_HEADERS = {
    'catalogue': ['product', 'price', 'description', 'stock', 'quality'],
    'utilisateurs': ['username', 'password', 'role', 'permissions'],
}

def _quote_identifier(identifier: str) -> str:
    if not identifier or '\x00' in identifier:
        raise ValueError(f'Identifiant SQLite invalide : {identifier!r}')
    return '"' + identifier.replace('"', '""') + '"'

def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize('NFD', text)
    return ''.join(
        character
        for character in decomposed
        if unicodedata.category(character) != 'Mn'
    ).casefold()

def _cell(row: list[str], column: int) -> str:
    return row[column] if -len(row) <= column < len(row) else ''

def _to_float(text: str) -> float | None:
    try:
        value = float(text.strip().replace(' ', '').replace(',', '.'))
    except ValueError:
        return None
    return None if math.isnan(value) else value

def _to_type(item: str, rtype: type) -> object:
    if rtype is str:
        return item
    if rtype is bool:
        return item.strip().casefold() in ('true', '1', 'yes', 'oui', 'vrai')
    if rtype is float:
        number = _to_float(item)
        if number is None:
            raise ValueError(f'Impossible de convertir {item!r} en float')
        return number
    return rtype(item)

def _database_path(path: str | Path | None) -> tuple[Path, str]:
    requested = Path('catalogue.db') if path is None else Path(path)
    if not requested.is_absolute():
        requested = DATA_DIR / requested

    database_path = requested.with_suffix('.db')
    return database_path, requested.stem

@contextmanager
def TEMP_DB(header: list[str], rows: list[list[object]]) -> Generator[Database]:
    """Crée une base SQLite temporaire et la supprime à la sortie du bloc."""
    with tempfile.TemporaryDirectory() as temporary_directory:
        database = Database(
            Path(temporary_directory) / 'test.db',
            table='data',
            header=header,
        )
        for row in rows:
            database.CREATE(row)
        yield database

def CREATE_FILE(
    path: str | Path = 'catalogue.db',
    header: list[str] | None = None,
    overwrite: bool = False,
) -> Path:
    """Crée une base SQLite avec une table vide.
    """
    database_path, table = _database_path(path)
    if database_path.exists():
        if not overwrite:
            return database_path
        database_path.unlink()
    Database(database_path, table=table, header=header)
    return database_path

class Database:
    """Accède à une table SQLite avec une API CRUD simple.
    """
    
    def __init__(
        self,
        path: str | Path | None = None,
        table: str | None = None,
        header: list[str] | None = None,
    ) -> None:
        self.PATH, inferred_table = _database_path(path)
        self.TABLE_NAME = table or inferred_table
        self.TABLE = _quote_identifier(self.TABLE_NAME)
        self.PATH.parent.mkdir(parents=True, exist_ok=True)
        self._initialize(header)

    @contextmanager
    def _connection(self) -> Generator[sqlite3.Connection]:
        connection = sqlite3.connect(self.PATH)
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize(self, header: list[str] | None) -> None:
        with self._connection() as connection:
            exists = connection.execute(
                'SELECT 1 FROM sqlite_master WHERE type = ? AND name = ?',
                ('table', self.TABLE_NAME),
            ).fetchone()
        if exists:
            return

        columns = header if header is not None else DEFAULT_HEADERS.get(self.TABLE_NAME, [])
        with self._connection() as connection:
            column_sql = ', '.join(
                f'{_quote_identifier(name)} TEXT' for name in columns
            )
            separator = ', ' if column_sql else ''
            connection.execute(
                f'CREATE TABLE {self.TABLE} ('
                f'"__position" INTEGER PRIMARY KEY{separator}{column_sql})'
            )

    @property
    def HEAD(self) -> list[str]:
        with self._connection() as connection:
            information = connection.execute(
                f'PRAGMA table_info({self.TABLE})'
            ).fetchall()
        return [
            row[1] for row in information
            if row[1] != '__position'
        ]

    @property
    def BODY(self) -> list[list[str]]:
        return [row for _, row in self._rows()]

    def _rows(self) -> list[IndexedRow]:
        columns = ', '.join(_quote_identifier(column) for column in self.HEAD)
        selected_columns = f', {columns}' if columns else ''
        with self._connection() as connection:
            rows = connection.execute(
                f'SELECT "__position"{selected_columns} FROM {self.TABLE} '
                'ORDER BY "__position"'
            ).fetchall()
        return [
            (
                int(row[0]),
                [str(value) if value is not None else '' for value in row[1:]],
            )
            for row in rows
        ]

    def READER(self, start: int = 0, end: int = 0) -> DB_Reader:
        return DB_Reader(self, start, end)

    def CREATE(self, item: list[object], index: int = -1) -> None:
        columns = self.HEAD
        if len(item) != len(columns):
            raise ValueError(f'{len(columns)} valeurs attendues, {len(item)} reçues')

        with self._connection() as connection:
            positions = [
                row[0]
                for row in connection.execute(
                    f'SELECT "__position" FROM {self.TABLE} ORDER BY "__position"'
                )
            ]
            insert_at = len(positions) if index < 0 else min(index, len(positions))
            for position in reversed(positions[insert_at:]):
                connection.execute(
                    f'UPDATE {self.TABLE} SET "__position" = ? '
                    'WHERE "__position" = ?',
                    (position + 1, position),
                )

            quoted_columns = ', '.join(
                _quote_identifier(column) for column in columns
            )
            named_columns = f', {quoted_columns}' if quoted_columns else ''
            placeholders = ', '.join('?' for _ in columns)
            value_placeholders = f', {placeholders}' if placeholders else ''
            connection.execute(
                f'INSERT INTO {self.TABLE} ("__position"{named_columns}) '
                f'VALUES (?{value_placeholders})',
                (insert_at, *(str(value) for value in item)),
            )

    def UPDATE(self, item: object | list[object], coords: int | list[int] = 0) -> None:
        row_index, column_index = (coords, None) if isinstance(coords, int) else coords
        rows = self._rows()
        try:
            position, row = rows[row_index]
        except IndexError:
            raise IndexError('Index de ligne inexistant') from None

        if column_index is None:
            if not isinstance(item, list) or len(item) != len(self.HEAD):
                raise ValueError(f'La ligne doit contenir {len(self.HEAD)} valeurs')
            values = [str(value) for value in item]
        else:
            if isinstance(item, list):
                raise ValueError('Une valeur unique est attendue pour une cellule')
            if not -len(row) <= column_index < len(row):
                raise IndexError('Index de colonne inexistant')
            row[column_index] = str(item)
            values = row

        assignments = ', '.join(
            f'{_quote_identifier(column)} = ?' for column in self.HEAD
        )
        if assignments:
            with self._connection() as connection:
                connection.execute(
                    f'UPDATE {self.TABLE} SET {assignments} WHERE "__position" = ?',
                    (*values, position),
                )

    def UPDATE_HEADER(self, item: str | list[str], index: int | None = None) -> None:
        headers = self.HEAD
        if isinstance(item, list) and index is None:
            if len(item) != len(headers):
                raise ValueError('Le nombre de colonnes ne peut pas changer')
            new_headers = item
            renames = [
                (old, new)
                for old, new in zip(headers, new_headers)
                if old != new
            ]
            with self._connection() as connection:
                temporary_names = [
                    f'__rename_{number}' for number in range(len(renames))
                ]
                for (old, _), temporary in zip(renames, temporary_names):
                    connection.execute(
                        f'ALTER TABLE {self.TABLE} RENAME COLUMN '
                        f'{_quote_identifier(old)} TO {_quote_identifier(temporary)}'
                    )
                for (_, new), temporary in zip(renames, temporary_names):
                    connection.execute(
                        f'ALTER TABLE {self.TABLE} RENAME COLUMN '
                        f'{_quote_identifier(temporary)} TO {_quote_identifier(new)}'
                    )
            return

        if isinstance(item, str) and index is not None:
            new_name = [item][0]
            old_name = headers[index]
            with self._connection() as connection:
                connection.execute(
                    f'ALTER TABLE {self.TABLE} RENAME COLUMN '
                    f'{_quote_identifier(old_name)} TO {_quote_identifier(new_name)}'
                )
            return

        raise ValueError('Fournis une liste de colonnes ou un nom et son index')

    def DELETE(self, index: int = -1) -> list[str]:
        rows = self._rows()
        try:
            position, values = rows[index]
        except IndexError:
            raise IndexError('Index de ligne inexistant') from None

        with self._connection() as connection:
            connection.execute(
                f'DELETE FROM {self.TABLE} WHERE "__position" = ?', (position,)
            )
            later_positions = connection.execute(
                f'SELECT "__position" FROM {self.TABLE} '
                'WHERE "__position" > ? ORDER BY "__position"',
                (position,),
            ).fetchall()
            for (later_position,) in later_positions:
                connection.execute(
                    f'UPDATE {self.TABLE} SET "__position" = ? '
                    'WHERE "__position" = ?',
                    (later_position - 1, later_position),
                )
        return values


class DB_Reader:
    """Trie, filtre et lit un segment d'une table SQLite."""

    def __init__(self, database: Database, start: int = 0, end: int = 0) -> None:
        rows = database._rows()
        self.HEAD = database.HEAD
        self.BODY: list[IndexedRow] = rows[slice(start, end or None)]

    def SELECT(self, index: int) -> DB_Reader:
        self.BODY = [self.BODY[index]]
        return self

    def ALPHA_SORT(self, column: int = 0, reverse: bool = False) -> DB_Reader:
        self.BODY.sort(
            key=lambda pair: _normalize(_cell(pair[1], column)),
            reverse=reverse,
        )
        return self

    def NUM_SORT(self, column: int = 0, reverse: bool = False) -> DB_Reader:
        numeric: list[tuple[float, IndexedRow]] = []
        others: list[IndexedRow] = []
        for pair in self.BODY:
            value = _to_float(_cell(pair[1], column))
            if value is None:
                others.append(pair)
            else:
                numeric.append((value, pair))
        numeric.sort(key=lambda item: item[0], reverse=reverse)
        self.BODY = [pair for _, pair in numeric] + others
        return self

    def SEARCH(self, query: str | list[str], columns: list[int] | None = None, exact: bool = False) -> DB_Reader:
            """Ne garde que les lignes du segment qui correspondent à la recherche (sans accents ni majuscules) sur les colonnes {columns}.
     
            Args:
                query (str | list[str]): Recherche. Accepte une liste notamment pour les recherches par catégories ou tags.
                columns (list[int] | None, optional): Index des colonnes sur lesquelles appliquer la recherche, None ou -1 signifie toutes les colonnes. Defaults to None.
                exact (bool, optional): Si vrai, TOUTES les cellules observées doivent contenir la recherche (sinon une seule suffit). Defaults to False.
     
            Returns:
                DB_Reader: Le lecteur, pour enchaîner.
            """
            if isinstance(query, str): query = [query]
            needles: list[str] = [_normalize(q) for q in query]
            wanted: list[int] = columns if columns is not None else [-1]
            all_columns: bool = -1 in wanted
     
            def matches(row: list[str]) -> bool:
                """Renvoie si la ligne correspond à la recherche.
     
                Args:
                    row (list[str]): Ligne du fichier SQLite.
     
                Returns:
                    bool: Correspondance.
                """
                cells: list[str] = row if all_columns else [_cell(row, c) for c in wanted]
                for needle in needles:
                    if exact: return all(needle == _normalize(cell) for cell in cells)
                    else: return any(needle in _normalize(cell) for cell in cells) # Renvoie vrai si n'importe quelle case observée de la ligne correspond.
                return False
     
            self.BODY = [pair for pair in self.BODY if matches(pair[1])]
            return self

    def READ(self, types: list[type] | None = None) -> list[object] | list[list[object]]:
        kinds = types or [str]
        lines = [
            [
                _to_type(cell, kinds[index % len(kinds)])
                for index, cell in enumerate(row)
            ]
            for _, row in self.BODY
        ]
        return lines[0] if len(lines) == 1 else lines

    def READ_WITH_ID(
        self,
        types: list[type] | None = None,
    ) -> list[object] | list[list[object]]:
        kinds = types or [str]
        lines = [
            [
                row_id,
                [
                    _to_type(cell, kinds[index % len(kinds)])
                    for index, cell in enumerate(row)
                ],
            ]
            for row_id, row in self.BODY
        ]
        return lines[0] if len(lines) == 1 else lines

    def PRINT_TABLE(self, pretty: bool = True) -> None:
        header = ['id'] + [str(value) for value in self.HEAD]
        rows = [[str(row_id)] + row for row_id, row in self.BODY]
        widths = [0] * max([len(header)] + [len(row) for row in rows])
        if pretty:
            for row in [header, *rows]:
                for index, value in enumerate(row):
                    widths[index] = max(widths[index], len(value))

        def format_row(row: list[str]) -> str:
            return ' | '.join(
                value.ljust(widths[index]) for index, value in enumerate(row)
            ).rstrip()

        print(format_row(header))
        if pretty:
            print('-+-'.join('-' * width for width in widths))
        for row in rows:
            print(format_row(row))

def TESTING() -> None:
    """Teste les opérations principales sur une base SQLite temporaire."""
    header = ['nom', 'prix', 'qte', 'actif']
    rows: list[list[object]] = [
        ['Guitare', '2.50', 10, True],
        ['Basse', '1,20', 5, False],
        ['Flûte à bec', 5, 0, 'oui'],
        ['Platine', 'abc', 7, True],
        ['Guitare électrique', '3.10', 4, True],
    ]
    types = [str, float, int, bool]

    with TEMP_DB(header, rows) as database:
        assert database.READER().ALPHA_SORT().SEARCH('guitare').SELECT(0).READ_WITH_ID(
            types
        ) == [0, ['Guitare', 2.5, 10, True]]
        assert database.READER().NUM_SORT(1).SEARCH('guitare').SELECT(-1).READ_WITH_ID(
            types
        ) == [4, ['Guitare électrique', 3.1, 4, True]]
        assert database.READER().SEARCH('zzz').READ_WITH_ID() == []
        assert database.READER().NUM_SORT(1).BODY[-1][1][0] == 'Platine'
        assert database.READER().SEARCH(
            'Flûte à bec', [0], exact=True
        ).READ_WITH_ID() == [2, ['Flûte à bec', '5', '0', 'oui']]
        assert [
            row_id for row_id, _ in database.READER(2, 5).BODY
        ] == [2, 3, 4]

        database.CREATE(['Rat', 3, 1, 'non'], index=2)
        assert database.BODY[2] == ['Rat', '3', '1', 'non']
        database.UPDATE(['Rat', 4, 2, 'oui'], 2)
        assert database.BODY[2][1] == '4'
        database.UPDATE('Raton', [2, 0])
        assert database.BODY[2][0] == 'Raton'
        assert database.DELETE(2) == ['Raton', '4', '2', 'oui']
        assert len(database.BODY) == 5

        database.UPDATE_HEADER('nom_produit', 0)
        assert database.HEAD[0] == 'nom_produit'
        database.UPDATE_HEADER(['produit', 'prix', 'quantite', 'actif'])
        assert database.HEAD == ['produit', 'prix', 'quantite', 'actif']

        database.CREATE(['Rat', 3, 1, 'non'])
        reloaded = Database(database.PATH, table='data')
        assert reloaded.BODY[-1] == ['Rat', '3', '1', 'non']

    print('Tests SQLite réussis.')

if __name__ == '__main__':
    TESTING()
