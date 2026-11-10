from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctions

import requests # Gère les requêtes d'API
import hashlib # Gère le hashing

# Seuls ces classes sont exportés avec "from api_utils import *", tout le reste est interne au script.
__all__ = [
    'PWNED_COUNT',
]

def PWNED_COUNT(password: str) -> int:
    """Récupère le nombre de fois qu'un mot de passe à été leaké en utilisant l'API Have I Been Pwned sans que le mdp ne quitte la machine.

    Args:
        password (str): Mot de passe.

    Returns:
        int: Nombre de leaks
    """
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    resp = requests.get(
        f"https://api.pwnedpasswords.com/range/{prefix}",
        headers={"Add-Padding": "true"},
        timeout=10,
    )
    resp.raise_for_status()

    for line in resp.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)
    return 0

# --------------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------------

def TESTING() -> None:
    """Teste le module d'API.
    """
    
    # 1. Have I Been Pwned
    n = PWNED_COUNT("password123")
    print(f"Found {n} times in breaches" if n else "Not found in known breaches")
    n = PWNED_COUNT("uildgbvylordywbvlwbyufvrydwrvgfuwdry")
    print(f"Found {n} times in breaches" if n else "Not found in known breaches")

if __name__ == "__main__":
    TESTING()