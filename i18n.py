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
        "de": "Prüfe, welche ESG-/CSR-Regulierungen für dein Unternehmen gelten.",
        "en": "Check which ESG/CSR regulations apply to your company.",
        "es": "Comprueba qué regulaciones ESG/CSR se aplican a tu empresa.",
        "fr": "Vérifiez quelles réglementations ESG/CSR s'appliquent à votre entreprise.",
        "it": "Verifica quali normative ESG/CSR si applicano alla tua azienda.",
        "zh": "查看哪些 ESG/CSR 法规适用于您的公司。",
    },
    "language_picker_label": {
        "de": "Sprache",
        "en": "Language",
        "es": "Idioma",
        "fr": "Langue",
        "it": "Lingua",
        "zh": "语言",
    },
    "disclaimer": {
        "de": "Alle Angaben ohne Gewähr.",
        "en": "All information provided without guarantee.",
        "es": "Toda la información se proporciona sin garantía.",
        "fr": "Toutes les informations sont données sans garantie.",
        "it": "Tutte le informazioni sono fornite senza garanzia.",
        "zh": "所有信息均不作担保。",
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
        "de": "Deine Daten werden pro Konto gespeichert und beim nächsten Login vorausgefüllt.",
        "en": "Your data is stored per account and pre-filled on next login.",
        "es": "Tus datos se guardan por cuenta y se rellenan previamente en el próximo inicio de sesión.",
        "fr": "Vos données sont enregistrées par compte et préremplies à la prochaine connexion.",
        "it": "I tuoi dati vengono salvati per account e precompilati al prossimo accesso.",
        "zh": "您的数据按账户保存,下次登录时自动填充。",
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
        "de": "Sucht anhand des Unternehmensnamens auf Website und Wikipedia. Es werden nur explizit gefundene Angaben übernommen — alle KI-gefüllten Felder werden hellblau umrandet und bleiben manuell änderbar.",
        "en": "Searches the company website and Wikipedia by company name. Only explicitly found values are filled in — all AI-filled fields get a light blue outline and stay editable.",
        "es": "Busca en el sitio web y Wikipedia por el nombre de la empresa. Solo se rellenan datos encontrados explícitamente; los campos rellenados por la IA se marcan con un borde azul claro y siguen siendo editables.",
        "fr": "Recherche sur le site web et Wikipédia à partir du nom de l'entreprise. Seules les valeurs trouvées explicitement sont remplies — les champs remplis par l'IA sont entourés de bleu clair et restent modifiables.",
        "it": "Cerca sul sito web e su Wikipedia in base al nome dell'azienda. Vengono inseriti solo i dati trovati esplicitamente; i campi compilati dall'IA sono contornati in azzurro e restano modificabili.",
        "zh": "根据公司名称搜索官网和维基百科。仅填写明确找到的信息——AI 填写的字段会以浅蓝色边框标出,且仍可手动修改。",
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
        "de": "Nettoumsatz pro Jahr (EUR)",
        "en": "Net revenue per year (EUR)",
        "es": "Ingresos netos anuales (EUR)",
        "fr": "Chiffre d'affaires net annuel (EUR)",
        "it": "Ricavi netti annui (EUR)",
        "zh": "年度净收入(欧元)",
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
        "de": "Führt Ihr Unternehmen Produkte aus Drittländern in die EU ein und stellt diese auf dem EU-Markt bereit bzw. bringt sie erstmals in Verkehr? Relevant u.a. für EUDR, FLR, PPWR, Ökodesign-VO, Konfliktmineralien-VO.",
        "en": "Does your company import products from third countries into the EU and make them available on the EU market or place them on the market for the first time? Relevant for EUDR, FLR, PPWR, Ecodesign Regulation, Conflict Minerals Regulation.",
        "es": "¿Su empresa importa productos de terceros países a la UE y los comercializa en el mercado de la UE o los introduce por primera vez en el mercado? Relevante para EUDR, FLR, PPWR, Reglamento de Ecodiseño, Reglamento de Minerales en Conflicto.",
        "fr": "Votre entreprise importe-t-elle des produits de pays tiers dans l'UE et les met-elle à disposition sur le marché de l'UE ou les place-t-elle pour la première fois sur le marché ? Pertinent pour EUDR, FLR, PPWR, règlement Écoconception, règlement sur les minéraux de conflit.",
        "it": "La vostra azienda importa prodotti da paesi terzi nell'UE e li mette a disposizione sul mercato UE o li immette sul mercato per la prima volta? Rilevante per EUDR, FLR, PPWR, Regolamento Ecodesign, Regolamento sui Minerali di Conflitto.",
        "zh": "贵公司是否从第三国向欧盟进口产品，并在欧盟市场上提供或首次投放市场？涉及 EUDR、FLR、PPWR、生态设计条例、冲突矿产条例等。",
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
        "de": "Mehrfachauswahl möglich. Steuert EUDR, PPWR, Ökodesign, Right-to-Repair, Konfliktmineralien.",
        "en": "Multi-select possible. Drives EUDR, PPWR, Ecodesign, Right-to-Repair, Conflict Minerals.",
        "es": "Selección múltiple posible. Afecta EUDR, PPWR, Ecodiseño, Derecho a Reparar, Minerales de Conflicto.",
        "fr": "Sélection multiple possible. Influence EUDR, PPWR, Écoconception, Droit à la Réparation, Minéraux de Conflit.",
        "it": "Selezione multipla possibile. Influenza EUDR, PPWR, Ecodesign, Diritto alla Riparazione, Minerali di Conflitto.",
        "zh": "可多选。影响 EUDR、PPWR、生态设计、维修权、冲突矿产。",
    },
    "products_label": {"de": "Kategorien", "en": "Categories", "es": "Categorías", "fr": "Catégories", "it": "Categorie", "zh": "类别"},
    "section_sites": {
        "de": "#### Standorte",
        "en": "#### Sites",
        "es": "#### Ubicaciones",
        "fr": "#### Sites",
        "it": "#### Sedi",
        "zh": "#### 场所",
    },
    "sites_hint": {
        "de": "Anzahl, Typ und Region je Standort. Weitere Zeilen legst du über „Standort hinzufügen“ an.",
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
    "whistle": {
        "de": "Für Beschäftigungsgeber mit 50 bis 249 Beschäftigten galt die Umsetzungsfrist bis 17.12.2023. "
              "In Deutschland wirkt die Richtlinie über das HinSchG.",
        "en": "For employers with 50 to 249 employees the transposition deadline ran until 17.12.2023. In "
              "Germany the directive takes effect through the HinSchG.",
        "es": "Para empleadores con 50 a 249 empleados el plazo de transposición fue hasta el 17.12.2023. En "
              "Alemania la directiva actúa a través de la HinSchG.",
        "fr": "Pour les employeurs de 50 à 249 salariés, le délai de transposition courait jusqu'au "
              "17.12.2023. En Allemagne, la directive produit ses effets via la HinSchG.",
        "it": "Per i datori di lavoro con 50-249 dipendenti il termine di recepimento era il 17.12.2023. In "
              "Germania la direttiva opera tramite la HinSchG.",
        "zh": "对于拥有 50 至 249 名员工的雇主，转化期限为 2023 年 12 月 17 日。在德国，该指令通过《举报人保护法》生效。",
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
    "konfliktmin": {
        "de": "Die Kernpflichten (Sorgfaltspflichten, Prüfung, Offenlegung) gelten seit 01.01.2021.",
        "en": "The core duties (due diligence, audit, disclosure) have applied since 01.01.2021.",
        "es": "Las obligaciones principales (diligencia debida, auditoría, divulgación) se aplican desde "
              "el 01.01.2021.",
        "fr": "Les obligations principales (diligence raisonnable, audit, publication) s'appliquent depuis "
              "le 01.01.2021.",
        "it": "Gli obblighi principali (dovere di diligenza, verifica, informativa) si applicano dal 01.01.2021.",
        "zh": "核心义务（尽职调查、审计、披露）自 2021 年 1 月 1 日起适用。",
    },
    "umweltstraf": {
        "de": "Datum der Umsetzungsfrist für die Mitgliedstaaten. Unternehmen sind mittelbar über das "
              "nationale Strafrecht betroffen.",
        "en": "Date of the transposition deadline for member states. Companies are affected indirectly "
              "through national criminal law.",
        "es": "Fecha límite de transposición para los Estados miembros. Las empresas se ven afectadas "
              "indirectamente a través del derecho penal nacional.",
        "fr": "Date limite de transposition pour les États membres. Les entreprises sont concernées "
              "indirectement via le droit pénal national.",
        "it": "Termine di recepimento per gli Stati membri. Le imprese sono interessate indirettamente "
              "tramite il diritto penale nazionale.",
        "zh": "为成员国规定的转化期限。企业通过国内刑法间接受到影响。",
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


# ---------- Begruendungs-Bausteine fuer gekoppelte Regulierungen ----------
#
# CSRD, CSRD_DE, ESRS, Taxonomie-VO, HinSchG und Whistleblower-RL werden nicht
# vom LLM bewertet, sondern von `regulations.coupling_verdict()` entschieden.
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
        "de": "Die oberste Muttergesellschaft sitzt außerhalb der EU und der Nettoumsatz beträgt "
              "{revenue} (Schwelle: mehr als 450 Mio. EUR); ob eine EU-Tochter oder "
              "Zweigniederlassung die zusätzlich nötigen 200 Mio. EUR erreicht, geht aus dem "
              "Profil nicht hervor.",
        "en": "The ultimate parent is established outside the EU and net turnover is {revenue} "
              "(threshold: more than EUR 450 million); whether an EU subsidiary or branch reaches "
              "the additionally required EUR 200 million is not stated in the profile.",
        "es": "La sociedad matriz última tiene su sede fuera de la UE y la cifra neta de negocios "
              "es de {revenue} (umbral: más de 450 millones EUR); el perfil no indica si una filial "
              "o sucursal en la UE alcanza los 200 millones EUR adicionales exigidos.",
        "fr": "La société mère ultime est établie hors de l'UE et le chiffre d'affaires net "
              "s'élève à {revenue} (seuil : plus de 450 millions EUR) ; le profil n'indique pas si "
              "une filiale ou succursale de l'UE atteint les 200 millions EUR supplémentaires "
              "requis.",
        "it": "La capogruppo ha sede fuori dall'UE e i ricavi netti ammontano a {revenue} (soglia: "
              "più di 450 milioni di EUR); dal profilo non risulta se una controllata o succursale "
              "UE raggiunga i 200 milioni di EUR ulteriormente richiesti.",
        "zh": "最终母公司设在欧盟境外，净营业额为 {revenue}（门槛：超过 4.5 亿欧元）；档案中未说明是否有欧盟子公司或分支机构"
              "达到另需的 2 亿欧元。",
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
}

COUPLING_CONCLUSIONS: dict[str, dict[str, dict[str, str]]] = {
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
    "ESRS": {
        "ja": {
            "de": "Die ESRS sind damit als verbindliches Berichtsformat anzuwenden.",
            "en": "The ESRS therefore have to be applied as the binding reporting format.",
            "es": "Por tanto, las ESRS deben aplicarse como formato de información vinculante.",
            "fr": "Les ESRS doivent donc être appliquées comme format de reporting contraignant.",
            "it": "Gli ESRS devono quindi essere applicati come formato di rendicontazione vincolante.",
            "zh": "因此必须按 ESRS 这一强制报告格式编制报告。",
        },
        "nein": {
            "de": "Ohne CSRD-Pflicht sind die ESRS nicht verbindlich anzuwenden.",
            "en": "Without a CSRD duty the ESRS are not binding.",
            "es": "Sin obligación CSRD, las ESRS no son de aplicación obligatoria.",
            "fr": "En l'absence d'obligation CSRD, les ESRS ne s'imposent pas.",
            "it": "In assenza di obbligo CSRD gli ESRS non sono vincolanti.",
            "zh": "无 CSRD 义务时，ESRS 不具强制适用性。",
        },
        "moeglich": {
            "de": "Ob die ESRS anzuwenden sind, folgt der noch zu klärenden CSRD-Pflicht.",
            "en": "Whether the ESRS apply follows the CSRD duty that still has to be clarified.",
            "es": "Que las ESRS sean aplicables depende de la obligación CSRD aún por aclarar.",
            "fr": "L'application des ESRS suit l'obligation CSRD encore à clarifier.",
            "it": "L'applicazione degli ESRS segue l'obbligo CSRD ancora da chiarire.",
            "zh": "ESRS 是否适用，取决于尚待厘清的 CSRD 义务。",
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
    "WhistleblowerRL": {
        "ja": {
            "de": "Die Richtlinie wirkt in Deutschland über das HinSchG; der interne Meldekanal ist "
                  "damit einzurichten.",
            "en": "In Germany the directive takes effect through the HinSchG; the internal "
                  "reporting channel therefore has to be set up.",
            "es": "En Alemania la Directiva actúa a través de la HinSchG; por tanto, debe "
                  "establecerse el canal interno de denuncias.",
            "fr": "En Allemagne, la directive produit ses effets via la HinSchG ; le canal de "
                  "signalement interne doit donc être mis en place.",
            "it": "In Germania la direttiva opera tramite l'HinSchG; il canale di segnalazione "
                  "interno va quindi istituito.",
            "zh": "该指令在德国通过《举报人保护法》产生效力，因此必须设立内部举报渠道。",
        },
        "nein": {
            "de": "Die über das HinSchG umgesetzte Pflicht greift damit nicht.",
            "en": "The obligation transposed via the HinSchG therefore does not apply.",
            "es": "La obligación transpuesta mediante la HinSchG no resulta por tanto aplicable.",
            "fr": "L'obligation transposée par la HinSchG ne s'applique donc pas.",
            "it": "L'obbligo recepito tramite l'HinSchG non trova quindi applicazione.",
            "zh": "因此，通过《举报人保护法》转化的义务不适用。",
        },
        "moeglich": {
            "de": "Ob die über das HinSchG umgesetzte Pflicht greift, hängt davon ab, ob das "
                  "Unternehmen zu den in § 12 Abs. 3 HinSchG aufgezählten Finanzunternehmen zählt.",
            "en": "Whether the obligation transposed via the HinSchG applies depends on whether the "
                  "company is one of the financial undertakings listed in section 12(3) HinSchG.",
            "es": "Que se aplique la obligación transpuesta mediante la HinSchG depende de si la "
                  "empresa figura entre las entidades financieras del § 12, apdo. 3, HinSchG.",
            "fr": "L'application de l'obligation transposée par la HinSchG dépend de la question de "
                  "savoir si l'entreprise fait partie des entreprises financières du § 12, al. 3, "
                  "HinSchG.",
            "it": "L'applicazione dell'obbligo recepito tramite l'HinSchG dipende dal fatto che "
                  "l'impresa rientri tra i soggetti finanziari del § 12, comma 3, HinSchG.",
            "zh": "通过《举报人保护法》转化的义务是否适用，取决于公司是否属于该法第 12 条第 3 款所列的金融企业。",
        },
    },
}

COUPLING_PASSAGES: dict[str, dict[str, str]] = {
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
    "ESRS": {
        "de": "Art. 1 der Delegierten Verordnung (EU) 2023/2772 i. V. m. Anhang I: Standards für "
              "die Berichterstattung nach Art. 19a und 29a der Richtlinie 2013/34/EU.",
        "en": "Art. 1 of Delegated Regulation (EU) 2023/2772 in conjunction with Annex I: standards "
              "for reporting under Art. 19a and 29a of Directive 2013/34/EU.",
        "es": "Art. 1 del Reglamento Delegado (UE) 2023/2772 en relación con el anexo I: normas para "
              "la información conforme a los arts. 19 bis y 29 bis de la Directiva 2013/34/UE.",
        "fr": "Art. 1er du règlement délégué (UE) 2023/2772, lu avec l'annexe I : normes pour le "
              "reporting au titre des art. 19 bis et 29 bis de la directive 2013/34/UE.",
        "it": "Art. 1 del regolamento delegato (UE) 2023/2772 in combinato disposto con l'allegato I: "
              "principi per la rendicontazione ex artt. 19 bis e 29 bis della direttiva 2013/34/UE.",
        "zh": "《授权条例》(EU) 2023/2772 第 1 条结合附件一：依《指令》2013/34/EU 第 19a 条和第 29a 条报告的准则。",
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
    "WhistleblowerRL": {
        "de": "Art. 8 Abs. 3 der Richtlinie (EU) 2019/1937: juristische Personen des privaten "
              "Sektors mit 50 oder mehr Arbeitnehmern richten interne Meldekanäle ein.",
        "en": "Art. 8(3) of Directive (EU) 2019/1937: legal entities in the private sector with 50 "
              "or more workers have to establish internal reporting channels.",
        "es": "Art. 8, apdo. 3, de la Directiva (UE) 2019/1937: las entidades jurídicas del sector "
              "privado con 50 o más trabajadores establecen canales internos de denuncia.",
        "fr": "Art. 8, par. 3, de la directive (UE) 2019/1937 : les entités juridiques du secteur "
              "privé comptant 50 travailleurs ou plus établissent des canaux de signalement interne.",
        "it": "Art. 8, par. 3, della direttiva (UE) 2019/1937: i soggetti giuridici del settore "
              "privato con 50 o più lavoratori istituiscono canali di segnalazione interni.",
        "zh": "《指令》(EU) 2019/1937 第 8 条第 3 款：拥有 50 名及以上员工的私营部门法律实体须设立内部举报渠道。",
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
    "Hauptsitz": {"de": "Hauptsitz", "en": "Headquarters", "es": "Sede central", "fr": "Siège social", "it": "Sede centrale", "zh": "总部"},
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
    "Verpackungen (eigene oder vertriebene)": {
        "de": "Verpackungen (eigene oder vertriebene)",
        "en": "Packaging (own or distributed)",
        "es": "Envases (propios o distribuidos)",
        "fr": "Emballages (propres ou distribués)",
        "it": "Imballaggi (propri o distribuiti)",
        "zh": "包装(自有或经销)",
    },
    "Elektronik / Haushaltsgeräte / IT-Hardware": {
        "de": "Elektronik / Haushaltsgeräte / IT-Hardware",
        "en": "Electronics / Appliances / IT hardware",
        "es": "Electrónica / Electrodomésticos / Hardware TI",
        "fr": "Électronique / Électroménager / Matériel IT",
        "it": "Elettronica / Elettrodomestici / Hardware IT",
        "zh": "电子产品 / 家电 / IT 硬件",
    },
    "Holz / Holzprodukte / Papier": {
        "de": "Holz / Holzprodukte / Papier",
        "en": "Wood / Wood products / Paper",
        "es": "Madera / Productos de madera / Papel",
        "fr": "Bois / Produits en bois / Papier",
        "it": "Legno / Prodotti in legno / Carta",
        "zh": "木材 / 木制品 / 纸张",
    },
    "Kaffee / Kakao": {"de": "Kaffee / Kakao", "en": "Coffee / Cocoa", "es": "Café / Cacao", "fr": "Café / Cacao", "it": "Caffè / Cacao", "zh": "咖啡 / 可可"},
    "Palmöl / Soja": {"de": "Palmöl / Soja", "en": "Palm oil / Soy", "es": "Aceite de palma / Soja", "fr": "Huile de palme / Soja", "it": "Olio di palma / Soia", "zh": "棕榈油 / 大豆"},
    "Kautschuk / Gummi": {"de": "Kautschuk / Gummi", "en": "Rubber", "es": "Caucho / Goma", "fr": "Caoutchouc", "it": "Gomma / Caucciù", "zh": "橡胶"},
    "Rinder / Rindsprodukte / Leder": {
        "de": "Rinder / Rindsprodukte / Leder",
        "en": "Cattle / Beef products / Leather",
        "es": "Bovino / Productos bovinos / Cuero",
        "fr": "Bovins / Produits bovins / Cuir",
        "it": "Bovini / Prodotti bovini / Pelle",
        "zh": "牛 / 牛肉产品 / 皮革",
    },
    "Zinn / Tantal / Wolfram / Gold (Direktimport)": {
        "de": "Zinn / Tantal / Wolfram / Gold (Direktimport)",
        "en": "Tin / Tantalum / Tungsten / Gold (direct import)",
        "es": "Estaño / Tantalio / Tungsteno / Oro (importación directa)",
        "fr": "Étain / Tantale / Tungstène / Or (import direct)",
        "it": "Stagno / Tantalio / Tungsteno / Oro (import diretto)",
        "zh": "锡 / 钽 / 钨 / 金(直接进口)",
    },
    "Chemische Stoffe": {"de": "Chemische Stoffe", "en": "Chemicals", "es": "Sustancias químicas", "fr": "Substances chimiques", "it": "Sostanze chimiche", "zh": "化学品"},
    "Textilien / Bekleidung / Leder": {
        "de": "Textilien / Bekleidung / Leder",
        "en": "Textiles / Clothing / Leather",
        "es": "Textiles / Ropa / Cuero",
        "fr": "Textiles / Habillement / Cuir",
        "it": "Tessili / Abbigliamento / Pelletteria",
        "zh": "纺织品 / 服装 / 皮革",
    },
    "Möbel / Baustoffe": {
        "de": "Möbel / Baustoffe",
        "en": "Furniture / Building materials",
        "es": "Muebles / Materiales de construcción",
        "fr": "Meubles / Matériaux de construction",
        "it": "Mobili / Materiali edili",
        "zh": "家具 / 建材",
    },
    "Lebensmittel / Getränke": {
        "de": "Lebensmittel / Getränke",
        "en": "Food / Beverages",
        "es": "Alimentos / Bebidas",
        "fr": "Alimentation / Boissons",
        "it": "Alimentare / Bevande",
        "zh": "食品 / 饮料",
    },
    "Keine physischen Produkte (nur Dienstleistung/Software)": {
        "de": "Keine physischen Produkte (nur Dienstleistung/Software)",
        "en": "No physical products (services/software only)",
        "es": "Sin productos físicos (solo servicios/software)",
        "fr": "Aucun produit physique (services/logiciels uniquement)",
        "it": "Nessun prodotto fisico (solo servizi/software)",
        "zh": "无实体产品(仅服务/软件)",
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


def normalize_lang(lang: str | None) -> str:
    """Filter auf erlaubte Codes, Default 'de'."""
    if lang and lang.lower() in LANG_CODES:
        return lang.lower()
    return "de"
