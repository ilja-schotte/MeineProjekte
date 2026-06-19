
from typing import List, Optional 
import sys



def MusterFunktion(
        user_id: int, 
        user_name: str,
        items: list[str],
        coordinates: tuple[float, float] | None = None,
        metadata: dict[str, float | int] | None = None,
        threshold: float | None = None
    ) -> dict[str, int]:

    """
    DESCRIPTION:
      Hier wird beschrieben was die Funktion macht.

    ARGS:
      user_id:      int                     Benutzer-ID. (required)
      user_name:    str                     Benutzername. (required)
      items:        list[str]               Itemliste. (required)
      
      coordinates:  tuple[float, float]     Ein Tupel bestehend aus (x, y) Koordinaten.
                                            (optional, default: None)

      metadata:     dict[str, float | int]  Dictionary mit Messwerten 
                                            (Schlüssel: Name, Wert: Zahl). 
                                            (optional, default: None)

      threshold:    float | None = None     Optionaler Schwellenwert für die Filterung. 
                                            (optional, default: None)
    RETURN:
      result:       dict[str, int]          Dictionary mit der Anzahl der verarbeiteten
                                            Elemente.
    """

    result = {}

    return result

result = MusterFunktion( 
    user_id = 3,
    user_name = 'name',
    items = ['A','B','C']
)

print(result)
print(sys.executable)