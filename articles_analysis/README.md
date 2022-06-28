# ANÀLISIS D'ARTICLES
Aquest directori conté el codi i els recursos per realitzat l'anàlisis dels articles descarregats anteriorment.

Aquest anàlisis es divideix en dos tipus:
- Anàlisis de casos
- Anàlisis de continguts

Els dos anàlisis es basen en la presencia (i no presència) de termes i expressions regulars.

## articles_analysisi.ipynb
- **Variables globals:**
    - NEWS_PATH: Directori arrel on es troben els articles descarregats.
    - INFO_FILE_PATH: Directori del fitxer on es troben els identificadors de cada article amb un identificador de cas
    
- **Requeriments:**
    - Fitxer Python amb un diccionari amb les expressions regulars guardades per categories. Aquest fitxer es pot trobar [aquí](https://github.com/BegonaLopez0/Dos-anys-de-not-cies-de-viol-ncia-sexual/blob/main/articles_analysis/utilities/regex_categories.py).
    - Fitxer txt que conté una llista de nacionalitats en espanyol. Es pot trobar [aquí](https://github.com/BegonaLopez0/Dos-anys-de-not-cies-de-viol-ncia-sexual/blob/main/articles_analysis/utilities/nacionalidades.txt).
