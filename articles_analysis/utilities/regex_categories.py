categories = {}
categories['AGE'] = [r'\b[1-9]?[0-9]\b[ años]{0,}', 'mayor[es]{0,}[ de edad]{0,}', 'menor[es]{0,}[ de edad]{0,}' ,'genario', 'adolescente', 'niñ[o,a]', 'joven', 'ancian[o,a]']

categories['SEXUAL_ASSAULT'] = ['agre[s|d]', 'viola[r|cion|dor]', 'penetra[r|cion|dor]', r'acostar[\w]+\scon', r'obligar[\w]+\srelaciones sexuales', 'prostitu']
categories['SEXUAL_HARASSMENT'] = ['acos', 'tocamientos', 'desnud', 'manosea', 'intimid', 'miradas (?:lujuriosas|lascivas|insistentes)', 'extorsion', 'ciberacoso', 'chantaj']
categories['SEXUAL_ABUSE'] = ['pederast', 'pedofil', 'abus', 'relaciones con una menor', 'viola[\w\s]+menor', '(?:explotacion|abuso) sexual infantil', 'drogad', 'incapaci', 'discapaci']

categories['BOND_RELATIONSHIP'] = ['matrimonio', 'espos[o,a]', 'pareja', 'novi[o,a]', 'amante', 'querid[o,a]','marido','su mujer','conyuge', 'exnovi[o,a]']
categories['BOND_RELATIVE'] = ['hij[o,a]', '\bti[o,a]\b', 'abuel[o,a]', 'sobrin[o,a]', 'ahijad[o,a]', 'niet[o,a]','[m,p]adre', 'prim[o,a]', 'descendiente', 'herman[o,a]']
categories['BOND_KNOWN'] = ['compañer[o,a]', 'amig[o,a]', 'profesor[a|es]{0,}', 'alumn[o,a]', 'jef[e,a]', 'emplead[o,a]', 'becari[o,a]', 'vecin[o,a]', 'maestr[o,a]', 'director', 'conocid[o,a]', 'entrenador', 'instructor', 'sacerdote']

categories['PLACE_PUBLIC'] = ['avenida', 'parque', 'calle', 'parada', 'bosque', 'plaza', 'carretera', 'puerto', 'estacion', 'jardin', 'fuente', 'montaña', 'espacio publico', 'mirador', 'metro', 'bus', 'tren', 'transporte publico', 'playa']
categories['PLACE_WORKPLACE'] = ['oficina', 'trabajo', 'almacen', 'tienda', 'despacho', 'taller', 'coworking', 'gabinete']
categories['PLACE_HOUSE'] = ['domicilio', 'casa', 'piso', 'morada', 'hogar', 'vivienda', 'habitacion', 'residencia', 'cocina', 'comedor', 'baño', 'balcon']
categories['PLACE_EDUCATIONAL'] = ['universidad', 'escuela', 'biblioteca', 'colegio', 'centro de (?:educacion|enseñanza)', 'instituto', 'liceo', 'academia', 'conservatorio', 'guarderia', 'facultad', 'recreo', 'estadio', 'pabellon', 'piscina', 'centro deportivo', 'vestuario']
categories['PLACE_LEISURE'] = ['teatro', 'cafeteria', 'discoteca', 'pub', 'bar', 'restaurante', 'centro comercial', 'cine', 'bolera', '[h|m]otel', 'sauna', 'spa', 'piscina', 'gimnasio', 'monumento', 'parque', 'acuario', 'acuarium', 'zoo']

categories['TIME'] = ['(?:la|esta|misma) mañana', '(?:este|al) mediodia', '(?:la|esta|misma) tarde', 'atardecer', 'medianoche', 'noche', 'madrugada']

categories['STIGMA_INTOXICATED'] = ['alcohol', 'embriagado', 'droga', 'borracho', 'ebrio', 'bebido', 'alcoholizado', 'fumado', 'estupefacientes', 'intoxicado', 'positivo [por|en]{0,}', 'cocaina', 'consumo de', 'metanfetamina', 'extasis', 'mdma', 'burundanga', 'marihuana', 'porro[s]{0,}', 'cannabis', 'hachis', 'sedante', 'speed', 'popper', 'lsd']
categories['STIGMA_CLOTHING'] = ['falda', 'vestido', 'camiseta', 'camisa', 'top','tacones', 'leggings', 'pantalones', r'\bropa\b', 'vestid[a,o,as,os] (?:de|con)', 'faldilla', 'destapada', 'ceñid', 'escote']
categories['STIGMA_ORIGIN'] = ['de origen|original de', 'su pais (?:natal|de origen|de procedencia)', 'del estado de', '(?:norte|sud|[a,e]l este|oeste|nordeste|sudeste|sureste|sudoeste|suroeste|noroeste)', 'orient(?:e|al)', 'occident(?:e|al)', r'\blatino\b', 'hispano',  r'\barabe\b', 'mahgrebi', 'caucasico', 'musulman', 'indi[a,o]', 'american[o,a]', 'europe[o,a]', 'asiatic', 'indigena']
categories['STIGMA_AGGRESSOR'] = ['depredador', 'pervertido', 'pervers', 'narcisita', 'solitario', 'enfermo[ sexual]{0,}', 'degenerad', 'depravad']
categories['STIGMA_VULNERABILITY'] = ['menor[es]{0,}[ de edad]{0,}', 'joven', 'indefens', 'fiest', 'desamparad', 'vulnerable', 'abandonad', 'mayor', 'solter', 'promiscu', 'virgen']

categories['EXPRESSION_EUPHEMISM'] = ['no consentido', 'inapropiad', 'indesead', 'acariciar', 'arrimarse', 'piropear', 'insistir', 'no deseado', 'bajo los efectos de', 'rob[a|e|o|u][\w\s]+inocencia', 'priv[\w\s]+libertad', 'satisfacer[\w\s]+deseos sexuales', 'acceso carnal', 'forz[\w\s]+sex']
categories['EXPRESSION_DOUBT'] = ['supuest\w+\s(?:caso|delito|viola|abus|acos|agre|victima|responsable|autor|testigo)', 'supuestamente', 'presunt[o,a]', 'acusad[o,a] de', 'presuncion de inocencia',  'acusaciones[\w\s]+falsas']
