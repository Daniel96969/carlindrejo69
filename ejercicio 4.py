"""
libreria_ortografia.py
Módulo simple de "corrector" que detecta palabras no reconocidas
y sugiere coincidencias cercanas usando difflib.
No es un corrector profesional: usa un diccionario pequeño interno.
"""
import re
import difflib
from typing import List, Tuple

# Diccionario pequeño de ejemplo (palabras en español comunes)
# Puedes ampliar esta lista o cargar desde un archivo externo.
DICT = {
    "hola", "mundo", "python", "programa", "ejemplo", "usuario", "archivo",
    "salir", "menu", "bienvenido", "guerrero", "mago", "explorador",
    "pocion", "antorcha", "goblin", "batalla", "ayuda", "nota", "estudiante",
    "edad", "calificacion", "calificaciones", "promedio", "lista"
}

_word_re = re.compile(r"[a-záéíóúüñ]+", re.IGNORECASE)

def tokenize(text: str) -> List[str]:
    """Devuelve lista de palabras (minúsculas) encontradas en el texto."""
    return [w.lower() for w in _word_re.findall(text)]

def check_text(text: str, max_suggestions: int = 3) -> List[Tuple[str, List[str]]]:
    """
    Revisa el texto y devuelve una lista de tuplas (palabra_no_reconocida, sugerencias).
    """
    tokens = tokenize(text)
    unknowns = []
    for w in tokens:
        if w not in DICT:
            # sugerencias usando difflib
            suggestions = difflib.get_close_matches(w, DICT, n=max_suggestions, cutoff=0.6)
            unknowns.append((w, suggestions))
    return unknowns

def add_word_to_dict(word: str):
    """Añade una palabra al diccionario (persistencia manual si se desea)."""
    DICT.add(word.lower())

if __name__ == "__main__":
    # prueba rápida si se ejecuta como script
    sample = "Hola mundoo. Este es un progrma de pytthon con pcoion."
    print("Texto:", sample)
    print("Resultados:", check_text(sample))
