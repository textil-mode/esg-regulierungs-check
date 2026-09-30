"""Zentrale Übersetzungen für die ESG-App.

Unterstützt: de, en, es, fr, it, zh
Strategie: UI-Strings nach Keys, Dropdown-Optionen per Mapping
(DE-String ist intern der "Key", damit bestehende DB-Einträge gültig bleiben).
"""
from __future__ import annotations

LANGUAGES: dict[str, str] = {
    "de": "Deutsch",
    "en": "English",
    "es": "Español",
    "fr": "Français",
    "it": "Italiano",
    "zh": "中文",
}

LANG_CODES = tuple(LANGUAGES.keys())


# ---------- UI-Strings ----------
UI: dict[str, dict[str, str]] = {
    # App-weit
    "app_title": {
        "de": "ESG-Regulierungs-Check",
        "en": "ESG Regulation Check",
        "es": "Verificación de Regulaciones ESG",
        "fr": "Vérification des Réglementations ESG",
        "it": "Verifica delle Normative ESG",
        "zh": "ESG 法规检查",
    },
    "app_subtitle": {
        "de": "Erhalten Sie einen ersten Überblick, welche ESG-Regulierungen für Ihr Unternehmen relevant sein könnten",
        "en": "Get a first overview of which ESG regulations could be relevant for your company",
        "es": "Obtenga una primera visión general de qué regulaciones ESG podrían ser relevantes para su empresa",
        "fr": "Obtenez un premier aperçu des réglementations ESG qui pourraient être pertinentes pour votre entreprise",
        "it": "Ottenga una prima panoramica delle normative ESG che potrebbero essere rilevanti per la sua azienda",
        "zh": "先大致了解哪些 ESG 法规可能与贵公司相关",
    },
    "beta_badge": {
        "de": "Beta-Version",
        "en": "Beta version",
        "es": "Versión beta",
        "fr": "Version bêta",
        "it": "Versione beta",
        "zh": "测试版",
    },
    "beta_hint": {
        "de": "Diese Anwendung befindet sich noch in der Erprobung. Inhalte, Bewertungen und Funktionen können sich ändern.",
        "en": "This application is still being trialled. Content, assessments and functions may change.",
        "es": "Esta aplicación aún se encuentra en fase de prueba. Los contenidos, las evaluaciones y las funciones pueden cambiar.",
        "fr": "Cette application est encore en phase d'essai. Les contenus, les évaluations et les fonctions peuvent évoluer.",
        "it": "Questa applicazione è ancora in fase di prova. Contenuti, valutazioni e funzioni possono cambiare.",
        "zh": "本应用仍处于试用阶段，内容、评估结果和功能可能会发生变化。",
    },
    "login_ack": {
        "de": "Ich habe den Hinweis gelesen und zur Kenntnis genommen.",
        "en": "I have read and noted the notice.",
        "es": "He leído y tomado nota de la advertencia.",
        "fr": "J'ai lu et pris connaissance de l'avertissement.",
        "it": "Ho letto e preso atto dell'avvertenza.",
        "zh": "我已阅读并知悉上述提示。",
    },
    "login_ack_required": {
        "de": "Bitte bestätigen Sie zuerst, dass Sie den Hinweis gelesen haben.",
        "en": "Please confirm first that you have read the notice.",
        "es": "Confirme primero que ha leído la advertencia.",
        "fr": "Veuillez d'abord confirmer que vous avez lu l'avertissement.",
        "it": "Confermi innanzitutto di aver letto l'avvertenza.",
        "zh": "请先确认您已阅读该提示。",
    },
    "language_picker_label": {
        "de": "Sprache",
        "en": "Language",
        "es": "Idioma",
        "fr": "Langue",
        "it": "Lingua",
        "zh": "语言",
    },
    # Beschriftung des Fragezeichens, das eine Ausfuellhilfe oeffnet. Steht als
    # aria-label am Schalter, damit Screenreader nicht nur "Fragezeichen" lesen.
    "help_label": {
        "de": "Erläuterung anzeigen",
        "en": "Show explanation",
        "es": "Mostrar explicación",
        "fr": "Afficher l'explication",
        "it": "Mostra la spiegazione",
        "zh": "显示说明",
    },
    # Haftungshinweis in drei Bausteinen: `disclaimer_lead` bleibt sichtbar,
    # `disclaimer_body` und `disclaimer_contact` stehen im aufklappbaren Teil.
    # So verdraengt der lange Text die Anmeldemaske nicht.
    "disclaimer_lead": {
        "de": "Hinweis: Der ESG-Regulierungs-Check dient ausschließlich der ersten Orientierung und gibt auf Grundlage der von Ihnen eingegebenen Unternehmensdaten einen unverbindlichen Überblick über möglicherweise relevante regulatorische Anforderungen.",
        "en": "Note: The ESG Regulation Check serves solely as a first orientation and provides, on the basis of the company data you enter, a non-binding overview of regulatory requirements that may be relevant.",
        "es": "Aviso: la Verificación de Regulaciones ESG sirve exclusivamente como primera orientación y ofrece, a partir de los datos de empresa que usted introduce, una visión general no vinculante de los requisitos regulatorios que podrían ser relevantes.",
        "fr": "Remarque : la Vérification des Réglementations ESG sert uniquement de première orientation et fournit, sur la base des données d'entreprise que vous saisissez, un aperçu non contraignant des exigences réglementaires susceptibles d'être pertinentes.",
        "it": "Nota: la Verifica delle Normative ESG serve esclusivamente come primo orientamento e fornisce, sulla base dei dati aziendali da lei inseriti, una panoramica non vincolante dei requisiti normativi che potrebbero essere rilevanti.",
        "zh": "提示：ESG 法规检查仅用于初步定位，并根据您输入的企业数据，就可能相关的监管要求提供不具约束力的概览。",
    },
    "disclaimer_body": {
        "de": "Die Ergebnisse stellen keine Rechtsberatung dar und ersetzen keine rechtliche oder fachliche Prüfung des Einzelfalls. Trotz sorgfältiger und regelmäßiger Aktualisierung übernimmt textil+mode keine Gewähr für die Vollständigkeit, Richtigkeit und Aktualität der bereitgestellten Informationen.",
        "en": "The results do not constitute legal advice and do not replace a legal or expert examination of the individual case. Despite careful and regular updating, textil+mode accepts no liability for the completeness, accuracy and topicality of the information provided.",
        "es": "Los resultados no constituyen asesoramiento jurídico ni sustituyen un examen jurídico o técnico del caso concreto. Pese a una actualización cuidadosa y periódica, textil+mode no asume garantía alguna por la integridad, exactitud y actualidad de la información facilitada.",
        "fr": "Les résultats ne constituent pas un conseil juridique et ne remplacent pas un examen juridique ou technique du cas d'espèce. Malgré une actualisation soigneuse et régulière, textil+mode n'assume aucune garantie quant à l'exhaustivité, l'exactitude et l'actualité des informations fournies.",
        "it": "I risultati non costituiscono consulenza legale e non sostituiscono un esame giuridico o tecnico del caso concreto. Nonostante un aggiornamento accurato e regolare, textil+mode non fornisce alcuna garanzia circa la completezza, la correttezza e l'attualità delle informazioni messe a disposizione.",
        "zh": "本结果不构成法律咨询，也不能替代对个案的法律或专业审查。尽管进行了细致且定期的更新，textil+mode 对所提供信息的完整性、准确性和时效性不作担保。",
    },
    "disclaimer_contact": {
        "de": "Sie haben Fragen zu einer Regulierung oder möchten die Betroffenheit Ihres Unternehmens vertieft prüfen? Wenden Sie sich gerne an das zuständige Team von textil+mode oder Ihres Mitgliedverbandes.",
        "en": "Do you have questions about a regulation or would you like to examine your company's exposure in more depth? Please contact the responsible team at textil+mode or at your member association.",
        "es": "¿Tiene preguntas sobre una regulación o desea examinar con más detalle la afectación de su empresa? Diríjase al equipo competente de textil+mode o de su asociación miembro.",
        "fr": "Vous avez des questions sur une réglementation ou souhaitez examiner plus en profondeur la situation de votre entreprise ? Adressez-vous à l'équipe compétente de textil+mode ou de votre fédération membre.",
        "it": "Ha domande su una normativa o desidera approfondire il coinvolgimento della sua azienda? Si rivolga al team competente di textil+mode o della sua associazione membro.",
        "zh": "对某项法规有疑问，或希望更深入地评估贵公司的受影响程度？欢迎联系 textil+mode 或贵会员协会的相关团队。",
    },
    # Kurzform fuer die PDF-Fusszeile: dort steht der Hinweis auf JEDER Seite,
    # der vollstaendige Text wuerde den Satzspiegel sprengen.
    "disclaimer_short": {
        "de": "Erstorientierung, keine Rechtsberatung; ohne Gewähr für Vollständigkeit und Aktualität.",
        "en": "First orientation, not legal advice; no warranty as to completeness or topicality.",
        "es": "Primera orientación, no asesoramiento jurídico; sin garantía de integridad ni actualidad.",
        "fr": "Première orientation, pas un conseil juridique ; sans garantie d'exhaustivité ni d'actualité.",
        "it": "Primo orientamento, non consulenza legale; senza garanzia di completezza e attualità.",
        "zh": "初步定位，非法律咨询；不保证完整性与时效性。",
    },
    # Punkt 7 der Vorgabe: Satz am Anfang des PDF.
    "pdf_disclaimer": {
        "de": "Ergebnis dient der Erstorientierung und stellt keine Rechtsberatung dar.",
        "en": "The result serves as a first orientation and does not constitute legal advice.",
        "es": "El resultado sirve de primera orientación y no constituye asesoramiento jurídico.",
        "fr": "Le résultat sert de première orientation et ne constitue pas un conseil juridique.",
        "it": "Il risultato serve da primo orientamento e non costituisce consulenza legale.",
        "zh": "本结果用于初步定位，不构成法律咨询。",
    },
    "disclaimer_more": {
        "de": "Vollständigen Hinweis anzeigen",
        "en": "Show full notice",
        "es": "Mostrar el aviso completo",
        "fr": "Afficher la mention complète",
        "it": "Mostra l'avviso completo",
        "zh": "显示完整提示",
    },
    "created_by": {
        "de": "© 2026 · Alle Rechte vorbehalten",
        "en": "© 2026 · All rights reserved",
        "es": "© 2026 · Todos los derechos reservados",
        "fr": "© 2026 · Tous droits réservés",
        "it": "© 2026 · Tutti i diritti riservati",
        "zh": "© 2026 · 版权所有",
    },
    "footer_privacy": {
        "de": "Datenschutz",
        "en": "Privacy",
        "es": "Protección de datos",
        "fr": "Protection des données",
        "it": "Privacy",
        "zh": "数据保护",
    },
    "footer_imprint": {
        "de": "Impressum",
        "en": "Imprint",
        "es": "Aviso legal",
        "fr": "Mentions légales",
        "it": "Note legali",
        "zh": "版本说明",
    },
    "account_delete_title": {
        "de": "Konto löschen",
        "en": "Delete account",
        "es": "Eliminar la cuenta",
        "fr": "Supprimer le compte",
        "it": "Eliminare l'account",
        "zh": "删除账户",
    },
    "account_delete_hint": {
        "de": "Gelöscht werden Ihr Zugang, sämtliche Unternehmensangaben und alle gespeicherten Prüfergebnisse. Das lässt sich nicht rückgängig machen.",
        "en": "This deletes your login, all company details and every stored check result. It cannot be undone.",
        "es": "Se eliminarán su acceso, todos los datos de la empresa y todos los resultados guardados. No se puede deshacer.",
        "fr": "Cela supprime votre accès, toutes les données de l'entreprise et tous les résultats enregistrés. L'opération est irréversible.",
        "it": "Vengono eliminati il suo accesso, tutti i dati aziendali e tutti i risultati salvati. L'operazione è irreversibile.",
        "zh": "将删除您的登录账户、全部企业信息以及所有已保存的检查结果。此操作无法撤销。",
    },
    "account_delete_password": {
        "de": "Zur Bestätigung Ihr Passwort",
        "en": "Your password, to confirm",
        "es": "Su contraseña, para confirmar",
        "fr": "Votre mot de passe, pour confirmer",
        "it": "La sua password, per conferma",
        "zh": "请输入密码以确认",
    },
    "account_delete_confirm": {
        "de": "Konto endgültig löschen? Alle Angaben und Ergebnisse gehen verloren.",
        "en": "Delete the account for good? All details and results will be lost.",
        "es": "¿Eliminar la cuenta definitivamente? Se perderán todos los datos y resultados.",
        "fr": "Supprimer définitivement le compte ? Toutes les données et tous les résultats seront perdus.",
        "it": "Eliminare definitivamente l'account? Tutti i dati e i risultati andranno persi.",
        "zh": "确定要永久删除账户吗？所有信息和结果都将丢失。",
    },
    "btn_account_delete": {
        "de": "Konto löschen",
        "en": "Delete account",
        "es": "Eliminar la cuenta",
        "fr": "Supprimer le compte",
        "it": "Elimina account",
        "zh": "删除账户",
    },
    "ok_account_deleted": {
        "de": "Ihr Konto und alle dazugehörigen Daten wurden gelöscht.",
        "en": "Your account and all associated data have been deleted.",
        "es": "Su cuenta y todos los datos asociados se han eliminado.",
        "fr": "Votre compte et toutes les données associées ont été supprimés.",
        "it": "Il suo account e tutti i dati associati sono stati eliminati.",
        "zh": "您的账户及全部相关数据已被删除。",
    },
    "err_quota": {
        "de": "Sie haben diese Funktion in der letzten Stunde sehr oft genutzt. Bitte versuchen Sie es später noch einmal.",
        "en": "You have used this function very often in the past hour. Please try again later.",
        "es": "Ha utilizado esta función muy a menudo en la última hora. Inténtelo de nuevo más tarde.",
        "fr": "Vous avez utilisé cette fonction très souvent au cours de la dernière heure. Veuillez réessayer plus tard.",
        "it": "Ha utilizzato questa funzione molto spesso nell'ultima ora. Riprovi più tardi.",
        "zh": "您在过去一小时内非常频繁地使用了此功能，请稍后再试。",
    },
    "hinweis_label": {
        "de": "Hinweis",
        "en": "Note",
        "es": "Aviso",
        "fr": "Note",
        "it": "Nota",
        "zh": "说明",
    },
    "hinweis_body": {
        "de": "Die Prüfergebnisse werden von einer künstlichen Intelligenz erzeugt. Sie können unvollständig oder falsch sein; eine Haftung dafür wird nicht übernommen. Diese Projektseite ist mithilfe von Claude Code und OpenAI Codex entstanden.",
        "en": "The check results are generated by an artificial intelligence. They may be incomplete or incorrect; no liability is accepted for them. This project page was created with the help of Claude Code and OpenAI Codex.",
        "es": "Los resultados de la verificación los genera una inteligencia artificial. Pueden ser incompletos o incorrectos; no se asume responsabilidad alguna por ellos. Esta página del proyecto se creó con la ayuda de Claude Code y OpenAI Codex.",
        "fr": "Les résultats de la vérification sont générés par une intelligence artificielle. Ils peuvent être incomplets ou erronés ; aucune responsabilité n'est assumée à cet égard. Cette page de projet a été créée avec l'aide de Claude Code et d'OpenAI Codex.",
        "it": "I risultati della verifica sono generati da un'intelligenza artificiale. Possono essere incompleti o errati; non si assume alcuna responsabilità al riguardo. Questa pagina del progetto è stata realizzata con l'aiuto di Claude Code e OpenAI Codex.",
        "zh": "检查结果由人工智能生成，可能不完整或有误，对此不承担任何责任。本项目页面是在 Claude Code 与 OpenAI Codex 的协助下创建的。",
    },

    # Auth
    "tab_login": {"de": "Anmelden", "en": "Sign in", "es": "Iniciar sesión", "fr": "Connexion", "it": "Accedi", "zh": "登录"},
    "tab_signup": {"de": "Registrieren", "en": "Sign up", "es": "Registrarse", "fr": "Inscription", "it": "Registrati", "zh": "注册"},
    "email": {"de": "E-Mail", "en": "Email", "es": "Correo electrónico", "fr": "E-mail", "it": "E-mail", "zh": "电子邮箱"},
    "password": {"de": "Passwort", "en": "Password", "es": "Contraseña", "fr": "Mot de passe", "it": "Password", "zh": "密码"},
    "password_min": {
        "de": "Passwort (mind. 8 Zeichen)",
        "en": "Password (min. 8 characters)",
        "es": "Contraseña (mín. 8 caracteres)",
        "fr": "Mot de passe (min. 8 caractères)",
        "it": "Password (min. 8 caratteri)",
        "zh": "密码(至少 8 个字符)",
    },
    "password_repeat": {
        "de": "Passwort wiederholen",
        "en": "Repeat password",
        "es": "Repetir contraseña",
        "fr": "Répéter le mot de passe",
        "it": "Ripeti la password",
        "zh": "重复密码",
    },
    "btn_login": {"de": "Anmelden", "en": "Sign in", "es": "Iniciar sesión", "fr": "Se connecter", "it": "Accedi", "zh": "登录"},
    "btn_signup": {"de": "Konto anlegen", "en": "Create account", "es": "Crear cuenta", "fr": "Créer un compte", "it": "Crea account", "zh": "创建账户"},
    "err_login_failed": {
        "de": "Anmeldung nicht möglich. Bitte prüfen Sie E-Mail und Passwort. Nach einer Registrierung ist die Anmeldung erst möglich, wenn Ihr Zugang freigeschaltet ist und Sie ein Passwort festgelegt haben.",
        "en": "Sign-in not possible. Please check your email and password. After registering, you can only sign in once your access has been activated and you have set a password.",
        "es": "No es posible iniciar sesión. Compruebe su correo electrónico y su contraseña. Tras registrarse, solo podrá iniciar sesión cuando su acceso esté activado y haya establecido una contraseña.",
        "fr": "Connexion impossible. Veuillez vérifier votre e-mail et votre mot de passe. Après une inscription, la connexion n'est possible qu'une fois votre accès activé et votre mot de passe défini.",
        "it": "Accesso non possibile. Verifichi e-mail e password. Dopo la registrazione è possibile accedere solo quando il Suo accesso è stato attivato e ha impostato una password.",
        "zh": "无法登录。请检查电子邮件地址和密码。注册后，须待您的访问权限开通并设置密码后方可登录。",
    },
    # Bewusst neutral: sagt nichts darueber aus, ob es das Konto gibt.
    # Zwei Fassungen wegen Singular/Plural — `_locked_message` in app.py waehlt.
    "err_login_locked": {
        "de": "Zu viele fehlgeschlagene Anmeldeversuche. Bitte versuchen Sie es in {minutes} Minuten erneut.",
        "en": "Too many failed sign-in attempts. Please try again in {minutes} minutes.",
        "es": "Demasiados intentos de inicio de sesión fallidos. Vuelva a intentarlo en {minutes} minutos.",
        "fr": "Trop de tentatives de connexion échouées. Veuillez réessayer dans {minutes} minutes.",
        "it": "Troppi tentativi di accesso non riusciti. Riprovi tra {minutes} minuti.",
        "zh": "登录失败次数过多。请在 {minutes} 分钟后重试。",
    },
    "err_login_locked_one": {
        "de": "Zu viele fehlgeschlagene Anmeldeversuche. Bitte versuchen Sie es in einer Minute erneut.",
        "en": "Too many failed sign-in attempts. Please try again in one minute.",
        "es": "Demasiados intentos de inicio de sesión fallidos. Vuelva a intentarlo en un minuto.",
        "fr": "Trop de tentatives de connexion échouées. Veuillez réessayer dans une minute.",
        "it": "Troppi tentativi di accesso non riusciti. Riprovi tra un minuto.",
        "zh": "登录失败次数过多。请在 1 分钟后重试。",
    },
    "err_email_invalid": {
        "de": "Ungültige E-Mail-Adresse.",
        "en": "Invalid email address.",
        "es": "Dirección de correo no válida.",
        "fr": "Adresse e-mail non valide.",
        "it": "Indirizzo e-mail non valido.",
        "zh": "电子邮箱地址无效。",
    },
    "err_pw_short": {
        "de": "Passwort muss mindestens 8 Zeichen haben.",
        "en": "Password must be at least 8 characters.",
        "es": "La contraseña debe tener al menos 8 caracteres.",
        "fr": "Le mot de passe doit comporter au moins 8 caractères.",
        "it": "La password deve contenere almeno 8 caratteri.",
        "zh": "密码至少需要 8 个字符。",
    },
    "err_pw_mismatch": {
        "de": "Passwörter stimmen nicht überein.",
        "en": "Passwords do not match.",
        "es": "Las contraseñas no coinciden.",
        "fr": "Les mots de passe ne correspondent pas.",
        "it": "Le password non corrispondono.",
        "zh": "两次输入的密码不一致。",
    },
    "err_email_exists": {
        "de": "E-Mail bereits registriert.",
        "en": "Email already registered.",
        "es": "Correo ya registrado.",
        "fr": "E-mail déjà enregistré.",
        "it": "E-mail già registrata.",
        "zh": "该邮箱已注册。",
    },
    "ok_account_created": {
        "de": "Konto angelegt.",
        "en": "Account created.",
        "es": "Cuenta creada.",
        "fr": "Compte créé.",
        "it": "Account creato.",
        "zh": "账户已创建。",
    },

    # Passwort aendern / vergessen / zuruecksetzen
    "link_forgot": {
        "de": "Passwort vergessen?",
        "en": "Forgot your password?",
        "es": "¿Olvidó su contraseña?",
        "fr": "Mot de passe oublié ?",
        "it": "Password dimenticata?",
        "zh": "忘记密码?",
    },
    "forgot_title": {
        "de": "Passwort vergessen",
        "en": "Forgot password",
        "es": "Contraseña olvidada",
        "fr": "Mot de passe oublié",
        "it": "Password dimenticata",
        "zh": "忘记密码",
    },
    # Stand 24.09.2026: Die Anwendung verschickt den Link selbst. Der fruehere
    # Text ("Diese Anwendung verschickt keine E-Mails") stimmte nicht mehr.
    # Der Hinweis bleibt, weil er drei Dinge vorab klaert, die sonst niemand
    # weiss: dass eine Mail kommt, wie lange der Link gilt, und dass sie im
    # Spam-Ordner liegen kann. Bewusst neutral formuliert ("Besteht ein
    # Konto") — die Seite darf nicht verraten, welche Adressen es gibt.
    "forgot_hint": {
        "de": ("Geben Sie Ihre E-Mail-Adresse ein. Besteht ein Konto dazu, "
               "erhalten Sie einen Link zum Neusetzen; er gilt 24 Stunden und "
               "lässt sich einmal verwenden. Sehen Sie gegebenenfalls im "
               "Spam-Ordner nach."),
        "en": ("Enter your email address. If an account exists for it, you "
               "will receive a link to set a new password; it is valid for "
               "24 hours and can be used once. Please also check your spam "
               "folder."),
        "es": ("Introduzca su dirección de correo electrónico. Si existe una "
               "cuenta asociada, recibirá un enlace para establecer una nueva "
               "contraseña; es válido 24 horas y solo puede utilizarse una "
               "vez. Consulte también la carpeta de correo no deseado."),
        "fr": ("Saisissez votre adresse e-mail. Si un compte y est associé, "
               "vous recevrez un lien pour définir un nouveau mot de passe ; "
               "il est valable 24 heures et ne peut être utilisé qu'une fois. "
               "Pensez à vérifier votre dossier de courrier indésirable."),
        "it": ("Inserisca il Suo indirizzo e-mail. Se esiste un account "
               "corrispondente, riceverà un collegamento per impostare una "
               "nuova password; è valido 24 ore e può essere utilizzato una "
               "sola volta. Controlli eventualmente la cartella spam."),
        "zh": ("请输入您的邮箱地址。如果该邮箱已注册账户，您将收到一个重设密码的链接；"
               "链接有效期为 24 小时，且只能使用一次。请注意查看垃圾邮件文件夹。"),
    },
    "btn_forgot": {
        "de": "Anfrage senden",
        "en": "Send request",
        "es": "Enviar solicitud",
        "fr": "Envoyer la demande",
        "it": "Invia richiesta",
        "zh": "发送请求",
    },
    "ok_reset_requested": {
        "de": "Anfrage ist eingegangen. Die Administration meldet sich bei Ihnen.",
        "en": "Request received. The administrator will get in touch with you.",
        "es": "Solicitud recibida. El administrador se pondrá en contacto con usted.",
        "fr": "Demande reçue. L'administrateur vous contactera.",
        "it": "Richiesta ricevuta. L'amministratore la contatterà.",
        "zh": "已收到请求。管理员将与您联系。",
    },
    # Gilt, sobald der SMTP-Zugang konfiguriert ist. Die Formulierung nennt bewusst
    # keine Tatsache ueber das Konto („Besteht ein Konto …"), damit die Seite
    # fuer bekannte und unbekannte Adressen dieselbe Auskunft gibt.
    "ok_reset_mail_sent": {
        "de": "Anfrage ist eingegangen. Besteht ein Konto zu dieser Adresse, erhalten Sie in Kürze eine E-Mail mit einem Link zum Zurücksetzen.",
        "en": "Request received. If an account exists for this address, you will shortly receive an email containing a reset link.",
        "es": "Solicitud recibida. Si existe una cuenta para esta dirección, recibirá en breve un correo electrónico con un enlace de restablecimiento.",
        "fr": "Demande reçue. Si un compte existe pour cette adresse, vous recevrez sous peu un courriel contenant un lien de réinitialisation.",
        "it": "Richiesta ricevuta. Se esiste un account per questo indirizzo, riceverà a breve un'e-mail con un collegamento per la reimpostazione.",
        "zh": "已收到请求。如果该地址存在账户，您很快会收到一封含重置链接的电子邮件。",
    },
    "err_reset_throttled": {
        "de": "Es wurden zu viele Anfragen gestellt. Bitte versuchen Sie es in einer Stunde erneut.",
        "en": "Too many requests have been made. Please try again in an hour.",
        "es": "Se han realizado demasiadas solicitudes. Vuelva a intentarlo en una hora.",
        "fr": "Trop de demandes ont été envoyées. Veuillez réessayer dans une heure.",
        "it": "Sono state inviate troppe richieste. La preghiamo di riprovare tra un'ora.",
        "zh": "请求次数过多。请在一小时后重试。",
    },
    # ---- Text der Reset-Mail (reiner Text, kein HTML, keine Emojis) ----
    # `{link}` wird zur Laufzeit ersetzt; der Platzhalter muss in jeder
    # Sprache genau einmal vorkommen.
    # --- Passwort vergessen: Zahlencode statt Link ----------------------
    # Eine Mail mit Einmal-Link und Zufallstoken sieht fuer Phishing-Filter
    # aus wie ein Angriff. Microsoft 365 hat genau solche Nachrichten am
    # 24.09.2026 stillschweigend aussortiert: Brevo meldete zugestellt, im
    # Postfach kamen sie nie an, auch nicht im Junk-Ordner. Eine Mail mit
    # blosser Zahl passiert die Filter.
    "mail_code_subject": {
        "de": "ESG-Regulierungs-Check: Ihr Code zum Zurücksetzen",
        "en": "ESG Regulation Check: your password reset code",
        "es": "Verificación de Regulaciones ESG: su código de restablecimiento",
        "fr": "Vérification des Réglementations ESG : votre code de réinitialisation",
        "it": "Verifica delle Normative ESG: il Suo codice di reimpostazione",
        "zh": "ESG 法规检查：您的重设密码代码",
    },
    "mail_code_body": {
        "de": (
            "Guten Tag,\n\n"
            "für Ihr Konto beim ESG-Regulierungs-Check wurde ein neues Passwort "
            "angefordert. Ihr Code lautet:\n\n"
            "    {code}\n\n"
            "Geben Sie ihn auf der Seite ein, auf der Sie die Anfrage gestellt "
            "haben. Der Code gilt {minuten} Minuten und lässt sich nur einmal "
            "verwenden.\n\n"
            "Wenn Sie diese Anfrage nicht gestellt haben, können Sie die Nachricht "
            "ignorieren. Ihr Passwort bleibt dann unverändert.\n\n"
            "Mit freundlichen Grüßen\n"
            "ESG-Regulierungs-Check"
        ),
        "en": (
            "Hello,\n\n"
            "A new password has been requested for your ESG Regulation Check "
            "account. Your code is:\n\n"
            "    {code}\n\n"
            "Enter it on the page where you made the request. The code is valid "
            "for {minuten} minutes and can only be used once.\n\n"
            "If you did not make this request, you can ignore this message. "
            "Your password will remain unchanged.\n\n"
            "Kind regards\n"
            "ESG Regulation Check"
        ),
        "es": (
            "Buenos días:\n\n"
            "Se ha solicitado una nueva contraseña para su cuenta de la "
            "Verificación de Regulaciones ESG. Su código es:\n\n"
            "    {code}\n\n"
            "Introdúzcalo en la página desde la que realizó la solicitud. El "
            "código es válido durante {minuten} minutos y solo puede utilizarse "
            "una vez.\n\n"
            "Si usted no ha realizado esta solicitud, puede ignorar este "
            "mensaje. Su contraseña permanecerá sin cambios.\n\n"
            "Atentamente,\n"
            "Verificación de Regulaciones ESG"
        ),
        "fr": (
            "Bonjour,\n\n"
            "Un nouveau mot de passe a été demandé pour votre compte de la "
            "Vérification des Réglementations ESG. Votre code est :\n\n"
            "    {code}\n\n"
            "Saisissez-le sur la page depuis laquelle vous avez fait la demande. "
            "Le code est valable {minuten} minutes et ne peut être utilisé "
            "qu'une seule fois.\n\n"
            "Si vous n'êtes pas à l'origine de cette demande, vous pouvez "
            "ignorer ce message. Votre mot de passe restera inchangé.\n\n"
            "Cordialement,\n"
            "Vérification des Réglementations ESG"
        ),
        "it": (
            "Buongiorno,\n\n"
            "È stata richiesta una nuova password per il Suo account della "
            "Verifica delle Normative ESG. Il Suo codice è:\n\n"
            "    {code}\n\n"
            "Lo inserisca nella pagina da cui ha effettuato la richiesta. Il "
            "codice è valido {minuten} minuti e può essere utilizzato una sola "
            "volta.\n\n"
            "Se non ha effettuato questa richiesta, può ignorare il messaggio. "
            "La Sua password rimarrà invariata.\n\n"
            "Cordiali saluti\n"
            "Verifica delle Normative ESG"
        ),
        "zh": (
            "您好：\n\n"
            "有人为您在 ESG 法规检查的账户申请了新密码。您的代码为：\n\n"
            "    {code}\n\n"
            "请在提交申请的页面上输入该代码。代码有效期为 {minuten} 分钟，且只能使用一次。\n\n"
            "如果这不是您本人的申请，可以忽略本邮件，您的密码不会发生变化。\n\n"
            "此致\n"
            "ESG 法规检查"
        ),
    },
    "pw_code_title": {
        "de": "Neues Passwort setzen",
        "en": "Set a new password",
        "es": "Establecer una nueva contraseña",
        "fr": "Définir un nouveau mot de passe",
        "it": "Impostare una nuova password",
        "zh": "设置新密码",
    },
    "pw_code_hint": {
        "de": "Besteht ein Konto zu dieser Adresse, haben wir Ihnen einen sechsstelligen Code geschickt. Er gilt 30 Minuten. Sehen Sie gegebenenfalls im Spam-Ordner nach.",
        "en": "If an account exists for this address, we have sent you a six-digit code. It is valid for 30 minutes. Please also check your spam folder.",
        "es": "Si existe una cuenta para esta dirección, le hemos enviado un código de seis dígitos. Es válido durante 30 minutos. Consulte también la carpeta de correo no deseado.",
        "fr": "Si un compte existe pour cette adresse, nous vous avons envoyé un code à six chiffres. Il est valable 30 minutes. Pensez à vérifier votre dossier de courrier indésirable.",
        "it": "Se esiste un account per questo indirizzo, Le abbiamo inviato un codice di sei cifre. È valido 30 minuti. Controlli eventualmente la cartella spam.",
        "zh": "如果该邮箱已注册账户，我们已向您发送六位数代码，有效期 30 分钟。请注意查看垃圾邮件文件夹。",
    },
    "field_code": {
        "de": "Code aus der E-Mail",
        "en": "Code from the email",
        "es": "Código del correo electrónico",
        "fr": "Code reçu par e-mail",
        "it": "Codice dall'e-mail",
        "zh": "邮件中的代码",
    },
    "err_code_invalid": {
        "de": "Der Code stimmt nicht, ist abgelaufen oder wurde bereits verwendet. Fordern Sie nötigenfalls einen neuen an.",
        "en": "The code is incorrect, has expired or has already been used. Request a new one if needed.",
        "es": "El código no es correcto, ha caducado o ya se ha utilizado. Solicite uno nuevo si es necesario.",
        "fr": "Le code est incorrect, a expiré ou a déjà été utilisé. Demandez-en un nouveau si nécessaire.",
        "it": "Il codice non è corretto, è scaduto o è già stato utilizzato. Se necessario, ne richieda uno nuovo.",
        "zh": "代码错误、已过期或已使用。如有需要，请重新申请。",
    },
    "ok_reset_code_sent": {
        "de": "Anfrage ist eingegangen. Besteht ein Konto zu dieser Adresse, erhalten Sie in Kürze eine E-Mail mit einem Code.",
        "en": "Request received. If an account exists for this address, you will shortly receive an email containing a code.",
        "es": "Solicitud recibida. Si existe una cuenta para esta dirección, recibirá en breve un correo electrónico con un código.",
        "fr": "Demande reçue. Si un compte existe pour cette adresse, vous recevrez sous peu un e-mail contenant un code.",
        "it": "Richiesta ricevuta. Se esiste un account per questo indirizzo, riceverà a breve un'e-mail con un codice.",
        "zh": "申请已收到。如果该邮箱已注册账户，您将很快收到包含代码的邮件。",
    },
    "mail_reset_subject": {
        "de": "ESG-Regulierungs-Check: Passwort zurücksetzen",
        "en": "ESG Regulation Check: reset your password",
        "es": "Verificación de Regulaciones ESG: restablecer la contraseña",
        "fr": "Vérification des Réglementations ESG : réinitialiser le mot de passe",
        "it": "Verifica delle Normative ESG: reimpostare la password",
        "zh": "ESG 法规检查：重置密码",
    },
    "mail_reset_body": {
        "de": (
            "Guten Tag,\n\n"
            "für Ihr Konto beim ESG-Regulierungs-Check wurde ein neues Passwort "
            "angefordert. Über den folgenden Link können Sie es setzen:\n\n"
            "{link}\n\n"
            "Der Link gilt 24 Stunden und lässt sich nur einmal verwenden.\n\n"
            "Wenn Sie diese Anfrage nicht gestellt haben, können Sie die Nachricht "
            "ignorieren. Ihr Passwort bleibt dann unverändert.\n\n"
            "Mit freundlichen Grüßen\n"
            "ESG-Regulierungs-Check"
        ),
        "en": (
            "Hello,\n\n"
            "A new password has been requested for your ESG Regulation Check "
            "account. You can set one using the following link:\n\n"
            "{link}\n\n"
            "The link is valid for 24 hours and can only be used once.\n\n"
            "If you did not make this request, you can ignore this message. "
            "Your password will remain unchanged.\n\n"
            "Kind regards\n"
            "ESG Regulation Check"
        ),
        "es": (
            "Buenos días:\n\n"
            "Se ha solicitado una nueva contraseña para su cuenta de la "
            "Verificación de Regulaciones ESG. Puede establecerla con el "
            "siguiente enlace:\n\n"
            "{link}\n\n"
            "El enlace es válido durante 24 horas y solo puede utilizarse una vez.\n\n"
            "Si usted no ha realizado esta solicitud, puede ignorar este mensaje. "
            "Su contraseña permanecerá sin cambios.\n\n"
            "Atentamente,\n"
            "Verificación de Regulaciones ESG"
        ),
        "fr": (
            "Bonjour,\n\n"
            "Un nouveau mot de passe a été demandé pour votre compte de la "
            "Vérification des Réglementations ESG. Vous pouvez le définir à "
            "l'aide du lien suivant :\n\n"
            "{link}\n\n"
            "Ce lien est valable 24 heures et ne peut être utilisé qu'une seule fois.\n\n"
            "Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer "
            "ce message. Votre mot de passe restera inchangé.\n\n"
            "Cordialement,\n"
            "Vérification des Réglementations ESG"
        ),
        "it": (
            "Buongiorno,\n\n"
            "È stata richiesta una nuova password per il Suo account della "
            "Verifica delle Normative ESG. Può impostarla tramite il seguente "
            "collegamento:\n\n"
            "{link}\n\n"
            "Il collegamento è valido per 24 ore e può essere utilizzato una sola volta.\n\n"
            "Se non ha effettuato questa richiesta, può ignorare il messaggio. "
            "La Sua password rimarrà invariata.\n\n"
            "Cordiali saluti\n"
            "Verifica delle Normative ESG"
        ),
        "zh": (
            "您好：\n\n"
            "有人为您在 ESG 法规检查的账户申请了新密码。您可以通过以下链接设置新密码：\n\n"
            "{link}\n\n"
            "该链接有效期为 24 小时，且只能使用一次。\n\n"
            "如果这不是您本人的申请，可以忽略本邮件，您的密码不会发生变化。\n\n"
            "此致\n"
            "ESG 法规检查"
        ),
    },
    # --- Registrierung: die Antwort ist fuer jede Adresse gleich -----------
    # Frueher stand hier "E-Mail bereits vergeben". Damit liess sich abfragen,
    # welche Mitgliedsunternehmen das Werkzeug nutzen (Befund M1, 24.09.2026).
    # Jetzt sieht der Absender in beiden Faellen dasselbe; was wirklich war,
    # erfaehrt nur der Inhaber der Adresse — per Mail.
    # --- Kontenuebersicht (nur Admin) -------------------------------------
    "admin_accounts_title": {
        "de": "Konten", "en": "Accounts", "es": "Cuentas",
        "fr": "Comptes", "it": "Account", "zh": "账户",
    },
    "admin_accounts_hint": {
        "de": ("Wer das Werkzeug nutzt. Die Registrierung verrät nach außen "
               "bewusst nicht mehr, ob es eine Adresse schon gibt — hier steht "
               "der tatsächliche Bestand."),
        "en": ("Who uses the tool. Registration deliberately no longer reveals "
               "whether an address already exists — this is the actual list."),
        "es": ("Quién utiliza la herramienta. El registro ya no revela "
               "deliberadamente si una dirección existe; esta es la lista real."),
        "fr": ("Qui utilise l'outil. L'inscription ne révèle volontairement "
               "plus si une adresse existe déjà — voici la liste réelle."),
        "it": ("Chi utilizza lo strumento. La registrazione non rivela più "
               "deliberatamente se un indirizzo esiste già: questo è l'elenco "
               "effettivo."),
        "zh": "谁在使用本工具。注册流程有意不再透露邮箱是否已存在，此处为实际名单。",
    },
    "admin_accounts_total": {
        "de": "Konten insgesamt", "en": "Accounts in total",
        "es": "Cuentas en total", "fr": "Comptes au total",
        "it": "Account in totale", "zh": "账户总数",
    },
    "admin_accounts_new30": {
        "de": "davon neu in 30 Tagen", "en": "new within 30 days",
        "es": "nuevas en 30 días", "fr": "nouveaux en 30 jours",
        "it": "nuovi in 30 giorni", "zh": "30 天内新增",
    },
    "admin_accounts_active30": {
        "de": "in 30 Tagen angemeldet", "en": "signed in within 30 days",
        "es": "con sesión en 30 días", "fr": "connectés en 30 jours",
        "it": "con accesso in 30 giorni", "zh": "30 天内登录",
    },
    "admin_accounts_registered": {
        "de": "Registriert", "en": "Registered", "es": "Registro",
        "fr": "Inscription", "it": "Registrazione", "zh": "注册时间",
    },
    "admin_accounts_last_login": {
        "de": "Zuletzt angemeldet", "en": "Last sign-in",
        "es": "Último acceso", "fr": "Dernière connexion",
        "it": "Ultimo accesso", "zh": "最近登录",
    },
    "admin_accounts_company": {
        "de": "Unternehmen (Eigenangabe)", "en": "Company (self-reported)",
        "es": "Empresa (autodeclarada)", "fr": "Entreprise (déclarative)",
        "it": "Azienda (autodichiarata)", "zh": "企业（自行填写）",
    },
    "admin_accounts_checks": {
        "de": "Prüfungen", "en": "Checks", "es": "Comprobaciones",
        "fr": "Vérifications", "it": "Verifiche", "zh": "检查次数",
    },
    "admin_accounts_last_check": {
        "de": "Letzte Prüfung", "en": "Last check", "es": "Última comprobación",
        "fr": "Dernière vérification", "it": "Ultima verifica", "zh": "最近检查",
    },
    "admin_accounts_never": {
        "de": "noch nie", "en": "never", "es": "nunca",
        "fr": "jamais", "it": "mai", "zh": "从未",
    },
    "admin_role_col": {
        "de": "Rolle",
        "en": "Role",
        "es": "Rol",
        "fr": "Rôle",
        "it": "Ruolo",
        "zh": "角色",
    },
    "admin_role_admin": {
        "de": "Admin",
        "en": "Admin",
        "es": "Admin",
        "fr": "Admin",
        "it": "Admin",
        "zh": "管理员",
    },
    "admin_role_fixed": {
        "de": "Admin (fest)",
        "en": "Admin (fixed)",
        "es": "Admin (fijo)",
        "fr": "Admin (fixe)",
        "it": "Admin (fisso)",
        "zh": "管理员（固定）",
    },
    "admin_role_btn_grant": {
        "de": "Zum Admin machen",
        "en": "Make admin",
        "es": "Hacer admin",
        "fr": "Nommer admin",
        "it": "Rendi admin",
        "zh": "设为管理员",
    },
    "admin_role_btn_revoke": {
        "de": "Admin-Recht entziehen",
        "en": "Revoke admin",
        "es": "Retirar admin",
        "fr": "Retirer les droits admin",
        "it": "Revoca admin",
        "zh": "撤销管理员",
    },
    "admin_role_confirm_grant": {
        "de": "Diesem Konto Admin-Rechte geben? Es kann dann Anfragen freischalten und ablehnen, alle Konten und Passwort-Anfragen sehen und Reset-Links für Mitgliederkonten erzeugen.",
        "en": "Give this account admin rights? It can then activate and reject requests, see all accounts and password requests, and create reset links for member accounts.",
        "es": "¿Dar derechos de administración a esta cuenta? Podrá activar y rechazar solicitudes, ver todas las cuentas y solicitudes de contraseña y crear enlaces de restablecimiento para cuentas de miembros.",
        "fr": "Donner les droits d'administration à ce compte ? Il pourra activer et refuser des demandes, voir tous les comptes et demandes de mot de passe et créer des liens de réinitialisation pour les comptes membres.",
        "it": "Concedere i diritti di amministrazione a questo account? Potrà attivare e rifiutare richieste, vedere tutti gli account e le richieste di password e creare link di reimpostazione per gli account dei membri.",
        "zh": "要授予此账户管理员权限吗？该账户将可以开通和拒绝申请、查看所有账户和密码请求，并为成员账户生成重置链接。",
    },
    "admin_role_confirm_revoke": {
        "de": "Diesem Konto die Admin-Rechte entziehen? Das Konto selbst bleibt nutzbar.",
        "en": "Revoke admin rights from this account? The account itself remains usable.",
        "es": "¿Retirar los derechos de administración a esta cuenta? La cuenta sigue siendo utilizable.",
        "fr": "Retirer les droits d'administration de ce compte ? Le compte reste utilisable.",
        "it": "Revocare i diritti di amministrazione a questo account? L'account resta utilizzabile.",
        "zh": "要撤销此账户的管理员权限吗？账户本身仍可使用。",
    },
    "admin_role_hint": {
        "de": "Admins können Zugangsanfragen freischalten und ablehnen, sehen alle Konten, die Passwort-Anfragen und den Regulierungs-Status und erhalten bei jeder neuen Registrierung eine E-Mail. Admin-Rechte vergeben und entziehen kann nur das fest hinterlegte Admin-Konto; die betroffene Person erhält dazu eine E-Mail.",
        "en": "Admins can activate and reject access requests, see all accounts, the password requests and the regulation status, and receive an email for every new registration. Only the fixed admin account can grant and revoke admin rights; the person concerned receives an email about it.",
        "es": "Los administradores pueden activar y rechazar solicitudes de acceso, ver todas las cuentas, las solicitudes de contraseña y el estado de las regulaciones, y reciben un correo con cada nuevo registro. Solo la cuenta de administración fija puede conceder y retirar derechos de administración; la persona afectada recibe un correo.",
        "fr": "Les administrateurs peuvent activer et refuser les demandes d'accès, voir tous les comptes, les demandes de mot de passe et l'état des réglementations, et reçoivent un e-mail à chaque nouvelle inscription. Seul le compte administrateur fixe peut accorder et retirer les droits d'administration ; la personne concernée en est informée par e-mail.",
        "it": "Gli amministratori possono attivare e rifiutare le richieste di accesso, vedere tutti gli account, le richieste di password e lo stato delle normative, e ricevono un'e-mail a ogni nuova registrazione. Solo l'account amministratore fisso può concedere e revocare i diritti di amministrazione; la persona interessata riceve un'e-mail.",
        "zh": "管理员可以开通和拒绝访问申请，查看所有账户、密码请求和法规状态，并在每次新注册时收到电子邮件。只有固定的管理员账户可以授予和撤销管理员权限；相关人员会收到电子邮件通知。",
    },
    "admin_role_granted": {
        "de": "{email} hat jetzt Admin-Rechte.",
        "en": "{email} now has admin rights.",
        "es": "{email} tiene ahora derechos de administración.",
        "fr": "{email} dispose désormais des droits d'administration.",
        "it": "{email} ha ora i diritti di amministrazione.",
        "zh": "{email} 现已拥有管理员权限。",
    },
    "admin_role_revoked": {
        "de": "{email} hat keine Admin-Rechte mehr.",
        "en": "{email} no longer has admin rights.",
        "es": "{email} ya no tiene derechos de administración.",
        "fr": "{email} n'a plus les droits d'administration.",
        "it": "{email} non ha più i diritti di amministrazione.",
        "zh": "{email} 已不再拥有管理员权限。",
    },
    "admin_role_only_owner": {
        "de": "Admin-Rechte vergeben und entziehen kann nur das fest hinterlegte Admin-Konto.",
        "en": "Only the fixed admin account can grant and revoke admin rights.",
        "es": "Solo la cuenta de administración fija puede conceder y retirar derechos de administración.",
        "fr": "Seul le compte administrateur fixe peut accorder et retirer les droits d'administration.",
        "it": "Solo l'account amministratore fisso può concedere e revocare i diritti di amministrazione.",
        "zh": "只有固定的管理员账户可以授予和撤销管理员权限。",
    },
    "admin_role_protected": {
        "de": "Das fest hinterlegte Admin-Konto lässt sich hier nicht ändern.",
        "en": "The fixed admin account cannot be changed here.",
        "es": "La cuenta de administración fija no se puede modificar aquí.",
        "fr": "Le compte administrateur fixe ne peut pas être modifié ici.",
        "it": "L'account amministratore fisso non può essere modificato qui.",
        "zh": "固定的管理员账户无法在此更改。",
    },
    "admin_role_missing": {
        "de": "Dieses Konto gibt es nicht (mehr) oder es ist noch nicht freigeschaltet.",
        "en": "This account does not exist (any more) or has not been activated yet.",
        "es": "Esta cuenta no existe (ya) o aún no está activada.",
        "fr": "Ce compte n'existe pas (ou plus) ou n'est pas encore activé.",
        "it": "Questo account non esiste (più) o non è ancora attivato.",
        "zh": "该账户不存在（或已删除），或尚未开通。",
    },
    "admin_role_reset_blocked": {
        "de": "Für Konten mit Admin-Rechten kann nur das fest hinterlegte Admin-Konto einen Reset-Link erzeugen. Die Person kann „Passwort vergessen“ auf der Anmeldeseite nutzen.",
        "en": "Only the fixed admin account can create a reset link for accounts with admin rights. The person can use “Forgot password” on the sign-in page.",
        "es": "Solo la cuenta de administración fija puede crear un enlace de restablecimiento para cuentas con derechos de administración. La persona puede usar «¿Olvidó su contraseña?» en la página de acceso.",
        "fr": "Seul le compte administrateur fixe peut créer un lien de réinitialisation pour les comptes disposant de droits d'administration. La personne peut utiliser « Mot de passe oublié » sur la page de connexion.",
        "it": "Solo l'account amministratore fisso può creare un link di reimpostazione per gli account con diritti di amministrazione. La persona può usare «Password dimenticata» nella pagina di accesso.",
        "zh": "只有固定的管理员账户可以为拥有管理员权限的账户生成重置链接。对方可以在登录页面使用“忘记密码”。",
    },
    "mail_admin_role_granted_subject": {
        "de": "ESG-Regulierungs-Check: Sie haben jetzt Admin-Rechte",
    },
    "mail_admin_role_granted_body": {
        "de": "Guten Tag,\n\nSie haben im ESG-Regulierungs-Check jetzt Admin-Rechte. Sie können damit Zugangsanfragen freischalten oder ablehnen, sehen alle Konten, die Passwort-Anfragen und den Regulierungs-Status und erhalten bei jeder neuen Registrierung eine E-Mail.\n\nZur Verwaltung (nach der Anmeldung):\n{link}\n\nErteilt von {von} am {zeit} UTC. Wenn Sie damit nicht gerechnet haben, wenden Sie sich bitte an diese Adresse.\n\nMit freundlichen Grüßen\nESG-Regulierungs-Check",
    },
    "mail_admin_role_revoked_subject": {
        "de": "ESG-Regulierungs-Check: Ihre Admin-Rechte wurden entzogen",
    },
    "mail_admin_role_revoked_body": {
        "de": "Guten Tag,\n\nIhre Admin-Rechte im ESG-Regulierungs-Check wurden am {zeit} UTC von {von} entzogen. Ihr Konto bleibt unverändert nutzbar.\n\n{link}\n\nMit freundlichen Grüßen\nESG-Regulierungs-Check",
    },
    "admin_sort_hint": {
        "de": "Nach dieser Spalte sortieren", "en": "Sort by this column",
        "es": "Ordenar por esta columna", "fr": "Trier selon cette colonne",
        "it": "Ordina per questa colonna", "zh": "按此列排序",
    },
    "admin_accounts_unknown": {
        "de": "nicht erfasst", "en": "not recorded", "es": "no registrado",
        "fr": "non enregistré", "it": "non registrato", "zh": "未记录",
    },
    "admin_accounts_unknown_hint": {
        "de": ("„nicht erfasst“ heißt: das Konto besteht seit vor dem "
               "24.09.2026 und hat sich seitdem nicht angemeldet. Der "
               "Zeitpunkt lässt sich nicht nachträglich ermitteln."),
        "en": ("\u201cnot recorded\u201d means the account predates "
               "24 Sept 2026 and has not signed in since. The time cannot be "
               "reconstructed."),
        "es": ("«no registrado» significa que la cuenta es anterior al "
               "24/09/2026 y no ha iniciado sesión desde entonces. El momento "
               "no puede reconstruirse."),
        "fr": ("« non enregistré » signifie que le compte est antérieur au "
               "24/09/2026 et ne s'est pas connecté depuis. La date ne peut "
               "être reconstituée."),
        "it": ("\u201cnon registrato\u201d significa che l'account è "
               "anteriore al 24/09/2026 e non ha effettuato accessi da allora. "
               "Il momento non è ricostruibile."),
        "zh": "“未记录”表示该账户创建于 2026-09-24 之前且此后未登录，时间无法追溯。",
    },
    "admin_accounts_empty": {
        "de": "Es besteht noch kein Konto.", "en": "No account exists yet.",
        "es": "Todavía no hay ninguna cuenta.", "fr": "Aucun compte pour l'instant.",
        "it": "Non esiste ancora alcun account.", "zh": "尚无账户。",
    },
    "ok_signup_check_mail": {
        "de": "Vielen Dank für Ihre Registrierung zum ESG-Regulierungs-Check. Wir prüfen nun Ihre Zugangsberechtigung.\n\nSobald die Prüfung abgeschlossen ist, erhalten Sie eine E-Mail mit den weiteren Schritten. Bis dahin ist eine Anmeldung noch nicht möglich.",
        "en": "Thank you for registering for the ESG Regulation Check. We are now reviewing your eligibility for access.\n\nAs soon as the review is complete, you will receive an email with the next steps. Until then, signing in is not yet possible.",
        "es": "Gracias por registrarse en la Verificación de Regulaciones ESG. Ahora revisaremos su autorización de acceso.\n\nEn cuanto termine la revisión, recibirá un correo electrónico con los siguientes pasos. Hasta entonces todavía no es posible iniciar sesión.",
        "fr": "Merci pour votre inscription à la Vérification des Réglementations ESG. Nous vérifions maintenant votre droit d'accès.\n\nDès que la vérification sera terminée, vous recevrez un e-mail indiquant les prochaines étapes. D'ici là, la connexion n'est pas encore possible.",
        "it": "Grazie per la Sua registrazione alla Verifica delle Normative ESG. Ora verifichiamo la Sua autorizzazione all'accesso.\n\nNon appena la verifica sarà conclusa, riceverà un'e-mail con i passaggi successivi. Fino ad allora non è ancora possibile accedere.",
        "zh": "感谢您注册 ESG 法规检查。我们现在将审核您的访问资格。\n\n审核完成后，您将收到一封电子邮件，告知后续步骤。在此之前暂时无法登录。",
    },
    "err_signup_throttled": {
        "de": ("Es wurden zu viele Konten von dieser Verbindung aus angelegt. "
               "Bitte versuchen Sie es später erneut."),
        "en": ("Too many accounts have been created from this connection. "
               "Please try again later."),
        "es": ("Se han creado demasiadas cuentas desde esta conexión. "
               "Inténtelo de nuevo más tarde."),
        "fr": ("Trop de comptes ont été créés depuis cette connexion. "
               "Veuillez réessayer plus tard."),
        "it": ("Sono stati creati troppi account da questa connessione. "
               "Riprovi più tardi."),
        "zh": "该网络创建的账户过多，请稍后再试。",
    },
    # --- Registrierung als Zugangsanfrage (29.09.2026) ---
    "err_account_pending": {
        "de": "Ihr Zugang ist noch nicht freigeschaltet. Sie erhalten eine E-Mail, sobald die Prüfung abgeschlossen ist.",
        "en": "Your access has not been activated yet. You will receive an email as soon as the review is complete.",
        "es": "Su acceso todavía no está activado. Recibirá un correo electrónico en cuanto termine la revisión.",
        "fr": "Votre accès n'est pas encore activé. Vous recevrez un e-mail dès que la vérification sera terminée.",
        "it": "Il Suo accesso non è ancora stato attivato. Riceverà un'e-mail non appena la verifica sarà conclusa.",
        "zh": "您的访问权限尚未开通。审核完成后，您将收到一封电子邮件。",
    },
    "mail_request_subject": {
        "de": "ESG-Regulierungs-Check: Ihre Registrierung ist eingegangen",
        "en": "ESG Regulation Check: we have received your registration",
        "es": "Verificación de Regulaciones ESG: hemos recibido su registro",
        "fr": "Vérification des Réglementations ESG : nous avons bien reçu votre inscription",
        "it": "Verifica delle Normative ESG: abbiamo ricevuto la Sua registrazione",
        "zh": "ESG 法规检查：我们已收到您的注册",
    },
    "mail_request_body": {
        "de": "Guten Tag,\n\nvielen Dank für Ihre Registrierung zum ESG-Regulierungs-Check. Wir prüfen sie und schicken Ihnen eine weitere E-Mail, sobald Ihr Zugang freigeschaltet ist. Bis dahin ist eine Anmeldung noch nicht möglich.\n\nWenn Sie sich nicht registriert haben, können Sie die Nachricht ignorieren.\n\nMit freundlichen Grüßen\nESG-Regulierungs-Check",
        "en": "Hello,\n\nThank you for registering for the ESG Regulation Check. We will review your registration and send you another email as soon as your access has been activated. Until then, signing in is not yet possible.\n\nIf you did not register, you can ignore this message.\n\nKind regards\nESG Regulation Check",
        "es": "Buenos días:\n\nGracias por su registro en la Verificación de Regulaciones ESG. Lo revisaremos y le enviaremos otro correo en cuanto su acceso esté activado. Hasta entonces todavía no es posible iniciar sesión.\n\nSi usted no se ha registrado, puede ignorar este mensaje.\n\nAtentamente,\nVerificación de Regulaciones ESG",
        "fr": "Bonjour,\n\nMerci pour votre inscription à la Vérification des Réglementations ESG. Nous allons l'examiner et vous enverrons un nouvel e-mail dès que votre accès sera activé. D'ici là, la connexion n'est pas encore possible.\n\nSi vous ne vous êtes pas inscrit, vous pouvez ignorer ce message.\n\nCordialement,\nVérification des Réglementations ESG",
        "it": "Buongiorno,\n\ngrazie per la Sua registrazione alla Verifica delle Normative ESG. La esamineremo e Le invieremo un'altra e-mail non appena il Suo accesso sarà attivato. Fino ad allora non è ancora possibile accedere.\n\nSe non si è registrato, può ignorare il messaggio.\n\nCordiali saluti\nVerifica delle Normative ESG",
        "zh": "您好：\n\n感谢您注册 ESG 法规检查。我们将进行审核，并在您的访问权限开通后再给您发送一封电子邮件。在此之前暂时无法登录。\n\n如果这不是您本人的注册，可以忽略本邮件。\n\n此致\nESG 法规检查",
    },
    "mail_admin_request_subject": {
        "de": "ESG-Regulierungs-Check: Neue Zugangsanfrage",
    },
    "mail_admin_request_body": {
        "de": "Neue Zugangsanfrage von {email} ({zeit} UTC).\n\nFreischalten oder ablehnen:\n{link}\n\nErst mit der Freischaltung erhält die Person den Anmeldelink.",
    },
    "admin_pending_title": {
        "de": "Offene Zugangsanfragen",
        "en": "Open access requests",
        "es": "Solicitudes de acceso pendientes",
        "fr": "Demandes d'accès en attente",
        "it": "Richieste di accesso in sospeso",
        "zh": "待处理的访问申请",
    },
    "admin_pending_hint": {
        "de": "Neue Registrierungen bleiben gesperrt, bis sie hier freigeschaltet werden. Beim Freischalten erhält die Person eine E-Mail mit einem Code, mit dem sie ihr Passwort festlegt (7 Tage gültig). Beim Ablehnen wird die Anfrage samt Daten gelöscht, ohne Nachricht an die Person. Unbearbeitete Anfragen werden nach 30 Tagen automatisch gelöscht.",
        "en": "New registrations stay locked until they are activated here. On activation, the person receives an email with a code to set their password (valid for 7 days). On rejection, the request and its data are deleted without notifying the person. Unprocessed requests are deleted automatically after 30 days.",
        "es": "Los nuevos registros permanecen bloqueados hasta que se activan aquí. Al activarlos, la persona recibe un correo con un código para establecer su contraseña (válido 7 días). Al rechazarlos, la solicitud y sus datos se eliminan sin avisar a la persona. Las solicitudes sin tramitar se eliminan automáticamente a los 30 días.",
        "fr": "Les nouvelles inscriptions restent bloquées jusqu'à leur activation ici. Lors de l'activation, la personne reçoit un e-mail avec un code pour définir son mot de passe (valable 7 jours). En cas de refus, la demande et ses données sont supprimées sans que la personne soit avertie. Les demandes non traitées sont supprimées automatiquement après 30 jours.",
        "it": "Le nuove registrazioni restano bloccate finché non vengono attivate qui. Con l'attivazione la persona riceve un'e-mail con un codice per impostare la password (valido 7 giorni). In caso di rifiuto la richiesta e i relativi dati vengono eliminati senza avvisare la persona. Le richieste non evase vengono eliminate automaticamente dopo 30 giorni.",
        "zh": "新注册在此处开通前将保持锁定。开通后，对方会收到一封包含验证码的电子邮件，用于设置密码（有效期 7 天）。拒绝时，申请及相关数据将被删除，且不会通知对方。未处理的申请将在 30 天后自动删除。",
    },
    "admin_pending_empty": {
        "de": "Keine offenen Anfragen.",
        "en": "No open requests.",
        "es": "No hay solicitudes pendientes.",
        "fr": "Aucune demande en attente.",
        "it": "Nessuna richiesta in sospeso.",
        "zh": "没有待处理的申请。",
    },
    "admin_pending_requested": {
        "de": "Angefragt",
        "en": "Requested",
        "es": "Solicitado",
        "fr": "Demandé le",
        "it": "Richiesto il",
        "zh": "申请时间",
    },
    "admin_btn_approve": {
        "de": "Freischalten",
        "en": "Activate",
        "es": "Activar",
        "fr": "Activer",
        "it": "Attiva",
        "zh": "开通",
    },
    "admin_btn_reject": {
        "de": "Ablehnen",
        "en": "Reject",
        "es": "Rechazar",
        "fr": "Refuser",
        "it": "Rifiuta",
        "zh": "拒绝",
    },
    "admin_reject_confirm": {
        "de": "Anfrage ablehnen und samt Daten löschen? Die Person erhält keine Nachricht.",
        "en": "Reject the request and delete its data? The person will not be notified.",
        "es": "¿Rechazar la solicitud y eliminar sus datos? La persona no recibirá ningún aviso.",
        "fr": "Refuser la demande et supprimer ses données ? La personne ne sera pas avertie.",
        "it": "Rifiutare la richiesta ed eliminarne i dati? La persona non riceverà alcun avviso.",
        "zh": "确定拒绝该申请并删除相关数据吗？对方不会收到任何通知。",
    },
    "admin_approved_ok": {
        "de": "{email} ist freigeschaltet und erhält per E-Mail den Code zum Festlegen des Passworts.",
        "en": "{email} has been activated and receives the code for setting the password by email.",
        "es": "{email} está activado y recibe por correo el código para establecer la contraseña.",
        "fr": "{email} est activé et reçoit par e-mail le code pour définir son mot de passe.",
        "it": "{email} è stato attivato e riceve via e-mail il codice per impostare la password.",
        "zh": "{email} 已开通，设置密码的验证码将通过电子邮件发送。",
    },
    "admin_approved_nomail": {
        "de": "{email} ist freigeschaltet. Der Mailversand ist nicht eingerichtet: bitte unter „Passwort-Resets“ einen Link erzeugen und der Person selbst geben.",
        "en": "{email} has been activated. Email sending is not set up: please create a link under “Password resets” and pass it to the person yourself.",
        "es": "{email} está activado. El envío de correos no está configurado: cree un enlace en «Restablecimientos de contraseña» y entrégueselo usted mismo a la persona.",
        "fr": "{email} est activé. L'envoi d'e-mails n'est pas configuré : veuillez créer un lien sous « Réinitialisations de mot de passe » et le transmettre vous-même à la personne.",
        "it": "{email} è stato attivato. L'invio di e-mail non è configurato: crei un link in «Reimpostazioni password» e lo consegni Lei stesso alla persona.",
        "zh": "{email} 已开通。邮件发送尚未配置：请在“密码重置”中生成链接并自行转交对方。",
    },
    "admin_rejected_ok": {
        "de": "Die Anfrage von {email} ist gelöscht.",
        "en": "The request from {email} has been deleted.",
        "es": "La solicitud de {email} se ha eliminado.",
        "fr": "La demande de {email} a été supprimée.",
        "it": "La richiesta di {email} è stata eliminata.",
        "zh": "{email} 的申请已删除。",
    },
    "admin_pending_missing": {
        "de": "Diese Anfrage ist nicht mehr offen.",
        "en": "This request is no longer open.",
        "es": "Esta solicitud ya no está pendiente.",
        "fr": "Cette demande n'est plus en attente.",
        "it": "Questa richiesta non è più in sospeso.",
        "zh": "该申请已不再处于待处理状态。",
    },
    "signup_hint": {
        "de": "Ein Passwort legen Sie erst nach der Freischaltung fest: Sie erhalten dann eine E-Mail mit einem Code.",
        "en": "You set a password only after your access has been activated: you will then receive an email with a code.",
        "es": "La contraseña se establece después de la activación: recibirá entonces un correo con un código.",
        "fr": "Vous définissez votre mot de passe après l'activation : vous recevrez alors un e-mail contenant un code.",
        "it": "La password si imposta solo dopo l'attivazione: riceverà allora un'e-mail con un codice.",
        "zh": "密码在访问权限开通后再设置：届时您会收到一封包含验证码的电子邮件。",
    },
    "mail_signup_subject": {
        "de": "ESG-Regulierungs-Check: Ihr Zugang ist freigeschaltet",
        "en": "ESG Regulation Check: your access has been activated",
        "es": "Verificación de Regulaciones ESG: su acceso está activado",
        "fr": "Vérification des Réglementations ESG : votre accès est activé",
        "it": "Verifica delle Normative ESG: il Suo accesso è stato attivato",
        "zh": "ESG 法规检查：您的访问权限已开通",
    },
    "mail_signup_body": {
        "de": "Guten Tag,\n\nIhr Zugang zum ESG-Regulierungs-Check ist freigeschaltet. Legen Sie jetzt Ihr Passwort fest. Ihr Code lautet:\n\n{code}\n\nGeben Sie ihn zusammen mit Ihrer E-Mail-Adresse und dem gewünschten Passwort hier ein:\n\n{link}\n\nDer Code gilt {tage} Tage. Ist er abgelaufen, fordern Sie auf der Anmeldeseite über „Passwort vergessen“ einen neuen an.\n\nWenn Sie sich nicht registriert haben, können Sie die Nachricht ignorieren.\n\nMit freundlichen Grüßen\nESG-Regulierungs-Check",
        "en": "Hello,\n\nYour access to the ESG Regulation Check has been activated. Please set your password now. Your code is:\n\n{code}\n\nEnter it together with your email address and the password you want here:\n\n{link}\n\nThe code is valid for {tage} days. If it has expired, request a new one on the sign-in page via “Forgot password”.\n\nIf you did not register, you can ignore this message.\n\nKind regards\nESG Regulation Check",
        "es": "Buenos días:\n\nSu acceso a la Verificación de Regulaciones ESG está activado. Establezca ahora su contraseña. Su código es:\n\n{code}\n\nIntrodúzcalo junto con su dirección de correo y la contraseña que desee aquí:\n\n{link}\n\nEl código es válido durante {tage} días. Si ha caducado, solicite uno nuevo en la página de acceso mediante «¿Olvidó su contraseña?».\n\nSi usted no se ha registrado, puede ignorar este mensaje.\n\nAtentamente,\nVerificación de Regulaciones ESG",
        "fr": "Bonjour,\n\nVotre accès à la Vérification des Réglementations ESG est activé. Définissez maintenant votre mot de passe. Votre code est :\n\n{code}\n\nSaisissez-le ici avec votre adresse e-mail et le mot de passe souhaité :\n\n{link}\n\nLe code est valable {tage} jours. S'il a expiré, demandez-en un nouveau sur la page de connexion via « Mot de passe oublié ».\n\nSi vous ne vous êtes pas inscrit, vous pouvez ignorer ce message.\n\nCordialement,\nVérification des Réglementations ESG",
        "it": "Buongiorno,\n\nil Suo accesso alla Verifica delle Normative ESG è stato attivato. Imposti ora la Sua password. Il Suo codice è:\n\n{code}\n\nLo inserisca qui insieme al Suo indirizzo e-mail e alla password desiderata:\n\n{link}\n\nIl codice è valido per {tage} giorni. Se è scaduto, ne richieda uno nuovo nella pagina di accesso tramite «Password dimenticata».\n\nSe non si è registrato, può ignorare il messaggio.\n\nCordiali saluti\nVerifica delle Normative ESG",
        "zh": "您好：\n\n您的 ESG 法规检查访问权限已开通，请现在设置密码。您的验证码是：\n\n{code}\n\n请在以下页面输入该验证码、您的电子邮件地址和想要设置的密码：\n\n{link}\n\n验证码有效期为 {tage} 天。如已过期，请在登录页面通过“忘记密码”重新申请。\n\n如果这不是您本人的注册，可以忽略本邮件。\n\n此致\nESG 法规检查",
    },
    # Antwort auf eine Registrierung mit bereits vergebener Adresse. Sie geht
    # an den Inhaber, nicht an den Absender des Formulars — deshalb darf sie
    # sagen, was Sache ist.
    "mail_exists_subject": {
        "de": "ESG-Regulierungs-Check: Es besteht bereits ein Konto",
        "en": "ESG Regulation Check: an account already exists",
        "es": "Verificación de Regulaciones ESG: ya existe una cuenta",
        "fr": "Vérification des Réglementations ESG : un compte existe déjà",
        "it": "Verifica delle Normative ESG: esiste già un account",
        "zh": "ESG 法规检查：账户已存在",
    },
    "mail_exists_body": {
        "de": (
            "Guten Tag,\n\n"
            "für diese Adresse wurde ein Konto beim ESG-Regulierungs-Check "
            "angefordert — es besteht aber bereits eines. Sie können sich "
            "wie gewohnt anmelden:\n\n"
            "{link}\n\n"
            "Falls Sie Ihr Passwort nicht mehr wissen, nutzen Sie dort "
            "„Passwort vergessen“.\n\n"
            "Wenn Sie das nicht waren, ist nichts geschehen: Es wurde kein "
            "neues Konto angelegt und Ihr Passwort ist unverändert.\n\n"
            "Mit freundlichen Grüßen\n"
            "ESG-Regulierungs-Check"
        ),
        "en": (
            "Hello,\n\n"
            "Someone requested an ESG Regulation Check account for this "
            "address, but one already exists. You can sign in as usual:\n\n"
            "{link}\n\n"
            "If you have forgotten your password, use “Forgot password” there.\n\n"
            "If this was not you, nothing has happened: no new account was "
            "created and your password is unchanged.\n\n"
            "Kind regards\n"
            "ESG Regulation Check"
        ),
        "es": (
            "Buenos días:\n\n"
            "Se ha solicitado una cuenta de la Verificación de Regulaciones ESG "
            "para esta dirección, pero ya existe una. Puede iniciar sesión como "
            "de costumbre:\n\n"
            "{link}\n\n"
            "Si ha olvidado su contraseña, utilice allí «¿Ha olvidado su "
            "contraseña?».\n\n"
            "Si no ha sido usted, no ha ocurrido nada: no se ha creado ninguna "
            "cuenta nueva y su contraseña no ha cambiado.\n\n"
            "Atentamente,\n"
            "Verificación de Regulaciones ESG"
        ),
        "fr": (
            "Bonjour,\n\n"
            "Un compte de la Vérification des Réglementations ESG a été demandé "
            "pour cette adresse, mais il en existe déjà un. Vous pouvez vous "
            "connecter comme d'habitude :\n\n"
            "{link}\n\n"
            "Si vous avez oublié votre mot de passe, utilisez « Mot de passe "
            "oublié ».\n\n"
            "Si vous n'êtes pas à l'origine de cette demande, rien ne s'est "
            "passé : aucun nouveau compte n'a été créé et votre mot de passe "
            "reste inchangé.\n\n"
            "Cordialement,\n"
            "Vérification des Réglementations ESG"
        ),
        "it": (
            "Buongiorno,\n\n"
            "È stato richiesto un account della Verifica delle Normative ESG "
            "per questo indirizzo, ma ne esiste già uno. Può accedere come di "
            "consueto:\n\n"
            "{link}\n\n"
            "Se ha dimenticato la password, utilizzi “Password dimenticata”.\n\n"
            "Se non è stato Lei, non è successo nulla: non è stato creato "
            "alcun nuovo account e la Sua password è invariata.\n\n"
            "Cordiali saluti\n"
            "Verifica delle Normative ESG"
        ),
        "zh": (
            "您好：\n\n"
            "有人为此邮箱申请注册 ESG 法规检查账户，但该邮箱已有账户。您可以照常登录：\n\n"
            "{link}\n\n"
            "如果忘记密码，请在登录页面使用“忘记密码”。\n\n"
            "如果这不是您本人的操作，则无需担心：系统没有创建新账户，您的密码也没有变化。\n\n"
            "此致\n"
            "ESG 法规检查"
        ),
    },
    # Nach jeder Passwortaenderung. Eine stille Kontouebernahme faellt sonst
    # erst beim naechsten Anmeldeversuch auf (Befund M3, 24.09.2026).
    "mail_pw_changed_subject": {
        "de": "ESG-Regulierungs-Check: Ihr Passwort wurde geändert",
        "en": "ESG Regulation Check: your password was changed",
        "es": "Verificación de Regulaciones ESG: su contraseña ha cambiado",
        "fr": "Vérification des Réglementations ESG : votre mot de passe a été modifié",
        "it": "Verifica delle Normative ESG: la Sua password è stata modificata",
        "zh": "ESG 法规检查：您的密码已更改",
    },
    "mail_pw_changed_body": {
        "de": (
            "Guten Tag,\n\n"
            "das Passwort Ihres Kontos beim ESG-Regulierungs-Check wurde "
            "soeben geändert.\n\n"
            "Wenn Sie das selbst waren, ist nichts weiter zu tun.\n\n"
            "Wenn nicht, fordern Sie über den folgenden Link umgehend ein "
            "neues Passwort an und wenden Sie sich an uns:\n\n"
            "{link}\n\n"
            "Mit freundlichen Grüßen\n"
            "ESG-Regulierungs-Check"
        ),
        "en": (
            "Hello,\n\n"
            "The password for your ESG Regulation Check account has just been "
            "changed.\n\n"
            "If this was you, there is nothing further to do.\n\n"
            "If it was not, use the following link to request a new password "
            "immediately, and contact us:\n\n"
            "{link}\n\n"
            "Kind regards\n"
            "ESG Regulation Check"
        ),
        "es": (
            "Buenos días:\n\n"
            "La contraseña de su cuenta de la Verificación de Regulaciones ESG "
            "acaba de cambiarse.\n\n"
            "Si ha sido usted, no tiene que hacer nada más.\n\n"
            "Si no ha sido usted, solicite de inmediato una nueva contraseña "
            "a través del siguiente enlace y póngase en contacto con nosotros:\n\n"
            "{link}\n\n"
            "Atentamente,\n"
            "Verificación de Regulaciones ESG"
        ),
        "fr": (
            "Bonjour,\n\n"
            "Le mot de passe de votre compte de la Vérification des "
            "Réglementations ESG vient d'être modifié.\n\n"
            "Si vous êtes à l'origine de cette modification, il n'y a rien "
            "d'autre à faire.\n\n"
            "Dans le cas contraire, demandez immédiatement un nouveau mot de "
            "passe via le lien suivant et contactez-nous :\n\n"
            "{link}\n\n"
            "Cordialement,\n"
            "Vérification des Réglementations ESG"
        ),
        "it": (
            "Buongiorno,\n\n"
            "La password del Suo account della Verifica delle Normative ESG è "
            "stata appena modificata.\n\n"
            "Se è stato Lei, non deve fare altro.\n\n"
            "In caso contrario, richieda subito una nuova password tramite il "
            "seguente collegamento e ci contatti:\n\n"
            "{link}\n\n"
            "Cordiali saluti\n"
            "Verifica delle Normative ESG"
        ),
        "zh": (
            "您好：\n\n"
            "您在 ESG 法规检查账户的密码刚刚被更改。\n\n"
            "如果是您本人操作，则无需进一步处理。\n\n"
            "如果不是，请通过以下链接立即申请新密码，并与我们联系：\n\n"
            "{link}\n\n"
            "此致\n"
            "ESG 法规检查"
        ),
    },
    "pw_change_title": {
        "de": "Passwort ändern",
        "en": "Change password",
        "es": "Cambiar contraseña",
        "fr": "Changer le mot de passe",
        "it": "Cambia password",
        "zh": "修改密码",
    },
    "pw_current": {
        "de": "Aktuelles Passwort",
        "en": "Current password",
        "es": "Contraseña actual",
        "fr": "Mot de passe actuel",
        "it": "Password attuale",
        "zh": "当前密码",
    },
    "btn_pw_save": {
        "de": "Passwort speichern",
        "en": "Save password",
        "es": "Guardar contraseña",
        "fr": "Enregistrer le mot de passe",
        "it": "Salva password",
        "zh": "保存密码",
    },
    "err_pw_current_wrong": {
        "de": "Das aktuelle Passwort stimmt nicht.",
        "en": "The current password is not correct.",
        "es": "La contraseña actual no es correcta.",
        "fr": "Le mot de passe actuel est incorrect.",
        "it": "La password attuale non è corretta.",
        "zh": "当前密码不正确。",
    },
    "ok_pw_changed": {
        "de": "Passwort geändert.",
        "en": "Password changed.",
        "es": "Contraseña cambiada.",
        "fr": "Mot de passe modifié.",
        "it": "Password modificata.",
        "zh": "密码已修改。",
    },
    "pw_reset_title": {
        "de": "Neues Passwort setzen",
        "en": "Set a new password",
        "es": "Establecer nueva contraseña",
        "fr": "Définir un nouveau mot de passe",
        "it": "Imposta una nuova password",
        "zh": "设置新密码",
    },
    "pw_reset_invalid_title": {
        "de": "Link nicht mehr gültig",
        "en": "Link no longer valid",
        "es": "Enlace ya no válido",
        "fr": "Lien plus valide",
        "it": "Link non più valido",
        "zh": "链接已失效",
    },
    "pw_reset_invalid_text": {
        "de": "Dieser Link wurde bereits benutzt oder ist abgelaufen. Bitte fordern Sie über „Passwort vergessen“ einen neuen an.",
        "en": "This link has already been used or has expired. Please request a new one via “Forgot your password?”.",
        "es": "Este enlace ya se ha utilizado o ha caducado. Solicite uno nuevo mediante «¿Olvidó su contraseña?».",
        "fr": "Ce lien a déjà été utilisé ou a expiré. Veuillez en demander un nouveau via « Mot de passe oublié ? ».",
        "it": "Questo link è già stato usato o è scaduto. Ne richieda uno nuovo tramite «Password dimenticata?».",
        "zh": "该链接已使用或已过期。请通过“忘记密码?”重新申请。",
    },
    "back_to_login": {
        "de": "Zurück zur Anmeldung",
        "en": "Back to sign in",
        "es": "Volver al inicio de sesión",
        "fr": "Retour à la connexion",
        "it": "Torna all'accesso",
        "zh": "返回登录",
    },
    "back_to_dashboard": {
        "de": "Zurück zur Übersicht",
        "en": "Back to overview",
        "es": "Volver al panel",
        "fr": "Retour à l'aperçu",
        "it": "Torna alla panoramica",
        "zh": "返回概览",
    },

    # Admin: Passwort-Resets
    "admin_resets_title": {
        "de": "Passwort-Resets",
        "en": "Password resets",
        "es": "Restablecimientos",
        "fr": "Réinitialisations",
        "it": "Reimpostazioni",
        "zh": "密码重设",
    },
    "admin_resets_hint": {
        "de": "Hier entsteht ein einmaliger Link, der 24 Stunden gilt. Geben Sie ihn der Person über einen anderen Kanal durch — am besten telefonisch, nicht per Mail an dieselbe Adresse.",
        "en": "This creates a one-time link valid for 24 hours. Pass it on through a different channel — by phone rather than to the same mailbox.",
        "es": "Aquí se genera un enlace de un solo uso válido 24 horas. Comuníquelo por otro canal, preferiblemente por teléfono.",
        "fr": "Un lien à usage unique valable 24 heures est créé ici. Transmettez-le par un autre canal, de préférence par téléphone.",
        "it": "Qui viene creato un link monouso valido 24 ore. Lo comunichi tramite un altro canale, preferibilmente per telefono.",
        "zh": "此处生成 24 小时内有效的一次性链接。请通过其他渠道（最好是电话）转达。",
    },
    "admin_btn_issue": {
        "de": "Link erzeugen",
        "en": "Create link",
        "es": "Generar enlace",
        "fr": "Créer un lien",
        "it": "Genera link",
        "zh": "生成链接",
    },
    "admin_link_for": {
        "de": "Link für",
        "en": "Link for",
        "es": "Enlace para",
        "fr": "Lien pour",
        "it": "Link per",
        "zh": "链接用于",
    },
    "admin_link_expires": {
        "de": "Gültig bis",
        "en": "Valid until",
        "es": "Válido hasta",
        "fr": "Valable jusqu'au",
        "it": "Valido fino al",
        "zh": "有效期至",
    },
    "admin_link_once": {
        "de": "nur einmal verwendbar",
        "en": "single use only",
        "es": "de un solo uso",
        "fr": "à usage unique",
        "it": "utilizzabile una sola volta",
        "zh": "仅可使用一次",
    },
    "admin_open_requests": {
        "de": "Offene Anfragen",
        "en": "Open requests",
        "es": "Solicitudes abiertas",
        "fr": "Demandes ouvertes",
        "it": "Richieste aperte",
        "zh": "待处理请求",
    },
    "admin_no_requests": {
        "de": "Keine offenen Anfragen.",
        "en": "No open requests.",
        "es": "No hay solicitudes abiertas.",
        "fr": "Aucune demande ouverte.",
        "it": "Nessuna richiesta aperta.",
        "zh": "没有待处理的请求。",
    },
    "admin_mail_log": {
        "de": "Mailversand",
        "en": "Mail delivery",
        "es": "Envío de correo",
        "fr": "Envoi des courriels",
        "it": "Invio delle e-mail",
        "zh": "邮件发送",
    },
    "admin_mail_none": {
        "de": "Noch kein Versand protokolliert.",
        "en": "No delivery recorded yet.",
        "es": "Aún no se ha registrado ningún envío.",
        "fr": "Aucun envoi enregistré pour l'instant.",
        "it": "Nessun invio registrato finora.",
        "zh": "尚未记录任何发送。",
    },
    "admin_mail_off": {
        "de": "Der automatische Versand ist nicht eingerichtet (SMTP_HOST, SMTP_USER, SMTP_PASSWORD oder MAIL_FROM fehlen). Anfragen landen weiterhin nur als Ticket in der Liste oben.",
        "en": "Automatic delivery is not set up (SMTP_HOST, SMTP_USER, SMTP_PASSWORD or MAIL_FROM are missing). Requests continue to appear only as tickets in the list above.",
        "es": "El envío automático no está configurado (faltan SMTP_HOST, SMTP_USER, SMTP_PASSWORD o MAIL_FROM). Las solicitudes siguen apareciendo solo como tickets en la lista anterior.",
        "fr": "L'envoi automatique n'est pas configuré (SMTP_HOST, SMTP_USER, SMTP_PASSWORD ou MAIL_FROM manquent). Les demandes continuent d'apparaître uniquement dans la liste ci-dessus.",
        "it": "L'invio automatico non è configurato (mancano SMTP_HOST, SMTP_USER, SMTP_PASSWORD o MAIL_FROM). Le richieste continuano a comparire solo nell'elenco qui sopra.",
        "zh": "尚未配置自动发送（缺少 SMTP_HOST、SMTP_USER、SMTP_PASSWORD 或 MAIL_FROM）。请求仍只会出现在上方列表中。",
    },
    "admin_mail_time": {
        "de": "Zeitpunkt",
        "en": "Time",
        "es": "Momento",
        "fr": "Horodatage",
        "it": "Momento",
        "zh": "时间",
    },
    "admin_mail_state_sent": {
        "de": "versendet",
        "en": "sent",
        "es": "enviado",
        "fr": "envoyé",
        "it": "inviata",
        "zh": "已发送",
    },
    "admin_mail_state_failed": {
        "de": "fehlgeschlagen",
        "en": "failed",
        "es": "fallido",
        "fr": "échec",
        "it": "non riuscita",
        "zh": "失败",
    },
    "admin_mail_id": {
        "de": "Nachrichtenkennung",
        "en": "Message ID",
        "es": "Identificador del mensaje",
        "fr": "Identifiant du message",
        "it": "Identificativo del messaggio",
        "zh": "邮件标识",
    },
    "admin_company": {
        "de": "Unternehmen",
        "en": "Company",
        "es": "Empresa",
        "fr": "Entreprise",
        "it": "Azienda",
        "zh": "公司",
    },
    "admin_requested_at": {
        "de": "Angefragt",
        "en": "Requested",
        "es": "Solicitado",
        "fr": "Demandé",
        "it": "Richiesto",
        "zh": "请求时间",
    },
    "admin_status": {
        "de": "Status",
        "en": "Status",
        "es": "Estado",
        "fr": "Statut",
        "it": "Stato",
        "zh": "状态",
    },
    "admin_state_open": {
        "de": "offen",
        "en": "open",
        "es": "abierta",
        "fr": "ouverte",
        "it": "aperta",
        "zh": "待处理",
    },
    "admin_state_issued": {
        "de": "Link erzeugt",
        "en": "link created",
        "es": "enlace generado",
        "fr": "lien créé",
        "it": "link generato",
        "zh": "已生成链接",
    },
    "err_user_unknown": {
        "de": "Diese E-Mail ist nicht registriert.",
        "en": "This email is not registered.",
        "es": "Este correo no está registrado.",
        "fr": "Cet e-mail n'est pas enregistré.",
        "it": "Questa e-mail non è registrata.",
        "zh": "该邮箱未注册。",
    },

    # Sidebar
    "logged_in_as": {"de": "Angemeldet", "en": "Signed in", "es": "Conectado", "fr": "Connecté", "it": "Connesso", "zh": "已登录"},
    "btn_logout": {"de": "Abmelden", "en": "Sign out", "es": "Cerrar sesión", "fr": "Déconnexion", "it": "Disconnetti", "zh": "退出登录"},
    "regulations_on_file": {
        "de": "Regulierungen hinterlegt",
        "en": "regulations on file",
        "es": "regulaciones registradas",
        "fr": "réglementations enregistrées",
        "it": "normative registrate",
        "zh": "项已登记的法规",
    },

    # Provider-Info
    "active_provider": {"de": "Aktiver Provider", "en": "Active provider", "es": "Proveedor activo", "fr": "Fournisseur actif", "it": "Provider attivo", "zh": "当前提供商"},
    "model": {"de": "Modell", "en": "Model", "es": "Modelo", "fr": "Modèle", "it": "Modello", "zh": "模型"},
    "err_anthropic_key": {
        "de": "ANTHROPIC_API_KEY fehlt in .env (LLM_PROVIDER=anthropic gesetzt).",
        "en": "ANTHROPIC_API_KEY missing in .env (LLM_PROVIDER=anthropic set).",
        "es": "Falta ANTHROPIC_API_KEY en .env (LLM_PROVIDER=anthropic configurado).",
        "fr": "ANTHROPIC_API_KEY manquant dans .env (LLM_PROVIDER=anthropic défini).",
        "it": "ANTHROPIC_API_KEY mancante in .env (LLM_PROVIDER=anthropic impostato).",
        "zh": "在 .env 中缺少 ANTHROPIC_API_KEY(已设置 LLM_PROVIDER=anthropic)。",
    },
    "err_openai_key": {
        "de": "OPENAI_API_KEY fehlt in .env (LLM_PROVIDER=openai gesetzt).",
        "en": "OPENAI_API_KEY missing in .env (LLM_PROVIDER=openai set).",
        "es": "Falta OPENAI_API_KEY en .env (LLM_PROVIDER=openai configurado).",
        "fr": "OPENAI_API_KEY manquant dans .env (LLM_PROVIDER=openai défini).",
        "it": "OPENAI_API_KEY mancante in .env (LLM_PROVIDER=openai impostato).",
        "zh": "在 .env 中缺少 OPENAI_API_KEY(已设置 LLM_PROVIDER=openai)。",
    },
    "env_hint": {
        "de": " Trage den Key in `.env` ein und starte die App neu.",
        "en": " Add the key to `.env` and restart the app.",
        "es": " Añade la clave en `.env` y reinicia la aplicación.",
        "fr": " Ajoutez la clé dans `.env` et redémarrez l'application.",
        "it": " Aggiungi la chiave in `.env` e riavvia l'applicazione.",
        "zh": " 请在 `.env` 中添加密钥并重启应用。",
    },

    # Company form - Section headers
    "section_company_data": {
        "de": "1. Unternehmensdaten",
        "en": "1. Company data",
        "es": "1. Datos de la empresa",
        "fr": "1. Données de l'entreprise",
        "it": "1. Dati aziendali",
        "zh": "1. 公司数据",
    },
    "section_company_hint": {
        "de": "Ihre Daten werden pro Konto gespeichert und beim nächsten Login vorausgefüllt.",
        "en": "Your data is stored per account and pre-filled on next login.",
        "es": "Tus datos se guardan por cuenta y se rellenan previamente en el próximo inicio de sesión.",
        "fr": "Vos données sont enregistrées par compte et préremplies à la prochaine connexion.",
        "it": "I tuoi dati vengono salvati per account e precompilati al prossimo accesso.",
        "zh": "您的数据按账户保存,下次登录时自动填充。",
    },
    # Der Stammdaten-Abschnitt ist einklappbar, sobald ein Ergebnis vorliegt.
    # Ohne den Hinweis waere das Dreieck des <summary> die einzige Andeutung.
    "company_toggle_hint": {
        "de": "Zum Ein- und Ausklappen anklicken",
        "en": "Click to expand or collapse",
        "es": "Haga clic para desplegar o plegar",
        "fr": "Cliquez pour déplier ou replier",
        "it": "Fare clic per espandere o comprimere",
        "zh": "点击展开或收起",
    },
    # Beschriftung fuer Quellenlinks, die keine Rechtsvorschrift, sondern ein
    # Entwurfsdokument sind (CSRD-Umsetzungsgesetz, noch nicht verkuendet).
    "src_note_csrd_de": {
        "de": "Regierungsentwurf – BT-Drucksache 21/1857 (PDF, 1,5 MB)",
        "en": "Government bill – Bundestag paper 21/1857 (PDF, 1.5 MB)",
        "es": "Proyecto de ley del Gobierno – documento del Bundestag 21/1857 (PDF, 1,5 MB)",
        "fr": "Projet de loi du gouvernement – document du Bundestag 21/1857 (PDF, 1,5 Mo)",
        "it": "Disegno di legge del governo – documento del Bundestag 21/1857 (PDF, 1,5 MB)",
        "zh": "联邦政府法案 – 联邦议院文件 21/1857（PDF，1.5 MB）",
    },
    "ok_saved": {"de": "Gespeichert.", "en": "Saved.", "es": "Guardado.", "fr": "Enregistré.", "it": "Salvato.", "zh": "已保存。"},
    "section_check_regulations": {
        "de": "2. Regulierungen prüfen",
        "en": "2. Check regulations",
        "es": "2. Verificar regulaciones",
        "fr": "2. Vérifier les réglementations",
        "it": "2. Verifica normative",
        "zh": "2. 检查法规",
    },
    "info_save_first": {
        "de": "Bitte zuerst Stammdaten speichern.",
        "en": "Please save master data first.",
        "es": "Por favor, guarda primero los datos maestros.",
        "fr": "Veuillez d'abord enregistrer les données de base.",
        "it": "Salva prima i dati anagrafici.",
        "zh": "请先保存基本数据。",
    },
    "btn_run_check": {"de": "Jetzt prüfen", "en": "Run check", "es": "Verificar ahora", "fr": "Vérifier", "it": "Verifica ora", "zh": "立即检查"},
    "nav_check": {"de": "Prüfung", "en": "Check", "es": "Verificación", "fr": "Vérification", "it": "Verifica", "zh": "检查"},
    "btn_regulations_list": {"de": "Regulierungsliste", "en": "Regulations list", "es": "Lista de regulaciones", "fr": "Liste des réglementations", "it": "Elenco regolamenti", "zh": "法规清单"},
    "page_regulations_list": {"de": "Regulierungsliste", "en": "Regulations list", "es": "Lista de regulaciones", "fr": "Liste des réglementations", "it": "Elenco regolamenti", "zh": "法规清单"},
    "col_regulation": {"de": "Regulierung", "en": "Regulation", "es": "Regulación", "fr": "Réglementation", "it": "Regolamento", "zh": "法规"},
    "col_guidelines": {"de": "Guidelines", "en": "Guidelines", "es": "Directrices", "fr": "Lignes directrices", "it": "Linee guida", "zh": "指南"},
    "col_link_date": {"de": "Quelle & Stand", "en": "Source & as of", "es": "Fuente y fecha", "fr": "Source & mise à jour", "it": "Fonte e aggiornamento", "zh": "来源与截至日期"},
    "stand_label": {"de": "Stand", "en": "As of", "es": "Fecha", "fr": "Mise à jour", "it": "Aggiornamento", "zh": "截至"},
    "no_guidelines": {"de": "—", "en": "—", "es": "—", "fr": "—", "it": "—", "zh": "—"},
    "reglist_search_placeholder": {"de": "Suchen (Regulierung, Guideline, …)", "en": "Search (regulation, guideline, …)", "es": "Buscar (regulación, directriz, …)", "fr": "Rechercher (réglementation, ligne directrice, …)", "it": "Cerca (regolamento, linea guida, …)", "zh": "搜索（法规、指南……）"},
    "open_source": {"de": "Zur Quelle", "en": "Open source", "es": "Abrir fuente", "fr": "Ouvrir la source", "it": "Apri fonte", "zh": "打开来源"},
    "btn_save_master": {
        "de": "Stammdaten speichern",
        "en": "Save master data",
        "es": "Guardar datos maestros",
        "fr": "Enregistrer les données de base",
        "it": "Salva dati anagrafici",
        "zh": "保存基本数据",
    },
    "autofill_btn": {
        "de": "KI-generiert ausfüllen",
        "en": "Fill in with AI",
        "es": "Rellenar con IA",
        "fr": "Remplir par IA",
        "it": "Compila con IA",
        "zh": "AI 自动填写",
    },
    "autofill_hint": {
        "de": "Sucht anhand des Unternehmensnamens auf Website und Wikipedia. Es werden nur explizit gefundene Angaben übernommen — alle KI-gefüllten Felder werden blau umrandet und bleiben manuell änderbar.",
        "en": "Searches the company website and Wikipedia by company name. Only explicitly found values are filled in — all AI-filled fields get a blue outline and stay editable.",
        "es": "Busca en el sitio web y Wikipedia por el nombre de la empresa. Solo se rellenan datos encontrados explícitamente; los campos rellenados por la IA se marcan con un borde azul y siguen siendo editables.",
        "fr": "Recherche sur le site web et Wikipédia à partir du nom de l'entreprise. Seules les valeurs trouvées explicitement sont remplies — les champs remplis par l'IA sont entourés de bleu et restent modifiables.",
        "it": "Cerca sul sito web e su Wikipedia in base al nome dell'azienda. Vengono inseriti solo i dati trovati esplicitamente; i campi compilati dall'IA sono contornati in blu e restano modificabili.",
        "zh": "根据公司名称搜索官网和维基百科。仅填写明确找到的信息——AI 填写的字段会以蓝色边框标出,且仍可手动修改。",
    },
    "autofill_need_name": {
        "de": "Bitte zuerst den Unternehmensnamen eintragen.",
        "en": "Please enter the company name first.",
        "es": "Introduzca primero el nombre de la empresa.",
        "fr": "Veuillez d'abord saisir le nom de l'entreprise.",
        "it": "Inserire prima il nome dell'azienda.",
        "zh": "请先输入公司名称。",
    },
    "autofill_running": {
        "de": "Suche läuft (Website / Wikipedia) …",
        "en": "Searching (website / Wikipedia) …",
        "es": "Buscando (sitio web / Wikipedia) …",
        "fr": "Recherche en cours (site web / Wikipédia) …",
        "it": "Ricerca in corso (sito web / Wikipedia) …",
        "zh": "正在搜索(官网 / 维基百科)…",
    },
    "autofill_done": {
        "de": "Felder übernommen — bitte prüfen und speichern. Quellen:",
        "en": "fields filled — please review and save. Sources:",
        "es": "campos rellenados — revise y guarde. Fuentes:",
        "fr": "champs remplis — vérifiez et enregistrez. Sources :",
        "it": "campi compilati — verificare e salvare. Fonti:",
        "zh": "个字段已填写——请检查并保存。来源:",
    },
    "autofill_none": {
        "de": "Keine explizit belegten Angaben gefunden.",
        "en": "No explicitly stated values found.",
        "es": "No se encontraron datos explícitos.",
        "fr": "Aucune donnée explicite trouvée.",
        "it": "Nessun dato esplicito trovato.",
        "zh": "未找到明确的信息。",
    },
    "autofill_error": {
        "de": "Suche fehlgeschlagen:",
        "en": "Search failed:",
        "es": "Error en la búsqueda:",
        "fr": "Échec de la recherche :",
        "it": "Ricerca non riuscita:",
        "zh": "搜索失败:",
    },
    "last_check": {"de": "Letzter Check", "en": "Last check", "es": "Última verificación", "fr": "Dernière vérification", "it": "Ultima verifica", "zh": "上次检查"},
    "last_result": {"de": "Letztes Ergebnis:", "en": "Last result:", "es": "Último resultado:", "fr": "Dernier résultat :", "it": "Ultimo risultato:", "zh": "上次结果:"},

    # Company form fields
    "field_name": {
        "de": "Unternehmensname (wir empfehlen die Nutzung eines Pseudonyms)",
        "en": "Company name (we recommend using a pseudonym)",
        "es": "Nombre de la empresa (recomendamos utilizar un seudónimo)",
        "fr": "Nom de l'entreprise (nous recommandons d'utiliser un pseudonyme)",
        "it": "Nome dell'azienda (consigliamo di utilizzare uno pseudonimo)",
        "zh": "公司名称（建议使用化名）",
    },
    "field_employees_total": {
        "de": "Mitarbeiter gesamt (weltweit)",
        "en": "Total employees (worldwide)",
        "es": "Empleados totales (mundial)",
        "fr": "Employés totaux (dans le monde)",
        "it": "Dipendenti totali (nel mondo)",
        "zh": "员工总数(全球)",
    },
    "field_employees_de": {
        "de": "davon Mitarbeiter in Deutschland",
        "en": "of which employees in Germany",
        "es": "de los cuales empleados en Alemania",
        "fr": "dont employés en Allemagne",
        "it": "di cui dipendenti in Germania",
        "zh": "其中在德国的员工",
    },
    "field_revenue": {
        "de": "Nettoumsatz weltweit pro Jahr (EUR)",
        "en": "Net revenue worldwide per year (EUR)",
        "es": "Ingresos netos anuales a nivel mundial (EUR)",
        "fr": "Chiffre d'affaires net annuel mondial (EUR)",
        "it": "Ricavi netti annui a livello mondiale (EUR)",
        "zh": "全球年度净收入(欧元)",
    },
    "field_revenue_eu": {
        "de": "Nettoumsatz pro Jahr in der EU (EUR)",
        "en": "Net revenue per year in the EU (EUR)",
        "es": "Ingresos netos anuales en la UE (EUR)",
        "fr": "Chiffre d'affaires net annuel dans l'UE (EUR)",
        "it": "Ricavi netti annui nell'UE (EUR)",
        "zh": "欧盟境内年度净收入(欧元)",
    },
    "field_balance_sheet": {
        "de": "Bilanzsumme (EUR)",
        "en": "Balance sheet total (EUR)",
        "es": "Total del balance (EUR)",
        "fr": "Total du bilan (EUR)",
        "it": "Totale di bilancio (EUR)",
        "zh": "资产负债表总额(欧元)",
    },
    "field_legal_form": {"de": "Rechtsform", "en": "Legal form", "es": "Forma jurídica", "fr": "Forme juridique", "it": "Forma giuridica", "zh": "法律形式"},
    "field_branch": {"de": "Branche", "en": "Industry", "es": "Sector", "fr": "Secteur", "it": "Settore", "zh": "行业"},
    "field_group_role": {"de": "Konzernstruktur", "en": "Group structure", "es": "Estructura del grupo", "fr": "Structure du groupe", "it": "Struttura del gruppo", "zh": "集团架构"},
    "field_b2c": {
        "de": "B2C-Geschäft (Verbraucher)",
        "en": "B2C business (consumers)",
        "es": "Negocio B2C (consumidores)",
        "fr": "Activité B2C (consommateurs)",
        "it": "Attività B2C (consumatori)",
        "zh": "B2C 业务(消费者)",
    },
    "field_listed": {
        "de": "Kapitalmarktorientiert / börsennotiert",
        "en": "Capital-market oriented / listed",
        "es": "Cotizada en bolsa / mercado de capitales",
        "fr": "Cotée en bourse / orientée marché des capitaux",
        "it": "Orientata al mercato dei capitali / quotata",
        "zh": "面向资本市场 / 上市",
    },
    "field_env_claims": {
        "de": "Umweltaussagen / Nachhaltigkeitssiegel im Marketing",
        "en": "Environmental claims / sustainability labels in marketing",
        "es": "Declaraciones ambientales / sellos de sostenibilidad en marketing",
        "fr": "Allégations environnementales / labels de durabilité en marketing",
        "it": "Dichiarazioni ambientali / marchi di sostenibilità nel marketing",
        "zh": "营销中的环境声明 / 可持续性标签",
    },
    # Neue Profilfelder vom 29.09.2026 (EnEfG, AbwV Anhang 38, REACH Art. 33 / SCIP)
    "field_energy_gwh": {
        "de": "Gesamtenergieverbrauch in Deutschland pro Jahr (GWh)",
        "en": "Total energy consumption in Germany per year (GWh)",
        "es": "Consumo total de energía en Alemania al año (GWh)",
        "fr": "Consommation totale d'énergie en Allemagne par an (GWh)",
        "it": "Consumo energetico totale in Germania all'anno (GWh)",
        "zh": "在德国的年度能源总消耗量（GWh）",
    },
    "field_wet_processing": {
        "de": "Abwasser aus Textilherstellung oder -veredlung in Deutschland",
        "en": "Wastewater from textile manufacturing or finishing in Germany",
        "es": "Aguas residuales de la fabricación o el acabado textil en Alemania",
        "fr": "Eaux usées issues de la fabrication ou de l'ennoblissement textile en Allemagne",
        "it": "Acque reflue dalla produzione o nobilitazione tessile in Germania",
        "zh": "在德国的纺织品生产或整理过程中产生废水",
    },
    # --- Mitgliedsverband bei der Registrierung (30.09.2026) ----------
    # Die Verbandsnamen selbst sind Eigennamen und bleiben unuebersetzt;
    # uebersetzt werden nur Beschriftung, Fehlertext und „Kein Mitglied“.
    "field_association": {
        "de": "Mitglied bei welchem Verband?",
        "en": "Member of which association?",
        "es": "¿Miembro de qué asociación?",
        "fr": "Membre de quelle fédération ?",
        "it": "Membro di quale associazione?",
        "zh": "您是哪个协会的会员？",
    },
    "association_choose": {
        "de": "Bitte wählen",
        "en": "Please select",
        "es": "Seleccione",
        "fr": "Veuillez choisir",
        "it": "Selezioni",
        "zh": "请选择",
    },
    "err_association_missing": {
        "de": "Bitte geben Sie an, bei welchem Verband Sie Mitglied sind.",
        "en": "Please state which association you are a member of.",
        "es": "Indique de qué asociación es miembro.",
        "fr": "Veuillez indiquer de quelle fédération vous êtes membre.",
        "it": "Indichi di quale associazione è membro.",
        "zh": "请说明您是哪个协会的会员。",
    },
    "admin_pending_association": {
        "de": "Verband",
        "en": "Association",
        "es": "Asociación",
        "fr": "Fédération",
        "it": "Associazione",
        "zh": "协会",
    },
    "field_svhc": {
        "de": "Enthalten Ihre Produkte Stoffe der ECHA-Kandidatenliste (SVHC) über 0,1 %?",
        "en": "Do your products contain substances on the ECHA Candidate List (SVHC) above 0.1%?",
        "es": "¿Contienen sus productos sustancias de la Lista de candidatas de la ECHA (SVHC) por encima del 0,1 %?",
        "fr": "Vos produits contiennent-ils des substances de la liste des substances candidates de l'ECHA (SVHC) au-delà de 0,1 % ?",
        "it": "I suoi prodotti contengono sostanze dell'elenco di sostanze candidate dell'ECHA (SVHC) oltre lo 0,1%?",
        "zh": "贵公司的产品是否含有 ECHA 候选清单（SVHC）中含量超过 0.1% 的物质？",
    },
    "field_eu_importer": {
        "de": "Import von Produkten aus Nicht-EU-Ländern",
        "en": "Import of products from non-EU countries",
        "es": "Importación de productos de países no pertenecientes a la UE",
        "fr": "Importation de produits en provenance de pays hors UE",
        "it": "Importazione di prodotti da paesi extra-UE",
        "zh": "从非欧盟国家进口产品",
    },

    # Product categories / sites
    "section_products": {
        "de": "#### Produktkategorien",
        "en": "#### Product categories",
        "es": "#### Categorías de productos",
        "fr": "#### Catégories de produits",
        "it": "#### Categorie di prodotto",
        "zh": "#### 产品类别",
    },
    "products_hint": {
        "de": "Mehrfachauswahl möglich. Steuert EUDR, PPWR, Ökodesign, Right-to-Repair und das Vernichtungsverbot.",
        "en": "Multi-select possible. Drives EUDR, PPWR, Ecodesign, Right-to-Repair and the destruction ban.",
        "es": "Selección múltiple posible. Afecta EUDR, PPWR, Ecodiseño, Derecho a Reparar y la prohibición de destrucción.",
        "fr": "Sélection multiple possible. Influence EUDR, PPWR, Écoconception, Droit à la Réparation et l'interdiction de destruction.",
        "it": "Selezione multipla possibile. Influenza EUDR, PPWR, Ecodesign, Diritto alla Riparazione e il divieto di distruzione.",
        "zh": "可多选。影响 EUDR、PPWR、生态设计、维修权与销毁禁令。",
    },
    "products_label": {"de": "Kategorien", "en": "Categories", "es": "Categorías", "fr": "Catégories", "it": "Categorie", "zh": "类别"},
    "section_roles": {
        "de": "#### Rolle in der Wertschöpfungskette",
        "en": "#### Role in the value chain",
        "es": "#### Función en la cadena de valor",
        "fr": "#### Rôle dans la chaîne de valeur",
        "it": "#### Ruolo nella catena del valore",
        "zh": "#### 在价值链中的角色",
    },
    "roles_hint": {
        "de": "Mehrfachauswahl möglich. Entscheidet mit, ob produktbezogene Pflichten an Ihrem Unternehmen hängen — etwa EUDR, PPWR, EmpCo und das Vernichtungsverbot.",
        "en": "Multi-select possible. Helps decide whether product-related duties attach to your company — e.g. EUDR, PPWR, EmpCo and the destruction ban.",
        "es": "Selección múltiple posible. Determina si las obligaciones sobre productos recaen en su empresa: EUDR, PPWR, EmpCo y la prohibición de destrucción.",
        "fr": "Sélection multiple possible. Détermine si les obligations liées aux produits pèsent sur votre entreprise : EUDR, PPWR, EmpCo et l'interdiction de destruction.",
        "it": "Selezione multipla possibile. Determina se gli obblighi sui prodotti ricadono sulla vostra impresa: EUDR, PPWR, EmpCo e il divieto di distruzione.",
        "zh": "可多选。用于判断与产品相关的义务是否落在贵公司身上——如 EUDR、PPWR、EmpCo 及销毁禁令。",
    },
    "section_materials": {
        "de": "#### Materialien",
        "en": "#### Materials",
        "es": "#### Materiales",
        "fr": "#### Matériaux",
        "it": "#### Materiali",
        "zh": "#### 材料",
    },
    "materials_hint": {
        "de": "Mehrfachauswahl möglich. Steuert EUDR (Leder/Rind, Naturkautschuk, Holz- und Zellulosefasern), die Zwangsarbeitsverordnung und die Ökodesign-Anforderungen an chemische Ausrüstungen.",
        "en": "Multi-select possible. Drives EUDR (leather/cattle, natural rubber, wood and cellulose fibres), the Forced Labour Regulation and the ecodesign requirements for chemical finishes.",
        "es": "Selección múltiple posible. Afecta al EUDR (cuero/bovino, caucho natural, fibras de madera y celulosa), al Reglamento sobre trabajo forzoso y a los requisitos de ecodiseño para acabados químicos.",
        "fr": "Sélection multiple possible. Influence l'EUDR (cuir/bovins, caoutchouc naturel, fibres de bois et de cellulose), le règlement sur le travail forcé et les exigences d'écoconception relatives aux apprêts chimiques.",
        "it": "Selezione multipla possibile. Influenza l'EUDR (pelle/bovini, gomma naturale, fibre di legno e cellulosa), il regolamento sul lavoro forzato e i requisiti di ecodesign per i finissaggi chimici.",
        "zh": "可多选。影响 EUDR（皮革/牛类、天然橡胶、木材与纤维素纤维）、强迫劳动条例以及针对化学整理的生态设计要求。",
    },
    "section_markets": {
        "de": "#### Absatzmärkte",
        "en": "#### Sales markets",
        "es": "#### Mercados de venta",
        "fr": "#### Marchés de vente",
        "it": "#### Mercati di sbocco",
        "zh": "#### 销售市场",
    },
    "markets_hint": {
        "de": "Mehrfachauswahl möglich. Produktbezogene Marktregeln wie EUDR, PPWR, Right to Repair, EmpCo und das Vernichtungsverbot knüpfen an das Inverkehrbringen in der EU an.",
        "en": "Multi-select possible. Product-related market rules such as EUDR, PPWR, Right to Repair, EmpCo and the destruction ban attach to placing products on the EU market.",
        "es": "Selección múltiple posible. Las normas de mercado sobre productos como EUDR, PPWR, derecho a reparar, EmpCo y la prohibición de destrucción se vinculan a la introducción en el mercado de la UE.",
        "fr": "Sélection multiple possible. Les règles de marché relatives aux produits (EUDR, PPWR, droit à la réparation, EmpCo, interdiction de destruction) se rattachent à la mise sur le marché de l'UE.",
        "it": "Selezione multipla possibile. Le regole di mercato sui prodotti come EUDR, PPWR, diritto alla riparazione, EmpCo e il divieto di distruzione si ricollegano all'immissione sul mercato dell'UE.",
        "zh": "可多选。EUDR、PPWR、维修权、EmpCo 及销毁禁令等与产品相关的市场规则，均以在欧盟投放市场为连接点。",
    },
    "section_sites": {
        "de": "#### Standorte",
        "en": "#### Sites",
        "es": "#### Ubicaciones",
        "fr": "#### Sites",
        "it": "#### Sedi",
        "zh": "#### 场所",
    },
    "sites_hint": {
        "de": "Anzahl, Typ und Region je Standort. Weitere Zeilen legen Sie über „Standort hinzufügen“ an.",
        "en": "Count, type and region per site. Use “Add site” for more rows.",
        "es": "Cantidad, tipo y región por ubicación. Usa «Añadir ubicación» para más filas.",
        "fr": "Nombre, type et région par site. Utilisez « Ajouter un site » pour d’autres lignes.",
        "it": "Numero, tipo e regione per sede. Usa «Aggiungi sede» per altre righe.",
        "zh": "每个场所的数量、类型和地区。用“添加场所”增加行。",
    },
    "site_type": {"de": "Typ", "en": "Type", "es": "Tipo", "fr": "Type", "it": "Tipo", "zh": "类型"},
    "site_region": {"de": "Region", "en": "Region", "es": "Región", "fr": "Région", "it": "Regione", "zh": "地区"},
    "site_count": {"de": "Anzahl", "en": "Count", "es": "Cantidad", "fr": "Nombre", "it": "Numero", "zh": "数量"},
    "site_remove_help": {
        "de": "Diese Zeile entfernen",
        "en": "Remove this row",
        "es": "Eliminar esta fila",
        "fr": "Supprimer cette ligne",
        "it": "Rimuovi questa riga",
        "zh": "删除此行",
    },
    "site_add": {
        "de": "Standort hinzufügen",
        "en": "Add site",
        "es": "Añadir ubicación",
        "fr": "Ajouter un site",
        "it": "Aggiungi sede",
        "zh": "添加场所",
    },

    # Analysis progress
    "step1": {"de": "Schritt 1/2: Gesetzestexte aktualisieren", "en": "Step 1/2: Updating law texts", "es": "Paso 1/2: Actualizar textos legales", "fr": "Étape 1/2 : Mise à jour des textes", "it": "Passo 1/2: aggiornamento testi", "zh": "步骤 1/2:更新法律文本"},
    "step2": {"de": "Schritt 2/2: Analyse via LLM", "en": "Step 2/2: LLM analysis", "es": "Paso 2/2: análisis LLM", "fr": "Étape 2/2 : analyse LLM", "it": "Passo 2/2: analisi LLM", "zh": "步骤 2/2:LLM 分析"},
    "analysis_waiting": {"de": "ausstehend", "en": "pending", "es": "pendiente", "fr": "en attente", "it": "in attesa", "zh": "待处理"},
    "analysis_slow": {
        "de": "Das KI-Modell ist gerade stark ausgelastet. Die Anwendung versucht es automatisch erneut und weicht bei Bedarf auf ein anderes Modell aus. Das kann einige Minuten dauern - bitte die Seite geöffnet lassen.",
        "en": "The AI model is currently under heavy load. The application retries automatically and switches to another model if needed. This may take a few minutes - please keep this page open.",
        "es": "El modelo de IA está muy solicitado en este momento. La aplicación lo reintenta automáticamente y, si es necesario, cambia a otro modelo. Puede tardar unos minutos: mantenga esta página abierta.",
        "fr": "Le modèle d'IA est actuellement très sollicité. L'application réessaie automatiquement et passe si nécessaire à un autre modèle. Cela peut prendre quelques minutes - veuillez laisser cette page ouverte.",
        "it": "Il modello di IA è al momento molto carico. L'applicazione riprova automaticamente e, se necessario, passa a un altro modello. Può richiedere alcuni minuti: lasciare aperta questa pagina.",
        "zh": "AI 模型当前负载较高。应用程序会自动重试,必要时切换到其他模型。这可能需要几分钟,请保持此页面打开。",
    },
    "law_check_progress": {
        "de": "Gesetzestext {i}/{n}: {name} ({lang}) wird geprüft …",
        "en": "Law text {i}/{n}: {name} ({lang}) being checked …",
        "es": "Texto legal {i}/{n}: se verifica {name} ({lang}) …",
        "fr": "Texte légal {i}/{n} : vérification de {name} ({lang}) …",
        "it": "Testo giuridico {i}/{n}: {name} ({lang}) in verifica …",
        "zh": "法律文本 {i}/{n}:正在检查 {name}({lang})…",
    },
    "law_no_fulltext": {
        "de": "{name}: {err} - fahre ohne Volltext fort.",
        "en": "{name}: {err} - continuing without full text.",
        "es": "{name}: {err} - continuando sin texto completo.",
        "fr": "{name} : {err} - poursuite sans texte intégral.",
        "it": "{name}: {err} - si continua senza testo integrale.",
        "zh": "{name}:{err} - 在无全文情况下继续。",
    },
    "cache_status": {
        "de": "{hits}/{total} aus Cache, {new} neu zu analysieren (Provider: {p}, Modell: {m})",
        "en": "{hits}/{total} from cache, {new} to analyze (provider: {p}, model: {m})",
        "es": "{hits}/{total} desde caché, {new} nuevos a analizar (proveedor: {p}, modelo: {m})",
        "fr": "{hits}/{total} depuis le cache, {new} à analyser (fournisseur : {p}, modèle : {m})",
        "it": "{hits}/{total} dalla cache, {new} da analizzare (provider: {p}, modello: {m})",
        "zh": "{hits}/{total} 来自缓存,{new} 需新分析(提供商:{p},模型:{m})",
    },
    "analysis_progress": {
        "de": "Analysiert {done}/{total} - zuletzt: {name}",
        "en": "Analyzed {done}/{total} - last: {name}",
        "es": "Analizado {done}/{total} - último: {name}",
        "fr": "Analysé {done}/{total} - dernier : {name}",
        "it": "Analizzato {done}/{total} - ultimo: {name}",
        "zh": "已分析 {done}/{total} - 最新:{name}",
    },
    "err_analysis_start": {
        "de": "Analyse-Start fehlgeschlagen",
        "en": "Analysis start failed",
        "es": "Error al iniciar el análisis",
        "fr": "Échec du démarrage de l'analyse",
        "it": "Avvio analisi fallito",
        "zh": "分析启动失败",
    },
    "btn_open_fullscreen": {
        "de": "Ergebnis in neuem Tab (Vollbild) öffnen",
        "en": "Open result in new tab (full-screen)",
        "es": "Abrir resultado en nueva pestaña (pantalla completa)",
        "fr": "Ouvrir le résultat dans un nouvel onglet (plein écran)",
        "it": "Apri risultato in una nuova scheda (schermo intero)",
        "zh": "在新标签页中打开结果(全屏)",
    },

    # Fullscreen page
    "fullscreen_title": {
        "de": "ESG-Regulierungs-Check - Vollbild",
        "en": "ESG Regulation Check - Full screen",
        "es": "Verificación ESG - Pantalla completa",
        "fr": "Vérification ESG - Plein écran",
        "it": "Verifica ESG - Schermo intero",
        "zh": "ESG 法规检查 - 全屏",
    },
    "fullscreen_status": {"de": "Stand", "en": "As of", "es": "Actualizado", "fr": "Statut", "it": "Stato", "zh": "更新时间"},
    "fullscreen_err_nouser": {
        "de": "Kein User übergeben. Bitte über das Hauptdashboard öffnen.",
        "en": "No user provided. Please open via main dashboard.",
        "es": "Sin usuario. Ábrelo desde el panel principal.",
        "fr": "Aucun utilisateur. Ouvrez via le tableau de bord principal.",
        "it": "Nessun utente. Apri tramite il dashboard principale.",
        "zh": "未提供用户。请通过主控制台打开。",
    },
    "fullscreen_err_uid": {
        "de": "Ungültige User-ID.",
        "en": "Invalid user ID.",
        "es": "ID de usuario no válido.",
        "fr": "ID utilisateur non valide.",
        "it": "ID utente non valido.",
        "zh": "用户 ID 无效。",
    },
    "fullscreen_no_result": {
        "de": "Noch kein Analyse-Ergebnis vorhanden. Erst auf der Hauptseite 'Jetzt prüfen' anklicken.",
        "en": "No analysis result yet. Click 'Run check' on the main page first.",
        "es": "Aún no hay resultado. Primero pulsa 'Verificar ahora' en la página principal.",
        "fr": "Aucun résultat pour le moment. Cliquez d'abord sur 'Vérifier' sur la page principale.",
        "it": "Nessun risultato disponibile. Clicca prima 'Verifica ora' nella pagina principale.",
        "zh": "尚无分析结果。请先在主页上点击“立即检查”。",
    },
    # ---------- Anwendungsbeginn / Status ----------
    "col_applies_from": {
        "de": "Gilt ab / Status", "en": "Applies from / status",
        "es": "Se aplica desde / estado", "fr": "S'applique à partir de / statut",
        "it": "Si applica dal / stato", "zh": "适用起始 / 状态",
    },
    "law_state_of": {
        "de": "Gesetzesstand vom", "en": "Legal text as of", "es": "Texto legal a fecha de",
        "fr": "Texte juridique au", "it": "Testo di legge al", "zh": "法律文本截至",
    },
    # ---------- Admin: Regulierungsstatus ----------
    "admin_regstatus_title": {
        "de": "Regulierungs-Status", "en": "Regulation status", "es": "Estado de las regulaciones",
        "fr": "État des réglementations", "it": "Stato dei regolamenti", "zh": "法规状态",
    },
    "admin_regstatus_hint": {
        "de": "Gesetzesstand je Regulierung, letzter Watchdog-Lauf und erkannte Textänderungen. "
              "Vorschläge sind KI-generiert und ändern nichts automatisch.",
        "en": "Legal text status per regulation, last watchdog run and detected text changes. "
              "Suggestions are AI-generated and change nothing automatically.",
        "es": "Estado del texto legal por regulación, última ejecución del watchdog y cambios detectados. "
              "Las sugerencias las genera la IA y no cambian nada automáticamente.",
        "fr": "État du texte juridique par réglementation, dernière exécution du watchdog et modifications "
              "détectées. Les suggestions sont générées par l'IA et ne modifient rien automatiquement.",
        "it": "Stato del testo di legge per regolamento, ultima esecuzione del watchdog e modifiche rilevate. "
              "I suggerimenti sono generati dall'IA e non modificano nulla automaticamente.",
        "zh": "各法规的法律文本状态、最近一次监测运行及检测到的文本变更。建议由人工智能生成，不会自动更改任何内容。",
    },
    "admin_regstatus_last_run": {
        "de": "Letzter Watchdog-Lauf", "en": "Last watchdog run", "es": "Última ejecución del watchdog",
        "fr": "Dernière exécution du watchdog", "it": "Ultima esecuzione del watchdog", "zh": "最近一次监测运行",
    },
    "admin_regstatus_never": {
        "de": "noch nie gelaufen", "en": "never run", "es": "nunca ejecutado",
        "fr": "jamais exécuté", "it": "mai eseguito", "zh": "从未运行",
    },
    "admin_regstatus_versions": {
        "de": "Fassungen", "en": "Versions", "es": "Versiones", "fr": "Versions",
        "it": "Versioni", "zh": "版本数",
    },
    "admin_regstatus_changes": {
        "de": "Erkannte Änderungen", "en": "Detected changes", "es": "Cambios detectados",
        "fr": "Modifications détectées", "it": "Modifiche rilevate", "zh": "检测到的变更",
    },
    "admin_regstatus_no_changes": {
        "de": "Keine Änderung erkannt.", "en": "No change detected.", "es": "Sin cambios detectados.",
        "fr": "Aucune modification détectée.", "it": "Nessuna modifica rilevata.", "zh": "未检测到变更。",
    },
    "admin_regstatus_errors": {
        "de": "Fehler im letzten Lauf", "en": "Errors in last run", "es": "Errores en la última ejecución",
        "fr": "Erreurs lors de la dernière exécution", "it": "Errori nell'ultima esecuzione", "zh": "上次运行中的错误",
    },
    "admin_regstatus_run_hint": {
        "de": "Der Watchdog wird nicht aus der Oberfläche gestartet, sondern per Cron auf dem Server "
              "(python watchdog.py).",
        "en": "The watchdog is not started from the interface but by cron on the server (python watchdog.py).",
        "es": "El watchdog no se inicia desde la interfaz, sino mediante cron en el servidor (python watchdog.py).",
        "fr": "Le watchdog n'est pas lancé depuis l'interface mais par cron sur le serveur (python watchdog.py).",
        "it": "Il watchdog non si avvia dall'interfaccia ma tramite cron sul server (python watchdog.py).",
        "zh": "监测程序不从界面启动，而是由服务器上的 cron 运行（python watchdog.py）。",
    },
    "admin_regstatus_no_text": {
        "de": "kein Text im Cache", "en": "no text cached", "es": "sin texto en caché",
        "fr": "aucun texte en cache", "it": "nessun testo in cache", "zh": "缓存中无文本",
    },
    "admin_regstatus_source": {
        "de": "Textquelle", "en": "Text source", "es": "Fuente del texto",
        "fr": "Source du texte", "it": "Fonte del testo", "zh": "文本来源",
    },
    "admin_regstatus_base_act": {
        "de": "Nur Ursprungsfassung",
        "en": "Original version only",
        "es": "Solo versión original",
        "fr": "Version d'origine uniquement",
        "it": "Solo versione originale",
        "zh": "仅原始版本",
    },
    "admin_regstatus_base_act_hint": {
        "de": "Die konsolidierte Fassung liess sich nicht ermitteln. Der gespeicherte Text ist der "
              "Ursprungsrechtsakt — spätere Änderungen fehlen darin. Bitte erneut prüfen, bevor "
              "Ergebnisse zu dieser Regulierung verwendet werden.",
        "en": "The consolidated version could not be determined. The stored text is the original act — "
              "later amendments are missing from it. Please re-check before relying on results for "
              "this regulation.",
        "es": "No se pudo determinar la versión consolidada. El texto almacenado es el acto original: "
              "le faltan las modificaciones posteriores. Vuelve a comprobarlo antes de usar los "
              "resultados de esta regulación.",
        "fr": "La version consolidée n'a pas pu être déterminée. Le texte enregistré est l'acte "
              "d'origine — les modifications ultérieures y manquent. Veuillez revérifier avant "
              "d'utiliser les résultats de cette réglementation.",
        "it": "Non è stato possibile determinare la versione consolidata. Il testo salvato è l'atto "
              "originale: mancano le modifiche successive. Verifica di nuovo prima di usare i "
              "risultati di questo regolamento.",
        "zh": "无法确定合并版本。所存文本为原始法案，其中缺少后续修订。在使用该法规的结果前请重新检查。",
    },
    # Handlungsplan: Fristen, erste Schritte, Schwellen-Naehe
    "deadline_label": {
        "de": "Gilt ab", "en": "Applies from", "es": "Se aplica desde",
        "fr": "S'applique à partir du", "it": "Si applica dal", "zh": "自此适用",
    },
    # Ohne bestimmbares Datum passt "Gilt ab" grammatisch nicht mehr
    # ("Gilt ab: Ruecknahme angekuendigt"). Dann traegt die Zeile das
    # Substantiv-Label und einen der drei Fortsetzungstexte darunter.
    "deadline_none_label": {
        "de": "Anwendungsbeginn", "en": "Start of application",
        "es": "Inicio de aplicación", "fr": "Début d'application",
        "it": "Inizio dell'applicazione", "zh": "适用起始",
    },
    "deadline_none_exempt": {
        "de": "keiner; das Unternehmen wird von der Norm nicht erfasst",
        "en": "none; the company is not covered by the rule",
        "es": "ninguno; la empresa no está sujeta a la norma",
        "fr": "aucun ; l'entreprise n'est pas visée par la règle",
        "it": "nessuno; l'impresa non rientra nella norma",
        "zh": "无；该企业不在此规范的适用范围内",
    },
    "deadline_open": {
        "de": "aus den Angaben nicht bestimmbar",
        "en": "cannot be determined from the data provided",
        "es": "no determinable con los datos indicados",
        "fr": "non déterminable à partir des données fournies",
        "it": "non determinabile in base ai dati forniti",
        "zh": "无法根据所填数据确定",
    },
    "deadline_none_draft": {
        "de": "noch offen; das Gesetzgebungsverfahren ist nicht abgeschlossen",
        "en": "not yet set; the legislative procedure is not complete",
        "es": "aún abierto; el procedimiento legislativo no ha concluido",
        "fr": "pas encore fixé ; la procédure législative n'est pas achevée",
        "it": "non ancora fissato; l'iter legislativo non è concluso",
        "zh": "尚未确定；立法程序未完成",
    },
    "deadline_none_withdrawn": {
        "de": "keiner; die Rücknahme des Vorschlags ist angekündigt",
        "en": "none; withdrawal of the proposal has been announced",
        "es": "ninguno; se ha anunciado la retirada de la propuesta",
        "fr": "aucun ; le retrait de la proposition a été annoncé",
        "it": "nessuno; è stato annunciato il ritiro della proposta",
        "zh": "无；已宣布撤回该提案",
    },
    "first_steps_label": {
        "de": "Erste Schritte", "en": "First steps", "es": "Primeros pasos",
        "fr": "Premières étapes", "it": "Primi passi", "zh": "第一步",
    },
    "first_steps_link": {
        "de": "Weiterführende Leitlinie", "en": "Further guidance",
        "es": "Directriz complementaria", "fr": "Ligne directrice complémentaire",
        "it": "Linee guida di approfondimento", "zh": "延伸指南",
    },
    "thresholds_title": {
        "de": "Nähe zu Schwellenwerten", "en": "Proximity to thresholds",
        "es": "Proximidad a los umbrales", "fr": "Proximité des seuils",
        "it": "Vicinanza alle soglie", "zh": "接近门槛值",
    },
    "thresholds_intro": {
        "de": "Die folgenden Schwellen liegen weniger als 20 Prozent von den Angaben dieses "
              "Unternehmens entfernt.",
        "en": "The following thresholds are less than 20 percent away from this company's figures.",
        "es": "Los siguientes umbrales están a menos del 20 por ciento de las cifras de esta empresa.",
        "fr": "Les seuils suivants se situent à moins de 20 pour cent des données de cette entreprise.",
        "it": "Le soglie seguenti distano meno del 20 per cento dai dati di questa impresa.",
        "zh": "以下门槛值与该企业的数据相差不到 20%。",
    },
    # ---------- PDF-Export ----------
    # "Gilt ab" liefert bereits "deadline_label"; ein eigener Schluessel dafuer
    # (frueher "csv_deadline") waere eine zweite Quelle fuer denselben Text.
    "btn_download_pdf": {
        "de": "Ergebnis als PDF", "en": "Result as PDF", "es": "Resultado en PDF",
        "fr": "Résultat en PDF", "it": "Risultato in PDF", "zh": "结果 PDF",
    },
    "pdf_created": {
        "de": "Erstellt am", "en": "Created on", "es": "Creado el",
        "fr": "Établi le", "it": "Creato il", "zh": "创建日期",
    },
    "pdf_summary": {
        "de": "Zusammenfassung", "en": "Summary", "es": "Resumen",
        "fr": "Synthèse", "it": "Sintesi", "zh": "摘要",
    },
    "results_hint": {
        "de": "Fragen zu Ihrem Ergebnis? Der ESG-Regulierungs-Check bietet eine erste Orientierung. Für eine vertiefte Einordnung einzelner Regelungen und ihrer Auswirkungen auf Ihr Unternehmen steht Ihnen das Team von textil+mode und seiner Mitgliedsverbände gerne zur Verfügung.",
        "en": "Questions about your result? The ESG Regulation Check offers a first orientation. For a deeper assessment of individual rules and their effects on your company, the team of textil+mode and its member associations is happy to help.",
        "es": "¿Preguntas sobre su resultado? La Verificación de Regulaciones ESG ofrece una primera orientación. Para una valoración más profunda de normas concretas y de sus efectos sobre su empresa, el equipo de textil+mode y de sus asociaciones miembro está a su disposición.",
        "fr": "Des questions sur votre résultat ? La Vérification des Réglementations ESG offre une première orientation. Pour une analyse approfondie de règles précises et de leurs effets sur votre entreprise, l'équipe de textil+mode et de ses fédérations membres se tient à votre disposition.",
        "it": "Domande sul suo risultato? La Verifica delle Normative ESG offre un primo orientamento. Per un inquadramento più approfondito delle singole norme e dei loro effetti sulla sua azienda, il team di textil+mode e delle sue associazioni membro è a sua disposizione.",
        "zh": "对结果有疑问？ESG 法规检查提供的是初步定位。如需就个别规定及其对贵公司的影响作更深入的评估，textil+mode 及其会员协会的团队乐意提供帮助。",
    },
    "pdf_source": {
        "de": "Quelle", "en": "Source", "es": "Fuente",
        "fr": "Source", "it": "Fonte", "zh": "来源",
    },
    "pdf_page": {
        "de": "Seite", "en": "Page", "es": "Página",
        "fr": "Page", "it": "Pagina", "zh": "页码",
    },
}


# ---------- Status des Rechtsakts ----------
# Schluessel entsprechen regulations.STATUS_* .
STATUS_LABELS: dict[str, dict[str, str]] = {
    "in_kraft": {
        "de": "in Kraft", "en": "in force", "es": "en vigor",
        "fr": "en vigueur", "it": "in vigore", "zh": "已生效",
    },
    "gilt_ab": {
        "de": "gilt ab", "en": "applies from", "es": "se aplica desde",
        "fr": "s'applique à partir du", "it": "si applica dal", "zh": "自此适用",
    },
    "entwurf": {
        "de": "Entwurf", "en": "draft", "es": "proyecto",
        "fr": "projet", "it": "progetto", "zh": "草案",
    },
    "rueckzug_angekuendigt": {
        "de": "Rücknahme angekündigt", "en": "withdrawal announced", "es": "retirada anunciada",
        "fr": "retrait annoncé", "it": "ritiro annunciato", "zh": "已宣布撤回",
    },
}


# ---------- Erlaeuterungen zum Anwendungsbeginn ----------
# Schluessel entsprechen dem Feld "note" in regulations.APPLICATION_BY_REG_KEY.
APPLIES_NOTES: dict[str, dict[str, str]] = {
    "csddd": {
        "de": "Nationale Umsetzung bis 26.07.2028. Kein größenabhängiger Phase-in mehr; "
              "die Berichtspflicht nach Art. 16 gilt für Geschäftsjahre ab 01.01.2030.",
        "en": "National transposition by 26.07.2028. No size-based phase-in any more; the reporting "
              "duty under Art. 16 applies to financial years starting on or after 01.01.2030.",
        "es": "Transposición nacional hasta el 26.07.2028. Ya no hay introducción escalonada por tamaño; "
              "la obligación de informar del art. 16 se aplica a ejercicios que comiencen desde el 01.01.2030.",
        "fr": "Transposition nationale au plus tard le 26.07.2028. Plus d'introduction progressive selon la "
              "taille ; l'obligation de déclaration de l'art. 16 s'applique aux exercices ouverts à compter "
              "du 01.01.2030.",
        "it": "Recepimento nazionale entro il 26.07.2028. Non c'è più un'introduzione graduale per dimensione; "
              "l'obbligo di rendicontazione dell'art. 16 vale per esercizi che iniziano dal 01.01.2030.",
        "zh": "各成员国须于 2028 年 7 月 26 日前完成转化。不再按企业规模分阶段实施；第 16 条的报告义务适用于 2030 年 1 月 1 日或之后开始的财政年度。",
    },
    "csrd": {
        "de": "Die neuen Schwellen gelten für Geschäftsjahre, die am oder nach dem 01.01.2027 beginnen. "
              "Nationale Umsetzung bis 19.03.2027. Für die Geschäftsjahre 2025 und 2026 können die "
              "Mitgliedstaaten Unternehmen unterhalb der neuen Schwellen befreien.",
        "en": "The new thresholds apply to financial years starting on or after 01.01.2027. National "
              "transposition by 19.03.2027. For financial years 2025 and 2026, member states may exempt "
              "companies below the new thresholds.",
        "es": "Los nuevos umbrales se aplican a ejercicios que comiencen a partir del 01.01.2027. "
              "Transposición nacional hasta el 19.03.2027. Para los ejercicios 2025 y 2026 los Estados "
              "miembros pueden eximir a las empresas por debajo de los nuevos umbrales.",
        "fr": "Les nouveaux seuils s'appliquent aux exercices ouverts à compter du 01.01.2027. Transposition "
              "nationale au plus tard le 19.03.2027. Pour les exercices 2025 et 2026, les États membres "
              "peuvent exempter les entreprises situées sous les nouveaux seuils.",
        "it": "Le nuove soglie valgono per esercizi che iniziano dal 01.01.2027. Recepimento nazionale entro "
              "il 19.03.2027. Per gli esercizi 2025 e 2026 gli Stati membri possono esentare le imprese sotto "
              "le nuove soglie.",
        "zh": "新门槛适用于 2027 年 1 月 1 日或之后开始的财政年度。各成员国须于 2027 年 3 月 19 日前完成转化。对于 2025 和 2026 财政年度，成员国可豁免低于新门槛的企业。",
    },
    "entwurf_de": {
        "de": "Das deutsche Gesetzgebungsverfahren ist nicht abgeschlossen; § 289b HGB trägt weiterhin "
              "die Fassung des CSR-RUG.",
        "en": "The German legislative procedure is not completed; section 289b HGB still carries the "
              "CSR-RUG wording.",
        "es": "El procedimiento legislativo alemán no ha concluido; el § 289b HGB mantiene la redacción "
              "del CSR-RUG.",
        "fr": "La procédure législative allemande n'est pas achevée ; le § 289b HGB conserve la rédaction "
              "issue du CSR-RUG.",
        "it": "La procedura legislativa tedesca non è conclusa; il § 289b HGB conserva ancora il testo "
              "del CSR-RUG.",
        "zh": "德国立法程序尚未完成；《商法典》第 289b 条仍为 CSR-RUG 版本。",
    },
    "lksg": {
        "de": "Seit 01.01.2024 liegt der Schwellenwert bei 1.000 Arbeitnehmern im Inland (vorher 3.000).",
        "en": "Since 01.01.2024 the threshold is 1,000 employees in Germany (previously 3,000).",
        "es": "Desde el 01.01.2024 el umbral es de 1.000 empleados en Alemania (antes 3.000).",
        "fr": "Depuis le 01.01.2024, le seuil est de 1 000 salariés en Allemagne (auparavant 3 000).",
        "it": "Dal 01.01.2024 la soglia è di 1.000 dipendenti in Germania (prima 3.000).",
        "zh": "自 2024 年 1 月 1 日起，门槛为德国境内 1,000 名员工（此前为 3,000 名）。",
    },
    "eudr": {
        "de": "Für Kleinst- und Kleinunternehmen, die am 31.12.2024 bereits als solche niedergelassen waren, "
              "gilt die Verordnung erst ab 30.06.2027.",
        "en": "For micro and small operators already established as such on 31.12.2024, the regulation only "
              "applies from 30.06.2027.",
        "es": "Para microempresas y pequeñas empresas ya establecidas como tales el 31.12.2024, el reglamento "
              "se aplica solo a partir del 30.06.2027.",
        "fr": "Pour les micro et petites entreprises déjà établies comme telles au 31.12.2024, le règlement ne "
              "s'applique qu'à compter du 30.06.2027.",
        "it": "Per le microimprese e le piccole imprese già stabilite come tali al 31.12.2024 il regolamento "
              "si applica solo dal 30.06.2027.",
        "zh": "对于在 2024 年 12 月 31 日已作为微型或小型经营者设立的企业，本条例自 2027 年 6 月 30 日起才适用。",
    },
    "flr": {
        "de": "Einzelne Vorschriften (Aufbau von Datenbank, Leitlinien und Behördenstrukturen) gelten "
              "bereits seit 13.12.2024.",
        "en": "Individual provisions (database, guidelines and authority structures) have applied since "
              "13.12.2024.",
        "es": "Algunas disposiciones (base de datos, directrices y estructuras administrativas) se aplican "
              "desde el 13.12.2024.",
        "fr": "Certaines dispositions (base de données, lignes directrices et structures administratives) "
              "s'appliquent depuis le 13.12.2024.",
        "it": "Alcune disposizioni (banca dati, linee guida e strutture amministrative) si applicano già "
              "dal 13.12.2024.",
        "zh": "部分条款（数据库、指南和主管机关架构）自 2024 年 12 月 13 日起已适用。",
    },
    "nfrd": {
        "de": "Durch die CSRD abgelöst; für aktuelle Prüfungen in der Regel nicht mehr maßgeblich.",
        "en": "Superseded by the CSRD; as a rule no longer decisive for current assessments.",
        "es": "Sustituida por la CSRD; por regla general ya no es determinante.",
        "fr": "Remplacée par la CSRD ; en règle générale, plus déterminante aujourd'hui.",
        "it": "Sostituita dalla CSRD; di norma non più rilevante per le valutazioni attuali.",
        "zh": "已被 CSRD 取代；通常对当前评估不再具有决定意义。",
    },
    "csr_rug": {
        "de": "Gilt erstmals für Geschäftsjahre, die nach dem 31.12.2016 beginnen; wird durch die "
              "CSRD-Umsetzung abgelöst.",
        "en": "First applies to financial years starting after 31.12.2016; will be superseded by the CSRD "
              "transposition.",
        "es": "Se aplica por primera vez a ejercicios iniciados después del 31.12.2016; será sustituida por "
              "la transposición de la CSRD.",
        "fr": "S'applique pour la première fois aux exercices ouverts après le 31.12.2016 ; sera remplacée "
              "par la transposition de la CSRD.",
        "it": "Si applica per la prima volta agli esercizi che iniziano dopo il 31.12.2016; sarà sostituita "
              "dal recepimento della CSRD.",
        "zh": "首次适用于 2016 年 12 月 31 日之后开始的财政年度；将被 CSRD 的转化立法取代。",
    },
    "taxonomie": {
        "de": "Für die Umweltziele Klimaschutz und Anpassung seit 01.01.2022, für die übrigen vier "
              "Umweltziele seit 01.01.2023.",
        "en": "For the climate mitigation and adaptation objectives since 01.01.2022, for the other four "
              "environmental objectives since 01.01.2023.",
        "es": "Para los objetivos de mitigación y adaptación climática desde el 01.01.2022, para los otros "
              "cuatro objetivos medioambientales desde el 01.01.2023.",
        "fr": "Pour les objectifs d'atténuation et d'adaptation climatiques depuis le 01.01.2022, pour les "
              "quatre autres objectifs environnementaux depuis le 01.01.2023.",
        "it": "Per gli obiettivi di mitigazione e adattamento climatico dal 01.01.2022, per gli altri quattro "
              "obiettivi ambientali dal 01.01.2023.",
        "zh": "气候减缓与适应目标自 2022 年 1 月 1 日起适用，其余四项环境目标自 2023 年 1 月 1 日起适用。",
    },
    "oekodesign": {
        "de": "Rahmenverordnung: konkrete Produktanforderungen entstehen erst durch delegierte Rechtsakte "
              "je Produktgruppe.",
        "en": "Framework regulation: concrete product requirements only arise from delegated acts per "
              "product group.",
        "es": "Reglamento marco: los requisitos concretos de producto surgen solo de actos delegados por "
              "grupo de productos.",
        "fr": "Règlement-cadre : les exigences produits concrètes ne naissent que des actes délégués par "
              "groupe de produits.",
        "it": "Regolamento quadro: i requisiti concreti di prodotto derivano solo da atti delegati per "
              "gruppo di prodotti.",
        "zh": "框架性条例：具体产品要求须由针对各产品组的授权法案确定。",
    },
    "vernichtungsverbot": {
        "de": "Art. 6 der Delegierten Verordnung (EU) 2026/296; dasselbe Datum nennt Art. 25 Abs. 1 der "
              "Verordnung (EU) 2024/1781 für das Verbot selbst. Mittlere Unternehmen folgen am 19.07.2030, "
              "Kleinst- und Kleinunternehmen sind ausgenommen.",
        "en": "Art. 6 of Delegated Regulation (EU) 2026/296; Art. 25(1) of Regulation (EU) 2024/1781 "
              "gives the same date for the ban itself. Medium-sized companies follow on 19.07.2030, "
              "micro and small companies are exempt.",
        "es": "Art. 6 del Reglamento Delegado (UE) 2026/296; el art. 25, apdo. 1, del Reglamento (UE) "
              "2024/1781 fija la misma fecha para la propia prohibición. Las medianas empresas quedan "
              "sujetas el 19.07.2030 y las micro y pequeñas están exentas.",
        "fr": "Art. 6 du règlement délégué (UE) 2026/296 ; l'art. 25, par. 1, du règlement (UE) "
              "2024/1781 retient la même date pour l'interdiction elle-même. Les moyennes entreprises "
              "suivent le 19.07.2030, les micro et petites entreprises sont exclues.",
        "it": "Art. 6 del regolamento delegato (UE) 2026/296; l'art. 25, par. 1, del regolamento (UE) "
              "2024/1781 indica la stessa data per il divieto stesso. Le medie imprese seguono il "
              "19.07.2030, le micro e piccole imprese sono escluse.",
        "zh": "授权条例 (EU) 2026/296 第 6 条；条例 (EU) 2024/1781 第 25 条第 1 款就禁令本身规定了同一日期。中型企业自 2030 年 7 月 19 日起适用，微型和小型企业不受约束。",
    },
    "empco": {
        "de": "Ab diesem Tag wenden die Mitgliedstaaten die Vorschriften an; in Deutschland über das "
              "Gesetz gegen den unlauteren Wettbewerb (UWG).",
        "en": "From this date member states apply the rules; in Germany through the Act against Unfair "
              "Competition (UWG).",
        "es": "A partir de esta fecha los Estados miembros aplican las normas; en Alemania mediante la Ley "
              "contra la competencia desleal (UWG).",
        "fr": "À partir de cette date, les États membres appliquent les règles ; en Allemagne via la loi "
              "contre la concurrence déloyale (UWG).",
        "it": "Da questa data gli Stati membri applicano le norme; in Germania tramite la legge contro la "
              "concorrenza sleale (UWG).",
        "zh": "自该日起，各成员国开始适用相关规则；在德国通过《反不正当竞争法》(UWG) 实施。",
    },
    # --- Katalogerweiterung 29.09.2026 ---
    "reach17": {
        "de": "PFHxA (Eintrag 79) gilt ab 10.10.2026 für Bekleidung, Schuhe und Imprägniermittel für Verbraucher, ab 10.10.2027 für die übrigen Textilien; DMAC und NEP (Einträge 80 und 81) ab 23.12.2026.",
        "en": "PFHxA (entry 79) applies from 10.10.2026 to clothing, footwear and waterproofing agents for consumers, and from 10.10.2027 to other textiles; DMAC and NEP (entries 80 and 81) from 23.12.2026.",
        "es": "El PFHxA (entrada 79) se aplica desde el 10.10.2026 a ropa, calzado e impermeabilizantes para consumidores y desde el 10.10.2027 a los demás textiles; DMAC y NEP (entradas 80 y 81), desde el 23.12.2026.",
        "fr": "Le PFHxA (entrée 79) s'applique à compter du 10.10.2026 aux vêtements, chaussures et agents d'imperméabilisation destinés aux consommateurs, et à compter du 10.10.2027 aux autres textiles ; le DMAC et la NEP (entrées 80 et 81), à compter du 23.12.2026.",
        "it": "Il PFHxA (voce 79) si applica dal 10.10.2026 ad abbigliamento, calzature e impermeabilizzanti per i consumatori e dal 10.10.2027 agli altri tessili; DMAC e NEP (voci 80 e 81) dal 23.12.2026.",
        "zh": "PFHxA（第 79 项）自 2026 年 10 月 10 日起适用于面向消费者的服装、鞋类和防水剂，自 2027 年 10 月 10 日起适用于其他纺织品；DMAC 和 NEP（第 80 和 81 项）自 2026 年 12 月 23 日起适用。",
    },
    "tkvo": {
        "de": "Die EU-Kommission hat eine Überarbeitung angekündigt, unter anderem mit digitalem Etikett; ein Vorschlag lag im September 2026 noch nicht vor.",
        "en": "The European Commission has announced a revision, including a digital label; as of September 2026, no proposal had yet been presented.",
        "es": "La Comisión Europea ha anunciado una revisión que incluye, entre otras cosas, una etiqueta digital; en septiembre de 2026 todavía no se había presentado ninguna propuesta.",
        "fr": "La Commission européenne a annoncé une révision, prévoyant notamment une étiquette numérique ; en septembre 2026, aucune proposition n'avait encore été présentée.",
        "it": "La Commissione europea ha annunciato una revisione, che prevede tra l'altro un'etichetta digitale; a settembre 2026 non era ancora stata presentata alcuna proposta.",
        "zh": "欧盟委员会已宣布将进行修订，其中包括数字标签；截至 2026 年 9 月，尚未提出相关提案。",
    },
    "mdr": {
        "de": "Altprodukte mit Bescheinigung nach den früheren Richtlinien dürfen bis 31.12.2027 bzw. 31.12.2028 weiter in Verkehr gebracht werden (Art. 120). Eine gezielte Überarbeitung der MDR (COM(2025) 1023) ist vorgeschlagen, aber nicht beschlossen.",
        "en": "Legacy devices with a certificate under the former directives may continue to be placed on the market until 31.12.2027 or 31.12.2028 (Art. 120). A targeted revision of the MDR (COM(2025) 1023) has been proposed but not adopted.",
        "es": "Los productos con certificado conforme a las directivas anteriores pueden seguir introduciéndose en el mercado hasta el 31.12.2027 o el 31.12.2028 (art. 120). Se ha propuesto una revisión específica del MDR (COM(2025) 1023), pero no se ha adoptado.",
        "fr": "Les dispositifs existants munis d'un certificat délivré au titre des anciennes directives peuvent continuer à être mis sur le marché jusqu'au 31.12.2027 ou au 31.12.2028 (art. 120). Une révision ciblée du MDR (COM(2025) 1023) a été proposée, mais n'est pas adoptée.",
        "it": "I dispositivi con certificato rilasciato ai sensi delle precedenti direttive possono continuare a essere immessi sul mercato fino al 31.12.2027 o al 31.12.2028 (art. 120). È stata proposta una revisione mirata del MDR (COM(2025) 1023), ma non è stata adottata.",
        "zh": "持有原指令项下证书的既有器械，可在 2027 年 12 月 31 日或 2028 年 12 月 31 日前继续投放市场（第 120 条）。针对 MDR 的定向修订（COM(2025) 1023）已被提出，但尚未通过。",
    },
    "eprfr": {
        "de": "Seit 10.07.2026 brauchen Anbieter ohne Sitz in Frankreich einen Bevollmächtigten, seit 01.09.2026 gelten Maluszuschläge von 0,25 bis 12 EUR je Produkt. Das Werbeverbot für Ultra-Fast-Fashion ab 01.01.2027 nimmt Anbieter aus anderen EU-Staaten aus.",
        "en": "Since 10.07.2026, suppliers without a registered office in France have needed an authorised representative (mandataire); since 01.09.2026, malus surcharges of 0.25 to 12 EUR per product have applied. The advertising ban on ultra-fast fashion from 01.01.2027 exempts suppliers from other EU member states.",
        "es": "Desde el 10.07.2026, los proveedores sin domicilio social en Francia necesitan un representante autorizado (mandataire); desde el 01.09.2026 se aplican recargos malus de 0,25 a 12 EUR por producto. La prohibición de publicidad de la ultra fast fashion a partir del 01.01.2027 excluye a los proveedores de otros Estados miembros de la UE.",
        "fr": "Depuis le 10.07.2026, les fournisseurs sans siège en France doivent disposer d'un mandataire ; depuis le 01.09.2026, des pénalités (malus) de 0,25 à 12 EUR par produit s'appliquent. L'interdiction de la publicité pour la mode ultra-éphémère à compter du 01.01.2027 exclut les fournisseurs établis dans d'autres États membres de l'UE.",
        "it": "Dal 10.07.2026 i fornitori senza sede in Francia necessitano di un mandatario (mandataire); dal 01.09.2026 si applicano maggiorazioni malus da 0,25 a 12 EUR per prodotto. Il divieto di pubblicità per l'ultra fast fashion dal 01.01.2027 esclude i fornitori di altri Stati membri dell'UE.",
        "zh": "自 2026 年 7 月 10 日起，在法国没有注册地的供应商须指定授权代表（mandataire）；自 2026 年 9 月 1 日起，每件产品适用 0.25 至 12 欧元的惩罚性附加费（malus）。自 2027 年 1 月 1 日起实施的超快时尚广告禁令不适用于来自其他欧盟成员国的供应商。",
    },
    "eprnl": {
        "de": "Nach Angaben von Rijkswaterstaat sollen neue Regeln, die auch Schuhe erfassen, voraussichtlich ab Anfang 2028 gelten.",
        "en": "According to Rijkswaterstaat (Dutch government agency), new rules that also cover footwear are expected to apply from early 2028.",
        "es": "Según Rijkswaterstaat (organismo público neerlandés), se prevé que nuevas normas que abarcan también el calzado se apliquen a partir de principios de 2028.",
        "fr": "Selon Rijkswaterstaat (agence publique néerlandaise), de nouvelles règles couvrant également les chaussures devraient s'appliquer à partir de début 2028.",
        "it": "Secondo Rijkswaterstaat (agenzia pubblica olandese), nuove regole che riguardano anche le calzature dovrebbero applicarsi presumibilmente dall'inizio del 2028.",
        "zh": "据 Rijkswaterstaat（荷兰公共工程与水利管理局）称，涵盖鞋类在内的新规则预计将自 2028 年初起适用。",
    },
    "enefg": {
        "de": "Ein Regierungsentwurf (BT-Drs. 21/8027) sieht vor, die Schwelle für das Managementsystem auf 23,6 GWh anzuheben und Umsetzungspläne auf 2,77 bis 23,6 GWh zu beschränken; beschlossen ist das noch nicht.",
        "en": "A government bill (Bundestag printed paper BT-Drs. 21/8027) provides for raising the threshold for the management system to 23.6 GWh and limiting implementation plans to 2.77 to 23.6 GWh; this has not yet been adopted.",
        "es": "Un proyecto de ley del Gobierno (BT-Drs. 21/8027) prevé elevar el umbral para el sistema de gestión a 23,6 GWh y limitar los planes de ejecución al tramo de 2,77 a 23,6 GWh; todavía no se ha aprobado.",
        "fr": "Un projet de loi du gouvernement (BT-Drs. 21/8027) prévoit de relever le seuil applicable au système de management à 23,6 GWh et de limiter les plans de mise en œuvre à la tranche de 2,77 à 23,6 GWh ; il n'est pas encore adopté.",
        "it": "Un disegno di legge del governo (BT-Drs. 21/8027) prevede di innalzare la soglia per il sistema di gestione a 23,6 GWh e di limitare i piani di attuazione alla fascia tra 2,77 e 23,6 GWh; non è ancora stato approvato.",
        "zh": "一项政府草案（BT-Drs. 21/8027）拟将管理体系的门槛提高至 23.6 GWh，并将实施计划的适用范围限定在 2.77 至 23.6 GWh；该草案尚未通过。",
    },
}


# ---------- Erlaeuterungen zum unternehmensbezogenen Anwendungsbeginn ----------
# Schluessel entsprechen dem Feld "hinweis" aus `deadlines.deadline_for()`.
# Aufgeloest wird ueber `t_deadline_note()`: erst hier, dann in APPLIES_NOTES
# (fuer Regulierungen ohne Staffelung wird der Normhinweis durchgereicht).
DEADLINE_NOTES: dict[str, dict[str, str]] = {
    "lksg_stufe_3000": {
        "de": "Ab 3.000 Arbeitnehmern im Inland galt das Gesetz bereits seit dem 01.01.2023 "
              "(§ 1 Abs. 1 Satz 3 LkSG).",
        "en": "From 3,000 employees in Germany the act already applied from 01.01.2023 "
              "(section 1(1) sentence 3 LkSG).",
        "es": "A partir de 3.000 empleados en Alemania la ley ya se aplicaba desde el 01.01.2023 "
              "(§ 1, apdo. 1, frase 3 LkSG).",
        "fr": "À partir de 3 000 salariés en Allemagne, la loi s'appliquait déjà depuis le 01.01.2023 "
              "(§ 1, al. 1, phrase 3 LkSG).",
        "it": "Con almeno 3.000 dipendenti in Germania la legge si applicava già dal 01.01.2023 "
              "(§ 1, c. 1, per. 3 LkSG).",
        "zh": "德国境内员工达 3,000 人的企业，自 2023 年 1 月 1 日起即已适用（《供应链尽职调查法》第 1 条第 1 款第 3 句）。",
    },
    "lksg_stufe_1000": {
        "de": "Die Schwelle von 1.000 Arbeitnehmern im Inland gilt seit dem 01.01.2024 "
              "(§ 1 Abs. 1 Satz 3 LkSG); davor lag sie bei 3.000.",
        "en": "The threshold of 1,000 employees in Germany has applied since 01.01.2024 "
              "(section 1(1) sentence 3 LkSG); before that it was 3,000.",
        "es": "El umbral de 1.000 empleados en Alemania se aplica desde el 01.01.2024 "
              "(§ 1, apdo. 1, frase 3 LkSG); antes era de 3.000.",
        "fr": "Le seuil de 1 000 salariés en Allemagne s'applique depuis le 01.01.2024 "
              "(§ 1, al. 1, phrase 3 LkSG) ; il était auparavant de 3 000.",
        "it": "La soglia di 1.000 dipendenti in Germania vale dal 01.01.2024 "
              "(§ 1, c. 1, per. 3 LkSG); in precedenza era di 3.000.",
        "zh": "德国境内 1,000 名员工的门槛自 2024 年 1 月 1 日起适用（《供应链尽职调查法》第 1 条第 1 款第 3 句），此前为 3,000 人。",
    },
    "csrd_welle1": {
        "de": "Als großes Unternehmen von öffentlichem Interesse mit mehr als 500 Beschäftigten "
              "gehört das Unternehmen zur ersten Welle und berichtet seit dem Geschäftsjahr 2024. "
              "Ob der nationale Gesetzgeber für die Geschäftsjahre 2025 und 2026 befreit, ist zu prüfen.",
        "en": "As a large public-interest entity with more than 500 employees the company belongs to "
              "the first wave and has reported since financial year 2024. Whether the national "
              "legislator grants an exemption for financial years 2025 and 2026 needs to be checked.",
        "es": "Como entidad grande de interés público con más de 500 empleados, la empresa pertenece a "
              "la primera ola e informa desde el ejercicio 2024. Debe comprobarse si el legislador "
              "nacional concede una exención para los ejercicios 2025 y 2026.",
        "fr": "En tant que grande entité d'intérêt public de plus de 500 salariés, l'entreprise relève "
              "de la première vague et publie depuis l'exercice 2024. Il convient de vérifier si le "
              "législateur national accorde une exemption pour les exercices 2025 et 2026.",
        "it": "In quanto grande ente di interesse pubblico con più di 500 dipendenti, l'impresa "
              "appartiene alla prima ondata e rendiconta dall'esercizio 2024. Occorre verificare se il "
              "legislatore nazionale concede un'esenzione per gli esercizi 2025 e 2026.",
        "zh": "作为员工超过 500 人的大型公众利益实体，该企业属于第一批，自 2024 财政年度起报告。须核实本国立法者是否对 2025 和 2026 财政年度给予豁免。",
    },
    "csrd_drittland": {
        "de": "Für Drittland-Konzerne gilt der eigenständige Anwendungsbeginn des Art. 40a der "
              "Bilanzrichtlinie. Er hängt vom Aufbau der Gruppe ab und ist für den konkreten Fall "
              "zu prüfen.",
        "en": "Third-country groups fall under the separate start date of Art. 40a of the Accounting "
              "Directive. It depends on the group structure and has to be checked for the individual case.",
        "es": "Para los grupos de terceros países rige la fecha de aplicación específica del art. 40a de "
              "la Directiva contable. Depende de la estructura del grupo y debe comprobarse caso por caso.",
        "fr": "Pour les groupes de pays tiers s'applique la date d'entrée en application distincte de "
              "l'art. 40a de la directive comptable. Elle dépend de la structure du groupe et doit être "
              "vérifiée au cas par cas.",
        "it": "Per i gruppi di paesi terzi vale la data di applicazione autonoma dell'art. 40a della "
              "direttiva contabile. Dipende dalla struttura del gruppo e va verificata caso per caso.",
        "zh": "第三国集团适用《会计指令》第 40a 条单独规定的适用起始日，具体取决于集团结构，须逐案核实。",
    },
    "csrd_neue_schwellen": {
        "de": "Erstes Geschäftsjahr, das am oder nach dem 01.01.2027 beginnt; der Bericht erscheint "
              "im Folgejahr. Nationale Umsetzung bis 19.03.2027.",
        "en": "First financial year beginning on or after 01.01.2027; the report is published in the "
              "following year. National transposition by 19.03.2027.",
        "es": "Primer ejercicio que comience a partir del 01.01.2027; el informe se publica al año "
              "siguiente. Transposición nacional hasta el 19.03.2027.",
        "fr": "Premier exercice ouvert à compter du 01.01.2027 ; le rapport paraît l'année suivante. "
              "Transposition nationale au plus tard le 19.03.2027.",
        "it": "Primo esercizio che inizia dal 01.01.2027; la relazione è pubblicata l'anno successivo. "
              "Recepimento nazionale entro il 19.03.2027.",
        "zh": "自 2027 年 1 月 1 日或之后开始的第一个财政年度；报告于次年发布。各成员国须于 2027 年 3 月 19 日前完成转化。",
    },
    "vernichtung_gross": {
        "de": "Das Unternehmen gilt nach der Größeneinstufung nicht als klein oder mittel; damit greift "
              "das Verbot seit dem 19.07.2026 (Art. 25 Abs. 1 der Verordnung (EU) 2024/1781). Die "
              "Einstufung folgt der Empfehlung 2003/361/EG und ist anhand der eigenen Abschlusszahlen "
              "zu bestätigen.",
        "en": "By size classification the company does not count as small or medium-sized, so the ban "
              "has applied since 19.07.2026 (Art. 25(1) of Regulation (EU) 2024/1781). The "
              "classification follows Recommendation 2003/361/EC and should be confirmed against your "
              "own financial statements.",
        "es": "Según la clasificación por tamaño, la empresa no es pequeña ni mediana, por lo que la "
              "prohibición se aplica desde el 19.07.2026 (art. 25, apdo. 1, del Reglamento (UE) "
              "2024/1781). La clasificación sigue la Recomendación 2003/361/CE y debe confirmarse con "
              "las cuentas anuales propias.",
        "fr": "Selon le classement par taille, l'entreprise n'est ni petite ni moyenne : l'interdiction "
              "s'applique donc depuis le 19.07.2026 (art. 25, par. 1, du règlement (UE) 2024/1781). Le "
              "classement suit la recommandation 2003/361/CE et doit être confirmé au vu des comptes "
              "annuels.",
        "it": "In base alla classificazione dimensionale l'impresa non è piccola né media: il divieto si "
              "applica quindi dal 19.07.2026 (art. 25, par. 1, del regolamento (UE) 2024/1781). La "
              "classificazione segue la raccomandazione 2003/361/CE e va confermata sui propri bilanci.",
        "zh": "按规模分类，本企业不属于小型或中型企业，故自 2026 年 7 月 19 日起适用该禁令（条例 (EU) 2024/1781 第 25 条第 1 款）。分类依据建议 2003/361/EC，应结合本企业年度财务报表确认。",
    },
    "vernichtung_mittel": {
        "de": "Für mittlere Unternehmen gilt das Verbot erst ab dem 19.07.2030 (Art. 25 Abs. 1 UAbs. 3 "
              "der Verordnung (EU) 2024/1781); dasselbe gilt für die Offenlegung nach Art. 24. Die "
              "Größeneinstufung folgt der Empfehlung 2003/361/EG.",
        "en": "For medium-sized companies the ban applies only from 19.07.2030 (Art. 25(1) third "
              "subparagraph of Regulation (EU) 2024/1781); the same holds for the disclosure under "
              "Art. 24. The size classification follows Recommendation 2003/361/EC.",
        "es": "Para las medianas empresas la prohibición solo se aplica desde el 19.07.2030 (art. 25, "
              "apdo. 1, párr. 3, del Reglamento (UE) 2024/1781); lo mismo vale para la divulgación del "
              "art. 24. La clasificación por tamaño sigue la Recomendación 2003/361/CE.",
        "fr": "Pour les moyennes entreprises, l'interdiction ne s'applique qu'à partir du 19.07.2030 "
              "(art. 25, par. 1, al. 3, du règlement (UE) 2024/1781) ; il en va de même de la "
              "publication au titre de l'art. 24. Le classement par taille suit la recommandation "
              "2003/361/CE.",
        "it": "Per le medie imprese il divieto si applica solo dal 19.07.2030 (art. 25, par. 1, terzo "
              "comma, del regolamento (UE) 2024/1781); lo stesso vale per l'informativa ex art. 24. La "
              "classificazione dimensionale segue la raccomandazione 2003/361/CE.",
        "zh": "对中型企业，该禁令自 2030 年 7 月 19 日起才适用（条例 (EU) 2024/1781 第 25 条第 1 款第三项），第 24 条的披露义务同理。规模分类依据建议 2003/361/EC。",
    },
    "vernichtung_klein": {
        "de": "Auf Kleinst- und Kleinunternehmen finden weder das Verbot noch die Offenlegungspflicht "
              "Anwendung (Art. 25 Abs. 1 UAbs. 2 und Art. 24 Abs. 1 der Verordnung (EU) 2024/1781); "
              "deshalb gibt es keinen Anwendungsbeginn. Die Einstufung folgt der Empfehlung 2003/361/EG.",
        "en": "Neither the ban nor the disclosure duty applies to micro and small companies (Art. 25(1) "
              "second subparagraph and Art. 24(1) of Regulation (EU) 2024/1781), so there is no start "
              "date. The classification follows Recommendation 2003/361/EC.",
        "es": "Ni la prohibición ni la obligación de divulgación se aplican a las microempresas y "
              "pequeñas empresas (art. 25, apdo. 1, párr. 2, y art. 24, apdo. 1, del Reglamento (UE) "
              "2024/1781); por eso no hay fecha de inicio. La clasificación sigue la Recomendación "
              "2003/361/CE.",
        "fr": "Ni l'interdiction ni l'obligation de publication ne s'appliquent aux micro et petites "
              "entreprises (art. 25, par. 1, al. 2, et art. 24, par. 1, du règlement (UE) 2024/1781) ; "
              "il n'y a donc pas de date d'application. Le classement suit la recommandation 2003/361/CE.",
        "it": "Né il divieto né l'obbligo di informativa si applicano alle micro e piccole imprese "
              "(art. 25, par. 1, secondo comma, e art. 24, par. 1, del regolamento (UE) 2024/1781): non "
              "esiste quindi una data di applicazione. La classificazione segue la raccomandazione "
              "2003/361/CE.",
        "zh": "禁令与披露义务均不适用于微型和小型企业（条例 (EU) 2024/1781 第 25 条第 1 款第二项、第 24 条第 1 款），故无适用起始日。分类依据建议 2003/361/EC。",
    },
    "taxonomie_folgt_csrd": {
        "de": "Die Offenlegung nach Art. 8 knüpft an die Berichtspflicht an und beginnt mit dem "
              "ersten CSRD-pflichtigen Geschäftsjahr dieses Unternehmens.",
        "en": "Disclosure under Art. 8 follows the reporting obligation and starts with this company's "
              "first CSRD reporting year.",
        "es": "La divulgación del art. 8 se vincula a la obligación de informar y comienza con el primer "
              "ejercicio con obligación CSRD de esta empresa.",
        "fr": "La publication au titre de l'art. 8 suit l'obligation de reporting et commence avec le "
              "premier exercice soumis à la CSRD pour cette entreprise.",
        "it": "L'informativa ex art. 8 segue l'obbligo di rendicontazione e inizia con il primo esercizio "
              "soggetto a CSRD di questa impresa.",
        "zh": "第 8 条的披露义务依附于报告义务，自本企业首个负有 CSRD 报告义务的财政年度起开始。",
    },
    "taxonomie_finanz": {
        "de": "Für Finanzmarktteilnehmer gilt die Verordnung eigenständig: seit 01.01.2022 für "
              "Klimaschutz und Anpassung, seit 01.01.2023 für die übrigen vier Umweltziele.",
        "en": "For financial market participants the regulation applies in its own right: since "
              "01.01.2022 for climate mitigation and adaptation, since 01.01.2023 for the other four "
              "environmental objectives.",
        "es": "Para los participantes en los mercados financieros el reglamento se aplica de forma "
              "autónoma: desde el 01.01.2022 para mitigación y adaptación climática, desde el 01.01.2023 "
              "para los otros cuatro objetivos medioambientales.",
        "fr": "Pour les acteurs des marchés financiers, le règlement s'applique de façon autonome : "
              "depuis le 01.01.2022 pour l'atténuation et l'adaptation climatiques, depuis le 01.01.2023 "
              "pour les quatre autres objectifs environnementaux.",
        "it": "Per i partecipanti ai mercati finanziari il regolamento si applica in modo autonomo: dal "
              "01.01.2022 per mitigazione e adattamento climatico, dal 01.01.2023 per gli altri quattro "
              "obiettivi ambientali.",
        "zh": "对金融市场参与者，本条例独立适用：气候减缓与适应目标自 2022 年 1 月 1 日起，其余四项环境目标自 2023 年 1 月 1 日起。",
    },
    "hinschg_ab_250": {
        "de": "Beschäftigungsgeber mit mindestens 250 Beschäftigten mussten die interne Meldestelle "
              "mit Inkrafttreten des Gesetzes einrichten (§ 42 HinSchG).",
        "en": "Employers with at least 250 employees had to set up the internal reporting channel when "
              "the act entered into force (section 42 HinSchG).",
        "es": "Los empleadores con al menos 250 empleados debían crear el canal interno de denuncia al "
              "entrar en vigor la ley (§ 42 HinSchG).",
        "fr": "Les employeurs d'au moins 250 salariés devaient mettre en place le canal de signalement "
              "interne dès l'entrée en vigueur de la loi (§ 42 HinSchG).",
        "it": "I datori di lavoro con almeno 250 dipendenti dovevano istituire il canale di segnalazione "
              "interno all'entrata in vigore della legge (§ 42 HinSchG).",
        "zh": "员工至少 250 人的雇主须在该法生效时即设立内部举报渠道（《举报人保护法》第 42 条）。",
    },
    "hinschg_ab_50": {
        "de": "Für Beschäftigungsgeber mit 50 bis 249 Beschäftigten gilt die Pflicht zur internen "
              "Meldestelle erst seit dem 17.12.2023 (§ 42 HinSchG).",
        "en": "For employers with 50 to 249 employees the duty to set up an internal reporting channel "
              "has only applied since 17.12.2023 (section 42 HinSchG).",
        "es": "Para empleadores con 50 a 249 empleados la obligación de canal interno rige solo desde el "
              "17.12.2023 (§ 42 HinSchG).",
        "fr": "Pour les employeurs de 50 à 249 salariés, l'obligation de canal interne ne s'applique que "
              "depuis le 17.12.2023 (§ 42 HinSchG).",
        "it": "Per i datori di lavoro con 50-249 dipendenti l'obbligo del canale interno vale solo dal "
              "17.12.2023 (§ 42 HinSchG).",
        "zh": "对拥有 50 至 249 名员工的雇主，设立内部举报渠道的义务自 2023 年 12 月 17 日起才适用（《举报人保护法》第 42 条）。",
    },
    "hinschg_finanz": {
        "de": "Als Beschäftigungsgeber nach § 12 Abs. 3 HinSchG (u. a. Wertpapierdienstleistungs"
              "unternehmen, Institute, Kapitalverwaltungsgesellschaften, Versicherer) besteht die "
              "Pflicht unabhängig von der Zahl der Beschäftigten; die Übergangsfrist bis 17.12.2023 "
              "gilt für diese Gruppe ausdrücklich nicht (§ 42 Abs. 1 Satz 2 HinSchG).",
        "en": "As an employer under section 12(3) HinSchG (investment firms, credit institutions, "
              "capital management companies, insurers and others) the duty applies irrespective of the "
              "number of employees; the transitional period until 17.12.2023 expressly does not apply "
              "to this group (section 42(1) sentence 2 HinSchG).",
        "es": "Como empleador del § 12, apdo. 3, HinSchG (empresas de servicios de inversión, "
              "entidades, sociedades gestoras, aseguradoras y otras), la obligación rige con "
              "independencia del número de empleados; el periodo transitorio hasta el 17.12.2023 no se "
              "aplica expresamente a este grupo (§ 42, apdo. 1, frase 2 HinSchG).",
        "fr": "En tant qu'employeur visé au § 12, al. 3, HinSchG (entreprises d'investissement, "
              "établissements, sociétés de gestion, assureurs et autres), l'obligation s'applique "
              "indépendamment du nombre de salariés ; la période transitoire jusqu'au 17.12.2023 ne "
              "s'applique expressément pas à ce groupe (§ 42, al. 1, phrase 2 HinSchG).",
        "it": "In quanto datore di lavoro ai sensi del § 12, c. 3, HinSchG (imprese di investimento, "
              "istituti, società di gestione, assicuratori e altri), l'obbligo vale a prescindere dal "
              "numero di dipendenti; il periodo transitorio fino al 17.12.2023 espressamente non si "
              "applica a questo gruppo (§ 42, c. 1, per. 2 HinSchG).",
        "zh": "作为《举报人保护法》第 12 条第 3 款所列的雇主（证券服务机构、金融机构、资产管理公司、保险公司等），该义务不受员工人数限制；至 2023 年 12 月 17 日的过渡期明确不适用于该类雇主（第 42 条第 1 款第 2 句）。",
    },
    "eudr_klein": {
        "de": "Spätere Frist für Kleinst- und Kleinunternehmen, die am 31.12.2024 bereits als solche "
              "niedergelassen waren (Art. 38 Abs. 3). Ob das Unternehmen darunter fällt, hängt auch an "
              "der Bilanzsumme und ist zu prüfen.",
        "en": "Later deadline for micro and small operators already established as such on 31.12.2024 "
              "(Art. 38(3)). Whether the company qualifies also depends on its balance sheet total and "
              "has to be checked.",
        "es": "Plazo posterior para microempresas y pequeñas empresas ya establecidas como tales el "
              "31.12.2024 (art. 38, apdo. 3). Si la empresa entra en esa categoría depende también del "
              "balance total y debe comprobarse.",
        "fr": "Délai plus tardif pour les micro et petites entreprises déjà établies comme telles au "
              "31.12.2024 (art. 38, § 3). L'appartenance à cette catégorie dépend aussi du total du "
              "bilan et doit être vérifiée.",
        "it": "Termine posticipato per le microimprese e le piccole imprese già stabilite come tali al "
              "31.12.2024 (art. 38, c. 3). L'appartenenza a tale categoria dipende anche dal totale di "
              "bilancio e va verificata.",
        "zh": "对在 2024 年 12 月 31 日已作为微型或小型经营者设立的企业适用较晚期限（第 38 条第 3 款）。是否属于该类别还取决于资产负债表总额，须另行核实。",
    },
}


# ---------- Hinweise zur Schwellen-Naehe ----------
# Schluessel entsprechen `thresholds.near_thresholds()`. Platzhalter wie bei
# COUPLING_FACTS: {employees}, {employees_de}, {revenue}.
THRESHOLD_HINTS: dict[str, dict[str, str]] = {
    "lksg_knapp_darunter": {
        "de": "Mit {employees_de} Beschäftigten in Deutschland liegt das Unternehmen dicht unter der "
              "LkSG-Schwelle. Ab 1.000 Arbeitnehmern im Inland würde zusätzlich das "
              "Lieferkettensorgfaltspflichtengesetz greifen.",
        "en": "With {employees_de} employees in Germany the company is just below the LkSG threshold. "
              "From 1,000 employees in Germany the German Supply Chain Due Diligence Act would apply "
              "in addition.",
        "es": "Con {employees_de} empleados en Alemania la empresa está justo por debajo del umbral de "
              "la LkSG. A partir de 1.000 empleados en Alemania se aplicaría además la Ley alemana de "
              "diligencia debida en las cadenas de suministro.",
        "fr": "Avec {employees_de} salariés en Allemagne, l'entreprise se situe juste sous le seuil de "
              "la LkSG. À partir de 1 000 salariés en Allemagne, la loi allemande sur le devoir de "
              "vigilance s'appliquerait en plus.",
        "it": "Con {employees_de} dipendenti in Germania l'impresa è appena sotto la soglia della LkSG. "
              "Da 1.000 dipendenti in Germania si applicherebbe in aggiunta la legge tedesca sul dovere "
              "di diligenza nelle catene di fornitura.",
        "zh": "该企业在德国有 {employees_de} 名员工，略低于《供应链尽职调查法》门槛。德国境内员工达到 1,000 人时，还将适用该法。",
    },
    "lksg_knapp_darueber": {
        "de": "Mit {employees_de} Beschäftigten in Deutschland liegt das Unternehmen nur knapp über der "
              "LkSG-Schwelle von 1.000 Arbeitnehmern. Die Pflicht entfällt erst, wenn die Schwelle im "
              "vorangegangenen Kalenderjahr nicht mehr erreicht wurde.",
        "en": "With {employees_de} employees in Germany the company is only just above the LkSG "
              "threshold of 1,000. The obligation ends only once the threshold was no longer reached in "
              "the preceding calendar year.",
        "es": "Con {employees_de} empleados en Alemania la empresa está apenas por encima del umbral de "
              "1.000 de la LkSG. La obligación decae solo cuando el umbral ya no se alcanzó en el año "
              "natural anterior.",
        "fr": "Avec {employees_de} salariés en Allemagne, l'entreprise dépasse à peine le seuil de 1 000 "
              "de la LkSG. L'obligation ne cesse que lorsque le seuil n'a plus été atteint au cours de "
              "l'année civile précédente.",
        "it": "Con {employees_de} dipendenti in Germania l'impresa supera di poco la soglia di 1.000 "
              "della LkSG. L'obbligo decade solo quando la soglia non è più stata raggiunta nell'anno "
              "solare precedente.",
        "zh": "该企业在德国有 {employees_de} 名员工，仅略高于《供应链尽职调查法》1,000 人的门槛。只有在上一日历年度不再达到该门槛时，义务才会终止。",
    },
    "hinschg_knapp_darunter": {
        "de": "Mit {employees_de} Beschäftigten in Deutschland liegt das Unternehmen dicht unter der "
              "Schwelle des HinSchG. Ab 50 Beschäftigten wäre eine interne Meldestelle einzurichten.",
        "en": "With {employees_de} employees in Germany the company is just below the HinSchG threshold. "
              "From 50 employees an internal reporting channel would have to be set up.",
        "es": "Con {employees_de} empleados en Alemania la empresa está justo por debajo del umbral de "
              "la HinSchG. A partir de 50 empleados habría que crear un canal interno de denuncia.",
        "fr": "Avec {employees_de} salariés en Allemagne, l'entreprise se situe juste sous le seuil de "
              "la HinSchG. À partir de 50 salariés, un canal de signalement interne devrait être créé.",
        "it": "Con {employees_de} dipendenti in Germania l'impresa è appena sotto la soglia della "
              "HinSchG. Da 50 dipendenti occorrerebbe istituire un canale di segnalazione interno.",
        "zh": "该企业在德国有 {employees_de} 名员工，略低于《举报人保护法》门槛。达到 50 名员工时须设立内部举报渠道。",
    },
    "hinschg_knapp_darueber": {
        "de": "Mit {employees_de} Beschäftigten in Deutschland liegt das Unternehmen nur knapp über der "
              "Schwelle von 50 Beschäftigten; die interne Meldestelle ist damit verpflichtend.",
        "en": "With {employees_de} employees in Germany the company is only just above the threshold of "
              "50; the internal reporting channel is therefore mandatory.",
        "es": "Con {employees_de} empleados en Alemania la empresa está apenas por encima del umbral de "
              "50; el canal interno de denuncia es por tanto obligatorio.",
        "fr": "Avec {employees_de} salariés en Allemagne, l'entreprise dépasse à peine le seuil de 50 ; "
              "le canal de signalement interne est donc obligatoire.",
        "it": "Con {employees_de} dipendenti in Germania l'impresa supera di poco la soglia di 50; il "
              "canale di segnalazione interno è quindi obbligatorio.",
        "zh": "该企业在德国有 {employees_de} 名员工，仅略高于 50 人门槛，因此必须设立内部举报渠道。",
    },
    "csrd_knapp_darunter": {
        "de": "Das Unternehmen liegt mit {employees} Beschäftigten und {revenue} Nettoumsatzerlösen "
              "dicht an den CSRD-Schwellen. Werden mehr als 1.000 Beschäftigte UND mehr als "
              "450 Mio. EUR Umsatz erreicht, käme die Nachhaltigkeitsberichterstattung hinzu.",
        "en": "With {employees} employees and net turnover of {revenue} the company is close to the CSRD "
              "thresholds. If more than 1,000 employees AND more than EUR 450 million turnover are "
              "reached, sustainability reporting would apply in addition.",
        "es": "Con {employees} empleados y {revenue} de cifra de negocios neta la empresa está cerca de "
              "los umbrales de la CSRD. Si se superan 1.000 empleados Y 450 millones EUR de cifra de "
              "negocios, se añadiría la información sobre sostenibilidad.",
        "fr": "Avec {employees} salariés et un chiffre d'affaires net de {revenue}, l'entreprise est "
              "proche des seuils de la CSRD. Au-delà de 1 000 salariés ET de 450 millions EUR de chiffre "
              "d'affaires, le reporting de durabilité s'ajouterait.",
        "it": "Con {employees} dipendenti e ricavi netti di {revenue} l'impresa è vicina alle soglie "
              "della CSRD. Superando 1.000 dipendenti E 450 milioni di EUR di ricavi, si aggiungerebbe "
              "la rendicontazione di sostenibilità.",
        "zh": "该企业有 {employees} 名员工、净营业额 {revenue}，接近 CSRD 门槛。若员工超过 1,000 人且营业额超过 4.5 亿欧元，将另需履行可持续发展报告义务。",
    },
    "csrd_knapp_darueber": {
        "de": "Das Unternehmen überschreitet die CSRD-Schwellen ({employees} Beschäftigte, {revenue} "
              "Nettoumsatzerlöse) nur knapp. Maßgeblich ist der Bilanzstichtag; ein Rückgang kann die "
              "Pflicht wieder entfallen lassen.",
        "en": "The company exceeds the CSRD thresholds ({employees} employees, {revenue} net turnover) "
              "only narrowly. The balance sheet date is decisive; a decline can end the obligation again.",
        "es": "La empresa supera los umbrales de la CSRD ({employees} empleados, {revenue} de cifra de "
              "negocios neta) solo por poco. Es determinante la fecha de cierre del balance; un descenso "
              "puede hacer decaer la obligación.",
        "fr": "L'entreprise ne dépasse que de peu les seuils de la CSRD ({employees} salariés, {revenue} "
              "de chiffre d'affaires net). La date de clôture fait foi ; une baisse peut faire disparaître "
              "l'obligation.",
        "it": "L'impresa supera di poco le soglie della CSRD ({employees} dipendenti, {revenue} di ricavi "
              "netti). Fa fede la data di chiusura del bilancio; una diminuzione può far venire meno "
              "l'obbligo.",
        "zh": "该企业仅略微超过 CSRD 门槛（{employees} 名员工、净营业额 {revenue}）。以资产负债表日为准；数值回落可能使义务再次消失。",
    },
    "csddd_knapp_darunter": {
        "de": "Das Unternehmen liegt mit {employees} Beschäftigten und {revenue} Nettoumsatz dicht an "
              "den CSDDD-Schwellen. Werden mehr als 5.000 Beschäftigte UND mehr als 1.500 Mio. EUR "
              "weltweiter Nettoumsatz erreicht, käme die Sorgfaltspflichtenrichtlinie hinzu.",
        "en": "With {employees} employees and net turnover of {revenue} the company is close to the CSDDD "
              "thresholds. If more than 5,000 employees AND more than EUR 1,500 million worldwide net "
              "turnover are reached, the due diligence directive would apply in addition.",
        "es": "Con {employees} empleados y {revenue} de cifra de negocios neta la empresa está cerca de "
              "los umbrales de la CSDDD. Si se superan 5.000 empleados Y 1.500 millones EUR de cifra de "
              "negocios mundial, se añadiría la directiva de diligencia debida.",
        "fr": "Avec {employees} salariés et un chiffre d'affaires net de {revenue}, l'entreprise est "
              "proche des seuils de la CSDDD. Au-delà de 5 000 salariés ET de 1 500 millions EUR de "
              "chiffre d'affaires mondial, la directive sur le devoir de vigilance s'ajouterait.",
        "it": "Con {employees} dipendenti e ricavi netti di {revenue} l'impresa è vicina alle soglie della "
              "CSDDD. Superando 5.000 dipendenti E 1.500 milioni di EUR di ricavi netti mondiali, si "
              "aggiungerebbe la direttiva sul dovere di diligenza.",
        "zh": "该企业有 {employees} 名员工、净营业额 {revenue}，接近 CSDDD 门槛。若员工超过 5,000 人且全球净营业额超过 15 亿欧元，将另需适用尽职调查指令。",
    },
    "csddd_knapp_darueber": {
        "de": "Das Unternehmen überschreitet die CSDDD-Schwellen ({employees} Beschäftigte, {revenue} "
              "Nettoumsatz) nur knapp. Maßgeblich sind zwei aufeinanderfolgende Geschäftsjahre "
              "(Art. 2 Abs. 5).",
        "en": "The company exceeds the CSDDD thresholds ({employees} employees, {revenue} net turnover) "
              "only narrowly. Two consecutive financial years are decisive (Art. 2(5)).",
        "es": "La empresa supera los umbrales de la CSDDD ({employees} empleados, {revenue} de cifra de "
              "negocios) solo por poco. Son determinantes dos ejercicios consecutivos (art. 2, apdo. 5).",
        "fr": "L'entreprise ne dépasse que de peu les seuils de la CSDDD ({employees} salariés, {revenue} "
              "de chiffre d'affaires). Deux exercices consécutifs font foi (art. 2, § 5).",
        "it": "L'impresa supera di poco le soglie della CSDDD ({employees} dipendenti, {revenue} di "
              "ricavi). Fanno fede due esercizi consecutivi (art. 2, c. 5).",
        "zh": "该企业仅略微超过 CSDDD 门槛（{employees} 名员工、净营业额 {revenue}）。以连续两个财政年度为准（第 2 条第 5 款）。",
    },
    # --- Katalogerweiterung 29.09.2026 ---
    "enefg_2_5_knapp_darunter": {
        "de": "Mit {energy} Gesamtendenergieverbrauch pro Jahr liegt das Unternehmen dicht unter der Schwelle von 2,5 GWh. Darüber wären nach § 9 EnEfG Umsetzungspläne für wirtschaftliche Einsparmaßnahmen zu erstellen und zu veröffentlichen.",
        "en": "With a total final energy consumption of {energy} per year the company is just below the threshold of 2.5 GWh. Above it, implementation plans for economically viable energy-saving measures would have to be drawn up and published under Section 9 of the German Energy Efficiency Act (EnEfG).",
        "es": "Con un consumo total de energía final de {energy} al año la empresa está justo por debajo del umbral de 2,5 GWh. Por encima de él habría que elaborar y publicar, conforme al § 9 de la Ley alemana de eficiencia energética (EnEfG), planes de ejecución para medidas de ahorro económicamente viables.",
        "fr": "Avec une consommation totale d'énergie finale de {energy} par an, l'entreprise se situe juste sous le seuil de 2,5 GWh. Au-delà, des plans de mise en œuvre pour les mesures d'économie économiquement viables devraient être établis et publiés en vertu du § 9 de la loi allemande sur l'efficacité énergétique (EnEfG).",
        "it": "Con un consumo totale di energia finale di {energy} all'anno l'impresa è appena sotto la soglia di 2,5 GWh. Al di sopra si dovrebbero elaborare e pubblicare, ai sensi del § 9 della legge tedesca sull'efficienza energetica (EnEfG), piani di attuazione per misure di risparmio economicamente convenienti.",
        "zh": "该企业每年最终能源总消耗量为 {energy}，略低于 2.5 GWh 的门槛。超过该门槛时，须根据德国《能源效率法》（EnEfG）第 9 条为经济可行的节能措施制定并公布实施计划。",
    },
    "enefg_2_5_knapp_darueber": {
        "de": "Mit {energy} Gesamtendenergieverbrauch pro Jahr liegt das Unternehmen nur knapp über der Schwelle von 2,5 GWh für die Umsetzungspläne nach § 9 EnEfG. Maßgeblich ist der Durchschnitt der letzten drei abgeschlossenen Kalenderjahre.",
        "en": "With a total final energy consumption of {energy} per year the company is only just above the threshold of 2.5 GWh for the implementation plans under Section 9 of the German Energy Efficiency Act (EnEfG). The average of the last three completed calendar years is decisive.",
        "es": "Con un consumo total de energía final de {energy} al año la empresa está apenas por encima del umbral de 2,5 GWh para los planes de ejecución del § 9 de la Ley alemana de eficiencia energética (EnEfG). Es determinante la media de los tres últimos años naturales cerrados.",
        "fr": "Avec une consommation totale d'énergie finale de {energy} par an, l'entreprise dépasse à peine le seuil de 2,5 GWh applicable aux plans de mise en œuvre au titre du § 9 de la loi allemande sur l'efficacité énergétique (EnEfG). La moyenne des trois dernières années civiles clôturées est déterminante.",
        "it": "Con un consumo totale di energia finale di {energy} all'anno l'impresa supera di poco la soglia di 2,5 GWh per i piani di attuazione di cui al § 9 della legge tedesca sull'efficienza energetica (EnEfG). È determinante la media degli ultimi tre anni civili conclusi.",
        "zh": "该企业每年最终能源总消耗量为 {energy}，仅略高于德国《能源效率法》（EnEfG）第 9 条规定的实施计划 2.5 GWh 门槛。以最近三个已结束日历年的平均值为准。",
    },
    "enefg_7_5_knapp_darunter": {
        "de": "Mit {energy} Gesamtendenergieverbrauch pro Jahr liegt das Unternehmen dicht unter der Schwelle von 7,5 GWh. Darüber wäre nach § 8 EnEfG ein Energie- oder Umweltmanagementsystem einzurichten.",
        "en": "With a total final energy consumption of {energy} per year the company is just below the threshold of 7.5 GWh. Above it, an energy or environmental management system would have to be set up under Section 8 of the German Energy Efficiency Act (EnEfG).",
        "es": "Con un consumo total de energía final de {energy} al año la empresa está justo por debajo del umbral de 7,5 GWh. Por encima de él habría que implantar, conforme al § 8 de la Ley alemana de eficiencia energética (EnEfG), un sistema de gestión energética o ambiental.",
        "fr": "Avec une consommation totale d'énergie finale de {energy} par an, l'entreprise se situe juste sous le seuil de 7,5 GWh. Au-delà, un système de management de l'énergie ou de l'environnement devrait être mis en place en vertu du § 8 de la loi allemande sur l'efficacité énergétique (EnEfG).",
        "it": "Con un consumo totale di energia finale di {energy} all'anno l'impresa è appena sotto la soglia di 7,5 GWh. Al di sopra si dovrebbe introdurre, ai sensi del § 8 della legge tedesca sull'efficienza energetica (EnEfG), un sistema di gestione dell'energia o ambientale.",
        "zh": "该企业每年最终能源总消耗量为 {energy}，略低于 7.5 GWh 的门槛。超过该门槛时，须根据德国《能源效率法》（EnEfG）第 8 条建立能源或环境管理体系。",
    },
    "enefg_7_5_knapp_darueber": {
        "de": "Mit {energy} Gesamtendenergieverbrauch pro Jahr liegt das Unternehmen nur knapp über der Schwelle von 7,5 GWh für das Managementsystem nach § 8 EnEfG. Eine Novelle im Bundestag sieht vor, diese Schwelle auf 23,6 GWh anzuheben.",
        "en": "With a total final energy consumption of {energy} per year the company is only just above the threshold of 7.5 GWh for the management system under Section 8 of the German Energy Efficiency Act (EnEfG). An amendment before the Bundestag provides for raising this threshold to 23.6 GWh.",
        "es": "Con un consumo total de energía final de {energy} al año la empresa está apenas por encima del umbral de 7,5 GWh para el sistema de gestión del § 8 de la Ley alemana de eficiencia energética (EnEfG). Una reforma en trámite en el Bundestag prevé elevar este umbral a 23,6 GWh.",
        "fr": "Avec une consommation totale d'énergie finale de {energy} par an, l'entreprise dépasse à peine le seuil de 7,5 GWh applicable au système de management au titre du § 8 de la loi allemande sur l'efficacité énergétique (EnEfG). Une réforme examinée au Bundestag prévoit de relever ce seuil à 23,6 GWh.",
        "it": "Con un consumo totale di energia finale di {energy} all'anno l'impresa supera di poco la soglia di 7,5 GWh per il sistema di gestione di cui al § 8 della legge tedesca sull'efficienza energetica (EnEfG). Una riforma all'esame del Bundestag prevede di innalzare questa soglia a 23,6 GWh.",
        "zh": "该企业每年最终能源总消耗量为 {energy}，仅略高于德国《能源效率法》（EnEfG）第 8 条规定的管理体系 7.5 GWh 门槛。联邦议院正在审议的一项修正案拟将该门槛提高至 23.6 GWh。",
    },
}


# ---------- Erste Schritte je Regulierung ----------
# Schluessel entsprechen `regulations.FIRST_STEPS_BY_REG_KEY`. Kuratiert und
# handgeschrieben, NICHT vom LLM erzeugt; die Fundstelle steht jeweils im Text.
# Der weiterfuehrende Link kommt aus GUIDELINES_BY_REG_KEY.
FIRST_STEPS: dict[str, dict[str, str]] = {
    # --- CSDDD ---
    "csddd_1": {
        "de": "Sorgfaltspflichten in die Unternehmenspolitik einbetten und ein Konzept samt "
              "Verhaltenskodex verabschieden (Art. 5, 7).",
        "en": "Embed due diligence in company policy and adopt a policy including a code of conduct "
              "(Art. 5, 7).",
        "es": "Integrar la diligencia debida en la política de la empresa y adoptar una política con "
              "código de conducta (art. 5, 7).",
        "fr": "Intégrer le devoir de vigilance dans la politique de l'entreprise et adopter une "
              "politique assortie d'un code de conduite (art. 5, 7).",
        "it": "Integrare il dovere di diligenza nelle politiche aziendali e adottare una policy con "
              "codice di condotta (art. 5, 7).",
        "zh": "将尽职调查纳入企业政策，并制定含行为准则的方针（第 5、7 条）。",
    },
    "csddd_2": {
        "de": "Tatsächliche und potenzielle negative Auswirkungen in der eigenen Tätigkeitskette "
              "ermitteln und nach Schwere und Eintrittswahrscheinlichkeit priorisieren (Art. 8, 9).",
        "en": "Identify actual and potential adverse impacts in the chain of activities and prioritise "
              "them by severity and likelihood (Art. 8, 9).",
        "es": "Identificar los impactos adversos reales y potenciales en la cadena de actividades y "
              "priorizarlos según gravedad y probabilidad (art. 8, 9).",
        "fr": "Identifier les incidences négatives réelles et potentielles dans la chaîne d'activités et "
              "les hiérarchiser selon leur gravité et leur probabilité (art. 8, 9).",
        "it": "Individuare gli impatti negativi effettivi e potenziali nella catena di attività e "
              "classificarli per gravità e probabilità (art. 8, 9).",
        "zh": "识别自身活动链中实际与潜在的负面影响，并按严重性和发生可能性排序（第 8、9 条）。",
    },
    "csddd_3": {
        "de": "Melde- und Beschwerdeverfahren einrichten, das auch Betroffenen außerhalb des "
              "Unternehmens offensteht (Art. 14).",
        "en": "Set up a notification and complaints procedure that is also open to affected persons "
              "outside the company (Art. 14).",
        "es": "Establecer un procedimiento de notificación y reclamación abierto también a las personas "
              "afectadas ajenas a la empresa (art. 14).",
        "fr": "Mettre en place une procédure de signalement et de plainte ouverte aussi aux personnes "
              "concernées extérieures à l'entreprise (art. 14).",
        "it": "Istituire una procedura di segnalazione e reclamo aperta anche alle persone interessate "
              "esterne all'impresa (art. 14).",
        "zh": "建立通报和申诉程序，并向企业外部的受影响人员开放（第 14 条）。",
    },
    "csddd_4": {
        "de": "Klimaübergangsplan zur Begrenzung der Erwärmung auf 1,5 °C vorbereiten (Art. 22).",
        "en": "Prepare a climate transition plan aligned with limiting warming to 1.5 °C (Art. 22).",
        "es": "Preparar un plan de transición climática para limitar el calentamiento a 1,5 °C (art. 22).",
        "fr": "Préparer un plan de transition climatique visant à limiter le réchauffement à 1,5 °C "
              "(art. 22).",
        "it": "Predisporre un piano di transizione climatica per limitare il riscaldamento a 1,5 °C "
              "(art. 22).",
        "zh": "编制将升温控制在 1.5 °C 以内的气候转型计划（第 22 条）。",
    },
    # --- LkSG ---
    "lksg_1": {
        "de": "Zuständigkeit festlegen: Menschenrechtsbeauftragten benennen und das Risikomanagement "
              "in die Abläufe einbetten (§ 4).",
        "en": "Assign responsibility: appoint a human rights officer and embed risk management in "
              "business processes (section 4).",
        "es": "Definir responsabilidades: nombrar un responsable de derechos humanos e integrar la "
              "gestión de riesgos en los procesos (§ 4).",
        "fr": "Définir les responsabilités : désigner un responsable des droits humains et intégrer la "
              "gestion des risques dans les processus (§ 4).",
        "it": "Definire le responsabilità: nominare un responsabile per i diritti umani e integrare la "
              "gestione dei rischi nei processi (§ 4).",
        "zh": "明确职责：任命人权事务专员，并将风险管理嵌入业务流程（第 4 条）。",
    },
    "lksg_2": {
        "de": "Jährliche und anlassbezogene Risikoanalyse für den eigenen Geschäftsbereich und die "
              "unmittelbaren Zulieferer durchführen (§ 5).",
        "en": "Carry out an annual and ad hoc risk analysis for the company's own operations and its "
              "direct suppliers (section 5).",
        "es": "Realizar un análisis de riesgos anual y ad hoc para el propio ámbito de negocio y los "
              "proveedores directos (§ 5).",
        "fr": "Réaliser une analyse de risques annuelle et ponctuelle pour son propre domaine d'activité "
              "et ses fournisseurs directs (§ 5).",
        "it": "Effettuare un'analisi dei rischi annuale e ad hoc per il proprio ambito aziendale e i "
              "fornitori diretti (§ 5).",
        "zh": "对自身经营范围和直接供应商开展年度及触发式风险分析（第 5 条）。",
    },
    "lksg_3": {
        "de": "Grundsatzerklärung zur Menschenrechtsstrategie verabschieden und Präventionsmaßnahmen "
              "im eigenen Geschäftsbereich und gegenüber Zulieferern verankern (§ 6).",
        "en": "Adopt a policy statement on the human rights strategy and anchor preventive measures "
              "internally and towards suppliers (section 6).",
        "es": "Adoptar una declaración de principios sobre la estrategia de derechos humanos y anclar "
              "medidas preventivas internamente y frente a los proveedores (§ 6).",
        "fr": "Adopter une déclaration de principe sur la stratégie en matière de droits humains et "
              "ancrer des mesures de prévention en interne et auprès des fournisseurs (§ 6).",
        "it": "Adottare una dichiarazione di principio sulla strategia per i diritti umani e radicare "
              "misure preventive internamente e verso i fornitori (§ 6).",
        "zh": "通过人权战略原则声明，并在自身经营范围内及对供应商落实预防措施（第 6 条）。",
    },
    "lksg_4": {
        "de": "Beschwerdeverfahren einrichten, die Umsetzung fortlaufend dokumentieren und den "
              "Jahresbericht beim BAFA einreichen (§§ 8, 10).",
        "en": "Set up a complaints procedure, document implementation continuously and file the annual "
              "report with BAFA (sections 8, 10).",
        "es": "Establecer un procedimiento de reclamación, documentar la aplicación de forma continua y "
              "presentar el informe anual ante la BAFA (§§ 8, 10).",
        "fr": "Mettre en place une procédure de plainte, documenter la mise en œuvre en continu et "
              "déposer le rapport annuel auprès de la BAFA (§§ 8, 10).",
        "it": "Istituire una procedura di reclamo, documentare l'attuazione in modo continuativo e "
              "presentare la relazione annuale alla BAFA (§§ 8, 10).",
        "zh": "建立申诉程序，持续记录落实情况，并向联邦经济和出口管制局提交年度报告（第 8、10 条）。",
    },
    # --- EUDR ---
    "eudr_1": {
        "de": "Prüfen, welche Erzeugnisse unter Anhang I fallen und ob das Unternehmen als "
              "Marktteilnehmer oder als Händler auftritt (Art. 2, 4, 5).",
        "en": "Check which products fall under Annex I and whether the company acts as an operator or "
              "as a trader (Art. 2, 4, 5).",
        "es": "Comprobar qué productos entran en el anexo I y si la empresa actúa como operador o como "
              "comerciante (art. 2, 4, 5).",
        "fr": "Vérifier quels produits relèvent de l'annexe I et si l'entreprise agit en tant "
              "qu'opérateur ou que commerçant (art. 2, 4, 5).",
        "it": "Verificare quali prodotti rientrano nell'allegato I e se l'impresa opera come operatore o "
              "come commerciante (art. 2, 4, 5).",
        "zh": "确认哪些产品属于附件一范围，以及企业是作为经营者还是贸易商（第 2、4、5 条）。",
    },
    "eudr_2": {
        "de": "Von den Lieferanten Geolokalisationsdaten der Erzeugungsflächen und Angaben zur "
              "Rechtmäßigkeit der Erzeugung einholen (Art. 9).",
        "en": "Obtain geolocation data of the plots of production and evidence of legal production from "
              "suppliers (Art. 9).",
        "es": "Obtener de los proveedores los datos de geolocalización de las parcelas de producción y "
              "pruebas de la legalidad de la producción (art. 9).",
        "fr": "Obtenir des fournisseurs les données de géolocalisation des parcelles de production et "
              "les preuves de la légalité de la production (art. 9).",
        "it": "Ottenere dai fornitori i dati di geolocalizzazione degli appezzamenti di produzione e le "
              "prove della legalità della produzione (art. 9).",
        "zh": "向供应商获取生产地块的地理位置数据及生产合法性证明（第 9 条）。",
    },
    "eudr_3": {
        "de": "Risikobewertung und Risikominderung dokumentieren; solange kein vernachlässigbares "
              "Risiko besteht, darf die Ware nicht in Verkehr gebracht werden (Art. 10, 11).",
        "en": "Document risk assessment and risk mitigation; as long as the risk is not negligible the "
              "goods must not be placed on the market (Art. 10, 11).",
        "es": "Documentar la evaluación y la reducción del riesgo; mientras el riesgo no sea "
              "insignificante, la mercancía no puede comercializarse (art. 10, 11).",
        "fr": "Documenter l'évaluation et l'atténuation des risques ; tant que le risque n'est pas "
              "négligeable, la marchandise ne peut pas être mise sur le marché (art. 10, 11).",
        "it": "Documentare la valutazione e l'attenuazione del rischio; finché il rischio non è "
              "trascurabile la merce non può essere immessa sul mercato (art. 10, 11).",
        "zh": "记录风险评估与风险缓解措施；风险未达到可忽略水平前，不得将货物投放市场（第 10、11 条）。",
    },
    "eudr_4": {
        "de": "Sorgfaltserklärung vor dem Inverkehrbringen im Informationssystem der Kommission "
              "abgeben (Art. 4, 33).",
        "en": "Submit the due diligence statement in the Commission's information system before placing "
              "goods on the market (Art. 4, 33).",
        "es": "Presentar la declaración de diligencia debida en el sistema de información de la Comisión "
              "antes de la comercialización (art. 4, 33).",
        "fr": "Déposer la déclaration de diligence raisonnable dans le système d'information de la "
              "Commission avant la mise sur le marché (art. 4, 33).",
        "it": "Presentare la dichiarazione di dovuta diligenza nel sistema informativo della Commissione "
              "prima dell'immissione sul mercato (art. 4, 33).",
        "zh": "在投放市场前于欧盟委员会信息系统提交尽职调查声明（第 4、33 条）。",
    },
    # --- FLR (Zwangsarbeitsverordnung) ---
    "flr_1": {
        "de": "Produkte und Vorstufen aus Regionen mit erhöhtem Zwangsarbeitsrisiko identifizieren; "
              "die Verordnung begründet keine eigene Sorgfaltspflicht, verbietet aber das "
              "Inverkehrbringen (Art. 3).",
        "en": "Identify products and inputs from regions with an elevated forced labour risk; the "
              "regulation creates no due diligence duty of its own but prohibits placing such goods on "
              "the market (Art. 3).",
        "es": "Identificar productos e insumos procedentes de regiones con mayor riesgo de trabajo "
              "forzoso; el reglamento no crea un deber de diligencia propio, pero prohíbe su "
              "comercialización (art. 3).",
        "fr": "Identifier les produits et intrants provenant de régions à risque élevé de travail forcé ; "
              "le règlement ne crée pas d'obligation de vigilance propre mais interdit la mise sur le "
              "marché (art. 3).",
        "it": "Individuare prodotti e semilavorati provenienti da regioni ad alto rischio di lavoro "
              "forzato; il regolamento non crea un obbligo di diligenza autonomo ma vieta l'immissione "
              "sul mercato (art. 3).",
        "zh": "识别来自强迫劳动高风险地区的产品和上游投入；该条例不设立独立的尽职调查义务，但禁止相关产品投放市场（第 3 条）。",
    },
    "flr_2": {
        "de": "Die Datenbank und die Leitlinien der Kommission zu Risikogebieten und -produkten "
              "auswerten (Art. 8, 11).",
        "en": "Evaluate the Commission's database and guidelines on risk areas and products (Art. 8, 11).",
        "es": "Analizar la base de datos y las directrices de la Comisión sobre zonas y productos de "
              "riesgo (art. 8, 11).",
        "fr": "Exploiter la base de données et les lignes directrices de la Commission sur les zones et "
              "produits à risque (art. 8, 11).",
        "it": "Analizzare la banca dati e le linee guida della Commissione su aree e prodotti a rischio "
              "(art. 8, 11).",
        "zh": "研判欧盟委员会关于风险地区和风险产品的数据库与指南（第 8、11 条）。",
    },
    "flr_3": {
        "de": "Nachweise zur Lieferkette so vorhalten, dass Auskunftsersuchen der Behörden fristgerecht "
              "beantwortet werden können (Art. 17).",
        "en": "Keep supply chain evidence ready so that authorities' requests for information can be "
              "answered within the deadline (Art. 17).",
        "es": "Mantener disponibles las pruebas de la cadena de suministro para responder en plazo a "
              "los requerimientos de las autoridades (art. 17).",
        "fr": "Conserver les preuves relatives à la chaîne d'approvisionnement afin de répondre dans les "
              "délais aux demandes des autorités (art. 17).",
        "it": "Tenere pronte le prove sulla catena di fornitura per rispondere nei termini alle richieste "
              "delle autorità (art. 17).",
        "zh": "备妥供应链证明材料，以便在期限内回应主管机关的问询（第 17 条）。",
    },
    # --- CSRD ---
    "csrd_1": {
        "de": "Doppelte Wesentlichkeitsanalyse durchführen: Auswirkungen des Unternehmens und "
              "finanzielle Risiken gleichermaßen bewerten (ESRS 1, Kapitel 3).",
        "en": "Carry out a double materiality assessment: evaluate the company's impacts and its "
              "financial risks alike (ESRS 1, chapter 3).",
        "es": "Realizar un análisis de doble materialidad: evaluar por igual los impactos de la empresa "
              "y los riesgos financieros (ESRS 1, capítulo 3).",
        "fr": "Réaliser une analyse de double matérialité : évaluer à parts égales les incidences de "
              "l'entreprise et les risques financiers (ESRS 1, chapitre 3).",
        "it": "Effettuare un'analisi di doppia materialità: valutare allo stesso modo gli impatti "
              "dell'impresa e i rischi finanziari (ESRS 1, capitolo 3).",
        "zh": "开展双重重要性分析：同等评估企业的影响与财务风险（ESRS 1 第 3 章）。",
    },
    "csrd_2": {
        "de": "Datenerhebung entlang der wesentlichen ESRS-Datenpunkte aufbauen und Zuständigkeiten, "
              "Quellen und Systeme festlegen.",
        "en": "Build data collection along the material ESRS data points and define responsibilities, "
              "sources and systems.",
        "es": "Construir la recogida de datos siguiendo los puntos de datos ESRS materiales y definir "
              "responsabilidades, fuentes y sistemas.",
        "fr": "Mettre en place la collecte de données selon les points de données ESRS matériels et "
              "définir responsabilités, sources et systèmes.",
        "it": "Impostare la raccolta dati lungo i data point ESRS materiali e definire responsabilità, "
              "fonti e sistemi.",
        "zh": "围绕重要的 ESRS 数据点建立数据采集，明确职责、数据来源与系统。",
    },
    "csrd_3": {
        "de": "Prüfbereitschaft herstellen: Die Nachhaltigkeitsberichterstattung wird mit begrenzter "
              "Sicherheit geprüft (Art. 34 Bilanzrichtlinie).",
        "en": "Prepare for assurance: sustainability reporting is subject to limited assurance (Art. 34 "
              "of the Accounting Directive).",
        "es": "Prepararse para la verificación: la información de sostenibilidad se verifica con "
              "seguridad limitada (art. 34 de la Directiva contable).",
        "fr": "Se préparer à l'assurance : le reporting de durabilité fait l'objet d'une assurance "
              "limitée (art. 34 de la directive comptable).",
        "it": "Prepararsi all'attestazione: la rendicontazione di sostenibilità è soggetta ad assurance "
              "limitata (art. 34 della direttiva contabile).",
        "zh": "做好鉴证准备：可持续发展报告须接受有限保证鉴证（《会计指令》第 34 条）。",
    },
    "csrd_4": {
        "de": "Bericht als eigenen Abschnitt des Lageberichts erstellen und im einheitlichen "
              "elektronischen Berichtsformat auszeichnen (Art. 29d).",
        "en": "Produce the report as a dedicated section of the management report and tag it in the "
              "single electronic reporting format (Art. 29d).",
        "es": "Elaborar el informe como sección propia del informe de gestión y etiquetarlo en el "
              "formato electrónico único (art. 29d).",
        "fr": "Établir le rapport comme section distincte du rapport de gestion et le baliser au format "
              "électronique unique (art. 29d).",
        "it": "Redigere la relazione come sezione autonoma della relazione sulla gestione e marcarla nel "
              "formato elettronico unico (art. 29d).",
        "zh": "将报告作为管理报告的独立章节编制，并按统一电子报告格式进行标记（第 29d 条）。",
    },
    # --- CSRD-Umsetzungsgesetz (DE) ---
    "csrd_de_1": {
        "de": "Verfahren beobachten: Bis zur Verkündung gilt § 289b HGB in der Fassung des CSR-RUG.",
        "en": "Monitor the legislative procedure: until promulgation, section 289b HGB applies in its "
              "CSR-RUG wording.",
        "es": "Seguir el procedimiento legislativo: hasta la promulgación rige el § 289b HGB en la "
              "redacción del CSR-RUG.",
        "fr": "Suivre la procédure législative : jusqu'à la promulgation, le § 289b HGB s'applique dans "
              "sa rédaction issue du CSR-RUG.",
        "it": "Seguire l'iter legislativo: fino alla promulgazione vale il § 289b HGB nella formulazione "
              "del CSR-RUG.",
        "zh": "关注立法进程：在公布之前，《商法典》第 289b 条仍适用 CSR-RUG 版本。",
    },
    "csrd_de_2": {
        "de": "Vorarbeiten an den ESRS ausrichten — der Entwurf übernimmt die europäischen Standards "
              "unverändert.",
        "en": "Align preparatory work with the ESRS — the draft adopts the European standards unchanged.",
        "es": "Orientar los trabajos preparatorios a los ESRS: el proyecto adopta sin cambios las normas "
              "europeas.",
        "fr": "Orienter les travaux préparatoires sur les ESRS : le projet reprend les normes "
              "européennes sans modification.",
        "it": "Orientare i lavori preparatori agli ESRS: la bozza recepisce senza modifiche gli standard "
              "europei.",
        "zh": "前期准备工作以 ESRS 为准——草案原样采纳欧洲标准。",
    },
    "csrd_de_3": {
        "de": "Prüfungsmandat frühzeitig klären (Abschlussprüfer oder unabhängiger Erbringer von "
              "Bestätigungsleistungen).",
        "en": "Clarify the assurance mandate early (statutory auditor or independent assurance services "
              "provider).",
        "es": "Aclarar pronto el mandato de verificación (auditor legal o proveedor independiente de "
              "servicios de aseguramiento).",
        "fr": "Clarifier rapidement le mandat d'assurance (commissaire aux comptes ou prestataire "
              "indépendant de services d'assurance).",
        "it": "Chiarire per tempo il mandato di assurance (revisore legale o fornitore indipendente di "
              "servizi di attestazione).",
        "zh": "尽早明确鉴证委托对象（法定审计师或独立鉴证服务提供者）。",
    },
    # --- NFRD ---
    "nfrd_1": {
        "de": "Prüfen, ob für zurückliegende Geschäftsjahre noch eine nichtfinanzielle Erklärung "
              "offen ist.",
        "en": "Check whether a non-financial statement is still outstanding for past financial years.",
        "es": "Comprobar si queda pendiente un estado no financiero de ejercicios anteriores.",
        "fr": "Vérifier si une déclaration non financière reste due pour des exercices antérieurs.",
        "it": "Verificare se resta da presentare una dichiarazione non finanziaria per esercizi passati.",
        "zh": "核查以往财政年度是否仍有未提交的非财务报表。",
    },
    "nfrd_2": {
        "de": "Umstellung auf die Berichterstattung nach CSRD und ESRS planen; die NFRD ist dadurch "
              "abgelöst.",
        "en": "Plan the switch to reporting under CSRD and ESRS; the NFRD has been superseded by them.",
        "es": "Planificar el cambio a la información según CSRD y ESRS; la NFRD queda sustituida.",
        "fr": "Planifier le passage au reporting selon la CSRD et les ESRS ; la NFRD est remplacée.",
        "it": "Pianificare il passaggio alla rendicontazione secondo CSRD ed ESRS; la NFRD è superata.",
        "zh": "规划向 CSRD 与 ESRS 报告体系的过渡；NFRD 已被取代。",
    },
    # --- CSR-RUG ---
    "csr_rug_1": {
        "de": "Prüfen, ob für das laufende Geschäftsjahr noch eine nichtfinanzielle Erklärung nach "
              "§ 289b HGB abzugeben ist.",
        "en": "Check whether a non-financial statement under section 289b HGB is still due for the "
              "current financial year.",
        "es": "Comprobar si para el ejercicio en curso sigue siendo obligatorio un estado no financiero "
              "según el § 289b HGB.",
        "fr": "Vérifier si une déclaration non financière au titre du § 289b HGB est encore due pour "
              "l'exercice en cours.",
        "it": "Verificare se per l'esercizio in corso sia ancora dovuta una dichiarazione non finanziaria "
              "ai sensi del § 289b HGB.",
        "zh": "核查本财政年度是否仍须依《商法典》第 289b 条提交非财务报表。",
    },
    "csr_rug_2": {
        "de": "Rahmenwerk benennen und die Prüfung durch den Aufsichtsrat sicherstellen "
              "(§ 171 Abs. 1 Satz 4 AktG).",
        "en": "Name the framework used and ensure the supervisory board's review (section 171(1) "
              "sentence 4 AktG).",
        "es": "Indicar el marco utilizado y asegurar el examen por el consejo de vigilancia "
              "(§ 171, apdo. 1, frase 4 AktG).",
        "fr": "Indiquer le référentiel utilisé et assurer l'examen par le conseil de surveillance "
              "(§ 171, al. 1, phrase 4 AktG).",
        "it": "Indicare il framework utilizzato e garantire l'esame da parte del consiglio di "
              "sorveglianza (§ 171, c. 1, per. 4 AktG).",
        "zh": "说明所采用的框架，并确保监事会进行审查（《股份公司法》第 171 条第 1 款第 4 句）。",
    },
    "csr_rug_3": {
        "de": "Übergang auf die CSRD-Berichterstattung planen.",
        "en": "Plan the transition to CSRD reporting.",
        "es": "Planificar la transición a la información según la CSRD.",
        "fr": "Planifier la transition vers le reporting CSRD.",
        "it": "Pianificare la transizione alla rendicontazione CSRD.",
        "zh": "规划向 CSRD 报告体系的过渡。",
    },
    # --- Taxonomie-Verordnung ---
    "taxonomie_1": {
        "de": "Wirtschaftstätigkeiten den delegierten Rechtsakten zuordnen und die taxonomiefähigen "
              "Anteile bestimmen.",
        "en": "Map economic activities to the delegated acts and determine the taxonomy-eligible shares.",
        "es": "Asignar las actividades económicas a los actos delegados y determinar las proporciones "
              "elegibles según la taxonomía.",
        "fr": "Rattacher les activités économiques aux actes délégués et déterminer les parts éligibles "
              "à la taxinomie.",
        "it": "Ricondurre le attività economiche agli atti delegati e determinare le quote ammissibili "
              "alla tassonomia.",
        "zh": "将经济活动对应到授权法案，确定符合分类目录条件的比例。",
    },
    "taxonomie_2": {
        "de": "Für taxonomiefähige Tätigkeiten die technischen Bewertungskriterien, die Vermeidung "
              "erheblicher Beeinträchtigungen und den Mindestschutz prüfen (Art. 3, 18).",
        "en": "For taxonomy-eligible activities, check the technical screening criteria, do-no-"
              "significant-harm and the minimum safeguards (Art. 3, 18).",
        "es": "Para las actividades elegibles, comprobar los criterios técnicos de selección, el "
              "principio de no causar perjuicio significativo y las garantías mínimas (art. 3, 18).",
        "fr": "Pour les activités éligibles, vérifier les critères d'examen technique, l'absence de "
              "préjudice important et les garanties minimales (art. 3, 18).",
        "it": "Per le attività ammissibili, verificare i criteri di vaglio tecnico, il principio DNSH e "
              "le garanzie minime (art. 3, 18).",
        "zh": "对符合条件的活动，核查技术筛选标准、无重大损害原则及最低保障要求（第 3、18 条）。",
    },
    "taxonomie_3": {
        "de": "Umsatz-, CapEx- und OpEx-Anteile nach der Delegierten Verordnung (EU) 2021/2178 "
              "ermitteln und in den vorgeschriebenen Meldebögen ausweisen (Art. 8).",
        "en": "Determine turnover, CapEx and OpEx shares under Delegated Regulation (EU) 2021/2178 and "
              "present them in the prescribed templates (Art. 8).",
        "es": "Determinar las proporciones de cifra de negocios, CapEx y OpEx según el Reglamento "
              "Delegado (UE) 2021/2178 y presentarlas en las plantillas prescritas (art. 8).",
        "fr": "Déterminer les parts de chiffre d'affaires, de CapEx et d'OpEx selon le règlement délégué "
              "(UE) 2021/2178 et les présenter dans les modèles prescrits (art. 8).",
        "it": "Determinare le quote di fatturato, CapEx e OpEx secondo il regolamento delegato (UE) "
              "2021/2178 e riportarle nei modelli prescritti (art. 8).",
        "zh": "依据授权条例 (EU) 2021/2178 计算营业额、资本性支出和运营支出的比例，并在规定表格中披露（第 8 条）。",
    },
    # --- SFDR ---
    # --- ESG-Rating-Verordnung ---
    # --- HinSchG ---
    "hinschg_1": {
        "de": "Interne Meldestelle einrichten und die dafür zuständige Person oder Organisationseinheit "
              "benennen (§§ 12, 15).",
        "en": "Set up an internal reporting office and appoint the responsible person or unit "
              "(sections 12, 15).",
        "es": "Crear un canal interno de denuncia y designar a la persona o unidad responsable "
              "(§§ 12, 15).",
        "fr": "Mettre en place un canal de signalement interne et désigner la personne ou l'unité "
              "responsable (§§ 12, 15).",
        "it": "Istituire un canale di segnalazione interno e designare la persona o l'unità responsabile "
              "(§§ 12, 15).",
        "zh": "设立内部举报机构，并指定负责人员或部门（第 12、15 条）。",
    },
    "hinschg_2": {
        "de": "Meldeweg in mündlicher Form und in Textform bereitstellen; auf Wunsch ist eine "
              "persönliche Zusammenkunft zu ermöglichen (§ 16).",
        "en": "Provide a reporting channel in oral and in written form; on request a personal meeting "
              "must be made possible (section 16).",
        "es": "Ofrecer una vía de denuncia oral y por escrito; a petición debe posibilitarse una reunión "
              "presencial (§ 16).",
        "fr": "Proposer un canal de signalement oral et écrit ; sur demande, une rencontre en personne "
              "doit être possible (§ 16).",
        "it": "Offrire un canale di segnalazione in forma orale e scritta; su richiesta va garantito un "
              "incontro di persona (§ 16).",
        "zh": "提供口头和书面举报途径；应请求须安排当面会谈（第 16 条）。",
    },
    "hinschg_3": {
        "de": "Fristen einhalten: Eingangsbestätigung binnen sieben Tagen, Rückmeldung binnen drei "
              "Monaten (§ 17).",
        "en": "Observe the deadlines: acknowledge receipt within seven days, give feedback within three "
              "months (section 17).",
        "es": "Cumplir los plazos: acuse de recibo en siete días, respuesta en tres meses (§ 17).",
        "fr": "Respecter les délais : accusé de réception sous sept jours, retour sous trois mois "
              "(§ 17).",
        "it": "Rispettare i termini: conferma di ricezione entro sette giorni, riscontro entro tre mesi "
              "(§ 17).",
        "zh": "遵守时限：七日内确认收到，三个月内给予反馈（第 17 条）。",
    },
    "hinschg_4": {
        "de": "Vertraulichkeit der Identität sichern und Meldungen dokumentieren; Verstöße sind "
              "bußgeldbewehrt (§§ 8, 11, 40).",
        "en": "Safeguard the confidentiality of identities and document reports; breaches carry fines "
              "(sections 8, 11, 40).",
        "es": "Garantizar la confidencialidad de la identidad y documentar las denuncias; las "
              "infracciones conllevan multas (§§ 8, 11, 40).",
        "fr": "Garantir la confidentialité de l'identité et documenter les signalements ; les "
              "manquements sont passibles d'amendes (§§ 8, 11, 40).",
        "it": "Garantire la riservatezza dell'identità e documentare le segnalazioni; le violazioni sono "
              "sanzionate (§§ 8, 11, 40).",
        "zh": "确保举报人身份保密并记录举报事项；违反规定将被处以罚款（第 8、11、40 条）。",
    },
    # --- Right to Repair ---
    "r2r_1": {
        "de": "Prüfen, ob eigene Produkte unter die in Anhang II genannten Warenkategorien fallen.",
        "en": "Check whether your products fall under the goods categories listed in Annex II.",
        "es": "Comprobar si los propios productos entran en las categorías de bienes del anexo II.",
        "fr": "Vérifier si vos produits relèvent des catégories de biens énumérées à l'annexe II.",
        "it": "Verificare se i propri prodotti rientrano nelle categorie di beni elencate nell'allegato II.",
        "zh": "核查自有产品是否属于附件二所列商品类别。",
    },
    "r2r_2": {
        "de": "Reparatur innerhalb angemessener Frist und zu angemessenem Preis organisieren und ein "
              "europäisches Reparaturformular bereitstellen (Art. 5, 4).",
        "en": "Organise repair within a reasonable time and at a reasonable price and provide the "
              "European repair information form (Art. 5, 4).",
        "es": "Organizar la reparación en un plazo y a un precio razonables y facilitar el formulario "
              "europeo de información sobre reparación (art. 5, 4).",
        "fr": "Organiser la réparation dans un délai et à un prix raisonnables et fournir le formulaire "
              "européen d'information sur la réparation (art. 5, 4).",
        "it": "Organizzare la riparazione entro un termine e a un prezzo ragionevoli e fornire il modulo "
              "europeo di informazioni sulla riparazione (art. 5, 4).",
        "zh": "在合理期限内以合理价格安排维修，并提供欧洲维修信息表（第 5、4 条）。",
    },
    "r2r_3": {
        "de": "Ersatzteile und Reparaturinformationen zugänglich machen; Klauseln, die unabhängige "
              "Reparatur behindern, sind unzulässig (Art. 5).",
        "en": "Make spare parts and repair information available; clauses that impede independent "
              "repair are not permitted (Art. 5).",
        "es": "Poner a disposición piezas de repuesto e información de reparación; las cláusulas que "
              "impiden la reparación independiente son inadmisibles (art. 5).",
        "fr": "Rendre accessibles les pièces détachées et les informations de réparation ; les clauses "
              "entravant la réparation indépendante sont interdites (art. 5).",
        "it": "Rendere disponibili pezzi di ricambio e informazioni sulla riparazione; le clausole che "
              "ostacolano la riparazione indipendente non sono ammesse (art. 5).",
        "zh": "提供备件和维修信息；妨碍独立维修的条款不予允许（第 5 条）。",
    },
    # --- Oekodesign-Verordnung (ESPR) ---
    "oekodesign_1": {
        "de": "Den Arbeitsplan der Kommission verfolgen: Konkrete Anforderungen entstehen erst durch "
              "delegierte Rechtsakte je Produktgruppe (Art. 4).",
        "en": "Follow the Commission's working plan: concrete requirements only arise from delegated "
              "acts per product group (Art. 4).",
        "es": "Seguir el plan de trabajo de la Comisión: los requisitos concretos solo surgen de actos "
              "delegados por grupo de productos (art. 4).",
        "fr": "Suivre le plan de travail de la Commission : les exigences concrètes ne naissent que des "
              "actes délégués par groupe de produits (art. 4).",
        "it": "Seguire il piano di lavoro della Commissione: i requisiti concreti derivano solo da atti "
              "delegati per gruppo di prodotti (art. 4).",
        "zh": "关注欧盟委员会的工作计划：具体要求须由针对各产品组的授权法案确定（第 4 条）。",
    },
    "oekodesign_2": {
        "de": "Auf den digitalen Produktpass vorbereiten: Produkt- und Materialdaten je Modell, Charge "
              "oder Artikel strukturiert vorhalten (Art. 9 ff.).",
        "en": "Prepare for the digital product passport: keep product and material data structured per "
              "model, batch or item (Art. 9 et seq.).",
        "es": "Prepararse para el pasaporte digital de producto: mantener datos de producto y material "
              "estructurados por modelo, lote o artículo (art. 9 y ss.).",
        "fr": "Se préparer au passeport numérique de produit : tenir des données produit et matériaux "
              "structurées par modèle, lot ou article (art. 9 et suiv.).",
        "it": "Prepararsi al passaporto digitale di prodotto: mantenere dati di prodotto e materiali "
              "strutturati per modello, lotto o articolo (art. 9 ss.).",
        "zh": "为数字产品护照做准备：按型号、批次或单品结构化保存产品与材料数据（第 9 条及以下）。",
    },
    "oekodesign_3": {
        "de": "Umgang mit unverkauften Verbrauchsgütern klären: Offenlegungspflicht über vernichtete "
              "Waren, für Textilien und Schuhe gilt ein Vernichtungsverbot (Art. 24, 25).",
        "en": "Clarify the handling of unsold consumer products: destroyed goods must be disclosed, and "
              "for textiles and footwear destruction is prohibited (Art. 24, 25).",
        "es": "Aclarar el tratamiento de productos de consumo no vendidos: obligación de informar sobre "
              "bienes destruidos; para textiles y calzado rige la prohibición de destrucción (art. 24, 25).",
        "fr": "Clarifier le traitement des produits de consommation invendus : obligation de publier les "
              "biens détruits ; pour les textiles et chaussures, la destruction est interdite (art. 24, 25).",
        "it": "Chiarire la gestione dei beni di consumo invenduti: obbligo di informativa sui beni "
              "distrutti; per tessili e calzature vige il divieto di distruzione (art. 24, 25).",
        "zh": "明确未售出消费品的处置方式：须披露被销毁商品，纺织品和鞋类适用销毁禁令（第 24、25 条）。",
    },
    # --- Vernichtungsverbot unverkaufter Konsumgueter (Del. VO (EU) 2026/296) ---
    "vernichtung_1": {
        "de": "Prüfen, ob unverkaufte Kleidung, Bekleidungszubehör oder Schuhe vernichtet oder "
              "entsorgt werden — nur diese Warengruppen listet Anhang VII der Verordnung (EU) 2024/1781.",
        "en": "Check whether unsold clothing, clothing accessories or footwear are destroyed or "
              "discarded — Annex VII to Regulation (EU) 2024/1781 lists only these product groups.",
        "es": "Comprobar si se destruye o desecha ropa, complementos de vestir o calzado sin vender: "
              "el anexo VII del Reglamento (UE) 2024/1781 solo enumera estos grupos de productos.",
        "fr": "Vérifier si des vêtements, accessoires vestimentaires ou chaussures invendus sont "
              "détruits ou éliminés — l'annexe VII du règlement (UE) 2024/1781 ne vise que ces groupes.",
        "it": "Verificare se abbigliamento, accessori di abbigliamento o calzature invenduti vengono "
              "distrutti o smaltiti: l'allegato VII del regolamento (UE) 2024/1781 elenca solo questi gruppi.",
        "zh": "核查是否销毁或处置未售出的服装、服饰配件或鞋类——条例 (EU) 2024/1781 附件七仅列明这些产品组。",
    },
    "vernichtung_2": {
        "de": "Vor jeder Vernichtung die Ausnahmen des Art. 2 der Delegierten Verordnung (EU) 2026/296 "
              "durchgehen; das Spendenangebot nach Buchstabe h greift erst, wenn keine der übrigen "
              "Ausnahmen zutrifft.",
        "en": "Before any destruction, work through the derogations in Art. 2 of Delegated Regulation "
              "(EU) 2026/296; the donation route in point (h) only applies if none of the others does.",
        "es": "Antes de cualquier destrucción, repasar las excepciones del art. 2 del Reglamento "
              "Delegado (UE) 2026/296; la vía de donación de la letra h) solo cabe si no aplica ninguna otra.",
        "fr": "Avant toute destruction, passer en revue les dérogations de l'art. 2 du règlement "
              "délégué (UE) 2026/296 ; l'offre de don du point h) ne joue que si aucune autre ne s'applique.",
        "it": "Prima di ogni distruzione, esaminare le deroghe dell'art. 2 del regolamento delegato "
              "(UE) 2026/296; l'offerta di donazione di cui alla lettera h) vale solo se nessun'altra si applica.",
        "zh": "销毁前逐条核对授权条例 (EU) 2026/296 第 2 条的例外情形；第 h 项的捐赠途径仅在其他例外均不适用时才可援引。",
    },
    "vernichtung_3": {
        "de": "Für den Spendenweg ein Angebot über mindestens acht Wochen dokumentieren — an mindestens "
              "drei geeignete sozialwirtschaftliche Einrichtungen in der Union oder über eine leicht "
              "zugängliche Seite der eigenen Website (Art. 2 Buchst. h).",
        "en": "For the donation route, document an offer running at least eight weeks — to at least "
              "three suitable social economy entities in the Union or via an easily accessible page on "
              "your own website (Art. 2(h)).",
        "es": "Para la vía de donación, documentar una oferta de al menos ocho semanas: a un mínimo de "
              "tres entidades de la economía social de la Unión o a través de una página fácilmente "
              "accesible del propio sitio web (art. 2, letra h).",
        "fr": "Pour la voie du don, documenter une offre d'au moins huit semaines — à au moins trois "
              "entités de l'économie sociale de l'Union ou via une page aisément accessible de son "
              "propre site web (art. 2, point h).",
        "it": "Per la via della donazione, documentare un'offerta di almeno otto settimane: ad almeno "
              "tre enti dell'economia sociale dell'Unione o tramite una pagina facilmente accessibile "
              "del proprio sito web (art. 2, lett. h).",
        "zh": "走捐赠途径的，须记录至少八周的捐赠要约——面向欧盟境内至少三家合适的社会经济实体，或通过本企业网站上易于访问的页面（第 2 条 h 项）。",
    },
    "vernichtung_4": {
        "de": "Nachweise nach Art. 3 fünf Jahre aufbewahren und binnen 30 Tagen elektronisch vorlegen "
              "können; zusätzlich jährlich Menge, Gewicht und Gründe der entsorgten Ware offenlegen "
              "(Art. 24 der Verordnung (EU) 2024/1781).",
        "en": "Keep the evidence required by Art. 3 for five years and be able to submit it "
              "electronically within 30 days; in addition disclose quantity, weight and reasons for "
              "discarded goods every year (Art. 24 of Regulation (EU) 2024/1781).",
        "es": "Conservar cinco años la documentación del art. 3 y poder presentarla electrónicamente en "
              "30 días; además, divulgar anualmente cantidad, peso y motivos de los productos "
              "desechados (art. 24 del Reglamento (UE) 2024/1781).",
        "fr": "Conserver cinq ans les justificatifs de l'art. 3 et pouvoir les transmettre par voie "
              "électronique sous 30 jours ; publier en outre chaque année la quantité, le poids et les "
              "motifs des produits éliminés (art. 24 du règlement (UE) 2024/1781).",
        "it": "Conservare per cinque anni la documentazione dell'art. 3 e poterla trasmettere in forma "
              "elettronica entro 30 giorni; inoltre pubblicare ogni anno quantità, peso e motivi dei "
              "prodotti smaltiti (art. 24 del regolamento (UE) 2024/1781).",
        "zh": "按第 3 条留存证明材料五年，并能在 30 天内以电子形式提交；此外须每年披露被处置商品的数量、重量及原因（条例 (EU) 2024/1781 第 24 条）。",
    },
    # --- PPWR ---
    "ppwr_1": {
        "de": "Verpackungsportfolio erfassen und gegen die Anforderungen an Recyclingfähigkeit und "
              "Verpackungsminimierung prüfen (Art. 6, 10).",
        "en": "Take stock of the packaging portfolio and check it against the recyclability and "
              "packaging minimisation requirements (Art. 6, 10).",
        "es": "Inventariar la cartera de envases y contrastarla con los requisitos de reciclabilidad y "
              "minimización (art. 6, 10).",
        "fr": "Recenser le portefeuille d'emballages et le confronter aux exigences de recyclabilité et "
              "de minimisation (art. 6, 10).",
        "it": "Censire il portafoglio imballaggi e verificarlo rispetto ai requisiti di riciclabilità e "
              "minimizzazione (art. 6, 10).",
        "zh": "梳理包装组合，并对照可回收性和包装最小化要求进行核查（第 6、10 条）。",
    },
    "ppwr_2": {
        "de": "Konformitätsbewertung, EU-Konformitätserklärung und Kennzeichnung der Verpackungen "
              "vorbereiten (Art. 11, 12, 38).",
        "en": "Prepare conformity assessment, the EU declaration of conformity and packaging labelling "
              "(Art. 11, 12, 38).",
        "es": "Preparar la evaluación de conformidad, la declaración UE de conformidad y el etiquetado "
              "de los envases (art. 11, 12, 38).",
        "fr": "Préparer l'évaluation de conformité, la déclaration UE de conformité et l'étiquetage des "
              "emballages (art. 11, 12, 38).",
        "it": "Predisporre la valutazione di conformità, la dichiarazione UE di conformità e "
              "l'etichettatura degli imballaggi (art. 11, 12, 38).",
        "zh": "准备符合性评估、欧盟符合性声明及包装标识（第 11、12、38 条）。",
    },
    "ppwr_3": {
        "de": "Registrierung und erweiterte Herstellerverantwortung je Mitgliedstaat klären, in dem "
              "Verpackungen erstmals bereitgestellt werden (Art. 44 f.).",
        "en": "Clarify registration and extended producer responsibility in each member state where "
              "packaging is first made available (Art. 44 et seq.).",
        "es": "Aclarar el registro y la responsabilidad ampliada del productor en cada Estado miembro "
              "donde se ponga por primera vez a disposición el envase (art. 44 y ss.).",
        "fr": "Clarifier l'enregistrement et la responsabilité élargie du producteur dans chaque État "
              "membre où l'emballage est mis à disposition pour la première fois (art. 44 et suiv.).",
        "it": "Chiarire registrazione e responsabilità estesa del produttore in ogni Stato membro in cui "
              "l'imballaggio è messo a disposizione per la prima volta (art. 44 ss.).",
        "zh": "在首次提供包装的每个成员国明确注册登记与生产者延伸责任（第 44 条及以下）。",
    },
    # --- MinRohSorgG ---
    "minroh_1": {
        "de": "Prüfen, ob das Unternehmen Unionseinführer mit Sitz in Deutschland ist und die "
              "Mengenschwellen der Verordnung (EU) 2017/821 überschreitet (§ 1).",
        "en": "Check whether the company is a Union importer established in Germany and exceeds the "
              "volume thresholds of Regulation (EU) 2017/821 (section 1).",
        "es": "Comprobar si la empresa es importador de la Unión con sede en Alemania y supera los "
              "umbrales de volumen del Reglamento (UE) 2017/821 (§ 1).",
        "fr": "Vérifier si l'entreprise est un importateur de l'Union établi en Allemagne et dépasse les "
              "seuils de volume du règlement (UE) 2017/821 (§ 1).",
        "it": "Verificare se l'impresa è un importatore dell'Unione con sede in Germania e supera le "
              "soglie di volume del regolamento (UE) 2017/821 (§ 1).",
        "zh": "核查企业是否为设在德国的欧盟进口商，且超过条例 (EU) 2017/821 的数量门槛（第 1 条）。",
    },
    "minroh_2": {
        "de": "Nachweise über die Erfüllung der Sorgfaltspflichten für die Kontrolle durch die BAFA "
              "bereithalten (§§ 4, 5).",
        "en": "Keep evidence of compliance with the due diligence obligations ready for BAFA's "
              "inspection (sections 4, 5).",
        "es": "Mantener disponibles las pruebas del cumplimiento de las obligaciones de diligencia "
              "debida para el control de la BAFA (§§ 4, 5).",
        "fr": "Tenir à disposition les preuves du respect des obligations de diligence pour le contrôle "
              "de la BAFA (§§ 4, 5).",
        "it": "Tenere a disposizione le prove dell'adempimento degli obblighi di diligenza per il "
              "controllo della BAFA (§§ 4, 5).",
        "zh": "备妥履行尽职调查义务的证明材料，以供联邦经济和出口管制局检查（第 4、5 条）。",
    },
    "minroh_3": {
        "de": "Fristen und Mitwirkungspflichten gegenüber der BAFA einhalten; Verstöße sind "
              "bußgeldbewehrt (§ 8).",
        "en": "Observe deadlines and duties to cooperate with BAFA; breaches carry fines (section 8).",
        "es": "Cumplir los plazos y deberes de colaboración ante la BAFA; las infracciones conllevan "
              "multas (§ 8).",
        "fr": "Respecter les délais et obligations de coopération envers la BAFA ; les manquements sont "
              "passibles d'amendes (§ 8).",
        "it": "Rispettare termini e obblighi di collaborazione verso la BAFA; le violazioni sono "
              "sanzionate (§ 8).",
        "zh": "遵守对联邦经济和出口管制局的时限和配合义务；违反规定将被处以罚款（第 8 条）。",
    },
    # --- EmpCo ---
    "empco_1": {
        "de": "Werbeaussagen inventarisieren: Pauschale Umweltaussagen ohne Nachweis und "
              "Klimaneutralitätsaussagen, die allein auf Kompensation beruhen, sind unzulässig.",
        "en": "Take stock of advertising claims: generic environmental claims without evidence and "
              "carbon-neutrality claims based solely on offsetting are not permitted.",
        "es": "Inventariar las afirmaciones publicitarias: las alegaciones ambientales genéricas sin "
              "pruebas y las de neutralidad climática basadas solo en compensación son inadmisibles.",
        "fr": "Recenser les allégations publicitaires : les allégations environnementales génériques non "
              "étayées et celles de neutralité carbone fondées uniquement sur la compensation sont "
              "interdites.",
        "it": "Censire le affermazioni pubblicitarie: le asserzioni ambientali generiche non provate e "
              "quelle di neutralità climatica basate solo su compensazione non sono ammesse.",
        "zh": "梳理广告宣称：无证据的笼统环保宣称，以及仅依靠碳抵消的气候中和宣称，均不被允许。",
    },
    "empco_2": {
        "de": "Nachhaltigkeitssiegel nur noch verwenden, wenn sie auf einem zertifizierten System "
              "beruhen oder von staatlichen Stellen stammen.",
        "en": "Use sustainability labels only if they are based on a certification scheme or come from "
              "public authorities.",
        "es": "Utilizar sellos de sostenibilidad solo si se basan en un sistema de certificación o "
              "proceden de autoridades públicas.",
        "fr": "N'utiliser des labels de durabilité que s'ils reposent sur un système de certification ou "
              "émanent d'autorités publiques.",
        "it": "Utilizzare marchi di sostenibilità solo se basati su un sistema di certificazione o "
              "provenienti da autorità pubbliche.",
        "zh": "仅在可持续性标签基于认证体系或由公共机构颁发时方可使用。",
    },
    "empco_3": {
        "de": "Angaben zu Haltbarkeit, Reparierbarkeit und Software-Updates prüfen; das Verschweigen "
              "bekannter Einschränkungen ist irreführend.",
        "en": "Review statements on durability, reparability and software updates; withholding known "
              "limitations is misleading.",
        "es": "Revisar las indicaciones sobre durabilidad, reparabilidad y actualizaciones de software; "
              "ocultar limitaciones conocidas es engañoso.",
        "fr": "Vérifier les indications sur la durabilité, la réparabilité et les mises à jour "
              "logicielles ; taire des limitations connues est trompeur.",
        "it": "Verificare le indicazioni su durabilità, riparabilità e aggiornamenti software; tacere "
              "limitazioni note è ingannevole.",
        "zh": "核查关于耐用性、可维修性和软件更新的说明；隐瞒已知限制构成误导。",
    },
    "empco_4": {
        "de": "Für jede Umweltaussage einen Beleg dokumentieren und die Belege aktuell halten.",
        "en": "Document evidence for every environmental claim and keep it up to date.",
        "es": "Documentar pruebas para cada alegación ambiental y mantenerlas actualizadas.",
        "fr": "Documenter une preuve pour chaque allégation environnementale et la tenir à jour.",
        "it": "Documentare una prova per ogni asserzione ambientale e mantenerla aggiornata.",
        "zh": "为每一项环保宣称留存证据，并保持证据持续更新。",
    },
    # --- Katalogerweiterung 29.09.2026 ---
    "reach17_1": {
        "de": "Sortiment gegen die Einträge 43, 46a, 68, 72, 76 und 79 abgleichen und je Artikel die relevanten Stoffe und Grenzwerte festhalten.",
        "en": "Check the product range against entries 43, 46a, 68, 72, 76 and 79 and record the relevant substances and limit values for each article.",
        "es": "Cotejar el surtido con las entradas 43, 46 bis, 68, 72, 76 y 79 y registrar para cada artículo las sustancias y los valores límite pertinentes.",
        "fr": "Comparer l'assortiment aux entrées 43, 46 bis, 68, 72, 76 et 79 et consigner pour chaque article les substances et valeurs limites pertinentes.",
        "it": "Confrontare l'assortimento con le voci 43, 46 bis, 68, 72, 76 e 79 e registrare per ogni articolo le sostanze e i valori limite pertinenti.",
        "zh": "将产品系列与第 43、46a、68、72、76 和 79 项条目进行比对，并逐一记录每件物品涉及的物质及限值。",
    },
    "reach17_2": {
        "de": "Von Lieferanten Prüfberichte akkreditierter Labore oder Konformitätserklärungen zu Azofarbstoffen, NPE, PFCA, PFHxA und den Stoffen der Anlage 12 verlangen.",
        "en": "Request test reports from accredited laboratories or declarations of conformity from suppliers on azo dyes, NPE, PFCA, PFHxA and the substances in Appendix 12.",
        "es": "Solicitar a los proveedores informes de ensayo de laboratorios acreditados o declaraciones de conformidad sobre colorantes azoicos, NPE, PFCA, PFHxA y las sustancias del apéndice 12.",
        "fr": "Exiger des fournisseurs des rapports d'essai de laboratoires accrédités ou des déclarations de conformité concernant les colorants azoïques, les NPE, les PFCA, le PFHxA et les substances de l'appendice 12.",
        "it": "Richiedere ai fornitori rapporti di prova di laboratori accreditati o dichiarazioni di conformità su coloranti azoici, NPE, PFCA, PFHxA e le sostanze dell'appendice 12.",
        "zh": "要求供应商提供经认可实验室出具的检测报告或符合性声明，涵盖偶氮染料、NPE、PFCA、PFHxA 以及附录 12 所列物质。",
    },
    "reach17_3": {
        "de": "PFHxA-freie Ausrüstungen für Ware vorbereiten, die ab 10.10.2026 (Bekleidung, Schuhe) bzw. 10.10.2027 (übrige Textilien) in Verkehr gebracht wird.",
        "en": "Prepare PFHxA-free finishes for goods placed on the market from 10.10.2026 (clothing, footwear) or 10.10.2027 (other textiles).",
        "es": "Preparar acabados sin PFHxA para la mercancía que se introduzca en el mercado a partir del 10.10.2026 (ropa, calzado) o del 10.10.2027 (demás textiles).",
        "fr": "Préparer des apprêts sans PFHxA pour les marchandises mises sur le marché à compter du 10.10.2026 (habillement, chaussures) ou du 10.10.2027 (autres textiles).",
        "it": "Predisporre finissaggi privi di PFHxA per la merce immessa sul mercato dal 10.10.2026 (abbigliamento, calzature) o dal 10.10.2027 (altri tessili).",
        "zh": "为自 2026 年 10 月 10 日（服装、鞋类）或 2027 年 10 月 10 日（其他纺织品）起投放市场的货品准备不含 PFHxA 的整理工艺。",
    },
    "reach17_4": {
        "de": "Bei eigener Nassveredlung oder Faserherstellung DMF-, DMAC- und NEP-Einsatz mit DNEL-Werten im Sicherheitsdatenblatt und Expositionsschutz dokumentieren.",
        "en": "Where wet finishing or fibre production is carried out in-house, document the use of DMF, DMAC and NEP together with the DNEL values in the safety data sheet and exposure protection.",
        "es": "En caso de acabado en húmedo o fabricación de fibras propios, documentar el uso de DMF, DMAC y NEP con los valores DNEL de la ficha de datos de seguridad y la protección frente a la exposición.",
        "fr": "En cas d'ennoblissement par voie humide ou de production de fibres en interne, documenter l'utilisation de DMF, DMAC et NEP avec les valeurs DNEL figurant dans la fiche de données de sécurité et la protection contre l'exposition.",
        "it": "In caso di finissaggio a umido o produzione di fibre in proprio, documentare l'impiego di DMF, DMAC e NEP con i valori DNEL della scheda di dati di sicurezza e la protezione dall'esposizione.",
        "zh": "如自行开展湿法整理或纤维生产，应记录 DMF、DMAC 和 NEP 的使用情况，连同安全数据表中的 DNEL 值及暴露防护措施。",
    },
    "reach33_1": {
        "de": "Stofflisten der Lieferanten gegen die aktuelle Kandidatenliste prüfen und das bei jeder Listenaktualisierung (in der Regel halbjährlich) wiederholen.",
        "en": "Check suppliers' substance lists against the current Candidate List and repeat this at every update of the list (usually every six months).",
        "es": "Comprobar las listas de sustancias de los proveedores frente a la Lista de candidatas vigente y repetirlo en cada actualización de la lista (por lo general, semestral).",
        "fr": "Vérifier les listes de substances des fournisseurs au regard de la liste des substances candidates en vigueur et répéter l'opération à chaque mise à jour de la liste (en règle générale semestrielle).",
        "it": "Verificare gli elenchi di sostanze dei fornitori rispetto all'elenco di sostanze candidate aggiornato e ripetere la verifica a ogni aggiornamento dell'elenco (di norma semestrale).",
        "zh": "对照现行候选清单核查供应商的物质清单，并在每次清单更新时（通常每半年一次）重复核查。",
    },
    "reach33_2": {
        "de": "Für jedes Erzeugnis mit einem Kandidatenstoff über 0,1 % die Information an gewerbliche Kunden vorbereiten, mindestens mit Stoffnamen.",
        "en": "For every article containing a Candidate List substance above 0.1%, prepare the information for business customers, including at least the name of the substance.",
        "es": "Para cada artículo con una sustancia de la Lista de candidatas por encima del 0,1 %, preparar la información destinada a los clientes profesionales, indicando como mínimo el nombre de la sustancia.",
        "fr": "Pour chaque article contenant une substance de la liste des substances candidates à plus de 0,1 %, préparer l'information destinée aux clients professionnels, comportant au minimum le nom de la substance.",
        "it": "Per ogni articolo con una sostanza dell'elenco di sostanze candidate superiore allo 0,1%, predisporre le informazioni per i clienti professionali, indicando almeno il nome della sostanza.",
        "zh": "对每件所含候选清单物质超过 0.1% 的物品，为企业客户准备相关信息，至少注明物质名称。",
    },
    "reach33_3": {
        "de": "Einen Ablauf festlegen, der Verbraucheranfragen binnen 45 Tagen kostenlos beantwortet.",
        "en": "Set up a procedure that answers consumer requests free of charge within 45 days.",
        "es": "Establecer un procedimiento que responda gratuitamente a las solicitudes de los consumidores en un plazo de 45 días.",
        "fr": "Définir une procédure permettant de répondre gratuitement aux demandes des consommateurs dans un délai de 45 jours.",
        "it": "Definire una procedura che risponda gratuitamente alle richieste dei consumatori entro 45 giorni.",
        "zh": "建立在 45 天内免费答复消费者询问的流程。",
    },
    "reach33_4": {
        "de": "Bei Mengen über 1 Tonne pro Jahr und Stoff die Notifizierungspflicht nach Art. 7 Abs. 2 gegenüber der ECHA prüfen.",
        "en": "For quantities above 1 tonne per year and substance, check the obligation to notify ECHA under Art. 7(2).",
        "es": "Para cantidades superiores a 1 tonelada anual por sustancia, comprobar la obligación de notificación a la ECHA prevista en el art. 7, apdo. 2.",
        "fr": "Pour des quantités supérieures à 1 tonne par an et par substance, vérifier l'obligation de notification à l'ECHA prévue à l'art. 7, par. 2.",
        "it": "Per quantitativi superiori a 1 tonnellata all'anno per sostanza, verificare l'obbligo di notifica all'ECHA di cui all'art. 7, par. 2.",
        "zh": "每种物质年用量超过 1 吨的，核查根据第 7 条第 2 款向 ECHA 通报的义务。",
    },
    "scip_1": {
        "de": "Erzeugnisse mit Kandidatenlistenstoffen über 0,1 % ermitteln, die an gewerbliche Kunden oder Händler geliefert oder importiert werden.",
        "en": "Identify articles containing Candidate List substances above 0.1% that are supplied to business customers or retailers, or imported.",
        "es": "Identificar los artículos con sustancias de la Lista de candidatas por encima del 0,1 % que se suministran a clientes profesionales o comerciantes, o que se importan.",
        "fr": "Recenser les articles contenant des substances de la liste des substances candidates à plus de 0,1 % qui sont livrés à des clients professionnels ou à des distributeurs, ou importés.",
        "it": "Individuare gli articoli con sostanze dell'elenco di sostanze candidate superiori allo 0,1% forniti a clienti professionali o rivenditori oppure importati.",
        "zh": "确定所含候选清单物质超过 0.1%、向企业客户或经销商供货或进口的物品。",
    },
    "scip_2": {
        "de": "Im ECHA-Portal einen Zugang (ECHA Account) anlegen und je Erzeugnis ein SCIP-Dossier mit den Angaben nach § 16f Abs. 1 ChemG einreichen.",
        "en": "Create an account (ECHA Account) on the ECHA portal and submit a SCIP dossier for each article with the information required under Section 16f(1) of the German Chemicals Act (ChemG).",
        "es": "Crear una cuenta (ECHA Account) en el portal de la ECHA y presentar por cada artículo un expediente SCIP con los datos exigidos por el § 16f, apdo. 1, de la Ley alemana de sustancias químicas (ChemG).",
        "fr": "Créer un compte (ECHA Account) sur le portail de l'ECHA et soumettre pour chaque article un dossier SCIP comportant les informations visées au § 16f, al. 1, de la loi allemande sur les produits chimiques (ChemG).",
        "it": "Creare un account (ECHA Account) sul portale dell'ECHA e presentare per ogni articolo un fascicolo SCIP con le informazioni di cui al § 16f, c. 1, della legge tedesca sulle sostanze chimiche (ChemG).",
        "zh": "在 ECHA 门户网站上创建账户（ECHA Account），并针对每件物品提交 SCIP 档案，载明德国《化学品法》（ChemG）第 16f 条第 1 款规定的信息。",
    },
    "scip_3": {
        "de": "Bei Handelsware, die unverändert weitergegeben wird, die SCIP-Nummer des Vorlieferanten erfragen und referenzieren.",
        "en": "For merchandise passed on unchanged, ask the upstream supplier for its SCIP number and reference it.",
        "es": "En la mercancía que se revende sin modificaciones, solicitar el número SCIP al proveedor anterior y referenciarlo.",
        "fr": "Pour les marchandises transmises sans modification, demander le numéro SCIP au fournisseur en amont et y faire référence.",
        "it": "Per la merce ceduta senza modifiche, chiedere il numero SCIP al fornitore a monte e farvi riferimento.",
        "zh": "对于原样转售的商品，向上游供应商索取 SCIP 编号并加以引用。",
    },
    "scip_4": {
        "de": "Meldungen bei jeder Aktualisierung der Kandidatenliste und bei Sortimentsänderungen nachführen.",
        "en": "Update notifications at every update of the Candidate List and whenever the product range changes.",
        "es": "Actualizar las notificaciones con cada actualización de la Lista de candidatas y con cada cambio en el surtido.",
        "fr": "Mettre à jour les notifications à chaque actualisation de la liste des substances candidates et à chaque modification de l'assortiment.",
        "it": "Aggiornare le notifiche a ogni aggiornamento dell'elenco di sostanze candidate e a ogni modifica dell'assortimento.",
        "zh": "每次候选清单更新以及产品系列变动时，相应更新通报。",
    },
    "pop_1": {
        "de": "Fluorcarbon-Ausrüstungen, Flammschutzmittel und UV-Stabilisatoren im Sortiment erfassen und bei Lieferanten die eingesetzten Substanzen erfragen.",
        "en": "Record fluorocarbon finishes, flame retardants and UV stabilisers in the product range and ask suppliers which substances are used.",
        "es": "Registrar los acabados con fluorocarbonos, los retardantes de llama y los estabilizadores UV del surtido y preguntar a los proveedores qué sustancias se emplean.",
        "fr": "Recenser dans l'assortiment les apprêts fluorocarbonés, les retardateurs de flamme et les stabilisants UV, et demander aux fournisseurs les substances utilisées.",
        "it": "Censire nell'assortimento i finissaggi fluorocarburici, i ritardanti di fiamma e gli stabilizzanti UV e chiedere ai fornitori le sostanze impiegate.",
        "zh": "梳理产品系列中的含氟碳整理、阻燃剂和紫外线稳定剂，并向供应商询问所用物质。",
    },
    "pop_2": {
        "de": "Prüfberichte zu PFOA, PFOS, PFHxS und deren verwandten Verbindungen für wasser- und schmutzabweisend ausgerüstete Artikel anfordern.",
        "en": "Request test reports on PFOA, PFOS, PFHxS and their related compounds for articles with a water- and dirt-repellent finish.",
        "es": "Solicitar informes de ensayo sobre PFOA, PFOS, PFHxS y sus compuestos afines para los artículos con acabado hidrófugo y antimanchas.",
        "fr": "Demander des rapports d'essai sur le PFOA, le PFOS, le PFHxS et leurs composés apparentés pour les articles à apprêt hydrofuge et antisalissure.",
        "it": "Richiedere rapporti di prova su PFOA, PFOS, PFHxS e i relativi composti affini per gli articoli con finissaggio idrorepellente e antimacchia.",
        "zh": "针对经防水防污整理的物品，索取有关 PFOA、PFOS、PFHxS 及其相关化合物的检测报告。",
    },
    "pop_3": {
        "de": "Kunststoff- und Beschichtungskomponenten auf UV-328 und Dechloran Plus prüfen und die sinkenden Grenzwerte ab 2027 bzw. 2028 einplanen.",
        "en": "Test plastic and coating components for UV-328 and Dechlorane Plus and plan for the decreasing limit values from 2027 and 2028 respectively.",
        "es": "Analizar los componentes de plástico y de recubrimiento en busca de UV-328 y Dechlorane Plus y prever la reducción de los valores límite a partir de 2027 y 2028, respectivamente.",
        "fr": "Contrôler les composants en plastique et les revêtements quant à la présence d'UV-328 et de Dechlorane Plus et anticiper la baisse des valeurs limites à partir de 2027 ou 2028.",
        "it": "Verificare i componenti in plastica e i rivestimenti per UV-328 e Dechlorane Plus e pianificare i valori limite decrescenti dal 2027 e dal 2028.",
        "zh": "检查塑料和涂层部件中的 UV-328 和得克隆（Dechlorane Plus），并对自 2027 年或 2028 年起逐步收紧的限值预作安排。",
    },
    "bpr_1": {
        "de": "Artikel mit antimikrobieller, geruchshemmender, milbenabweisender oder insektizider Ausrüstung erfassen und die eingesetzten Wirkstoffe beim Lieferanten erfragen.",
        "en": "Record articles with an antimicrobial, odour-inhibiting, anti-mite or insecticidal finish and ask the supplier which active substances are used.",
        "es": "Registrar los artículos con acabado antimicrobiano, antiolor, antiácaros o insecticida y preguntar al proveedor qué sustancias activas se emplean.",
        "fr": "Recenser les articles dotés d'un apprêt antimicrobien, anti-odeurs, anti-acariens ou insecticide et demander au fournisseur les substances actives utilisées.",
        "it": "Censire gli articoli con finissaggio antimicrobico, antiodore, antiacaro o insetticida e chiedere al fornitore i principi attivi impiegati.",
        "zh": "梳理具有抗菌、防臭、防螨或杀虫整理的物品，并向供应商询问所用活性物质。",
    },
    "bpr_2": {
        "de": "Prüfen, ob jeder Wirkstoff für die betreffende Produktart genehmigt oder im Prüfprogramm gelistet ist.",
        "en": "Check whether each active substance is approved for the relevant product-type or listed in the review programme.",
        "es": "Comprobar si cada sustancia activa está aprobada para el tipo de producto de que se trate o figura en el programa de revisión.",
        "fr": "Vérifier si chaque substance active est approuvée pour le type de produits concerné ou inscrite au programme d'examen.",
        "it": "Verificare se ciascun principio attivo è approvato per il tipo di prodotto pertinente o figura nel programma di riesame.",
        "zh": "核查每种活性物质是否已就相关产品类型获得批准或列入审查计划。",
    },
    "bpr_3": {
        "de": "Etiketten nach Art. 58 Abs. 3 anpassen, sobald biozide Eigenschaften beworben werden, und Werbeaussagen mit Belegen hinterlegen.",
        "en": "Adapt labels in line with Art. 58(3) as soon as biocidal properties are advertised, and back up advertising claims with evidence.",
        "es": "Adaptar las etiquetas conforme al art. 58, apdo. 3, en cuanto se publiciten propiedades biocidas, y respaldar las alegaciones publicitarias con pruebas.",
        "fr": "Adapter les étiquettes conformément à l'art. 58, par. 3, dès que des propriétés biocides sont mises en avant, et étayer les allégations publicitaires par des justificatifs.",
        "it": "Adeguare le etichette ai sensi dell'art. 58, par. 3, non appena si pubblicizzano proprietà biocide, e corredare di prove le dichiarazioni pubblicitarie.",
        "zh": "一旦宣传杀生物特性，即按第 58 条第 3 款调整标签，并为宣传声明备妥证明材料。",
    },
    "tkvo_1": {
        "de": "Etiketten und Produktseiten auf ausschließlich zulässige Faserbezeichnungen nach Anhang I und korrekte Prozentangaben prüfen.",
        "en": "Check labels and product pages for the exclusive use of permitted fibre names under Annex I and for correct percentages.",
        "es": "Comprobar que en etiquetas y fichas de producto solo se usan denominaciones de fibras admitidas según el anexo I y porcentajes correctos.",
        "fr": "Vérifier que les étiquettes et fiches produits n'utilisent que des dénominations de fibres autorisées selon l'annexe I et des pourcentages corrects.",
        "it": "Verificare che etichette e pagine prodotto usino esclusivamente denominazioni delle fibre ammesse ai sensi dell'allegato I e percentuali corrette.",
        "zh": "核查标签和产品页面是否仅使用附件 I 允许的纤维名称并标注正确的百分比。",
    },
    "tkvo_2": {
        "de": "Für jeden Absatzmarkt die Etikettierung in der jeweiligen Amtssprache sicherstellen.",
        "en": "Ensure labelling in the official language of each sales market.",
        "es": "Garantizar el etiquetado en la lengua oficial de cada mercado de venta.",
        "fr": "Garantir l'étiquetage dans la langue officielle de chaque marché de vente.",
        "it": "Garantire l'etichettatura nella lingua ufficiale di ciascun mercato di vendita.",
        "zh": "确保在每个销售市场使用当地官方语言进行标签标注。",
    },
    "tkvo_3": {
        "de": "Bei Eigenmarken klären, dass das Unternehmen als Hersteller für Richtigkeit und Anbringung des Etiketts einsteht.",
        "en": "For own brands, clarify that the company, as manufacturer, is responsible for the accuracy and affixing of the label.",
        "es": "En las marcas propias, dejar claro que la empresa responde, como fabricante, de la exactitud y la colocación de la etiqueta.",
        "fr": "Pour les marques propres, préciser que l'entreprise répond, en tant que fabricant, de l'exactitude et de l'apposition de l'étiquette.",
        "it": "Per i marchi propri, chiarire che l'impresa risponde, in qualità di fabbricante, della correttezza e dell'apposizione dell'etichetta.",
        "zh": "对于自有品牌，明确企业作为制造商须对标签的准确性和加贴负责。",
    },
    "tkvo_4": {
        "de": "Im Onlineshop die Faserzusammensetzung vor dem Kaufabschluss gut sichtbar anzeigen.",
        "en": "In the online shop, display the fibre composition clearly before the purchase is concluded.",
        "es": "En la tienda en línea, mostrar la composición en fibras de forma bien visible antes de que se cierre la compra.",
        "fr": "Dans la boutique en ligne, afficher la composition en fibres de manière bien visible avant la conclusion de l'achat.",
        "it": "Nel negozio online, mostrare la composizione fibrosa in modo ben visibile prima della conclusione dell'acquisto.",
        "zh": "在网店中，于完成购买前醒目展示纤维成分。",
    },
    "gpsr_1": {
        "de": "Für jedes Produkt eine interne Risikoanalyse und technische Unterlagen anlegen und zehn Jahre aufbewahren.",
        "en": "Draw up an internal risk analysis and technical documentation for each product and keep them for ten years.",
        "es": "Elaborar para cada producto un análisis de riesgos interno y la documentación técnica y conservarlos durante diez años.",
        "fr": "Établir pour chaque produit une analyse interne des risques et une documentation technique et les conserver pendant dix ans.",
        "it": "Predisporre per ogni prodotto un'analisi dei rischi interna e la documentazione tecnica e conservarle per dieci anni.",
        "zh": "为每件产品编制内部风险分析和技术文件，并保存十年。",
    },
    "gpsr_2": {
        "de": "Produkte und Verpackungen mit Chargen- oder Artikelnummer sowie Name, Postanschrift und E-Mail-Adresse des Herstellers bzw. Einführers versehen.",
        "en": "Provide products and packaging with a batch or article number and the name, postal address and email address of the manufacturer or importer.",
        "es": "Identificar productos y envases con el número de lote o de artículo y con el nombre, la dirección postal y la dirección de correo electrónico del fabricante o del importador.",
        "fr": "Apposer sur les produits et emballages un numéro de lot ou d'article ainsi que le nom, l'adresse postale et l'adresse électronique du fabricant ou de l'importateur.",
        "it": "Apporre su prodotti e imballaggi il numero di lotto o di articolo nonché nome, indirizzo postale e indirizzo e-mail del fabbricante o dell'importatore.",
        "zh": "在产品及包装上标注批次号或货号，以及制造商或进口商的名称、邮政地址和电子邮件地址。",
    },
    "gpsr_3": {
        "de": "Bei Ware von Herstellern außerhalb der EU einen in der EU niedergelassenen verantwortlichen Wirtschaftsakteur benennen.",
        "en": "For goods from manufacturers outside the EU, designate a responsible economic operator established in the EU.",
        "es": "Para mercancías de fabricantes de fuera de la UE, designar un operador económico responsable establecido en la UE.",
        "fr": "Pour les marchandises de fabricants établis hors de l'UE, désigner un opérateur économique responsable établi dans l'UE.",
        "it": "Per la merce di fabbricanti extra UE, designare un operatore economico responsabile stabilito nell'UE.",
        "zh": "对于来自欧盟以外制造商的货品，指定一名在欧盟设立的负责任经济经营者。",
    },
    "gpsr_4": {
        "de": "Online-Angebote um Herstellerangaben, Produktabbildung und Warnhinweise nach Art. 19 ergänzen und ein Registrierungskonto im Safety-Business-Gateway anlegen.",
        "en": "Add manufacturer details, a product image and warnings under Art. 19 to online offers and create a registration account on the Safety Business Gateway.",
        "es": "Completar las ofertas en línea con los datos del fabricante, una imagen del producto y las advertencias previstas en el art. 19, y crear una cuenta de registro en el Safety Business Gateway.",
        "fr": "Compléter les offres en ligne par les coordonnées du fabricant, une image du produit et les avertissements prévus à l'art. 19, et créer un compte d'enregistrement sur le Safety Business Gateway.",
        "it": "Integrare le offerte online con i dati del fabbricante, un'immagine del prodotto e le avvertenze di cui all'art. 19 e creare un account di registrazione nel Safety Business Gateway.",
        "zh": "在线上商品信息中补充第 19 条规定的制造商信息、产品图片和警示信息，并在 Safety Business Gateway 上注册账户。",
    },
    "psa_1": {
        "de": "Klären, welche Produkte als PSA gelten, und jedem Produkt eine Risikokategorie nach Anhang I zuordnen.",
        "en": "Clarify which products qualify as PPE and assign each product to a risk category under Annex I.",
        "es": "Aclarar qué productos se consideran EPI y asignar a cada uno una categoría de riesgo según el anexo I.",
        "fr": "Déterminer quels produits constituent des EPI et attribuer à chacun une catégorie de risque selon l'annexe I.",
        "it": "Chiarire quali prodotti sono DPI e assegnare a ciascuno una categoria di rischio ai sensi dell'allegato I.",
        "zh": "明确哪些产品属于个人防护装备，并按附件 I 为每件产品划定风险类别。",
    },
    "psa_2": {
        "de": "Für Kategorie II und III eine notifizierte Stelle für die EU-Baumusterprüfung beauftragen.",
        "en": "For categories II and III, commission a notified body to carry out the EU type-examination.",
        "es": "Para las categorías II y III, encargar el examen UE de tipo a un organismo notificado.",
        "fr": "Pour les catégories II et III, charger un organisme notifié de l'examen UE de type.",
        "it": "Per le categorie II e III, incaricare un organismo notificato dell'esame UE del tipo.",
        "zh": "对于 II 类和 III 类产品，委托公告机构进行欧盟型式检验。",
    },
    "psa_3": {
        "de": "Technische Unterlagen, EU-Konformitätserklärung, CE-Kennzeichnung und Gebrauchsanleitung vor dem Inverkehrbringen vollständig bereitstellen.",
        "en": "Provide complete technical documentation, the EU declaration of conformity, CE marking and instructions for use before placing on the market.",
        "es": "Poner a disposición de forma completa la documentación técnica, la declaración UE de conformidad, el marcado CE y las instrucciones de uso antes de la introducción en el mercado.",
        "fr": "Mettre à disposition, de manière complète, la documentation technique, la déclaration UE de conformité, le marquage CE et la notice d'instructions avant la mise sur le marché.",
        "it": "Mettere a disposizione in modo completo la documentazione tecnica, la dichiarazione di conformità UE, la marcatura CE e le istruzioni per l'uso prima dell'immissione sul mercato.",
        "zh": "在投放市场前，完整备齐技术文件、欧盟符合性声明、CE 标志和使用说明。",
    },
    "psa_4": {
        "de": "Als Importeur oder Händler Konformitätserklärung und CE-Kennzeichnung jeder Lieferung stichprobenartig prüfen.",
        "en": "As importer or distributor, spot-check the declaration of conformity and CE marking of every delivery.",
        "es": "Como importador o distribuidor, comprobar por muestreo la declaración de conformidad y el marcado CE de cada entrega.",
        "fr": "En tant qu'importateur ou distributeur, contrôler par sondage la déclaration de conformité et le marquage CE de chaque livraison.",
        "it": "In qualità di importatore o distributore, verificare a campione la dichiarazione di conformità e la marcatura CE di ogni fornitura.",
        "zh": "作为进口商或经销商，对每批货物的符合性声明和 CE 标志进行抽查。",
    },
    "mdr_1": {
        "de": "Prüfen, ob Produkte mit medizinischer Zweckbestimmung beworben oder gekennzeichnet werden, und deren Risikoklasse bestimmen.",
        "en": "Check whether products are advertised or labelled with a medical intended purpose and determine their risk class.",
        "es": "Comprobar si se publicitan o etiquetan productos con una finalidad prevista médica y determinar su clase de riesgo.",
        "fr": "Vérifier si des produits sont promus ou étiquetés avec une destination médicale et déterminer leur classe de risque.",
        "it": "Verificare se vi sono prodotti pubblicizzati o etichettati con una destinazione d'uso medica e determinarne la classe di rischio.",
        "zh": "核查是否有产品以医疗预期用途进行宣传或标注，并确定其风险等级。",
    },
    "mdr_2": {
        "de": "Für Produkte mit Altbescheinigung nach MDD die Fristen 31.12.2027 bzw. 31.12.2028 und den Stand des Zertifizierungsverfahrens bei der Benannten Stelle dokumentieren.",
        "en": "For products with a legacy certificate under the MDD, document the deadlines of 31.12.2027 or 31.12.2028 and the status of the certification procedure with the notified body.",
        "es": "Para los productos con certificado antiguo con arreglo a la MDD, documentar los plazos del 31.12.2027 o del 31.12.2028 y el estado del procedimiento de certificación ante el organismo notificado.",
        "fr": "Pour les produits disposant d'un ancien certificat au titre de la MDD, documenter les échéances du 31.12.2027 ou du 31.12.2028 et l'état d'avancement de la procédure de certification auprès de l'organisme notifié.",
        "it": "Per i prodotti con un certificato precedente ai sensi della MDD, documentare le scadenze del 31.12.2027 o del 31.12.2028 e lo stato della procedura di certificazione presso l'organismo notificato.",
        "zh": "对于持有 MDD 旧证书的产品，记录 2027 年 12 月 31 日或 2028 年 12 月 31 日的期限以及在公告机构的认证程序进展。",
    },
    "mdr_3": {
        "de": "Qualitätsmanagementsystem, technische Dokumentation und verantwortliche Person nach Art. 15 einrichten bzw. nachweisen.",
        "en": "Establish or demonstrate a quality management system, technical documentation and a person responsible for regulatory compliance under Art. 15.",
        "es": "Implantar o acreditar un sistema de gestión de la calidad, la documentación técnica y una persona responsable del cumplimiento de la normativa conforme al art. 15.",
        "fr": "Mettre en place ou justifier un système de management de la qualité, la documentation technique et une personne chargée de veiller au respect de la réglementation conformément à l'art. 15.",
        "it": "Istituire o dimostrare un sistema di gestione della qualità, la documentazione tecnica e una persona responsabile del rispetto della normativa ai sensi dell'art. 15.",
        "zh": "建立或证明具备质量管理体系、技术文件以及第 15 条规定的法规合规负责人。",
    },
    "mdr_4": {
        "de": "Als Importeur oder Händler CE-Kennzeichnung, EU-Konformitätserklärung und Registrierung des Herstellers vor der Bereitstellung prüfen.",
        "en": "As importer or distributor, check the CE marking, the EU declaration of conformity and the manufacturer's registration before making the product available.",
        "es": "Como importador o distribuidor, comprobar el marcado CE, la declaración UE de conformidad y el registro del fabricante antes de la comercialización.",
        "fr": "En tant qu'importateur ou distributeur, vérifier le marquage CE, la déclaration UE de conformité et l'enregistrement du fabricant avant la mise à disposition.",
        "it": "In qualità di importatore o distributore, verificare la marcatura CE, la dichiarazione di conformità UE e la registrazione del fabbricante prima della messa a disposizione.",
        "zh": "作为进口商或经销商，在提供产品前核查 CE 标志、欧盟符合性声明及制造商注册情况。",
    },
    "schuh_1": {
        "de": "Für jedes Schuhmodell den Materialanteil von Obermaterial, Futter und Decksohle sowie Laufsohle nach der 80-Prozent-Regel bestimmen.",
        "en": "For each footwear model, determine the material content of the upper, the lining and sock, and the outer sole according to the 80% rule.",
        "es": "Para cada modelo de calzado, determinar la proporción de material del empeine, del forro y la plantilla y de la suela según la regla del 80 %.",
        "fr": "Pour chaque modèle de chaussure, déterminer la part de matière de la tige, de la doublure et de la semelle de propreté ainsi que de la semelle extérieure selon la règle des 80 %.",
        "it": "Per ogni modello di calzatura, determinare la quota di materiale di tomaia, fodera e sottopiede nonché suola secondo la regola dell'80%.",
        "zh": "按 80% 规则，确定每款鞋的鞋面、衬里和鞋垫以及外底的材料构成。",
    },
    "schuh_2": {
        "de": "Kennzeichnung per Piktogramm oder Schrift an mindestens einem Schuh jedes Paares haltbar anbringen lassen.",
        "en": "Have the labelling durably affixed to at least one shoe of each pair by pictogram or written indication.",
        "es": "Hacer que el etiquetado se coloque de forma duradera, mediante pictograma o texto, en al menos un zapato de cada par.",
        "fr": "Faire apposer l'étiquetage de manière durable, par pictogramme ou indication écrite, sur au moins une chaussure de chaque paire.",
        "it": "Far apporre in modo durevole l'etichettatura, tramite pittogramma o indicazione scritta, su almeno una calzatura di ogni paio.",
        "zh": "安排以图形符号或文字方式，在每双鞋中至少一只上持久地加贴标签。",
    },
    "schuh_3": {
        "de": "Im Wareneingang des Handels stichprobenartig prüfen, ob die Kennzeichnung vorhanden und plausibel ist.",
        "en": "At goods receipt in retail, spot-check whether the labelling is present and plausible.",
        "es": "En la recepción de mercancía del comercio, comprobar por muestreo si el etiquetado existe y es plausible.",
        "fr": "À la réception des marchandises dans le commerce, vérifier par sondage que l'étiquetage est présent et plausible.",
        "it": "Al ricevimento merci nel commercio, verificare a campione che l'etichettatura sia presente e plausibile.",
        "zh": "在零售商收货环节，抽查标签是否存在且内容合理。",
    },
    "eprfr_1": {
        "de": "Ermitteln, welche Bekleidungs-, Schuh- und Heimtextilartikel an Endkunden in Frankreich gehen, und das Unternehmen bei Refashion registrieren.",
        "en": "Determine which clothing, footwear and household linen items go to end customers in France, and register the company with Refashion.",
        "es": "Determinar qué artículos de ropa, calzado y textiles para el hogar se destinan a clientes finales en Francia, y registrar la empresa en Refashion.",
        "fr": "Déterminer quels articles d'habillement, chaussures et linge de maison sont destinés à des clients finaux en France, et enregistrer l'entreprise auprès de Refashion.",
        "it": "Individuare quali articoli di abbigliamento, calzature e tessili per la casa sono destinati a clienti finali in Francia, e registrare l'impresa presso Refashion.",
        "zh": "确定哪些服装、鞋类和家用纺织品面向法国终端客户，并在 Refashion 为企业注册。",
    },
    "eprfr_2": {
        "de": "Ohne Niederlassung in Frankreich schriftlich einen dort niedergelassenen Bevollmächtigten benennen oder die Übernahme durch den Marktplatz schriftlich absichern.",
        "en": "Without an establishment in France, appoint in writing an authorised representative (mandataire) established there, or secure the marketplace's assumption of the obligations in writing.",
        "es": "Sin establecimiento en Francia, designar por escrito un representante autorizado (mandataire) establecido allí o asegurar por escrito que el marketplace asume las obligaciones.",
        "fr": "Sans établissement en France, désigner par écrit un mandataire qui y est établi ou garantir par écrit la prise en charge par la place de marché.",
        "it": "In assenza di una sede in Francia, designare per iscritto un mandatario (mandataire) ivi stabilito o assicurarsi per iscritto che il marketplace se ne faccia carico.",
        "zh": "如在法国没有营业机构，须书面指定一名在当地设立的授权代表（mandataire），或以书面形式确保由线上交易平台承担相关义务。",
    },
    "eprfr_3": {
        "de": "Stückzahlen je Produktkategorie erfassen und die Beitragsmeldung an das éco-organisme einrichten.",
        "en": "Record unit numbers per product category and set up the contribution declaration to the éco-organisme (producer responsibility organisation).",
        "es": "Registrar el número de unidades por categoría de producto y organizar la declaración de contribuciones al éco-organisme (organización de responsabilidad del productor).",
        "fr": "Recenser les quantités unitaires par catégorie de produits et mettre en place la déclaration des contributions à l'éco-organisme.",
        "it": "Rilevare il numero di pezzi per categoria di prodotto e impostare la dichiarazione dei contributi all'éco-organisme (organizzazione per la responsabilità del produttore).",
        "zh": "按产品类别统计件数，并建立向 éco-organisme（生产者责任组织）申报缴费的机制。",
    },
    "eprfr_4": {
        "de": "Sortimentsbreite, Angebotsfrequenz und Reparierbarkeit auswerten, um mögliche Maluszuschläge ab 2026 abzuschätzen.",
        "en": "Evaluate range breadth, offer frequency and reparability to estimate possible malus surcharges from 2026.",
        "es": "Evaluar la amplitud del surtido, la frecuencia de la oferta y la reparabilidad para estimar posibles recargos malus a partir de 2026.",
        "fr": "Évaluer l'étendue de l'assortiment, la fréquence de l'offre et la réparabilité afin d'estimer d'éventuelles pénalités (malus) à partir de 2026.",
        "it": "Valutare ampiezza dell'assortimento, frequenza dell'offerta e riparabilità per stimare eventuali maggiorazioni malus dal 2026.",
        "zh": "评估产品系列广度、上新频率和可修复性，以估算自 2026 年起可能产生的惩罚性附加费（malus）。",
    },
    "eprnl_1": {
        "de": "Prüfen, ob Kleidung oder Haushaltswäsche erstmals in den Niederlanden angeboten wird, auch per Versand aus dem Ausland.",
        "en": "Check whether clothing or household linen is offered for the first time in the Netherlands, including by shipment from abroad.",
        "es": "Comprobar si se ofrece por primera vez ropa o ropa de hogar en los Países Bajos, también mediante envío desde el extranjero.",
        "fr": "Vérifier si des vêtements ou du linge de maison sont proposés pour la première fois aux Pays-Bas, y compris par expédition depuis l'étranger.",
        "it": "Verificare se abbigliamento o biancheria per la casa vengono offerti per la prima volta nei Paesi Bassi, anche tramite spedizione dall'estero.",
        "zh": "核查是否首次在荷兰提供服装或家用布草，包括从国外发货的情况。",
    },
    "eprnl_2": {
        "de": "Bei Rijkswaterstaat melden oder einer Produzentenorganisation (z. B. Stichting UPV Textiel) beitreten.",
        "en": "Register with Rijkswaterstaat (Dutch government agency) or join a producer organisation (e.g. Stichting UPV Textiel).",
        "es": "Registrarse ante Rijkswaterstaat (organismo público neerlandés) o adherirse a una organización de productores (p. ej., Stichting UPV Textiel).",
        "fr": "S'enregistrer auprès de Rijkswaterstaat (agence publique néerlandaise) ou adhérer à une organisation de producteurs (p. ex. Stichting UPV Textiel).",
        "it": "Registrarsi presso Rijkswaterstaat (agenzia pubblica olandese) o aderire a un'organizzazione di produttori (ad es. Stichting UPV Textiel).",
        "zh": "向 Rijkswaterstaat（荷兰公共工程与水利管理局）申报，或加入生产者组织（例如 Stichting UPV Textiel）。",
    },
    "eprnl_3": {
        "de": "Ohne Niederlassung in den Niederlanden einen dort ansässigen Bevollmächtigten benennen.",
        "en": "Without an establishment in the Netherlands, appoint an authorised representative (gemachtigd vertegenwoordiger) based there.",
        "es": "Sin establecimiento en los Países Bajos, designar un representante autorizado (gemachtigd vertegenwoordiger) con sede allí.",
        "fr": "Sans établissement aux Pays-Bas, désigner un mandataire (gemachtigd vertegenwoordiger) qui y est établi.",
        "it": "In assenza di una sede nei Paesi Bassi, designare un mandatario (gemachtigd vertegenwoordiger) ivi stabilito.",
        "zh": "如在荷兰没有营业机构，须指定一名当地的授权代表（gemachtigd vertegenwoordiger）。",
    },
    "eprnl_4": {
        "de": "In Verkehr gebrachte Mengen in Kilogramm je Kalenderjahr erfassen und den Jahresbericht vor dem 1. August vorbereiten.",
        "en": "Record the quantities placed on the market in kilograms per calendar year and prepare the annual report before 1 August.",
        "es": "Registrar las cantidades introducidas en el mercado en kilogramos por año natural y preparar el informe anual antes del 1 de agosto.",
        "fr": "Consigner les quantités mises sur le marché en kilogrammes par année civile et préparer le rapport annuel avant le 1er août.",
        "it": "Rilevare i quantitativi immessi sul mercato in chilogrammi per anno civile e predisporre la relazione annuale prima del 1° agosto.",
        "zh": "按日历年以千克为单位统计投放市场的数量，并在 8 月 1 日前准备年度报告。",
    },
    "abwv38_1": {
        "de": "Klären, ob direkt in ein Gewässer oder indirekt in die Kanalisation eingeleitet wird und welche Genehmigung (Erlaubnis oder § 58 WHG) vorliegt.",
        "en": "Clarify whether wastewater is discharged directly into a water body or indirectly into the sewer system, and which authorisation (permit, or approval under Section 58 of the German Water Resources Act (WHG)) is in place.",
        "es": "Aclarar si el vertido se realiza directamente a una masa de agua o indirectamente al alcantarillado y qué autorización existe (permiso o autorización conforme al § 58 de la Ley alemana de aguas (WHG)).",
        "fr": "Déterminer si le rejet se fait directement dans un milieu aquatique ou indirectement dans le réseau d'assainissement et de quelle autorisation l'entreprise dispose (permis ou autorisation au titre du § 58 de la loi allemande sur le régime des eaux (WHG)).",
        "it": "Chiarire se lo scarico avviene direttamente in un corpo idrico o indirettamente in fognatura e quale autorizzazione sussiste (permesso o autorizzazione ai sensi del § 58 della legge tedesca sulle acque (WHG)).",
        "zh": "明确废水是直接排入水体还是间接排入排水管网，以及持有何种许可（排放许可或依据德国《水资源法》（WHG）第 58 条的批准）。",
    },
    "abwv38_2": {
        "de": "Ein betriebliches Abwasserkataster mit Teilströmen, Restflotten und Restdruckpasten aufbauen bzw. aktualisieren.",
        "en": "Set up or update an in-house wastewater register covering partial flows, residual liquors and residual printing pastes.",
        "es": "Crear o actualizar un catastro interno de aguas residuales con los flujos parciales, los baños residuales y las pastas de estampación residuales.",
        "fr": "Établir ou mettre à jour un inventaire interne des eaux usées recensant les flux partiels, les bains résiduels et les pâtes d'impression résiduelles.",
        "it": "Predisporre o aggiornare un catasto aziendale delle acque reflue con flussi parziali, bagni residui e paste di stampa residue.",
        "zh": "建立或更新企业废水台账，涵盖分支水流、残余染液和残余印花浆。",
    },
    "abwv38_3": {
        "de": "Das Betriebstagebuch mit Herstellerangaben führen, dass Farbstoffe und Textilhilfsmittel keine nach Teil E unzulässigen Stoffe enthalten.",
        "en": "Keep the operating log with manufacturers' statements that dyes and textile auxiliaries contain no substances prohibited under Part E.",
        "es": "Llevar el diario de explotación con las declaraciones de los fabricantes de que los colorantes y los auxiliares textiles no contienen sustancias prohibidas según la parte E.",
        "fr": "Tenir le journal d'exploitation avec les déclarations des fabricants attestant que les colorants et les auxiliaires textiles ne contiennent aucune substance interdite selon la partie E.",
        "it": "Tenere il registro di esercizio con le dichiarazioni dei fabbricanti attestanti che coloranti e ausiliari tessili non contengono sostanze non ammesse ai sensi della parte E.",
        "zh": "在运行日志中记录制造商的说明，证明染料和纺织助剂不含 E 部分规定不得使用的物质。",
    },
    "abwv38_4": {
        "de": "Eigenüberwachung auf AOX, Schwermetalle und CSB mit den festgesetzten Überwachungswerten abgleichen.",
        "en": "Compare self-monitoring for AOX, heavy metals and COD with the stipulated monitoring values.",
        "es": "Contrastar el autocontrol de AOX, metales pesados y DQO con los valores de control establecidos.",
        "fr": "Comparer l'autosurveillance de l'AOX, des métaux lourds et de la DCO aux valeurs de surveillance fixées.",
        "it": "Confrontare l'autocontrollo di AOX, metalli pesanti e COD con i valori di controllo stabiliti.",
        "zh": "将 AOX、重金属和化学需氧量（COD）的自行监测与规定的监测值进行比对。",
    },
    "enefg_1": {
        "de": "Den Gesamtendenergieverbrauch der letzten drei abgeschlossenen Kalenderjahre über alle Energieträger ermitteln und mit 2,5 und 7,5 GWh vergleichen.",
        "en": "Determine the total final energy consumption across all energy sources for the last three completed calendar years and compare it with 2.5 and 7.5 GWh.",
        "es": "Determinar el consumo total de energía final de los tres últimos años naturales cerrados para todas las fuentes de energía y compararlo con 2,5 y 7,5 GWh.",
        "fr": "Déterminer la consommation totale d'énergie finale des trois dernières années civiles clôturées, toutes sources d'énergie confondues, et la comparer à 2,5 et 7,5 GWh.",
        "it": "Determinare il consumo totale di energia finale degli ultimi tre anni civili conclusi per tutti i vettori energetici e confrontarlo con 2,5 e 7,5 GWh.",
        "zh": "统计最近三个已结束日历年所有能源载体的最终能源总消耗量，并与 2.5 GWh 和 7.5 GWh 进行比较。",
    },
    "enefg_2": {
        "de": "Über 7,5 GWh ein nach DIN EN ISO 50001 zertifiziertes EnMS oder EMAS einführen und Abwärmequellen erfassen.",
        "en": "Above 7.5 GWh, introduce an energy management system (EnMS) certified to DIN EN ISO 50001 or EMAS, and record sources of waste heat.",
        "es": "Por encima de 7,5 GWh, implantar un sistema de gestión energética (EnMS) certificado según DIN EN ISO 50001 o EMAS y registrar las fuentes de calor residual.",
        "fr": "Au-delà de 7,5 GWh, mettre en place un système de management de l'énergie (EnMS) certifié selon la norme DIN EN ISO 50001 ou l'EMAS, et recenser les sources de chaleur fatale.",
        "it": "Oltre 7,5 GWh, introdurre un sistema di gestione dell'energia (EnMS) certificato secondo DIN EN ISO 50001 o EMAS e rilevare le fonti di calore di scarto.",
        "zh": "超过 7.5 GWh 的，须建立经 DIN EN ISO 50001 认证的能源管理体系（EnMS）或 EMAS，并登记余热来源。",
    },
    "enefg_3": {
        "de": "Über 2,5 GWh die wirtschaftlichen Maßnahmen nach DIN EN 17463 bewerten, Umsetzungspläne bestätigen lassen und veröffentlichen.",
        "en": "Above 2.5 GWh, assess the economically viable measures in accordance with DIN EN 17463, have the implementation plans confirmed and publish them.",
        "es": "Por encima de 2,5 GWh, evaluar las medidas rentables según DIN EN 17463, hacer confirmar los planes de ejecución y publicarlos.",
        "fr": "Au-delà de 2,5 GWh, évaluer les mesures économiquement viables selon la norme DIN EN 17463, faire confirmer les plans de mise en œuvre et les publier.",
        "it": "Oltre 2,5 GWh, valutare le misure economicamente convenienti secondo DIN EN 17463, far confermare i piani di attuazione e pubblicarli.",
        "zh": "超过 2.5 GWh 的，须按 DIN EN 17463 评估经济可行的措施，使实施计划获得确认并予以公布。",
    },
    "enefg_4": {
        "de": "Das Gesetzgebungsverfahren zu BT-Drs. 21/8027 verfolgen, da sich Schwellen und Fristen voraussichtlich ändern.",
        "en": "Follow the legislative procedure on Bundestag printed paper (BT-Drs.) 21/8027, as thresholds and deadlines are expected to change.",
        "es": "Seguir el procedimiento legislativo relativo al documento del Bundestag (BT-Drs.) 21/8027, ya que previsiblemente cambiarán umbrales y plazos.",
        "fr": "Suivre la procédure législative relative au document du Bundestag (BT-Drs.) 21/8027, car les seuils et les délais devraient changer.",
        "it": "Seguire la procedura legislativa relativa allo stampato del Bundestag (BT-Drs.) 21/8027, poiché soglie e scadenze dovrebbero cambiare.",
        "zh": "跟踪联邦议院印刷品（BT-Drs.）21/8027 所涉立法程序，因为门槛和期限预计将发生变化。",
    },
}


# ---------- Begruendungs-Bausteine fuer gekoppelte Regulierungen ----------
#
# CSRD, CSRD_DE, Taxonomie-VO, HinSchG und CSR-RUG
# werden nicht vom LLM bewertet, sondern von `regulations.coupling_verdict()`
# entschieden.
# Die Begruendung entsteht aus zwei Bausteinen und behaelt damit die
# Zwei-Satz-Struktur der LLM-Antworten:
#   Satz 1 (COUPLING_FACTS)       — Schwellenwert und der Ist-Wert des Unternehmens
#   Satz 2 (COUPLING_CONCLUSIONS) — was daraus fuer genau diese Regulierung folgt
# Dazu die feste Fundstelle aus COUPLING_PASSAGES. Alles handgeschrieben und in
# allen sechs Sprachen hinterlegt: gleiche Lage -> immer derselbe Wortlaut.

# Tausendertrennzeichen je Sprache (fr: geschuetztes Leerzeichen).
_THOUSANDS_SEP: dict[str, str] = {
    "de": ".", "en": ",", "es": ".", "fr": " ", "it": ".", "zh": ",",
}

COUPLING_FACTS: dict[str, dict[str, str]] = {
    "csrd_ueber_schwelle": {
        "de": "Das Unternehmen hat {employees} Beschäftigte (Schwelle: mehr als 1.000) und "
              "{revenue} Nettoumsatzerlöse (Schwelle: mehr als 450 Mio. EUR) und überschreitet "
              "damit beide Merkmale des Art. 19a Abs. 1 der Bilanzrichtlinie.",
        "en": "The company has {employees} employees (threshold: more than 1,000) and net turnover "
              "of {revenue} (threshold: more than EUR 450 million), exceeding both criteria of "
              "Art. 19a(1) of the Accounting Directive.",
        "es": "La empresa tiene {employees} empleados (umbral: más de 1.000) y una cifra neta de "
              "negocios de {revenue} (umbral: más de 450 millones EUR), por lo que supera ambos "
              "criterios del art. 19 bis, apdo. 1, de la Directiva contable.",
        "fr": "L'entreprise compte {employees} salariés (seuil : plus de 1 000) et un chiffre "
              "d'affaires net de {revenue} (seuil : plus de 450 millions EUR) ; elle dépasse donc "
              "les deux critères de l'art. 19 bis, par. 1, de la directive comptable.",
        "it": "L'impresa ha {employees} dipendenti (soglia: più di 1.000) e ricavi netti di "
              "{revenue} (soglia: più di 450 milioni di EUR), superando entrambi i criteri "
              "dell'art. 19 bis, par. 1, della direttiva contabile.",
        "zh": "公司有 {employees} 名员工（门槛：超过 1,000 名），净营业额为 {revenue}（门槛：超过 4.5 亿欧元），"
              "两项标准均已超过《会计指令》第 19a 条第 1 款的门槛。",
    },
    "csrd_unter_schwelle": {
        "de": "Das Unternehmen hat {employees} Beschäftigte (Schwelle: mehr als 1.000) und "
              "{revenue} Nettoumsatzerlöse (Schwelle: mehr als 450 Mio. EUR); beide Merkmale des "
              "Art. 19a Abs. 1 der Bilanzrichtlinie müssen kumulativ erfüllt sein, und mindestens "
              "eines davon ist es nicht — Bilanzsumme und Börsennotierung zählen seit der "
              "Omnibus-Änderung nicht mehr.",
        "en": "The company has {employees} employees (threshold: more than 1,000) and net turnover "
              "of {revenue} (threshold: more than EUR 450 million); both criteria of Art. 19a(1) of "
              "the Accounting Directive have to be met cumulatively, and at least one of them is "
              "not — balance sheet total and stock exchange listing no longer count after the "
              "Omnibus amendment.",
        "es": "La empresa tiene {employees} empleados (umbral: más de 1.000) y una cifra neta de "
              "negocios de {revenue} (umbral: más de 450 millones EUR); ambos criterios del "
              "art. 19 bis, apdo. 1, de la Directiva contable deben cumplirse de forma acumulativa "
              "y al menos uno de ellos no se cumple — el balance total y la cotización bursátil ya "
              "no cuentan tras la modificación Ómnibus.",
        "fr": "L'entreprise compte {employees} salariés (seuil : plus de 1 000) et un chiffre "
              "d'affaires net de {revenue} (seuil : plus de 450 millions EUR) ; les deux critères "
              "de l'art. 19 bis, par. 1, de la directive comptable doivent être remplis "
              "cumulativement et au moins l'un d'eux ne l'est pas — le total du bilan et la "
              "cotation ne comptent plus depuis la révision Omnibus.",
        "it": "L'impresa ha {employees} dipendenti (soglia: più di 1.000) e ricavi netti di "
              "{revenue} (soglia: più di 450 milioni di EUR); entrambi i criteri dell'art. 19 bis, "
              "par. 1, della direttiva contabile devono essere soddisfatti cumulativamente e almeno "
              "uno di essi non lo è — il totale di bilancio e la quotazione non contano più dopo la "
              "modifica Omnibus.",
        "zh": "公司有 {employees} 名员工（门槛：超过 1,000 名），净营业额为 {revenue}（门槛：超过 4.5 亿欧元）；"
              "《会计指令》第 19a 条第 1 款的两项标准必须同时满足，而其中至少有一项未满足——经 Omnibus 修订后，"
              "资产负债表总额和上市与否已不再计入。",
    },
    "csrd_ueber_schwelle_tochter": {
        "de": "Das Unternehmen hat {employees} Beschäftigte (Schwelle: mehr als 1.000) und "
              "{revenue} Nettoumsatzerlöse (Schwelle: mehr als 450 Mio. EUR), überschreitet damit "
              "beide Merkmale des Art. 19a Abs. 1 der Bilanzrichtlinie und ist zugleich "
              "Tochterunternehmen — nach Art. 19a Abs. 9 ist eine Befreiung möglich, wenn der "
              "Konzernbericht der Mutter es einbezieht.",
        "en": "The company has {employees} employees (threshold: more than 1,000) and net turnover "
              "of {revenue} (threshold: more than EUR 450 million), thus exceeding both criteria of "
              "Art. 19a(1) of the Accounting Directive, and it is a subsidiary — under Art. 19a(9) "
              "an exemption is possible if the parent's consolidated report covers it.",
        "es": "La empresa tiene {employees} empleados (umbral: más de 1.000) y una cifra neta de "
              "negocios de {revenue} (umbral: más de 450 millones EUR), supera así ambos criterios "
              "del art. 19 bis, apdo. 1, de la Directiva contable y es a la vez filial: según el "
              "art. 19 bis, apdo. 9, cabe una exención si el informe consolidado de la matriz la "
              "incluye.",
        "fr": "L'entreprise compte {employees} salariés (seuil : plus de 1 000) et un chiffre "
              "d'affaires net de {revenue} (seuil : plus de 450 millions EUR), dépasse donc les "
              "deux critères de l'art. 19 bis, par. 1, de la directive comptable et est en même "
              "temps une filiale : l'art. 19 bis, par. 9, permet une exemption si le rapport "
              "consolidé de la mère la couvre.",
        "it": "L'impresa ha {employees} dipendenti (soglia: più di 1.000) e ricavi netti di "
              "{revenue} (soglia: più di 450 milioni di EUR), supera quindi entrambi i criteri "
              "dell'art. 19 bis, par. 1, della direttiva contabile ed è al contempo una "
              "controllata: l'art. 19 bis, par. 9, consente un'esenzione se la relazione "
              "consolidata della capogruppo la include.",
        "zh": "公司有 {employees} 名员工（门槛：超过 1,000 名），净营业额为 {revenue}（门槛：超过 4.5 亿欧元），"
              "已超过《会计指令》第 19a 条第 1 款的两项标准，同时又是子公司——依第 19a 条第 9 款，"
              "若母公司的合并报告已涵盖本公司，则可豁免。",
    },
    "csrd_drittland": {
        "de": "Die oberste Muttergesellschaft sitzt außerhalb der EU und der Nettoumsatz in der "
              "Union beträgt {revenue_eu} (Schwelle des Art. 40a Bilanzrichtlinie: mehr als "
              "450 Mio. EUR); ob zusätzlich eine EU-Tochter als großes Unternehmen gilt oder eine "
              "Zweigniederlassung mehr als 200 Mio. EUR Umsatz erzielt, geht aus dem Profil "
              "nicht hervor.",
        "en": "The ultimate parent is established outside the EU and net turnover in the Union is "
              "{revenue_eu} (threshold of Art. 40a of the Accounting Directive: more than EUR 450 "
              "million); whether an EU subsidiary additionally qualifies as a large undertaking, or "
              "a branch exceeds EUR 200 million in turnover, is not stated in the profile.",
        "es": "La sociedad matriz última tiene su sede fuera de la UE y la cifra neta de negocios "
              "en la Unión es de {revenue_eu} (umbral del art. 40a de la Directiva contable: más "
              "de 450 millones EUR); el perfil no indica si además una filial en la UE es una gran "
              "empresa o si una sucursal supera los 200 millones EUR de cifra de negocios.",
        "fr": "La société mère ultime est établie hors de l'UE et le chiffre d'affaires net réalisé "
              "dans l'Union s'élève à {revenue_eu} (seuil de l'art. 40a de la directive comptable : "
              "plus de 450 millions EUR) ; le profil n'indique pas si une filiale de l'UE est en outre "
              "une grande entreprise ni si une succursale dépasse 200 millions EUR de chiffre "
              "d'affaires.",
        "it": "La capogruppo ha sede fuori dall'UE e i ricavi netti realizzati nell'Unione "
              "ammontano a {revenue_eu} (soglia dell'art. 40a della direttiva contabile: più di "
              "450 milioni di EUR); dal profilo non risulta se una controllata UE sia inoltre una "
              "grande impresa né se una succursale superi i 200 milioni di EUR di ricavi.",
        "zh": "最终母公司设在欧盟境外，在欧盟境内的净营业额为 {revenue_eu}（《会计指令》第 40a 条门槛：超过 4.5 亿欧元）；"
              "档案中未说明欧盟子公司是否另属大型企业，或分支机构营业额是否超过 2 亿欧元。",
    },
    # Altprofile und Nutzer, die den EU-Umsatz nicht angeben: Art. 40a stellt
    # auf den Unionsumsatz ab, im Profil steht nur der weltweite. Der Fall wird
    # deshalb offen gehalten und die Luecke ausdruecklich benannt.
    "csrd_drittland_ohne_eu_umsatz": {
        "de": "Die oberste Muttergesellschaft sitzt außerhalb der EU und der weltweite Nettoumsatz "
              "beträgt {revenue}; Art. 40a der Bilanzrichtlinie stellt jedoch auf den Nettoumsatz "
              "in der Union ab (mehr als 450 Mio. EUR), und dieser ist im Profil nicht angegeben.",
        "en": "The ultimate parent is established outside the EU and worldwide net turnover is "
              "{revenue}; Art. 40a of the Accounting Directive, however, relies on net turnover in "
              "the Union (more than EUR 450 million), which the profile does not state.",
        "es": "La sociedad matriz última tiene su sede fuera de la UE y la cifra neta de negocios "
              "mundial es de {revenue}; sin embargo, el art. 40a de la Directiva contable se basa "
              "en la cifra de negocios en la Unión (más de 450 millones EUR), que no consta en el "
              "perfil.",
        "fr": "La société mère ultime est établie hors de l'UE et le chiffre d'affaires net mondial "
              "s'élève à {revenue} ; l'art. 40a de la directive comptable se fonde toutefois sur le "
              "chiffre d'affaires réalisé dans l'Union (plus de 450 millions EUR), qui n'est pas "
              "indiqué dans le profil.",
        "it": "La capogruppo ha sede fuori dall'UE e i ricavi netti mondiali ammontano a {revenue}; "
              "l'art. 40a della direttiva contabile si basa però sui ricavi netti realizzati "
              "nell'Unione (più di 450 milioni di EUR), che il profilo non indica.",
        "zh": "最终母公司设在欧盟境外，全球净营业额为 {revenue}；但《会计指令》第 40a 条以在欧盟境内的净营业额为准"
              "（超过 4.5 亿欧元），而档案中未填写该数值。",
    },
    "csrd_welle1": {
        "de": "Das Unternehmen ist kapitalmarktorientiert und hat {employees} Beschäftigte "
              "(Welle-1-Schwelle: mehr als 500), erreicht mit {revenue} aber nicht die ab dem "
              "Geschäftsjahr 2027 geltende Umsatzschwelle von 450 Mio. EUR; ob der Sitzstaat die "
              "Befreiungsoption für 2025/2026 gezogen hat, ist offen.",
        "en": "The company is capital-market oriented and has {employees} employees (wave 1 "
              "threshold: more than 500), but with {revenue} it does not reach the turnover "
              "threshold of EUR 450 million applicable from financial year 2027; whether its home "
              "member state used the exemption option for 2025/2026 is open.",
        "es": "La empresa cotiza en un mercado regulado y tiene {employees} empleados (umbral de la "
              "primera ola: más de 500), pero con {revenue} no alcanza el umbral de 450 millones "
              "EUR aplicable desde el ejercicio 2027; queda abierto si su Estado miembro ha usado "
              "la opción de exención para 2025/2026.",
        "fr": "L'entreprise est cotée et compte {employees} salariés (seuil de la vague 1 : plus de "
              "500), mais avec {revenue} elle n'atteint pas le seuil de 450 millions EUR applicable "
              "à partir de l'exercice 2027 ; la question de savoir si son État membre a utilisé "
              "l'option d'exemption pour 2025/2026 reste ouverte.",
        "it": "L'impresa è quotata e ha {employees} dipendenti (soglia della prima ondata: più di "
              "500), ma con {revenue} non raggiunge la soglia di 450 milioni di EUR valida "
              "dall'esercizio 2027; resta aperto se lo Stato membro abbia esercitato l'opzione di "
              "esenzione per il 2025/2026.",
        "zh": "公司为资本市场导向企业，有 {employees} 名员工（第一批门槛：超过 500 名），但 {revenue} 的营业额未达到自 2027 "
              "财政年度起适用的 4.5 亿欧元门槛；其所在成员国是否行使了 2025/2026 年度的豁免选项尚不明确。",
    },
    "hinschg_ab_50": {
        "de": "Das Unternehmen beschäftigt {employees_de} Personen in Deutschland und erreicht "
              "damit die Schwelle von 50 Beschäftigten des § 12 Abs. 2 HinSchG.",
        "en": "The company employs {employees_de} people in Germany and thus reaches the threshold "
              "of 50 employees in section 12(2) HinSchG.",
        "es": "La empresa emplea a {employees_de} personas en Alemania y alcanza así el umbral de "
              "50 empleados del § 12, apdo. 2, HinSchG.",
        "fr": "L'entreprise emploie {employees_de} personnes en Allemagne et atteint ainsi le seuil "
              "de 50 salariés du § 12, al. 2, HinSchG.",
        "it": "L'impresa occupa {employees_de} persone in Germania e raggiunge così la soglia di 50 "
              "dipendenti del § 12, comma 2, HinSchG.",
        "zh": "公司在德国雇用 {employees_de} 人，已达到《举报人保护法》第 12 条第 2 款规定的 50 人门槛。",
    },
    "hinschg_unter_50_finanz": {
        "de": "Das Unternehmen beschäftigt {employees_de} Personen in Deutschland und bleibt damit "
              "unter der Schwelle von 50 Beschäftigten, gehört aber zum Finanzsektor, den § 12 "
              "Abs. 3 HinSchG unabhängig von der Beschäftigtenzahl erfasst.",
        "en": "The company employs {employees_de} people in Germany and thus stays below the "
              "threshold of 50 employees, but belongs to the financial sector, which section 12(3) "
              "HinSchG covers irrespective of headcount.",
        "es": "La empresa emplea a {employees_de} personas en Alemania y queda por debajo del "
              "umbral de 50 empleados, pero pertenece al sector financiero, al que el § 12, "
              "apdo. 3, HinSchG alcanza con independencia del número de empleados.",
        "fr": "L'entreprise emploie {employees_de} personnes en Allemagne et reste sous le seuil de "
              "50 salariés, mais relève du secteur financier, que le § 12, al. 3, HinSchG vise "
              "indépendamment de l'effectif.",
        "it": "L'impresa occupa {employees_de} persone in Germania e resta sotto la soglia di 50 "
              "dipendenti, ma appartiene al settore finanziario, che il § 12, comma 3, HinSchG "
              "include a prescindere dal numero di dipendenti.",
        "zh": "公司在德国雇用 {employees_de} 人，低于 50 人门槛，但属于金融领域，"
              "《举报人保护法》第 12 条第 3 款对该领域的适用不以员工人数为条件。",
    },
    "hinschg_unter_50": {
        "de": "Das Unternehmen beschäftigt {employees_de} Personen in Deutschland und bleibt damit "
              "unter der Schwelle von 50 Beschäftigten des § 12 Abs. 2 HinSchG.",
        "en": "The company employs {employees_de} people in Germany and thus stays below the "
              "threshold of 50 employees in section 12(2) HinSchG.",
        "es": "La empresa emplea a {employees_de} personas en Alemania y queda así por debajo del "
              "umbral de 50 empleados del § 12, apdo. 2, HinSchG.",
        "fr": "L'entreprise emploie {employees_de} personnes en Allemagne et reste ainsi sous le "
              "seuil de 50 salariés du § 12, al. 2, HinSchG.",
        "it": "L'impresa occupa {employees_de} persone in Germania e resta quindi sotto la soglia "
              "di 50 dipendenti del § 12, comma 2, HinSchG.",
        "zh": "公司在德国雇用 {employees_de} 人，低于《举报人保护法》第 12 条第 2 款规定的 50 人门槛。",
    },
    # --- CSR-RUG (§ 289b HGB) ---
    "csr_rug_erfuellt": {
        "de": "Das Unternehmen ist kapitalmarktorientiert und beschäftigte im Jahresdurchschnitt "
              "{employees} Arbeitnehmer (Schwelle: mehr als 500); eine kapitalmarktorientierte "
              "Kapitalgesellschaft gilt nach § 267 Abs. 3 Satz 2 HGB stets als groß, womit das "
              "Größenmerkmal des § 289b Abs. 1 Nr. 1 HGB regelmäßig mitverwirklicht ist.",
        "en": "The company is capital-market oriented and had {employees} employees on annual average "
              "(threshold: more than 500); under section 267(3) sentence 2 HGB a capital-market "
              "oriented company always counts as large, so the size criterion of section 289b(1) no. 1 "
              "HGB is regularly met as well.",
        "es": "La empresa está orientada al mercado de capitales y tenía {employees} trabajadores de "
              "media anual (umbral: más de 500); según el § 267, apdo. 3, frase 2 HGB una sociedad "
              "orientada al mercado de capitales cuenta siempre como grande, por lo que el criterio de "
              "tamaño del § 289b, apdo. 1, n.º 1, HGB queda por regla general cumplido.",
        "fr": "L'entreprise fait appel au marché des capitaux et employait {employees} salariés en "
              "moyenne annuelle (seuil : plus de 500) ; selon le § 267, al. 3, phrase 2 HGB, une "
              "société faisant appel au marché des capitaux est toujours réputée grande, de sorte que "
              "le critère de taille du § 289b, al. 1, n° 1, HGB est en règle générale rempli.",
        "it": "L'impresa fa ricorso al mercato dei capitali e aveva {employees} dipendenti in media "
              "annua (soglia: più di 500); ai sensi del § 267, c. 3, per. 2 HGB una società che fa "
              "ricorso al mercato dei capitali è sempre considerata grande, per cui il criterio "
              "dimensionale del § 289b, c. 1, n. 1, HGB risulta di regola soddisfatto.",
        "zh": "该企业属于资本市场导向企业，年平均雇员 {employees} 人（门槛：超过 500 人）；依《商法典》第 267 条第 3 款第 2 句，资本市场导向的资合公司始终视为大型企业，因此第 289b 条第 1 款第 1 项的规模要件通常一并满足。",
    },
    "csr_rug_erfuellt_tochter": {
        "de": "Das Unternehmen ist kapitalmarktorientiert, beschäftigte im Jahresdurchschnitt "
              "{employees} Arbeitnehmer (Schwelle: mehr als 500) und ist zugleich Tochterunternehmen — "
              "nach § 289b Abs. 2 HGB ist eine Befreiung möglich, wenn der Konzernlagebericht der "
              "Mutter eine nichtfinanzielle Konzernerklärung enthält.",
        "en": "The company is capital-market oriented, had {employees} employees on annual average "
              "(threshold: more than 500) and is at the same time a subsidiary — under section 289b(2) "
              "HGB an exemption is possible if the parent's consolidated management report contains a "
              "consolidated non-financial statement.",
        "es": "La empresa está orientada al mercado de capitales, tenía {employees} trabajadores de "
              "media anual (umbral: más de 500) y es a la vez filial: según el § 289b, apdo. 2, HGB "
              "cabe una exención si el informe de gestión consolidado de la matriz incluye un estado "
              "no financiero consolidado.",
        "fr": "L'entreprise fait appel au marché des capitaux, employait {employees} salariés en "
              "moyenne annuelle (seuil : plus de 500) et est en même temps une filiale : selon le "
              "§ 289b, al. 2, HGB, une exemption est possible si le rapport de gestion consolidé de la "
              "société mère contient une déclaration non financière consolidée.",
        "it": "L'impresa fa ricorso al mercato dei capitali, aveva {employees} dipendenti in media "
              "annua (soglia: più di 500) ed è al contempo una controllata: ai sensi del § 289b, c. 2, "
              "HGB è possibile un'esenzione se la relazione consolidata sulla gestione della "
              "capogruppo contiene una dichiarazione non finanziaria consolidata.",
        "zh": "该企业属于资本市场导向企业，年平均雇员 {employees} 人（门槛：超过 500 人），同时又是子公司——依《商法典》第 289b 条第 2 款，若母公司的合并管理报告中含有合并非财务声明，则可获豁免。",
    },
    "csr_rug_rechtsform": {
        "de": "Das Unternehmen ist kapitalmarktorientiert und beschäftigte {employees} Arbeitnehmer "
              "(Schwelle: mehr als 500), hat aber eine Rechtsform außerhalb der von § 289b HGB und "
              "§ 264a HGB erfassten Kapitalgesellschaften.",
        "en": "The company is capital-market oriented and had {employees} employees (threshold: more "
              "than 500), but its legal form lies outside the companies covered by sections 289b and "
              "264a HGB.",
        "es": "La empresa está orientada al mercado de capitales y tenía {employees} trabajadores "
              "(umbral: más de 500), pero su forma jurídica queda fuera de las sociedades cubiertas por "
              "los §§ 289b y 264a HGB.",
        "fr": "L'entreprise fait appel au marché des capitaux et employait {employees} salariés "
              "(seuil : plus de 500), mais sa forme juridique se situe hors des sociétés visées par les "
              "§§ 289b et 264a HGB.",
        "it": "L'impresa fa ricorso al mercato dei capitali e aveva {employees} dipendenti (soglia: più "
              "di 500), ma la sua forma giuridica esula dalle società coperte dai §§ 289b e 264a HGB.",
        "zh": "该企业属于资本市场导向企业，雇员 {employees} 人（门槛：超过 500 人），但其法律形式不属于《商法典》第 289b 条和第 264a 条所涵盖的资合公司。",
    },
    "csr_rug_finanz": {
        "de": "Das Unternehmen ist nicht kapitalmarktorientiert, beschäftigte aber {employees} "
              "Arbeitnehmer (Schwelle: mehr als 500); für Kreditinstitute und Versicherungsunternehmen "
              "entfällt das Merkmal der Kapitalmarktorientierung (§ 340a Abs. 1a, § 341a Abs. 1a HGB).",
        "en": "The company is not capital-market oriented but had {employees} employees (threshold: "
              "more than 500); for credit institutions and insurance undertakings the capital-market "
              "criterion does not apply (sections 340a(1a), 341a(1a) HGB).",
        "es": "La empresa no está orientada al mercado de capitales, pero tenía {employees} "
              "trabajadores (umbral: más de 500); para entidades de crédito y aseguradoras decae el "
              "criterio de orientación al mercado de capitales (§ 340a, apdo. 1a, y § 341a, apdo. 1a, "
              "HGB).",
        "fr": "L'entreprise ne fait pas appel au marché des capitaux mais employait {employees} "
              "salariés (seuil : plus de 500) ; pour les établissements de crédit et les entreprises "
              "d'assurance, le critère de l'appel au marché des capitaux ne s'applique pas "
              "(§ 340a, al. 1a, et § 341a, al. 1a, HGB).",
        "it": "L'impresa non fa ricorso al mercato dei capitali ma aveva {employees} dipendenti "
              "(soglia: più di 500); per gli enti creditizi e le imprese di assicurazione il criterio "
              "del ricorso al mercato dei capitali non si applica (§ 340a, c. 1a, e § 341a, c. 1a, HGB).",
        "zh": "该企业并非资本市场导向企业，但雇员 {employees} 人（门槛：超过 500 人）；对信贷机构和保险企业而言，资本市场导向这一要件不适用（《商法典》第 340a 条第 1a 款、第 341a 条第 1a 款）。",
    },
    "csr_rug_unter_500": {
        "de": "Das Unternehmen ist kapitalmarktorientiert, beschäftigte im Jahresdurchschnitt aber nur "
              "{employees} Arbeitnehmer und erreicht damit die Schwelle des § 289b Abs. 1 Nr. 3 HGB "
              "von mehr als 500 Arbeitnehmern nicht.",
        "en": "The company is capital-market oriented but had only {employees} employees on annual "
              "average and therefore does not reach the threshold of more than 500 employees in "
              "section 289b(1) no. 3 HGB.",
        "es": "La empresa está orientada al mercado de capitales, pero solo tenía {employees} "
              "trabajadores de media anual y no alcanza el umbral de más de 500 del § 289b, apdo. 1, "
              "n.º 3, HGB.",
        "fr": "L'entreprise fait appel au marché des capitaux mais n'employait que {employees} salariés "
              "en moyenne annuelle et n'atteint donc pas le seuil de plus de 500 du § 289b, al. 1, "
              "n° 3, HGB.",
        "it": "L'impresa fa ricorso al mercato dei capitali ma aveva solo {employees} dipendenti in "
              "media annua e non raggiunge quindi la soglia di oltre 500 del § 289b, c. 1, n. 3, HGB.",
        "zh": "该企业虽属资本市场导向企业，但年平均雇员仅 {employees} 人，未达到《商法典》第 289b 条第 1 款第 3 项超过 500 人的门槛。",
    },
    "csr_rug_nicht_kapitalmarkt": {
        "de": "Das Unternehmen ist nicht kapitalmarktorientiert im Sinne des § 264d HGB; dieses "
              "Merkmal verlangt § 289b Abs. 1 Nr. 2 HGB kumulativ neben der Größe und mehr als 500 "
              "Arbeitnehmern (laut Profil {employees}).",
        "en": "The company is not capital-market oriented within the meaning of section 264d HGB; "
              "section 289b(1) no. 2 HGB requires this criterion cumulatively alongside size and more "
              "than 500 employees ({employees} according to the profile).",
        "es": "La empresa no está orientada al mercado de capitales en el sentido del § 264d HGB; el "
              "§ 289b, apdo. 1, n.º 2, HGB exige este criterio de forma acumulativa junto al tamaño y "
              "a más de 500 trabajadores (según el perfil, {employees}).",
        "fr": "L'entreprise ne fait pas appel au marché des capitaux au sens du § 264d HGB ; le "
              "§ 289b, al. 1, n° 2, HGB exige ce critère cumulativement avec la taille et plus de 500 "
              "salariés ({employees} selon le profil).",
        "it": "L'impresa non fa ricorso al mercato dei capitali ai sensi del § 264d HGB; il § 289b, "
              "c. 1, n. 2, HGB richiede tale criterio cumulativamente con la dimensione e con più di "
              "500 dipendenti (secondo il profilo {employees}).",
        "zh": "该企业不属于《商法典》第 264d 条意义上的资本市场导向企业；第 289b 条第 1 款第 2 项要求该要件与规模及超过 500 名雇员（档案显示 {employees} 人）累积满足。",
    },
    # --- Katalogerweiterung 29.09.2026 ---
    "svhc_ja": {
        "de": "Das Unternehmen gibt an, dass seine Produkte Stoffe der ECHA-Kandidatenliste mit mehr als 0,1 Massenprozent enthalten (Schwelle: 0,1 Massenprozent je Erzeugnis).",
        "en": "The company states that its products contain substances on the ECHA Candidate List above 0.1% by weight (threshold: 0.1% by weight per article).",
        "es": "La empresa indica que sus productos contienen sustancias de la Lista de candidatas de la ECHA en más del 0,1 % en peso (umbral: 0,1 % en peso por artículo).",
        "fr": "L'entreprise indique que ses produits contiennent des substances de la liste des substances candidates de l'ECHA à plus de 0,1 % en masse (seuil : 0,1 % en masse par article).",
        "it": "L'impresa dichiara che i suoi prodotti contengono sostanze dell'elenco di sostanze candidate dell'ECHA in misura superiore allo 0,1% in peso (soglia: 0,1% in peso per articolo).",
        "zh": "公司表示，其产品含有 ECHA 候选清单中质量分数超过 0.1% 的物质（门槛：每件物品质量分数 0.1%）。",
    },
    "svhc_nein": {
        "de": "Das Unternehmen gibt an, dass seine Produkte keine Stoffe der ECHA-Kandidatenliste mit mehr als 0,1 Massenprozent enthalten (Schwelle: 0,1 Massenprozent je Erzeugnis).",
        "en": "The company states that its products do not contain substances on the ECHA Candidate List above 0.1% by weight (threshold: 0.1% by weight per article).",
        "es": "La empresa indica que sus productos no contienen sustancias de la Lista de candidatas de la ECHA en más del 0,1 % en peso (umbral: 0,1 % en peso por artículo).",
        "fr": "L'entreprise indique que ses produits ne contiennent pas de substances de la liste des substances candidates de l'ECHA à plus de 0,1 % en masse (seuil : 0,1 % en masse par article).",
        "it": "L'impresa dichiara che i suoi prodotti non contengono sostanze dell'elenco di sostanze candidate dell'ECHA in misura superiore allo 0,1% in peso (soglia: 0,1% in peso per articolo).",
        "zh": "公司表示，其产品不含 ECHA 候选清单中质量分数超过 0.1% 的物质（门槛：每件物品质量分数 0.1%）。",
    },
    "svhc_unbekannt": {
        "de": "Das Unternehmen weiß nach eigener Angabe nicht, ob seine Produkte Stoffe der ECHA-Kandidatenliste mit mehr als 0,1 Massenprozent enthalten (Schwelle: 0,1 Massenprozent je Erzeugnis).",
        "en": "By its own account, the company does not know whether its products contain substances on the ECHA Candidate List above 0.1% by weight (threshold: 0.1% by weight per article).",
        "es": "Según sus propias indicaciones, la empresa no sabe si sus productos contienen sustancias de la Lista de candidatas de la ECHA en más del 0,1 % en peso (umbral: 0,1 % en peso por artículo).",
        "fr": "Selon ses propres indications, l'entreprise ne sait pas si ses produits contiennent des substances de la liste des substances candidates de l'ECHA à plus de 0,1 % en masse (seuil : 0,1 % en masse par article).",
        "it": "Secondo quanto dichiara, l'impresa non sa se i suoi prodotti contengano sostanze dell'elenco di sostanze candidate dell'ECHA in misura superiore allo 0,1% in peso (soglia: 0,1% in peso per articolo).",
        "zh": "据公司自述，其不清楚产品是否含有 ECHA 候选清单中质量分数超过 0.1% 的物质（门槛：每件物品质量分数 0.1%）。",
    },
    "kein_eu_markt": {
        "de": "Das Unternehmen setzt nach seinen Angaben ausschließlich außerhalb von EU und EWR ab, während die Vorschrift an das Bereitstellen der Produkte auf dem Markt der Union anknüpft.",
        "en": "According to its information, the company sells exclusively outside the EU and EEA, whereas the provision is linked to making the products available on the Union market.",
        "es": "Según sus datos, la empresa vende exclusivamente fuera de la UE y del EEE, mientras que la norma se vincula a la comercialización de los productos en el mercado de la Unión.",
        "fr": "Selon ses indications, l'entreprise vend exclusivement en dehors de l'UE et de l'EEE, alors que la disposition se rattache à la mise à disposition des produits sur le marché de l'Union.",
        "it": "Secondo quanto dichiarato, l'impresa vende esclusivamente al di fuori dell'UE e del SEE, mentre la norma si ricollega alla messa a disposizione dei prodotti sul mercato dell'Unione.",
        "zh": "据公司提供的信息，其仅在欧盟和欧洲经济区以外销售，而该规定以在欧盟市场上提供产品为适用前提。",
    },
    "bpr_ausruestung": {
        "de": "Das Unternehmen setzt nach seinen Angaben eine antimikrobielle bzw. biozide Ausrüstung ein; solche Textilien sind behandelte Waren im Sinne der Biozid-Verordnung.",
        "en": "According to its information, the company uses an antimicrobial or biocidal finish; such textiles are treated articles within the meaning of the Biocidal Products Regulation.",
        "es": "Según sus datos, la empresa utiliza un acabado antimicrobiano o biocida; estos textiles son artículos tratados en el sentido del Reglamento de biocidas.",
        "fr": "Selon ses indications, l'entreprise utilise un apprêt antimicrobien ou biocide ; ces textiles sont des articles traités au sens du règlement sur les produits biocides.",
        "it": "Secondo quanto dichiarato, l'impresa utilizza un finissaggio antimicrobico o biocida; tali tessili sono articoli trattati ai sensi del regolamento sui biocidi.",
        "zh": "据公司提供的信息，其采用抗菌或杀生物整理；此类纺织品属于《生物杀灭剂法规》所指的经处理物品。",
    },
    "bpr_unbekannt": {
        "de": "Das Unternehmen kann nach seinen Angaben nicht ausschließen, dass seine Textilien chemisch ausgerüstet sind; ob darunter eine biozide Ausrüstung ist, die sie zu behandelten Waren macht, steht damit nicht fest.",
        "en": "According to its information, the company cannot rule out that its textiles are chemically finished; whether this includes a biocidal finish that makes them treated articles is therefore not established.",
        "es": "Según sus datos, la empresa no puede descartar que sus textiles tengan acabados químicos; por tanto, no consta si entre ellos hay un acabado biocida que los convierta en artículos tratados.",
        "fr": "Selon ses indications, l'entreprise ne peut pas exclure que ses textiles aient reçu des apprêts chimiques ; il n'est donc pas établi s'il s'y trouve un apprêt biocide qui en ferait des articles traités.",
        "it": "Secondo quanto dichiarato, l'impresa non può escludere che i suoi tessili siano sottoposti a finissaggi chimici; non è quindi accertato se tra questi vi sia un finissaggio biocida che li renda articoli trattati.",
        "zh": "据公司提供的信息，其无法排除其纺织品经过化学整理；因此无法确定其中是否有使其成为经处理物品的杀生物整理。",
    },
    "bpr_keine": {
        "de": "Das Unternehmen gibt keine antimikrobielle oder biozide Ausrüstung seiner Produkte an; ohne sie liegt keine behandelte Ware im Sinne der Biozid-Verordnung vor.",
        "en": "The company does not state any antimicrobial or biocidal finish of its products; without one, there is no treated article within the meaning of the Biocidal Products Regulation.",
        "es": "La empresa no indica ningún acabado antimicrobiano o biocida de sus productos; sin él no existe un artículo tratado en el sentido del Reglamento de biocidas.",
        "fr": "L'entreprise n'indique aucun apprêt antimicrobien ou biocide de ses produits ; en son absence, il n'y a pas d'article traité au sens du règlement sur les produits biocides.",
        "it": "L'impresa non indica alcun finissaggio antimicrobico o biocida dei suoi prodotti; in sua assenza non sussiste un articolo trattato ai sensi del regolamento sui biocidi.",
        "zh": "公司未说明其产品采用任何抗菌或杀生物整理；没有此类整理，即不构成《生物杀灭剂法规》所指的经处理物品。",
    },
    "psa_kategorie": {
        "de": "Das Unternehmen führt die Produktkategorie „Schutztextilien / PSA“; persönliche Schutzausrüstung unterliegt der PSA-Verordnung, sobald sie auf dem Markt bereitgestellt wird.",
        "en": "The company lists the product category “Protective textiles / PPE”; personal protective equipment is subject to the PPE Regulation as soon as it is made available on the market.",
        "es": "La empresa incluye la categoría de producto «Textiles de protección / EPI»; los equipos de protección individual están sujetos al Reglamento de EPI en cuanto se comercializan.",
        "fr": "L'entreprise indique la catégorie de produits « Textiles de protection / EPI » ; les équipements de protection individuelle relèvent du règlement EPI dès leur mise à disposition sur le marché.",
        "it": "L'impresa indica la categoria di prodotto «Tessili protettivi / DPI»; i dispositivi di protezione individuale sono soggetti al regolamento DPI non appena sono messi a disposizione sul mercato.",
        "zh": "公司列有“防护纺织品 / 个人防护装备”产品类别；个人防护装备一旦在市场上提供，即受《个人防护装备法规》约束。",
    },
    "psa_zulieferer": {
        "de": "Das Unternehmen führt die Produktkategorie „Schutztextilien / PSA“, ist aber nach seinen Angaben nur Zulieferer; die Pflichten der PSA-Verordnung treffen Hersteller, Bevollmächtigte, Einführer und Händler des fertigen Produkts.",
        "en": "The company lists the product category “Protective textiles / PPE” but, according to its information, is only a supplier; the obligations of the PPE Regulation fall on manufacturers, authorised representatives, importers and distributors of the finished product.",
        "es": "La empresa incluye la categoría de producto «Textiles de protección / EPI», pero según sus datos es solo proveedora; las obligaciones del Reglamento de EPI recaen en los fabricantes, representantes autorizados, importadores y distribuidores del producto acabado.",
        "fr": "L'entreprise indique la catégorie de produits « Textiles de protection / EPI », mais n'est selon ses indications qu'un fournisseur ; les obligations du règlement EPI incombent aux fabricants, mandataires, importateurs et distributeurs du produit fini.",
        "it": "L'impresa indica la categoria di prodotto «Tessili protettivi / DPI», ma secondo quanto dichiarato è solo fornitore; gli obblighi del regolamento DPI gravano su fabbricanti, mandatari, importatori e distributori del prodotto finito.",
        "zh": "公司列有“防护纺织品 / 个人防护装备”产品类别，但据其提供的信息仅为供应商；《个人防护装备法规》规定的义务由成品的制造商、授权代表、进口商和分销商承担。",
    },
    "psa_keine": {
        "de": "Das Unternehmen führt die Produktkategorie „Schutztextilien / PSA“ nicht; die PSA-Verordnung gilt nur für persönliche Schutzausrüstung.",
        "en": "The company does not list the product category “Protective textiles / PPE”; the PPE Regulation applies only to personal protective equipment.",
        "es": "La empresa no incluye la categoría de producto «Textiles de protección / EPI»; el Reglamento de EPI solo se aplica a los equipos de protección individual.",
        "fr": "L'entreprise n'indique pas la catégorie de produits « Textiles de protection / EPI » ; le règlement EPI ne s'applique qu'aux équipements de protection individuelle.",
        "it": "L'impresa non indica la categoria di prodotto «Tessili protettivi / DPI»; il regolamento DPI si applica solo ai dispositivi di protezione individuale.",
        "zh": "公司未列有“防护纺织品 / 个人防护装备”产品类别；《个人防护装备法规》仅适用于个人防护装备。",
    },
    "mdr_kategorie": {
        "de": "Das Unternehmen führt die Produktkategorie „Medizin- und Gesundheitstextilien“; ein Medizinprodukt liegt aber nur vor, wenn der Hersteller dem Produkt eine medizinische Zweckbestimmung gibt (Art. 2 Nr. 1 MDR).",
        "en": "The company lists the product category “Medical and healthcare textiles”; however, a product is a medical device only if the manufacturer assigns it a medical intended purpose (Art. 2(1) MDR).",
        "es": "La empresa incluye la categoría de producto «Textiles médicos y sanitarios»; sin embargo, solo hay un producto sanitario si el fabricante atribuye al producto una finalidad prevista médica (art. 2, punto 1, MDR).",
        "fr": "L'entreprise indique la catégorie de produits « Textiles médicaux et de santé » ; un dispositif médical n'existe toutefois que si le fabricant confère au produit une destination médicale (art. 2, point 1, MDR).",
        "it": "L'impresa indica la categoria di prodotto «Tessili medicali e sanitari»; tuttavia un dispositivo medico sussiste solo se il fabbricante attribuisce al prodotto una destinazione d'uso medica (art. 2, punto 1, MDR).",
        "zh": "公司列有“医疗与卫生用纺织品”产品类别；但只有在制造商赋予产品医疗预期用途时，该产品才属于医疗器械（MDR 第 2 条第 1 点）。",
    },
    "mdr_zulieferer": {
        "de": "Das Unternehmen führt die Produktkategorie „Medizin- und Gesundheitstextilien“, ist aber nach seinen Angaben nur Zulieferer; die Pflichten der MDR treffen Hersteller, Bevollmächtigte, Importeure und Händler von Medizinprodukten.",
        "en": "The company lists the product category “Medical and healthcare textiles” but, according to its information, is only a supplier; the obligations of the MDR fall on manufacturers, authorised representatives, importers and distributors of medical devices.",
        "es": "La empresa incluye la categoría de producto «Textiles médicos y sanitarios», pero según sus datos es solo proveedora; las obligaciones del MDR recaen en los fabricantes, representantes autorizados, importadores y distribuidores de productos sanitarios.",
        "fr": "L'entreprise indique la catégorie de produits « Textiles médicaux et de santé », mais n'est selon ses indications qu'un fournisseur ; les obligations du MDR incombent aux fabricants, mandataires, importateurs et distributeurs de dispositifs médicaux.",
        "it": "L'impresa indica la categoria di prodotto «Tessili medicali e sanitari», ma secondo quanto dichiarato è solo fornitore; gli obblighi del MDR gravano su fabbricanti, mandatari, importatori e distributori di dispositivi medici.",
        "zh": "公司列有“医疗与卫生用纺织品”产品类别，但据其提供的信息仅为供应商；MDR 规定的义务由医疗器械的制造商、授权代表、进口商和分销商承担。",
    },
    "mdr_keine": {
        "de": "Das Unternehmen führt die Produktkategorie „Medizin- und Gesundheitstextilien“ nicht; die MDR gilt nur für Produkte mit medizinischer Zweckbestimmung.",
        "en": "The company does not list the product category “Medical and healthcare textiles”; the MDR applies only to products with a medical intended purpose.",
        "es": "La empresa no incluye la categoría de producto «Textiles médicos y sanitarios»; el MDR solo se aplica a productos con una finalidad prevista médica.",
        "fr": "L'entreprise n'indique pas la catégorie de produits « Textiles médicaux et de santé » ; le MDR ne s'applique qu'aux produits ayant une destination médicale.",
        "it": "L'impresa non indica la categoria di prodotto «Tessili medicali e sanitari»; il MDR si applica solo a prodotti con una destinazione d'uso medica.",
        "zh": "公司未列有“医疗与卫生用纺织品”产品类别；MDR 仅适用于具有医疗预期用途的产品。",
    },
    "schuh_kategorie": {
        "de": "Das Unternehmen führt die Produktkategorie „Schuhe“; Schuherzeugnisse sind nach § 10a Bedarfsgegenständeverordnung vor dem gewerbsmäßigen Inverkehrbringen mit den Materialien von Obermaterial, Futter und Decksohle sowie Laufsohle zu kennzeichnen.",
        "en": "The company lists the product category “Footwear”; under Section 10a of the German Consumer Goods Ordinance (BedGgstV), footwear must be labelled with the materials of the upper, the lining and sock, and the outer sole before being placed on the market commercially.",
        "es": "La empresa incluye la categoría de producto «Calzado»; según el § 10a del Reglamento alemán de artículos de consumo (BedGgstV), los artículos de calzado deben etiquetarse, antes de su introducción comercial en el mercado, con los materiales del empeine, del forro y la plantilla y de la suela.",
        "fr": "L'entreprise indique la catégorie de produits « Chaussures » ; selon le § 10a du règlement allemand sur les objets usuels (BedGgstV), les articles chaussants doivent, avant leur mise sur le marché à titre professionnel, être étiquetés avec les matériaux de la tige, de la doublure et de la semelle de propreté ainsi que de la semelle extérieure.",
        "it": "L'impresa indica la categoria di prodotto «Calzature»; ai sensi del § 10a del regolamento tedesco sugli oggetti d'uso (BedGgstV), le calzature devono essere etichettate, prima dell'immissione sul mercato a titolo professionale, con i materiali di tomaia, fodera e sottopiede nonché suola.",
        "zh": "公司列有“鞋类”产品类别；根据德国《日用品条例》（BedGgstV）第 10a 条，鞋类产品在以商业方式投放市场前，须标明鞋面、衬里和鞋垫以及外底的材料。",
    },
    "schuh_zulieferer": {
        "de": "Das Unternehmen führt die Produktkategorie „Schuhe“, ist aber nach seinen Angaben nur Zulieferer; die Kennzeichnung schulden Hersteller, Bevollmächtigter oder Erstinverkehrbringer in der EU, Händler müssen sie bei der Abgabe sicherstellen.",
        "en": "The company lists the product category “Footwear” but, according to its information, is only a supplier; the labelling is owed by the manufacturer, its authorised representative or the person first placing the product on the market in the EU, and distributors must ensure it when supplying the product.",
        "es": "La empresa incluye la categoría de producto «Calzado», pero según sus datos es solo proveedora; el etiquetado corresponde al fabricante, a su representante autorizado o a quien introduzca el producto por primera vez en el mercado de la UE, y los distribuidores deben garantizarlo en la entrega.",
        "fr": "L'entreprise indique la catégorie de produits « Chaussures », mais n'est selon ses indications qu'un fournisseur ; l'étiquetage incombe au fabricant, à son mandataire ou à la personne qui met le produit sur le marché de l'UE pour la première fois, et les distributeurs doivent l'assurer lors de la remise.",
        "it": "L'impresa indica la categoria di prodotto «Calzature», ma secondo quanto dichiarato è solo fornitore; l'etichettatura spetta al fabbricante, al suo mandatario o a chi immette per primo il prodotto sul mercato dell'UE, e i distributori devono garantirla al momento della cessione.",
        "zh": "公司列有“鞋类”产品类别，但据其提供的信息仅为供应商；标签义务由制造商、其授权代表或在欧盟首次投放市场者承担，经销商须在交付时确保标签到位。",
    },
    "schuh_keine": {
        "de": "Das Unternehmen führt die Produktkategorie „Schuhe“ nicht; die Schuhkennzeichnung betrifft nur Schuhe.",
        "en": "The company does not list the product category “Footwear”; footwear labelling concerns only footwear.",
        "es": "La empresa no incluye la categoría de producto «Calzado»; el etiquetado del calzado solo afecta al calzado.",
        "fr": "L'entreprise n'indique pas la catégorie de produits « Chaussures » ; l'étiquetage des chaussures ne concerne que les chaussures.",
        "it": "L'impresa non indica la categoria di prodotto «Calzature»; l'etichettatura delle calzature riguarda solo le calzature.",
        "zh": "公司未列有“鞋类”产品类别；鞋类标签规定仅涉及鞋类。",
    },
    "enefg_ueber_7_5": {
        "de": "Der Gesamtendenergieverbrauch des Unternehmens in Deutschland liegt bei {energy} pro Jahr (Schwellen: mehr als 7,5 GWh für das Managementsystem, mehr als 2,5 GWh für die Umsetzungspläne).",
        "en": "The company's total final energy consumption in Germany is {energy} per year (thresholds: more than 7.5 GWh for the management system, more than 2.5 GWh for the implementation plans).",
        "es": "El consumo total de energía final de la empresa en Alemania asciende a {energy} al año (umbrales: más de 7,5 GWh para el sistema de gestión, más de 2,5 GWh para los planes de ejecución).",
        "fr": "La consommation totale d'énergie finale de l'entreprise en Allemagne s'élève à {energy} par an (seuils : plus de 7,5 GWh pour le système de management, plus de 2,5 GWh pour les plans de mise en œuvre).",
        "it": "Il consumo totale di energia finale dell'impresa in Germania è di {energy} all'anno (soglie: più di 7,5 GWh per il sistema di gestione, più di 2,5 GWh per i piani di attuazione).",
        "zh": "公司在德国的最终能源总消耗量为每年 {energy}（门槛：管理体系为超过 7.5 GWh，实施计划为超过 2.5 GWh）。",
    },
    "enefg_ueber_2_5": {
        "de": "Der Gesamtendenergieverbrauch des Unternehmens in Deutschland liegt bei {energy} pro Jahr (Schwellen: mehr als 2,5 GWh für die Umsetzungspläne, mehr als 7,5 GWh für das Managementsystem).",
        "en": "The company's total final energy consumption in Germany is {energy} per year (thresholds: more than 2.5 GWh for the implementation plans, more than 7.5 GWh for the management system).",
        "es": "El consumo total de energía final de la empresa en Alemania asciende a {energy} al año (umbrales: más de 2,5 GWh para los planes de ejecución, más de 7,5 GWh para el sistema de gestión).",
        "fr": "La consommation totale d'énergie finale de l'entreprise en Allemagne s'élève à {energy} par an (seuils : plus de 2,5 GWh pour les plans de mise en œuvre, plus de 7,5 GWh pour le système de management).",
        "it": "Il consumo totale di energia finale dell'impresa in Germania è di {energy} all'anno (soglie: più di 2,5 GWh per i piani di attuazione, più di 7,5 GWh per il sistema di gestione).",
        "zh": "公司在德国的最终能源总消耗量为每年 {energy}（门槛：实施计划为超过 2.5 GWh，管理体系为超过 7.5 GWh）。",
    },
    "enefg_unter_2_5": {
        "de": "Der Gesamtendenergieverbrauch des Unternehmens in Deutschland liegt bei {energy} pro Jahr und damit nicht über der niedrigsten Schwelle von 2,5 GWh.",
        "en": "The company's total final energy consumption in Germany is {energy} per year and thus not above the lowest threshold of 2.5 GWh.",
        "es": "El consumo total de energía final de la empresa en Alemania asciende a {energy} al año y, por tanto, no supera el umbral más bajo de 2,5 GWh.",
        "fr": "La consommation totale d'énergie finale de l'entreprise en Allemagne s'élève à {energy} par an et ne dépasse donc pas le seuil le plus bas de 2,5 GWh.",
        "it": "Il consumo totale di energia finale dell'impresa in Germania è di {energy} all'anno e quindi non supera la soglia più bassa di 2,5 GWh.",
        "zh": "公司在德国的最终能源总消耗量为每年 {energy}，因此未超过 2.5 GWh 的最低门槛。",
    },
    "enefg_ohne_angabe": {
        "de": "Das Unternehmen hat keinen Gesamtendenergieverbrauch angegeben; die Pflichten des Energieeffizienzgesetzes hängen an den Schwellen von mehr als 2,5 GWh und mehr als 7,5 GWh pro Jahr.",
        "en": "The company has not stated its total final energy consumption; the obligations of the German Energy Efficiency Act (EnEfG) depend on the thresholds of more than 2.5 GWh and more than 7.5 GWh per year.",
        "es": "La empresa no ha indicado su consumo total de energía final; las obligaciones de la Ley alemana de eficiencia energética (EnEfG) dependen de los umbrales de más de 2,5 GWh y más de 7,5 GWh al año.",
        "fr": "L'entreprise n'a pas indiqué sa consommation totale d'énergie finale ; les obligations de la loi allemande sur l'efficacité énergétique (EnEfG) dépendent des seuils de plus de 2,5 GWh et de plus de 7,5 GWh par an.",
        "it": "L'impresa non ha indicato il proprio consumo totale di energia finale; gli obblighi della legge tedesca sull'efficienza energetica (EnEfG) dipendono dalle soglie di più di 2,5 GWh e di più di 7,5 GWh all'anno.",
        "zh": "公司未填写最终能源总消耗量；德国《能源效率法》（EnEfG）规定的义务取决于每年超过 2.5 GWh 和超过 7.5 GWh 的门槛。",
    },
    "abwv_nass": {
        "de": "Das Unternehmen gibt an, dass an einem Standort in Deutschland bei der Herstellung oder Veredlung von Textilien Abwasser entsteht; für Abwasser aus der Bearbeitung und Verarbeitung von Spinnstoffen und Garnen sowie der Textilveredlung gilt Anhang 38 der Abwasserverordnung.",
        "en": "The company states that wastewater is generated at a site in Germany during the manufacture or finishing of textiles; Annex 38 of the German Wastewater Ordinance (AbwV) applies to wastewater from the treatment and processing of textile fibres and yarns and from textile finishing.",
        "es": "La empresa indica que en una planta en Alemania se generan aguas residuales durante la fabricación o el acabado de textiles; a las aguas residuales procedentes del tratamiento y la transformación de fibras textiles e hilados y del acabado textil se aplica el anexo 38 del Reglamento alemán de aguas residuales (AbwV).",
        "fr": "L'entreprise indique que des eaux usées sont produites sur un site en Allemagne lors de la fabrication ou de l'ennoblissement de textiles ; l'annexe 38 du règlement allemand sur les eaux usées (AbwV) s'applique aux eaux usées issues du traitement et de la transformation des fibres textiles et des fils ainsi que de l'ennoblissement textile.",
        "it": "L'impresa dichiara che in uno stabilimento in Germania si producono acque reflue durante la produzione o la nobilitazione di tessili; alle acque reflue derivanti dal trattamento e dalla lavorazione di fibre tessili e filati e dal finissaggio tessile si applica l'allegato 38 del regolamento tedesco sulle acque reflue (AbwV).",
        "zh": "公司表示，其在德国的某一场所在生产或整理纺织品时产生废水；纺织纤维和纱线的处理与加工以及纺织品整理所产生的废水适用德国《废水条例》（AbwV）附件 38。",
    },
    "abwv_branche_veredlung": {
        "de": "Das Unternehmen ordnet sich der Branche „Veredlung von Textilien und Bekleidung“ zu, gibt aber kein Abwasser aus Textilherstellung oder -veredlung in Deutschland an; Anhang 38 der Abwasserverordnung gilt nur für Abwasser aus solchen Prozessen.",
        "en": "The company assigns itself to the sector “Finishing of textiles and apparel” but does not state any wastewater from textile manufacturing or finishing in Germany; Annex 38 of the German Wastewater Ordinance (AbwV) applies only to wastewater from such processes.",
        "es": "La empresa se adscribe al sector «Acabado de textiles y prendas de vestir», pero no indica aguas residuales de la fabricación o el acabado textil en Alemania; el anexo 38 del Reglamento alemán de aguas residuales (AbwV) solo se aplica a las aguas residuales procedentes de dichos procesos.",
        "fr": "L'entreprise se rattache au secteur « Ennoblissement textile et de l'habillement », mais n'indique pas d'eaux usées issues de la fabrication ou de l'ennoblissement textile en Allemagne ; l'annexe 38 du règlement allemand sur les eaux usées (AbwV) ne s'applique qu'aux eaux usées issues de tels procédés.",
        "it": "L'impresa si colloca nel settore «Finissaggio di tessili e abbigliamento», ma non indica acque reflue dalla produzione o nobilitazione tessile in Germania; l'allegato 38 del regolamento tedesco sulle acque reflue (AbwV) si applica solo alle acque reflue derivanti da tali processi.",
        "zh": "公司将自身归入“纺织品和服装整理”行业，但未说明在德国的纺织品生产或整理过程中产生废水；德国《废水条例》（AbwV）附件 38 仅适用于此类工艺产生的废水。",
    },
    "abwv_keine": {
        "de": "Das Unternehmen gibt kein Abwasser aus Textilherstellung oder -veredlung an einem Standort in Deutschland an; Anhang 38 der Abwasserverordnung gilt nur für Abwasser aus der Bearbeitung und Verarbeitung von Spinnstoffen und Garnen sowie der Textilveredlung.",
        "en": "The company does not state any wastewater from textile manufacturing or finishing at a site in Germany; Annex 38 of the German Wastewater Ordinance (AbwV) applies only to wastewater from the treatment and processing of textile fibres and yarns and from textile finishing.",
        "es": "La empresa no indica aguas residuales de la fabricación o el acabado textil en ninguna planta en Alemania; el anexo 38 del Reglamento alemán de aguas residuales (AbwV) solo se aplica a las aguas residuales procedentes del tratamiento y la transformación de fibras textiles e hilados y del acabado textil.",
        "fr": "L'entreprise n'indique pas d'eaux usées issues de la fabrication ou de l'ennoblissement textile sur un site en Allemagne ; l'annexe 38 du règlement allemand sur les eaux usées (AbwV) ne s'applique qu'aux eaux usées issues du traitement et de la transformation des fibres textiles et des fils ainsi que de l'ennoblissement textile.",
        "it": "L'impresa non indica acque reflue dalla produzione o nobilitazione tessile in uno stabilimento in Germania; l'allegato 38 del regolamento tedesco sulle acque reflue (AbwV) si applica solo alle acque reflue derivanti dal trattamento e dalla lavorazione di fibre tessili e filati e dal finissaggio tessile.",
        "zh": "公司未说明在德国的场所在纺织品生产或整理过程中产生废水；德国《废水条例》（AbwV）附件 38 仅适用于纺织纤维和纱线的处理与加工以及纺织品整理所产生的废水。",
    },
    # --- Katalogerweiterung 29.09.2026 ---
    "eprfr_absatz": {
        "de": "Das Unternehmen setzt nach seinen Angaben in Frankreich ab und führt Produkte, die der französischen Herstellerverantwortung für Textilien unterliegen (Bekleidung, Schuhe, Heim- und Haustextilien für Privatpersonen).",
        "en": "According to its information, the company sells in France and carries products that are subject to French extended producer responsibility for textiles (clothing, footwear, household linen and home textiles for private individuals).",
        "es": "Según sus datos, la empresa vende en Francia y comercializa productos sujetos a la responsabilidad ampliada del productor de textiles en Francia (ropa, calzado, ropa de hogar y textiles para la casa destinados a particulares).",
        "fr": "Selon ses indications, l'entreprise vend en France et commercialise des produits relevant de la responsabilité élargie du producteur pour les textiles en France (habillement, chaussures, linge de maison et textiles pour la maison destinés aux particuliers).",
        "it": "Secondo quanto dichiarato, l'impresa vende in Francia e tratta prodotti soggetti alla responsabilità estesa del produttore per i tessili in Francia (abbigliamento, calzature, biancheria e tessili per la casa destinati a privati).",
        "zh": "据公司提供的信息，其在法国销售，且经营受法国纺织品生产者延伸责任约束的产品（面向私人消费者的服装、鞋类、家用布草及家居纺织品）。",
    },
    "eprfr_kein_absatz": {
        "de": "Das Unternehmen gibt weder Frankreich noch andere EU-/EWR-Staaten als Absatzmarkt an; die französische Herstellerverantwortung für Textilien knüpft an das Inverkehrbringen in Frankreich an.",
        "en": "The company indicates neither France nor other EU/EEA states as a sales market; French extended producer responsibility for textiles is linked to placing products on the market in France.",
        "es": "La empresa no indica como mercado de venta ni Francia ni otros Estados de la UE/EEE; la responsabilidad ampliada del productor de textiles en Francia se vincula a la introducción en el mercado en Francia.",
        "fr": "L'entreprise n'indique comme marché de vente ni la France ni d'autres États de l'UE/EEE ; la responsabilité élargie du producteur pour les textiles en France est liée à la mise sur le marché en France.",
        "it": "L'impresa non indica come mercato di vendita né la Francia né altri Stati UE/SEE; la responsabilità estesa del produttore per i tessili in Francia è legata all'immissione sul mercato in Francia.",
        "zh": "公司未将法国或其他欧盟/欧洲经济区国家列为销售市场；法国纺织品生产者延伸责任以在法国投放市场为连接点。",
    },
    "eprfr_keine_produkte": {
        "de": "Das Unternehmen führt keine der erfassten Produktgruppen (Bekleidung, Schuhe, Heim- und Haustextilien für Privatpersonen); nur für sie gilt die französische Herstellerverantwortung für Textilien.",
        "en": "The company does not carry any of the covered product groups (clothing, footwear, household linen and home textiles for private individuals); French extended producer responsibility for textiles applies only to these.",
        "es": "La empresa no comercializa ninguno de los grupos de productos cubiertos (ropa, calzado, ropa de hogar y textiles para la casa destinados a particulares); la responsabilidad ampliada del productor de textiles en Francia solo se aplica a ellos.",
        "fr": "L'entreprise ne commercialise aucun des groupes de produits visés (habillement, chaussures, linge de maison et textiles pour la maison destinés aux particuliers) ; la responsabilité élargie du producteur pour les textiles en France ne s'applique qu'à eux.",
        "it": "L'impresa non tratta nessuno dei gruppi di prodotti interessati (abbigliamento, calzature, biancheria e tessili per la casa destinati a privati); la responsabilità estesa del produttore per i tessili in Francia si applica solo a questi.",
        "zh": "公司未经营任何受涵盖的产品类别（面向私人消费者的服装、鞋类、家用布草及家居纺织品）；法国纺织品生产者延伸责任仅适用于这些产品。",
    },
    "eprfr_andere_eu": {
        "de": "Das Unternehmen gibt „andere EU-/EWR-Staaten“ als Absatzmarkt an, aber nicht ausdrücklich Frankreich; die französische Herstellerverantwortung für Textilien greift nur bei Absatz in Frankreich.",
        "en": "The company indicates “other EU/EEA states” as a sales market, but not France explicitly; French extended producer responsibility for textiles applies only to sales in France.",
        "es": "La empresa indica «otros Estados de la UE/EEE» como mercado de venta, pero no Francia de forma expresa; la responsabilidad ampliada del productor de textiles en Francia solo se aplica a las ventas en Francia.",
        "fr": "L'entreprise indique « autres États de l'UE/EEE » comme marché de vente, mais pas expressément la France ; la responsabilité élargie du producteur pour les textiles en France ne s'applique qu'en cas de vente en France.",
        "it": "L'impresa indica «altri Stati UE/SEE» come mercato di vendita, ma non espressamente la Francia; la responsabilità estesa del produttore per i tessili in Francia si applica solo in caso di vendita in Francia.",
        "zh": "公司将“其他欧盟/欧洲经济区国家”列为销售市场，但未明确列出法国；法国纺织品生产者延伸责任仅在于法国销售时适用。",
    },
    "eprfr_zulieferer": {
        "de": "Das Unternehmen setzt nach seinen Angaben in Frankreich ab, ist aber nur Zulieferer; verpflichtet ist, wer die fertigen Produkte in Frankreich in Verkehr bringt.",
        "en": "According to its information, the company sells in France but is only a supplier; the obligation lies with whoever places the finished products on the market in France.",
        "es": "Según sus datos, la empresa vende en Francia, pero es solo proveedora; la obligación recae en quien introduce los productos acabados en el mercado en Francia.",
        "fr": "Selon ses indications, l'entreprise vend en France, mais n'est qu'un fournisseur ; l'obligation incombe à celui qui met les produits finis sur le marché en France.",
        "it": "Secondo quanto dichiarato, l'impresa vende in Francia, ma è solo fornitore; l'obbligo grava su chi immette i prodotti finiti sul mercato in Francia.",
        "zh": "据公司提供的信息，其在法国销售，但仅为供应商；负有义务的是在法国将成品投放市场的一方。",
    },
    "eprfr_ohne_b2c": {
        "de": "Das Unternehmen setzt nach seinen Angaben in Frankreich ab, gibt aber kein Endkundengeschäft an; erfasst sind nur Produkte für Privatpersonen.",
        "en": "According to its information, the company sells in France but does not indicate any business with end customers; only products for private individuals are covered.",
        "es": "Según sus datos, la empresa vende en Francia, pero no indica actividad con clientes finales; solo están cubiertos los productos destinados a particulares.",
        "fr": "Selon ses indications, l'entreprise vend en France, mais n'indique aucune activité auprès de clients finaux ; seuls les produits destinés aux particuliers sont visés.",
        "it": "Secondo quanto dichiarato, l'impresa vende in Francia, ma non indica alcuna attività con clienti finali; sono interessati solo i prodotti destinati a privati.",
        "zh": "据公司提供的信息，其在法国销售，但未填写面向终端客户的业务；受涵盖的仅为面向私人消费者的产品。",
    },
    "eprnl_absatz": {
        "de": "Das Unternehmen setzt nach seinen Angaben in den Niederlanden ab und führt Produkte, die der niederländischen Herstellerverantwortung für Textilien unterliegen (Kleidung einschließlich Berufskleidung sowie Haushaltstextilien).",
        "en": "According to its information, the company sells in the Netherlands and carries products that are subject to Dutch extended producer responsibility for textiles (clothing including workwear, and household textiles).",
        "es": "Según sus datos, la empresa vende en los Países Bajos y comercializa productos sujetos a la responsabilidad ampliada del productor de textiles en los Países Bajos (ropa, incluida la ropa de trabajo, y textiles para el hogar).",
        "fr": "Selon ses indications, l'entreprise vend aux Pays-Bas et commercialise des produits relevant de la responsabilité élargie du producteur pour les textiles aux Pays-Bas (vêtements, y compris vêtements de travail, ainsi que textiles de maison).",
        "it": "Secondo quanto dichiarato, l'impresa vende nei Paesi Bassi e tratta prodotti soggetti alla responsabilità estesa del produttore per i tessili nei Paesi Bassi (abbigliamento, compreso quello da lavoro, e tessili per la casa).",
        "zh": "据公司提供的信息，其在荷兰销售，且经营受荷兰纺织品生产者延伸责任约束的产品（服装，包括工作服，以及家用纺织品）。",
    },
    "eprnl_kein_absatz": {
        "de": "Das Unternehmen gibt weder die Niederlande noch andere EU-/EWR-Staaten als Absatzmarkt an; die niederländische Herstellerverantwortung für Textilien knüpft an das Inverkehrbringen in den Niederlanden an.",
        "en": "The company indicates neither the Netherlands nor other EU/EEA states as a sales market; Dutch extended producer responsibility for textiles is linked to placing products on the market in the Netherlands.",
        "es": "La empresa no indica como mercado de venta ni los Países Bajos ni otros Estados de la UE/EEE; la responsabilidad ampliada del productor de textiles en los Países Bajos se vincula a la introducción en el mercado en los Países Bajos.",
        "fr": "L'entreprise n'indique comme marché de vente ni les Pays-Bas ni d'autres États de l'UE/EEE ; la responsabilité élargie du producteur pour les textiles aux Pays-Bas est liée à la mise sur le marché aux Pays-Bas.",
        "it": "L'impresa non indica come mercato di vendita né i Paesi Bassi né altri Stati UE/SEE; la responsabilità estesa del produttore per i tessili nei Paesi Bassi è legata all'immissione sul mercato nei Paesi Bassi.",
        "zh": "公司未将荷兰或其他欧盟/欧洲经济区国家列为销售市场；荷兰纺织品生产者延伸责任以在荷兰投放市场为连接点。",
    },
    "eprnl_keine_produkte": {
        "de": "Das Unternehmen führt keine der erfassten Produktgruppen (Kleidung einschließlich Berufskleidung, Haushaltstextilien); Schuhe sind in den Niederlanden derzeit nicht erfasst.",
        "en": "The company does not carry any of the covered product groups (clothing including workwear, household textiles); footwear is currently not covered in the Netherlands.",
        "es": "La empresa no comercializa ninguno de los grupos de productos cubiertos (ropa, incluida la ropa de trabajo, textiles para el hogar); el calzado no está cubierto actualmente en los Países Bajos.",
        "fr": "L'entreprise ne commercialise aucun des groupes de produits visés (vêtements, y compris vêtements de travail, textiles de maison) ; les chaussures ne sont actuellement pas visées aux Pays-Bas.",
        "it": "L'impresa non tratta nessuno dei gruppi di prodotti interessati (abbigliamento, compreso quello da lavoro, tessili per la casa); le calzature non sono attualmente interessate nei Paesi Bassi.",
        "zh": "公司未经营任何受涵盖的产品类别（服装，包括工作服；家用纺织品）；鞋类目前在荷兰不受涵盖。",
    },
    "eprnl_andere_eu": {
        "de": "Das Unternehmen gibt „andere EU-/EWR-Staaten“ als Absatzmarkt an, aber nicht ausdrücklich die Niederlande; die niederländische Herstellerverantwortung für Textilien greift nur bei Absatz in den Niederlanden.",
        "en": "The company indicates “other EU/EEA states” as a sales market, but not the Netherlands explicitly; Dutch extended producer responsibility for textiles applies only to sales in the Netherlands.",
        "es": "La empresa indica «otros Estados de la UE/EEE» como mercado de venta, pero no los Países Bajos de forma expresa; la responsabilidad ampliada del productor de textiles en los Países Bajos solo se aplica a las ventas en los Países Bajos.",
        "fr": "L'entreprise indique « autres États de l'UE/EEE » comme marché de vente, mais pas expressément les Pays-Bas ; la responsabilité élargie du producteur pour les textiles aux Pays-Bas ne s'applique qu'en cas de vente aux Pays-Bas.",
        "it": "L'impresa indica «altri Stati UE/SEE» come mercato di vendita, ma non espressamente i Paesi Bassi; la responsabilità estesa del produttore per i tessili nei Paesi Bassi si applica solo in caso di vendita nei Paesi Bassi.",
        "zh": "公司将“其他欧盟/欧洲经济区国家”列为销售市场，但未明确列出荷兰；荷兰纺织品生产者延伸责任仅在于荷兰销售时适用。",
    },
    "eprnl_zulieferer": {
        "de": "Das Unternehmen setzt nach seinen Angaben in den Niederlanden ab, ist aber nur Zulieferer; verpflichtet ist, wer die fertigen Textilprodukte dort in Verkehr bringt.",
        "en": "According to its information, the company sells in the Netherlands but is only a supplier; the obligation lies with whoever places the finished textile products on the market there.",
        "es": "Según sus datos, la empresa vende en los Países Bajos, pero es solo proveedora; la obligación recae en quien introduce allí en el mercado los productos textiles acabados.",
        "fr": "Selon ses indications, l'entreprise vend aux Pays-Bas, mais n'est qu'un fournisseur ; l'obligation incombe à celui qui y met sur le marché les produits textiles finis.",
        "it": "Secondo quanto dichiarato, l'impresa vende nei Paesi Bassi, ma è solo fornitore; l'obbligo grava su chi vi immette sul mercato i prodotti tessili finiti.",
        "zh": "据公司提供的信息，其在荷兰销售，但仅为供应商；负有义务的是在当地将纺织成品投放市场的一方。",
    },
}

COUPLING_CONCLUSIONS: dict[str, dict[str, dict[str, str]]] = {
    "CSR-RUG": {
        "ja": {
            "de": "Die nichtfinanzielle Erklärung nach § 289b HGB ist damit im Lagebericht abzugeben; "
                  "mit der CSRD-Umsetzung tritt die Nachhaltigkeitsberichterstattung an ihre Stelle.",
            "en": "The non-financial statement under section 289b HGB therefore has to be included in "
                  "the management report; sustainability reporting will replace it once the CSRD is "
                  "transposed.",
            "es": "Por tanto, el estado no financiero del § 289b HGB debe incluirse en el informe de "
                  "gestión; con la transposición de la CSRD lo sustituirá la información de "
                  "sostenibilidad.",
            "fr": "La déclaration non financière du § 289b HGB doit donc figurer dans le rapport de "
                  "gestion ; avec la transposition de la CSRD, le reporting de durabilité la "
                  "remplacera.",
            "it": "La dichiarazione non finanziaria del § 289b HGB va quindi inserita nella relazione "
                  "sulla gestione; con il recepimento della CSRD sarà sostituita dalla rendicontazione "
                  "di sostenibilità.",
            "zh": "因此须在管理报告中作出《商法典》第 289b 条规定的非财务声明；随着 CSRD 的转化，可持续发展报告将取而代之。",
        },
        "nein": {
            "de": "Eine Pflicht zur nichtfinanziellen Erklärung nach § 289b HGB besteht damit nicht.",
            "en": "There is therefore no duty to provide a non-financial statement under section 289b "
                  "HGB.",
            "es": "Por tanto, no existe obligación de presentar un estado no financiero conforme al "
                  "§ 289b HGB.",
            "fr": "Il n'existe donc pas d'obligation de déclaration non financière au titre du § 289b "
                  "HGB.",
            "it": "Non sussiste quindi alcun obbligo di dichiarazione non finanziaria ai sensi del "
                  "§ 289b HGB.",
            "zh": "因此不负有《商法典》第 289b 条规定的非财务声明义务。",
        },
        "moeglich": {
            "de": "Die Pflicht zur nichtfinanziellen Erklärung nach § 289b HGB ist deshalb im "
                  "Einzelfall zu prüfen.",
            "en": "The duty to provide a non-financial statement under section 289b HGB therefore has "
                  "to be assessed case by case.",
            "es": "Por ello, la obligación de estado no financiero conforme al § 289b HGB debe "
                  "examinarse caso por caso.",
            "fr": "L'obligation de déclaration non financière au titre du § 289b HGB doit donc être "
                  "examinée au cas par cas.",
            "it": "L'obbligo di dichiarazione non finanziaria ai sensi del § 289b HGB va quindi "
                  "verificato caso per caso.",
            "zh": "因此需就个案审查《商法典》第 289b 条规定的非财务声明义务。",
        },
    },
    "CSRD": {
        "ja": {
            "de": "Es besteht damit eine Berichtspflicht nach der CSRD; die neuen Schwellen gelten "
                  "für Geschäftsjahre ab dem 01.01.2027.",
            "en": "A reporting duty under the CSRD therefore applies; the new thresholds apply to "
                  "financial years starting on or after 01.01.2027.",
            "es": "Existe por tanto una obligación de informar conforme a la CSRD; los nuevos "
                  "umbrales se aplican a ejercicios que comiencen a partir del 01.01.2027.",
            "fr": "Une obligation de déclaration au titre de la CSRD s'applique donc ; les nouveaux "
                  "seuils valent pour les exercices ouverts à compter du 01.01.2027.",
            "it": "Sussiste quindi un obbligo di rendicontazione ai sensi della CSRD; le nuove "
                  "soglie valgono per gli esercizi che iniziano dal 01.01.2027.",
            "zh": "因此负有 CSRD 报告义务；新门槛适用于 2027 年 1 月 1 日或之后开始的财政年度。",
        },
        "nein": {
            "de": "Eine Berichtspflicht nach der CSRD besteht damit nicht.",
            "en": "There is therefore no reporting duty under the CSRD.",
            "es": "Por tanto, no existe obligación de informar conforme a la CSRD.",
            "fr": "Il n'existe donc pas d'obligation de déclaration au titre de la CSRD.",
            "it": "Non sussiste quindi alcun obbligo di rendicontazione ai sensi della CSRD.",
            "zh": "因此不负有 CSRD 报告义务。",
        },
        "moeglich": {
            "de": "Die CSRD-Berichtspflicht ist deshalb im Einzelfall zu prüfen.",
            "en": "The CSRD reporting duty therefore has to be assessed case by case.",
            "es": "Por ello, la obligación de informar conforme a la CSRD debe examinarse caso por caso.",
            "fr": "L'obligation de déclaration CSRD doit donc être examinée au cas par cas.",
            "it": "L'obbligo di rendicontazione CSRD va quindi verificato caso per caso.",
            "zh": "因此需就个案审查 CSRD 报告义务。",
        },
    },
    "CSRD_DE": {
        "ja": {
            "de": "Das CSRD-Umsetzungsgesetz überträgt diese Pflicht in den Lagebericht nach "
                  "§§ 289b ff. HGB-E.",
            "en": "The German CSRD implementation act carries this duty into the management report "
                  "under sections 289b et seq. HGB (draft).",
            "es": "La ley alemana de transposición de la CSRD traslada esta obligación al informe "
                  "de gestión conforme a los §§ 289b y ss. HGB (proyecto).",
            "fr": "La loi allemande de transposition de la CSRD reporte cette obligation dans le "
                  "rapport de gestion selon les §§ 289b et suivants HGB (projet).",
            "it": "La legge tedesca di recepimento della CSRD trasferisce questo obbligo nella "
                  "relazione sulla gestione ai sensi dei §§ 289b ss. HGB (progetto).",
            "zh": "德国 CSRD 转化法将该义务纳入《商法典》第 289b 条及以下（草案）规定的管理报告。",
        },
        "nein": {
            "de": "Damit greifen auch die §§ 289b ff. HGB in der Fassung des Umsetzungsgesetzes nicht.",
            "en": "Consequently sections 289b et seq. HGB as amended by the implementation act do "
                  "not apply either.",
            "es": "En consecuencia, tampoco se aplican los §§ 289b y ss. HGB en la redacción de la "
                  "ley de transposición.",
            "fr": "Par conséquent, les §§ 289b et suivants HGB dans la version de la loi de "
                  "transposition ne s'appliquent pas non plus.",
            "it": "Di conseguenza non si applicano nemmeno i §§ 289b ss. HGB nella versione della "
                  "legge di recepimento.",
            "zh": "因此，转化法版本的《商法典》第 289b 条及以下亦不适用。",
        },
        "moeglich": {
            "de": "Ob die §§ 289b ff. HGB-E greifen, folgt der noch zu klärenden CSRD-Pflicht.",
            "en": "Whether sections 289b et seq. HGB (draft) apply follows the CSRD duty that still "
                  "has to be clarified.",
            "es": "Que se apliquen los §§ 289b y ss. HGB (proyecto) depende de la obligación CSRD "
                  "aún por aclarar.",
            "fr": "L'application des §§ 289b et suivants HGB (projet) suit l'obligation CSRD encore "
                  "à clarifier.",
            "it": "L'applicazione dei §§ 289b ss. HGB (progetto) segue l'obbligo CSRD ancora da "
                  "chiarire.",
            "zh": "《商法典》第 289b 条及以下（草案）是否适用，取决于尚待厘清的 CSRD 义务。",
        },
    },
    "TaxonomieVO": {
        "ja": {
            "de": "Damit greift auch die Taxonomie-Offenlegung nach Art. 8 (Anteile an Umsatz, "
                  "CapEx und OpEx).",
            "en": "The taxonomy disclosure under Art. 8 (shares of turnover, CapEx and OpEx) "
                  "therefore applies as well.",
            "es": "Por tanto, también se aplica la divulgación de taxonomía del art. 8 (porcentajes "
                  "de volumen de negocios, CapEx y OpEx).",
            "fr": "La publication taxonomique de l'art. 8 (part du chiffre d'affaires, des CapEx et "
                  "des OpEx) s'applique donc également.",
            "it": "Si applica quindi anche l'informativa sulla tassonomia dell'art. 8 (quote di "
                  "fatturato, CapEx e OpEx).",
            "zh": "因此还须履行第 8 条的分类法披露义务（营业额、资本支出和运营支出占比）。",
        },
        "nein": {
            "de": "Ohne CSRD-Pflicht besteht keine Offenlegungspflicht nach Art. 8.",
            "en": "Without a CSRD duty there is no disclosure obligation under Art. 8.",
            "es": "Sin obligación CSRD no existe obligación de divulgación conforme al art. 8.",
            "fr": "En l'absence d'obligation CSRD, aucune publication au titre de l'art. 8 n'est due.",
            "it": "In assenza di obbligo CSRD non sussiste alcun obbligo informativo ex art. 8.",
            "zh": "无 CSRD 义务时，不产生第 8 条的披露义务。",
        },
        "moeglich": {
            "de": "Ob nach Art. 8 offenzulegen ist, folgt der noch zu klärenden CSRD-Pflicht.",
            "en": "Whether disclosure under Art. 8 is required follows the CSRD duty that still has "
                  "to be clarified.",
            "es": "Que haya que divulgar conforme al art. 8 depende de la obligación CSRD aún por "
                  "aclarar.",
            "fr": "L'obligation de publier au titre de l'art. 8 suit l'obligation CSRD encore à "
                  "clarifier.",
            "it": "L'obbligo di informativa ex art. 8 segue l'obbligo CSRD ancora da chiarire.",
            "zh": "是否须按第 8 条披露，取决于尚待厘清的 CSRD 义务。",
        },
        "finanzmarkt": {
            "de": "Die Branche gehört jedoch zum Finanzsektor, den Art. 8 unabhängig von der "
                  "CSRD-Schwelle erfasst — das ist gesondert zu prüfen.",
            "en": "The sector is part of the financial industry, however, which Art. 8 covers "
                  "independently of the CSRD threshold — this has to be checked separately.",
            "es": "No obstante, el sector pertenece al ámbito financiero, que el art. 8 cubre con "
                  "independencia del umbral CSRD; esto debe examinarse por separado.",
            "fr": "Le secteur relève toutefois de la finance, que l'art. 8 couvre indépendamment du "
                  "seuil CSRD — ce point doit être vérifié séparément.",
            "it": "Il settore rientra però nella finanza, che l'art. 8 copre indipendentemente "
                  "dalla soglia CSRD: va verificato separatamente.",
            "zh": "但该行业属于金融领域，第 8 条对其的适用不受 CSRD 门槛限制，需另行审查。",
        },
    },
    "HinSchG": {
        "ja": {
            "de": "Eine interne Meldestelle nach § 12 HinSchG ist damit einzurichten.",
            "en": "An internal reporting channel under section 12 HinSchG therefore has to be set up.",
            "es": "Debe establecerse por tanto un canal interno de denuncias conforme al § 12 HinSchG.",
            "fr": "Un canal de signalement interne au sens du § 12 HinSchG doit donc être mis en place.",
            "it": "Va quindi istituito un canale di segnalazione interno ai sensi del § 12 HinSchG.",
            "zh": "因此必须依《举报人保护法》第 12 条设立内部举报机构。",
        },
        "nein": {
            "de": "Eine interne Meldestelle nach § 12 HinSchG ist damit nicht verpflichtend.",
            "en": "An internal reporting channel under section 12 HinSchG is therefore not mandatory.",
            "es": "Por tanto, no es obligatorio un canal interno de denuncias conforme al § 12 HinSchG.",
            "fr": "Un canal de signalement interne au sens du § 12 HinSchG n'est donc pas obligatoire.",
            "it": "Un canale di segnalazione interno ai sensi del § 12 HinSchG non è quindi obbligatorio.",
            "zh": "因此无须依《举报人保护法》第 12 条设立内部举报机构。",
        },
        "moeglich": {
            "de": "Ob eine interne Meldestelle einzurichten ist, hängt davon ab, ob das Unternehmen "
                  "zu den in § 12 Abs. 3 HinSchG aufgezählten Finanzunternehmen zählt.",
            "en": "Whether an internal reporting office is required depends on whether the company "
                  "is one of the financial undertakings listed in section 12(3) HinSchG.",
            "es": "Que deba crearse un canal interno de denuncias depende de si la empresa figura "
                  "entre las entidades financieras enumeradas en el § 12, apdo. 3, HinSchG.",
            "fr": "L'obligation de mettre en place un service de signalement interne dépend de la "
                  "question de savoir si l'entreprise fait partie des entreprises financières "
                  "énumérées au § 12, al. 3, HinSchG.",
            "it": "L'obbligo di istituire un ufficio di segnalazione interno dipende dal fatto che "
                  "l'impresa rientri tra i soggetti finanziari elencati nel § 12, comma 3, HinSchG.",
            "zh": "是否须设立内部举报机构，取决于公司是否属于《举报人保护法》第 12 条第 3 款所列的金融企业。",
        },
    },
    # --- Katalogerweiterung 29.09.2026 ---
    "REACH_ART33": {
        "ja": {
            "de": "Abnehmer müssen deshalb mindestens den Namen des Stoffes und die für eine sichere Verwendung nötigen Informationen erhalten, Verbraucher auf Anfrage binnen 45 Tagen kostenlos.",
            "en": "Recipients must therefore receive at least the name of the substance and the information needed for safe use, consumers on request within 45 days free of charge.",
            "es": "Por tanto, los destinatarios deben recibir como mínimo el nombre de la sustancia y la información necesaria para un uso seguro, y los consumidores, previa solicitud, en un plazo de 45 días y de forma gratuita.",
            "fr": "Les destinataires doivent donc recevoir au minimum le nom de la substance et les informations nécessaires à une utilisation sûre, les consommateurs sur demande, dans un délai de 45 jours et gratuitement.",
            "it": "I destinatari devono quindi ricevere almeno il nome della sostanza e le informazioni necessarie per un uso sicuro, i consumatori su richiesta entro 45 giorni e gratuitamente.",
            "zh": "因此，接收者必须至少获得该物质的名称以及安全使用所需的信息，消费者提出要求的，须在 45 天内免费获得。",
        },
        "nein": {
            "de": "Eine Informationspflicht nach Art. 33 REACH entsteht damit nicht; sie lebt aber auf, sobald die Kandidatenliste um einen enthaltenen Stoff erweitert wird.",
            "en": "No duty to communicate information under Art. 33 REACH therefore arises; however, it arises as soon as a contained substance is added to the Candidate List.",
            "es": "Por tanto, no surge ninguna obligación de información conforme al art. 33 REACH; no obstante, esta nace en cuanto se añada a la Lista de candidatas una sustancia contenida.",
            "fr": "Aucune obligation d'information au titre de l'art. 33 REACH ne naît donc ; elle apparaît toutefois dès qu'une substance contenue est ajoutée à la liste des substances candidates.",
            "it": "Non sorge quindi alcun obbligo di informazione ai sensi dell'art. 33 REACH; esso sorge tuttavia non appena una sostanza contenuta viene aggiunta all'elenco di sostanze candidate.",
            "zh": "因此不产生 REACH 第 33 条规定的信息传递义务；但一旦所含物质被列入候选清单，该义务即产生。",
        },
        "moeglich": {
            "de": "Ob die Informationspflicht nach Art. 33 REACH besteht, ist deshalb über eine Abfrage bei den Lieferanten zu klären; maßgeblich ist jedes einzelne Bauteil.",
            "en": "Whether the duty to communicate information under Art. 33 REACH applies must therefore be clarified by querying suppliers; each individual component is decisive.",
            "es": "Por ello, si existe la obligación de información conforme al art. 33 REACH debe aclararse mediante una consulta a los proveedores; es determinante cada componente por separado.",
            "fr": "L'existence de l'obligation d'information au titre de l'art. 33 REACH doit donc être clarifiée par une consultation des fournisseurs ; chaque composant pris isolément est déterminant.",
            "it": "Se sussista l'obbligo di informazione ai sensi dell'art. 33 REACH va quindi chiarito con una richiesta ai fornitori; è determinante ogni singolo componente.",
            "zh": "因此，是否存在 REACH 第 33 条规定的信息传递义务，须通过向供应商询问来确认；每个组成部分均单独起决定作用。",
        },
    },
    "SCIP": {
        "ja": {
            "de": "Die Erzeugnisse sind deshalb unverzüglich nach dem Inverkehrbringen in der SCIP-Datenbank der ECHA zu melden (§ 16f ChemG).",
            "en": "The articles must therefore be notified to ECHA's SCIP database without delay after being placed on the market (Section 16f of the German Chemicals Act, ChemG).",
            "es": "Por tanto, los artículos deben notificarse en la base de datos SCIP de la ECHA sin demora tras su introducción en el mercado (§ 16f de la Ley alemana de sustancias químicas, ChemG).",
            "fr": "Les articles doivent donc être déclarés dans la base de données SCIP de l'ECHA sans délai après leur mise sur le marché (§ 16f de la loi allemande sur les produits chimiques, ChemG).",
            "it": "Gli articoli devono quindi essere notificati nella banca dati SCIP dell'ECHA senza indugio dopo l'immissione sul mercato (§ 16f della legge tedesca sulle sostanze chimiche, ChemG).",
            "zh": "因此，物品投放市场后须立即向 ECHA 的 SCIP 数据库申报（德国《化学品法》第 16f 条，ChemG）。",
        },
        "haendler_b2c": {
            "de": "Ob gemeldet werden muss, hängt deshalb davon ab, ob ausschließlich an Verbraucher abgegeben wird; Händler mit gewerblichen Abnehmern sind meldepflichtig.",
            "en": "Whether a notification is required therefore depends on whether supplies go exclusively to consumers; distributors with business customers are required to notify.",
            "es": "Por ello, la obligación de notificar depende de si se suministra exclusivamente a consumidores; los distribuidores con clientes profesionales están obligados a notificar.",
            "fr": "L'obligation de déclaration dépend donc de la question de savoir si la remise se fait exclusivement à des consommateurs ; les distributeurs ayant des clients professionnels sont tenus de déclarer.",
            "it": "L'obbligo di notifica dipende quindi dal fatto che la cessione avvenga esclusivamente a consumatori; i distributori con clienti professionali sono soggetti all'obbligo di notifica.",
            "zh": "因此，是否须申报取决于是否仅向消费者供货；拥有商业客户的经销商负有申报义务。",
        },
        "nein": {
            "de": "Eine SCIP-Meldung ist damit nicht erforderlich; sie wird fällig, sobald ein enthaltener Stoff auf die Kandidatenliste kommt.",
            "en": "A SCIP notification is therefore not required; it becomes due as soon as a contained substance is added to the Candidate List.",
            "es": "Por tanto, no es necesaria una notificación SCIP; será exigible en cuanto una sustancia contenida se incluya en la Lista de candidatas.",
            "fr": "Une déclaration SCIP n'est donc pas requise ; elle devient exigible dès qu'une substance contenue est inscrite sur la liste des substances candidates.",
            "it": "Una notifica SCIP non è quindi necessaria; diventa dovuta non appena una sostanza contenuta viene inserita nell'elenco di sostanze candidate.",
            "zh": "因此无需进行 SCIP 申报；一旦所含物质被列入候选清单，即须申报。",
        },
        "moeglich": {
            "de": "Ob eine SCIP-Meldung erforderlich ist, ist deshalb über eine Abfrage bei den Lieferanten zu klären.",
            "en": "Whether a SCIP notification is required must therefore be clarified by querying suppliers.",
            "es": "Por ello, si es necesaria una notificación SCIP debe aclararse mediante una consulta a los proveedores.",
            "fr": "La nécessité d'une déclaration SCIP doit donc être clarifiée par une consultation des fournisseurs.",
            "it": "Se sia necessaria una notifica SCIP va quindi chiarito con una richiesta ai fornitori.",
            "zh": "因此，是否需要进行 SCIP 申报，须通过向供应商询问来确认。",
        },
    },
    "BPR": {
        "ja": {
            "de": "Die Waren dürfen deshalb nur mit genehmigten Wirkstoffen behandelt sein und müssen gekennzeichnet werden, sobald mit einer bioziden Eigenschaft geworben wird (Art. 58 Biozid-Verordnung).",
            "en": "The articles may therefore only be treated with approved active substances and must be labelled as soon as a biocidal property is claimed (Art. 58 of the Biocidal Products Regulation).",
            "es": "Por tanto, los artículos solo pueden estar tratados con sustancias activas aprobadas y deben etiquetarse en cuanto se alegue una propiedad biocida (art. 58 del Reglamento de biocidas).",
            "fr": "Les articles ne peuvent donc être traités qu'avec des substances actives approuvées et doivent être étiquetés dès qu'une propriété biocide est revendiquée (art. 58 du règlement sur les produits biocides).",
            "it": "Gli articoli possono quindi essere trattati solo con principi attivi approvati e devono essere etichettati non appena si dichiara una proprietà biocida (art. 58 del regolamento sui biocidi).",
            "zh": "因此，这些物品只能使用已获批准的活性物质进行处理，一旦宣称具有杀生物特性即须加贴标签（《生物杀灭剂法规》第 58 条）。",
        },
        "nein": {
            "de": "Die Pflichten für behandelte Waren nach Art. 58 der Biozid-Verordnung greifen damit nicht.",
            "en": "The obligations for treated articles under Art. 58 of the Biocidal Products Regulation therefore do not apply.",
            "es": "Por tanto, no se aplican las obligaciones para artículos tratados del art. 58 del Reglamento de biocidas.",
            "fr": "Les obligations relatives aux articles traités prévues à l'art. 58 du règlement sur les produits biocides ne s'appliquent donc pas.",
            "it": "Gli obblighi per gli articoli trattati di cui all'art. 58 del regolamento sui biocidi non si applicano quindi.",
            "zh": "因此，《生物杀灭剂法规》第 58 条关于经处理物品的义务不适用。",
        },
        "moeglich": {
            "de": "Ob die Pflichten für behandelte Waren greifen, ist deshalb anhand der Rezepturen der Ausrüstung zu klären.",
            "en": "Whether the obligations for treated articles apply must therefore be clarified on the basis of the finishing formulations.",
            "es": "Por ello, si se aplican las obligaciones para artículos tratados debe aclararse a partir de las formulaciones del acabado.",
            "fr": "L'applicabilité des obligations relatives aux articles traités doit donc être clarifiée à partir des formulations des apprêts.",
            "it": "Se si applichino gli obblighi per gli articoli trattati va quindi chiarito sulla base delle formulazioni del finissaggio.",
            "zh": "因此，是否适用经处理物品的相关义务，须根据整理剂配方加以确认。",
        },
    },
    "PSA": {
        "ja": {
            "de": "Die Schutzausrüstung braucht deshalb vor dem Inverkehrbringen eine Konformitätsbewertung, eine EU-Konformitätserklärung und die CE-Kennzeichnung.",
            "en": "Before being placed on the market, the protective equipment therefore requires a conformity assessment, an EU declaration of conformity and the CE marking.",
            "es": "Por tanto, antes de su introducción en el mercado el equipo de protección requiere una evaluación de la conformidad, una declaración UE de conformidad y el marcado CE.",
            "fr": "Avant sa mise sur le marché, l'équipement de protection nécessite donc une évaluation de la conformité, une déclaration UE de conformité et le marquage CE.",
            "it": "Prima dell'immissione sul mercato il dispositivo di protezione richiede quindi una valutazione della conformità, una dichiarazione di conformità UE e la marcatura CE.",
            "zh": "因此，防护装备在投放市场前须经过合格评定，并具备欧盟符合性声明和 CE 标志。",
        },
        "nein": {
            "de": "Die PSA-Verordnung ist für das Unternehmen damit nicht einschlägig.",
            "en": "The PPE Regulation therefore does not apply to the company.",
            "es": "Por tanto, el Reglamento de EPI no es aplicable a la empresa.",
            "fr": "Le règlement EPI ne s'applique donc pas à l'entreprise.",
            "it": "Il regolamento DPI non è quindi applicabile all'impresa.",
            "zh": "因此，《个人防护装备法规》不适用于该公司。",
        },
        "moeglich": {
            "de": "Ob Pflichten aus der PSA-Verordnung bestehen, hängt deshalb von der eigenen Rolle beim Inverkehrbringen ab und ist im Einzelfall zu prüfen.",
            "en": "Whether obligations under the PPE Regulation exist therefore depends on the company's own role in placing the product on the market and has to be assessed case by case.",
            "es": "Por ello, la existencia de obligaciones derivadas del Reglamento de EPI depende del papel propio en la introducción en el mercado y debe examinarse caso por caso.",
            "fr": "L'existence d'obligations au titre du règlement EPI dépend donc du rôle propre de l'entreprise dans la mise sur le marché et doit être examinée au cas par cas.",
            "it": "La sussistenza di obblighi derivanti dal regolamento DPI dipende quindi dal proprio ruolo nell'immissione sul mercato e va valutata caso per caso.",
            "zh": "因此，是否负有《个人防护装备法规》规定的义务，取决于公司在投放市场中的自身角色，须个案审查。",
        },
    },
    "MDR": {
        "nein": {
            "de": "Die Medizinprodukte-Verordnung ist für das Unternehmen damit nicht einschlägig.",
            "en": "The Medical Device Regulation therefore does not apply to the company.",
            "es": "Por tanto, el Reglamento sobre productos sanitarios no es aplicable a la empresa.",
            "fr": "Le règlement relatif aux dispositifs médicaux ne s'applique donc pas à l'entreprise.",
            "it": "Il regolamento sui dispositivi medici non è quindi applicabile all'impresa.",
            "zh": "因此，《医疗器械法规》不适用于该公司。",
        },
        "moeglich": {
            "de": "Ob die Medizinprodukte-Verordnung greift, ist deshalb anhand der Zweckbestimmung jedes einzelnen Produkts zu prüfen, etwa bei Kompressionsstrümpfen, Bandagen oder OP-Textilien.",
            "en": "Whether the Medical Device Regulation applies must therefore be assessed on the basis of the intended purpose of each individual product, for example for compression stockings, supports or surgical textiles.",
            "es": "Por ello, si se aplica el Reglamento sobre productos sanitarios debe examinarse a partir de la finalidad prevista de cada producto, por ejemplo en medias de compresión, vendajes o textiles quirúrgicos.",
            "fr": "L'applicabilité du règlement relatif aux dispositifs médicaux doit donc être examinée au regard de la destination de chaque produit, par exemple pour les bas de compression, les bandages ou les textiles chirurgicaux.",
            "it": "Se si applichi il regolamento sui dispositivi medici va quindi valutato in base alla destinazione d'uso di ogni singolo prodotto, ad esempio per calze a compressione, bendaggi o tessili chirurgici.",
            "zh": "因此，是否适用《医疗器械法规》，须根据每件产品的预期用途进行审查，例如压力袜、护具或手术用纺织品。",
        },
    },
    "Schuhkennzeichnung": {
        "ja": {
            "de": "Jedes Paar ist deshalb vor dem Inverkehrbringen lesbar und haltbar mit Piktogrammen oder Text zu den Materialien zu kennzeichnen; Sicherheitsschuhe als Schutzausrüstung, gebrauchte Schuhe und Spielzeugschuhe sind ausgenommen.",
            "en": "Before being placed on the market, each pair must therefore be labelled legibly and durably with pictograms or text on the materials; safety footwear covered as protective equipment, used footwear and toy footwear are exempt.",
            "es": "Por tanto, antes de su introducción en el mercado cada par debe etiquetarse de forma legible y duradera con pictogramas o texto sobre los materiales; están exentos el calzado de seguridad como equipo de protección, el calzado usado y el calzado de juguete.",
            "fr": "Avant la mise sur le marché, chaque paire doit donc être étiquetée de manière lisible et durable par des pictogrammes ou un texte indiquant les matériaux ; les chaussures de sécurité relevant des équipements de protection, les chaussures usagées et les chaussures jouets en sont exemptées.",
            "it": "Prima dell'immissione sul mercato ogni paio va quindi etichettato in modo leggibile e durevole con pittogrammi o testo relativi ai materiali; sono escluse le calzature di sicurezza in quanto dispositivi di protezione, le calzature usate e le calzature giocattolo.",
            "zh": "因此，每双鞋在投放市场前须以清晰、持久的方式用图形符号或文字标明材料；作为防护装备的安全鞋、旧鞋和玩具鞋除外。",
        },
        "nein": {
            "de": "Die Schuhkennzeichnung ist für das Unternehmen damit nicht einschlägig.",
            "en": "Footwear labelling therefore does not apply to the company.",
            "es": "Por tanto, el etiquetado del calzado no es aplicable a la empresa.",
            "fr": "L'étiquetage des chaussures ne s'applique donc pas à l'entreprise.",
            "it": "L'etichettatura delle calzature non è quindi applicabile all'impresa.",
            "zh": "因此，鞋类标签规定不适用于该公司。",
        },
        "moeglich": {
            "de": "Ob eine Kennzeichnungspflicht besteht, hängt deshalb davon ab, wer die Schuhe in den Verkehr bringt, und ist im Einzelfall zu prüfen.",
            "en": "Whether a labelling obligation exists therefore depends on who places the footwear on the market and has to be assessed case by case.",
            "es": "Por ello, la existencia de una obligación de etiquetado depende de quién introduce el calzado en el mercado y debe examinarse caso por caso.",
            "fr": "L'existence d'une obligation d'étiquetage dépend donc de la personne qui met les chaussures sur le marché et doit être examinée au cas par cas.",
            "it": "La sussistenza di un obbligo di etichettatura dipende quindi da chi immette le calzature sul mercato e va valutata caso per caso.",
            "zh": "因此，是否负有标签义务取决于由谁将鞋投放市场，须个案审查。",
        },
    },
    "EnEfG": {
        "ja_management": {
            "de": "Das Unternehmen muss deshalb ein Energie- oder Umweltmanagementsystem betreiben und für die darin als wirtschaftlich ermittelten Einsparmaßnahmen Umsetzungspläne erstellen und veröffentlichen.",
            "en": "The company must therefore operate an energy or environmental management system and draw up and publish implementation plans for the energy-saving measures identified in it as economically viable.",
            "es": "Por tanto, la empresa debe mantener un sistema de gestión energética o ambiental y elaborar y publicar planes de ejecución para las medidas de ahorro que este identifique como económicamente viables.",
            "fr": "L'entreprise doit donc exploiter un système de management de l'énergie ou de l'environnement et établir et publier des plans de mise en œuvre pour les mesures d'économie qui y sont identifiées comme économiquement viables.",
            "it": "L'impresa deve quindi gestire un sistema di gestione dell'energia o ambientale ed elaborare e pubblicare piani di attuazione per le misure di risparmio in esso individuate come economicamente convenienti.",
            "zh": "因此，公司必须运行能源或环境管理体系，并针对体系中确认为经济可行的节能措施制定并公布实施计划。",
        },
        "ja_umsetzungsplan": {
            "de": "Das Unternehmen muss deshalb für die im Energieaudit oder Managementsystem als wirtschaftlich ermittelten Einsparmaßnahmen binnen drei Jahren Umsetzungspläne erstellen und veröffentlichen; ein Managementsystem ist nicht vorgeschrieben.",
            "en": "The company must therefore draw up and publish, within three years, implementation plans for the energy-saving measures identified as economically viable in the energy audit or management system; a management system is not mandatory.",
            "es": "Por tanto, la empresa debe elaborar y publicar en un plazo de tres años planes de ejecución para las medidas de ahorro identificadas como económicamente viables en la auditoría energética o en el sistema de gestión; no es obligatorio un sistema de gestión.",
            "fr": "L'entreprise doit donc établir et publier, dans un délai de trois ans, des plans de mise en œuvre pour les mesures d'économie identifiées comme économiquement viables dans l'audit énergétique ou le système de management ; un système de management n'est pas obligatoire.",
            "it": "L'impresa deve quindi elaborare e pubblicare entro tre anni piani di attuazione per le misure di risparmio individuate come economicamente convenienti nell'audit energetico o nel sistema di gestione; un sistema di gestione non è obbligatorio.",
            "zh": "因此，公司必须在三年内针对能源审计或管理体系中确认为经济可行的节能措施制定并公布实施计划；不强制要求建立管理体系。",
        },
        "nein": {
            "de": "Die Pflichten der §§ 8 und 9 des Energieeffizienzgesetzes greifen damit nicht.",
            "en": "The obligations under Sections 8 and 9 of the German Energy Efficiency Act (EnEfG) therefore do not apply.",
            "es": "Por tanto, no se aplican las obligaciones de los §§ 8 y 9 de la Ley alemana de eficiencia energética (EnEfG).",
            "fr": "Les obligations des §§ 8 et 9 de la loi allemande sur l'efficacité énergétique (EnEfG) ne s'appliquent donc pas.",
            "it": "Gli obblighi dei §§ 8 e 9 della legge tedesca sull'efficienza energetica (EnEfG) non si applicano quindi.",
            "zh": "因此，德国《能源效率法》（EnEfG）第 8 条和第 9 条规定的义务不适用。",
        },
        "moeglich": {
            "de": "Ob Pflichten bestehen, lässt sich deshalb erst mit dem Verbrauch der letzten drei Kalenderjahre beurteilen.",
            "en": "Whether obligations exist can therefore only be assessed on the basis of the consumption of the last three calendar years.",
            "es": "Por ello, la existencia de obligaciones solo puede valorarse con el consumo de los tres últimos años naturales.",
            "fr": "L'existence d'obligations ne peut donc être appréciée qu'au vu de la consommation des trois dernières années civiles.",
            "it": "La sussistenza di obblighi può quindi essere valutata solo sulla base del consumo degli ultimi tre anni civili.",
            "zh": "因此，是否负有义务，只有根据最近三个日历年的能耗才能判断。",
        },
    },
    "AbwV38": {
        "ja": {
            "de": "Das Abwasser muss deshalb die Anforderungen des Anhangs 38 erfüllen, bei weniger als 5 m³ je Tag nur die allgemeinen Anforderungen und den CSB-Wert.",
            "en": "The wastewater must therefore meet the requirements of Annex 38, and below 5 m³ per day only the general requirements and the COD value.",
            "es": "Por tanto, las aguas residuales deben cumplir los requisitos del anexo 38 y, con menos de 5 m³ al día, solo los requisitos generales y el valor de DQO.",
            "fr": "Les eaux usées doivent donc satisfaire aux exigences de l'annexe 38 et, en dessous de 5 m³ par jour, uniquement aux exigences générales et à la valeur de DCO.",
            "it": "Le acque reflue devono quindi soddisfare i requisiti dell'allegato 38 e, al di sotto di 5 m³ al giorno, solo i requisiti generali e il valore di COD.",
            "zh": "因此，废水必须符合附件 38 的要求，每日少于 5 m³ 的仅须符合一般要求和化学需氧量（COD）限值。",
        },
        "nein": {
            "de": "Anhang 38 der Abwasserverordnung ist für das Unternehmen damit nicht einschlägig.",
            "en": "Annex 38 of the German Wastewater Ordinance (AbwV) therefore does not apply to the company.",
            "es": "Por tanto, el anexo 38 del Reglamento alemán de aguas residuales (AbwV) no es aplicable a la empresa.",
            "fr": "L'annexe 38 du règlement allemand sur les eaux usées (AbwV) ne s'applique donc pas à l'entreprise.",
            "it": "L'allegato 38 del regolamento tedesco sulle acque reflue (AbwV) non è quindi applicabile all'impresa.",
            "zh": "因此，德国《废水条例》（AbwV）附件 38 不适用于该公司。",
        },
        "moeglich": {
            "de": "Ob Anhang 38 greift, ist deshalb anhand der Prozesse an den deutschen Standorten zu prüfen.",
            "en": "Whether Annex 38 applies must therefore be assessed on the basis of the processes at the German sites.",
            "es": "Por ello, si se aplica el anexo 38 debe examinarse a partir de los procesos de las plantas en Alemania.",
            "fr": "L'applicabilité de l'annexe 38 doit donc être examinée au regard des procédés mis en œuvre sur les sites allemands.",
            "it": "Se si applichi l'allegato 38 va quindi valutato in base ai processi negli stabilimenti tedeschi.",
            "zh": "因此，是否适用附件 38，须根据德国各生产场所的工艺进行审查。",
        },
    },
    # --- Katalogerweiterung 29.09.2026 ---
    "EPR_FR": {
        "ja": {
            "de": "Das Unternehmen muss deshalb einer zugelassenen Branchenorganisation (derzeit Refashion) beitreten und Beiträge zahlen; ohne Sitz in Frankreich ist seit 10.07.2026 ein dort niedergelassener Bevollmächtigter zu benennen.",
            "en": "The company must therefore join an approved producer responsibility organisation (éco-organisme, currently Refashion) and pay contributions; without a registered office in France, an authorised representative (mandataire) established there has had to be appointed since 10.07.2026.",
            "es": "Por tanto, la empresa debe adherirse a una organización de responsabilidad del productor autorizada (éco-organisme, actualmente Refashion) y abonar contribuciones; sin domicilio social en Francia, desde el 10.07.2026 debe designarse un representante autorizado (mandataire) establecido allí.",
            "fr": "L'entreprise doit donc adhérer à un éco-organisme agréé (actuellement Refashion) et verser des contributions ; sans siège en France, elle doit, depuis le 10.07.2026, désigner un mandataire qui y est établi.",
            "it": "L'impresa deve quindi aderire a un'organizzazione per la responsabilità del produttore autorizzata (éco-organisme, attualmente Refashion) e versare contributi; in assenza di una sede in Francia, dal 10.07.2026 deve essere designato un mandatario (mandataire) ivi stabilito.",
            "zh": "因此，公司必须加入经批准的生产者责任组织（éco-organisme，目前为 Refashion）并缴纳费用；在法国没有注册地的，自 2026 年 7 月 10 日起须指定一名在当地设立的授权代表（mandataire）。",
        },
        "nein": {
            "de": "Die französische Herstellerverantwortung für Textilien ist für das Unternehmen damit nicht einschlägig.",
            "en": "French extended producer responsibility for textiles is therefore not relevant to the company.",
            "es": "Por tanto, la responsabilidad ampliada del productor de textiles en Francia no es pertinente para la empresa.",
            "fr": "La responsabilité élargie du producteur pour les textiles en France ne concerne donc pas l'entreprise.",
            "it": "La responsabilità estesa del produttore per i tessili in Francia non è quindi pertinente per l'impresa.",
            "zh": "因此，法国纺织品生产者延伸责任不适用于该公司。",
        },
        "moeglich": {
            "de": "Ob die Pflicht besteht, ist deshalb anhand der tatsächlichen Lieferungen nach Frankreich und der Abnehmer zu prüfen.",
            "en": "Whether the obligation applies must therefore be checked on the basis of actual deliveries to France and the customers.",
            "es": "Por ello, si existe la obligación debe comprobarse a partir de las entregas efectivas a Francia y de los destinatarios.",
            "fr": "L'existence de l'obligation doit donc être vérifiée au regard des livraisons effectives vers la France et des destinataires.",
            "it": "Se l'obbligo sussista va quindi verificato sulla base delle forniture effettive verso la Francia e dei destinatari.",
            "zh": "因此，是否负有该义务，须根据实际向法国的供货情况及收货方予以核查。",
        },
    },
    "EPR_NL": {
        "ja": {
            "de": "Das Unternehmen muss deshalb die Sammel- und Recyclingquoten selbst oder über eine Produzentenorganisation erfüllen und jährlich vor dem 1. August berichten; ohne Sitz in den Niederlanden ist ein dort niedergelassener Bevollmächtigter zu benennen.",
            "en": "The company must therefore meet the collection and recycling targets itself or through a producer organisation and report annually before 1 August; without a registered office in the Netherlands, an authorised representative (gemachtigd vertegenwoordiger) established there must be appointed.",
            "es": "Por tanto, la empresa debe cumplir los objetivos de recogida y reciclado por sí misma o a través de una organización de productores e informar cada año antes del 1 de agosto; sin domicilio social en los Países Bajos, debe designarse un representante autorizado (gemachtigd vertegenwoordiger) establecido allí.",
            "fr": "L'entreprise doit donc atteindre les taux de collecte et de recyclage elle-même ou par l'intermédiaire d'une organisation de producteurs et en rendre compte chaque année avant le 1er août ; sans siège aux Pays-Bas, elle doit désigner un mandataire (gemachtigd vertegenwoordiger) qui y est établi.",
            "it": "L'impresa deve quindi conseguire gli obiettivi di raccolta e riciclaggio direttamente o tramite un'organizzazione di produttori e riferire ogni anno prima del 1° agosto; in assenza di una sede nei Paesi Bassi, deve essere designato un mandatario (gemachtigd vertegenwoordiger) ivi stabilito.",
            "zh": "因此，公司必须自行或通过生产者组织完成收集和回收配额，并每年在 8 月 1 日前提交报告；在荷兰没有注册地的，须指定一名在当地设立的授权代表（gemachtigd vertegenwoordiger）。",
        },
        "nein": {
            "de": "Die niederländische Herstellerverantwortung für Textilien ist für das Unternehmen damit nicht einschlägig.",
            "en": "Dutch extended producer responsibility for textiles is therefore not relevant to the company.",
            "es": "Por tanto, la responsabilidad ampliada del productor de textiles en los Países Bajos no es pertinente para la empresa.",
            "fr": "La responsabilité élargie du producteur pour les textiles aux Pays-Bas ne concerne donc pas l'entreprise.",
            "it": "La responsabilità estesa del produttore per i tessili nei Paesi Bassi non è quindi pertinente per l'impresa.",
            "zh": "因此，荷兰纺织品生产者延伸责任不适用于该公司。",
        },
        "moeglich": {
            "de": "Ob die Pflicht besteht, ist deshalb anhand der tatsächlichen Lieferungen in die Niederlande zu prüfen.",
            "en": "Whether the obligation applies must therefore be checked on the basis of actual deliveries to the Netherlands.",
            "es": "Por ello, si existe la obligación debe comprobarse a partir de las entregas efectivas a los Países Bajos.",
            "fr": "L'existence de l'obligation doit donc être vérifiée au regard des livraisons effectives vers les Pays-Bas.",
            "it": "Se l'obbligo sussista va quindi verificato sulla base delle forniture effettive verso i Paesi Bassi.",
            "zh": "因此，是否负有该义务，须根据实际向荷兰的供货情况予以核查。",
        },
    },
}

COUPLING_PASSAGES: dict[str, dict[str, str]] = {
    "CSR-RUG": {
        "de": "§ 289b Abs. 1 HGB: Kapitalgesellschaft, die die Voraussetzungen des § 267 Abs. 3 "
              "Satz 1 erfüllt, kapitalmarktorientiert im Sinne des § 264d ist und im Jahresdurchschnitt "
              "mehr als 500 Arbeitnehmer beschäftigt.",
        "en": "Section 289b(1) HGB: a company that meets the conditions of section 267(3) sentence 1, "
              "is capital-market oriented within the meaning of section 264d and has more than 500 "
              "employees on annual average.",
        "es": "§ 289b, apdo. 1, HGB: sociedad que cumple los requisitos del § 267, apdo. 3, frase 1, "
              "está orientada al mercado de capitales según el § 264d y tiene más de 500 trabajadores "
              "de media anual.",
        "fr": "§ 289b, al. 1, HGB : société remplissant les conditions du § 267, al. 3, phrase 1, "
              "faisant appel au marché des capitaux au sens du § 264d et employant plus de 500 "
              "salariés en moyenne annuelle.",
        "it": "§ 289b, c. 1, HGB: società che soddisfa i requisiti del § 267, c. 3, per. 1, fa ricorso "
              "al mercato dei capitali ai sensi del § 264d e ha più di 500 dipendenti in media annua.",
        "zh": "《商法典》第 289b 条第 1 款：满足第 267 条第 3 款第 1 句条件、属于第 264d 条意义上的资本市场导向企业且年平均雇员超过 500 人的资合公司。",
    },
    "CSRD": {
        "de": "Art. 19a Abs. 1 der Richtlinie 2013/34/EU (i. d. F. der Richtlinie (EU) 2026/470): "
              "große Unternehmen mit mehr als 1.000 Beschäftigten und mehr als 450 Mio. EUR "
              "Nettoumsatzerlösen.",
        "en": "Art. 19a(1) of Directive 2013/34/EU (as amended by Directive (EU) 2026/470): large "
              "undertakings with more than 1,000 employees and more than EUR 450 million net turnover.",
        "es": "Art. 19 bis, apdo. 1, de la Directiva 2013/34/UE (según la Directiva (UE) 2026/470): "
              "grandes empresas con más de 1.000 empleados y más de 450 millones EUR de cifra neta "
              "de negocios.",
        "fr": "Art. 19 bis, par. 1, de la directive 2013/34/UE (telle que modifiée par la directive "
              "(UE) 2026/470) : grandes entreprises de plus de 1 000 salariés et plus de 450 "
              "millions EUR de chiffre d'affaires net.",
        "it": "Art. 19 bis, par. 1, della direttiva 2013/34/UE (come modificata dalla direttiva (UE) "
              "2026/470): grandi imprese con più di 1.000 dipendenti e oltre 450 milioni di EUR di "
              "ricavi netti.",
        "zh": "《指令》2013/34/EU 第 19a 条第 1 款（经指令 (EU) 2026/470 修订）：员工超过 1,000 名且净营业额超过 "
              "4.5 亿欧元的大型企业。",
    },
    "CSRD_DE": {
        "de": "§ 289b HGB in der Fassung des CSRD-Umsetzungsgesetzes (Regierungsentwurf): "
              "Nachhaltigkeitsberichterstattung im Lagebericht nach den Schwellen der CSRD.",
        "en": "Section 289b HGB as drafted in the CSRD implementation act (government bill): "
              "sustainability reporting in the management report following the CSRD thresholds.",
        "es": "§ 289b HGB en la redacción de la ley de transposición de la CSRD (proyecto del "
              "Gobierno): información de sostenibilidad en el informe de gestión según los umbrales "
              "de la CSRD.",
        "fr": "§ 289b HGB dans la version de la loi de transposition de la CSRD (projet du "
              "gouvernement) : reporting de durabilité dans le rapport de gestion selon les seuils "
              "de la CSRD.",
        "it": "§ 289b HGB nella versione della legge di recepimento della CSRD (disegno di legge "
              "governativo): rendicontazione di sostenibilità nella relazione sulla gestione secondo "
              "le soglie della CSRD.",
        "zh": "CSRD 转化法（政府草案）版本的《商法典》第 289b 条：按 CSRD 门槛在管理报告中进行可持续发展报告。",
    },
    "TaxonomieVO": {
        "de": "Art. 8 Abs. 1 der Verordnung (EU) 2020/852: Offenlegungspflicht für Unternehmen, die "
              "eine nichtfinanzielle Erklärung nach Art. 19a oder 29a der Richtlinie 2013/34/EU "
              "abgeben müssen.",
        "en": "Art. 8(1) of Regulation (EU) 2020/852: disclosure duty for undertakings required to "
              "publish a non-financial statement under Art. 19a or 29a of Directive 2013/34/EU.",
        "es": "Art. 8, apdo. 1, del Reglamento (UE) 2020/852: obligación de divulgación para las "
              "empresas obligadas a presentar un estado no financiero conforme a los arts. 19 bis o "
              "29 bis de la Directiva 2013/34/UE.",
        "fr": "Art. 8, par. 1, du règlement (UE) 2020/852 : obligation de publication pour les "
              "entreprises tenues de publier une déclaration non financière au titre des art. 19 bis "
              "ou 29 bis de la directive 2013/34/UE.",
        "it": "Art. 8, par. 1, del regolamento (UE) 2020/852: obbligo informativo per le imprese "
              "tenute a pubblicare una dichiarazione non finanziaria ex artt. 19 bis o 29 bis della "
              "direttiva 2013/34/UE.",
        "zh": "《条例》(EU) 2020/852 第 8 条第 1 款：须依《指令》2013/34/EU 第 19a 条或第 29a 条提交非财务报表的企业负有披露义务。",
    },
    "HinSchG": {
        "de": "§ 12 Abs. 1 und 2 HinSchG: Beschäftigungsgeber mit in der Regel mindestens 50 "
              "Beschäftigten richten eine interne Meldestelle ein.",
        "en": "Section 12(1) and (2) HinSchG: employers with as a rule at least 50 employees have to "
              "set up an internal reporting office.",
        "es": "§ 12, apdos. 1 y 2, HinSchG: los empleadores con al menos 50 empleados por regla "
              "general deben crear un órgano interno de denuncias.",
        "fr": "§ 12, al. 1 et 2, HinSchG : les employeurs comptant en règle générale au moins 50 "
              "salariés mettent en place un service de signalement interne.",
        "it": "§ 12, commi 1 e 2, HinSchG: i datori di lavoro con di regola almeno 50 dipendenti "
              "istituiscono un ufficio di segnalazione interno.",
        "zh": "《举报人保护法》第 12 条第 1、2 款：通常雇用至少 50 名员工的雇主须设立内部举报机构。",
    },
    # --- Katalogerweiterung 29.09.2026 ---
    "REACH_ART33": {
        "de": "Art. 33 Abs. 1 REACH: Jeder Lieferant eines Erzeugnisses, das einen Stoff der Kandidatenliste in einer Konzentration von mehr als 0,1 Massenprozent enthält, stellt dem Abnehmer die ihm vorliegenden, für eine sichere Verwendung ausreichenden Informationen zur Verfügung.",
        "en": "Art. 33(1) REACH: Any supplier of an article containing a substance on the Candidate List in a concentration above 0.1% weight by weight shall provide the recipient of the article with sufficient information, available to the supplier, to allow safe use.",
        "es": "Art. 33, apdo. 1, REACH: Todo proveedor de un artículo que contenga una sustancia de la Lista de candidatas en una concentración superior al 0,1 % en peso/peso facilitará al destinatario del artículo la información suficiente de que disponga para permitir un uso seguro.",
        "fr": "Art. 33, par. 1, REACH : Tout fournisseur d'un article contenant une substance de la liste des substances candidates dans une concentration supérieure à 0,1 % masse/masse fournit au destinataire de l'article des informations suffisantes dont il dispose pour permettre une utilisation sûre.",
        "it": "Art. 33, par. 1, REACH: Il fornitore di un articolo contenente una sostanza dell'elenco di sostanze candidate in concentrazione superiore allo 0,1% in peso/peso fornisce al destinatario dell'articolo informazioni sufficienti, di cui dispone, per consentirne un uso sicuro.",
        "zh": "REACH 第 33 条第 1 款：物品中所含候选清单物质的浓度按质量计超过 0.1% 的，该物品的任何供应商均应向物品接收者提供其所掌握的、足以确保安全使用的信息。",
    },
    "SCIP": {
        "de": "§ 16f ChemG: Lieferanten von Erzeugnissen mit einem Stoff der Kandidatenliste über 0,1 Massenprozent übermitteln der ECHA unverzüglich nach dem Inverkehrbringen die Informationen nach Art. 33 Abs. 1 REACH.",
        "en": "Section 16f ChemG: Suppliers of articles containing a substance on the Candidate List above 0.1% by weight shall submit the information under Art. 33(1) REACH to ECHA without delay after placing them on the market.",
        "es": "§ 16f ChemG: Los proveedores de artículos que contengan una sustancia de la Lista de candidatas en más del 0,1 % en peso transmitirán a la ECHA, sin demora tras su introducción en el mercado, la información prevista en el art. 33, apdo. 1, REACH.",
        "fr": "§ 16f ChemG : Les fournisseurs d'articles contenant une substance de la liste des substances candidates à plus de 0,1 % en masse transmettent à l'ECHA, sans délai après la mise sur le marché, les informations visées à l'art. 33, par. 1, REACH.",
        "it": "§ 16f ChemG: I fornitori di articoli contenenti una sostanza dell'elenco di sostanze candidate in misura superiore allo 0,1% in peso trasmettono all'ECHA, senza indugio dopo l'immissione sul mercato, le informazioni di cui all'art. 33, par. 1, REACH.",
        "zh": "德国《化学品法》（ChemG）第 16f 条：含有质量分数超过 0.1% 的候选清单物质的物品，其供应商应在投放市场后立即向 ECHA 提交 REACH 第 33 条第 1 款规定的信息。",
    },
    "BPR": {
        "de": "Art. 58 Abs. 2 Biozid-VO: Eine behandelte Ware darf nur in Verkehr gebracht werden, wenn alle Wirkstoffe der Biozidprodukte, mit denen sie behandelt wurde oder die sie enthält, für die betreffende Produktart genehmigt sind.",
        "en": "Art. 58(2) of the Biocidal Products Regulation: A treated article shall not be placed on the market unless all active substances contained in the biocidal products that it was treated with or incorporates are approved for the relevant product-type.",
        "es": "Art. 58, apdo. 2, del Reglamento de biocidas: No se introducirá en el mercado ningún artículo tratado a menos que todas las sustancias activas contenidas en los biocidas con los que se haya tratado o que incorpore estén aprobadas para el tipo de producto de que se trate.",
        "fr": "Art. 58, par. 2, du règlement sur les produits biocides : Un article traité n'est mis sur le marché que si toutes les substances actives contenues dans les produits biocides avec lesquels il a été traité ou qu'il intègre sont approuvées pour le type de produits concerné.",
        "it": "Art. 58, par. 2, del regolamento sui biocidi: Un articolo trattato non è immesso sul mercato a meno che tutti i principi attivi contenuti nei biocidi con cui è stato trattato o che esso incorpora siano approvati per il tipo di prodotto pertinente.",
        "zh": "《生物杀灭剂法规》第 58 条第 2 款：经处理物品只有在其处理所用或所含的生物杀灭产品中的全部活性物质已就相关产品类型获得批准时，方可投放市场。",
    },
    "PSA": {
        "de": "Art. 1 PSA-VO: Die Verordnung legt Anforderungen an Entwurf und Herstellung persönlicher Schutzausrüstung fest, die auf dem Markt bereitgestellt werden soll, um Gesundheit und Sicherheit der Nutzer zu schützen.",
        "en": "Art. 1 of the PPE Regulation: This Regulation lays down requirements for the design and manufacture of personal protective equipment which is to be made available on the market, in order to ensure protection of the health and safety of users.",
        "es": "Art. 1 del Reglamento de EPI: El presente Reglamento establece requisitos para el diseño y la fabricación de los equipos de protección individual que vayan a comercializarse, con el fin de garantizar la protección de la salud y la seguridad de los usuarios.",
        "fr": "Art. 1er du règlement EPI : Le présent règlement établit des exigences relatives à la conception et à la fabrication des équipements de protection individuelle qui doivent être mis à disposition sur le marché, afin de garantir la protection de la santé et la sécurité des utilisateurs.",
        "it": "Art. 1 del regolamento DPI: Il presente regolamento stabilisce i requisiti per la progettazione e la fabbricazione dei dispositivi di protezione individuale che devono essere messi a disposizione sul mercato, al fine di garantire la protezione della salute e della sicurezza degli utilizzatori.",
        "zh": "《个人防护装备法规》第 1 条：本法规规定了拟在市场上提供的个人防护装备的设计和制造要求，以保护使用者的健康和安全。",
    },
    "MDR": {
        "de": "Art. 2 Nr. 1 MDR: Medizinprodukt ist ein Produkt, das dem Hersteller zufolge für Menschen bestimmt ist und allein oder in Kombination einen oder mehrere spezifische medizinische Zwecke erfüllen soll.",
        "en": "Art. 2(1) MDR: “Medical device” means a product intended by the manufacturer to be used, alone or in combination, for human beings for one or more specific medical purposes.",
        "es": "Art. 2, punto 1, MDR: «Producto sanitario» es todo producto destinado por el fabricante a ser utilizado en personas, por separado o en combinación, con uno o varios fines médicos específicos.",
        "fr": "Art. 2, point 1, MDR : Un « dispositif médical » est tout produit destiné par le fabricant à être utilisé, seul ou en association, chez l'homme pour une ou plusieurs fins médicales précises.",
        "it": "Art. 2, punto 1, MDR: Per «dispositivo medico» si intende qualunque prodotto destinato dal fabbricante a essere impiegato sull'uomo, da solo o in combinazione, per una o più destinazioni d'uso mediche specifiche.",
        "zh": "MDR 第 2 条第 1 点：“医疗器械”是指制造商预期单独或组合用于人体、以实现一项或多项特定医疗目的的产品。",
    },
    "Schuhkennzeichnung": {
        "de": "§ 10a Abs. 1 BedGgstV: Schuherzeugnisse nach Anlage 11 Nr. 1 müssen vom Hersteller, seinem Bevollmächtigten oder dem Erstinverkehrbringer in der EU vor dem gewerbsmäßigen Inverkehrbringen mit den Angaben nach Absatz 2 versehen werden.",
        "en": "Section 10a(1) BedGgstV: Footwear under Annex 11 No. 1 must be provided with the information under subsection 2 by the manufacturer, its authorised representative or the person first placing it on the market in the EU before it is placed on the market commercially.",
        "es": "§ 10a, apdo. 1, BedGgstV: Los artículos de calzado del anexo 11, punto 1, deben llevar las indicaciones del apartado 2, colocadas por el fabricante, su representante autorizado o quien los introduzca por primera vez en el mercado de la UE, antes de su introducción comercial en el mercado.",
        "fr": "§ 10a, al. 1, BedGgstV : Les articles chaussants visés à l'annexe 11, point 1, doivent être munis des indications prévues à l'alinéa 2 par le fabricant, son mandataire ou la personne qui les met la première sur le marché de l'UE, avant leur mise sur le marché à titre professionnel.",
        "it": "§ 10a, c. 1, BedGgstV: Le calzature di cui all'allegato 11, punto 1, devono essere corredate delle indicazioni di cui al comma 2 dal fabbricante, dal suo mandatario o da chi le immette per primo sul mercato dell'UE prima dell'immissione sul mercato a titolo professionale.",
        "zh": "德国《日用品条例》（BedGgstV）第 10a 条第 1 款：附件 11 第 1 项所列鞋类产品，须由制造商、其授权代表或在欧盟首次投放市场者在以商业方式投放市场前标注第 2 款规定的信息。",
    },
    "EnEfG": {
        "de": "§ 8 Abs. 1 EnEfG: Unternehmen mit einem jährlichen durchschnittlichen Gesamtendenergieverbrauch innerhalb der letzten drei abgeschlossenen Kalenderjahre von mehr als 7,5 Gigawattstunden sind verpflichtet, ein Energie- oder Umweltmanagementsystem einzurichten.",
        "en": "Section 8(1) EnEfG: Companies with an average annual total final energy consumption of more than 7.5 gigawatt hours over the last three completed calendar years are obliged to set up an energy or environmental management system.",
        "es": "§ 8, apdo. 1, EnEfG: Las empresas con un consumo total medio anual de energía final superior a 7,5 gigavatios hora en los tres últimos años naturales cerrados están obligadas a implantar un sistema de gestión energética o ambiental.",
        "fr": "§ 8, al. 1, EnEfG : Les entreprises dont la consommation totale annuelle moyenne d'énergie finale au cours des trois dernières années civiles clôturées dépasse 7,5 gigawattheures sont tenues de mettre en place un système de management de l'énergie ou de l'environnement.",
        "it": "§ 8, c. 1, EnEfG: Le imprese con un consumo totale medio annuo di energia finale superiore a 7,5 gigawattora negli ultimi tre anni civili conclusi sono tenute a introdurre un sistema di gestione dell'energia o ambientale.",
        "zh": "德国《能源效率法》（EnEfG）第 8 条第 1 款：最近三个已结束日历年内年平均最终能源总消耗量超过 7.5 吉瓦时的企业，有义务建立能源或环境管理体系。",
    },
    "AbwV38": {
        "de": "Anhang 38 Teil A Abs. 1 AbwV: Dieser Anhang gilt für Abwasser, dessen Schadstofffracht im Wesentlichen aus der gewerblichen und industriellen Bearbeitung und Verarbeitung von Spinnstoffen und Garnen sowie der Textilveredlung stammt.",
        "en": "Annex 38, Part A(1) AbwV: This Annex applies to wastewater whose pollutant load originates essentially from the commercial and industrial treatment and processing of textile fibres and yarns and from textile finishing.",
        "es": "Anexo 38, parte A, apdo. 1, AbwV: El presente anexo se aplica a las aguas residuales cuya carga contaminante procede esencialmente del tratamiento y la transformación comercial e industrial de fibras textiles e hilados y del acabado textil.",
        "fr": "Annexe 38, partie A, al. 1, AbwV : La présente annexe s'applique aux eaux usées dont la charge polluante provient pour l'essentiel du traitement et de la transformation artisanaux et industriels des fibres textiles et des fils ainsi que de l'ennoblissement textile.",
        "it": "Allegato 38, parte A, c. 1, AbwV: Il presente allegato si applica alle acque reflue il cui carico inquinante deriva essenzialmente dal trattamento e dalla lavorazione commerciale e industriale di fibre tessili e filati e dal finissaggio tessile.",
        "zh": "德国《废水条例》（AbwV）附件 38 A 部分第 1 款：本附件适用于污染物负荷主要来自纺织纤维和纱线的商业及工业处理与加工以及纺织品整理的废水。",
    },
    # --- Katalogerweiterung 29.09.2026 ---
    "EPR_FR": {
        "de": "Art. L541-10-1 Nr. 11° Code de l'environnement: Der erweiterten Herstellerverantwortung unterliegen neue Bekleidungstextilien, Schuhe und Haushaltswäsche für Privatpersonen sowie neue Heimtextilien, soweit sie keine Möbelbestandteile sind.",
        "en": "Art. L541-10-1 No. 11° of the Code de l'environnement: Extended producer responsibility covers new clothing textiles, footwear and household linen intended for private individuals, as well as new home textiles, except those that are furniture components.",
        "es": "Art. L541-10-1, n.º 11°, del Code de l'environnement: Están sujetos a la responsabilidad ampliada del productor los productos textiles de vestir, el calzado y la ropa de hogar nuevos destinados a particulares, así como los productos textiles nuevos para la casa, salvo los que sean elementos de mobiliario.",
        "fr": "Art. L541-10-1, 11°, du code de l'environnement : Relèvent de la responsabilité élargie du producteur les produits textiles d'habillement, chaussures ou linge de maison neufs destinés aux particuliers ainsi que les produits textiles neufs pour la maison, à l'exclusion de ceux qui sont des éléments d'ameublement.",
        "it": "Art. L541-10-1, n. 11°, del Code de l'environnement: Sono soggetti alla responsabilità estesa del produttore i prodotti tessili di abbigliamento, le calzature e la biancheria per la casa nuovi destinati a privati, nonché i prodotti tessili nuovi per la casa, esclusi quelli che costituiscono elementi di arredo.",
        "zh": "法国《环境法典》（Code de l'environnement）第 L541-10-1 条第 11° 项：面向私人消费者的新服装纺织品、鞋类和家用布草，以及新的家居纺织品（属于家具组成部分者除外），均受生产者延伸责任约束。",
    },
    "EPR_NL": {
        "de": "Art. 1 Abs. 1 Besluit UPV textiel: Producent ist, wer beruflich und unabhängig von der Verkaufstechnik Textilprodukte in den Niederlanden in Verkehr bringt (in de handel brengt).",
        "en": "Art. 1(1) Besluit UPV textiel: A producer is anyone who, in a professional capacity and irrespective of the selling technique used, places textile products on the market in the Netherlands (in de handel brengt).",
        "es": "Art. 1, apdo. 1, Besluit UPV textiel: Es productor quien, con carácter profesional e independientemente de la técnica de venta, introduce productos textiles en el mercado de los Países Bajos (in de handel brengt).",
        "fr": "Art. 1, par. 1, Besluit UPV textiel : Est producteur quiconque, à titre professionnel et quelle que soit la technique de vente, met des produits textiles sur le marché aux Pays-Bas (in de handel brengt).",
        "it": "Art. 1, par. 1, Besluit UPV textiel: È produttore chiunque, a titolo professionale e indipendentemente dalla tecnica di vendita, immette prodotti tessili sul mercato nei Paesi Bassi (in de handel brengt).",
        "zh": "荷兰《Besluit UPV textiel》（纺织品生产者延伸责任法令）第 1 条第 1 款：凡以职业身份、不论采用何种销售方式在荷兰将纺织品投放市场（in de handel brengt）者，即为生产者。",
    },
}


def fmt_int(value, lang: str = "de") -> str:
    """Ganzzahl mit sprachueblichem Tausendertrennzeichen."""
    try:
        number = int(round(float(value or 0)))
    except (TypeError, ValueError):
        number = 0
    return f"{number:,}".replace(",", _THOUSANDS_SEP.get(normalize_lang(lang), "."))


def fmt_eur(value, lang: str = "de") -> str:
    """Betrag mit Waehrungskuerzel, z. B. '450.000.000 EUR'."""
    return f"{fmt_int(value, lang)} EUR"


# Dezimaltrennzeichen: Komma ausser im Englischen und Chinesischen.
_DECIMAL_SEP: dict[str, str] = {"de": ",", "en": ".", "es": ",", "fr": ",", "it": ",", "zh": "."}


def fmt_gwh(value, lang: str = "de") -> str:
    """Energiemenge mit bis zu zwei Nachkommastellen, z. B. '7,5 GWh'."""
    try:
        number = float(value or 0)
    except (TypeError, ValueError):
        number = 0.0
    text = f"{number:.2f}".rstrip("0").rstrip(".")
    return text.replace(".", _DECIMAL_SEP.get(normalize_lang(lang), ",")) + " GWh"


def coupling_fact(verdict: dict, lang: str = "de") -> str:
    """Satz 1 der deterministischen Begruendung (Schwelle + Ist-Wert)."""
    lang = normalize_lang(lang)
    template = COUPLING_FACTS.get(verdict.get("fact", ""), {}).get(lang, "")
    if not template:
        return ""
    values = verdict.get("values") or {}
    return template.format(
        employees=fmt_int(values.get("employees"), lang),
        employees_de=fmt_int(values.get("employees_de"), lang),
        revenue=fmt_eur(values.get("revenue_eur"), lang),
        revenue_eu=fmt_eur(values.get("revenue_eu_eur"), lang),
        energy=fmt_gwh(values.get("energy_gwh"), lang),
    )


def coupling_texts(reg_key: str, verdict: dict, lang: str = "de") -> tuple[str, str] | None:
    """(Begruendung, Fundstelle) fuer eine gekoppelte Regulierung.

    None, wenn fuer diesen Fall kein Baustein hinterlegt ist — dann bewertet
    weiterhin das LLM (mit der Praemisse aus `regulations.coupling_premise`).
    """
    lang = normalize_lang(lang)
    fact = coupling_fact(verdict, lang)
    conclusion = (COUPLING_CONCLUSIONS.get(reg_key, {})
                  .get(verdict.get("conclusion", ""), {}).get(lang, ""))
    passage = COUPLING_PASSAGES.get(reg_key, {}).get(lang, "")
    if not (fact and conclusion and passage):
        return None
    # Im Chinesischen trennt das Satzzeichen selbst, ein Leerzeichen waere falsch.
    separator = "" if lang == "zh" else " "
    return f"{fact}{separator}{conclusion}", passage


# ---------- Dropdown-Optionen (Key = DE-Wert, damit DB-kompatibel) ----------
BRANCH_LABELS: dict[str, dict[str, str]] = {
    "Spinnstoffaufbereitung und Spinnerei": {
        "de": "Spinnstoffaufbereitung und Spinnerei",
        "en": "Preparation and spinning of textile fibres",
        "es": "Preparación e hilado de fibras textiles",
        "fr": "Préparation de fibres textiles et filature",
        "it": "Preparazione e filatura di fibre tessili",
        "zh": "纺织纤维预处理及纺纱",
    },
    "Weberei": {
        "de": "Weberei",
        "en": "Weaving of textiles",
        "es": "Fabricación de tejidos textiles",
        "fr": "Tissage",
        "it": "Tessitura",
        "zh": "机织物制造",
    },
    "Veredlung von Textilien und Bekleidung": {
        "de": "Veredlung von Textilien und Bekleidung",
        "en": "Finishing of textiles and apparel",
        "es": "Acabado de textiles y prendas de vestir",
        "fr": "Ennoblissement textile et de l'habillement",
        "it": "Finissaggio di tessili e abbigliamento",
        "zh": "纺织品和服装整理",
    },
    "Herstellung von gewirktem und gestricktem Stoff": {
        "de": "Herstellung von gewirktem und gestricktem Stoff",
        "en": "Manufacture of knitted and crocheted fabrics",
        "es": "Fabricación de tejidos de punto",
        "fr": "Fabrication d'étoffes à mailles",
        "it": "Fabbricazione di tessuti a maglia",
        "zh": "针织和钩针织物制造",
    },
    "Herstellung von konfektionierten Textilwaren (ohne Bekleidung)": {
        "de": "Herstellung von konfektionierten Textilwaren (ohne Bekleidung)",
        "en": "Manufacture of made-up textile articles, except apparel",
        "es": "Fabricación de artículos confeccionados con textiles, excepto prendas de vestir",
        "fr": "Fabrication d'articles textiles, sauf habillement",
        "it": "Confezionamento di articoli tessili (esclusi gli articoli di abbigliamento)",
        "zh": "纺织制成品制造（服装除外）",
    },
    "Herstellung von Teppichen": {
        "de": "Herstellung von Teppichen",
        "en": "Manufacture of carpets and rugs",
        "es": "Fabricación de alfombras y moquetas",
        "fr": "Fabrication de tapis et moquettes",
        "it": "Fabbricazione di tappeti e moquette",
        "zh": "地毯制造",
    },
    "Herstellung von Seilerwaren": {
        "de": "Herstellung von Seilerwaren",
        "en": "Manufacture of cordage, rope, twine and netting",
        "es": "Fabricación de cuerdas, cordeles, bramantes y redes",
        "fr": "Fabrication de ficelles, cordes et filets",
        "it": "Fabbricazione di spago, corde, funi e reti",
        "zh": "绳索、缆绳及网具制造",
    },
    "Herstellung von Vliesstoff und Erzeugnissen daraus (ohne Bekleidung)": {
        "de": "Herstellung von Vliesstoff und Erzeugnissen daraus (ohne Bekleidung)",
        "en": "Manufacture of non-wovens and articles made from non-wovens, except apparel",
        "es": "Fabricación de telas no tejidas y artículos confeccionados con ellas, excepto prendas de vestir",
        "fr": "Fabrication de non-tissés et d'articles en non-tissés, sauf habillement",
        "it": "Fabbricazione di tessuti non tessuti e di articoli in tali materie (esclusi gli articoli di abbigliamento)",
        "zh": "非织造布及其制品制造（服装除外）",
    },
    "Herstellung von technischen Textilien": {
        "de": "Herstellung von technischen Textilien",
        "en": "Manufacture of other technical and industrial textiles",
        "es": "Fabricación de otros productos textiles de uso técnico e industrial",
        "fr": "Fabrication d'autres textiles techniques et industriels",
        "it": "Fabbricazione di altri articoli tessili tecnici e industriali",
        "zh": "产业用及技术用纺织品制造",
    },
    "Herstellung von sonstigen Textilwaren a. n. g.": {
        "de": "Herstellung von sonstigen Textilwaren a. n. g.",
        "en": "Manufacture of other textiles n.e.c.",
        "es": "Fabricación de otros productos textiles n.c.o.p.",
        "fr": "Fabrication d'autres textiles n.c.a.",
        "it": "Fabbricazione di altri prodotti tessili n.c.a.",
        "zh": "其他未列明纺织品制造",
    },
    "Herstellung von Lederbekleidung": {
        "de": "Herstellung von Lederbekleidung",
        "en": "Manufacture of leather clothes",
        "es": "Confección de prendas de vestir de cuero",
        "fr": "Fabrication de vêtements en cuir",
        "it": "Confezione di capi di abbigliamento in pelle",
        "zh": "皮革服装制造",
    },
    "Herstellung von Arbeits- und Berufsbekleidung": {
        "de": "Herstellung von Arbeits- und Berufsbekleidung",
        "en": "Manufacture of workwear",
        "es": "Confección de ropa de trabajo",
        "fr": "Fabrication de vêtements de travail",
        "it": "Confezione di camici e divise da lavoro",
        "zh": "工作服及职业装制造",
    },
    "Herstellung von sonstiger Oberbekleidung": {
        "de": "Herstellung von sonstiger Oberbekleidung",
        "en": "Manufacture of other outerwear",
        "es": "Confección de otras prendas de vestir exteriores",
        "fr": "Fabrication d'autres vêtements de dessus",
        "it": "Confezione di altro abbigliamento esterno",
        "zh": "其他外衣制造",
    },
    "Herstellung von Wäsche": {
        "de": "Herstellung von Wäsche",
        "en": "Manufacture of underwear",
        "es": "Confección de ropa interior",
        "fr": "Fabrication de vêtements de dessous",
        "it": "Confezione di biancheria intima",
        "zh": "内衣制造",
    },
    "Herstellung von sonstiger Bekleidung und Bekleidungszubehör a. n. g.": {
        "de": "Herstellung von sonstiger Bekleidung und Bekleidungszubehör a. n. g.",
        "en": "Manufacture of other wearing apparel and accessories n.e.c.",
        "es": "Confección de otras prendas de vestir y complementos n.c.o.p.",
        "fr": "Fabrication d'autres vêtements et accessoires n.c.a.",
        "it": "Confezione di altri articoli di abbigliamento e accessori n.c.a.",
        "zh": "其他未列明服装及服饰配件制造",
    },
    "Herstellung von Pelzwaren": {
        "de": "Herstellung von Pelzwaren",
        "en": "Manufacture of articles of fur",
        "es": "Fabricación de artículos de peletería",
        "fr": "Fabrication d'articles en fourrure",
        "it": "Confezione di articoli in pelliccia",
        "zh": "毛皮制品制造",
    },
    "Herstellung von Strumpfwaren": {
        "de": "Herstellung von Strumpfwaren",
        "en": "Manufacture of knitted and crocheted hosiery",
        "es": "Fabricación de calcetería",
        "fr": "Fabrication d'articles chaussants à mailles",
        "it": "Fabbricazione di articoli di calzetteria in maglia",
        "zh": "针织袜类制造",
    },
    "Herstellung von sonstiger Bekleidung aus gewirktem und gestricktem Stoff": {
        "de": "Herstellung von sonstiger Bekleidung aus gewirktem und gestricktem Stoff",
        "en": "Manufacture of other knitted and crocheted apparel",
        "es": "Fabricación de otras prendas de vestir de punto",
        "fr": "Fabrication d'autres vêtements à mailles",
        "it": "Fabbricazione di altri articoli di abbigliamento in maglia",
        "zh": "其他针织或钩针编织服装制造",
    },
    "Herstellung von Leder und Lederfaserstoff; Zurichtung und Färben von Fellen": {
        "de": "Herstellung von Leder und Lederfaserstoff; Zurichtung und Färben von Fellen",
        "en": "Tanning and dressing of leather; dressing and dyeing of fur",
        "es": "Preparación, curtido y acabado del cuero; preparación y teñido de pieles",
        "fr": "Apprêt et tannage des cuirs; préparation et teinture des fourrures",
        "it": "Preparazione e concia del cuoio; preparazione e tintura di pellicce",
        "zh": "皮革鞣制及加工；毛皮鞣制与染色",
    },
    "Lederverarbeitung (ohne Herstellung von Lederbekleidung)": {
        "de": "Lederverarbeitung (ohne Herstellung von Lederbekleidung)",
        "en": "Manufacture of luggage, handbags and saddlery (except leather clothes)",
        "es": "Fabricación de artículos de marroquinería y guarnicionería (excepto prendas de vestir de cuero)",
        "fr": "Fabrication d'articles de voyage, de maroquinerie et de sellerie (hors vêtements en cuir)",
        "it": "Fabbricazione di articoli da viaggio, borse, pelletteria e selleria (esclusi i capi di abbigliamento in pelle)",
        "zh": "皮革制品加工（皮革服装除外）",
    },
    "Herstellung von Schuhen": {
        "de": "Herstellung von Schuhen",
        "en": "Manufacture of footwear",
        "es": "Fabricación de calzado",
        "fr": "Fabrication de chaussures",
        "it": "Fabbricazione di calzature",
        "zh": "鞋类制造",
    },
    "Wäscherei und chemische Reinigung": {
        "de": "Wäscherei und chemische Reinigung",
        "en": "Washing and (dry-)cleaning of textile and fur products",
        "es": "Lavado y limpieza de prendas textiles y de piel",
        "fr": "Blanchisserie-teinturerie",
        "it": "Lavanderia e pulitura a secco",
        "zh": "洗衣及干洗",
    },
}

SITE_TYPE_LABELS: dict[str, dict[str, str]] = {
    "Unternehmenssitz / Hauptverwaltung (einschließlich satzungsmäßigem Sitz, Hauptniederlassung und Verwaltungssitz)": {
        "de": "Unternehmenssitz / Hauptverwaltung (einschließlich satzungsmäßigem Sitz, Hauptniederlassung und Verwaltungssitz)",
        "en": "Registered office / head office (including registered seat, principal place of business and administrative seat)",
        "es": "Domicilio social / administración central (incluidos el domicilio estatutario, el establecimiento principal y la sede administrativa)",
        "fr": "Siège de l'entreprise / administration centrale (y compris siège statutaire, établissement principal et siège administratif)",
        "it": "Sede dell'impresa / amministrazione centrale (compresi sede legale, sede principale e sede amministrativa)",
        "zh": "公司住所 / 主行政管理机构（包括章程登记住所、主要营业地和管理住所）",
    },
    "Zweigniederlassung / Niederlassung (rechtlich oder organisatorisch verselbstständigte Niederlassungen)": {
        "de": "Zweigniederlassung / Niederlassung (rechtlich oder organisatorisch verselbstständigte Niederlassungen)",
        "en": "Branch / establishment (branches with legal or organisational autonomy)",
        "es": "Sucursal / establecimiento (sucursales con autonomía jurídica u organizativa)",
        "fr": "Succursale / établissement (établissements juridiquement ou organisationnellement autonomes)",
        "it": "Succursale / stabilimento (succursali giuridicamente o organizzativamente autonome)",
        "zh": "分支机构 / 营业机构（在法律上或组织上具有独立性的机构）",
    },
    "Produktionsstätte / Werk (Herstellung, Verarbeitung oder Veredelung)": {
        "de": "Produktionsstätte / Werk (Herstellung, Verarbeitung oder Veredelung)",
        "en": "Production site / plant (manufacturing, processing or finishing)",
        "es": "Planta de producción / fábrica (fabricación, transformación o acabado)",
        "fr": "Site de production / usine (fabrication, transformation ou ennoblissement)",
        "it": "Stabilimento produttivo / impianto (fabbricazione, trasformazione o nobilitazione)",
        "zh": "生产基地 / 工厂（生产、加工或整理）",
    },
    "Lager / Logistikzentrum (Lagerung, Versand oder Distribution)": {
        "de": "Lager / Logistikzentrum (Lagerung, Versand oder Distribution)",
        "en": "Warehouse / logistics centre (storage, dispatch or distribution)",
        "es": "Almacén / centro logístico (almacenamiento, expedición o distribución)",
        "fr": "Entrepôt / centre logistique (stockage, expédition ou distribution)",
        "it": "Magazzino / centro logistico (stoccaggio, spedizione o distribuzione)",
        "zh": "仓库 / 物流中心（仓储、发运或配送）",
    },
    "Vertriebsstandort / Verkaufsstelle (Vertriebsbüros, Showrooms, eigene Verkaufsstellen/Filialen)": {
        "de": "Vertriebsstandort / Verkaufsstelle (Vertriebsbüros, Showrooms, eigene Verkaufsstellen/Filialen)",
        "en": "Sales site / point of sale (sales offices, showrooms, own outlets/stores)",
        "es": "Emplazamiento de ventas / punto de venta (oficinas de ventas, showrooms, puntos de venta o tiendas propias)",
        "fr": "Site de vente / point de vente (bureaux commerciaux, showrooms, points de vente ou magasins propres)",
        "it": "Sede commerciale / punto vendita (uffici vendite, showroom, punti vendita o negozi propri)",
        "zh": "销售场所 / 销售点（销售办公室、展厅、自有销售点 / 门店）",
    },
    "Forschungs- und Entwicklungsstandort": {
        "de": "Forschungs- und Entwicklungsstandort",
        "en": "Research and development site",
        "es": "Emplazamiento de investigación y desarrollo",
        "fr": "Site de recherche et développement",
        "it": "Sede di ricerca e sviluppo",
        "zh": "研发场所",
    },
}

LOCATION_LABELS: dict[str, dict[str, str]] = {
    "Deutschland": {"de": "Deutschland", "en": "Germany", "es": "Alemania", "fr": "Allemagne", "it": "Germania", "zh": "德国"},
    "EU (ohne Deutschland)": {
        "de": "EU (ohne Deutschland)",
        "en": "EU (excl. Germany)",
        "es": "UE (sin Alemania)",
        "fr": "UE (hors Allemagne)",
        "it": "UE (escl. Germania)",
        "zh": "欧盟(不含德国)",
    },
    "Weltweit (außerhalb EU)": {
        "de": "Weltweit (außerhalb EU)",
        "en": "Worldwide (outside EU)",
        "es": "Mundial (fuera de la UE)",
        "fr": "Mondial (hors UE)",
        "it": "Globale (fuori UE)",
        "zh": "全球(欧盟以外)",
    },
}

LEGAL_FORM_LABELS: dict[str, dict[str, str]] = {
    "AG / SE": {"de": "AG / SE", "en": "AG / SE (stock corp.)", "es": "AG / SE (sociedad anónima)", "fr": "AG / SE (société anonyme)", "it": "AG / SE (società per azioni)", "zh": "AG / SE(股份公司)"},
    "GmbH": {"de": "GmbH", "en": "GmbH (limited liability)", "es": "GmbH (S.R.L.)", "fr": "GmbH (SARL)", "it": "GmbH (S.r.l.)", "zh": "GmbH(有限责任公司)"},
    "GmbH & Co. KG": {"de": "GmbH & Co. KG", "en": "GmbH & Co. KG", "es": "GmbH & Co. KG", "fr": "GmbH & Co. KG", "it": "GmbH & Co. KG", "zh": "GmbH & Co. KG"},
    "KG / OHG": {
        "de": "KG / OHG",
        "en": "KG / OHG (partnership)",
        "es": "KG / OHG (sociedad colectiva)",
        "fr": "KG / OHG (société en nom collectif)",
        "it": "KG / OHG (società in nome collettivo)",
        "zh": "KG / OHG(合伙企业)",
    },
    "Einzelunternehmen": {"de": "Einzelunternehmen", "en": "Sole proprietorship", "es": "Empresa unipersonal", "fr": "Entreprise individuelle", "it": "Ditta individuale", "zh": "个体经营"},
    "Genossenschaft": {"de": "Genossenschaft", "en": "Cooperative", "es": "Cooperativa", "fr": "Coopérative", "it": "Cooperativa", "zh": "合作社"},
    "Stiftung / Verein": {
        "de": "Stiftung / Verein",
        "en": "Foundation / Association",
        "es": "Fundación / Asociación",
        "fr": "Fondation / Association",
        "it": "Fondazione / Associazione",
        "zh": "基金会 / 协会",
    },
    "Limited / Ltd.": {"de": "Limited / Ltd.", "en": "Limited / Ltd.", "es": "Limited / Ltd.", "fr": "Limited / Ltd.", "it": "Limited / Ltd.", "zh": "Limited / Ltd."},
    "Sonstige": {"de": "Sonstige", "en": "Other", "es": "Otros", "fr": "Autre", "it": "Altro", "zh": "其他"},
}

GROUP_ROLE_LABELS: dict[str, dict[str, str]] = {
    "Eigenständig (kein Konzern)": {
        "de": "Eigenständig (kein Konzern)",
        "en": "Standalone (no group)",
        "es": "Independiente (sin grupo)",
        "fr": "Autonome (pas de groupe)",
        "it": "Autonoma (nessun gruppo)",
        "zh": "独立(非集团)",
    },
    "Mutterunternehmen mit Sitz in EU": {
        "de": "Mutterunternehmen mit Sitz in EU",
        "en": "Parent company based in EU",
        "es": "Empresa matriz con sede en la UE",
        "fr": "Société mère basée dans l'UE",
        "it": "Capogruppo con sede nell'UE",
        "zh": "总部位于欧盟的母公司",
    },
    "Mutterunternehmen mit Sitz außerhalb EU": {
        "de": "Mutterunternehmen mit Sitz außerhalb EU",
        "en": "Parent company based outside EU",
        "es": "Empresa matriz con sede fuera de la UE",
        "fr": "Société mère basée hors UE",
        "it": "Capogruppo con sede fuori dall'UE",
        "zh": "总部位于欧盟外的母公司",
    },
    "Tochter, EU-Muttergesellschaft": {
        "de": "Tochter, EU-Muttergesellschaft",
        "en": "Subsidiary, EU parent",
        "es": "Filial, matriz de la UE",
        "fr": "Filiale, mère UE",
        "it": "Controllata, capogruppo UE",
        "zh": "子公司,欧盟母公司",
    },
    "Tochter, Nicht-EU-Muttergesellschaft": {
        "de": "Tochter, Nicht-EU-Muttergesellschaft",
        "en": "Subsidiary, non-EU parent",
        "es": "Filial, matriz fuera de la UE",
        "fr": "Filiale, mère hors UE",
        "it": "Controllata, capogruppo non UE",
        "zh": "子公司,非欧盟母公司",
    },
}

PRODUCT_CAT_LABELS: dict[str, dict[str, str]] = {
    "Textile Vor- und Zwischenprodukte – Fasern, Garne, Gewebe, Gestricke, Vliesstoffe": {
        "de": "Textile Vor- und Zwischenprodukte – Fasern, Garne, Gewebe, Gestricke, Vliesstoffe",
        "en": "Textile intermediates – fibres, yarns, woven and knitted fabrics, non-wovens",
        "es": "Productos textiles intermedios: fibras, hilados, tejidos, géneros de punto, telas no tejidas",
        "fr": "Produits textiles intermédiaires – fibres, fils, tissus, étoffes à mailles, non-tissés",
        "it": "Semilavorati tessili – fibre, filati, tessuti, maglieria, tessuti non tessuti",
        "zh": "纺织中间产品——纤维、约线、机织物、针织物、非织造布",
    },
    "Bekleidung und Bekleidungszubehör": {
        "de": "Bekleidung und Bekleidungszubehör",
        "en": "Clothing and clothing accessories",
        "es": "Prendas de vestir y complementos",
        "fr": "Vêtements et accessoires d'habillement",
        "it": "Abbigliamento e accessori di abbigliamento",
        "zh": "服装及服饰配件",
    },
    "Schuhe": {
        "de": "Schuhe",
        "en": "Footwear",
        "es": "Calzado",
        "fr": "Chaussures",
        "it": "Calzature",
        "zh": "鞋类",
    },
    "Lederwaren und Accessoires": {
        "de": "Lederwaren und Accessoires",
        "en": "Leather goods and accessories",
        "es": "Marroquinería y accesorios",
        "fr": "Maroquinerie et accessoires",
        "it": "Pelletteria e accessori",
        "zh": "皮革制品及配饰",
    },
    "Heim- und Haustextilien": {
        "de": "Heim- und Haustextilien",
        "en": "Home and household textiles",
        "es": "Textiles del hogar y para el hogar",
        "fr": "Textiles de maison et d'ameublement",
        "it": "Tessili per la casa e per l'arredamento",
        "zh": "家用及家居纺织品",
    },
    "Schutztextilien / PSA": {
        "de": "Schutztextilien / PSA",
        "en": "Protective textiles / PPE",
        "es": "Textiles de protección / EPI",
        "fr": "Textiles de protection / EPI",
        "it": "Tessili protettivi / DPI",
        "zh": "防护纺织品 / 个人防护装备",
    },
    "Medizin- und Gesundheitstextilien": {
        "de": "Medizin- und Gesundheitstextilien",
        "en": "Medical and healthcare textiles",
        "es": "Textiles médicos y sanitarios",
        "fr": "Textiles médicaux et de santé",
        "it": "Tessili medicali e sanitari",
        "zh": "医疗与卫生用纺织品",
    },
    "Mobilitäts- und Transporttextilien – Automotive, Luft- und Raumfahrt, Bahn, Schifffahrt": {
        "de": "Mobilitäts- und Transporttextilien – Automotive, Luft- und Raumfahrt, Bahn, Schifffahrt",
        "en": "Mobility and transport textiles – automotive, aerospace, rail, shipping",
        "es": "Textiles para movilidad y transporte: automoción, aeroespacial, ferrocarril, náutica",
        "fr": "Textiles pour la mobilité et le transport – automobile, aéronautique, ferroviaire, maritime",
        "it": "Tessili per mobilità e trasporti – automotive, aerospazio, ferrovia, navale",
        "zh": "交通运输用纺织品——汽车、航空航天、轨道交通、船舶",
    },
    "Industrie- und Filtertextilien – Filter, Förderbänder, technische Gewebe, textile Maschinenkomponenten": {
        "de": "Industrie- und Filtertextilien – Filter, Förderbänder, technische Gewebe, textile Maschinenkomponenten",
        "en": "Industrial and filtration textiles – filters, conveyor belts, technical fabrics, textile machine components",
        "es": "Textiles industriales y de filtración: filtros, cintas transportadoras, tejidos técnicos, componentes textiles de maquinaria",
        "fr": "Textiles industriels et de filtration – filtres, bandes transporteuses, tissus techniques, composants textiles de machines",
        "it": "Tessili industriali e per filtrazione – filtri, nastri trasportatori, tessuti tecnici, componenti tessili per macchine",
        "zh": "工业与过滤用纺织品——过滤材料、输送带、技术织物、纺织机械部件",
    },
    "Bau- und Geotextilien – Bautextilien, Membranen, Gewebe für Erd-/Straßenbau": {
        "de": "Bau- und Geotextilien – Bautextilien, Membranen, Gewebe für Erd-/Straßenbau",
        "en": "Construction and geotextiles – building textiles, membranes, fabrics for earthworks and road construction",
        "es": "Textiles para construcción y geotextiles: textiles de obra, membranas, tejidos para obras de tierra y carreteras",
        "fr": "Textiles de construction et géotextiles – textiles du bâtiment, membranes, tissus pour terrassement et voirie",
        "it": "Tessili per l'edilizia e geotessili – tessili da costruzione, membrane, tessuti per movimento terra e strade",
        "zh": "建筑与土工用纺织品——建筑织物、膜材、土方及道路工程织物",
    },
    "Agrartextilien – Netze, Vliese, Abdeckungen etc.": {
        "de": "Agrartextilien – Netze, Vliese, Abdeckungen etc.",
        "en": "Agricultural textiles – nets, fleeces, covers etc.",
        "es": "Textiles agrícolas: redes, velos, cubiertas, etc.",
        "fr": "Textiles agricoles – filets, voiles, bâches, etc.",
        "it": "Tessili per l'agricoltura – reti, teli, coperture ecc.",
        "zh": "农用纺织品——网具、无纺布、覆盖物等",
    },
    "Sport- und Freizeittextilien": {
        "de": "Sport- und Freizeittextilien",
        "en": "Sports and leisure textiles",
        "es": "Textiles deportivos y de ocio",
        "fr": "Textiles de sport et de loisirs",
        "it": "Tessili per sport e tempo libero",
        "zh": "运动与休闲用纺织品",
    },
    "Sonstige technische Textilien": {
        "de": "Sonstige technische Textilien",
        "en": "Other technical textiles",
        "es": "Otros textiles técnicos",
        "fr": "Autres textiles techniques",
        "it": "Altri tessili tecnici",
        "zh": "其他技术用纺织品",
    },
}


ROLE_LABELS: dict[str, dict[str, str]] = {
    "Hersteller (stellt Produkte selbst her oder lässt sie herstellen und vermarktet sie unter eigenem Namen/eigener Marke)": {
        "de": "Hersteller (stellt Produkte selbst her oder lässt sie herstellen und vermarktet sie unter eigenem Namen/eigener Marke)",
        "en": "Manufacturer (makes products itself or has them made and markets them under its own name/brand)",
        "es": "Fabricante (fabrica los productos o los manda fabricar y los comercializa con su propio nombre o marca)",
        "fr": "Fabricant (fabrique les produits ou les fait fabriquer et les commercialise sous son propre nom/sa propre marque)",
        "it": "Fabbricante (produce i prodotti o li fa produrre e li commercializza con il proprio nome/marchio)",
        "zh": "制造商（自行生产或委托生产，并以自有名称/品牌销售）",
    },
    "Importeur (bringt Produkte aus einem Drittstaat auf den EU-Markt)": {
        "de": "Importeur (bringt Produkte aus einem Drittstaat auf den EU-Markt)",
        "en": "Importer (places products from a third country on the EU market)",
        "es": "Importador (introduce en el mercado de la UE productos procedentes de un tercer país)",
        "fr": "Importateur (met sur le marché de l'UE des produits provenant d'un pays tiers)",
        "it": "Importatore (immette sul mercato UE prodotti provenienti da un paese terzo)",
        "zh": "进口商（将第三国产品投放欧盟市场）",
    },
    "Händler/Vertreiber (stellt Produkte anderer Unternehmen auf dem Markt bereit)": {
        "de": "Händler/Vertreiber (stellt Produkte anderer Unternehmen auf dem Markt bereit)",
        "en": "Distributor/retailer (makes other companies' products available on the market)",
        "es": "Distribuidor (comercializa en el mercado productos de otras empresas)",
        "fr": "Distributeur (met à disposition sur le marché des produits d'autres entreprises)",
        "it": "Distributore (mette a disposizione sul mercato prodotti di altre imprese)",
        "zh": "经销商/分销商（在市场上提供其他企业的产品）",
    },
    "Markeninhaber / Vertrieb unter eigener oder lizenzierter Marke": {
        "de": "Markeninhaber / Vertrieb unter eigener oder lizenzierter Marke",
        "en": "Brand owner / sales under own brand",
        "es": "Titular de la marca / venta bajo marca propia",
        "fr": "Titulaire de la marque / vente sous marque propre",
        "it": "Titolare del marchio / vendita a marchio proprio",
        "zh": "品牌所有者 / 以自有品牌销售",
    },
    "Zulieferer": {
        "de": "Zulieferer",
        "en": "Supplier",
        "es": "Proveedor",
        "fr": "Fournisseur",
        "it": "Fornitore",
        "zh": "供应商",
    },
}


MATERIAL_LABELS: dict[str, dict[str, str]] = {
    "Baumwolle": {
        "de": "Baumwolle",
        "en": "Cotton",
        "es": "Algodón",
        "fr": "Coton",
        "it": "Cotone",
        "zh": "棉",
    },
    "Sonstige pflanzliche Naturfasern (z. B. Flachs/Leinen, Hanf, Jute)": {
        "de": "Sonstige pflanzliche Naturfasern (z. B. Flachs/Leinen, Hanf, Jute)",
        "en": "Other plant-based natural fibres (e.g. flax/linen, hemp, jute)",
        "es": "Otras fibras naturales vegetales (p. ej. lino, cáñamo, yute)",
        "fr": "Autres fibres naturelles végétales (p. ex. lin, chanvre, jute)",
        "it": "Altre fibre naturali vegetali (p. es. lino, canapa, iuta)",
        "zh": "其他植物性天然纤维（如亚麻、大麻、黄麻）",
    },
    "Tierische Fasern (z. B. Wolle, Kaschmir, Mohair, Alpaka, Seide)": {
        "de": "Tierische Fasern (z. B. Wolle, Kaschmir, Mohair, Alpaka, Seide)",
        "en": "Animal fibres (e.g. wool, cashmere, mohair, alpaca, silk)",
        "es": "Fibras animales (p. ej. lana, cachemira, mohair, alpaca, seda)",
        "fr": "Fibres animales (p. ex. laine, cachemire, mohair, alpaga, soie)",
        "it": "Fibre animali (p. es. lana, cashmere, mohair, alpaca, seta)",
        "zh": "动物纤维（如羊毛、羊绒、马海毛、羊驼毛、蚕丝）",
    },
    "Zellulosebasierte Chemiefasern (z. B. Viskose, Modal, Lyocell)": {
        "de": "Zellulosebasierte Chemiefasern (z. B. Viskose, Modal, Lyocell)",
        "en": "Cellulose-based man-made fibres (e.g. viscose, modal, lyocell)",
        "es": "Fibras químicas de celulosa (p. ej. viscosa, modal, liocel)",
        "fr": "Fibres chimiques cellulosiques (p. ex. viscose, modal, lyocell)",
        "it": "Fibre chimiche cellulosiche (p. es. viscosa, modal, lyocell)",
        "zh": "纤维素基化学纤维（如粘胶、莫代尔、莱赛尔）",
    },
    "Synthetische Chemiefasern (z. B. Polyester, Polyamid, Polyacryl, Elastan)": {
        "de": "Synthetische Chemiefasern (z. B. Polyester, Polyamid, Polyacryl, Elastan)",
        "en": "Synthetic man-made fibres (e.g. polyester, polyamide, acrylic, elastane)",
        "es": "Fibras químicas sintéticas (p. ej. poliéster, poliamida, acrílico, elastano)",
        "fr": "Fibres chimiques synthétiques (p. ex. polyester, polyamide, acrylique, élasthanne)",
        "it": "Fibre chimiche sintetiche (p. es. poliestere, poliammide, acrilico, elastan)",
        "zh": "合成化学纤维（如涤纶、锦纶、腈纶、氨纶）",
    },
    "Leder / Rindererzeugnisse": {
        "de": "Leder / Rindererzeugnisse",
        "en": "Leather / cattle products",
        "es": "Cuero / productos bovinos",
        "fr": "Cuir / produits bovins",
        "it": "Pelle / prodotti bovini",
        "zh": "皮革 / 牛类产品",
    },
    "Naturkautschuk": {
        "de": "Naturkautschuk",
        "en": "Natural rubber",
        "es": "Caucho natural",
        "fr": "Caoutchouc naturel",
        "it": "Gomma naturale",
        "zh": "天然橡胶",
    },
    "Recyclingmaterialien": {
        "de": "Recyclingmaterialien",
        "en": "Recycled materials",
        "es": "Materiales reciclados",
        "fr": "Matériaux recyclés",
        "it": "Materiali riciclati",
        "zh": "再生材料",
    },
    "Sonstige Materialien": {
        "de": "Sonstige Materialien",
        "en": "Other materials",
        "es": "Otros materiales",
        "fr": "Autres matériaux",
        "it": "Altri materiali",
        "zh": "其他材料",
    },
    "Wasser-, öl- oder schmutzabweisende Ausrüstung": {
        "de": "Wasser-, öl- oder schmutzabweisende Ausrüstung",
        "en": "Water-, oil- or soil-repellent finish",
        "es": "Acabado hidrófugo, oleófugo o antisuciedad",
        "fr": "Apprêt déperlant, oléofuge ou antisalissure",
        "it": "Finissaggio idrorepellente, oleorepellente o antimacchia",
        "zh": "拒水、拒油或防污整理",
    },
    "Flammhemmende / flammwidrige Ausrüstung": {
        "de": "Flammhemmende / flammwidrige Ausrüstung",
        "en": "Flame-retardant finish",
        "es": "Acabado ignífugo / retardante de llama",
        "fr": "Apprêt ignifuge / retardateur de flamme",
        "it": "Finissaggio ignifugo / antifiamma",
        "zh": "阻燃整理",
    },
    "Antimikrobielle / biozide Ausrüstung": {
        "de": "Antimikrobielle / biozide Ausrüstung",
        "en": "Antimicrobial / biocidal finish",
        "es": "Acabado antimicrobiano / biocida",
        "fr": "Apprêt antimicrobien / biocide",
        "it": "Finissaggio antimicrobico / biocida",
        "zh": "抗菌 / 生物杀灭整理",
    },
    "PFAS-haltige Ausrüstung": {
        "de": "PFAS-haltige Ausrüstung",
        "en": "PFAS-containing finish",
        "es": "Acabado con PFAS",
        "fr": "Apprêt contenant des PFAS",
        "it": "Finissaggio contenente PFAS",
        "zh": "含 PFAS 的整理",
    },
    "Sonstige besondere chemische Ausrüstung": {
        "de": "Sonstige besondere chemische Ausrüstung",
        "en": "Other special chemical finish",
        "es": "Otro acabado químico especial",
        "fr": "Autre apprêt chimique particulier",
        "it": "Altro finissaggio chimico particolare",
        "zh": "其他特殊化学整理",
    },
    "Nicht bekannt / kann nicht ausgeschlossen werden": {
        "de": "Nicht bekannt / kann nicht ausgeschlossen werden",
        "en": "Not known / cannot be ruled out",
        "es": "No se conoce / no puede descartarse",
        "fr": "Non connu / ne peut être exclu",
        "it": "Non noto / non può essere escluso",
        "zh": "不清楚 / 无法排除",
    },
}


MATERIAL_GROUP_LABELS: dict[str, dict[str, str]] = {
    "Naturfasern": {
        "de": "Naturfasern",
        "en": "Natural fibres",
        "es": "Fibras naturales",
        "fr": "Fibres naturelles",
        "it": "Fibre naturali",
        "zh": "天然纤维",
    },
    "Chemiefasern": {
        "de": "Chemiefasern",
        "en": "Man-made fibres",
        "es": "Fibras químicas",
        "fr": "Fibres chimiques",
        "it": "Fibre chimiche",
        "zh": "化学纤维",
    },
    "Weitere Materialien": {
        "de": "Weitere Materialien",
        "en": "Other materials",
        "es": "Otros materiales",
        "fr": "Autres matériaux",
        "it": "Altri materiali",
        "zh": "其他材料",
    },
    "Chemische Ausrüstungen / Behandlungen": {
        "de": "Chemische Ausrüstungen / Behandlungen",
        "en": "Chemical finishes / treatments",
        "es": "Acabados / tratamientos químicos",
        "fr": "Apprêts / traitements chimiques",
        "it": "Finissaggi / trattamenti chimici",
        "zh": "化学整理 / 处理",
    },
}


SALES_MARKET_LABELS: dict[str, dict[str, str]] = {
    "Deutschland": {
        "de": "Deutschland", "en": "Germany", "es": "Alemania",
        "fr": "Allemagne", "it": "Germania", "zh": "德国",
    },
    "Frankreich": {
        "de": "Frankreich", "en": "France", "es": "Francia",
        "fr": "France", "it": "Francia", "zh": "法国",
    },
    "Niederlande": {
        "de": "Niederlande", "en": "Netherlands", "es": "Países Bajos",
        "fr": "Pays-Bas", "it": "Paesi Bassi", "zh": "荷兰",
    },
    "andere EU-/EWR-Staaten": {
        "de": "andere EU-/EWR-Staaten",
        "en": "other EU/EEA states",
        "es": "otros Estados de la UE/EEE",
        "fr": "autres États de l'UE/EEE",
        "it": "altri Stati UE/SEE",
        "zh": "其他欧盟/欧洲经济区国家",
    },
    "außerhalb EU/EWR": {
        "de": "außerhalb EU/EWR",
        "en": "outside the EU/EEA",
        "es": "fuera de la UE/EEE",
        "fr": "hors UE/EEE",
        "it": "fuori dall'UE/SEE",
        "zh": "欧盟/欧洲经济区以外",
    },
}

# Einfachauswahl SVHC (Key = DE-Wert, DB-kompatibel), siehe regulations.SVHC_OPTIONS.
# Nur „Kein Mitglied“ wird uebersetzt; die Verbandsnamen sind Eigennamen
# und bleiben in jeder Sprache wie auf textil-mode.de. `t_opt` faellt fuer
# jeden nicht genannten Wert auf den Wert selbst zurueck.
ASSOCIATION_LABELS: dict[str, dict[str, str]] = {
    "Kein Mitglied": {
        "de": "Kein Mitglied",
        "en": "Not a member",
        "es": "No es miembro",
        "fr": "Non-membre",
        "it": "Non è membro",
        "zh": "非会员",
    },
}

SVHC_LABELS: dict[str, dict[str, str]] = {
    "Nicht bekannt": {
        "de": "Nicht bekannt", "en": "Not known", "es": "No se sabe",
        "fr": "Pas connu", "it": "Non noto", "zh": "不清楚",
    },
    "Ja": {"de": "Ja", "en": "Yes", "es": "Sí", "fr": "Oui", "it": "Sì", "zh": "是"},
    "Nein": {"de": "Nein", "en": "No", "es": "No", "fr": "Non", "it": "No", "zh": "否"},
}


# ---------- Ausfuellhilfen / Erlaeuterungen zu Fachbegriffen ----------
#
# Eigene Struktur neben `UI`, weil diese Texte laenger sind und eine andere
# Aufgabe haben: sie erklaeren einen Begriff, statt eine Oberflaeche zu
# beschriften. Der Schluessel ist kurz und feldbezogen; ausgegeben werden sie
# ueber `t_help()`.
#
# Fachliche Leitplanken (bewusst so formuliert):
#   - keine Rechtsberatung, keine erfundenen Pflichten;
#   - wo eine Norm gemeint ist, wird sie genannt, der Satz bleibt aber auch
#     ohne Kenntnis der Norm verstaendlich;
#   - wo die Gesetze unterschiedlich zaehlen (Beschaeftigte), sagt der Text das
#     und raet zur hoeheren Angabe, statt eine Scheinregel zu erfinden.
FIELD_HELP: dict[str, dict[str, str]] = {
    # Neue Felder vom 29.09.2026 — Texte von Claude formuliert, Freigabe durch
    # den Nutzer steht aus (anders als die woertlichen Vorgaben vom 15.09.2026).
    "energy_gwh": {
        "de": "Geben Sie den Gesamtendenergieverbrauch Ihres Unternehmens in Deutschland an, als Durchschnitt der letzten drei abgeschlossenen Kalenderjahre in Gigawattstunden (1 GWh = 1.000.000 kWh). Gemeint sind alle Energieträger zusammen, etwa Strom, Erdgas, Heizöl und Fernwärme. An diesen Wert knüpft das Energieeffizienzgesetz an (§§ 8 und 9 EnEfG). Die Zahlen finden Sie in Ihren Energieabrechnungen oder in Ihrem Energieaudit.",
        "en": "Enter your company's total final energy consumption in Germany as the average of the last three completed calendar years, in gigawatt hours (1 GWh = 1,000,000 kWh). This covers all energy sources together, such as electricity, natural gas, heating oil and district heating. The German Energy Efficiency Act refers to this figure (Sections 8 and 9 EnEfG). You will find the figures in your energy bills or your energy audit.",
        "es": "Indique el consumo total de energía final de su empresa en Alemania como media de los tres últimos años naturales cerrados, en gigavatios hora (1 GWh = 1.000.000 kWh). Se incluyen todas las fuentes de energía en conjunto, como electricidad, gas natural, gasóleo de calefacción y calefacción urbana. La Ley alemana de eficiencia energética se basa en este valor (arts. 8 y 9 EnEfG). Encontrará las cifras en sus facturas de energía o en su auditoría energética.",
        "fr": "Indiquez la consommation totale d'énergie finale de votre entreprise en Allemagne, en moyenne des trois dernières années civiles clôturées, en gigawattheures (1 GWh = 1 000 000 kWh). Sont visées toutes les sources d'énergie confondues, par exemple l'électricité, le gaz naturel, le fioul et le chauffage urbain. La loi allemande sur l'efficacité énergétique se réfère à cette valeur (§§ 8 et 9 EnEfG). Vous trouverez les chiffres dans vos factures d'énergie ou dans votre audit énergétique.",
        "it": "Indichi il consumo totale di energia finale della sua azienda in Germania come media degli ultimi tre anni civili conclusi, in gigawattora (1 GWh = 1.000.000 kWh). Sono comprese tutte le fonti di energia insieme, ad esempio elettricità, gas naturale, gasolio da riscaldamento e teleriscaldamento. La legge tedesca sull'efficienza energetica fa riferimento a questo valore (§§ 8 e 9 EnEfG). Trova i dati nelle bollette energetiche o nel suo audit energetico.",
        "zh": "请填写贵公司在德国的最终能源总消耗量，按最近三个已结束日历年的平均值计算，单位为吉瓦时（1 GWh = 1,000,000 kWh）。包括所有能源载体，例如电力、天然气、取暖油和区域供热。德国《能源效率法》以该数值为依据（《能源效率法》第 8 条和第 9 条）。相关数据可在能源账单或能源审计报告中查到。",
    },
    "wet_processing": {
        "de": "Setzen Sie den Haken, wenn an einem Standort Ihres Unternehmens in Deutschland bei der Herstellung oder Veredlung von Textilien Abwasser entsteht, z. B. beim Waschen, Bleichen, Färben, Bedrucken oder Ausrüsten. Dies gilt auch, wenn das Abwasser in die öffentliche Kanalisation eingeleitet wird. Für solches Abwasser können die Anforderungen des Anhangs 38 der Abwasserverordnung gelten. Gewerbliche Wäschereien werden gesondert geregelt.",
        "en": "Tick this box if wastewater is generated at one of your company's sites in Germany during the manufacture or finishing of textiles, e.g. during washing, bleaching, dyeing, printing or applying finishes. This also applies if the wastewater is discharged into the public sewer. The requirements of Annex 38 of the German Wastewater Ordinance may apply to such wastewater. Commercial laundries are regulated separately.",
        "es": "Marque la casilla si en una planta de su empresa en Alemania se generan aguas residuales durante la fabricación o el acabado de textiles, p. ej. al lavar, blanquear, teñir, estampar o aplicar aprestos. Esto se aplica también si las aguas residuales se vierten a la red pública de alcantarillado. A estas aguas residuales pueden aplicarse los requisitos del anexo 38 del Reglamento alemán de aguas residuales. Las lavanderías industriales se regulan por separado.",
        "fr": "Cochez la case si des eaux usées sont produites sur un site de votre entreprise en Allemagne lors de la fabrication ou de l'ennoblissement de textiles, par ex. lors du lavage, du blanchiment, de la teinture, de l'impression ou de l'apprêt. Cela vaut aussi lorsque les eaux usées sont déversées dans le réseau public d'assainissement. Ces eaux usées peuvent être soumises aux exigences de l'annexe 38 du règlement allemand sur les eaux usées. Les blanchisseries industrielles font l'objet d'une réglementation distincte.",
        "it": "Selezioni la casella se in uno stabilimento della Sua impresa in Germania si producono acque reflue durante la produzione o la nobilitazione di tessili, ad es. durante lavaggio, candeggio, tintura, stampa o finissaggio. Ciò vale anche se le acque reflue vengono immesse nella rete fognaria pubblica. A tali acque reflue possono applicarsi i requisiti dell'allegato 38 del regolamento tedesco sulle acque reflue. Le lavanderie industriali sono disciplinate separatamente.",
        "zh": "如果贵公司在德国的某个场所在生产或整理纺织品时产生废水（例如洗涤、漂白、染色、印花或后整理），请勾选此项。即使废水排入公共排水管网也适用。此类废水可能须符合德国《废水条例》附件 38 的要求。商业洗衣店另有专门规定。",
    },
    "svhc": {
        "de": "Die ECHA-Kandidatenliste enthält besonders besorgniserregende Stoffe (SVHC). Enthält ein Produkt oder ein einzelner Bestandteil – z. B. ein Knopf – einen solchen Stoff mit mehr als 0,1 Massenprozent, können Informations- und Meldepflichten bestehen. Wenn Sie es nicht wissen, wählen Sie „Nicht bekannt“ und fragen Sie bei Ihren Lieferanten nach.",
        "en": "The ECHA Candidate List contains substances of very high concern (SVHC). If a product or an individual component – e.g. a button – contains such a substance above 0.1% by weight, information and notification obligations may apply. If you do not know, select “Not known” and ask your suppliers.",
        "es": "La Lista de candidatas de la ECHA contiene sustancias extremadamente preocupantes (SVHC). Si un producto o un componente concreto – p. ej. un botón – contiene una de estas sustancias en más del 0,1 % en peso, pueden existir obligaciones de información y notificación. Si no lo sabe, seleccione «No se sabe» y consulte a sus proveedores.",
        "fr": "La liste des substances candidates de l'ECHA contient des substances extrêmement préoccupantes (SVHC). Si un produit ou un composant individuel – par ex. un bouton – contient une telle substance à plus de 0,1 % en masse, des obligations d'information et de déclaration peuvent s'appliquer. Si vous ne le savez pas, choisissez « Pas connu » et renseignez-vous auprès de vos fournisseurs.",
        "it": "L'elenco di sostanze candidate dell'ECHA contiene sostanze estremamente preoccupanti (SVHC). Se un prodotto o un singolo componente – ad es. un bottone – contiene una di queste sostanze in misura superiore allo 0,1% in peso, possono sussistere obblighi di informazione e di notifica. Se non lo sa, selezioni «Non noto» e chieda ai suoi fornitori.",
        "zh": "ECHA 候选清单收录高度关注物质（SVHC）。如果某件产品或其中单个组成部分（例如一粒纽扣）所含此类物质的质量分数超过 0.1%，可能须履行信息告知和申报义务。如不清楚，请选择“不清楚”，并向供应商询问。",
    },
    "employees_total": {
        "de": "Geben Sie die Gesamtzahl der Beschäftigten Ihres Unternehmens weltweit an. Bei Teilzeitbeschäftigten und Beschäftigten von Tochtergesellschaften können je nach Regulierung unterschiedliche Berechnungsregeln gelten. Sind Sie bei der Berechnung unsicher, geben Sie bitte die höhere Beschäftigtenzahl an. Der ESG-Regulierungs-Check dient der Erstorientierung; die jeweils maßgebliche Berechnung kann je nach Regulierung abweichen.",
        "en": "Enter the total number of your company's employees worldwide. For part-time employees and for employees of subsidiaries, different calculation rules may apply depending on the regulation. If you are unsure how to calculate the figure, please enter the higher number of employees. The ESG Regulation Check provides an initial orientation; the calculation that actually applies may differ from one regulation to another.",
        "es": "Indique el número total de empleados de su empresa en todo el mundo. En el caso de los empleados a tiempo parcial y de los empleados de filiales pueden aplicarse reglas de cálculo distintas según la regulación. Si no está seguro del cálculo, indique la cifra de empleados más alta. El chequeo regulatorio ESG ofrece una primera orientación; el cálculo determinante puede variar según la regulación.",
        "fr": "Indiquez le nombre total de salariés de votre entreprise dans le monde. Pour les salariés à temps partiel et pour les salariés des filiales, des règles de calcul différentes peuvent s'appliquer selon la réglementation. Si vous n'êtes pas sûr du calcul, indiquez le nombre de salariés le plus élevé. Le check réglementaire ESG sert de première orientation ; le calcul déterminant peut varier d'une réglementation à l'autre.",
        "it": "Indichi il numero complessivo dei dipendenti della sua azienda a livello mondiale. Per i dipendenti a tempo parziale e per i dipendenti delle società controllate possono valere regole di calcolo diverse a seconda della normativa. Se non è sicuro del calcolo, indichi il numero di dipendenti più alto. Il check normativo ESG offre un primo orientamento; il calcolo determinante può variare a seconda della normativa.",
        "zh": "请填写贵公司在全球范围内的员工总数。对于兼职员工以及子公司员工，不同法规可能适用不同的计算规则。如对计算方式不确定，请填写较高的员工人数。ESG 法规检查仅用于初步定位；各项法规实际适用的计算方式可能有所不同。",
    },
    "employees_de": {
        "de": "Geben Sie die Zahl der Beschäftigten an, die in Deutschland tätig sind. Ins Ausland entsandte Beschäftigte zählen grundsätzlich mit. Für die Prüfung nach dem Lieferkettengesetz gelten Besonderheiten: Leiharbeitskräfte werden bei einer Einsatzdauer von mehr als sechs Monaten berücksichtigt. Bei Konzernmuttergesellschaften werden außerdem die in Deutschland beschäftigten Arbeitnehmer der konzernangehörigen Gesellschaften einbezogen (§ 1 Abs. 3 LkSG).",
        "en": "Enter the number of employees working in Germany. Employees posted abroad are generally included. Special rules apply to the assessment under the German Supply Chain Act: temporary agency workers are counted where the assignment lasts more than six months. For group parent companies, the employees working in Germany at group companies are also included (Section 1(3) LkSG).",
        "es": "Indique el número de empleados que trabajan en Alemania. Los empleados desplazados al extranjero se computan por regla general. Para la comprobación conforme a la Ley alemana de cadenas de suministro rigen particularidades: los trabajadores cedidos por empresas de trabajo temporal se computan cuando el periodo de servicio supera los seis meses. En las sociedades matrices de un grupo se incluyen además los trabajadores empleados en Alemania por las sociedades del grupo (art. 1, apdo. 3, LkSG).",
        "fr": "Indiquez le nombre de salariés exerçant en Allemagne. Les salariés détachés à l'étranger sont en principe pris en compte. Des particularités s'appliquent à l'examen au titre de la loi allemande sur le devoir de vigilance : les travailleurs intérimaires sont pris en compte lorsque leur mission dépasse six mois. Pour les sociétés mères d'un groupe, les salariés employés en Allemagne par les sociétés du groupe sont en outre inclus (§ 1, al. 3, LkSG).",
        "it": "Indichi il numero di dipendenti che operano in Germania. I dipendenti distaccati all'estero sono di norma inclusi. Per la verifica ai sensi della legge tedesca sulle catene di fornitura valgono regole particolari: i lavoratori somministrati sono considerati se l'impiego supera i sei mesi. Nelle società capogruppo sono inoltre inclusi i lavoratori occupati in Germania dalle società del gruppo (§ 1, comma 3, LkSG).",
        "zh": "请填写在德国工作的员工人数。外派至境外的员工原则上计入。依据德国供应链法进行审查时另有特殊规定：派遣员工在派驻期超过六个月时计入。对于集团母公司，还需计入集团所属公司在德国雇用的员工（《供应链法》第 1 条第 3 款）。",
    },
    "revenue": {
        "de": "Geben Sie den Nettoumsatz Ihres Unternehmens weltweit aus dem letzten abgeschlossenen Geschäftsjahr an. Gemeint sind die Umsatzerlöse aus dem Verkauf von Waren und Dienstleistungen ohne Umsatzsteuer sowie abzüglich Rabatten und Retouren. Bei einer Muttergesellschaft kann für bestimmte Regulierungen, insbesondere die CSRD, der konsolidierte Nettoumsatz der gesamten Unternehmensgruppe maßgeblich sein.",
        "en": "Enter your company's worldwide net turnover for the last completed financial year. This means the revenue from the sale of goods and services excluding VAT and after deducting discounts and returns. For a parent company, certain regulations — the CSRD in particular — may look at the consolidated net turnover of the entire group.",
        "es": "Indique la cifra neta de negocios mundial de su empresa correspondiente al último ejercicio cerrado. Se entienden los ingresos por la venta de bienes y servicios sin IVA y una vez deducidos descuentos y devoluciones. En el caso de una sociedad matriz, para determinadas regulaciones, en particular la CSRD, puede ser determinante la cifra neta de negocios consolidada de todo el grupo.",
        "fr": "Indiquez le chiffre d'affaires net mondial de votre entreprise pour le dernier exercice clos. Il s'agit des produits tirés de la vente de biens et de services, hors TVA et après déduction des remises et des retours. Pour une société mère, certaines réglementations, en particulier la CSRD, peuvent retenir le chiffre d'affaires net consolidé de l'ensemble du groupe.",
        "it": "Indichi il fatturato netto mondiale della sua azienda relativo all'ultimo esercizio chiuso. Si intendono i ricavi dalla vendita di beni e servizi al netto dell'IVA e previa deduzione di sconti e resi. Per una società madre, per determinate normative, in particolare la CSRD, può essere determinante il fatturato netto consolidato dell'intero gruppo.",
        "zh": "请填写贵公司最近一个已结束会计年度的全球净营业额。指销售商品和提供服务所得的收入，不含增值税，并已扣除折扣和退货。对于母公司而言，某些法规（尤其是 CSRD）可能以整个企业集团的合并净营业额为准。",
    },
    "revenue_eu": {
        "de": "Geben Sie den Nettoumsatz an, den Ihr Unternehmen in der EU erzielt hat. Für bestimmte Regulierungen, insbesondere die CSRD bei Unternehmen mit Sitz außerhalb der EU, ist der EU-Umsatz der letzten zwei aufeinanderfolgenden Geschäftsjahre relevant. Bei Unternehmensgruppen kann der in der EU erzielte Umsatz der gesamten Gruppe maßgeblich sein. Erzielen Sie Ihren gesamten Umsatz in der EU, entspricht der Wert dem weltweiten Nettoumsatz.",
        "en": "Enter the net turnover your company generated in the EU. For certain regulations — in particular the CSRD for companies established outside the EU — the EU turnover of the last two consecutive financial years is relevant. For groups, the turnover generated in the EU by the entire group may be decisive. If you generate all of your turnover in the EU, this figure equals the worldwide net turnover.",
        "es": "Indique la cifra neta de negocios que su empresa ha obtenido en la UE. Para determinadas regulaciones, en particular la CSRD en el caso de empresas con domicilio fuera de la UE, es relevante la cifra de negocios en la UE de los dos últimos ejercicios consecutivos. En los grupos puede ser determinante la cifra de negocios obtenida en la UE por todo el grupo. Si obtiene la totalidad de su cifra de negocios en la UE, el valor coincide con la cifra neta de negocios mundial.",
        "fr": "Indiquez le chiffre d'affaires net réalisé par votre entreprise dans l'UE. Pour certaines réglementations, en particulier la CSRD pour les entreprises établies hors de l'UE, le chiffre d'affaires réalisé dans l'UE au cours des deux derniers exercices consécutifs est pertinent. Pour les groupes, le chiffre d'affaires réalisé dans l'UE par l'ensemble du groupe peut être déterminant. Si vous réalisez la totalité de votre chiffre d'affaires dans l'UE, la valeur correspond au chiffre d'affaires net mondial.",
        "it": "Indichi il fatturato netto realizzato dalla sua azienda nell'UE. Per determinate normative, in particolare la CSRD per le imprese con sede fuori dall'UE, rileva il fatturato UE degli ultimi due esercizi consecutivi. Nei gruppi può essere determinante il fatturato realizzato nell'UE dall'intero gruppo. Se realizza l'intero fatturato nell'UE, il valore corrisponde al fatturato netto mondiale.",
        "zh": "请填写贵公司在欧盟境内实现的净营业额。对于某些法规，尤其是针对设立在欧盟以外企业的 CSRD，相关的是最近连续两个会计年度的欧盟营业额。对于企业集团，可能以整个集团在欧盟实现的营业额为准。如果贵公司的全部营业额均在欧盟实现，则该数值与全球净营业额相同。",
    },
    "balance_sheet": {
        "de": "Geben Sie die Bilanzsumme Ihres Unternehmens zum Ende des letzten abgeschlossenen Geschäftsjahres an. Den Wert finden Sie in Ihrem Jahresabschluss. Bei Unternehmensgruppen kann je nach Regulierung die Bilanzsumme des Konzernabschlusses maßgeblich sein.",
        "en": "Enter your company's balance sheet total as at the end of the last completed financial year. You will find the figure in your annual financial statements. For groups, the balance sheet total of the consolidated financial statements may be decisive, depending on the regulation.",
        "es": "Indique el total del balance de su empresa al cierre del último ejercicio cerrado. Encontrará el valor en sus cuentas anuales. En los grupos puede ser determinante, según la regulación, el total del balance de las cuentas consolidadas.",
        "fr": "Indiquez le total du bilan de votre entreprise à la clôture du dernier exercice clos. Vous trouverez cette valeur dans vos comptes annuels. Pour les groupes, le total du bilan des comptes consolidés peut être déterminant selon la réglementation.",
        "it": "Indichi il totale di bilancio della sua azienda alla chiusura dell'ultimo esercizio concluso. Il valore è riportato nel bilancio d'esercizio. Nei gruppi può essere determinante, a seconda della normativa, il totale di bilancio del bilancio consolidato.",
        "zh": "请填写贵公司最近一个已结束会计年度末的资产负债表总额。该数值可在年度财务报表中查到。对于企业集团，视法规而定，可能以合并财务报表的资产负债表总额为准。",
    },
    "legal_form": {
        "de": "Wählen Sie die Rechtsform Ihres Unternehmens. Die Rechtsform kann neben Unternehmensgröße und weiteren Kriterien dafür relevant sein, ob bestimmte regulatorische Anforderungen für Ihr Unternehmen gelten.",
        "en": "Select your company's legal form. Alongside company size and further criteria, the legal form can determine whether certain regulatory requirements apply to your company.",
        "es": "Seleccione la forma jurídica de su empresa. Junto al tamaño de la empresa y otros criterios, la forma jurídica puede ser relevante para determinar si a su empresa le aplican determinadas exigencias regulatorias.",
        "fr": "Sélectionnez la forme juridique de votre entreprise. Outre la taille de l'entreprise et d'autres critères, la forme juridique peut déterminer si certaines exigences réglementaires s'appliquent à votre entreprise.",
        "it": "Selezioni la forma giuridica della sua azienda. Oltre alle dimensioni dell'impresa e ad altri criteri, la forma giuridica può essere rilevante per stabilire se determinati requisiti normativi si applichino alla sua azienda.",
        "zh": "请选择贵公司的法律形式。除企业规模和其他标准外，法律形式也可能影响某些监管要求是否适用于贵公司。",
    },
    "branch": {
        "de": "Wählen Sie die Branche aus, die der Haupttätigkeit Ihres Unternehmens entspricht. Die Auswahl orientiert sich an der europäischen Wirtschaftszweigklassifikation NACE. Weitere Tätigkeiten Ihres Unternehmens können über die Produktkategorien und Rollen berücksichtigt werden.",
        "en": "Select the sector that corresponds to your company's main activity. The list follows the European statistical classification of economic activities, NACE. Further activities of your company can be captured through the product categories and the roles.",
        "es": "Seleccione el sector que corresponde a la actividad principal de su empresa. La selección se orienta por la clasificación europea de actividades económicas NACE. Otras actividades de su empresa pueden recogerse a través de las categorías de productos y de los roles.",
        "fr": "Sélectionnez le secteur correspondant à l'activité principale de votre entreprise. La liste s'appuie sur la nomenclature européenne des activités économiques NACE. Les autres activités de votre entreprise peuvent être prises en compte via les catégories de produits et les rôles.",
        "it": "Selezioni il settore corrispondente all'attività principale della sua azienda. L'elenco si basa sulla classificazione europea delle attività economiche NACE. Ulteriori attività della sua azienda possono essere considerate tramite le categorie di prodotto e i ruoli.",
        "zh": "请选择与贵公司主营业务相对应的行业。选项以欧盟经济活动分类 NACE 为依据。贵公司的其他经营活动可通过产品类别和角色加以体现。",
    },
    "group_role": {
        "de": "Geben Sie an, ob Ihr Unternehmen eigenständig oder Teil einer Unternehmensgruppe ist und ob es sich um eine Mutter- oder Tochtergesellschaft handelt. Bei Tochtergesellschaften ist zusätzlich relevant, ob die Muttergesellschaft innerhalb oder außerhalb der EU ansässig ist. Diese Angaben werden benötigt, da einige Regulierungen Schwellenwerte auf Ebene der Unternehmensgruppe berücksichtigen oder für Drittlandsunternehmen besondere Regelungen vorsehen.",
        "en": "State whether your company is independent or part of a group and whether it is a parent or a subsidiary. For subsidiaries it also matters whether the parent company is established inside or outside the EU. This information is needed because some regulations apply thresholds at group level or provide special rules for third-country companies.",
        "es": "Indique si su empresa es independiente o forma parte de un grupo y si se trata de una sociedad matriz o de una filial. En el caso de las filiales también es relevante si la sociedad matriz está domiciliada dentro o fuera de la UE. Estos datos son necesarios porque algunas regulaciones aplican umbrales a nivel de grupo o prevén reglas especiales para empresas de terceros países.",
        "fr": "Indiquez si votre entreprise est autonome ou fait partie d'un groupe et s'il s'agit d'une société mère ou d'une filiale. Pour les filiales, il importe également de savoir si la société mère est établie dans l'UE ou en dehors. Ces informations sont nécessaires car certaines réglementations appliquent des seuils au niveau du groupe ou prévoient des règles particulières pour les entreprises de pays tiers.",
        "it": "Indichi se la sua azienda è autonoma o fa parte di un gruppo e se si tratta di una società madre o di una controllata. Per le controllate rileva inoltre se la società madre abbia sede all'interno o all'esterno dell'UE. Queste informazioni servono perché alcune normative considerano le soglie a livello di gruppo o prevedono regole particolari per le imprese di paesi terzi.",
        "zh": "请说明贵公司是独立企业还是企业集团的一部分，以及属于母公司还是子公司。对于子公司，还需说明母公司设立在欧盟境内还是境外。这些信息是必要的，因为部分法规在集团层面适用门槛值，或对第三国企业设有特别规定。",
    },
    "b2c": {
        "de": "Kreuzen Sie an, wenn Sie Waren an private Endverbraucher verkaufen — im eigenen Laden, im Online-Shop oder im Fernabsatz. Verkauf allein an Handel, Industrie oder öffentliche Auftraggeber ist kein B2C. Verbraucherbezogene Vorgaben wie die EmpCo-Richtlinie und das Recht auf Reparatur knüpfen hieran an.",
        "en": "Tick this if you sell goods to private end consumers — in your own shop, in an online shop or by distance selling. Selling only to retailers, industry or public purchasers is not B2C. Consumer-facing rules such as the EmpCo Directive and the right to repair attach to this.",
        "es": "Marque esta casilla si vende bienes a consumidores finales particulares, ya sea en tienda propia, en tienda en línea o a distancia. Vender únicamente a comercio, industria o entidades públicas no es B2C. Normas dirigidas al consumidor, como la Directiva EmpCo y el derecho a reparar, se vinculan a esto.",
        "fr": "Cochez si vous vendez des biens à des consommateurs finaux privés — en boutique, en boutique en ligne ou à distance. Vendre uniquement au commerce, à l'industrie ou à des acheteurs publics n'est pas du B2C. Des règles destinées aux consommateurs, comme la directive EmpCo et le droit à la réparation, s'y rattachent.",
        "it": "Selezioni la casella se vende beni a consumatori finali privati, in negozio proprio, in un negozio online o a distanza. Vendere solo a commercio, industria o committenti pubblici non è B2C. Regole rivolte ai consumatori, come la direttiva EmpCo e il diritto alla riparazione, si ricollegano a questo.",
        "zh": "如果贵公司向私人最终消费者销售商品——无论是自有门店、网店还是远程销售——请勾选此项。仅向贸易商、工业客户或公共采购方销售不属于 B2C。面向消费者的规定（如 EmpCo 指令和维修权）以此为连接点。",
    },
    "listed": {
        "de": "Kreuzen Sie an, wenn Ihr Unternehmen Wertpapiere – z. B. Aktien oder Anleihen – ausgegeben hat, die an einem organisierten Markt gehandelt werden oder deren Zulassung dort beantragt wurde (§ 264d HGB). Der Handel ausschließlich im Freiverkehr gilt nicht als Kapitalmarktorientierung in diesem Sinne.",
        "en": "Tick this box if your company has issued securities — shares or bonds, for example — that are traded on an organised market or for which admission to such a market has been applied for (Section 264d HGB). Trading exclusively in the open market does not count as capital-market orientation in this sense.",
        "es": "Marque esta casilla si su empresa ha emitido valores —por ejemplo acciones u obligaciones— que se negocian en un mercado organizado o cuya admisión a dicho mercado se ha solicitado (art. 264d HGB). La negociación exclusivamente en el mercado no organizado no se considera orientación al mercado de capitales en este sentido.",
        "fr": "Cochez cette case si votre entreprise a émis des valeurs mobilières – par exemple des actions ou des obligations – négociées sur un marché organisé ou dont l'admission à un tel marché a été demandée (§ 264d HGB). La négociation exclusivement sur le marché libre ne vaut pas orientation vers le marché des capitaux au sens du présent point.",
        "it": "Selezioni questa casella se la sua azienda ha emesso strumenti finanziari – per esempio azioni od obbligazioni – negoziati su un mercato organizzato o per i quali è stata richiesta l'ammissione a tale mercato (§ 264d HGB). La negoziazione esclusivamente sul mercato non regolamentato non costituisce orientamento al mercato dei capitali in questo senso.",
        "zh": "如果贵公司发行了在有组织市场交易、或已申请在该市场上市的有价证券（例如股票或债券），请勾选此项（《德国商法典》第 264d 条）。仅在场外自由交易市场交易的，不属于本项意义上的资本市场导向。",
    },
    "env_claims": {
        "de": "Kreuzen Sie an, wenn Ihr Unternehmen Umwelt- oder Nachhaltigkeitsaussagen in Werbung, auf Produkten oder Verpackungen verwendet – z. B. „klimaneutral“, „aus recyceltem Material“ oder „umweltfreundlich“ – oder eigene bzw. fremde Nachhaltigkeitssiegel nutzt. Hier geht es nur darum, ob solche Aussagen oder Siegel verwendet werden, nicht darum, ob sie rechtlich zulässig oder ausreichend belegt sind.",
        "en": "Tick this box if your company uses environmental or sustainability claims in advertising, on products or on packaging — such as “climate neutral”, “made from recycled material” or “environmentally friendly” — or uses sustainability labels of its own or of third parties. What matters here is only whether such claims or labels are used, not whether they are legally permissible or sufficiently substantiated.",
        "es": "Marque esta casilla si su empresa utiliza declaraciones medioambientales o de sostenibilidad en la publicidad, en los productos o en los envases —por ejemplo «climáticamente neutro», «de material reciclado» o «respetuoso con el medio ambiente»— o emplea distintivos de sostenibilidad propios o ajenos. Aquí solo se trata de si se utilizan tales declaraciones o distintivos, no de si son jurídicamente admisibles o están suficientemente justificados.",
        "fr": "Cochez cette case si votre entreprise utilise des allégations environnementales ou de durabilité dans la publicité, sur les produits ou sur les emballages – par exemple « neutre en carbone », « en matériau recyclé » ou « respectueux de l'environnement » – ou utilise des labels de durabilité propres ou de tiers. Il s'agit ici uniquement de savoir si de telles allégations ou de tels labels sont utilisés, non de savoir s'ils sont juridiquement admissibles ou suffisamment étayés.",
        "it": "Selezioni questa casella se la sua azienda utilizza asserzioni ambientali o di sostenibilità nella pubblicità, sui prodotti o sugli imballaggi – per esempio «neutrale dal punto di vista climatico», «in materiale riciclato» o «ecologico» – oppure impiega marchi di sostenibilità propri o di terzi. Qui rileva soltanto se tali asserzioni o marchi vengano utilizzati, non se siano giuridicamente ammissibili o sufficientemente comprovati.",
        "zh": "如果贵公司在广告、产品或包装上使用环境或可持续性声明——例如“气候中性”“采用再生材料”或“环境友好”——或使用自有或第三方的可持续性标识，请勾选此项。此处仅涉及是否使用此类声明或标识，而不涉及其在法律上是否被允许或是否有充分依据。",
    },
    "eu_importer": {
        "de": "Kreuzen Sie an, wenn Ihr Unternehmen Produkte aus einem Drittland in die EU einführt und diese erstmals auf dem EU-Markt bereitstellt. Das ist beispielsweise der Fall, wenn Sie Produkte in Asien fertigen lassen, selbst in die EU einführen und hier verkaufen oder abgeben. Beziehen Sie dagegen Waren, die bereits von einem anderen Unternehmen in die EU eingeführt und auf dem EU-Markt bereitgestellt wurden, sind Sie grundsätzlich nicht der Importeur.",
        "en": "Tick this box if your company imports products from a third country into the EU and makes them available on the EU market for the first time. That is the case, for example, if you have products made in Asia, import them into the EU yourself and sell or supply them here. If, by contrast, you source goods that another company has already imported into the EU and made available on the EU market, you are generally not the importer.",
        "es": "Marque esta casilla si su empresa importa productos de un tercer país a la UE y los comercializa por primera vez en el mercado de la UE. Es el caso, por ejemplo, si manda fabricar productos en Asia, los importa usted mismo a la UE y los vende o entrega aquí. Si, por el contrario, adquiere mercancías que otra empresa ya ha importado a la UE y comercializado en el mercado de la UE, por regla general usted no es el importador.",
        "fr": "Cochez cette case si votre entreprise importe des produits d'un pays tiers dans l'UE et les met pour la première fois à disposition sur le marché de l'UE. C'est par exemple le cas si vous faites fabriquer des produits en Asie, les importez vous-même dans l'UE et les vendez ou les remettez ici. En revanche, si vous vous procurez des marchandises déjà importées dans l'UE et mises à disposition sur le marché de l'UE par une autre entreprise, vous n'êtes en principe pas l'importateur.",
        "it": "Selezioni questa casella se la sua azienda importa prodotti da un paese terzo nell'UE e li mette per la prima volta a disposizione sul mercato UE. È il caso, per esempio, se fa produrre i prodotti in Asia, li importa personalmente nell'UE e li vende o li cede qui. Se invece acquista merci già importate nell'UE e messe a disposizione sul mercato UE da un'altra impresa, di norma non è lei l'importatore.",
        "zh": "如果贵公司将产品从第三国输入欧盟，并首次在欧盟市场上提供该产品，请勾选此项。例如：贵公司在亚洲委托生产，自行将产品输入欧盟并在此销售或交付。相反，如果贵公司采购的货物已由另一家企业输入欧盟并在欧盟市场上提供，则原则上贵公司不是进口商。",
    },
    "products": {
        "de": "Kreuzen Sie alle Produktkategorien an, die Ihr Unternehmen herstellt, einführt oder vertreibt – auch wenn sie nur einen kleinen Teil des Sortiments ausmachen. Produktbezogene regulatorische Anforderungen können für einzelne Warengruppen gelten, unabhängig vom Schwerpunkt Ihrer Geschäftstätigkeit.",
        "en": "Tick all product categories that your company manufactures, imports or distributes – even where they account for only a small part of the range. Product-related regulatory requirements can apply to individual product groups, irrespective of the main focus of your business activity.",
        "es": "Marque todas las categorías de productos que su empresa fabrica, importa o distribuye, aunque representen solo una pequeña parte del surtido. Las exigencias regulatorias relativas a los productos pueden aplicarse a grupos de mercancías concretos, con independencia del foco principal de su actividad empresarial.",
        "fr": "Cochez toutes les catégories de produits que votre entreprise fabrique, importe ou distribue – même si elles ne représentent qu'une petite part de l'assortiment. Les exigences réglementaires liées aux produits peuvent s'appliquer à des groupes de marchandises isolés, indépendamment de l'activité principale de votre entreprise.",
        "it": "Selezioni tutte le categorie di prodotto che la sua azienda produce, importa o distribuisce – anche se rappresentano solo una piccola parte dell'assortimento. I requisiti normativi relativi ai prodotti possono valere per singoli gruppi merceologici, indipendentemente dal fulcro della sua attività.",
        "zh": "请勾选贵公司生产、进口或销售的所有产品类别——即使其在产品组合中占比很小。与产品相关的监管要求可能针对个别品类适用，而与贵公司经营活动的重心无关。",
    },
    "roles": {
        "de": "Wählen Sie alle Rollen aus, die Ihr Unternehmen tatsächlich übernimmt. Mehrere Rollen können gleichzeitig zutreffen. Entscheidend ist die tatsächliche Tätigkeit Ihres Unternehmens – auch bei Lizenzmodellen. Die genaue rechtliche Einordnung als Hersteller, Importeur, Händler oder anderer Wirtschaftsakteur kann je nach Regulierung abweichen.",
        "en": "Select all roles that your company actually performs. Several roles can apply at the same time. What counts is the actual activity of your company – including under licensing models. The precise legal classification as manufacturer, importer, distributor or other economic operator may differ from one regulation to another.",
        "es": "Seleccione todos los roles que su empresa asume efectivamente. Pueden aplicarse varios roles a la vez. Lo determinante es la actividad real de su empresa, también en los modelos de licencia. La calificación jurídica exacta como fabricante, importador, distribuidor u otro agente económico puede variar según la regulación.",
        "fr": "Sélectionnez tous les rôles que votre entreprise assume effectivement. Plusieurs rôles peuvent s'appliquer simultanément. C'est l'activité réelle de votre entreprise qui est déterminante – y compris dans les modèles de licence. La qualification juridique exacte de fabricant, d'importateur, de distributeur ou d'autre opérateur économique peut varier selon la réglementation.",
        "it": "Selezioni tutti i ruoli che la sua azienda svolge effettivamente. Più ruoli possono valere contemporaneamente. È determinante l'attività effettiva della sua azienda – anche nei modelli di licenza. L'esatto inquadramento giuridico come fabbricante, importatore, distributore o altro operatore economico può variare a seconda della normativa.",
        "zh": "请选择贵公司实际承担的所有角色。可同时适用多个角色。关键在于贵公司的实际经营活动——在品牌授权模式下同样如此。作为制造商、进口商、经销商或其他经济经营者的确切法律定性，可能因法规而异。",
    },
    "materials": {
        "de": "Wählen Sie alle Materialien aus, die in Ihren Produkten enthalten sind – einschließlich Materialien in zugekauften Bestandteilen. Die Materialzusammensetzung kann für die Prüfung einzelner regulatorischer Anforderungen relevant sein. Ist Ihnen die Zusammensetzung bei Teilen Ihres Sortiments nicht bekannt, wählen Sie zusätzlich „Nicht bekannt / kann nicht ausgeschlossen werden“.",
        "en": "Select all materials contained in your products – including materials in bought-in components. The material composition can be relevant for assessing individual regulatory requirements. If you do not know the composition for parts of your range, additionally select “Not known / cannot be ruled out”.",
        "es": "Seleccione todos los materiales presentes en sus productos, incluidos los materiales de los componentes comprados. La composición material puede ser relevante para comprobar determinadas exigencias regulatorias. Si desconoce la composición en parte de su surtido, seleccione además «No se conoce / no puede descartarse».",
        "fr": "Sélectionnez tous les matériaux présents dans vos produits – y compris les matériaux contenus dans les composants achetés. La composition des matériaux peut être pertinente pour l'examen de certaines exigences réglementaires. Si vous ne connaissez pas la composition pour une partie de votre assortiment, sélectionnez également « Inconnu / ne peut pas être exclu ».",
        "it": "Selezioni tutti i materiali contenuti nei suoi prodotti – compresi i materiali dei componenti acquistati. La composizione dei materiali può essere rilevante per la verifica di singoli requisiti normativi. Se non conosce la composizione per una parte dell'assortimento, selezioni anche «Non noto / non può essere escluso».",
        "zh": "请选择贵公司产品中含有的所有材料——包括外购部件中的材料。材料构成可能与个别监管要求的审查相关。如果贵公司对部分产品的材料构成不了解，请同时选择“不清楚 / 无法排除”。",
    },
    "markets": {
        "de": "Wählen Sie aus, in welchen Märkten Ihr Unternehmen seine Produkte verkauft oder vertreibt – unabhängig davon, wo diese hergestellt werden. Die Absatzmärkte sind relevant, weil bestimmte regulatorische Anforderungen davon abhängen, ob Produkte in Deutschland, in anderen EU-/EWR-Staaten oder außerhalb der EU angeboten oder verkauft werden.",
        "en": "Select the markets in which your company sells or distributes its products – regardless of where they are manufactured. The sales markets are relevant because certain regulatory requirements depend on whether products are offered or sold in Germany, in other EU/EEA states or outside the EU.",
        "es": "Seleccione en qué mercados vende o distribuye su empresa sus productos, con independencia de dónde se fabriquen. Los mercados de venta son relevantes porque determinadas exigencias regulatorias dependen de si los productos se ofrecen o se venden en Alemania, en otros Estados de la UE/EEE o fuera de la UE.",
        "fr": "Sélectionnez les marchés sur lesquels votre entreprise vend ou distribue ses produits – indépendamment du lieu de fabrication. Les marchés de vente sont pertinents car certaines exigences réglementaires dépendent du fait que les produits soient proposés ou vendus en Allemagne, dans d'autres États de l'UE/EEE ou hors de l'UE.",
        "it": "Selezioni i mercati in cui la sua azienda vende o distribuisce i propri prodotti – indipendentemente dal luogo di produzione. I mercati di sbocco sono rilevanti perché determinati requisiti normativi dipendono dal fatto che i prodotti siano offerti o venduti in Germania, in altri Stati UE/SEE o fuori dall'UE.",
        "zh": "请选择贵公司在哪些市场销售或分销其产品——与产品的生产地无关。销售市场具有重要意义，因为某些监管要求取决于产品是在德国、其他欧盟 / 欧洲经济区国家还是在欧盟以外提供或销售。",
    },
    "sites": {
        "de": "Geben Sie an, welche Arten von Standorten Ihr Unternehmen unterhält, in welcher Region sie liegen und wie viele es jeweils sind. Die Standortart und der Standort können für die Prüfung einzelner regulatorischer Anforderungen relevant sein.",
        "en": "State what types of sites your company maintains, in which region they are located and how many there are of each. The type of site and its location can be relevant for assessing individual regulatory requirements.",
        "es": "Indique qué tipos de emplazamientos mantiene su empresa, en qué región se encuentran y cuántos hay de cada uno. El tipo de emplazamiento y su ubicación pueden ser relevantes para comprobar determinadas exigencias regulatorias.",
        "fr": "Indiquez quels types de sites votre entreprise exploite, dans quelle région ils se situent et combien il y en a de chaque. Le type de site et sa localisation peuvent être pertinents pour l'examen de certaines exigences réglementaires.",
        "it": "Indichi quali tipi di sedi la sua azienda mantiene, in quale regione si trovano e quante sono per ciascun tipo. Il tipo di sede e la sua ubicazione possono essere rilevanti per la verifica di singoli requisiti normativi.",
        "zh": "请说明贵公司设有哪些类型的经营场所、位于哪个地区以及各有多少处。场所类型及其所在地可能与个别监管要求的审查相关。",
    },
    "metric_yes": {
        "de": "Nach Ihren Angaben spricht alles dafür, dass diese Regulierung Ihr Unternehmen erfasst. Die Karte nennt die Fundstelle, den Anwendungsbeginn und erste Schritte. Eine rechtliche Prüfung des Einzelfalls ersetzt das nicht.",
        "en": "On the basis of your entries, everything points to this regulation covering your company. The card gives the source passage, the date of application and first steps. It does not replace a legal review of the individual case.",
        "es": "Según sus datos, todo apunta a que esta regulación afecta a su empresa. La tarjeta indica el pasaje de referencia, la fecha de aplicación y los primeros pasos. No sustituye a un examen jurídico del caso concreto.",
        "fr": "D'après vos indications, tout indique que cette réglementation s'applique à votre entreprise. La fiche indique le passage de référence, la date d'application et les premières étapes. Cela ne remplace pas un examen juridique du cas d'espèce.",
        "it": "In base ai suoi dati, tutto indica che questa normativa riguarda la sua azienda. La scheda riporta il passaggio di riferimento, la data di applicazione e i primi passi. Non sostituisce un esame giuridico del caso concreto.",
        "zh": "根据贵公司填写的信息，种种迹象表明该法规适用于贵公司。卡片中列出了依据条款、适用起始日期和首批行动步骤。这不能替代针对个案的法律审查。",
    },
    "metric_maybe": {
        "de": "Die Angaben reichen für eine eindeutige Antwort nicht aus, oder Ihr Unternehmen liegt nahe an einer Schwelle. Prüfen Sie diese Fälle zuerst — hier entscheidet sich, ob Aufwand entsteht. Oft genügt eine genauere Angabe im Formular.",
        "en": "Your entries are not enough for a clear answer, or your company is close to a threshold. Look at these cases first — this is where it is decided whether any effort arises. Often a more precise entry in the form is enough.",
        "es": "Los datos no bastan para una respuesta clara, o su empresa está cerca de un umbral. Revise primero estos casos: aquí se decide si surge carga de trabajo. A menudo basta con una indicación más precisa en el formulario.",
        "fr": "Vos indications ne suffisent pas pour une réponse claire, ou votre entreprise est proche d'un seuil. Examinez ces cas en premier : c'est là que se décide l'existence d'une charge. Souvent, une indication plus précise dans le formulaire suffit.",
        "it": "I dati non bastano per una risposta univoca, oppure la sua azienda è vicina a una soglia. Esamini prima questi casi: qui si decide se sorgono oneri. Spesso basta un'indicazione più precisa nel modulo.",
        "zh": "所填信息不足以给出明确结论，或贵公司接近某一门槛。请优先查看这些情形——是否产生工作量在此决定。通常在表单中填写得更精确即可澄清。",
    },
    "metric_no": {
        "de": "Nach Ihren Angaben greift diese Regulierung derzeit nicht. Das ist eine Momentaufnahme: Wachsen Beschäftigtenzahl oder Umsatz, kommen Produkte oder Absatzmärkte hinzu, kann sich das Ergebnis ändern. Prüfen Sie deshalb nach größeren Veränderungen erneut.",
        "en": "On the basis of your entries this regulation currently does not apply. That is a snapshot: if headcount or turnover grow, or products or markets are added, the result can change. Run the check again after major changes.",
        "es": "Según sus datos, esta regulación no se aplica por ahora. Es una instantánea: si crecen la plantilla o la cifra de negocios, o se añaden productos o mercados, el resultado puede cambiar. Vuelva a verificar tras cambios importantes.",
        "fr": "D'après vos indications, cette réglementation ne s'applique pas actuellement. Il s'agit d'un instantané : si l'effectif ou le chiffre d'affaires augmentent, ou si des produits ou des marchés s'ajoutent, le résultat peut changer. Refaites la vérification après des changements importants.",
        "it": "In base ai suoi dati questa normativa al momento non si applica. È un'istantanea: se crescono organico o fatturato, o si aggiungono prodotti o mercati, il risultato può cambiare. Ripeta la verifica dopo cambiamenti rilevanti.",
        "zh": "根据所填信息，该法规目前不适用。这只是当前状况：若员工人数或营业额增长，或新增产品或销售市场，结论可能改变。发生较大变化后请重新检查。",
    },
    "deadline": {
        "de": "Der Zeitpunkt, ab dem die Regulierung für ein Unternehmen mit Ihrem Profil gilt. Viele Vorschriften starten gestaffelt nach Größe; hier steht die Stufe, die zu Ihren Angaben passt — nicht das allgemeine Inkrafttreten. Steht statt eines Datums ein Hinweis, ist der Anwendungsbeginn noch offen.",
        "en": "The point from which the regulation applies to a company with your profile. Many rules phase in by size; what is shown here is the stage that matches your entries — not the general entry into force. Where a note appears instead of a date, the start of application is still open.",
        "es": "El momento a partir del cual la regulación se aplica a una empresa con su perfil. Muchas normas se aplican de forma escalonada según el tamaño; aquí figura el escalón que corresponde a sus datos, no la entrada en vigor general. Si en lugar de una fecha aparece una indicación, el inicio de aplicación sigue abierto.",
        "fr": "Le moment à partir duquel la réglementation s'applique à une entreprise ayant votre profil. De nombreuses règles s'appliquent par paliers selon la taille ; figure ici le palier correspondant à vos indications, et non l'entrée en vigueur générale. Si une mention remplace la date, le début d'application reste ouvert.",
        "it": "Il momento a partire dal quale la normativa si applica a un'impresa con il suo profilo. Molte norme si applicano per scaglioni in base alla dimensione; qui compare lo scaglione che corrisponde ai suoi dati, non l'entrata in vigore generale. Se al posto della data compare una nota, l'inizio dell'applicazione è ancora aperto.",
        "zh": "指该法规对与贵公司情况相符的企业开始适用的时间。许多规定按规模分阶段实施；此处显示的是与所填信息相符的阶段，而非一般生效日期。若显示的不是日期而是说明，则适用起始时间尚未确定。",
    },
    "passage": {
        "de": "Die Stelle im Gesetzestext, auf die sich die Einschätzung stützt — sinngemäß wiedergegeben und auf rund 280 Zeichen gekürzt. Zahlen mit Schwellenbezug sind rot hervorgehoben. Den vollen Wortlaut erreichen Sie über den Link im Titel der Karte.",
        "en": "The passage of the legal text on which the assessment rests — rendered in substance and shortened to about 280 characters. Figures relating to thresholds are highlighted in red. The full wording is available via the link in the card title.",
        "es": "El pasaje del texto legal en el que se apoya la valoración, reproducido en lo esencial y acortado a unos 280 caracteres. Las cifras relacionadas con umbrales aparecen destacadas en rojo. El texto íntegro está disponible a través del enlace del título de la tarjeta.",
        "fr": "Le passage du texte légal sur lequel repose l'appréciation, restitué dans sa substance et raccourci à environ 280 caractères. Les chiffres relatifs aux seuils sont surlignés en rouge. Le texte intégral est accessible par le lien dans le titre de la fiche.",
        "it": "Il passaggio del testo normativo su cui si fonda la valutazione, riportato nella sostanza e abbreviato a circa 280 caratteri. Le cifre riferite a soglie sono evidenziate in rosso. Il testo integrale è raggiungibile tramite il link nel titolo della scheda.",
        "zh": "该评估所依据的法律条文段落，按其含义转述并截取至约 280 个字符。与门槛有关的数字以红色标出。完整原文可通过卡片标题中的链接查看。",
    },
    "law_state": {
        "de": "Das Datum, an dem die Anwendung den zugrunde liegenden Gesetzestext zuletzt von der amtlichen Quelle geladen hat. Genutzt wird, soweit vorhanden, die konsolidierte Fassung — also der Text einschließlich späterer Änderungen. Ein älteres Datum heißt nicht, dass der Text veraltet ist, sondern nur, dass seither kein neuer Abruf stattgefunden hat.",
        "en": "The date on which the application last downloaded the underlying legal text from the official source. Where available, the consolidated version is used — the text including later amendments. An older date does not mean the text is out of date, only that no new retrieval has taken place since.",
        "es": "La fecha en la que la aplicación descargó por última vez el texto legal de la fuente oficial. Se utiliza, cuando existe, la versión consolidada, es decir, el texto con las modificaciones posteriores. Una fecha antigua no significa que el texto esté desfasado, sino solo que desde entonces no ha habido una nueva descarga.",
        "fr": "La date à laquelle l'application a téléchargé pour la dernière fois le texte légal depuis la source officielle. La version consolidée est utilisée lorsqu'elle existe, c'est-à-dire le texte intégrant les modifications ultérieures. Une date ancienne ne signifie pas que le texte est périmé, mais seulement qu'aucun nouveau téléchargement n'a eu lieu depuis.",
        "it": "La data in cui l'applicazione ha scaricato per l'ultima volta il testo normativo dalla fonte ufficiale. Ove disponibile viene usata la versione consolidata, cioè il testo comprensivo delle modifiche successive. Una data meno recente non significa che il testo sia superato, ma solo che da allora non è avvenuto un nuovo scaricamento.",
        "zh": "本应用最近一次从官方来源下载相关法律文本的日期。如有合并版本，则使用合并版，即包含后续修订的文本。日期较早并不意味着文本过时，只说明此后未再进行新的抓取。",
    },
}


# ---------- Helper ----------
def t(key: str, lang: str = "de") -> str:
    entry = UI.get(key, {})
    return entry.get(lang) or entry.get("de") or key


def t_opt(value: str, mapping: dict[str, dict[str, str]], lang: str = "de") -> str:
    entry = mapping.get(value, {})
    return entry.get(lang) or entry.get("de") or value


def t_status(status: str, lang: str = "de") -> str:
    """Label fuer den Status eines Rechtsakts (in_kraft, gilt_ab, …)."""
    return t_opt(status, STATUS_LABELS, lang)


def t_applies_note(note_key: str, lang: str = "de") -> str:
    """Erlaeuterung zum Anwendungsbeginn (leer, wenn kein Hinweis hinterlegt)."""
    if not note_key:
        return ""
    return t_opt(note_key, APPLIES_NOTES, lang) if note_key in APPLIES_NOTES else ""


def t_deadline_note(note_key: str, lang: str = "de") -> str:
    """Erlaeuterung zum unternehmensbezogenen Anwendungsbeginn.

    Erst `DEADLINE_NOTES` (Staffelung fuer dieses Unternehmen), sonst der
    allgemeine Normhinweis aus `APPLIES_NOTES`. Leer, wenn nichts hinterlegt ist.
    """
    if not note_key:
        return ""
    if note_key in DEADLINE_NOTES:
        return t_opt(note_key, DEADLINE_NOTES, lang)
    return t_applies_note(note_key, lang)


def t_first_step(step_key: str, lang: str = "de") -> str:
    """Ein kuratierter erster Schritt (leer, wenn der Schluessel unbekannt ist)."""
    return t_opt(step_key, FIRST_STEPS, lang) if step_key in FIRST_STEPS else ""


def t_threshold_hint(hint: dict, lang: str = "de") -> str:
    """Hinweis zur Schwellen-Naehe aus `thresholds.near_thresholds()`."""
    lang = normalize_lang(lang)
    template = THRESHOLD_HINTS.get(hint.get("key", ""), {}).get(lang, "")
    if not template:
        return ""
    values = hint.get("values") or {}
    return template.format(
        employees=fmt_int(values.get("employees"), lang),
        employees_de=fmt_int(values.get("employees_de"), lang),
        revenue=fmt_eur(values.get("revenue_eur"), lang),
        energy=fmt_gwh(values.get("energy_gwh"), lang),
    )


def t_help(key: str, lang: str = "de") -> str:
    """Erlaeuterungstext zu einem Feld/Begriff; leer, wenn es keinen gibt."""
    entry = FIELD_HELP.get(key)
    if not entry:
        return ""
    return entry.get(lang) or entry.get("de", "")


def normalize_lang(lang: str | None) -> str:
    """Filter auf erlaubte Codes, Default 'de'."""
    if lang and lang.lower() in LANG_CODES:
        return lang.lower()
    return "de"
