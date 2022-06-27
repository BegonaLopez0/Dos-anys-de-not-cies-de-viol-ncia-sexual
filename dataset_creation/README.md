# Col·lecció de dades
En aquest repositori trobem el codi i els recursos utilitzats per crear el conjunt d'articles dels mitjans de comunicació més importants a Espanya.

Consisteix en tres fases:
1. Obtenció dels tuits.
2. Classificació segons si són de violència sexual o no.
3. Obtenció dels articles de les notícies que tracten de violència sexual.

## Descripció del codi
### 1. tweets_download.py
Obtenció dels tweets dels medis seleccionats per un periode determinat.

- **Variables globals:**
  - ACCOUNTS: Llistat de comptes.
  - DATA_PATH: Directori arrel on s'emmagatzemen les dades.
  - FREQ: Freqüència de fitxers.
  - MAX_TWEETS: Número màxim de tweets en un fitxer. Cal tenir en compte les limitacions de la API.
  - START_DAY: Dia inicial.
  - FINAL_DAY: Dia final.
  - MONTH: Mes del periode seleccionat, on es guardaran els tuits.
  - YEAR: Any del peropde seleccionat, on es guardaran els tuits.
  
- **Entrada:** Cap.

- **Sortida:** Un fitxer per cada compte i periode segons la freqüència seleccionada des del dia inicial fins el final en format csv i jsonl.
