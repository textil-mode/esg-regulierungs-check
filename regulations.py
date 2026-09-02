"""Kuratierte Liste der 22 ESG-/CSR-Regulierungen mit Anwendbarkeitskriterien.

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
        "relevant_fields": ["employees", "revenue_eur", "group_role", "legal_form", "sites"],
        "name": "CSDDD",
        "full_name": "Richtlinie (EU) 2024/1760 - Sorgfaltspflichten von Unternehmen im Hinblick auf Nachhaltigkeit",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024L1760",
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
        "name": "LkSG",
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
        "relevant_fields": ["product_categories", "eu_importer", "branch"],
        "name": "EUDR",
        "full_name": "Verordnung (EU) 2023/1115 über entwaldungsfreie Lieferketten",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02023R1115",
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
        "relevant_fields": ["product_categories", "eu_importer", "branch"],
        "name": "FLR (Zwangsarbeitsverordnung)",
        "full_name": "Verordnung (EU) 2024/3015 - Verbot von in Zwangsarbeit hergestellten Produkten",
        # ELI-Form bewusst beibehalten: zu 2024/3015 gibt es (Stand 09/2026)
        # keine konsolidierte Fassung, der Ursprungsrechtsakt IST der geltende
        # Text. Gleiches gilt fuer Right to Repair (2024/1799). Alle uebrigen
        # EU-Quellen zeigen auf die datumslose konsolidierte CELEX-ID, sonst
        # lieferte der Abruf dauerhaft die Ursprungsfassung — bei der EUDR waere
        # das der Stand VOR den beiden Verschiebungen gewesen.
        "url": "https://eur-lex.europa.eu/eli/reg/2024/3015/oj",
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
        "relevant_fields": ["employees", "revenue_eur", "listed", "group_role"],
        "name": "CSRD",
        "full_name": "Richtlinie (EU) 2022/2464 - Nachhaltigkeitsberichterstattung",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02022L2464",
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
        "relevant_fields": ["employees", "revenue_eur", "listed", "group_role"],
        "name": "CSRD-Umsetzungsgesetz (DE)",
        "full_name": "Gesetz zur Umsetzung der Richtlinie (EU) 2022/2464",
        "url": "https://dserver.bundestag.de/btd/21/018/2101857.pdf",
        "scope": "DE",
        "criteria": (
            "Deutsche Umsetzung der CSRD; gilt für in Deutschland ansässige große Unternehmen und "
            "Konzerne gemäß den CSRD-Schwellen (siehe CSRD). Berichtspflicht im Lagebericht (§ 289b HGB-E)."
        ),
        "key_article": "§§ 289b-289h HGB-E",
    },
    {
        "nr": 7,
        "key": "ESRS",
        "relevant_fields": ["employees", "revenue_eur", "listed", "group_role"],
        "name": "ESRS",
        "full_name": "Delegierte Verordnung (EU) 2023/2772 - Nachhaltigkeitsberichterstattung (Standards)",
        # Zeigte bis 09/2026 faelschlich auf die CSRD (02022L2464); die Karte
        # zitierte deshalb CSRD-Artikel statt der ESRS.
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02023R2772",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02023R2772",
        "scope": "EU",
        "criteria": (
            "Technische Standards für die Nachhaltigkeitsberichterstattung. Gelten für alle Unternehmen, "
            "die unter die CSRD fallen. Anwendung abhängig von CSRD-Pflicht."
        ),
        "key_article": "Annex I (ESRS 1, ESRS 2, E1-E5, S1-S4, G1)",
    },
    {
        "nr": 8,
        "key": "NFRD",
        "relevant_fields": [
            "employees", "revenue_eur", "balance_sheet_eur", "listed", "legal_form",
        ],
        "name": "NFRD",
        "full_name": "Richtlinie 2014/95/EU - nichtfinanzielle Berichterstattung",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02014L0095",
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
        "nr": 9,
        "key": "CSR-RUG",
        "relevant_fields": [
            "employees", "employees_de", "revenue_eur", "balance_sheet_eur", "listed", "legal_form",
            "group_role", "sites",
        ],
        "name": "CSR-RUG",
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
        "nr": 10,
        "key": "TaxonomieVO",
        "relevant_fields": ["employees", "revenue_eur", "listed", "group_role", "branch"],
        "name": "Taxonomie-Verordnung",
        "full_name": "Verordnung (EU) 2020/852 - Rahmen für nachhaltige Investitionen",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02020R0852",
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
        "nr": 11,
        "key": "SFDR",
        "relevant_fields": ["branch"],
        "name": "SFDR",
        "full_name": "Verordnung (EU) 2019/2088 - nachhaltigkeitsbezogene Offenlegungspflichten",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02019R2088",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02019R2088",
        "scope": "EU",
        "criteria": (
            "Gilt ausschließlich für Finanzmarktteilnehmer (Vermögensverwalter, Versicherer, AIFM, UCITS) "
            "und Finanzberater. Nicht für Realwirtschaft. "
            "Anwendbar wenn Branche = Finanzdienstleistungen/Versicherungen."
        ),
        "key_article": "Art. 2, 3",
    },
    {
        "nr": 12,
        "key": "ESGRatingVO",
        "relevant_fields": ["branch"],
        "name": "ESG Rating VO",
        "full_name": "Verordnung (EU) 2024/3005 - ESG-Ratings",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024R3005",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024R3005",
        "scope": "EU",
        "criteria": (
            "Gilt für Anbieter von ESG-Ratings mit Tätigkeit in der EU. "
            "Nicht für bewertete Unternehmen selbst. Relevant nur bei Branche = ESG-Rating-Anbieter."
        ),
        "key_article": "Art. 2",
    },
    {
        "nr": 13,
        "key": "WhistleblowerRL",
        "relevant_fields": ["employees_de", "branch"],
        "name": "Whistleblower-Richtlinie",
        "full_name": "Richtlinie (EU) 2019/1937 - Schutz von Hinweisgebern",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02019L1937",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02019L1937",
        "scope": "EU",
        "criteria": (
            "Richtet sich an Mitgliedstaaten. In DE umgesetzt durch HinSchG. "
            "Direkte Anwendung für Unternehmen über HinSchG."
        ),
        "key_article": "Art. 8",
    },
    {
        "nr": 14,
        "key": "HinSchG",
        "relevant_fields": ["employees_de", "branch"],
        "name": "HinSchG",
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
        "nr": 15,
        "key": "RightToRepair",
        "relevant_fields": ["product_categories", "branch", "eu_importer"],
        "name": "Right to Repair",
        "full_name": "Richtlinie (EU) 2024/1799 - Reparatur von Waren",
        "url": "https://eur-lex.europa.eu/eli/dir/2024/1799/oj",
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
        "nr": 16,
        "key": "Oekodesign",
        "relevant_fields": ["product_categories", "branch", "eu_importer"],
        "name": "Ökodesign-VO",
        "full_name": "Verordnung (EU) 2024/1781 - nachhaltige Produkte (ESPR)",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024R1781",
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
        "nr": 17,
        "key": "PPWR",
        "relevant_fields": ["product_categories", "branch", "eu_importer"],
        "name": "PPWR",
        "full_name": "Verordnung (EU) 2025/40 - Verpackungen und Verpackungsabfälle",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02025R0040",
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
        "nr": 18,
        "key": "KonfliktminVO",
        "relevant_fields": ["product_categories", "eu_importer", "branch"],
        "name": "Konfliktmineralien-VO",
        "full_name": "Verordnung (EU) 2017/821 - Konfliktmineralien",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02017R0821",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02017R0821",
        "scope": "EU",
        "criteria": (
            "Gilt für Unionseinführer von Zinn, Tantal, Wolfram, deren Erzen und Gold. "
            "Volumenschwellen pro Mineral in Anhang I. Branche relevant: Metallimporteure, Elektronik, "
            "Schmuck, Automobil mit Direktimport."
        ),
        "key_article": "Art. 1, Anhang I",
    },
    {
        "nr": 19,
        "key": "MinRohSorgG",
        "relevant_fields": ["product_categories", "eu_importer", "sites"],
        "name": "MinRohSorgG",
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
        "nr": 20,
        "key": "UmweltstrafRL",
        "relevant_fields": ["branch"],
        "name": "EU Umweltstrafrechts-RL",
        "full_name": "Richtlinie (EU) 2024/1203 - strafrechtlicher Schutz der Umwelt",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024L1203",
        "text_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024L1203",
        "scope": "EU",
        "criteria": (
            "Richtet sich primär an Mitgliedstaaten (Umsetzung ins nationale Strafrecht). "
            "Unternehmen sind indirekt betroffen: juristische Personen haftbar für definierte Umweltstraftaten. "
            "Alle Branchen, insbes. Industrie/Chemie/Abfall."
        ),
        "key_article": "Art. 3, 7",
    },
    {
        "nr": 21,
        "key": "EmpCo",
        "relevant_fields": ["b2c", "env_claims"],
        "name": "EmpCo",
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
    {
        "nr": 22,
        "key": "GreenClaims",
        "relevant_fields": ["b2c", "env_claims", "employees", "revenue_eur"],
        # Kein "(Entwurf)" im Namen: der Zusatz stuende auch in der englischen
        # und franzoesischen Tabelle auf Deutsch. Den Entwurfscharakter tragen
        # der Status-Badge und der Stand-Hinweis, beide uebersetzt.
        "name": "Green Claims Directive",
        "full_name": "Vorschlag Richtlinie - Begründung/Kommunikation ausdrücklicher Umweltaussagen",
        "url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:52023PC0166",
        "text_url": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:52023PC0166",
        "scope": "EU",
        "criteria": (
            "Entwurf, nicht in Kraft. Die EU-Kommission hat am 20.06.2025 angekündigt, den Vorschlag "
            "zurückzuziehen; förmlich zurückgenommen ist er bislang nicht, das Verfahren ruht. "
            "Für Unternehmen ergeben sich daraus derzeit KEINE unmittelbaren Pflichten — die Regeln zu "
            "Umweltaussagen greifen aktuell über die EmpCo-Richtlinie (EU) 2024/825 bzw. das UWG. "
            "Bei Verabschiedung würde sie B2C-Unternehmen mit ausdrücklichen Umweltaussagen treffen; "
            "Kleinstunternehmen (<10 MA & Umsatz <2 Mio EUR) wären ausgenommen."
        ),
        "key_article": "Art. 1, 3",
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
         "url": "https://www.csr-in-deutschland.de/DE/Wirtschaft-Menschenrechte/Ueber-das-Gesetz/FAQ/faq_node.html"},
    ],
    "EUDR": [
        {"name": "EU-Kommission – Entwaldungsfreie Lieferketten (EUDR)",
         "url": "https://environment.ec.europa.eu/topics/forests/deforestation/regulation-deforestation-free-products_en"},
    ],
    "FLR": [
        {"name": "EU-Kommission – Forced Labour Regulation",
         "url": "https://commission.europa.eu/business-economy-euro/doing-business-eu/sustainable-economy/forced-labour-regulation_en"},
    ],
    "CSRD": [
        {"name": "EU-Kommission – CSRD Implementierung & Q&A",
         "url": "https://finance.ec.europa.eu/regulation-and-supervision/financial-services-legislation/implementing-and-delegated-acts/corporate-sustainability-reporting-directive_en"},
    ],
    "CSRD_DE": [
        {"name": "IDW – CSRD-Umsetzung in Deutschland",
         "url": "https://www.idw.de/idw/im-fokus/csrd"},
    ],
    "ESRS": [
        {"name": "EFRAG – European Sustainability Reporting Standards",
         "url": "https://www.efrag.org/en/projects/european-sustainability-reporting-standards-esrs"},
    ],
    "NFRD": [
        {"name": "EU-Kommission – Non-Financial Reporting (Historie)",
         "url": "https://finance.ec.europa.eu/capital-markets-union-and-financial-markets/company-reporting-and-auditing/company-reporting/corporate-sustainability-reporting_en"},
    ],
    "CSR-RUG": [
        {"name": "DRSC – Deutsche Anwendungshinweise zur nichtfinanziellen Berichterstattung",
         "url": "https://www.drsc.de/themen/nachhaltigkeitsberichterstattung/"},
    ],
    "TaxonomieVO": [
        {"name": "EU-Kommission – EU-Taxonomie",
         "url": "https://finance.ec.europa.eu/sustainable-finance/tools-and-standards/eu-taxonomy-sustainable-activities_en"},
    ],
    "SFDR": [
        {"name": "EU-Kommission – SFDR Offenlegungspflichten",
         "url": "https://finance.ec.europa.eu/sustainable-finance/disclosures/sustainability-related-disclosure-financial-services-sector_en"},
    ],
    "ESGRatingVO": [
        {"name": "ESMA – ESG Ratings",
         "url": "https://www.esma.europa.eu/esmas-activities/sustainable-finance/esg-ratings"},
    ],
    "WhistleblowerRL": [
        {"name": "EU-Kommission – Schutz von Hinweisgebern",
         "url": "https://commission.europa.eu/aid-development-cooperation-fundamental-rights/your-rights-eu/whistleblowers-protection_en"},
    ],
    "HinSchG": [
        {"name": "Bundesamt für Justiz – Externe Meldestelle (HinSchG)",
         "url": "https://www.bundesjustizamt.de/DE/MeldestelledesBundes/MeldestelledesBundes_node.html"},
    ],
    "RightToRepair": [
        {"name": "EU-Kommission – Right to Repair",
         "url": "https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/european-green-deal/right-repair_en"},
    ],
    "Oekodesign": [
        {"name": "EU-Kommission – Ecodesign for Sustainable Products Regulation (ESPR)",
         "url": "https://commission.europa.eu/energy-climate-change-environment/standards-tools-and-labels/products-labelling-rules-and-requirements/sustainable-products/ecodesign-sustainable-products-regulation_en"},
    ],
    "PPWR": [
        {"name": "EU-Kommission – Verpackungen und Verpackungsabfälle",
         "url": "https://environment.ec.europa.eu/topics/waste-and-recycling/packaging-waste_en"},
    ],
    "KonfliktminVO": [
        {"name": "EU-Kommission – Konfliktmineralien-Verordnung",
         "url": "https://policy.trade.ec.europa.eu/development-and-sustainability/conflict-minerals-regulation_en"},
    ],
    "MinRohSorgG": [
        {"name": "BAFA – Mineralische Rohstoffe",
         "url": "https://www.bafa.de/DE/Wirtschaft_Rohstoffe/Mineralische_Rohstoffe/mineralische_rohstoffe_node.html"},
    ],
    "UmweltstrafRL": [
        {"name": "EU-Kommission – Environmental Crime Directive",
         "url": "https://environment.ec.europa.eu/law/environmental-crime_en"},
    ],
    "EmpCo": [
        {"name": "EU-Kommission – Stärkung der Verbraucher für den grünen Wandel",
         "url": "https://commission.europa.eu/law/law-topic/consumer-protection-law/empowering-consumers-green-transition_en"},
    ],
    "GreenClaims": [
        {"name": "EU-Kommission – Green Claims",
         "url": "https://environment.ec.europa.eu/topics/circular-economy/green-claims_en"},
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
    "ESRS": ["esrs_1", "esrs_2", "esrs_3"],
    "NFRD": ["nfrd_1", "nfrd_2"],
    "CSR-RUG": ["csr_rug_1", "csr_rug_2", "csr_rug_3"],
    "TaxonomieVO": ["taxonomie_1", "taxonomie_2", "taxonomie_3"],
    "SFDR": ["sfdr_1", "sfdr_2", "sfdr_3"],
    "ESGRatingVO": ["esgrating_1", "esgrating_2", "esgrating_3"],
    "WhistleblowerRL": ["whistle_1", "whistle_2", "whistle_3"],
    "HinSchG": ["hinschg_1", "hinschg_2", "hinschg_3", "hinschg_4"],
    "RightToRepair": ["r2r_1", "r2r_2", "r2r_3"],
    "Oekodesign": ["oekodesign_1", "oekodesign_2", "oekodesign_3"],
    "PPWR": ["ppwr_1", "ppwr_2", "ppwr_3"],
    "KonfliktminVO": ["konfliktmin_1", "konfliktmin_2", "konfliktmin_3"],
    "MinRohSorgG": ["minroh_1", "minroh_2", "minroh_3"],
    "UmweltstrafRL": ["umweltstraf_1", "umweltstraf_2", "umweltstraf_3"],
    "EmpCo": ["empco_1", "empco_2", "empco_3", "empco_4"],
    "GreenClaims": ["greenclaims_1", "greenclaims_2"],
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
    "ESRS":            "22.12.2023",
    "NFRD":            "15.11.2014",
    "CSR-RUG":         "11.04.2017",
    "TaxonomieVO":     "22.06.2020",
    "SFDR":            "09.12.2019",
    "ESGRatingVO":     "12.12.2024",
    "WhistleblowerRL": "26.11.2019",
    "HinSchG":         "02.06.2023",
    "RightToRepair":   "10.07.2024",
    "Oekodesign":      "28.06.2024",
    "PPWR":            "22.01.2025",
    "KonfliktminVO":   "19.05.2017",
    "MinRohSorgG":     "18.12.2020",
    "UmweltstrafRL":   "30.04.2024",
    "EmpCo":           "06.03.2024",
    # Datum des Kommissionsvorschlags COM(2023) 166 final.
    "GreenClaims":     "22.03.2023",
}

# Regulierungen, deren Datum oben nur ein Entwurfsstand ist (keine Verkuendung).
# Die Liste ersetzt die frueheren deutschen Freitexte "Entwurf 2025" /
# "Entwurf 22.03.2023", die auch in EN/FR/ES/IT/ZH auf Deutsch erschienen.
DRAFT_PUBLISHED: frozenset[str] = frozenset({"CSRD_DE", "GreenClaims"})


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
    # Art. 2 Del. VO (EU) 2023/2772: gilt fuer Geschaeftsjahre ab 01.01.2024.
    "ESRS":            {"applies_from": "01.01.2024"},
    # Art. 4 Abs. 1 UAbs. 2 RL 2014/95/EU: ab dem am 01.01.2017 beginnenden GJ.
    "NFRD":            {"applies_from": "01.01.2017", "note": "nfrd"},
    # §§ 289b ff. HGB: erstmals fuer nach dem 31.12.2016 beginnende Geschaeftsjahre.
    "CSR-RUG":         {"applies_from": "01.01.2017", "note": "csr_rug"},
    # Art. 27 Abs. 2 VO (EU) 2020/852.
    "TaxonomieVO":     {"applies_from": "01.01.2022", "note": "taxonomie"},
    # Art. 20 Abs. 2 VO (EU) 2019/2088.
    "SFDR":            {"applies_from": "10.03.2021"},
    # Art. 53 VO (EU) 2024/3005.
    "ESGRatingVO":     {"applies_from": "02.07.2026"},
    # Art. 26 Abs. 1 RL (EU) 2019/1937 (Abs. 2: 50-249 Beschaeftigte ab 17.12.2023).
    "WhistleblowerRL": {"applies_from": "17.12.2021", "note": "whistle"},
    # Art. 10 Abs. 2 HinSchG-Artikelgesetz.
    "HinSchG":         {"applies_from": "02.07.2023"},
    # Art. 22 Abs. 1 UAbs. 3 RL (EU) 2024/1799.
    "RightToRepair":   {"applies_from": "31.07.2026"},
    # Art. 80 VO (EU) 2024/1781 (20. Tag nach ABl. vom 28.06.2024).
    "Oekodesign":      {"applies_from": "18.07.2024", "note": "oekodesign"},
    # Art. 71 VO (EU) 2025/40.
    "PPWR":            {"applies_from": "12.08.2026"},
    # Art. 20 Abs. 2/3 VO (EU) 2017/821.
    "KonfliktminVO":   {"applies_from": "09.07.2017", "note": "konfliktmin"},
    # Art. 3 MinRohSorgG-Artikelgesetz (Fussnote gesetze-im-internet.de).
    "MinRohSorgG":     {"applies_from": "07.05.2020"},
    # Art. 28 Abs. 1 RL (EU) 2024/1203 (Umsetzungsfrist der Mitgliedstaaten).
    "UmweltstrafRL":   {"applies_from": "21.05.2026", "note": "umweltstraf"},
    # Art. 4 Abs. 1 UAbs. 2 RL (EU) 2024/825.
    "EmpCo":           {"applies_from": "27.09.2026", "note": "empco"},
    # Kommission hat die Ruecknahme am 20.06.2025 angekuendigt, aber nicht vollzogen.
    "GreenClaims":     {"applies_from": "", "status": STATUS_RUECKZUG, "note": "greenclaims"},
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
#   ESRS / Taxonomie-VO / CSRD-Umsetzungsgesetz folgen der CSRD-Pflicht,
#   die Whistleblower-RL wird in DE ueber das HinSchG umgesetzt.
# Damit das LLM diese nicht isoliert und widerspruechlich bewertet (z. B.
# CSRD = nein, aber ESRS = ja fuer dasselbe Unternehmen), wird der ausloesende
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
    if non_eu_parent and rev > 450_000_000:
        return "moeglich", "csrd_drittland"
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


# child_key -> (Eltern-Label, Statusfunktion)
_COUPLINGS: dict[str, tuple[str, object]] = {
    "CSRD":            ("CSRD", csrd_status),
    "CSRD_DE":         ("CSRD", csrd_status),
    "ESRS":            ("CSRD", csrd_status),
    "TaxonomieVO":     ("CSRD", csrd_status),
    "HinSchG":         ("HinSchG", hinschg_status),
    "WhistleblowerRL": ("HinSchG", hinschg_status),
}

# child_key -> erlaeuternde Beziehung (warum die Eltern-Pflicht hier bindet)
_COUPLING_RELATION: dict[str, str] = {
    "CSRD_DE": ("Das CSRD-Umsetzungsgesetz setzt die CSRD in deutsches Recht um; fuer in "
                "Deutschland ansaessige Unternehmen gilt dieselbe Pflichtlage wie bei der CSRD."),
    "ESRS": "Die ESRS gelten ausschliesslich fuer Unternehmen, die der CSRD unterliegen.",
    "TaxonomieVO": ("Die Taxonomie-Offenlegung (Art. 8) trifft Unternehmen, die der CSRD "
                    "unterliegen; Finanzmarktteilnehmer sind zusaetzlich eigenstaendig erfasst."),
    "WhistleblowerRL": ("Die EU-Whistleblower-Richtlinie wird in Deutschland ueber das HinSchG "
                        "umgesetzt; es gilt dieselbe Schwelle von 50 Beschaeftigten."),
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
    applies, fact = status_fn(profile)
    conclusion = applies
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
    "Land-/Forstwirtschaft, Fischerei",
    "Bergbau / Gewinnung von Steinen und Erden",
    "Verarbeitendes Gewerbe / Industrie",
    "Chemie / Pharma",
    "Metallverarbeitung / Maschinenbau",
    "Automobil / Fahrzeugbau",
    "Elektronik / Elektrotechnik",
    "Textil / Bekleidung / Leder",
    "Lebensmittel / Getränke",
    "Möbel / Holz / Papier",
    "Energieversorgung",
    "Wasser- / Abfallwirtschaft",
    "Bauwirtschaft",
    "Handel (Groß-/Einzelhandel)",
    "Verkehr / Logistik",
    "Gastgewerbe / Tourismus",
    "Information / Telekommunikation / IT",
    "Finanzdienstleistungen",
    "Versicherungen",
    "Immobilien",
    "Beratung / Recht / Wirtschaftsprüfung",
    "Forschung / Entwicklung",
    "Bildung",
    "Gesundheit / Soziales",
    "Kunst / Unterhaltung / Medien",
    "Sonstige Dienstleistungen",
]

SITE_TYPES = [
    "Hauptsitz",
    "Produktionsstätte",
    "Vertriebsbüro",
    "Lager / Logistikzentrum",
    "Forschung / Entwicklung",
    "Filiale / Niederlassung",
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

PRODUCT_CATEGORIES = [
    "Verpackungen (eigene oder vertriebene)",
    "Elektronik / Haushaltsgeräte / IT-Hardware",
    "Holz / Holzprodukte / Papier",
    "Kaffee / Kakao",
    "Palmöl / Soja",
    "Kautschuk / Gummi",
    "Rinder / Rindsprodukte / Leder",
    "Zinn / Tantal / Wolfram / Gold (Direktimport)",
    "Chemische Stoffe",
    "Textilien / Bekleidung / Leder",
    "Möbel / Baustoffe",
    "Lebensmittel / Getränke",
    "Keine physischen Produkte (nur Dienstleistung/Software)",
]
