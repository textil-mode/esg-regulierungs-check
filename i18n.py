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
    "language_picker_label": {
        "de": "Sprache",
        "en": "Language",
        "es": "Idioma",
        "fr": "Langue",
        "it": "Lingua",
        "zh": "语言",
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
    "hinweis_label": {
        "de": "Hinweis",
        "en": "Note",
        "es": "Aviso",
        "fr": "Note",
        "it": "Nota",
        "zh": "说明",
    },
    "hinweis_body": {
        "de": "Diese Projektseite ist mithilfe von Claude Code und OpenAI Codex entstanden.",
        "en": "This project page was created with the help of Claude Code and OpenAI Codex.",
        "es": "Esta página del proyecto se creó con la ayuda de Claude Code y OpenAI Codex.",
        "fr": "Cette page de projet a été créée avec l'aide de Claude Code et d'OpenAI Codex.",
        "it": "Questa pagina del progetto è stata realizzata con l'aiuto di Claude Code e OpenAI Codex.",
        "zh": "本项目页面是在 Claude Code 与 OpenAI Codex 的协助下创建的。",
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
        "de": "E-Mail oder Passwort falsch.",
        "en": "Email or password incorrect.",
        "es": "Correo o contraseña incorrectos.",
        "fr": "E-mail ou mot de passe incorrect.",
        "it": "E-mail o password errati.",
        "zh": "邮箱或密码错误。",
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
    "forgot_hint": {
        "de": "Diese Anwendung verschickt keine E-Mails. Ihre Anfrage geht an die Administration, die Ihnen einen einmaligen Link zum Neusetzen zukommen lässt.",
        "en": "This application does not send emails. Your request goes to the administrator, who will send you a one-time link to set a new password.",
        "es": "Esta aplicación no envía correos. Su solicitud llega al administrador, que le enviará un enlace de un solo uso para establecer una nueva contraseña.",
        "fr": "Cette application n'envoie pas d'e-mails. Votre demande est transmise à l'administrateur, qui vous enverra un lien à usage unique pour définir un nouveau mot de passe.",
        "it": "Questa applicazione non invia e-mail. La richiesta arriva all'amministratore, che le invierà un link monouso per impostare una nuova password.",
        "zh": "本应用不发送邮件。您的请求将转交管理员，管理员会向您发送一次性重设链接。",
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
    "field_name": {"de": "Unternehmensname", "en": "Company name", "es": "Nombre de la empresa", "fr": "Nom de l'entreprise", "it": "Nome dell'azienda", "zh": "公司名称"},
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
    "field_employees_de_help": {
        "de": "Wichtig für LkSG (>1000 Inland) und HinSchG (≥50 Inland).",
        "en": "Important for LkSG (>1000 domestic) and HinSchG (≥50 domestic).",
        "es": "Importante para LkSG (>1000 nacionales) y HinSchG (≥50 nacionales).",
        "fr": "Important pour LkSG (>1000 nationaux) et HinSchG (≥50 nationaux).",
        "it": "Importante per LkSG (>1000 nazionali) e HinSchG (≥50 nazionali).",
        "zh": "对 LkSG(>1000 本国)和 HinSchG(≥50 本国)重要。",
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
    "field_revenue_eu_help": {
        "de": "Maßgeblich für Unternehmen aus Drittländern: CSRD (Art. 40a Bilanzrichtlinie, mehr als 450 Mio. EUR) und CSDDD (Art. 2 Abs. 2, mehr als 1,5 Mrd. EUR) stellen dort auf den Umsatz in der Union ab.",
        "en": "Decisive for third-country companies: CSRD (Art. 40a Accounting Directive, more than EUR 450 million) and CSDDD (Art. 2(2), more than EUR 1.5 billion) rely on turnover in the Union.",
        "es": "Determinante para empresas de terceros países: la CSRD (art. 40a de la Directiva contable, más de 450 millones EUR) y la CSDDD (art. 2, apdo. 2, más de 1500 millones EUR) se basan en la cifra de negocios en la Unión.",
        "fr": "Déterminant pour les entreprises de pays tiers : la CSRD (art. 40a de la directive comptable, plus de 450 millions EUR) et la CSDDD (art. 2, par. 2, plus de 1,5 milliard EUR) se fondent sur le chiffre d'affaires réalisé dans l'Union.",
        "it": "Determinante per le imprese di paesi terzi: la CSRD (art. 40a della direttiva contabile, oltre 450 milioni di EUR) e la CSDDD (art. 2, par. 2, oltre 1,5 miliardi di EUR) si basano sul fatturato realizzato nell'Unione.",
        "zh": "对第三国企业具有决定意义：CSRD（《会计指令》第 40a 条，超过 4.5 亿欧元）与 CSDDD（第 2 条第 2 款，超过 15 亿欧元）均以在欧盟境内的营业额为准。",
    },
    "field_balance_sheet": {
        "de": "Bilanzsumme (EUR)",
        "en": "Balance sheet total (EUR)",
        "es": "Total del balance (EUR)",
        "fr": "Total du bilan (EUR)",
        "it": "Totale di bilancio (EUR)",
        "zh": "资产负债表总额(欧元)",
    },
    "field_balance_help": {
        "de": "Relevant für CSRD-Schwelle (25 Mio Bilanzsumme ODER 50 Mio Umsatz).",
        "en": "Relevant for CSRD threshold (25M balance OR 50M revenue).",
        "es": "Relevante para el umbral CSRD (25M balance O 50M ingresos).",
        "fr": "Pertinent pour le seuil CSRD (25M bilan OU 50M CA).",
        "it": "Rilevante per la soglia CSRD (25M bilancio O 50M ricavi).",
        "zh": "与 CSRD 门槛相关(2500 万资产负债表或 5000 万收入)。",
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
    "field_env_claims_help": {
        "de": "Wichtig für EmpCo-Richtlinie und Green Claims.",
        "en": "Important for EmpCo Directive and Green Claims.",
        "es": "Importante para la Directiva EmpCo y Green Claims.",
        "fr": "Important pour la directive EmpCo et Green Claims.",
        "it": "Importante per la direttiva EmpCo e Green Claims.",
        "zh": "对 EmpCo 指令和绿色声明很重要。",
    },
    "field_eu_importer": {
        "de": "EU-Importeur / erstmaliges Inverkehrbringen in der EU",
        "en": "EU importer / first placing on the EU market",
        "es": "Importador en la UE / primera puesta en el mercado de la UE",
        "fr": "Importateur UE / première mise sur le marché de l'UE",
        "it": "Importatore UE / prima immissione sul mercato UE",
        "zh": "欧盟进口商 / 首次在欧盟市场投放",
    },
    "field_eu_importer_help": {
        "de": "Führt Ihr Unternehmen Produkte aus Drittländern in die EU ein und stellt diese auf dem EU-Markt bereit bzw. bringt sie erstmals in Verkehr? Relevant u.a. für EUDR, FLR, PPWR, Ökodesign-VO, MinRohSorgG.",
        "en": "Does your company import products from third countries into the EU and make them available on the EU market or place them on the market for the first time? Relevant for EUDR, FLR, PPWR, Ecodesign Regulation, MinRohSorgG.",
        "es": "¿Su empresa importa productos de terceros países a la UE y los comercializa en el mercado de la UE o los introduce por primera vez en el mercado? Relevante para EUDR, FLR, PPWR, Reglamento de Ecodiseño, MinRohSorgG.",
        "fr": "Votre entreprise importe-t-elle des produits de pays tiers dans l'UE et les met-elle à disposition sur le marché de l'UE ou les place-t-elle pour la première fois sur le marché ? Pertinent pour EUDR, FLR, PPWR, règlement Écoconception, MinRohSorgG.",
        "it": "La vostra azienda importa prodotti da paesi terzi nell'UE e li mette a disposizione sul mercato UE o li immette sul mercato per la prima volta? Rilevante per EUDR, FLR, PPWR, Regolamento Ecodesign, MinRohSorgG.",
        "zh": "贵公司是否从第三国向欧盟进口产品，并在欧盟市场上提供或首次投放市场？涉及 EUDR、FLR、PPWR、生态设计条例、MinRohSorgG 等。",
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
    "greenclaims": {
        "de": "Die EU-Kommission hat am 20.06.2025 angekündigt, den Vorschlag zurückzuziehen; förmlich "
              "zurückgenommen ist er nicht. Es bestehen derzeit keine Pflichten aus diesem Entwurf.",
        "en": "On 20.06.2025 the EU Commission announced its intention to withdraw the proposal; it has not "
              "been formally withdrawn. No obligations currently arise from this draft.",
        "es": "El 20.06.2025 la Comisión anunció su intención de retirar la propuesta; formalmente no ha sido "
              "retirada. Actualmente no derivan obligaciones de este proyecto.",
        "fr": "Le 20.06.2025, la Commission a annoncé son intention de retirer la proposition ; elle n'a pas "
              "été formellement retirée. Aucune obligation ne découle actuellement de ce projet.",
        "it": "Il 20.06.2025 la Commissione ha annunciato l'intenzione di ritirare la proposta; formalmente "
              "non è stata ritirata. Da questo progetto non derivano attualmente obblighi.",
        "zh": "欧盟委员会于 2025 年 6 月 20 日宣布拟撤回该提案，但尚未正式撤回。目前该草案不产生任何义务。",
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
    "sfdr_1": {
        "de": "Finanzprodukte einstufen und die Angaben nach Art. 6, 8 oder 9 festlegen.",
        "en": "Classify financial products and determine the disclosures under Art. 6, 8 or 9.",
        "es": "Clasificar los productos financieros y definir la información según los art. 6, 8 o 9.",
        "fr": "Classer les produits financiers et définir les informations au titre des art. 6, 8 ou 9.",
        "it": "Classificare i prodotti finanziari e definire le informazioni ai sensi degli art. 6, 8 o 9.",
        "zh": "对金融产品进行分类，并确定第 6、8 或 9 条项下的披露内容。",
    },
    "sfdr_2": {
        "de": "Strategien zur Einbeziehung von Nachhaltigkeitsrisiken und die Vergütungspolitik auf "
              "der Website offenlegen (Art. 3, 5).",
        "en": "Publish policies on the integration of sustainability risks and the remuneration policy "
              "on the website (Art. 3, 5).",
        "es": "Publicar en la web las políticas de integración de riesgos de sostenibilidad y la "
              "política de remuneración (art. 3, 5).",
        "fr": "Publier sur le site web les politiques d'intégration des risques de durabilité et la "
              "politique de rémunération (art. 3, 5).",
        "it": "Pubblicare sul sito le politiche di integrazione dei rischi di sostenibilità e la "
              "politica di remunerazione (art. 3, 5).",
        "zh": "在网站上披露可持续性风险纳入策略及薪酬政策（第 3、5 条）。",
    },
    "sfdr_3": {
        "de": "Erklärung zu den wichtigsten nachteiligen Nachhaltigkeitsauswirkungen abgeben oder das "
              "Unterlassen begründen (Art. 4).",
        "en": "Publish a statement on principal adverse sustainability impacts or explain why not "
              "(Art. 4).",
        "es": "Publicar una declaración sobre las principales incidencias adversas en materia de "
              "sostenibilidad o explicar por qué no (art. 4).",
        "fr": "Publier une déclaration sur les principales incidences négatives en matière de durabilité "
              "ou expliquer son abstention (art. 4).",
        "it": "Pubblicare una dichiarazione sui principali effetti negativi per la sostenibilità o "
              "spiegarne la mancanza (art. 4).",
        "zh": "发布主要不利可持续性影响声明，或说明不发布的理由（第 4 条）。",
    },
    # --- ESG-Rating-Verordnung ---
    "esgrating_1": {
        "de": "Prüfen, ob eigene Bewertungen als ESG-Rating im Sinne des Art. 3 gelten; bewertete "
              "Unternehmen selbst sind nicht erfasst.",
        "en": "Check whether your own assessments qualify as ESG ratings under Art. 3; rated companies "
              "themselves are not covered.",
        "es": "Comprobar si las propias valoraciones constituyen una calificación ESG conforme al art. 3; "
              "las empresas calificadas no están sujetas.",
        "fr": "Vérifier si vos propres évaluations constituent une notation ESG au sens de l'art. 3 ; "
              "les entreprises notées ne sont pas visées.",
        "it": "Verificare se le proprie valutazioni costituiscono un rating ESG ai sensi dell'art. 3; le "
              "imprese valutate non rientrano nell'ambito.",
        "zh": "核查自身评估是否构成第 3 条所指的 ESG 评级；被评级企业本身不在适用范围内。",
    },
    "esgrating_2": {
        "de": "Zulassung bei der ESMA vorbereiten und die organisatorischen Anforderungen an "
              "Unabhängigkeit und Interessenkonflikte umsetzen (Art. 4 ff., Anhang III).",
        "en": "Prepare authorisation by ESMA and implement the organisational requirements on "
              "independence and conflicts of interest (Art. 4 et seq., Annex III).",
        "es": "Preparar la autorización ante la ESMA e implantar los requisitos organizativos de "
              "independencia y conflictos de interés (art. 4 y ss., anexo III).",
        "fr": "Préparer l'agrément auprès de l'AEMF et mettre en œuvre les exigences organisationnelles "
              "d'indépendance et de conflits d'intérêts (art. 4 et suiv., annexe III).",
        "it": "Preparare l'autorizzazione presso l'ESMA e attuare i requisiti organizzativi su "
              "indipendenza e conflitti di interesse (art. 4 ss., allegato III).",
        "zh": "准备向 ESMA 申请授权，并落实关于独立性和利益冲突的组织性要求（第 4 条及以下、附件三）。",
    },
    "esgrating_3": {
        "de": "Methoden, Modelle und Grundannahmen offenlegen und laufend aktuell halten (Anhang I).",
        "en": "Disclose methodologies, models and key assumptions and keep them up to date (Annex I).",
        "es": "Divulgar metodologías, modelos e hipótesis fundamentales y mantenerlos actualizados "
              "(anexo I).",
        "fr": "Publier les méthodologies, modèles et hypothèses clés et les tenir à jour (annexe I).",
        "it": "Divulgare metodologie, modelli e ipotesi di base e mantenerli aggiornati (allegato I).",
        "zh": "披露方法论、模型和基本假设，并持续保持更新（附件一）。",
    },
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
    # --- Green Claims (Entwurf) ---
    "greenclaims_1": {
        "de": "Aus dem Entwurf ergeben sich derzeit keine Pflichten; das Verfahren ruht seit der "
              "angekündigten Rücknahme und ist nur zu beobachten.",
        "en": "The draft currently creates no obligations; the procedure has been dormant since the "
              "announced withdrawal and merely needs to be monitored.",
        "es": "El proyecto no genera actualmente obligaciones; el procedimiento está paralizado desde la "
              "retirada anunciada y solo debe seguirse.",
        "fr": "Le projet ne crée actuellement aucune obligation ; la procédure est suspendue depuis le "
              "retrait annoncé et doit seulement être suivie.",
        "it": "Dalla bozza non derivano attualmente obblighi; la procedura è sospesa dal ritiro "
              "annunciato e va solo monitorata.",
        "zh": "该草案目前不产生任何义务；自宣布拟撤回后程序处于停滞状态，只需持续关注。",
    },
    "greenclaims_2": {
        "de": "Umweltaussagen bereits heute nach der EmpCo-Richtlinie beziehungsweise dem UWG belegen — "
              "diese Regeln gelten unabhängig vom Entwurf.",
        "en": "Substantiate environmental claims already today under the EmpCo Directive or the German "
              "UWG — those rules apply irrespective of the draft.",
        "es": "Fundamentar ya hoy las alegaciones ambientales conforme a la Directiva EmpCo o la UWG "
              "alemana: esas reglas se aplican con independencia del proyecto.",
        "fr": "Étayer dès aujourd'hui les allégations environnementales au titre de la directive EmpCo "
              "ou de l'UWG allemande : ces règles s'appliquent indépendamment du projet.",
        "it": "Documentare già oggi le asserzioni ambientali secondo la direttiva EmpCo o la UWG tedesca: "
              "tali regole valgono a prescindere dalla bozza.",
        "zh": "现在即应依据 EmpCo 指令或德国《反不正当竞争法》为环保宣称提供依据——这些规则与该草案无关，独立适用。",
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
    "Land-/Forstwirtschaft, Fischerei": {
        "de": "Land-/Forstwirtschaft, Fischerei",
        "en": "Agriculture / Forestry / Fishing",
        "es": "Agricultura / Silvicultura / Pesca",
        "fr": "Agriculture / Sylviculture / Pêche",
        "it": "Agricoltura / Silvicoltura / Pesca",
        "zh": "农业 / 林业 / 渔业",
    },
    "Bergbau / Gewinnung von Steinen und Erden": {
        "de": "Bergbau / Gewinnung von Steinen und Erden",
        "en": "Mining / Quarrying",
        "es": "Minería / Extracción de piedras y tierras",
        "fr": "Exploitation minière / Extraction",
        "it": "Attività estrattiva / Cave",
        "zh": "采矿 / 采石",
    },
    "Verarbeitendes Gewerbe / Industrie": {
        "de": "Verarbeitendes Gewerbe / Industrie",
        "en": "Manufacturing / Industry",
        "es": "Manufactura / Industria",
        "fr": "Industrie manufacturière",
        "it": "Manifatturiero / Industria",
        "zh": "制造业 / 工业",
    },
    "Chemie / Pharma": {
        "de": "Chemie / Pharma",
        "en": "Chemicals / Pharmaceuticals",
        "es": "Química / Farmacéutica",
        "fr": "Chimie / Pharmacie",
        "it": "Chimica / Farmaceutica",
        "zh": "化工 / 制药",
    },
    "Metallverarbeitung / Maschinenbau": {
        "de": "Metallverarbeitung / Maschinenbau",
        "en": "Metal processing / Machinery",
        "es": "Metalurgia / Maquinaria",
        "fr": "Métallurgie / Machines",
        "it": "Lavorazione metalli / Macchinari",
        "zh": "金属加工 / 机械制造",
    },
    "Automobil / Fahrzeugbau": {
        "de": "Automobil / Fahrzeugbau",
        "en": "Automotive / Vehicle construction",
        "es": "Automoción / Fabricación de vehículos",
        "fr": "Automobile / Construction de véhicules",
        "it": "Automotive / Costruzione veicoli",
        "zh": "汽车 / 车辆制造",
    },
    "Elektronik / Elektrotechnik": {
        "de": "Elektronik / Elektrotechnik",
        "en": "Electronics / Electrical engineering",
        "es": "Electrónica / Electrotecnia",
        "fr": "Électronique / Électrotechnique",
        "it": "Elettronica / Elettrotecnica",
        "zh": "电子 / 电气工程",
    },
    "Textil / Bekleidung / Leder": {
        "de": "Textil / Bekleidung / Leder",
        "en": "Textile / Clothing / Leather",
        "es": "Textil / Ropa / Cuero",
        "fr": "Textile / Habillement / Cuir",
        "it": "Tessile / Abbigliamento / Pelletteria",
        "zh": "纺织 / 服装 / 皮革",
    },
    "Lebensmittel / Getränke": {
        "de": "Lebensmittel / Getränke",
        "en": "Food / Beverages",
        "es": "Alimentos / Bebidas",
        "fr": "Alimentation / Boissons",
        "it": "Alimentare / Bevande",
        "zh": "食品 / 饮料",
    },
    "Möbel / Holz / Papier": {
        "de": "Möbel / Holz / Papier",
        "en": "Furniture / Wood / Paper",
        "es": "Muebles / Madera / Papel",
        "fr": "Meubles / Bois / Papier",
        "it": "Mobili / Legno / Carta",
        "zh": "家具 / 木材 / 纸张",
    },
    "Energieversorgung": {
        "de": "Energieversorgung",
        "en": "Energy supply",
        "es": "Suministro de energía",
        "fr": "Fourniture d'énergie",
        "it": "Fornitura di energia",
        "zh": "能源供应",
    },
    "Wasser- / Abfallwirtschaft": {
        "de": "Wasser- / Abfallwirtschaft",
        "en": "Water / Waste management",
        "es": "Gestión de agua / residuos",
        "fr": "Eau / Gestion des déchets",
        "it": "Gestione acqua / rifiuti",
        "zh": "水务 / 废物管理",
    },
    "Bauwirtschaft": {
        "de": "Bauwirtschaft",
        "en": "Construction",
        "es": "Construcción",
        "fr": "Construction",
        "it": "Edilizia",
        "zh": "建筑业",
    },
    "Handel (Groß-/Einzelhandel)": {
        "de": "Handel (Groß-/Einzelhandel)",
        "en": "Trade (Wholesale/Retail)",
        "es": "Comercio (mayorista / minorista)",
        "fr": "Commerce (gros / détail)",
        "it": "Commercio (all'ingrosso / al dettaglio)",
        "zh": "贸易(批发 / 零售)",
    },
    "Verkehr / Logistik": {
        "de": "Verkehr / Logistik",
        "en": "Transport / Logistics",
        "es": "Transporte / Logística",
        "fr": "Transport / Logistique",
        "it": "Trasporti / Logistica",
        "zh": "交通 / 物流",
    },
    "Gastgewerbe / Tourismus": {
        "de": "Gastgewerbe / Tourismus",
        "en": "Hospitality / Tourism",
        "es": "Hostelería / Turismo",
        "fr": "Hôtellerie / Tourisme",
        "it": "Ospitalità / Turismo",
        "zh": "酒店 / 旅游",
    },
    "Information / Telekommunikation / IT": {
        "de": "Information / Telekommunikation / IT",
        "en": "Information / Telecom / IT",
        "es": "Información / Telecomunicaciones / TI",
        "fr": "Information / Télécom / IT",
        "it": "Informazione / Telecomunicazioni / IT",
        "zh": "信息 / 电信 / IT",
    },
    "Finanzdienstleistungen": {
        "de": "Finanzdienstleistungen",
        "en": "Financial services",
        "es": "Servicios financieros",
        "fr": "Services financiers",
        "it": "Servizi finanziari",
        "zh": "金融服务",
    },
    "Versicherungen": {
        "de": "Versicherungen",
        "en": "Insurance",
        "es": "Seguros",
        "fr": "Assurances",
        "it": "Assicurazioni",
        "zh": "保险",
    },
    "Immobilien": {
        "de": "Immobilien",
        "en": "Real estate",
        "es": "Bienes raíces",
        "fr": "Immobilier",
        "it": "Immobiliare",
        "zh": "房地产",
    },
    "Beratung / Recht / Wirtschaftsprüfung": {
        "de": "Beratung / Recht / Wirtschaftsprüfung",
        "en": "Consulting / Legal / Auditing",
        "es": "Consultoría / Derecho / Auditoría",
        "fr": "Conseil / Droit / Audit",
        "it": "Consulenza / Legale / Revisione",
        "zh": "咨询 / 法律 / 审计",
    },
    "Forschung / Entwicklung": {
        "de": "Forschung / Entwicklung",
        "en": "Research / Development",
        "es": "Investigación / Desarrollo",
        "fr": "Recherche / Développement",
        "it": "Ricerca / Sviluppo",
        "zh": "研究 / 开发",
    },
    "Bildung": {"de": "Bildung", "en": "Education", "es": "Educación", "fr": "Éducation", "it": "Istruzione", "zh": "教育"},
    "Gesundheit / Soziales": {
        "de": "Gesundheit / Soziales",
        "en": "Health / Social",
        "es": "Salud / Asuntos sociales",
        "fr": "Santé / Social",
        "it": "Sanità / Sociale",
        "zh": "健康 / 社会事务",
    },
    "Kunst / Unterhaltung / Medien": {
        "de": "Kunst / Unterhaltung / Medien",
        "en": "Arts / Entertainment / Media",
        "es": "Arte / Entretenimiento / Medios",
        "fr": "Arts / Divertissement / Médias",
        "it": "Arte / Intrattenimento / Media",
        "zh": "艺术 / 娱乐 / 媒体",
    },
    "Sonstige Dienstleistungen": {
        "de": "Sonstige Dienstleistungen",
        "en": "Other services",
        "es": "Otros servicios",
        "fr": "Autres services",
        "it": "Altri servizi",
        "zh": "其他服务",
    },
}

SITE_TYPE_LABELS: dict[str, dict[str, str]] = {
    "Hauptverwaltung, Hauptniederlassung, Verwaltungssitz, satzungsmäßigen Sitz oder Zweigniederlassung": {
        "de": "Hauptverwaltung, Hauptniederlassung, Verwaltungssitz, satzungsmäßigen Sitz oder Zweigniederlassung",
        "en": "Head office, principal place of business, administrative seat, registered office or branch",
        "es": "Administración central, establecimiento principal, sede administrativa, domicilio social o sucursal",
        "fr": "Administration centrale, établissement principal, siège administratif, siège statutaire ou succursale",
        "it": "Amministrazione centrale, sede principale, sede amministrativa, sede legale o succursale",
        "zh": "主行政管理机构、主要营业地、管理住所、章程登记住所或分支机构",
    },
    "Produktionsstätte": {
        "de": "Produktionsstätte",
        "en": "Production site",
        "es": "Planta de producción",
        "fr": "Site de production",
        "it": "Stabilimento produttivo",
        "zh": "生产基地",
    },
    "Vertriebsbüro": {
        "de": "Vertriebsbüro",
        "en": "Sales office",
        "es": "Oficina de ventas",
        "fr": "Bureau commercial",
        "it": "Ufficio vendite",
        "zh": "销售办公室",
    },
    "Lager / Logistikzentrum": {
        "de": "Lager / Logistikzentrum",
        "en": "Warehouse / Logistics center",
        "es": "Almacén / Centro logístico",
        "fr": "Entrepôt / Centre logistique",
        "it": "Magazzino / Centro logistico",
        "zh": "仓库 / 物流中心",
    },
    "Forschung / Entwicklung": {
        "de": "Forschung / Entwicklung",
        "en": "Research / Development",
        "es": "Investigación / Desarrollo",
        "fr": "Recherche / Développement",
        "it": "Ricerca / Sviluppo",
        "zh": "研究 / 开发",
    },
    "Filiale / Niederlassung": {
        "de": "Filiale / Niederlassung",
        "en": "Branch office",
        "es": "Sucursal",
        "fr": "Succursale",
        "it": "Filiale",
        "zh": "分支机构",
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
    "Verpackungen von Produkten / Versand- oder Transportverpackungen": {
        "de": "Verpackungen von Produkten / Versand- oder Transportverpackungen",
        "en": "Product packaging / shipping or transport packaging",
        "es": "Envases de productos / embalajes de envío o transporte",
        "fr": "Emballages de produits / emballages d'expédition ou de transport",
        "it": "Imballaggi di prodotti / imballaggi per spedizione o trasporto",
        "zh": "产品包装 / 运输或物流包装",
    },
    "Holz": {"de": "Holz", "en": "Wood", "es": "Madera", "fr": "Bois", "it": "Legno", "zh": "木材"},
    "Holzprodukte": {
        "de": "Holzprodukte", "en": "Wood products", "es": "Productos de madera",
        "fr": "Produits en bois", "it": "Prodotti in legno", "zh": "木制品",
    },
    "Papier": {"de": "Papier", "en": "Paper", "es": "Papel", "fr": "Papier", "it": "Carta", "zh": "纸张"},
    "Kautschuk/Gummi": {
        "de": "Kautschuk/Gummi", "en": "Rubber", "es": "Caucho / Goma",
        "fr": "Caoutchouc", "it": "Gomma / Caucciù", "zh": "橡胶",
    },
    "Bekleidung": {
        "de": "Bekleidung", "en": "Clothing", "es": "Ropa",
        "fr": "Habillement", "it": "Abbigliamento", "zh": "服装",
    },
    "Heimtextilien": {
        "de": "Heimtextilien", "en": "Home textiles", "es": "Textiles del hogar",
        "fr": "Textiles de maison", "it": "Tessili per la casa", "zh": "家用纺织品",
    },
    "technische Textilien": {
        "de": "technische Textilien", "en": "Technical textiles", "es": "Textiles técnicos",
        "fr": "Textiles techniques", "it": "Tessili tecnici", "zh": "产业用纺织品",
    },
    "PSA": {
        "de": "PSA (persönliche Schutzausrüstung)",
        "en": "PPE (personal protective equipment)",
        "es": "EPI (equipos de protección individual)",
        "fr": "EPI (équipements de protection individuelle)",
        "it": "DPI (dispositivi di protezione individuale)",
        "zh": "个人防护装备（PPE）",
    },
    "Schuhe": {"de": "Schuhe", "en": "Footwear", "es": "Calzado", "fr": "Chaussures", "it": "Calzature", "zh": "鞋类"},
    "Lederwaren": {
        "de": "Lederwaren", "en": "Leather goods", "es": "Marroquinería",
        "fr": "Maroquinerie", "it": "Pelletteria", "zh": "皮革制品",
    },
    "textile Medizinprodukte": {
        "de": "textile Medizinprodukte", "en": "Textile medical devices",
        "es": "Productos sanitarios textiles", "fr": "Dispositifs médicaux textiles",
        "it": "Dispositivi medici tessili", "zh": "纺织类医疗器械",
    },
    "Automotive-Textilien": {
        "de": "Automotive-Textilien", "en": "Automotive textiles", "es": "Textiles para automoción",
        "fr": "Textiles pour l'automobile", "it": "Tessili per l'automotive", "zh": "汽车用纺织品",
    },
}


ROLE_LABELS: dict[str, dict[str, str]] = {
    "Hersteller": {
        "de": "Hersteller", "en": "Manufacturer", "es": "Fabricante",
        "fr": "Fabricant", "it": "Fabbricante", "zh": "制造商",
    },
    "Marke": {
        "de": "Marke", "en": "Brand", "es": "Marca",
        "fr": "Marque", "it": "Marchio", "zh": "品牌方",
    },
    "Importeur": {
        "de": "Importeur", "en": "Importer", "es": "Importador",
        "fr": "Importateur", "it": "Importatore", "zh": "进口商",
    },
    "Händler": {
        "de": "Händler", "en": "Distributor / retailer", "es": "Distribuidor / minorista",
        "fr": "Distributeur / détaillant", "it": "Distributore / rivenditore", "zh": "经销商 / 零售商",
    },
    "Onlinehändler": {
        "de": "Onlinehändler", "en": "Online retailer", "es": "Comercio en línea",
        "fr": "Commerçant en ligne", "it": "Rivenditore online", "zh": "线上零售商",
    },
    "Zulieferer": {
        "de": "Zulieferer", "en": "Supplier", "es": "Proveedor",
        "fr": "Fournisseur", "it": "Fornitore", "zh": "供应商",
    },
}


MATERIAL_LABELS: dict[str, dict[str, str]] = {
    "Baumwolle und andere Naturfasern": {
        "de": "Baumwolle und andere Naturfasern",
        "en": "Cotton and other natural fibres",
        "es": "Algodón y otras fibras naturales",
        "fr": "Coton et autres fibres naturelles",
        "it": "Cotone e altre fibre naturali",
        "zh": "棉及其他天然纤维",
    },
    "Materialien tierischen Ursprungs (außer Leder), z. B. Wolle": {
        "de": "Materialien tierischen Ursprungs (außer Leder), z. B. Wolle",
        "en": "Materials of animal origin (other than leather), e.g. wool",
        "es": "Materiales de origen animal (salvo el cuero), p. ej. lana",
        "fr": "Matériaux d'origine animale (hors cuir), p. ex. laine",
        "it": "Materiali di origine animale (esclusa la pelle), p. es. lana",
        "zh": "动物来源材料（皮革除外），如羊毛",
    },
    "Leder bzw. Rindererzeugnisse": {
        "de": "Leder bzw. Rindererzeugnisse",
        "en": "Leather or cattle products",
        "es": "Cuero o productos bovinos",
        "fr": "Cuir ou produits bovins",
        "it": "Pelle o prodotti bovini",
        "zh": "皮革及牛类产品",
    },
    "Naturkautschuk": {
        "de": "Naturkautschuk", "en": "Natural rubber", "es": "Caucho natural",
        "fr": "Caoutchouc naturel", "it": "Gomma naturale", "zh": "天然橡胶",
    },
    "Zellulosebasierte Chemiefasern (z. B. Viskose, Modal, Lyocell)": {
        "de": "Zellulosebasierte Chemiefasern (z. B. Viskose, Modal, Lyocell)",
        "en": "Cellulose-based man-made fibres (e.g. viscose, modal, lyocell)",
        "es": "Fibras químicas de celulosa (p. ej. viscosa, modal, liocel)",
        "fr": "Fibres chimiques cellulosiques (p. ex. viscose, modal, lyocell)",
        "it": "Fibre chimiche cellulosiche (p. es. viscosa, modal, lyocell)",
        "zh": "纤维素基化学纤维（如粘胶、莫代尔、莱赛尔）",
    },
    "Synthetische Fasern": {
        "de": "Synthetische Fasern", "en": "Synthetic fibres", "es": "Fibras sintéticas",
        "fr": "Fibres synthétiques", "it": "Fibre sintetiche", "zh": "合成纤维",
    },
    "Recyclingmaterialien": {
        "de": "Recyclingmaterialien", "en": "Recycled materials", "es": "Materiales reciclados",
        "fr": "Matériaux recyclés", "it": "Materiali riciclati", "zh": "再生材料",
    },
    "Besondere chemische Ausrüstungen (ohne PFAS, z. B. Flammschutz, Wasserabweisung)": {
        "de": "Besondere chemische Ausrüstungen (ohne PFAS, z. B. Flammschutz, Wasserabweisung)",
        "en": "Special chemical finishes (other than PFAS, e.g. flame retardant, water repellent)",
        "es": "Acabados químicos especiales (sin PFAS, p. ej. ignífugos, hidrófugos)",
        "fr": "Apprêts chimiques particuliers (hors PFAS, p. ex. ignifuges, déperlants)",
        "it": "Finissaggi chimici particolari (esclusi PFAS, p. es. ignifughi, idrorepellenti)",
        "zh": "特殊化学整理（不含 PFAS，如阻燃、拒水）",
    },
    "PFAS-haltige Ausrüstung": {
        "de": "PFAS-haltige Ausrüstung",
        "en": "PFAS-containing finish",
        "es": "Acabado con PFAS",
        "fr": "Apprêt contenant des PFAS",
        "it": "Finissaggio contenente PFAS",
        "zh": "含 PFAS 的整理",
    },
}


SALES_MARKET_LABELS: dict[str, dict[str, str]] = {
    "Deutschland": {
        "de": "Deutschland", "en": "Germany", "es": "Alemania",
        "fr": "Allemagne", "it": "Germania", "zh": "德国",
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
    )


def normalize_lang(lang: str | None) -> str:
    """Filter auf erlaubte Codes, Default 'de'."""
    if lang and lang.lower() in LANG_CODES:
        return lang.lower()
    return "de"
