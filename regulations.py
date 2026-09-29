"""Kuratierte Liste der 19 ESG-/CSR-Regulierungen mit Anwendbarkeitskriterien.

Die `criteria`-Felder sind bewusst in natürlicher Sprache gehalten, damit
Claude sie gemeinsam mit dem Unternehmensprofil auswerten kann.

`relevant_fields` nennt je Regulierung die Profilfelder, die deren Bewertung
tatsächlich tragen — Herleitung ist immer der `criteria`-Text daneben (bei den
gekoppelten Regulierungen zusätzlich die Statusfunktion, die den Fall bestimmt).
Nur diese Felder gehen in den Begründungs-Cache ein: ändert der Nutzer ein Feld,
das für eine Regulierung ohne Bedeutung ist (z. B. den Firmennamen), bleibt deren
Begründung wortgleich bestehen. `name` gehört deshalb nie dazu; `language` kommt
über `relevant_fields_for()` automatisch hinzu, weil die Begründung in der
UI-Sprache formuliert wird.
"""

REGULATIONS = [
    {
        "nr": 1,
        "key": "CSDDD",
        "relevant_fields": ["employees", "revenue_eur", "revenue_eu_eur", "group_role",
                            "legal_form", "sites"],
        "name": "CSDDD – EU-Lieferkettenrichtlinie",
        "full_name": "Richtlinie (EU) 2024/1760 - Sorgfaltspflichten von Unternehmen im Hinblick auf Nachhaltigkeit",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024L1760&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024L1760",
        "scope": "EU",
        # Stand: konsolidierte Fassung 02024L1760 vom 18.03.2026, Art. 2 und
        # Art. 37, geaendert durch Richtlinie (EU) 2026/470 (ABl. L, 2026/470,
        # 26.02.2026). Die frueheren Werte (>1000 MA / >450 Mio. EUR mit
        # dreistufigem Phase-in) sind damit ueberholt.
        "criteria": (
            "Gilt für Unternehmen, die nach dem Recht eines Mitgliedstaats gegründet wurden und im "
            "Durchschnitt mehr als 5.000 Beschäftigte hatten UND einen weltweiten Nettoumsatz von "
            "mehr als 1.500 Mio EUR erzielten (beide Merkmale kumulativ) — oder die oberste "
            "Muttergesellschaft einer Gruppe sind, die diese Schwellen konsolidiert erreicht. "
            "Für Unternehmen aus Drittländern: Nettoumsatz >1.500 Mio EUR in der Union. "
            "Zusätzlich erfasst: Franchise-/Lizenzmodelle mit Lizenzgebühren >75 Mio EUR und "
            "weltweitem Nettoumsatz >275 Mio EUR. "
            "Die Schwellen müssen in ZWEI AUFEINANDERFOLGENDEN Geschäftsjahren überschritten sein "
            "(Art. 2 Abs. 5); umgekehrt endet die Pflicht erst, wenn sie in beiden letzten "
            "Geschäftsjahren nicht mehr erfüllt waren. Teilzeitkräfte zählen in Vollzeitäquivalenten, "
            "Leiharbeitnehmer werden mitgezählt (Art. 2 Abs. 4). "
            "Kein größenabhängiger Phase-in mehr: die nationalen Vorschriften gelten einheitlich "
            "ab 26.07.2029, die Berichtspflicht nach Art. 16 für Geschäftsjahre ab 01.01.2030. "
            "Branche: alle."
        ),
        "key_article": "Art. 2 (Anwendungsbereich)",
    },
    {
        "nr": 2,
        "key": "LkSG",
        "relevant_fields": ["employees_de", "sites", "group_role"],
        "name": "LkSG – deutsches Lieferkettengesetz",
        "full_name": "Lieferkettensorgfaltspflichtengesetz",
        # Bis 09/2026 zeigten beide URLs auf die BAFA-Uebersichtsseite — ein
        # Pressetext ohne § 1. Jetzt der amtliche Volltext.
        "url": "https://www.gesetze-im-internet.de/lksg/BJNR295910021.html",
        "text_url": "https://www.gesetze-im-internet.de/lksg/BJNR295910021.html",
        "scope": "DE",
        "criteria": (
            "Gilt für Unternehmen mit Hauptverwaltung, Hauptniederlassung, Verwaltungssitz, satzungsmäßigem "
            "Sitz oder Zweigniederlassung in Deutschland ab 1000 Arbeitnehmern im Inland "
            "(inkl. entsandte Arbeitnehmer, Leiharbeitnehmer wenn >6 Monate). Branche: alle."
        ),
        "key_article": "§ 1 LkSG (Anwendungsbereich)",
    },
    {
        "nr": 3,
        "key": "EUDR",
        # `materials` traegt hier die eigentliche Entscheidung mit: die
        # Verordnung haengt am Rohstoff (Rind/Leder, Kautschuk, Holz und die
        # daraus gewonnenen zellulosebasierten Fasern), nicht am Fertigprodukt.
        # `value_chain_roles`, weil Art. 1 Marktteilnehmer UND Haendler erfasst.
        "relevant_fields": ["product_categories", "materials", "value_chain_roles",
                            "eu_importer", "branch", "sales_markets"],
        "name": "EUDR – EU-Entwaldungsverordnung",
        "full_name": "Verordnung (EU) 2023/1115 über entwaldungsfreie Lieferketten",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32023R1115&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02023R1115",
        "scope": "EU",
        "criteria": (
            "Gilt für alle Marktteilnehmer und Händler, die in der EU bestimmte Rohstoffe "
            "(Rinder, Kakao, Kaffee, Ölpalme, Kautschuk, Soja, Holz) oder daraus hergestellte Erzeugnisse "
            "in Verkehr bringen, bereitstellen oder ausführen. KMU-Erleichterungen möglich, aber keine Befreiung. "
            "Relevanz hängt an Branche/Produktportfolio, nicht an Mitarbeiterzahl."
        ),
        "key_article": "Art. 1, 3 (Gegenstand & Verbot)",
    },
    {
        "nr": 4,
        "key": "FLR",
        "relevant_fields": ["product_categories", "materials", "value_chain_roles",
                            "eu_importer", "branch"],
        "name": "FLR – EU-Zwangsarbeitsverordnung",
        "full_name": "Verordnung (EU) 2024/3015 - Verbot von in Zwangsarbeit hergestellten Produkten",
        # ELI-Form bewusst beibehalten: zu 2024/3015 gibt es (Stand 09/2026)
        # keine konsolidierte Fassung, der Ursprungsrechtsakt IST der geltende
        # Text. Gleiches gilt fuer Right to Repair (2024/1799). Alle uebrigen
        # EU-Quellen zeigen auf die datumslose konsolidierte CELEX-ID, sonst
        # lieferte der Abruf dauerhaft die Ursprungsfassung — bei der EUDR waere
        # das der Stand VOR den beiden Verschiebungen gewesen.
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024R3015&locale=de",
        "text_url": "https://eur-lex.europa.eu/eli/reg/2024/3015/oj",
        "scope": "EU",
        "criteria": (
            "Gilt für alle Wirtschaftsakteure, die Produkte in der EU in Verkehr bringen, auf dem Markt "
            "bereitstellen oder ausführen. Keine MA-Schwelle. Risikobasierter Ansatz; Fokus auf Unternehmen "
            "mit globalen Lieferketten in Hochrisikoregionen. Branche: alle."
        ),
        "key_article": "Art. 1, 3",
    },
    {
        "nr": 5,
        "key": "CSRD",
        "relevant_fields": ["employees", "revenue_eur", "revenue_eu_eur", "listed", "group_role"],
        "name": "CSRD – EU-Nachhaltigkeitsberichtsrichtlinie",
        "full_name": "Richtlinie (EU) 2022/2464 - Nachhaltigkeitsberichterstattung",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32022L2464&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02022L2464",
        "scope": "EU",
        # Stand: Art. 19a Abs. 1, Art. 29a Abs. 1 und Art. 40a Abs. 1 der
        # Bilanzrichtlinie 2013/34/EU in der konsolidierten Fassung 02013L0034
        # (Aenderung M9 = Richtlinie (EU) 2026/470). Die Bilanzsumme ist seither
        # KEIN Kriterium mehr; beide verbliebenen Merkmale gelten kumulativ.
        "criteria": (
            "Nach der Omnibus-Änderung (Richtlinie (EU) 2026/470) berichtspflichtig sind Unternehmen, "
            "bei denen am Bilanzstichtag sowohl die Grenze von 450 Mio EUR Nettoumsatzerlösen ALS AUCH "
            "die Grenze von durchschnittlich 1.000 Beschäftigten überschritten wird (beide Merkmale "
            "kumulativ). Für Mutterunternehmen gelten dieselben Schwellen auf konsolidierter Basis. "
            "Die Bilanzsumme ist kein Kriterium mehr; eine Börsennotierung allein begründet keine Pflicht. "
            "Drittland-Konzerne: EU-Nettoumsatz >450 Mio EUR in zwei aufeinanderfolgenden Geschäftsjahren "
            "UND eine EU-Tochter bzw. Zweigniederlassung mit Nettoumsatz >200 Mio EUR. "
            "Die neuen Schwellen gelten für Geschäftsjahre, die am oder nach dem 01.01.2027 beginnen. "
            "Branche: alle."
        ),
        "key_article": "Art. 19a, 29a (aktualisiert)",
    },
    {
        "nr": 6,
        "key": "CSRD_DE",
        "relevant_fields": ["employees", "revenue_eur", "revenue_eu_eur", "listed", "group_role"],
        "name": "CSRD-UmsG – deutsches CSRD-Umsetzungsgesetz",
        "full_name": "Gesetz zur Umsetzung der Richtlinie (EU) 2022/2464",
        # Das Gesetz ist noch nicht verkuendet (Stand 09/2026: nach der
        # Anhoerung vom 13.04.2026 weiter im Rechtsausschuss). Amtliche
        # Fundstelle ist deshalb der Regierungsentwurf als Drucksache.
        # `url_note_key` beschriftet den Link, damit klar ist, was einen
        # erwartet - eine 1,5-MB-PDF ohne Sprungmarke ist sonst eine
        # Ueberraschung.
        "url": "https://dserver.bundestag.de/btd/21/018/2101857.pdf",
        "url_note_key": "src_note_csrd_de",
        "scope": "DE",
        "criteria": (
            "Deutsche Umsetzung der CSRD; gilt für in Deutschland ansässige große Unternehmen und "
            "Konzerne gemäß den CSRD-Schwellen (siehe CSRD). Berichtspflicht im Lagebericht (§ 289b HGB-E)."
        ),
        "key_article": "§§ 289b-289h HGB-E",
    },
    {
        "nr": 7,
        "key": "NFRD",
        "relevant_fields": [
            "employees", "revenue_eur", "balance_sheet_eur", "listed", "legal_form",
        ],
        "name": "NFRD – EU-Richtlinie zur nichtfinanziellen Berichterstattung",
        "full_name": "Richtlinie 2014/95/EU - nichtfinanzielle Berichterstattung",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32014L0095&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02014L0095",
        "scope": "EU",
        "criteria": (
            "Vorläufer der CSRD. Ersetzt für Geschäftsjahre ab 2024 schrittweise durch CSRD. "
            "Historisch: große Unternehmen von öffentlichem Interesse mit >500 MA. "
            "Für aktuelle Prüfung i.d.R. nicht mehr relevant."
        ),
        "key_article": "Art. 19a",
    },
    {
        "nr": 8,
        "key": "CSR-RUG",
        # Genau die Felder, die `csr_rug_status()` auswertet — sonst wandern
        # Aenderungen an bedeutungslosen Feldern in den Cache-Schluessel.
        "relevant_fields": ["employees", "listed", "legal_form", "group_role", "branch"],
        "name": "CSR-RUG – CSR-Richtlinie-Umsetzungsgesetz",
        "full_name": "Gesetz zur Stärkung der nichtfinanziellen Berichterstattung",
        # Der BGBl.-Jahrgang 2017 liegt nur im JS-Viewer von bgbl.de und ist
        # maschinell nicht abrufbar (die alte URL lieferte die Portal-Startseite,
        # 556 Zeichen). Stattdessen der geltende Normtext, den das CSR-RUG
        # eingefuegt hat: § 289b HGB (Anwendungsbereich der nichtfinanziellen
        # Erklaerung).
        # url = lesbare Einzelvorschrift, text_url = HGB-Gesamtausgabe, damit
        # alle vier vom CSR-RUG eingefuegten §§ 289b-289e im Kontext landen.
        #
        # ACHTUNG, stille Abhaengigkeit: Die HGB-Gesamtausgabe hat rund 842 000
        # Zeichen und wird vom Fetcher auf LAW_TEXT_MAX_CHARS (Default 400 000)
        # gekappt. § 289b steht bei Zeichen ~259 000 — der Puffer betraegt also
        # nur rund 141 000 Zeichen. Waechst das HGB vor dieser Stelle deutlich,
        # oder wird LAW_TEXT_MAX_CHARS gesenkt, faellt der Anwendungsbereich
        # kommentarlos aus dem Kontext. `test_lawparse.py` prueft deshalb, dass
        # "§ 289b" im gespeicherten Text vorkommt.
        "url": "https://www.gesetze-im-internet.de/hgb/__289b.html",
        "text_url": "https://www.gesetze-im-internet.de/hgb/BJNR002190897.html",
        "scope": "DE",
        "criteria": (
            "Deutsche Umsetzung der NFRD (§§ 289b ff. HGB alte Fassung). "
            "Große kapitalmarktorientierte Unternehmen >500 MA. "
            "Wird durch CSRD-Umsetzung abgelöst."
        ),
        "key_article": "§§ 289b-289e HGB a.F.",
    },
    {
        "nr": 9,
        "key": "TaxonomieVO",
        "relevant_fields": ["employees", "revenue_eur", "revenue_eu_eur", "listed",
                            "group_role", "branch"],
        "name": "Taxonomie-VO – EU-Klassifikation nachhaltiger Tätigkeiten",
        "full_name": "Verordnung (EU) 2020/852 - Rahmen für nachhaltige Investitionen",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32020R0852&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02020R0852",
        "scope": "EU",
        "criteria": (
            "Gilt für Unternehmen, die unter die NFRD/CSRD fallen, sowie für Finanzmarktteilnehmer. "
            "Offenlegung der Taxonomie-Konformität (Umsatz-, CapEx-, OpEx-Anteile). "
            "Relevanz gekoppelt an CSRD-Pflicht."
        ),
        "key_article": "Art. 8",
    },
    {
        "nr": 10,
        "key": "HinSchG",
        "relevant_fields": ["employees_de", "branch"],
        "name": "HinSchG – deutsches Hinweisgeberschutzgesetz",
        "full_name": "Hinweisgeberschutzgesetz",
        # Die Verzeichnis-Seite (…/hinschg/) liefert nur das Inhaltsverzeichnis
        # (2 365 Zeichen). Der Volltext liegt auf der BJNR-Seite.
        "url": "https://www.gesetze-im-internet.de/hinschg/BJNR08C0B0023.html",
        "text_url": "https://www.gesetze-im-internet.de/hinschg/BJNR08C0B0023.html",
        "scope": "DE",
        "criteria": (
            "Gilt für Beschäftigungsgeber in Deutschland ab 50 Beschäftigten. "
            "Pflicht zur Einrichtung interner Meldestellen. Branche: alle."
        ),
        "key_article": "§ 12 HinSchG",
    },
    {
        "nr": 11,
        "key": "RightToRepair",
        "relevant_fields": ["product_categories", "branch", "eu_importer", "sales_markets"],
        "name": "Right to Repair – EU-Reparaturrichtlinie",
        "full_name": "Richtlinie (EU) 2024/1799 - Reparatur von Waren",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024L1799&locale=de",
        "text_url": "https://eur-lex.europa.eu/eli/dir/2024/1799/oj",
        "scope": "EU",
        "criteria": (
            "Gilt für Hersteller bestimmter Warenkategorien (z.B. Haushaltsgeräte, Smartphones, Tablets) "
            "die in der EU in Verkehr gebracht werden. Branche relevant: Konsumgüterhersteller, Elektronik. "
            "Keine MA-Schwelle."
        ),
        "key_article": "Art. 2, 5",
    },
    {
        "nr": 12,
        "key": "Oekodesign",
        # `materials`, weil die Oekodesign-Anforderungen an Stoffen ansetzen
        # (u. a. besorgniserregende chemische Ausruestungen).
        "relevant_fields": ["product_categories", "materials", "value_chain_roles",
                            "branch", "eu_importer"],
        "name": "Ökodesign-VO (ESPR) – EU-Verordnung für nachhaltige Produkte",
        "full_name": "Verordnung (EU) 2024/1781 - nachhaltige Produkte (ESPR)",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024R1781&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024R1781",
        "scope": "EU",
        "criteria": (
            "Gilt für Hersteller, Importeure, Händler von physischen Produkten (mit Ausnahmen wie Lebensmittel) "
            "die in der EU in Verkehr gebracht werden. Branche: nahezu alle warenproduzierenden. "
            "Keine MA-Schwelle."
        ),
        "key_article": "Art. 1, 2",
    },
    {
        "nr": 13,
        "key": "Vernichtungsverbot",
        "relevant_fields": [
            "employees", "revenue_eur", "balance_sheet_eur",
            "product_categories", "value_chain_roles", "branch", "sales_markets",
        ],
        "name": "Vernichtungsverbot – unverkaufte Kleidung und Schuhe",
        "full_name": (
            "Delegierte Verordnung (EU) 2026/296 - Ausnahmen vom Verbot der Vernichtung "
            "unverkaufter Verbraucherprodukte (zur Ökodesign-Verordnung (EU) 2024/1781)"
        ),
        # Zu 2026/296 gibt es (Stand 09/2026) keine konsolidierte Fassung; der
        # Ursprungsrechtsakt IST der geltende Text. Deshalb die `3...`-CELEX-ID,
        # die `fetcher._cellar_text` direkt als gewuenschte Fassung behandelt —
        # wie bei der ESG-Rating-VO (32024R3005). Geprueft am 02.09.2026:
        # publications.europa.eu/resource/celex/32026R0296 liefert den Volltext.
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32026R0296&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32026R0296",
        "scope": "EU",
        # Alle Angaben am Volltext geprueft (02.09.2026):
        #   - Del. VO (EU) 2026/296, ABl. L, 2026/296 vom 22.04.2026, Art. 6:
        #     "Sie gilt ab dem 19. Juli 2026."
        #   - Verbot selbst: Art. 25 Abs. 1 VO (EU) 2024/1781 — ab 19.07.2026,
        #     nicht fuer Kleinst- und Kleinunternehmen, fuer mittlere Unternehmen
        #     ab 19.07.2030. Erfasst sind die Waren des Anhangs VII (Kleidung und
        #     Bekleidungszubehoer, KN 4203/61/62/6504/6505; Schuhe, KN 6401-6405).
        #   - Offenlegung: Art. 24 Abs. 1 VO (EU) 2024/1781 (gleiche Staffelung).
        "criteria": (
            "Betrifft Wirtschaftsteilnehmer, die unverkaufte Verbraucherprodukte der in Anhang VII "
            "der Verordnung (EU) 2024/1781 gelisteten Warengruppen vernichten oder entsorgen: "
            "Kleidung und Bekleidungszubehoer (KN 4203, 61, 62, 6504, 6505) sowie Schuhe "
            "(KN 6401-6405). Das Vernichtungsverbot des Art. 25 Abs. 1 der Verordnung (EU) 2024/1781 "
            "gilt seit dem 19.07.2026; Kleinst- und Kleinunternehmen sind ausgenommen, mittlere "
            "Unternehmen werden ab dem 19.07.2030 erfasst (Groessenklassen nach der Empfehlung "
            "2003/361/EG). Keine Umsatzschwelle im eigentlichen Sinn. "
            "Die Delegierte Verordnung (EU) 2026/296 legt die Ausnahmen abschliessend fest "
            "(Art. 2): gefaehrliche Produkte, sonstige Rechtsverstoesse, Verletzung von Rechten "
            "des geistigen Eigentums bzw. abgelaufene Lizenzen, technisch nicht entfernbare "
            "Kennzeichen, Beschaedigung/Verschlechterung/Kontamination einschliesslich "
            "Hygienemaengeln ohne kosteneffiziente Reparatur, Funktionsuntauglichkeit sowie — "
            "nur nachrangig — ein mindestens achtwoechiges, erfolgloses Spendenangebot an "
            "mindestens drei geeignete sozialwirtschaftliche Einrichtungen in der Union oder "
            "ueber eine leicht zugaengliche Seite der eigenen Website. "
            "Wer sich auf eine Ausnahme beruft, muss die Nachweise nach Art. 3 fuenf Jahre "
            "aufbewahren und binnen 30 Tagen elektronisch vorlegen; nach Art. 4 ist der "
            "Abfallbehandlungseinrichtung eine Erklaerung ueber die geltende Ausnahme zu geben. "
            "Unabhaengig davon verlangt Art. 24 der Verordnung (EU) 2024/1781 die jaehrliche "
            "Offenlegung von Menge und Gewicht entsorgter unverkaufter Verbraucherprodukte. "
            "Branche: Bekleidung, Schuhe, Lederwaren, Handel und Onlinehandel damit."
        ),
        "key_article": "Art. 2 (Ausnahmen), Art. 3 (Dokumentation)",
    },
    {
        "nr": 14,
        "key": "PPWR",
        "relevant_fields": ["product_categories", "value_chain_roles",
                            "branch", "eu_importer", "sales_markets"],
        "name": "PPWR – EU-Verpackungsverordnung",
        "full_name": "Verordnung (EU) 2025/40 - Verpackungen und Verpackungsabfälle",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32025R0040&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02025R0040",
        "scope": "EU",
        "criteria": (
            "Gilt für Hersteller, Importeure, Händler, Fulfilment-Dienstleister und Endvertreiber von "
            "Verpackungen in der EU. Branche relevant: alle Unternehmen mit physischen Produkten/Verpackungen. "
            "Keine MA-Schwelle."
        ),
        "key_article": "Art. 1, 3",
    },
    {
        "nr": 15,
        "key": "MinRohSorgG",
        "relevant_fields": ["product_categories", "eu_importer", "sites"],
        "name": "MinRohSorgG – Sorgfaltspflichten für mineralische Rohstoffe",
        "full_name": "Mineralische-Rohstoffe-Sorgfaltspflichtengesetz",
        # Wie beim HinSchG: die Verzeichnis-Seite liefert nur 767 Zeichen.
        "url": "https://www.gesetze-im-internet.de/minrohsorgg/BJNR086410020.html",
        "text_url": "https://www.gesetze-im-internet.de/minrohsorgg/BJNR086410020.html",
        "scope": "DE",
        "criteria": (
            "Deutsche Durchführung der Konfliktmineralien-VO. Gilt für Unionseinführer mit Sitz in DE "
            "oberhalb der Volumenschwellen aus Anhang I der VO (EU) 2017/821."
        ),
        "key_article": "§ 3 MinRohSorgG",
    },
    {
        "nr": 16,
        "key": "EmpCo",
        "relevant_fields": ["b2c", "env_claims", "value_chain_roles", "sales_markets"],
        "name": "EmpCo – EU-Greenwashing-Richtlinie (UWG)",
        "full_name": "Richtlinie (EU) 2024/825 - Stärkung der Verbraucher für den ökologischen Wandel (UWG-Umsetzung DE)",
        "url": "https://www.gesetze-im-internet.de/uwg_2004/BJNR141400004.html",
        "text_url": "https://www.gesetze-im-internet.de/uwg_2004/BJNR141400004.html",
        "scope": "EU",
        "criteria": (
            "Gilt für alle Unternehmen, die Verbrauchern gegenüber Umweltaussagen machen oder Nachhaltigkeits"
            "siegel verwenden (B2C). Keine MA-Schwelle. Branchenrelevanz: alle B2C-Unternehmen."
        ),
        "key_article": "Art. 1",
    },
    # --- Katalogerweiterung 29.09.2026: Chemikalien-, Produkt-, Standort- und
    # Absatzmarktrecht fuer die Textil- und Modewirtschaft ---
    {
        "nr": 17,
        "key": "REACH_XVII",
        "relevant_fields": ["product_categories", "value_chain_roles", "materials", "sales_markets", "eu_importer", "b2c"],
        "name": "REACH Anhang XVII – Stoffbeschränkungen für Textilien und Leder",
        "full_name": "Verordnung (EG) Nr. 1907/2006 (REACH), Titel VIII und Anhang XVII – Beschränkungen der Herstellung, des Inverkehrbringens und der Verwendung bestimmter gefährlicher Stoffe, Gemische und Erzeugnisse",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32006R1907&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02006R1907",
        "scope": "EU",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (http://publications.europa.eu/resource/celex/02006R1907-20260622 (Accept: application/xhtml+xml, Accept-Language: deu) – Art. 3, 67, 141, Anhang XVII Nr. 43, 46a, 68, 72, 76, 77, 79, 80, 81, Anlage 12, Liste der Änderungsrechtsakte M1–M85; https://publications.europa.eu/webapi/rdf/sparql – Änderungsrechtsakte seit 01.06.2025 (32025R1090, 32025R1731, 32025R1988, 32026R0859, 32026R1168) und jüngste Konsolidierung 02006R1907-20260622).
        "criteria": (
            "Nach Art. 67 Abs. 1 darf ein Stoff als solcher, in einem Gemisch oder in einem Erzeugnis, "
            "für den eine Beschränkung nach Anhang XVII gilt, nur hergestellt, in Verkehr gebracht oder "
            "verwendet werden, wenn die Maßgaben dieser Beschränkung beachtet werden; betroffen sind "
            "damit Hersteller, Importeure (die Einfuhr gilt nach Art. 3 Nr. 12 als Inverkehrbringen) und "
            "Händler, keine Mitarbeiter- oder Umsatzschwelle. Eintrag 43: Azofarbstoffe, die aromatische "
            "Amine der Anlage 8 in Konzentrationen > 30 mg/kg freisetzen können, dürfen nicht in Textil- "
            "und Ledererzeugnissen mit längerem Haut- oder Mundkontakt verwendet werden (Kleidung, "
            "Bettwäsche, Handtücher, Schuhe, Handschuhe u. a.); Azofarbstoffe der Anlage 9 nicht über 0,1 "
            "Gew.-% zum Färben. Eintrag 46a: Nonylphenolethoxylate ab 0,01 Gew.-% in waschbaren "
            "Textilerzeugnissen (mindestens 80 % Textilfasern) seit 03.02.2021 verboten, ausgenommen "
            "Gebraucht- und reine Recyclingtextilien ohne NPE-Einsatz. Eintrag 68: C9–C14-PFCA seit "
            "25.02.2023 in Erzeugnissen nur unter 25 ppb (Summe PFCA und Salze) bzw. 260 ppb (verwandte "
            "Stoffe), für öl- und wasserabweisende Arbeitsschutztextilien seit 04.07.2023. Eintrag 72 (VO "
            "(EU) 2018/1513): seit 01.11.2020 dürfen die CMR-Stoffe der Anlage 12 in Kleidung, Zubehör, "
            "hautnahen Textilien und Schuhwaren für Verbraucher nicht die dort genannten Konzentrationen "
            "im homogenen Material erreichen (je Stoff 1 bis 3 000 mg/kg, z. B. Formaldehyd 75 mg/kg); "
            "ausgenommen u. a. reine Leder-/Pelzprodukte, nicht textile Verschlüsse, Gebrauchtware, "
            "Teppiche sowie Produkte nach PSA-Verordnung und MDR. Eintrag 76 (VO (EU) 2021/2030): "
            "N,N-Dimethylformamid ab 0,3 % nur mit DNEL-Werten und Risikomanagement, seit 12.12.2023, für "
            "PU-Beschichtung von Textilien seit 12.12.2024, für Trocken- und Nassspinnen synthetischer "
            "Fasern seit 12.12.2025. Branche: Textil- und Bekleidungsherstellung, Textilveredlung, "
            "Schuhe, Lederwaren, Handel und Import dieser Waren. Einordnung des Profils: Die "
            "Beschraenkungen binden jedes Unternehmen, das Textil-, Leder- oder Schuherzeugnisse in der "
            "EU herstellt, einfuehrt oder in Verkehr bringt; ob ein einzelner Stoff tatsaechlich "
            "enthalten ist, sagt das Profil nicht. Werden solche Erzeugnisse (auch Vor- und "
            "Zwischenprodukte) auf dem Markt der Union bereitgestellt, ist die Pflicht zur Einhaltung "
            "deshalb gegeben (ja); nur wenn ausschliesslich ausserhalb von EU/EWR abgesetzt wird, greift "
            "sie nicht."
        ),
        "key_article": "Art. 67, Anhang XVII Nr. 43, 46a, 68, 72, 76 (neu: 79, 80, 81)",
        "text_from": "^\\s*(?:ANHANG|ANNEX|ANNEXE|ANEXO|ALLEGATO)\\s+XVII\\s*$",
        "focus_entries": ["43", "46a", "68", "72", "76", "79", "80", "81"],
        "focus_label": "Anhang XVII Nr. {n}",
    },
    {
        "nr": 18,
        "key": "REACH_ART33",
        "relevant_fields": ["svhc_status"],
        "name": "REACH Art. 33 – Informationspflicht zu SVHC in Erzeugnissen",
        "full_name": "Verordnung (EG) Nr. 1907/2006 (REACH), Art. 33 – Pflicht zur Weitergabe von Informationen über Stoffe in Erzeugnissen (Stoffe der Kandidatenliste nach Art. 59 Abs. 1)",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32006R1907&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02006R1907",
        "scope": "EU",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (http://publications.europa.eu/resource/celex/02006R1907-20260622 – Art. 3 Nr. 3, 4, 10–14, 33–35; Art. 7 Abs. 2 und 7; Art. 33; Art. 141).
        "criteria": (
            "Verpflichtet ist jeder Lieferant eines Erzeugnisses, also nach Art. 3 Nr. 33 der Produzent "
            "oder Importeur eines Erzeugnisses, der Händler oder ein anderer Akteur der Lieferkette, der "
            "das Erzeugnis in Verkehr bringt. Enthält ein Erzeugnis einen Stoff der Kandidatenliste "
            "(Kriterien des Art. 57, ermittelt nach Art. 59 Abs. 1) in einer Konzentration von mehr als "
            "0,1 Massenprozent (w/w), muss er dem gewerblichen Abnehmer die ihm vorliegenden, für eine "
            "sichere Verwendung ausreichenden Informationen geben, mindestens den Namen des Stoffes (Art. "
            "33 Abs. 1). Verbrauchern sind diese Informationen auf Ersuchen binnen 45 Tagen kostenlos zur "
            "Verfügung zu stellen (Art. 33 Abs. 2). Die Pflicht besteht unabhängig von Menge und "
            "Unternehmensgröße und greift, sobald ein enthaltener Stoff in die Kandidatenliste "
            "aufgenommen wird. Zusätzlich müssen Produzenten und Importeure von Erzeugnissen die ECHA "
            "unterrichten, wenn ein solcher Stoff über 0,1 % enthalten ist und die Menge insgesamt mehr "
            "als 1 Tonne pro Jahr beträgt (Art. 7 Abs. 2, sechs Monate nach Aufnahme in die Liste). "
            "Branche: alle, die Textilien, Bekleidung, Schuhe, Accessoires oder andere Erzeugnisse "
            "herstellen, importieren oder weiterverkaufen."
        ),
        "key_article": "Art. 33 (i. V. m. Art. 3 Nr. 33, Art. 7 Abs. 2, Art. 59)",
    },
    {
        "nr": 19,
        "key": "SCIP",
        "relevant_fields": ["svhc_status", "value_chain_roles", "b2c"],
        "name": "SCIP – Meldepflicht für SVHC in Erzeugnissen an die ECHA",
        "full_name": "§ 16f Chemikaliengesetz (ChemG) – Informationspflicht der Lieferanten gegenüber der ECHA-Datenbank nach Art. 9 Abs. 2 RL 2008/98/EG (Umsetzung von Art. 9 Abs. 1 Buchst. i Abfallrahmenrichtlinie)",
        "url": "https://www.gesetze-im-internet.de/chemg/__16f.html",
        "text_url": "https://www.gesetze-im-internet.de/chemg/__16f.html",
        "scope": "EU",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (https://www.gesetze-im-internet.de/chemg/__16f.html; https://www.gesetze-im-internet.de/chemg/BJNR017180980.html (Stand: zuletzt geändert durch Art. 1 G v. 29.3.2026, BGBl. 2026 I Nr. 86; § 26 Abs. 1 Nr. 6a)).
        "criteria": (
            "Verpflichtet ist, wer als Lieferant eines Erzeugnisses im Sinne von Art. 3 Nr. 33 REACH "
            "(Produzent, Importeur, Händler oder anderer Akteur der Lieferkette) Erzeugnisse in Verkehr "
            "bringt, die einen Kandidatenlistenstoff über 0,1 Massenprozent enthalten und daher unter "
            "Art. 33 Abs. 1 REACH fallen. Er muss der ECHA unverzüglich nach dem Inverkehrbringen für die "
            "SCIP-Datenbank Stoffname (mit EG- und CAS-Nummer, falls verfügbar), Konzentrationsbereich, "
            "Material- oder Gemischkategorie, Bezeichnung und Identifikator des Erzeugnisses, "
            "Erzeugniskategorie, Komponenten bei komplexen Gegenständen, Herstellung in oder außerhalb "
            "der EU sowie Hinweise zur sicheren Verwendung übermitteln (§ 16f Abs. 1 ChemG). Ausgenommen "
            "sind Erzeugnisse mit militärischer Zweckbestimmung. Nach Auslegung der "
            "Bund/Länder-Arbeitsgemeinschaft Chemikaliensicherheit besteht keine Meldepflicht, wenn "
            "ausschließlich an Verbraucher abgegeben wird, und bereits der Import eines solchen "
            "Erzeugnisses löst sie aus. Die Pflicht gilt seit dem 05.01.2021; Verstöße sind nach § 26 "
            "Abs. 1 Nr. 6a ChemG bußgeldbewehrt. In den übrigen Mitgliedstaaten gilt dieselbe Pflicht "
            "über deren Umsetzung von Art. 9 Abs. 1 Buchst. i RL 2008/98/EG. Branche: alle Hersteller, "
            "Importeure und Händler von Erzeugnissen im B2B-Vertrieb, auch Textilien, Schuhe und "
            "Accessoires."
        ),
        "key_article": "§ 16f ChemG (i. V. m. Art. 33 Abs. 1 REACH)",
    },
    {
        "nr": 20,
        "key": "POP",
        "relevant_fields": ["materials", "product_categories", "value_chain_roles", "sales_markets", "eu_importer"],
        "name": "POP-Verordnung – EU-Verbot persistenter organischer Schadstoffe",
        "full_name": "Verordnung (EU) 2019/1021 über persistente organische Schadstoffe (Neufassung)",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32019R1021&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02019R1021",
        "scope": "EU",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (http://publications.europa.eu/resource/celex/02019R1021-20260930 – Art. 3, 4, 7, 22, Anhang I (PFOA, PFOS, PFHxS, DecaBDE/PBDE, Dechloran Plus, UV-328, Methoxychlor, Chlorpyrifos), Änderungsliste M1–M18; https://publications.europa.eu/webapi/rdf/sparql – Änderungsrechtsakte seit 01.06.2025: 32025R1482, 32025R2457, 32026R1423).
        "criteria": (
            "Die Herstellung, das Inverkehrbringen und die Verwendung der in Anhang I aufgeführten Stoffe "
            "als solche, in Gemischen oder in Erzeugnissen sind verboten (Art. 3 Abs. 1); das Verbot "
            "trifft jeden Hersteller, Importeur und Händler von Erzeugnissen, ohne Größen- oder "
            "Mengenschwelle. Ausgenommen sind unbeabsichtigte Spurenverunreinigungen unterhalb der in "
            "Anhang I je Stoff festgelegten Werte (Art. 4 Abs. 1 Buchst. b) und Erzeugnisse, die vor "
            "Geltung des Verbots bereits verwendet wurden (Art. 4 Abs. 2). Textilrelevante Grenzwerte in "
            "Anhang I: PFOA, PFOS und PFHxS sowie deren Salze je höchstens 0,025 mg/kg, verwandte "
            "Verbindungen je höchstens 1 mg/kg; DecaBDE und die übrigen PBDE in Gemischen und "
            "Erzeugnissen in Summe 10 mg/kg, bei Recyclingmaterial abweichend 350 mg/kg ab 30.12.2025 und "
            "200 mg/kg ab 30.12.2027; Dechloran Plus bis 15.04.2028 höchstens 1 000 mg/kg, danach 1 "
            "mg/kg; UV-328 höchstens 100 mg/kg ab 04.08.2025, 10 mg/kg ab 04.08.2027 und 1 mg/kg ab "
            "04.08.2029. Für nach dem 15.07.2019 neu aufgenommene Stoffe gilt für Erzeugnisse, die bis "
            "zum Geltungsbeginn hergestellt wurden, eine Übergangsfrist von sechs Monaten (Art. 4 Abs. "
            "2). Abfälle mit Stoffen des Anhangs IV oberhalb der dortigen Grenzwerte sind so zu "
            "behandeln, dass die POP zerstört werden (Art. 7). Branche: Textil- und "
            "Bekleidungsherstellung (wasser-, öl- und schmutzabweisende sowie flammhemmende "
            "Ausrüstungen), Schuhe, Import und Handel mit Erzeugnissen, Recycling. Einordnung des "
            "Profils: Das Verbot gilt fuer alle Erzeugnisse; praktisch bedeutsam ist es bei wasser-, oel- "
            "oder schmutzabweisender, flammhemmender oder PFAS-haltiger Ausruestung und bei "
            "Beschichtungen. Nennt das Profil eine solche Ausruestung und wird in der EU abgesetzt, gilt "
            "es (ja); ist die Ausruestung nicht bekannt oder nennt das Profil keine solche Ausruestung, "
            "ist es zu pruefen (moeglich); nein nur bei Absatz ausschliesslich ausserhalb von EU/EWR."
        ),
        "key_article": "Art. 3, Art. 4, Anhang I (PFOA, PFOS, PFHxS, PBDE/DecaBDE, Dechloran Plus, UV-328)",
    },
    {
        "nr": 21,
        "key": "BPR",
        "relevant_fields": ["materials", "sales_markets"],
        "name": "Biozid-VO – Kennzeichnung behandelter Waren",
        "full_name": "Verordnung (EU) Nr. 528/2012 über die Bereitstellung auf dem Markt und die Verwendung von Biozidprodukten, Art. 58 – Inverkehrbringen von behandelten Waren",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32012R0528&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02012R0528",
        "scope": "EU",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (http://publications.europa.eu/resource/celex/02012R0528-20260819 – Art. 3 Abs. 1 Buchst. l, Art. 58, 94, 97; https://publications.europa.eu/webapi/rdf/sparql – Änderungsrechtsakte seit 01.06.2025: 32026R0447, 32026R1165).
        "criteria": (
            "Behandelte Waren sind Stoffe, Gemische oder Erzeugnisse, die mit einem oder mehreren "
            "Biozidprodukten behandelt wurden oder solche absichtlich enthalten (Art. 3 Abs. 1 Buchst. "
            "l), etwa antimikrobiell, antibakteriell oder gegen Insekten ausgerüstete Textilien und "
            "Schuhe. Sie dürfen nur in Verkehr gebracht werden, wenn alle enthaltenen Wirkstoffe für die "
            "jeweilige Produktart und Verwendung genehmigt bzw. in der Liste nach Art. 9 Abs. 2 oder in "
            "Anhang I aufgeführt sind und deren Bedingungen erfüllt sind (Art. 58 Abs. 2). Die für das "
            "Inverkehrbringen verantwortliche Person muss die Ware kennzeichnen, wenn der Hersteller "
            "biozide Eigenschaften bewirbt oder die Wirkstoffgenehmigung es verlangt: Hinweis auf "
            "enthaltene Biozidprodukte, belegte biozide Eigenschaft, alle Wirkstoffe, Nanomaterialien mit "
            "dem Zusatz „Nano“ und Verwendungshinweise (Art. 58 Abs. 3), deutlich sichtbar und in der "
            "Amtssprache des Mitgliedstaats (Art. 58 Abs. 6). Der Lieferant muss Verbrauchern auf Antrag "
            "binnen 45 Tagen kostenlos Informationen über die biozide Behandlung geben (Art. 58 Abs. 5). "
            "Keine Größen- oder Mengenschwelle; ausgenommen ist nur die reine Begasung oder Desinfektion "
            "von Transport- und Lagerbehältern ohne zu erwartende Rückstände (Art. 58 Abs. 1). Die "
            "Verordnung gilt seit 01.09.2013, Art. 94 enthält Übergangsregeln für Wirkstoffe im "
            "Prüfprogramm. Branche: Textil- und Bekleidungsherstellung, Textilveredlung, Schuhe, Import "
            "und Handel mit ausgerüsteter Ware."
        ),
        "key_article": "Art. 58 (i. V. m. Art. 3 Abs. 1 Buchst. l, Art. 94)",
    },
    {
        "nr": 22,
        "key": "TKVO",
        "relevant_fields": ["product_categories", "value_chain_roles", "sales_markets", "eu_importer", "b2c"],
        "name": "TKVO – EU-Textilkennzeichnungsverordnung",
        "full_name": "Verordnung (EU) Nr. 1007/2011 über die Bezeichnungen von Textilfasern und die damit zusammenhängende Etikettierung und Kennzeichnung der Faserzusammensetzung von Textilerzeugnissen",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32011R1007&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02011R1007",
        "scope": "EU",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (http://publications.europa.eu/resource/celex/02011R1007-20180215 – Art. 2, 3, 11, 12, 14, 15, 16, 17, 28; https://publications.europa.eu/webapi/rdf/sparql – keine Änderungsrechtsakte seit 01.06.2025, jüngste Konsolidierung 02011R1007-20180215).
        "criteria": (
            "Die Verordnung gilt für Textilerzeugnisse, die auf dem Unionsmarkt bereitgestellt werden, "
            "sowie für gleichgestellte Erzeugnisse mit mindestens 80 % Textilfaseranteil, Möbel-, Schirm- "
            "und Matratzenbezüge und Textilkomponenten, deren Zusammensetzung angegeben wird (Art. 2). "
            "Textilerzeugnisse müssen bei der Bereitstellung auf dem Markt mit der Faserzusammensetzung "
            "etikettiert oder gekennzeichnet sein, dauerhaft, gut lesbar und fest angebracht (Art. 14), "
            "nur mit den Faserbezeichnungen des Anhangs I (Art. 5) und in der Amtssprache des "
            "Mitgliedstaats, in dem sie Verbrauchern angeboten werden (Art. 16 Abs. 3). Verantwortlich "
            "ist der Hersteller, bei Herstellern außerhalb der Union der Einführer; ein Händler gilt als "
            "Hersteller, wenn er unter eigenem Namen oder eigener Marke in Verkehr bringt, das Etikett "
            "selbst anbringt oder dessen Inhalt ändert, und muss sonst prüfen, dass die Kennzeichnung "
            "vorhanden ist (Art. 15). Die Faserangaben müssen Verbrauchern vor dem Kauf deutlich sichtbar "
            "sein, auch im Onlinehandel (Art. 16 Abs. 1). Nichttextile Teile tierischen Ursprungs sind "
            "mit „Enthält nichttextile Teile tierischen Ursprungs“ anzugeben (Art. 12). Ausgenommen sind "
            "u. a. die in Anhang V aufgeführten Erzeugnisse und Maßanfertigungen selbständiger Schneider "
            "(Art. 2 Abs. 4, Art. 17). Keine Größenschwelle. Branche: Textil- und Bekleidungsherstellung, "
            "Heimtextilien, Import, Groß- und Einzelhandel einschließlich Onlinehandel. Einordnung des "
            "Profils: Textilprodukte im Sinne der Verordnung sind alle Produktkategorien ausser Schuhen "
            "und reinen Lederwaren (dort nur, soweit Textilteile gekennzeichnet werden). Werden solche "
            "Produkte in der EU bereitgestellt und ist das Unternehmen Hersteller, Markeninhaber, "
            "Importeur oder Haendler, gilt die Verordnung (ja); fuehrt das Profil nur Schuhe oder "
            "Lederwaren, ist es zu pruefen (moeglich)."
        ),
        "key_article": "Art. 14, 15, 16 (i. V. m. Art. 2, 5, 11, 12, Anhang I)",
    },
    {
        "nr": 23,
        "key": "GPSR",
        "relevant_fields": ["b2c", "product_categories", "value_chain_roles", "sales_markets", "eu_importer"],
        "name": "GPSR – EU-Produktsicherheitsverordnung",
        "full_name": "Verordnung (EU) 2023/988 über die allgemeine Produktsicherheit",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32023R0988&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02023R0988",
        "scope": "EU",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (http://publications.europa.eu/resource/celex/02023R0988-20260529 – Art. 2, 3, 4, 9, 11, 12, 16, 19, 20, 51, 52, Änderungsliste (M1 = VO (EU) 2024/2748); https://publications.europa.eu/webapi/rdf/sparql – einziger Änderungsrechtsakt 32024R2748).
        "criteria": (
            "Die Verordnung gilt für neue, gebrauchte, reparierte oder wiederaufgearbeitete "
            "Verbraucherprodukte, die in Verkehr gebracht oder auf dem Markt bereitgestellt werden, "
            "soweit keine spezifischeren Sicherheitsvorschriften der Union bestehen (Art. 2); Textilien, "
            "Bekleidung und Schuhe für Verbraucher fallen damit grundsätzlich darunter. Pflichten treffen "
            "die Wirtschaftsakteure nach Art. 3: Hersteller, Bevollmächtigte, Einführer, Händler und "
            "Fulfilment-Dienstleister sowie Anbieter von Online-Marktplätzen. Hersteller müssen vor dem "
            "Inverkehrbringen eine interne Risikoanalyse durchführen und technische Unterlagen erstellen, "
            "die sie zehn Jahre aufbewahren, das Produkt mit Typen-, Chargen- oder Seriennummer sowie "
            "Name, Postanschrift und elektronischer Adresse kennzeichnen und Anweisungen und "
            "Sicherheitsinformationen in der Landessprache beifügen (Art. 9). Einführer prüfen diese "
            "Anforderungen und geben zusätzlich ihre eigenen Kontaktdaten an (Art. 11), Händler "
            "vergewissern sich vor der Bereitstellung (Art. 12). Ein Produkt darf nur in Verkehr gebracht "
            "werden, wenn ein in der Union niedergelassener Wirtschaftsakteur dafür verantwortlich ist "
            "(Art. 16). Online-Angebote müssen Herstellerangaben, bei Herstellern außerhalb der EU die "
            "verantwortliche Person, Produktabbildung und Warnhinweise enthalten (Art. 19); Unfälle sind "
            "über das Safety-Business-Gateway zu melden (Art. 20). Geltung seit 13.12.2024, keine "
            "Größenschwelle. Branche: alle Hersteller, Importeure und Händler von Verbraucherprodukten "
            "einschließlich Onlinehandel. Einordnung des Profils: Die Verordnung erfasst "
            "Verbraucherprodukte. Mit B2C-Geschaeft und Absatz in der EU gilt sie (ja). Ohne "
            "B2C-Geschaeft ist sie zu pruefen (moeglich), weil auch Produkte, die vernuenftigerweise bei "
            "Verbrauchern landen, erfasst sein koennen; fuer PSA und Medizinprodukte gehen deren "
            "Spezialvorschriften vor."
        ),
        "key_article": "Art. 9, 11, 12, 16, 19 (Anwendungsbereich Art. 2)",
    },
    {
        "nr": 24,
        "key": "PSA",
        "relevant_fields": ["product_categories", "value_chain_roles", "sales_markets"],
        "name": "PSA-Verordnung – persönliche Schutzausrüstung",
        "full_name": "Verordnung (EU) 2016/425 über persönliche Schutzausrüstungen und zur Aufhebung der Richtlinie 89/686/EWG",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32016R0425&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02016R0425",
        "scope": "EU",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (http://publications.europa.eu/resource/celex/02016R0425-20260529 – Art. 2, 3, 8, 10, 11, 18, 19, 47, 48, Anhang I; https://publications.europa.eu/webapi/rdf/sparql – einziger Änderungsrechtsakt 32024R2748).
        "criteria": (
            "Die Verordnung gilt für Ausrüstung, die entworfen und hergestellt wird, um von einer Person "
            "als Schutz gegen Risiken für Gesundheit oder Sicherheit getragen oder gehalten zu werden, "
            "einschließlich unerlässlicher Ersatzteile und Verbindungssysteme (Art. 2, Art. 3 Nr. 1), "
            "etwa Schutzkleidung, Schutzhandschuhe und Sicherheitsschuhe. Nicht erfasst ist unter anderem "
            "PSA für Streit- und Ordnungskräfte sowie private Schutzausrüstung gegen nicht extreme "
            "Witterung oder gegen Nässe beim Geschirrspülen (Art. 2 Abs. 2). Pflichten treffen "
            "Hersteller, Bevollmächtigte, Einführer und Händler (Art. 3 Nr. 4 bis 8): Hersteller müssen "
            "die grundlegenden Gesundheitsschutz- und Sicherheitsanforderungen des Anhangs II erfüllen, "
            "technische Unterlagen erstellen, das Konformitätsbewertungsverfahren nach Risikokategorie "
            "durchführen, die EU-Konformitätserklärung ausstellen, die CE-Kennzeichnung anbringen und die "
            "Unterlagen zehn Jahre aufbewahren (Art. 8). Kategorie I erlaubt die interne "
            "Fertigungskontrolle, Kategorie II und III verlangen eine EU-Baumusterprüfung durch eine "
            "notifizierte Stelle, Kategorie III zusätzlich überwachte Fertigung (Art. 18, 19, Anhang I). "
            "Einführer bringen nur konforme PSA in Verkehr und prüfen Konformitätsbewertung, Unterlagen "
            "und CE-Kennzeichnung (Art. 10), Händler kontrollieren CE-Kennzeichnung, Unterlagen und "
            "Anleitung (Art. 11). Geltung seit 21.04.2018, keine Größenschwelle. Branche: Hersteller, "
            "Importeure und Händler von Schutzkleidung, Arbeits- und Sicherheitsschuhen, Handschuhen und "
            "technischen Textilien mit Schutzfunktion."
        ),
        "key_article": "Art. 8, 10, 11, 19 (Anwendungsbereich Art. 2, Risikokategorien Anhang I)",
    },
    {
        "nr": 25,
        "key": "MDR",
        "relevant_fields": ["product_categories", "value_chain_roles", "sales_markets"],
        "name": "MDR – EU-Medizinprodukteverordnung",
        "full_name": "Verordnung (EU) 2017/745 über Medizinprodukte",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32017R0745&locale=de",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02017R0745",
        "scope": "EU",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (http://publications.europa.eu/resource/celex/02017R0745-20260719 – Art. 2 Nr. 1, 30, 32–35; Art. 10, 13, 14, 15, 120, 123; Änderungsliste M1–M8; https://publications.europa.eu/webapi/rdf/sparql – Änderungsrechtsakte seit 01.06.2025: 32025R1920, 32025R2457, 32026R1359, 32026R1451).
        "criteria": (
            "Medizinprodukte sind Gegenstände, Materialien oder andere Produkte, die dem Hersteller "
            "zufolge für Menschen bestimmt sind und einen medizinischen Zweck nach Art. 2 Nr. 1 erfüllen "
            "sollen; textile Produkte fallen darunter, wenn der Hersteller ihnen eine solche "
            "Zweckbestimmung gibt. Wirtschaftsakteure sind Hersteller (wer ein Produkt herstellt oder "
            "herstellen lässt und unter eigenem Namen oder eigener Marke vermarktet), Bevollmächtigte für "
            "Hersteller außerhalb der Union, Importeure und Händler (Art. 2 Nr. 30, 32 bis 35). "
            "Hersteller müssen unter anderem ein Risikomanagement- und Qualitätsmanagementsystem "
            "einrichten, eine klinische Bewertung durchführen, technische Dokumentation erstellen und "
            "eine für die Einhaltung der Regulierungsvorschriften verantwortliche Person benennen (Art. "
            "10, 15); Importeure prüfen CE-Kennzeichnung und EU-Konformitätserklärung (Art. 13), Händler "
            "die Anforderungen mit gebührender Sorgfalt (Art. 14). Die Verordnung gilt seit 26.05.2021 "
            "(Art. 123 Abs. 2). Nach Art. 120 Abs. 3a bis 3c dürfen Produkte mit gültiger Bescheinigung "
            "nach den alten Richtlinien bis 31.12.2027 (Klasse III, implantierbare Klasse IIb) bzw. "
            "31.12.2028 (übrige Klasse IIb, IIa, Klasse I steril oder mit Messfunktion) weiter in Verkehr "
            "gebracht werden, sofern bis 26.05.2024 ein QMS eingerichtet und ein Antrag gestellt sowie "
            "bis 26.09.2024 eine schriftliche Vereinbarung mit einer Benannten Stelle geschlossen wurde; "
            "dasselbe Datum 31.12.2028 gilt für bisher selbstzertifizierte Produkte, die nun eine "
            "Benannte Stelle brauchen (Abs. 3b). Keine Größenschwelle. Branche: Hersteller, Importeure "
            "und Händler medizinischer Textilien und Hilfsmittel."
        ),
        "key_article": "Art. 2, 10, 13, 14, 120, 123",
    },
    {
        "nr": 26,
        "key": "Schuhkennzeichnung",
        "relevant_fields": ["product_categories", "value_chain_roles", "sales_markets"],
        "name": "Schuhkennzeichnung – Materialangaben für Schuhe",
        "full_name": "Richtlinie 94/11/EG über die Kennzeichnung von Materialien für die Hauptbestandteile von Schuherzeugnissen zum Verkauf an den Verbraucher; deutsche Umsetzung: § 10a und Anlage 11 Bedarfsgegenständeverordnung (BedGgstV)",
        "url": "https://www.gesetze-im-internet.de/bedggstv/__10a.html",
        "text_url": "https://www.gesetze-im-internet.de/bedggstv/BJNR008660992.html",
        "scope": "EU",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (https://www.gesetze-im-internet.de/bedggstv/__10a.html; https://www.gesetze-im-internet.de/bedggstv/anlage_11.html).
        "criteria": (
            "Schuherzeugnisse sind Erzeugnisse mit Sohle, die den Fuß schützen oder bedecken, "
            "einschließlich getrennt verkaufter Bestandteile, soweit sie zur Abgabe an Verbraucher "
            "bestimmt sind (Anlage 11 Nr. 1 BedGgstV, Art. 1 RL 94/11/EG). Vor dem gewerbsmäßigen "
            "Inverkehrbringen muss der Hersteller oder sein in der EU niedergelassener Bevollmächtigter, "
            "ohne EU-Niederlassung derjenige, der die Schuhe erstmals in der EU in Verkehr bringt, an "
            "mindestens einem Schuh jedes Paares lesbar, haltbar und gut sichtbar das Material von "
            "Obermaterial, Futter und Decksohle sowie Laufsohle angeben, als Piktogramm oder schriftlich "
            "(§ 10a Abs. 1 und 2). Anzugeben ist das Material, das mindestens 80 % der Fläche von "
            "Obermaterial bzw. Futter und Decksohle oder 80 % des Volumens der Laufsohle ausmacht, sonst "
            "die beiden Hauptmaterialien (§ 10a Abs. 3, Art. 4 Abs. 1 RL). Materialkategorien sind Leder, "
            "beschichtetes Leder, natürliche und synthetische Textilien sowie sonstiges Material (Anlage "
            "11 Nr. 3). Wer Schuhe gewerbsmäßig abgibt, also auch der Handel, muss sicherstellen, dass "
            "die Kennzeichnung bei der Abgabe angebracht ist (§ 10a Abs. 1 Satz 3). Ausgenommen sind "
            "gebrauchte Schuhe, Sicherheitsschuhwerk nach PSA-Recht und Spielzeugschuhe (§ 10a Abs. 2). "
            "Keine Größenschwelle; die Richtlinie ist in allen Mitgliedstaaten seit 23.03.1996 "
            "anzuwenden. Branche: Schuhhersteller, Importeure und Schuhhandel einschließlich "
            "Onlinehandel."
        ),
        "key_article": "§ 10a BedGgstV, Anlage 11 (Art. 1, 4 RL 94/11/EG)",
    },
    {
        "nr": 27,
        "key": "EnEfG",
        "relevant_fields": ["energy_gwh"],
        "name": "EnEfG – Energieeffizienzgesetz",
        "full_name": "Gesetz zur Steigerung der Energieeffizienz in Deutschland (Energieeffizienzgesetz – EnEfG) vom 13.11.2023 (BGBl. 2023 I Nr. 309)",
        "url": "https://www.gesetze-im-internet.de/enefg/BJNR1350B0023.html",
        "text_url": "https://www.gesetze-im-internet.de/enefg/BJNR1350B0023.html",
        "scope": "DE",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (https://www.gesetze-im-internet.de/enefg/__8.html; https://www.gesetze-im-internet.de/enefg/__9.html).
        "criteria": (
            "Unternehmen mit einem jährlichen durchschnittlichen Gesamtendenergieverbrauch innerhalb der "
            "letzten drei abgeschlossenen Kalenderjahre von mehr als 7,5 Gigawattstunden müssen ein "
            "Energiemanagementsystem nach DIN EN ISO 50001 oder ein Umweltmanagementsystem nach EMAS "
            "einrichten (§ 8 Abs. 1, § 3 Nr. 16 und 29). Wer diesen Status bis 17.11.2023 erlangt hatte, "
            "musste das System bis 18.07.2025 einrichten, wer ihn später erlangt, spätestens 20 Monate "
            "danach; bis dahin entfällt die Energieauditpflicht nach § 8 EDL-G (§ 8 Abs. 2). Das System "
            "muss zusätzlich Energieflüsse, Prozesstemperaturen und Abwärmequellen erfassen, technisch "
            "realisierbare Einspar- und Abwärmemaßnahmen identifizieren und diese nach DIN EN 17463 auf "
            "Wirtschaftlichkeit bewerten (§ 8 Abs. 3). Unternehmen mit mehr als 2,5 Gigawattstunden "
            "müssen binnen drei Jahren konkrete, durchführbare Umsetzungspläne für alle als "
            "wirtschaftlich identifizierten Maßnahmen aus EnMS, UMS oder Energieaudit erstellen, von "
            "Zertifizierern, Umweltgutachtern oder Energieauditoren bestätigen lassen und veröffentlichen "
            "(§ 9); wirtschaftlich ist eine Maßnahme mit positivem Kapitalwert nach höchstens 50 % der "
            "Nutzungsdauer, begrenzt auf Nutzungsdauern bis 15 Jahre. Maßgeblich ist allein der "
            "Energieverbrauch, nicht Beschäftigtenzahl oder Umsatz. Das Gesetz gilt seit 18.11.2023. "
            "Branche: alle energieintensiven Unternehmen, insbesondere Textilveredlung, Spinnereien und "
            "Webereien."
        ),
        "key_article": "§ 8, § 9",
    },
    {
        "nr": 28,
        "key": "AbwV38",
        "relevant_fields": ["wet_processing_de", "branch"],
        "name": "AbwV Anhang 38 – Abwasseranforderungen für Textilherstellung und -veredlung",
        "full_name": "Abwasserverordnung (AbwV), Anhang 38 – Textilherstellung, Textilveredlung",
        "url": "https://www.gesetze-im-internet.de/abwv/anhang_38.html",
        "text_url": "https://www.gesetze-im-internet.de/abwv/anhang_38.html",
        "scope": "DE",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (https://www.gesetze-im-internet.de/abwv/anhang_38.html; https://www.gesetze-im-internet.de/abwv/__1.html).
        "criteria": (
            "Anhang 38 gilt für Abwasser, dessen Schadstofffracht im Wesentlichen aus der gewerblichen "
            "und industriellen Bearbeitung und Verarbeitung von Spinnstoffen und Garnen sowie der "
            "Textilveredlung stammt; ausgenommen sind Abwasser aus der Rohwollwäsche, dem Foto- und "
            "Galvanikbereich, der Chemischreinigung mit Halogenkohlenwasserstoffen sowie aus "
            "Betriebswasseraufbereitung und indirekten Kühlsystemen (Teil A). Die AbwV bestimmt "
            "Mindestanforderungen für das Einleiten in Gewässer; Betreiberpflichten und gekennzeichnete "
            "Emissionsgrenzwerte hat der Einleiter einzuhalten, die übrigen Anforderungen werden in der "
            "wasserrechtlichen Zulassung festgesetzt (§ 1 AbwV). Allgemein ist die Schadstofffracht durch "
            "Wiederverwendung von Druckerei-Waschwasser, Verzicht auf schwer abbaubare Schlichten, "
            "Komplexbildner und Tenside, Verzicht auf APEO und chlorierende Wollvorbehandlung sowie "
            "Minimierung und Behandlung von Restflotten und Restdruckpasten zu verringern, nachzuweisen "
            "in einem betrieblichen Abwasserkataster (Teil B). An der Einleitungsstelle gelten u. a. CSB "
            "160 mg/l, BSB5 25 mg/l, Phosphor 2 mg/l, Gesamtstickstoff 20 mg/l und Farbgrenzwerte (Teil "
            "C); vor Vermischung AOX 0,5 mg/l, Chrom, Kupfer und Nickel je 0,5 mg/l, Zink und Zinn je 2 "
            "mg/l (Teil D). Am Ort des Anfalls sind u. a. chlororganische Carrier, APEO aus Wasch- und "
            "Reinigungsmitteln, Chrom-VI als Oxidationsmittel sowie EDTA, DTPA und Phosphonate als "
            "Enthärter unzulässig (Teil E). Unter 5 m³ Abwasser je Tag gelten nur Teil B und der "
            "CSB-Wert; für Anlagen, die vor dem 01.06.2000 rechtmäßig in Betrieb waren, gelten "
            "Erleichterungen (Teil F). Für Indirekteinleiter in die öffentliche Kanalisation werden die "
            "Anforderungen der Teile D und E über die Genehmigung nach § 58 WHG festgesetzt. Branche: "
            "Spinnereien, Webereien, Strickereien, Färbereien, Druckereien und Ausrüster."
        ),
        "key_article": "Anhang 38 Teile A–F (i. V. m. § 1 AbwV)",
    },
    {
        "nr": 29,
        "key": "EPR_FR",
        "relevant_fields": ["sales_markets", "value_chain_roles", "product_categories", "b2c"],
        "name": "REP TLC – Herstellerverantwortung für Textilien in Frankreich",
        "full_name": "Responsabilité élargie du producteur (REP) für Textilien, Schuhe und Haushaltswäsche (TLC), Code de l'environnement Art. L541-10 ff., insbesondere L541-10-1 Nr. 11°, L541-10-9-1 und L541-10-27, zuletzt geändert durch Loi n° 2026-602 du 8 juillet 2026",
        "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049464324",
        "text_url": "https://www.senat.fr/leg/tas25-150.pdf",
        "scope": "FR",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049464324 (L541-10-1, Fassung seit 24.04.2024, per Stealth-Browser); https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049464284 (L541-10, Fassung seit 24.04.2024)).
        "criteria": (
            "Der REP TLC unterliegen neue Bekleidungstextilien, Schuhe und Haushaltswäsche für "
            "Privatpersonen sowie seit 01.01.2020 neue Heimtextilien, soweit sie keine Möbelbestandteile "
            "oder Möbelbezüge sind (Art. L541-10-1 Nr. 11°). Produzent ist jede natürliche oder "
            "juristische Person, die solche Produkte entwickelt, herstellt, handhabt, behandelt, verkauft "
            "oder einführt (Art. L541-10 I); sie erfüllt ihre Pflicht durch Beitritt und Beitragszahlung "
            "an eine zugelassene Branchenorganisation (éco-organisme, derzeit Refashion) oder über ein "
            "zugelassenes individuelles System. Die Pflicht besteht für das Inverkehrbringen auf dem "
            "französischen Markt seit 01.01.2007 und ist unabhängig von Unternehmensgröße oder Umsatz. "
            "Seit 10.07.2026 muss eine nicht in Frankreich niedergelassene Person, die der REP "
            "unterliegt, schriftlich einen in Frankreich niedergelassenen Bevollmächtigten (mandataire) "
            "benennen, der in alle REP-Pflichten eintritt; die Pflicht gilt als erfüllt, wenn ein in "
            "Frankreich niedergelassener Marktplatzbetreiber nach L541-10-9 die Pflichten für die "
            "Produkte übernimmt (Art. L541-10-9-1). Seit 01.09.2026 werden die Beiträge für TLC "
            "zusätzlich nach Sortimentsbreite, Angebotsfrequenz und Reparaturanreiz moduliert; als "
            "Maluszuschlag beträgt dies je Produkt 0,25 bis 12 EUR in 2026 und steigt bis auf 2 bis 20 "
            "EUR ab 2030, auf begründeten Antrag begrenzt auf 50 % des Nettoverkaufspreises (Art. "
            "L541-10-27 II). Branche: Bekleidungs-, Schuh- und Heimtextilhersteller, Marken, Importeure, "
            "Händler und Onlinehändler mit Verkauf an Endkunden in Frankreich. Einordnung des Profils: "
            "Entscheidend ist der Absatzmarkt Frankreich. Ist \"Frankreich\" angegeben und fuehrt das "
            "Profil Bekleidung, Schuhe oder Heim- und Haustextilien fuer Privatpersonen (B2C), gilt die "
            "Pflicht fuer Hersteller, Markeninhaber, Importeure und Haendler (ja). Ist nur \"andere "
            "EU-/EWR-Staaten\" angegeben, kann Frankreich darunter sein (moeglich); ohne B2C-Geschaeft "
            "ebenfalls moeglich. Sind weder \"Frankreich\" noch \"andere EU-/EWR-Staaten\" angegeben "
            "(etwa nur Deutschland oder die Niederlande): nein."
        ),
        "key_article": "Art. L541-10-1 Nr. 11°, L541-10 I, L541-10-9-1, L541-10-27 Code de l'environnement",
    },
    {
        "nr": 30,
        "key": "EPR_NL",
        "relevant_fields": ["sales_markets", "value_chain_roles", "product_categories", "b2c"],
        "name": "UPV Textiel – Herstellerverantwortung für Textilien in den Niederlanden",
        "full_name": "Besluit uitgebreide producentenverantwoordelijkheid textiel vom 14.04.2023 (BWBR0048093), Stb. 2023, 132",
        "url": "https://wetten.overheid.nl/BWBR0048093/",
        "text_url": "https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0048093/2023-07-01_0/xml/BWBR0048093_2023-07-01_0.xml",
        "scope": "NL",
        # Katalogerweiterung 29.09.2026, am Primaertext geprueft (https://wetten.overheid.nl/BWBR0048093/2023-07-01 (Art. 1–9, 'Geraadpleegd op 29-09-2026', 'Geldend van 01-07-2023 t/m heden'); https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0048093/2023-07-01_0/xml/BWBR0048093_2023-07-01_0.xml (Stb. 2023, 132, 21-04-2023)).
        "criteria": (
            "Produzent ist, wer beruflich, unabhängig von der Verkaufstechnik, Textilprodukte in den "
            "Niederlanden erstmals auf dem Markt anbietet (Art. 1 Abs. 1); erfasst sind neu hergestellte "
            "Textilprodukte der Kategorien Kleidung (Verbraucher- und Berufskleidung, KN-Kapitel 61 und "
            "62) und Haushaltstextilien (Tisch-, Bett- und Haushaltswäsche, KN-Position 6302) im Sinne "
            "der Textilkennzeichnungsverordnung (Art. 1 Abs. 2). Ein nicht in den Niederlanden "
            "niedergelassener Produzent muss einen dort niedergelassenen Bevollmächtigten (gemachtigd "
            "vertegenwoordiger) benennen (Art. 2). Der Produzent muss dafür sorgen, dass vom Gewicht der "
            "im Vorjahr in Verkehr gebrachten Textilien 2025 mindestens 50 % zur Wiederverwendung "
            "vorbereitet oder recycelt werden, jährlich steigend bis 75 % ab 2030 (Art. 3); davon zur "
            "Wiederverwendung mindestens 20 % 2025 bis 25 % ab 2030, in den Niederlanden selbst 10 % bis "
            "15 % (Art. 4), und vom Recycling Faser-zu-Faser mindestens 25 % 2025 bis 33 % ab 2030 (Art. "
            "5). Er muss möglichst viel recycelte Fasern aus Alttextilien einsetzen (Art. 6) und jährlich "
            "vor dem 1. August über das Vorjahr berichten (Art. 7 i. V. m. Art. 5 Besluit regeling voor "
            "uitgebreide producentenverantwoordelijkheid). Die Pflichten können über eine "
            "Produzentenorganisation erfüllt werden; keine Größen- oder Mengenschwelle. Branche: "
            "Bekleidungs- und Heimtextilhersteller, Marken, Importeure und ausländische Versender mit "
            "Absatz in den Niederlanden. Einordnung des Profils: Entscheidend ist der Absatzmarkt "
            "Niederlande. Ist \"Niederlande\" angegeben und fuehrt das Profil Bekleidung (auch "
            "Berufskleidung) oder Heim- und Haustextilien, gilt die Pflicht fuer den, der die Produkte "
            "dort erstmals anbietet: Hersteller, Markeninhaber, Importeur oder Versandhaendler (ja). Ist "
            "nur \"andere EU-/EWR-Staaten\" angegeben, koennen die Niederlande darunter sein (moeglich); "
            "Schuhe allein sind derzeit nicht erfasst. Sind weder \"Niederlande\" noch \"andere "
            "EU-/EWR-Staaten\" angegeben (etwa nur Deutschland oder Frankreich): nein."
        ),
        "key_article": "Art. 1, 2, 3–5, 7",
    },
]


# ---------------------------------------------------------------------------
# Guidelines je Regulierung.
#
# Quelle: offizielle Kommissions-/Behörden-Leitlinien (EU Commission, BAFA,
# EFRAG, ESMA ...). Werden beim Analyse-Lauf zusätzlich zum Gesetzestext
# gefetched und als Kontext an das LLM übergeben. Auf der Seite
# "Regulierungsliste" werden sie mit Link + Stand angezeigt.
#
# Schema: {reg_key: [{"name": str, "url": str}, ...]}
# Nicht aufgeführte reg_keys haben aktuell keine kuratierten Guidelines.
# ---------------------------------------------------------------------------
GUIDELINES_BY_REG_KEY: dict[str, list[dict]] = {
    "CSDDD": [
        {"name": "EU-Kommission – Corporate Sustainability Due Diligence",
         "url": "https://commission.europa.eu/business-economy-euro/doing-business-eu/sustainability-due-diligence-responsible-business/corporate-sustainability-due-diligence_en"},
    ],
    "LkSG": [
        {"name": "BAFA – Handreichungen zum LkSG",
         "url": "https://www.bafa.de/DE/Lieferketten/Handreichungen/handreichungen_node.html"},
        {"name": "BMAS/CSR in Deutschland – LkSG FAQ",
         "url": "https://www.csr-in-deutschland.de/DE/Gesetze/Lieferkettensorgfaltspflichtengesetz/FAQ/faq-art.html"},
    ],
    "EUDR": [
        {"name": "EU-Kommission – Entwaldungsfreie Lieferketten (EUDR)",
         "url": "https://environment.ec.europa.eu/topics/forests/deforestation/regulation-deforestation-free-products_en"},
    ],
    "FLR": [
        {"name": "EU-Kommission – Forced Labour Regulation",
         "url": "https://single-market-economy.ec.europa.eu/single-market/goods/forced-labour-regulation_en"},
    ],
    "CSRD": [
        {"name": "EU-Kommission – CSRD Implementierung & Q&A",
         "url": "https://finance.ec.europa.eu/regulation-and-supervision/financial-services-legislation/implementing-and-delegated-acts/corporate-sustainability-reporting-directive_en"},
    ],
    "CSRD_DE": [
        {"name": "DRSC – Stand des CSRD-Umsetzungsgesetzes (Anhörung und Änderungsantrag)",
         "url": "https://www.drsc.de/news/csrd-umsetzungsgesetz-oeffentliche-anhoerung-aenderungsantrag/"},
        {"name": "IDW – Themenübersicht Nachhaltigkeitsberichterstattung (CSRD/ESRS)",
         "url": "https://www.idw.de/idw/themen-branchen/nachhaltigkeit/"},
    ],
    "NFRD": [
        {"name": "EU-Kommission – Non-Financial Reporting (Historie)",
         "url": "https://finance.ec.europa.eu/capital-markets-union-and-financial-markets/company-reporting-and-auditing/company-reporting/corporate-sustainability-reporting_en"},
    ],
    "CSR-RUG": [
        {"name": "DRSC – DRS 20: nichtfinanzielle Erklärung (CSR-RUG)",
         "url": "https://www.drsc.de/projekte/aenderung-drs-20-an-csr-rlug/"},
    ],
    "TaxonomieVO": [
        {"name": "EU-Kommission – EU-Taxonomie",
         "url": "https://finance.ec.europa.eu/sustainable-finance/tools-and-standards/eu-taxonomy-sustainable-activities_en"},
    ],
    "HinSchG": [
        {"name": "Bundesamt für Justiz – Externe Meldestelle (HinSchG)",
         "url": "https://www.bundesjustizamt.de/DE/MeldestelledesBundes/MeldestelledesBundes_node.html"},
    ],
    "RightToRepair": [
        {"name": "EU-Kommission – Richtlinie zur Reparatur von Waren (Right to Repair)",
         "url": "https://commission.europa.eu/law/law-topic/consumer-protection-law/directive-repair-goods_en"},
    ],
    "Oekodesign": [
        {"name": "EU-Kommission – Ecodesign for Sustainable Products Regulation (ESPR)",
         "url": "https://environment.ec.europa.eu/strategy/circular-economy/ecodesign-sustainable-products-regulation_en"},
    ],
    "Vernichtungsverbot": [
        {"name": "EU-Kommission – Verbot der Vernichtung unverkaufter Kleidung und Schuhe",
         "url": "https://environment.ec.europa.eu/news/ban-destruction-unsold-clothes-and-shoes-enters-application-2026-07-17_en"},
        {"name": "Umweltbundesamt – Vernichtungsverbot und Transparenzpflicht für unverkaufte Waren",
         "url": "https://www.umweltbundesamt.de/themen/wirtschaft-konsum/produkte/oekodesign/oekodesign-verordnung/vernichtungsverbot-transparenzpflicht-fuer"},
    ],
    "PPWR": [
        {"name": "EU-Kommission – Verpackungen und Verpackungsabfälle",
         "url": "https://environment.ec.europa.eu/topics/waste-and-recycling/packaging-waste_en"},
    ],
    "MinRohSorgG": [
        {"name": "DEKSOR (BGR) – Deutsche Kontrollstelle EU-Sorgfaltspflichten in Rohstofflieferketten",
         "url": "https://www.bgr.bund.de/DE/BGR/Deksor/deksor_node.html"},
    ],
    "EmpCo": [
        {"name": "EU-Kommission – Nachhaltiger Konsum / Stärkung der Verbraucher für den grünen Wandel",
         "url": "https://commission.europa.eu/topics/consumers/consumer-rights-and-complaints/sustainable-consumption_en"},
    ],
    # --- Katalogerweiterung 29.09.2026 ---
    "REACH_XVII": [
        {"name": "EU-Kommission – REACH-Beschränkungen (Restrictions)",
         "url": "https://single-market-economy.ec.europa.eu/sectors/chemicals/reach/restrictions_en"},
        {"name": "ECHA – Liste der unter REACH beschränkten Stoffe (Anhang XVII)",
         "url": "https://echa.europa.eu/substances-restricted-under-reach"},
    ],
    "REACH_ART33": [
        {"name": "Umweltbundesamt – REACH (Chemikalienverordnung)",
         "url": "https://www.umweltbundesamt.de/themen/chemikalien/reach-chemikalien-reach"},
        {"name": "ECHA – Kandidatenliste der besonders besorgniserregenden Stoffe",
         "url": "https://echa.europa.eu/candidate-list-table"},
    ],
    "SCIP": [
        {"name": "BLAC – FAQ zur SCIP-Meldepflicht nach § 16f ChemG (Stand 08.02.2024)",
         "url": "https://www.blac.de/documents/faq-zu-scip-oeffentlich-stand-08022024_1710239041.pdf"},
        {"name": "ECHA – SCIP-Datenbank",
         "url": "https://echa.europa.eu/de/scip"},
    ],
    "POP": [
        {"name": "EU-Kommission – Abfälle mit persistenten organischen Schadstoffen (POP)",
         "url": "https://environment.ec.europa.eu/topics/waste-and-recycling/waste-containing-pops_en"},
        {"name": "Umweltbundesamt – Stockholmer Übereinkommen zu POP",
         "url": "https://www.umweltbundesamt.de/themen/chemikalien/internationales-chemikalienmanagement/uebereinkommen-von-stockholm-zu-pop"},
        {"name": "ECHA – Understanding POPs",
         "url": "https://echa.europa.eu/understanding-pops"},
    ],
    "BPR": [
        {"name": "EU-Kommission – Biozidprodukte",
         "url": "https://health.ec.europa.eu/biocidal-products_en"},
        {"name": "ECHA – Behandelte Waren (treated articles)",
         "url": "https://echa.europa.eu/regulations/biocidal-products-regulation/treated-articles"},
    ],
    "TKVO": [
        {"name": "EU-Kommission – Verordnung (EU) Nr. 1007/2011 (Textilkennzeichnung)",
         "url": "https://single-market-economy.ec.europa.eu/sectors/textiles-ecosystem/regulation-eu-10072011_en"},
        {"name": "EU-Kommission – Überarbeitung der Verordnung (EU) Nr. 1007/2011",
         "url": "https://single-market-economy.ec.europa.eu/sectors/textiles-ecosystem/review-regulation-eu-10072011_en"},
    ],
    "GPSR": [
        {"name": "EU-Kommission – Produktsicherheit",
         "url": "https://commission.europa.eu/topics/business-and-industry/product-safety_en"},
        {"name": "EU-Kommission – GPSR-Fragen und Antworten für Unternehmen (PDF)",
         "url": "https://webgate.ec.europa.eu/safety/consumers/consumers_safety_gate/obligationsForBusinesses/documents/Q&A.pdf"},
    ],
    "PSA": [
        {"name": "EU-Kommission – Persönliche Schutzausrüstung (PSA)",
         "url": "https://single-market-economy.ec.europa.eu/sectors/mechanical-engineering/personal-protective-equipment-ppe_en"},
        {"name": "BAuA – Bereitstellung persönlicher Schutzausrüstungen auf dem Markt",
         "url": "https://www.baua.de/DE/Themen/Arbeitsgestaltung/Sichere-Produkte/Persoenliche-Schutzausruestungen/Bereitstellung-Markt"},
    ],
    "MDR": [
        {"name": "EU-Kommission – Neue Verordnungen zu Medizinprodukten",
         "url": "https://health.ec.europa.eu/medical-devices-new-regulations_en"},
        {"name": "BfArM – Medizinprodukte",
         "url": "https://www.bfarm.de/DE/Medizinprodukte/_node.html"},
    ],
    "Schuhkennzeichnung": [
        {"name": "EU-Kommission – Schuhindustrie (Footwear industry)",
         "url": "https://single-market-economy.ec.europa.eu/sectors/textiles-ecosystem/footwear-industry_en"},
    ],
    "EnEfG": [
        {"name": "BAFA – Energieaudit nach EDL-G, Energie- und Umweltmanagementsysteme nach EnEfG",
         "url": "https://www.bafa.de/DE/Energie/Energieberatung/Energieaudit/energieaudit_node.html"},
        {"name": "BAFA – Merkblatt zum Energieeffizienzgesetz (PDF)",
         "url": "https://www.bafa.de/SharedDocs/Downloads/DE/Energie/ea_merkblatt_energieefffizienzgesetz.pdf?__blob=publicationFile&v=6"},
    ],
    "AbwV38": [
        {"name": "Bayerisches Landesamt für Umwelt – Merkblatt 4.5/2-38: Hinweise zu Anhang 38 AbwV",
         "url": "https://www.lfu.bayern.de/wasser/merkblattsammlung/teil4_oberirdische_gewaesser/doc/nr_452_38.pdf"},
        {"name": "Umweltbundesamt – Textilindustrie",
         "url": "https://www.umweltbundesamt.de/themen/wirtschaft-konsum/industriebranchen/textilindustrie"},
        {"name": "Umweltbundesamt – Anforderungen an das Einleiten von Abwasser (Abwasserverordnung)",
         "url": "https://www.umweltbundesamt.de/themen/wasser/abwasser/anforderungen-an-das-einleiten-von-abwasser"},
    ],
    "EPR_FR": [
        {"name": "Ministère de la Transition écologique – Produits textiles (TLC)",
         "url": "https://www.ecologie.gouv.fr/politiques-publiques/produits-textiles-tlc"},
        {"name": "Refashion – Informationen für Inverkehrbringer",
         "url": "https://pro.refashion.fr/"},
    ],
    "EPR_NL": [
        {"name": "Inspectie Leefomgeving en Transport – UPV textiel",
         "url": "https://www.ilent.nl/onderwerpen/producentenverantwoordelijkheid/upv-textiel"},
        {"name": "Rijkswaterstaat (Afval Circulair) – UPV textiel",
         "url": "https://afvalcirculair.nl/uitgebreide-producentenverantwoordelijkheid-upv/overzicht-upv/upv-textiel/"},
    ],
}


def guidelines_for(reg_key: str) -> list[dict]:
    """Liefert die kuratierten Guidelines für eine Regulierung (oder leere Liste)."""
    return GUIDELINES_BY_REG_KEY.get(reg_key, [])


# ---------------------------------------------------------------------------
# Erste Schritte je Regulierung — statisch, kuratiert, kein LLM.
#
# Zwei bis vier Stichpunkte, die beschreiben, womit ein erfasstes Unternehmen
# anfaengt. Hergeleitet aus dem Gesetzestext (Fundstelle steht jeweils im
# uebersetzten Text) und den kuratierten Guidelines; NICHT aus einer
# LLM-Antwort. Hier stehen nur die Schluessel — die Texte liegen in sechs
# Sprachen in `i18n.FIRST_STEPS`, wie bei allen anderen Inhalten der App.
#
# Der weiterfuehrende Link kommt aus GUIDELINES_BY_REG_KEY oben, damit es
# keine zweite, unabhaengig veraltende Linkliste gibt (`first_steps_link`).
#
# Diese Struktur wird zur Renderzeit gelesen und geht in keinen Cache ein.
# ---------------------------------------------------------------------------
FIRST_STEPS_BY_REG_KEY: dict[str, list[str]] = {
    "CSDDD": ["csddd_1", "csddd_2", "csddd_3", "csddd_4"],
    "LkSG": ["lksg_1", "lksg_2", "lksg_3", "lksg_4"],
    "EUDR": ["eudr_1", "eudr_2", "eudr_3", "eudr_4"],
    "FLR": ["flr_1", "flr_2", "flr_3"],
    "CSRD": ["csrd_1", "csrd_2", "csrd_3", "csrd_4"],
    "CSRD_DE": ["csrd_de_1", "csrd_de_2", "csrd_de_3"],
    "NFRD": ["nfrd_1", "nfrd_2"],
    "CSR-RUG": ["csr_rug_1", "csr_rug_2", "csr_rug_3"],
    "TaxonomieVO": ["taxonomie_1", "taxonomie_2", "taxonomie_3"],
    "HinSchG": ["hinschg_1", "hinschg_2", "hinschg_3", "hinschg_4"],
    "RightToRepair": ["r2r_1", "r2r_2", "r2r_3"],
    "Oekodesign": ["oekodesign_1", "oekodesign_2", "oekodesign_3"],
    "Vernichtungsverbot": ["vernichtung_1", "vernichtung_2", "vernichtung_3", "vernichtung_4"],
    "PPWR": ["ppwr_1", "ppwr_2", "ppwr_3"],
    "MinRohSorgG": ["minroh_1", "minroh_2", "minroh_3"],
    "EmpCo": ["empco_1", "empco_2", "empco_3", "empco_4"],
    # --- Katalogerweiterung 29.09.2026 ---
    "REACH_XVII": ["reach17_1", "reach17_2", "reach17_3", "reach17_4"],
    "REACH_ART33": ["reach33_1", "reach33_2", "reach33_3", "reach33_4"],
    "SCIP": ["scip_1", "scip_2", "scip_3", "scip_4"],
    "POP": ["pop_1", "pop_2", "pop_3"],
    "BPR": ["bpr_1", "bpr_2", "bpr_3"],
    "TKVO": ["tkvo_1", "tkvo_2", "tkvo_3", "tkvo_4"],
    "GPSR": ["gpsr_1", "gpsr_2", "gpsr_3", "gpsr_4"],
    "PSA": ["psa_1", "psa_2", "psa_3", "psa_4"],
    "MDR": ["mdr_1", "mdr_2", "mdr_3", "mdr_4"],
    "Schuhkennzeichnung": ["schuh_1", "schuh_2", "schuh_3"],
    "EnEfG": ["enefg_1", "enefg_2", "enefg_3", "enefg_4"],
    "AbwV38": ["abwv38_1", "abwv38_2", "abwv38_3", "abwv38_4"],
    "EPR_FR": ["eprfr_1", "eprfr_2", "eprfr_3", "eprfr_4"],
    "EPR_NL": ["eprnl_1", "eprnl_2", "eprnl_3", "eprnl_4"],
}


def first_steps_for(reg_key: str) -> list[str]:
    """Schluessel der ersten Schritte (Texte kommen aus `i18n.FIRST_STEPS`)."""
    return FIRST_STEPS_BY_REG_KEY.get(reg_key, [])


def first_steps_link(reg_key: str) -> dict | None:
    """Weiterfuehrende Leitlinie zu den ersten Schritten (oder None)."""
    guides = guidelines_for(reg_key)
    return guides[0] if guides else None


# ---------------------------------------------------------------------------
# Veroeffentlichungsdatum je Regulierung (statisch gepflegt).
#
# Fuer EU-Verordnungen/Richtlinien das Datum der Veroeffentlichung im
# Amtsblatt (OJ). Fuer deutsche Gesetze das Datum der Bundesgesetzblatt-
# Veroeffentlichung. Format: DD.MM.YYYY.
# ---------------------------------------------------------------------------
PUBLISHED_BY_REG_KEY: dict[str, str] = {
    "CSDDD":           "05.07.2024",
    "LkSG":            "16.07.2021",
    "EUDR":            "09.06.2023",
    "FLR":             "12.12.2024",
    "CSRD":            "16.12.2022",
    # Kein Veroeffentlichungsdatum — das Gesetz ist nicht verkuendet.
    # Der Entwurfshinweis kommt uebersetzt aus i18n (siehe DRAFT_PUBLISHED).
    "CSRD_DE":         "",
    "NFRD":            "15.11.2014",
    "CSR-RUG":         "11.04.2017",
    "TaxonomieVO":     "22.06.2020",
    "HinSchG":         "02.06.2023",
    "RightToRepair":   "10.07.2024",
    "Oekodesign":      "28.06.2024",
    # ABl. L, 2026/296 vom 22.04.2026 (Kopfzeile des Volltextes).
    "Vernichtungsverbot": "22.04.2026",
    "PPWR":            "22.01.2025",
    "MinRohSorgG":     "18.12.2020",
    "EmpCo":           "06.03.2024",
    # Datum des Kommissionsvorschlags COM(2023) 166 final.
    # --- Katalogerweiterung 29.09.2026 ---
    # ABl. L 396 vom 30.12.2006, S. 1 (Berichtigung ABl. L 136 vom 29.5.2007, S. 3); Eintrag 72: VO (EU) 2018/1513, 
    "REACH_XVII": "30.12.2006",
    # ABl. L 396 vom 30.12.2006, S. 1
    "REACH_ART33": "30.12.2006",
    # Gesetz zur Umsetzung der Abfallrahmenrichtlinie der Europäischen Union vom 23.10.2020, Art. 4, BGBl. I S. 2232
    "SCIP": "28.10.2020",
    # ABl. L 169 vom 25.6.2019, S. 45
    "POP": "25.06.2019",
    # ABl. L 167 vom 27.6.2012, S. 1
    "BPR": "27.06.2012",
    # ABl. L 272 vom 18.10.2011, S. 1
    "TKVO": "18.10.2011",
    # ABl. L 135 vom 23.5.2023, S. 1
    "GPSR": "23.05.2023",
    # ABl. L 81 vom 31.3.2016, S. 51
    "PSA": "31.03.2016",
    # ABl. L 117 vom 5.5.2017, S. 1
    "MDR": "05.05.2017",
    # ABl. L 100 vom 19.4.1994, S. 37 (RL 94/11/EG); deutsche Umsetzung: BedGgstV i. d. F. der Bek. vom 23.12.1997, 
    "Schuhkennzeichnung": "19.04.1994",
    # BGBl. 2023 I Nr. 309 vom 17.11.2023 (recht.bund.de)
    "EnEfG": "17.11.2023",
    # Dritte Verordnung zur Änderung der Abwasserverordnung vom 29.05.2000, BGBl. I Nr. 24 vom 31.05.2000, S. 751 (E
    "AbwV38": "31.05.2000",
    # Loi n° 2020-105 du 10 février 2020 (AGEC), JORF vom 11.02.2020 – Neufassung der Art. L541-10 ff.; Änderungen d
    "EPR_FR": "11.02.2020",
    # Staatsblad 2023, 132, uitgegeven 21.04.2023 (Besluit vom 14.04.2023)
    "EPR_NL": "21.04.2023",
}

# Regulierungen, deren Datum oben nur ein Entwurfsstand ist (keine Verkuendung).
# Die Liste ersetzt die frueheren deutschen Freitexte "Entwurf 2025" /
# "Entwurf 22.03.2023", die auch in EN/FR/ES/IT/ZH auf Deutsch erschienen.
DRAFT_PUBLISHED: frozenset[str] = frozenset({"CSRD_DE"})


def published_for(reg_key: str) -> str:
    """Veroeffentlichungsdatum (oder leerer Platzhalter)."""
    return PUBLISHED_BY_REG_KEY.get(reg_key) or "—"


def published_is_draft(reg_key: str) -> bool:
    """True, wenn das Datum nur einen Entwurfsstand bezeichnet."""
    return reg_key in DRAFT_PUBLISHED


# ---------------------------------------------------------------------------
# Anwendungsbeginn und Status je Regulierung.
#
# Das Veroeffentlichungsdatum sagt nichts darueber, ab wann ein Unternehmen die
# Pflichten tatsaechlich erfuellen muss — dafuer steht hier `applies_from`.
# Jeder Wert wurde am 01.09.2026 am konsolidierten Volltext der Primaerquelle
# geprueft; die Fundstelle steht als Kommentar dahinter.
#
# `status` wird normalerweise NICHT gepflegt, sondern aus `applies_from` gegen
# das heutige Datum abgeleitet (`in_kraft` / `gilt_ab`) — sonst veraltet die
# Angabe stillschweigend. Nur `entwurf` und `rueckzug_angekuendigt` lassen sich
# nicht aus einem Datum ableiten und stehen deshalb explizit da.
#
# `note` verweist auf einen Schluessel in i18n.APPLIES_NOTES (6 Sprachen).
# ---------------------------------------------------------------------------
STATUS_IN_KRAFT = "in_kraft"
STATUS_GILT_AB = "gilt_ab"
STATUS_ENTWURF = "entwurf"
STATUS_RUECKZUG = "rueckzug_angekuendigt"

APPLICATION_BY_REG_KEY: dict[str, dict] = {
    # Art. 37 Abs. 1 (kons. Fassung 02024L1760, Stand 18.03.2026, geaendert
    # durch RL (EU) 2026/470): Umsetzung bis 26.07.2028, Anwendung ab 26.07.2029.
    "CSDDD":           {"applies_from": "26.07.2029", "note": "csddd"},
    # Art. 5 Abs. 1 LkSG-Artikelgesetz; § 1 Abs. 1 S. 3: ab 01.01.2024 gilt 1 000.
    "LkSG":            {"applies_from": "01.01.2023", "note": "lksg"},
    # Art. 38 Abs. 2/3 (kons. 02023R1115, Stand 26.12.2025).
    "EUDR":            {"applies_from": "30.12.2026", "note": "eudr"},
    # Art. 39 VO (EU) 2024/3015.
    "FLR":             {"applies_from": "14.12.2027", "note": "flr"},
    # Neue Schwellen fuer Geschaeftsjahre ab 01.01.2027 (Erwaegungsgrund zu
    # Art. 5 Abs. 2 RL (EU) 2022/2464 i.d.F. der RL (EU) 2026/470);
    # nationale Umsetzung bis 19.03.2027 (Art. 5 Abs. 1 RL (EU) 2026/470).
    "CSRD":            {"applies_from": "01.01.2027", "note": "csrd"},
    # Gesetzgebungsverfahren nicht abgeschlossen (Stand 09/2026).
    "CSRD_DE":         {"applies_from": "", "status": STATUS_ENTWURF, "note": "entwurf_de"},
    # Art. 4 Abs. 1 UAbs. 2 RL 2014/95/EU: ab dem am 01.01.2017 beginnenden GJ.
    "NFRD":            {"applies_from": "01.01.2017", "note": "nfrd"},
    # §§ 289b ff. HGB: erstmals fuer nach dem 31.12.2016 beginnende Geschaeftsjahre.
    "CSR-RUG":         {"applies_from": "01.01.2017", "note": "csr_rug"},
    # Art. 27 Abs. 2 VO (EU) 2020/852.
    "TaxonomieVO":     {"applies_from": "01.01.2022", "note": "taxonomie"},
    # Art. 20 Abs. 2 VO (EU) 2019/2088.
    # Art. 53 VO (EU) 2024/3005.
    # Art. 26 Abs. 1 RL (EU) 2019/1937 (Abs. 2: 50-249 Beschaeftigte ab 17.12.2023).
    # Art. 10 Abs. 2 HinSchG-Artikelgesetz.
    "HinSchG":         {"applies_from": "02.07.2023"},
    # Art. 22 Abs. 1 UAbs. 3 RL (EU) 2024/1799.
    "RightToRepair":   {"applies_from": "31.07.2026"},
    # Art. 80 VO (EU) 2024/1781 (20. Tag nach ABl. vom 28.06.2024).
    "Oekodesign":      {"applies_from": "18.07.2024", "note": "oekodesign"},
    # Art. 6 Del. VO (EU) 2026/296: "Sie gilt ab dem 19. Juli 2026." Dasselbe
    # Datum nennt Art. 25 Abs. 1 VO (EU) 2024/1781 fuer das Verbot selbst;
    # mittlere Unternehmen folgen am 19.07.2030 (Staffelung siehe deadlines.py).
    "Vernichtungsverbot": {"applies_from": "19.07.2026", "note": "vernichtungsverbot"},
    # Art. 71 VO (EU) 2025/40.
    "PPWR":            {"applies_from": "12.08.2026"},
    # Art. 3 MinRohSorgG-Artikelgesetz (Fussnote gesetze-im-internet.de).
    "MinRohSorgG":     {"applies_from": "07.05.2020"},
    # Art. 4 Abs. 1 UAbs. 2 RL (EU) 2024/825.
    "EmpCo":           {"applies_from": "27.09.2026", "note": "empco"},
    # Kommission hat die Ruecknahme am 20.06.2025 angekuendigt, aber nicht vollzogen.
    # --- Katalogerweiterung 29.09.2026 ---
    # Art. 141 Abs. 4 VO (EG) Nr. 1907/2006: „Titel VIII und Anhang XVII gelten ab dem 1. Juni 2009.“
    "REACH_XVII": {"applies_from": "01.06.2009", "note": "reach17"},
    # Art. 141 Abs. 1 VO (EG) Nr. 1907/2006 (Inkrafttreten 01.06.2007); Titel IV (Art. 31–36) ist in den abweichende
    "REACH_ART33": {"applies_from": "01.06.2007"},
    # Art. 9 Abs. 1 Buchst. i RL 2008/98/EG i. d. F. RL (EU) 2018/851 („ab dem 5. Januar 2021“, zitiert in BLAC-FAQ 
    "SCIP": {"applies_from": "05.01.2021"},
    # Art. 22 VO (EU) 2019/1021: Inkrafttreten am zwanzigsten Tag nach der Veröffentlichung (ABl. vom 25.06.2019); k
    "POP": {"applies_from": "15.07.2019"},
    # Art. 97 VO (EU) Nr. 528/2012: „Sie gilt ab dem 1. September 2013.“
    "BPR": {"applies_from": "01.09.2013"},
    # Art. 28 Unterabs. 2 VO (EU) Nr. 1007/2011: „Sie gilt ab dem 8. Mai 2012.“
    "TKVO": {"applies_from": "08.05.2012", "note": "tkvo"},
    # Art. 52 Unterabs. 2 VO (EU) 2023/988: „Sie gilt ab dem 13. Dezember 2024.“
    "GPSR": {"applies_from": "13.12.2024"},
    # Art. 48 Abs. 2 VO (EU) 2016/425: „Diese Verordnung gilt ab dem 21. April 2018“ (Art. 20–36 und 44 ab 21.10.201
    "PSA": {"applies_from": "21.04.2018"},
    # Art. 123 Abs. 2 VO (EU) 2017/745 i. d. F. der VO (EU) 2020/561: „Sie gilt ab dem 26. Mai 2021.“
    "MDR": {"applies_from": "26.05.2021", "note": "mdr"},
    # Art. 6 Abs. 2 RL 94/11/EG: Anwendung der nationalen Vorschriften „ab 23. März 1996“ (für vor dem 23.09.1997 an
    "Schuhkennzeichnung": {"applies_from": "23.03.1996"},
    # Fußnote gesetze-im-internet.de: „Das G wurde als Artikel 1 des G v. 13.11.2023 I Nr. 309 vom Bundestag beschlo
    "EnEfG": {"applies_from": "18.11.2023", "note": "enefg"},
    # LfU Bayern, Merkblatt Nr. 4.5/2-38 (Stand 01.11.2011), Abschnitt 1: „Erlass: 29.05.2000 (3. Verordnung zur Änd
    "AbwV38": {"applies_from": "01.06.2000"},
    # Art. L541-10-3 Code de l'environnement (Fassung vom 19.08.2015 bis 12.02.2020): „A compter du 1er janvier 2007
    "EPR_FR": {"applies_from": "01.01.2007", "note": "eprfr"},
    # Art. 8 Besluit uitgebreide producentenverantwoordelijkheid textiel: „Dit besluit treedt in werking met ingang 
    "EPR_NL": {"applies_from": "01.07.2023", "note": "eprnl"},
}


def _parse_ddmmyyyy(value: str):
    from datetime import date
    try:
        d, m, y = value.split(".")
        return date(int(y), int(m), int(d))
    except (ValueError, AttributeError):
        return None


def application_for(reg_key: str, today=None) -> dict:
    """Liefert {applies_from, status, note} fuer eine Regulierung.

    `status` kommt aus dem Datum, wenn es nicht explizit hinterlegt ist:
    liegt `applies_from` in der Zukunft, ist der Status `gilt_ab`, sonst
    `in_kraft`. So bleibt die Angabe ohne Pflegeaufwand richtig.
    """
    from datetime import date
    entry = APPLICATION_BY_REG_KEY.get(reg_key) or {}
    applies_from = entry.get("applies_from") or ""
    status = entry.get("status")
    if not status:
        parsed = _parse_ddmmyyyy(applies_from)
        ref = today or date.today()
        status = STATUS_GILT_AB if (parsed and parsed > ref) else STATUS_IN_KRAFT
    return {
        "applies_from": applies_from,
        "status": status,
        "note": entry.get("note") or "",
    }


# ---------------------------------------------------------------------------
# Gekoppelte Regulierungen — deterministisch bestimmte, verbindliche Vorgaben.
#
# Einige Regulierungen haengen rechtlich an einer "Eltern"-Regulierung:
#   Taxonomie-VO und CSRD-Umsetzungsgesetz folgen der CSRD-Pflicht.
# Daneben laeuft hier das CSR-RUG mit: es haengt an keiner anderen Regulierung,
# seine Merkmale stehen aber genauso abschliessend im Gesetz (§ 289b Abs. 1 HGB)
# und gehoeren deshalb nicht vor ein Sprachmodell.
# Damit das LLM diese nicht isoliert und widerspruechlich bewertet (z. B.
# CSRD = nein, aber Taxonomie = ja fuer dasselbe Unternehmen), wird der ausloesende
# Schwellenwert EINMAL aus dem Profil berechnet. Quelle der Schwellen: die
# jeweiligen `criteria` oben (CSRD post-Omnibus, HinSchG § 12).
#
# Weil die Entscheidung damit feststeht, formuliert das LLM diese Faelle gar
# nicht mehr: `coupling_verdict()` liefert den Fall, `i18n.coupling_texts()`
# den lektorierten Satz dazu (6 Sprachen). Das kostet null LLM-Calls und ist
# fuer immer wortgleich. Nur eine Kopplung ohne hinterlegten Textbaustein
# faellt auf das LLM zurueck — dann greift `coupling_premise()`.
# ---------------------------------------------------------------------------

_NON_EU_PARENT_MARKERS = ("außerhalb EU", "Nicht-EU")
_SUBSIDIARY_MARKER = "Tochter"

# Branchen, die Art. 8 Taxonomie-VO unabhaengig von der CSRD-Schwelle erfasst;
# dieselbe Liste traegt § 12 Abs. 3 HinSchG (bestimmte Finanzunternehmen).
_FINANCIAL_BRANCHES = frozenset({"Finanzdienstleistungen", "Versicherungen"})


def csrd_status(profile: dict) -> tuple[str, str]:
    """CSRD-Berichtspflicht (post-Omnibus) deterministisch aus dem Profil.

    Liefert (applies, fact_key) mit applies in {ja, nein, moeglich}. `fact_key`
    benennt den erkannten Sachverhalt und waehlt in `i18n.COUPLING_FACTS` den
    ersten Satz der Begruendung aus — der Text selbst steht dort in allen sechs
    Sprachen, damit dieselbe Lage immer wortgleich beschrieben wird.
    Schwelle nach Art. 19a Abs. 1 / Art. 29a Abs. 1 der Bilanzrichtlinie
    2013/34/EU i.d.F. der Richtlinie (EU) 2026/470: >1000 Beschaeftigte im
    Jahresdurchschnitt UND >450 Mio. EUR Nettoumsatzerloese — beide Merkmale
    kumulativ. Die Bilanzsumme ist kein Kriterium mehr.

    Fuer Unternehmen aus Drittlaendern stellt Art. 40a der Bilanzrichtlinie
    nicht auf den weltweiten, sondern auf den in der UNION erzielten
    Nettoumsatz ab ("Nettoumsatzerloese von mehr als 450 000 000 EUR ... in der
    Union"). Seit 09/2026 gibt es dafuer ein eigenes Profilfeld
    (`revenue_eu_eur`); es wird hier ausgewertet. Ist es leer — Altprofile und
    Nutzer, die den EU-Umsatz nicht kennen —, faellt die Pruefung ersatzweise
    auf den weltweiten Umsatz zurueck und sagt in der Begruendung ausdruecklich,
    dass der EU-Umsatz fehlt. Ohne diesen Rueckfall verschwaende der Hinweis
    fuer jedes Bestandsprofil kommentarlos.

    Diese Werte gelten fuer Geschaeftsjahre ab dem 01.01.2027. Fuer die
    Geschaeftsjahre 2024 bis 2026 gilt daneben WEITER die Welle-1-Regel des
    Art. 5 Abs. 2 UAbs. 1 lit. a RL (EU) 2022/2464 (grosse Unternehmen von
    oeffentlichem Interesse mit >500 Beschaeftigten). Die Mitgliedstaaten
    DUERFEN diese Unternehmen fuer 2025/2026 befreien, muessen aber nicht —
    deshalb wird der Fall als "moeglich" ausgewiesen und nicht verneint.
    """
    from datetime import date
    emp = profile.get("employees") or 0
    rev = profile.get("revenue_eur") or 0
    rev_eu = profile.get("revenue_eu_eur") or 0
    listed = bool(profile.get("listed"))
    group = profile.get("group_role") or ""
    non_eu_parent = any(m in group for m in _NON_EU_PARENT_MARKERS)
    if emp > 1000 and rev > 450_000_000:
        # Art. 19a Abs. 9 / 29a Abs. 8 der Bilanzrichtlinie: ein Tochter-
        # unternehmen ist befreit, wenn es in den Konzern-Nachhaltigkeits-
        # bericht der Mutter einbezogen ist. Die Pflicht besteht also, kann
        # aber auf Konzernebene erfuellt werden — das muss die Begruendung
        # sagen, sonst faellt der Vorbehalt weg, den vorher das LLM lieferte.
        if _SUBSIDIARY_MARKER in group:
            return "ja", "csrd_ueber_schwelle_tochter"
        return "ja", "csrd_ueber_schwelle"
    if non_eu_parent:
        if rev_eu > 450_000_000:
            return "moeglich", "csrd_drittland"
        if not rev_eu and rev > 450_000_000:
            return "moeglich", "csrd_drittland_ohne_eu_umsatz"
    # Welle 1 laeuft mit dem Geschaeftsjahr 2026 aus; Berichte dazu erscheinen
    # noch im Laufe von 2027. Das Zeitfenster steht hier, damit die Aussage
    # danach von selbst verschwindet statt zu veralten.
    if listed and emp > 500 and date.today() < date(2028, 1, 1):
        return "moeglich", "csrd_welle1"
    return "nein", "csrd_unter_schwelle"


def hinschg_status(profile: dict) -> tuple[str, str]:
    """HinSchG-Pflicht: interne Meldestelle ab 50 Beschaeftigten im Inland.

    Liefert (applies, fact_key) wie `csrd_status`. § 12 Abs. 3 HinSchG nimmt
    bestimmte Finanzunternehmen (u. a. Wertpapierdienstleistungsunternehmen,
    Kapitalverwaltungsgesellschaften, Versicherer) von der Beschaeftigten-
    schwelle aus — ohne diese Ausnahme wuerde der Baustein einem kleinen
    Finanzdienstleister hart "nein" sagen, und anders als frueher gibt es kein
    LLM mehr, das den Sonderfall auffangen koennte.
    """
    emp_de = profile.get("employees_de") or 0
    if emp_de >= 50:
        return "ja", "hinschg_ab_50"
    if (profile.get("branch") or "") in _FINANCIAL_BRANCHES:
        return "moeglich", "hinschg_unter_50_finanz"
    return "nein", "hinschg_unter_50"


# Rechtsformen, auf die § 289b HGB unmittelbar anwendbar ist: Kapital-
# gesellschaften und die ihnen ueber § 264a HGB gleichgestellte GmbH & Co. KG
# (Personenhandelsgesellschaft ohne natuerliche Person als Vollhafter).
_KAPITALGESELLSCHAFTEN = frozenset({"AG / SE", "GmbH", "GmbH & Co. KG", "Limited / Ltd."})


def csr_rug_status(profile: dict) -> tuple[str, str]:
    """Nichtfinanzielle Erklaerung nach § 289b HGB (CSR-RUG), deterministisch.

    Liefert (applies, fact_key) wie `csrd_status`. § 289b Abs. 1 HGB nennt drei
    KUMULATIVE Merkmale, geprueft am Volltext (gesetze-im-internet.de, HGB):
      1. Voraussetzungen des § 267 Abs. 3 Satz 1 (grosse Kapitalgesellschaft),
      2. kapitalmarktorientiert im Sinne des § 264d,
      3. im Jahresdurchschnitt mehr als 500 Arbeitnehmer.
    Merkmal 1 muss nicht eigens geprueft werden: § 267 Abs. 3 Satz 2 bestimmt,
    dass eine Kapitalgesellschaft im Sinn des § 264d STETS als gross gilt. Ist
    Merkmal 2 erfuellt, ist Merkmal 1 es damit auch. Uebrig bleibt eine
    Zwei-Faktoren-Pruefung aus `listed` und `employees`.

    Zwei Sonderlagen, die eine reine Schwellenpruefung falsch beantworten
    wuerde und die deshalb als "moeglich" ausgewiesen werden:
    - § 340a Abs. 1a und § 341a Abs. 1a HGB verpflichten Kreditinstitute und
      Versicherungsunternehmen OHNE das Merkmal der Kapitalmarktorientierung,
      wenn sie als gross gelten und mehr als 500 Arbeitnehmer haben. Ob ein
      Unternehmen der Branche "Finanzdienstleistungen" ein Kreditinstitut in
      diesem Sinn ist, sagt das Profil nicht.
    - Rechtsformen ausserhalb von § 289b/§ 264a HGB (etwa KG/OHG, Verein,
      Genossenschaft): dort greifen eigene Vorschriften; die Angabe
      "kapitalmarktorientiert" allein traegt das Ergebnis nicht.
    """
    emp = profile.get("employees") or 0
    listed = bool(profile.get("listed"))
    group = profile.get("group_role") or ""
    legal_form = profile.get("legal_form") or ""

    if listed and emp > 500:
        # Ohne Angabe der Rechtsform (Altprofile) nicht stillschweigend eine
        # Kapitalgesellschaft unterstellen — dann lieber "moeglich".
        if legal_form not in _KAPITALGESELLSCHAFTEN:
            return "moeglich", "csr_rug_rechtsform"
        # § 289b Abs. 2 HGB befreit ein einbezogenes Tochterunternehmen, wenn
        # der Konzernlagebericht der Mutter eine nichtfinanzielle Konzern-
        # erklaerung enthaelt. Die Pflicht besteht, kann aber auf Konzernebene
        # erfuellt werden — genau wie bei der CSRD.
        if _SUBSIDIARY_MARKER in group:
            return "ja", "csr_rug_erfuellt_tochter"
        return "ja", "csr_rug_erfuellt"
    if (not listed and emp > 500
            and (profile.get("branch") or "") in _FINANCIAL_BRANCHES):
        return "moeglich", "csr_rug_finanz"
    if listed:
        return "nein", "csr_rug_unter_500"
    return "nein", "csr_rug_nicht_kapitalmarkt"


# ---------------------------------------------------------------------------
# Regelbasierte Entscheidungen fuer die Katalogerweiterung vom 29.09.2026.
#
# Diese acht Vorschriften haengen an Merkmalen, die das Profil eindeutig
# beantwortet (eine Produktkategorie, ein Material, die SVHC-Angabe, der
# Energieverbrauch, die Nassveredlung). Ein Sprachmodell braeuchte es dafuer
# nicht und koennte es nur schlechter: dieselben Bausteine wie beim CSR-RUG,
# null LLM-Aufrufe, fuer immer wortgleich.
#
# Rueckgabe wie `csrd_status`: (applies, fact_key) oder (applies, fact_key,
# conclusion_key), wenn derselbe Ausgang je nach Fall anders fortzusetzen ist
# (EnEfG: ueber 7,5 GWh Managementsystem UND Umsetzungsplaene, darunter nur
# Umsetzungsplaene).
# ---------------------------------------------------------------------------

_EU_MARKETS = frozenset({"Deutschland", "Frankreich", "Niederlande", "andere EU-/EWR-Staaten"})
_ROLE_ZULIEFERER = "Zulieferer"
_ROLE_HAENDLER = "Händler/Vertreiber (stellt Produkte anderer Unternehmen auf dem Markt bereit)"


def _only_outside_eu(profile: dict) -> bool:
    """True, wenn der Nutzer Absatzmaerkte angegeben hat und keiner in EU/EWR liegt.

    Ohne Angabe (Altprofile) wird NICHT auf "ausserhalb" geschlossen — ein
    Unternehmen mit Sitz in Deutschland setzt im Regelfall auch dort ab.
    """
    markets = set(profile.get("sales_markets") or ())
    return bool(markets) and not (markets & _EU_MARKETS)


def _only_supplier(profile: dict) -> bool:
    """True, wenn als einzige Rolle "Zulieferer" angegeben ist."""
    roles = set(profile.get("value_chain_roles") or ())
    return roles == {_ROLE_ZULIEFERER}


def reach_art33_status(profile: dict):
    """REACH Art. 33: Informationspflicht jedes Lieferanten eines Erzeugnisses."""
    svhc = profile.get("svhc_status") or ""
    if svhc == "Ja":
        return "ja", "svhc_ja"
    if svhc == "Nein":
        return "nein", "svhc_nein"
    return "moeglich", "svhc_unbekannt"


def scip_status(profile: dict):
    """SCIP-Meldung nach § 16f ChemG — dieselbe Angabe wie Art. 33.

    Sonderfall: ein reiner Haendler, der nur an Verbraucher abgibt, ist nach
    Auslegung der ECHA nicht meldepflichtig. Ob er AUSSCHLIESSLICH an
    Verbraucher liefert, sagt das Profil nicht — deshalb "moeglich".
    """
    applies, fact = reach_art33_status(profile)
    roles = set(profile.get("value_chain_roles") or ())
    if applies == "ja" and roles == {_ROLE_HAENDLER} and profile.get("b2c"):
        return "moeglich", "svhc_ja", "haendler_b2c"
    return applies, fact


def bpr_status(profile: dict):
    """Biozid-VO Art. 58: behandelte Waren (antimikrobielle Ausruestung)."""
    materials = set(profile.get("materials") or ())
    if _only_outside_eu(profile):
        return "nein", "kein_eu_markt"
    if "Antimikrobielle / biozide Ausrüstung" in materials:
        return "ja", "bpr_ausruestung"
    if "Nicht bekannt / kann nicht ausgeschlossen werden" in materials:
        return "moeglich", "bpr_unbekannt"
    return "nein", "bpr_keine"


def _category_status(profile: dict, category: str, fact_prefix: str):
    """Gemeinsamer Ablauf fuer Vorschriften, die an einer Produktkategorie haengen."""
    if category not in set(profile.get("product_categories") or ()):
        return "nein", f"{fact_prefix}_keine"
    if _only_outside_eu(profile):
        return "nein", "kein_eu_markt"
    if _only_supplier(profile):
        return "moeglich", f"{fact_prefix}_zulieferer"
    return "ja", f"{fact_prefix}_kategorie"


def psa_status(profile: dict):
    """PSA-Verordnung: Kategorie "Schutztextilien / PSA"."""
    return _category_status(profile, "Schutztextilien / PSA", "psa")


def mdr_status(profile: dict):
    """MDR: Kategorie "Medizin- und Gesundheitstextilien".

    Nicht jedes Gesundheitstextil ist ein Medizinprodukt — entscheidend ist die
    vom Hersteller bestimmte medizinische Zweckbestimmung (Art. 2 Nr. 1 MDR).
    Die Kategorie allein traegt deshalb hoechstens "moeglich".
    """
    applies, fact = _category_status(profile, "Medizin- und Gesundheitstextilien", "mdr")
    if applies == "ja":
        return "moeglich", fact
    return applies, fact


def schuh_status(profile: dict):
    """Schuhkennzeichnung (RL 94/11/EG, § 10a BedGgstV): Kategorie "Schuhe"."""
    return _category_status(profile, "Schuhe", "schuh")


# § 8 Abs. 1 und § 9 Abs. 1 EnEfG (BGBl. 2023 I Nr. 309): mehr als 7,5 GWh
# bzw. mehr als 2,5 GWh durchschnittlicher Gesamtendenergieverbrauch.
_ENEFG_MANAGEMENT_GWH = 7.5
_ENEFG_UMSETZUNGSPLAN_GWH = 2.5


def enefg_status(profile: dict):
    """Energieeffizienzgesetz: Managementsystem (§ 8) und Umsetzungsplaene (§ 9)."""
    gwh = float(profile.get("energy_gwh") or 0)
    if gwh <= 0:
        return "moeglich", "enefg_ohne_angabe"
    if gwh > _ENEFG_MANAGEMENT_GWH:
        return "ja", "enefg_ueber_7_5", "ja_management"
    if gwh > _ENEFG_UMSETZUNGSPLAN_GWH:
        return "ja", "enefg_ueber_2_5", "ja_umsetzungsplan"
    return "nein", "enefg_unter_2_5"


def abwv38_status(profile: dict):
    """Abwasserverordnung Anhang 38: Abwasser aus Textilherstellung oder -veredlung in Deutschland."""
    if profile.get("wet_processing_de"):
        return "ja", "abwv_nass"
    if (profile.get("branch") or "") == "Veredlung von Textilien und Bekleidung":
        return "moeglich", "abwv_branche_veredlung"
    return "nein", "abwv_keine"


# Ruecknahmesysteme in Frankreich und den Niederlanden. Zuerst ueber das LLM
# bewertet; im Live-Test am 29.09.2026 schloss es aus dem Absatzmarkt
# "Niederlande" auf eine Pflicht in Frankreich und zitierte einen Artikel, der in
# der abrufbaren Quelle gar nicht steht. Die Entscheidung haengt allein an
# Haekchen im Profil — deshalb regelbasiert.
_EPR_FR_PRODUKTE = frozenset({
    # Art. L541-10-1 Nr. 11° C. env.: Bekleidung, Schuhe, Haushaltswaesche und
    # neue Heimtextilien fuer Privatpersonen.
    "Bekleidung und Bekleidungszubehör", "Schuhe", "Heim- und Haustextilien",
    "Sport- und Freizeittextilien",
})
_EPR_NL_PRODUKTE = frozenset({
    # Art. 1 Abs. 2 Besluit UPV textiel: Kleidung (auch Berufskleidung, KN 61/62)
    # und Haushaltstextilien (KN 6302); Schuhe sind (noch) nicht erfasst.
    "Bekleidung und Bekleidungszubehör", "Heim- und Haustextilien",
    "Sport- und Freizeittextilien",
})


def _epr_status(profile: dict, land: str, produkte: frozenset, prefix: str,
                nur_b2c: bool):
    markets = set(profile.get("sales_markets") or ())
    cats = set(profile.get("product_categories") or ())
    if land not in markets and "andere EU-/EWR-Staaten" not in markets:
        return "nein", f"{prefix}_kein_absatz"
    if not (cats & produkte):
        return "nein", f"{prefix}_keine_produkte"
    if land not in markets:
        return "moeglich", f"{prefix}_andere_eu"
    if _only_supplier(profile):
        return "moeglich", f"{prefix}_zulieferer"
    if nur_b2c and not profile.get("b2c"):
        return "moeglich", f"{prefix}_ohne_b2c"
    return "ja", f"{prefix}_absatz"


def epr_fr_status(profile: dict):
    """Frankreich, REP TLC: Absatz nach Frankreich, erfasste Produkte, fuer Privatpersonen."""
    return _epr_status(profile, "Frankreich", _EPR_FR_PRODUKTE, "eprfr", nur_b2c=True)


def epr_nl_status(profile: dict):
    """Niederlande, UPV Textiel: erstmaliges Anbieten dort, auch Berufskleidung (B2B)."""
    return _epr_status(profile, "Niederlande", _EPR_NL_PRODUKTE, "eprnl", nur_b2c=False)


# child_key -> (Bezugs-Label, Statusfunktion)
#
# CSR-RUG haengt an keiner Elternregulierung, wird hier aber mitgefuehrt: die
# Entscheidung steht mit § 289b Abs. 1 HGB genauso fest wie bei den gekoppelten
# Faellen, und der Weg ueber diese Tabelle liefert die Textbausteine und den
# Vorrang vor dem LLM-Pfad ohne zweite Mechanik.
_COUPLINGS: dict[str, tuple[str, object]] = {
    "CSRD":            ("CSRD", csrd_status),
    "CSRD_DE":         ("CSRD", csrd_status),
    "TaxonomieVO":     ("CSRD", csrd_status),
    "HinSchG":         ("HinSchG", hinschg_status),
    "CSR-RUG":         ("CSR-RUG", csr_rug_status),
    # Katalogerweiterung 29.09.2026 (siehe Block oben)
    "REACH_ART33":     ("REACH Art. 33", reach_art33_status),
    "SCIP":            ("SCIP", scip_status),
    "BPR":             ("Biozid-VO", bpr_status),
    "PSA":             ("PSA-VO", psa_status),
    "MDR":             ("MDR", mdr_status),
    "Schuhkennzeichnung": ("Schuhkennzeichnung", schuh_status),
    "EnEfG":           ("EnEfG", enefg_status),
    "AbwV38":          ("AbwV Anhang 38", abwv38_status),
    "EPR_FR":          ("REP TLC", epr_fr_status),
    "EPR_NL":          ("UPV Textiel", epr_nl_status),
}

# child_key -> erlaeuternde Beziehung (warum die Eltern-Pflicht hier bindet)
_COUPLING_RELATION: dict[str, str] = {
    "CSRD_DE": ("Das CSRD-Umsetzungsgesetz setzt die CSRD in deutsches Recht um; fuer in "
                "Deutschland ansaessige Unternehmen gilt dieselbe Pflichtlage wie bei der CSRD."),
    "TaxonomieVO": ("Die Taxonomie-Offenlegung (Art. 8) trifft Unternehmen, die der CSRD "
                    "unterliegen; Finanzmarktteilnehmer sind zusaetzlich eigenstaendig erfasst."),
}


def coupling_verdict(reg_key: str, profile: dict) -> dict | None:
    """Deterministische Entscheidung fuer eine gekoppelte Regulierung (oder None).

    Rueckgabe: {applies, fact, conclusion, values}. `fact` waehlt den ersten
    Satz der Begruendung (Schwelle + Ist-Wert), `conclusion` den zweiten Satz
    (Folge fuer genau diese Regulierung); beide Texte stehen in `i18n`.
    """
    spec = _COUPLINGS.get(reg_key)
    if not spec:
        return None
    _parent_label, status_fn = spec
    outcome = status_fn(profile)
    applies, fact = outcome[0], outcome[1]
    # Optionaler dritter Wert: eigener Folgesatz, wenn derselbe Ausgang je nach
    # Fall anders weitergeht (siehe enefg_status, scip_status).
    conclusion = outcome[2] if len(outcome) > 2 else applies
    if (reg_key == "TaxonomieVO" and applies == "nein"
            and (profile.get("branch") or "") in _FINANCIAL_BRANCHES):
        # Art. 8 erfasst Finanzmarktteilnehmer eigenstaendig — ohne diese
        # Ausnahme wuerde die Kopplung an die CSRD sie faelschlich verneinen.
        applies, conclusion = "moeglich", "finanzmarkt"
    return {
        "applies": applies,
        "fact": fact,
        "conclusion": conclusion,
        "values": {
            "employees": profile.get("employees") or 0,
            "employees_de": profile.get("employees_de") or 0,
            "revenue_eur": profile.get("revenue_eur") or 0,
            "revenue_eu_eur": profile.get("revenue_eu_eur") or 0,
            "energy_gwh": profile.get("energy_gwh") or 0,
        },
    }


def coupling_premise(reg_key: str, profile: dict) -> str:
    """Verbindliche, vorberechnete Vorgabe fuer gekoppelte Regulierungen (oder '').

    Wird in den LLM-Prompt eingefuegt, damit gekoppelte Regulierungen nicht
    isoliert zu widerspruechlichen Ergebnissen kommen. Greift nur noch fuer
    Kopplungen OHNE hinterlegte Textbausteine — die uebrigen werden gar nicht
    erst an das LLM gegeben (siehe `llm.deterministic_result`).
    """
    from i18n import coupling_fact  # lokal: haelt die Importrichtung eindeutig

    verdict = coupling_verdict(reg_key, profile)
    if not verdict:
        return ""
    parent_label = _COUPLINGS[reg_key][0]
    lines = [f"{parent_label}-Pflicht = {verdict['applies'].upper()}. "
             f"Begruendung: {coupling_fact(verdict, 'de')}"]
    rel = _COUPLING_RELATION.get(reg_key)
    if rel:
        lines.append(rel)
    return "\n".join(lines)


# Profilfelder, die jede Begruendung beeinflussen, unabhaengig von der Regulierung.
_ALWAYS_RELEVANT: tuple[str, ...] = ("language",)


def relevant_fields_for(reg: dict) -> tuple[str, ...]:
    """Profilfelder, die das Ergebnis dieser Regulierung tragen (sortiert).

    Grundlage ist `relevant_fields` der Regulierung; `language` kommt immer
    hinzu, weil die Begruendung in der UI-Sprache formuliert wird.
    """
    fields = set(reg.get("relevant_fields") or ())
    fields.update(_ALWAYS_RELEVANT)
    return tuple(sorted(fields))


# Branchen: sprachneutrale Keys (= DE-String mit Umlauten) für DB-Persistenz.
# Übersetzungen: siehe i18n.BRANCH_LABELS
BRANCHES = [
    # NACE 13 - Herstellung von Textilien
    "Spinnstoffaufbereitung und Spinnerei",
    "Weberei",
    "Veredlung von Textilien und Bekleidung",
    "Herstellung von gewirktem und gestricktem Stoff",
    "Herstellung von konfektionierten Textilwaren (ohne Bekleidung)",
    "Herstellung von Teppichen",
    "Herstellung von Seilerwaren",
    "Herstellung von Vliesstoff und Erzeugnissen daraus (ohne Bekleidung)",
    "Herstellung von technischen Textilien",
    "Herstellung von sonstigen Textilwaren a. n. g.",
    # NACE 14 - Herstellung von Bekleidung
    "Herstellung von Lederbekleidung",
    "Herstellung von Arbeits- und Berufsbekleidung",
    "Herstellung von sonstiger Oberbekleidung",
    "Herstellung von Wäsche",
    "Herstellung von sonstiger Bekleidung und Bekleidungszubehör a. n. g.",
    "Herstellung von Pelzwaren",
    "Herstellung von Strumpfwaren",
    "Herstellung von sonstiger Bekleidung aus gewirktem und gestricktem Stoff",
    # NACE 15 - Herstellung von Leder, Lederwaren und Schuhen
    "Herstellung von Leder und Lederfaserstoff; Zurichtung und Färben von Fellen",
    "Lederverarbeitung (ohne Herstellung von Lederbekleidung)",
    "Herstellung von Schuhen",
    # NACE 96.01
    "Wäscherei und chemische Reinigung",
]

# Standort-Typen: sprachneutrale Keys (= DE-String) fuer die DB-Persistenz.
#
# Die Liste wurde am 15.09.2026 vollstaendig ersetzt: sie trennt jetzt den
# Unternehmenssitz von der Zweigniederlassung (frueher ein gemeinsamer Wert)
# und fasst Vertriebsbuero und Filiale zum Vertriebsstandort zusammen.
# Altprofile tragen die alten Werte; `db._SITE_TYPE_RENAMES` hebt sie beim
# Lesen und Schreiben auf die heutigen Bezeichnungen (siehe dort — zwei
# Zuordnungen sind fachlich unscharf und dort begruendet).
SITE_TYPES = [
    "Unternehmenssitz / Hauptverwaltung (einschließlich satzungsmäßigem Sitz, Hauptniederlassung und Verwaltungssitz)",
    "Zweigniederlassung / Niederlassung (rechtlich oder organisatorisch verselbstständigte Niederlassungen)",
    "Produktionsstätte / Werk (Herstellung, Verarbeitung oder Veredelung)",
    "Lager / Logistikzentrum (Lagerung, Versand oder Distribution)",
    "Vertriebsstandort / Verkaufsstelle (Vertriebsbüros, Showrooms, eigene Verkaufsstellen/Filialen)",
    "Forschungs- und Entwicklungsstandort",
]

LOCATIONS = ["Deutschland", "EU (ohne Deutschland)", "Weltweit (außerhalb EU)"]

LEGAL_FORMS = [
    "AG / SE",
    "GmbH",
    "GmbH & Co. KG",
    "KG / OHG",
    "Einzelunternehmen",
    "Genossenschaft",
    "Stiftung / Verein",
    "Limited / Ltd.",
    "Sonstige",
]

GROUP_ROLES = [
    "Eigenständig (kein Konzern)",
    "Mutterunternehmen mit Sitz in EU",
    "Mutterunternehmen mit Sitz außerhalb EU",
    "Tochter, EU-Muttergesellschaft",
    "Tochter, Nicht-EU-Muttergesellschaft",
]

# Produktkategorien: sprachneutrale Keys (= DE-String) fuer die DB-Persistenz.
# Uebersetzungen: siehe i18n.PRODUCT_CAT_LABELS.
#
# Die Liste wurde am 02.09.2026 vollstaendig ausgetauscht und auf die
# Warengruppen der Textil- und Modewirtschaft zugeschnitten. Profile aus der
# Zeit davor tragen die alten Werte; `db.get_company()` filtert alles heraus,
# was hier nicht mehr steht, damit weder Formular noch LLM-Prompt noch der
# Cache-Schluessel einen unbekannten Wert sehen (siehe dort).
PRODUCT_CATEGORIES = [
    "Textile Vor- und Zwischenprodukte – Fasern, Garne, Gewebe, Gestricke, Vliesstoffe",
    "Bekleidung und Bekleidungszubehör",
    "Schuhe",
    "Lederwaren und Accessoires",
    "Heim- und Haustextilien",
    "Schutztextilien / PSA",
    "Medizin- und Gesundheitstextilien",
    "Mobilitäts- und Transporttextilien – Automotive, Luft- und Raumfahrt, Bahn, Schifffahrt",
    "Industrie- und Filtertextilien – Filter, Förderbänder, technische Gewebe, textile Maschinenkomponenten",
    "Bau- und Geotextilien – Bautextilien, Membranen, Gewebe für Erd-/Straßenbau",
    "Agrartextilien – Netze, Vliese, Abdeckungen etc.",
    "Sport- und Freizeittextilien",
    "Sonstige technische Textilien",
]

# Rolle in der Wertschoepfungskette (Mehrfachauswahl).
#
# Traegt die Frage, ob eine produktbezogene Pflicht ueberhaupt an diesem
# Unternehmen haengt: das Vernichtungsverbot und die PPWR richten sich an
# "Wirtschaftsteilnehmer", die EUDR an Marktteilnehmer UND Haendler, die
# EmpCo-Vorgaben an denjenigen, der die Umweltaussage gegenueber Verbrauchern
# macht. Uebersetzungen: siehe i18n.ROLE_LABELS.
VALUE_CHAIN_ROLES = [
    "Hersteller (stellt Produkte selbst her oder lässt sie herstellen und vermarktet sie unter eigenem Namen/eigener Marke)",
    "Importeur (bringt Produkte aus einem Drittstaat auf den EU-Markt)",
    "Händler/Vertreiber (stellt Produkte anderer Unternehmen auf dem Markt bereit)",
    "Markeninhaber / Vertrieb unter eigener oder lizenzierter Marke",
    "Zulieferer",
]

# Eingesetzte Materialien (Mehrfachauswahl).
#
# Fuer die EUDR entscheidet der Rohstoff (Rinderleder, Naturkautschuk, Holz und
# zellulosebasierte Fasern), fuer die Zwangsarbeitsverordnung das Rohstoffrisiko
# und fuer die Oekodesign-Anforderungen die chemische Ausruestung (PFAS).
# Uebersetzungen: siehe i18n.MATERIAL_LABELS.
MATERIALS = [
    # Naturfasern
    "Baumwolle",
    "Sonstige pflanzliche Naturfasern (z. B. Flachs/Leinen, Hanf, Jute)",
    "Tierische Fasern (z. B. Wolle, Kaschmir, Mohair, Alpaka, Seide)",
    # Chemiefasern
    "Zellulosebasierte Chemiefasern (z. B. Viskose, Modal, Lyocell)",
    "Synthetische Chemiefasern (z. B. Polyester, Polyamid, Polyacryl, Elastan)",
    # Weitere Materialien
    "Leder / Rindererzeugnisse",
    "Naturkautschuk",
    "Recyclingmaterialien",
    "Sonstige Materialien",
    # Chemische Ausruestungen / Behandlungen
    "Wasser-, öl- oder schmutzabweisende Ausrüstung",
    "Flammhemmende / flammwidrige Ausrüstung",
    "Antimikrobielle / biozide Ausrüstung",
    "PFAS-haltige Ausrüstung",
    "Sonstige besondere chemische Ausrüstung",
    "Nicht bekannt / kann nicht ausgeschlossen werden",
]

# Gliederung der Materialliste fuer das Formular (nur Darstellung; gespeichert,
# an das LLM gereicht und gecacht wird weiterhin die flache Liste `MATERIALS`).
# Uebersetzung der Ueberschriften: siehe i18n.MATERIAL_GROUP_LABELS.
MATERIAL_GROUPS = [
    ("Naturfasern", MATERIALS[0:3]),
    ("Chemiefasern", MATERIALS[3:5]),
    ("Weitere Materialien", MATERIALS[5:9]),
    ("Chemische Ausrüstungen / Behandlungen", MATERIALS[9:]),
]

# Absatzmaerkte (Mehrfachauswahl).
#
# Wo ein Unternehmen absetzt, entscheidet mit darueber, ob eine produkt-
# bezogene Marktordnung ueberhaupt greift: EUDR, PPWR, Vernichtungsverbot,
# Right to Repair und die EmpCo-Vorgaben knuepfen an das Inverkehrbringen bzw.
# Bereitstellen auf dem Unionsmarkt an. Wer ausschliesslich ausserhalb der EU
# absetzt, wird von ihnen nicht erfasst.
#
# Frankreich und die Niederlande stehen seit 29.09.2026 einzeln da: beide haben
# eigene Ruecknahmesysteme fuer Textilien (REP TLC bzw. UPV Textiel), die auch
# Anbieter aus Deutschland erfassen. "andere EU-/EWR-Staaten" meint seitdem die
# uebrigen; Altprofile mit diesem Haken koennen trotzdem nach FR/NL liefern —
# die beiden Karten sagen dann "Pruefen" statt "Nicht einschlaegig".
# Uebersetzungen: siehe i18n.SALES_MARKET_LABELS.
SALES_MARKETS = [
    "Deutschland",
    "Frankreich",
    "Niederlande",
    "andere EU-/EWR-Staaten",
    "außerhalb EU/EWR",
]

# Enthalten Produkte Stoffe der ECHA-Kandidatenliste ueber 0,1 %? (Einfachauswahl)
# Traegt REACH Art. 33 und die SCIP-Meldung. "Nicht bekannt" ist die
# Voreinstellung und fuehrt zu "Pruefen" — die meisten Unternehmen wissen es
# ohne Lieferantenabfrage nicht. Uebersetzungen: siehe i18n.SVHC_LABELS.
SVHC_OPTIONS = [
    "Nicht bekannt",
    "Ja",
    "Nein",
]
