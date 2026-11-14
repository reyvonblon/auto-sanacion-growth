#!/usr/bin/env python3
"""SQLite persistence layer for the Auto Sanación Funnel, School, and Francis CRM."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "autosanacion.db"
BOOK_PROFILE_PATH = PROJECT_ROOT / "config" / "book_profile.json"


def get_db_path() -> Path:
    env_path = os.environ.get("AUTOSANACION_DB_PATH")
    return Path(env_path) if env_path else DEFAULT_DB_PATH


def get_connection() -> sqlite3.Connection:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def init_db() -> None:
    """Create tables if missing and seed initial config & School curriculum."""
    conn = get_connection()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                whatsapp TEXT DEFAULT '',
                source TEXT DEFAULT 'landing',
                stage TEXT DEFAULT 'nuevo_lead',
                notes TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sales_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_label TEXT NOT NULL,
                marketplace TEXT NOT NULL,
                units INTEGER DEFAULT 0,
                kenp INTEGER DEFAULT 0,
                royalty_usd REAL DEFAULT 0.0,
                ad_spend_usd REAL DEFAULT 0.0,
                orders_ads INTEGER DEFAULT 0,
                source TEXT DEFAULT 'manual',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS school_modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_index INTEGER NOT NULL,
                chapter_ref TEXT NOT NULL,
                title TEXT NOT NULL,
                subtitle TEXT NOT NULL,
                description TEXT NOT NULL,
                qr_slug TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS school_lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id INTEGER NOT NULL,
                order_index INTEGER NOT NULL,
                title TEXT NOT NULL,
                duration_minutes INTEGER DEFAULT 12,
                video_url TEXT DEFAULT '',
                reading_guide TEXT NOT NULL,
                exercise_prompt TEXT NOT NULL,
                FOREIGN KEY (module_id) REFERENCES school_modules(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS student_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                lesson_id INTEGER NOT NULL,
                completed INTEGER DEFAULT 0,
                reflection_text TEXT DEFAULT '',
                francis_feedback TEXT DEFAULT '',
                updated_at TEXT NOT NULL,
                UNIQUE(lead_id, lesson_id),
                FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE,
                FOREIGN KEY (lesson_id) REFERENCES school_lessons(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS qr_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT NOT NULL,
                chapter_ref TEXT DEFAULT '',
                user_agent TEXT DEFAULT '',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS outbox_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                channel TEXT NOT NULL,
                recipient TEXT DEFAULT '',
                subject TEXT DEFAULT '',
                body TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                scheduled_for TEXT NOT NULL,
                sent_at TEXT DEFAULT '',
                error_msg TEXT DEFAULT '',
                created_at TEXT NOT NULL
            );
            """
        )
        _seed_defaults(conn)
        conn.commit()
    finally:
        conn.close()


def _seed_defaults(conn: sqlite3.Connection) -> None:
    profile = {}
    if BOOK_PROFILE_PATH.exists():
        profile = json.loads(BOOK_PROFILE_PATH.read_text(encoding="utf-8"))
    book = profile.get("book", {})

    default_settings = {
        "book_title": book.get(
            "title",
            "AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar",
        ),
        "author_name": book.get("author", "Francis Jaramillo"),
        "isbn13": book.get("isbn13_paperback", "979-8403609579"),
        "asin_kindle": book.get("asin_kindle", "B09QN8HTQQ"),
        "asin_paperback": book.get("asin_paperback", "B09QN8HTQQ"),
        "asin_english": book.get("asin_english", "B09XZHFXDK"),
        "asin_audible": book.get("asin_audible", "B0D2MMD456"),
        "amazon_domain": "amazon.com",
        "whatsapp_number": "",
        "school_welcome_message": (
            "Bienvenido a la Escuela Auto Sanación. El libro es tu mapa; aquí "
            "caminamos paso a paso con ejercicios prácticos y acompañamiento."
        ),
    }
    for k, v in default_settings.items():
        conn.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            (k, str(v)),
        )

    existing_modules = conn.execute("SELECT COUNT(*) FROM school_modules").fetchone()[0]
    if existing_modules == 0:
        modules_seed = [
            (
                1,
                "Capítulo 1",
                "El Despertar de tus Recursos Internos",
                "Comprender la inteligencia biológica y emocional del cuerpo",
                "Base fundamental del libro: cómo dejar de vivir en alerta constante y activar los mecanismos naturales de equilibrio.",
                "cap-1",
                [
                    (
                        1,
                        "Tu cuerpo escucha lo que sientes",
                        12,
                        "",
                        "Lee la introducción y el Capítulo 1 del libro. Subraya las frases donde reconozcas señales que tu cuerpo te ha estado enviando.",
                        "Escribe 3 señales físicas o emocionales que hoy notas en tu cuerpo y qué mensaje crees que intentan darte.",
                    ),
                    (
                        2,
                        "Pausa Integrativa de 5 Minutos",
                        8,
                        "",
                        "Practica la respiración consciente descrita en el cierre del módulo antes de dormir durante 3 días seguidos.",
                        "¿Qué cambió en tu nivel de tensión o claridad mental después de hacer la pausa integrativa?",
                    ),
                ],
            ),
            (
                2,
                "Capítulo 2",
                "Mente, Emoción y Biología (Psiconeuroinmunología)",
                "Del miedo y el diagnóstico a la participación activa en tu bienestar",
                "Cómo los pensamientos sostenidos, las heridas no expresadas y el estrés crónico dialogan con el sistema inmunológico.",
                "cap-2",
                [
                    (
                        1,
                        "De víctima de la incertidumbre a protagonista",
                        15,
                        "",
                        "Reflexiona sobre el testimonio de Francis enfrentando el cáncer en el embarazo y cómo transformó el pánico en acción serena.",
                        "Identifica una situación actual que te genere miedo e indica qué parte SÍ depende de tu cuidado diario.",
                    )
                ],
            ),
            (
                3,
                "Capítulo 3",
                "Sanación Emocional y Teoterapia Familiar",
                "Soltar cargas invisibles, perdón y vínculos que sanan",
                "Herramientas psicológicas y espirituales para liberar duelos congelados, culpa y dinámicas familiares que agotan.",
                "cap-3",
                [
                    (
                        1,
                        "Mapa emocional y liberación del peso interior",
                        14,
                        "",
                        "Revisa el capítulo sobre emociones retenidas y realiza la carta terapéutica (no enviada) que propone la autora.",
                        "Sin entrar en detalles que no desees compartir, ¿qué emoción decidiste soltar hoy y qué paz te deja?",
                    )
                ],
            ),
            (
                4,
                "Capítulo 4",
                "Hábitos Diarios de Medicina Integrativa",
                "Sueño, alimentación consciente, calma y coherencia diaria",
                "Cómo traducir la teoría del libro en una rutina sencilla y sostenible para cuerpo, mente y alma.",
                "cap-4",
                [
                    (
                        1,
                        "Tu protocolo personal de 3 hábitos",
                        11,
                        "",
                        "Elige solo 3 micro-hábitos del libro (descanso, alimentación antiinflamatoria, oración/meditación o movimiento suave).",
                        "Comprométete aquí con tus 3 micro-hábitos para los próximos 7 días.",
                    )
                ],
            ),
            (
                5,
                "Capítulo 5",
                "Resiliencia en Procesos Difíciles",
                "Acompañamiento para pacientes, cuidadores y momentos de crisis",
                "Guía práctica para sostener la esperanza cuando la realidad médica o emocional exige fortaleza diaria.",
                "cap-5",
                [
                    (
                        1,
                        "Red de apoyo y diálogo compasivo",
                        13,
                        "",
                        "Aplica las pautas de comunicación compasiva contigo mismo y con tu familia vistas en este bloque del libro.",
                        "¿Qué frase de aliento o verdad necesitas recordarte cada mañana esta semana?",
                    )
                ],
            ),
            (
                6,
                "Cierre e Integración",
                "Plan de Vida y Comunidad Auto Sanación",
                "Sostener tu proceso y compartir el mensaje",
                "Evaluación de avances desde el día 1, continuidad con Francis y cómo multiplicar el bienestar en tu entorno.",
                "cap-6",
                [
                    (
                        1,
                        "Tu antes y después con el libro",
                        10,
                        "",
                        "Compara tus respuestas del Módulo 1 con tu estado emocional y hábitos actuales.",
                        "¿Cuál fue el aprendizaje más valioso que te llevas del libro y las clases? Si deseas, déjale un mensaje directo a Francis.",
                    )
                ],
            ),
        ]

        for order_idx, ch_ref, title, subtitle, desc, qr_slug, lessons in modules_seed:
            cur = conn.execute(
                """
                INSERT INTO school_modules (order_index, chapter_ref, title, subtitle, description, qr_slug)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (order_idx, ch_ref, title, subtitle, desc, qr_slug),
            )
            mod_id = cur.lastrowid
            for l_idx, l_title, dur, v_url, guide, prompt in lessons:
                conn.execute(
                    """
                    INSERT INTO school_lessons
                        (module_id, order_index, title, duration_minutes, video_url, reading_guide, exercise_prompt)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (mod_id, l_idx, l_title, dur, v_url, guide, prompt),
                )


def get_settings() -> dict[str, str]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
        return {r["key"]: r["value"] for r in rows}
    finally:
        conn.close()


def update_settings(updates: dict[str, Any]) -> dict[str, str]:
    conn = get_connection()
    try:
        for k, v in updates.items():
            conn.execute(
                "INSERT INTO settings (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (str(k), str(v if v is not None else "")),
            )
        conn.commit()
    finally:
        conn.close()
    return get_settings()


def upsert_lead(
    name: str,
    email: str,
    whatsapp: str = "",
    source: str = "landing",
    stage: str = "nuevo_lead",
    notes: str = "",
) -> dict[str, Any]:
    clean_email = email.strip().lower()
    clean_name = name.strip()
    if not clean_email or not clean_name:
        raise ValueError("Nombre y correo son obligatorios.")
    ts = now_iso()
    conn = get_connection()
    try:
        existing = conn.execute("SELECT * FROM leads WHERE email = ?", (clean_email,)).fetchone()
        if existing:
            conn.execute(
                """
                UPDATE leads
                SET name = ?,
                    whatsapp = CASE WHEN ? != '' THEN ? ELSE whatsapp END,
                    notes = CASE WHEN ? != '' THEN ? ELSE notes END,
                    updated_at = ?
                WHERE email = ?
                """,
                (clean_name, whatsapp.strip(), whatsapp.strip(), notes.strip(), notes.strip(), ts, clean_email),
            )
        else:
            cur = conn.execute(
                """
                INSERT INTO leads (name, email, whatsapp, source, stage, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (clean_name, clean_email, whatsapp.strip(), source.strip() or "landing", stage, notes.strip(), ts, ts),
            )
            new_lead_id = cur.lastrowid
            from datetime import timedelta

            day3_ts = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
            conn.execute(
                """
                INSERT INTO outbox_jobs (lead_id, channel, recipient, subject, body, status, scheduled_for, created_at)
                VALUES (?, 'email', ?, ?, ?, 'pending', ?, ?)
                """,
                (
                    new_lead_id,
                    clean_email,
                    "Tu acceso a la Escuela Auto Sanación + Pausa Integrativa",
                    f"Hola {clean_name},\n\nGracias por acercarte a Auto Sanación. Ya tienes acceso abierto a la Escuela paso a paso y a la guía práctica de Pausa Integrativa de 5 minutos.\n\nCon cariño,\nFrancis Jaramillo",
                    ts,
                    ts,
                ),
            )
            conn.execute(
                """
                INSERT INTO outbox_jobs (lead_id, channel, recipient, subject, body, status, scheduled_for, created_at)
                VALUES (?, 'email', ?, ?, ?, 'pending', ?, ?)
                """,
                (
                    new_lead_id,
                    clean_email,
                    "Cómo activar los recursos de tu cuerpo (y el libro en Amazon)",
                    f"Hola {clean_name},\n\nCuando enfrenté un diagnóstico difícil durante mi embarazo, entendí que el libro debía ser una guía práctica de cuerpo, mente y alma. Si aún no tienes tu ejemplar en Amazon o quieres continuar el Capítulo 1 en la Escuela, responde a este correo.\n\nFrancis Jaramillo",
                    day3_ts,
                    ts,
                ),
            )
        conn.commit()
        row = conn.execute("SELECT * FROM leads WHERE email = ?", (clean_email,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def list_leads(search: str = "", stage: str = "") -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        query = "SELECT * FROM leads WHERE 1=1"
        params: list[Any] = []
        if search.strip():
            like = f"%{search.strip().lower()}%"
            query += " AND (LOWER(name) LIKE ? OR LOWER(email) LIKE ? OR LOWER(whatsapp) LIKE ?)"
            params.extend([like, like, like])
        if stage.strip():
            query += " AND stage = ?"
            params.append(stage.strip())
        query += " ORDER BY updated_at DESC, id DESC"
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def update_lead(lead_id: int, stage: str | None = None, notes: str | None = None) -> dict[str, Any] | None:
    conn = get_connection()
    try:
        existing = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
        if not existing:
            return None
        new_stage = stage if stage is not None else existing["stage"]
        new_notes = notes if notes is not None else existing["notes"]
        conn.execute(
            "UPDATE leads SET stage = ?, notes = ?, updated_at = ? WHERE id = ?",
            (new_stage, new_notes, now_iso(), lead_id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def add_sale_entry(
    period_label: str,
    marketplace: str,
    units: int,
    kenp: int,
    royalty_usd: float,
    ad_spend_usd: float = 0.0,
    orders_ads: int = 0,
    source: str = "manual",
) -> dict[str, Any]:
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            INSERT INTO sales_entries
                (period_label, marketplace, units, kenp, royalty_usd, ad_spend_usd, orders_ads, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                period_label.strip() or datetime.now().strftime("%Y-%m-%d"),
                marketplace.strip() or "Amazon.com",
                int(units),
                int(kenp),
                float(royalty_usd),
                float(ad_spend_usd),
                int(orders_ads),
                source,
                now_iso(),
            ),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM sales_entries WHERE id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def list_sales() -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM sales_entries ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_school_curriculum() -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        modules = [
            dict(r)
            for r in conn.execute(
                "SELECT * FROM school_modules ORDER BY order_index ASC, id ASC"
            ).fetchall()
        ]
        lessons = [
            dict(r)
            for r in conn.execute(
                "SELECT * FROM school_lessons ORDER BY module_id ASC, order_index ASC, id ASC"
            ).fetchall()
        ]
        lessons_by_mod: dict[int, list[dict[str, Any]]] = {}
        for lesson in lessons:
            lessons_by_mod.setdefault(lesson["module_id"], []).append(lesson)
        for mod in modules:
            mod["lessons"] = lessons_by_mod.get(mod["id"], [])
        return modules
    finally:
        conn.close()


def update_lesson(
    lesson_id: int,
    title: str | None = None,
    video_url: str | None = None,
    reading_guide: str | None = None,
    exercise_prompt: str | None = None,
) -> dict[str, Any] | None:
    conn = get_connection()
    try:
        existing = conn.execute("SELECT * FROM school_lessons WHERE id = ?", (lesson_id,)).fetchone()
        if not existing:
            return None
        conn.execute(
            """
            UPDATE school_lessons
            SET title = ?, video_url = ?, reading_guide = ?, exercise_prompt = ?
            WHERE id = ?
            """,
            (
                title if title is not None else existing["title"],
                video_url if video_url is not None else existing["video_url"],
                reading_guide if reading_guide is not None else existing["reading_guide"],
                exercise_prompt if exercise_prompt is not None else existing["exercise_prompt"],
                lesson_id,
            ),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM school_lessons WHERE id = ?", (lesson_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def create_lesson(
    module_id: int,
    title: str,
    video_url: str = "",
    reading_guide: str = "",
    exercise_prompt: str = "",
    duration_minutes: int = 12,
) -> dict[str, Any]:
    conn = get_connection()
    try:
        max_order = conn.execute(
            "SELECT COALESCE(MAX(order_index), 0) FROM school_lessons WHERE module_id = ?",
            (module_id,),
        ).fetchone()[0]
        cur = conn.execute(
            """
            INSERT INTO school_lessons
                (module_id, order_index, title, duration_minutes, video_url, reading_guide, exercise_prompt)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (module_id, int(max_order) + 1, title.strip(), int(duration_minutes), video_url.strip(), reading_guide.strip(), exercise_prompt.strip()),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM school_lessons WHERE id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def save_student_progress(
    email: str,
    name: str,
    lesson_id: int,
    completed: bool,
    reflection_text: str,
    whatsapp: str = "",
) -> dict[str, Any]:
    lead = upsert_lead(
        name=name or email.split("@")[0],
        email=email,
        whatsapp=whatsapp,
        source="escuela",
        stage="en_escuela",
    )
    conn = get_connection()
    try:
        conn.execute(
            """
            UPDATE leads
            SET stage = CASE WHEN stage = 'nuevo_lead' THEN 'en_escuela' ELSE stage END,
                updated_at = ?
            WHERE id = ?
            """,
            (now_iso(), lead["id"]),
        )
        conn.execute(
            """
            INSERT INTO student_progress (lead_id, lesson_id, completed, reflection_text, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(lead_id, lesson_id) DO UPDATE SET
                completed = excluded.completed,
                reflection_text = excluded.reflection_text,
                updated_at = excluded.updated_at
            """,
            (lead["id"], int(lesson_id), 1 if completed else 0, reflection_text.strip(), now_iso()),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM student_progress WHERE lead_id = ? AND lesson_id = ?",
            (lead["id"], int(lesson_id)),
        ).fetchone()
        return {"lead": lead, "progress": dict(row)}
    finally:
        conn.close()


def get_student_progress_by_email(email: str) -> dict[str, Any]:
    clean_email = email.strip().lower()
    conn = get_connection()
    try:
        lead = conn.execute("SELECT * FROM leads WHERE email = ?", (clean_email,)).fetchone()
        if not lead:
            return {"found": False, "lead": None, "items": []}
        rows = conn.execute(
            "SELECT * FROM student_progress WHERE lead_id = ?",
            (lead["id"],),
        ).fetchall()
        return {"found": True, "lead": dict(lead), "items": [dict(r) for r in rows]}
    finally:
        conn.close()


def list_student_reflections() -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT
                sp.id AS progress_id,
                sp.lead_id,
                sp.lesson_id,
                sp.completed,
                sp.reflection_text,
                sp.francis_feedback,
                sp.updated_at,
                l.name AS student_name,
                l.email AS student_email,
                l.whatsapp AS student_whatsapp,
                l.stage AS student_stage,
                sl.title AS lesson_title,
                sm.chapter_ref AS chapter_ref,
                sm.title AS module_title
            FROM student_progress sp
            JOIN leads l ON l.id = sp.lead_id
            JOIN school_lessons sl ON sl.id = sp.lesson_id
            JOIN school_modules sm ON sm.id = sl.module_id
            ORDER BY sp.updated_at DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def save_francis_feedback(progress_id: int, feedback: str) -> dict[str, Any] | None:
    conn = get_connection()
    try:
        existing = conn.execute("SELECT * FROM student_progress WHERE id = ?", (progress_id,)).fetchone()
        if not existing:
            return None
        conn.execute(
            "UPDATE student_progress SET francis_feedback = ?, updated_at = ? WHERE id = ?",
            (feedback.strip(), now_iso(), progress_id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM student_progress WHERE id = ?", (progress_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def log_qr_scan(slug: str, chapter_ref: str = "", user_agent: str = "") -> dict[str, Any]:
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO qr_events (slug, chapter_ref, user_agent, created_at) VALUES (?, ?, ?, ?)",
            (slug.strip(), chapter_ref, user_agent[:240], now_iso()),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM qr_events WHERE id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def get_qr_context(slug: str) -> dict[str, Any]:
    conn = get_connection()
    try:
        mod = conn.execute("SELECT * FROM school_modules WHERE qr_slug = ?", (slug.strip(),)).fetchone()
        if mod:
            return {
                "slug": slug,
                "chapter_ref": mod["chapter_ref"],
                "title": mod["title"],
                "subtitle": mod["subtitle"],
                "description": mod["description"],
                "module_id": mod["id"],
            }
        presets = {
            "contacto": {
                "slug": "contacto",
                "chapter_ref": "Contacto Directo",
                "title": "Habla directamente con Francis Jaramillo",
                "subtitle": "Acompañamiento, consultas y comunidad Auto Sanación",
                "description": "Escaneaste el QR de contacto directo del libro. Escríbele a Francis por WhatsApp o únete a la Escuela Auto Sanación.",
                "module_id": 1,
            },
            "escuela": {
                "slug": "escuela",
                "chapter_ref": "Escuela Auto Sanación",
                "title": "Profundiza el libro paso a paso en la Escuela",
                "subtitle": "Clases, ejercicios guiados y seguimiento personal",
                "description": "El libro es la columna vertebral; aquí profundizas cada capítulo con prácticas guiadas por Francis.",
                "module_id": 1,
            },
            "resena": {
                "slug": "resena",
                "chapter_ref": "Comunidad de Lectores",
                "title": "¿Cómo te ayudó Auto Sanación?",
                "subtitle": "Comparte tu experiencia honesta y recibe acompañamiento",
                "description": "Tu opinión en Amazon ayuda a que más personas descubran estas herramientas de bienestar.",
                "module_id": 6,
            },
        }
        return presets.get(
            slug.strip(),
            {
                "slug": slug,
                "chapter_ref": "Libro Inteligente",
                "title": "Bienvenido desde el QR de Auto Sanación",
                "subtitle": "Conecta con Francis Jaramillo y profundiza en la Escuela",
                "description": "Has accedido desde un código QR del libro. Elige cómo quieres continuar tu proceso.",
                "module_id": 1,
            },
        )
    finally:
        conn.close()


def get_dashboard_metrics() -> dict[str, Any]:
    conn = get_connection()
    try:
        today_prefix = datetime.now().strftime("%Y-%m-%d")
        total_leads = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        leads_today = conn.execute(
            "SELECT COUNT(*) FROM leads WHERE created_at LIKE ?", (f"{today_prefix}%",)
        ).fetchone()[0]
        students_count = conn.execute(
            "SELECT COUNT(DISTINCT lead_id) FROM student_progress"
        ).fetchone()[0]
        pending_feedback = conn.execute(
            "SELECT COUNT(*) FROM student_progress WHERE reflection_text != '' AND francis_feedback = ''"
        ).fetchone()[0]
        qr_scans = conn.execute("SELECT COUNT(*) FROM qr_events").fetchone()[0]
        sales_agg = conn.execute(
            """
            SELECT
                COALESCE(SUM(units), 0) AS total_units,
                COALESCE(SUM(kenp), 0) AS total_kenp,
                COALESCE(SUM(royalty_usd), 0.0) AS total_royalty,
                COALESCE(SUM(ad_spend_usd), 0.0) AS total_ad_spend
            FROM sales_entries
            """
        ).fetchone()
        total_royalty = round(float(sales_agg["total_royalty"]), 2)
        total_ad_spend = round(float(sales_agg["total_ad_spend"]), 2)
        tacos = round((total_ad_spend / total_royalty * 100.0), 2) if total_royalty > 0 else None

        qr_by_slug = [
            dict(r)
            for r in conn.execute(
                "SELECT slug, COUNT(*) AS scans FROM qr_events GROUP BY slug ORDER BY scans DESC LIMIT 10"
            ).fetchall()
        ]
        return {
            "total_leads": total_leads,
            "leads_today": leads_today,
            "students_count": students_count,
            "pending_feedback": pending_feedback,
            "qr_scans": qr_scans,
            "qr_by_slug": qr_by_slug,
            "total_units": int(sales_agg["total_units"]),
            "total_kenp": int(sales_agg["total_kenp"]),
            "total_royalty_usd": total_royalty,
            "total_ad_spend_usd": total_ad_spend,
            "tacos_percent": tacos,
            "net_profit_usd": round(total_royalty - total_ad_spend, 2),
        }
    finally:
        conn.close()


def queue_outbox_job(
    channel: str,
    body: str,
    recipient: str = "",
    subject: str = "",
    lead_id: int | None = None,
    scheduled_for: str | None = None,
) -> dict[str, Any]:
    ts = now_iso()
    sched = scheduled_for or ts
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            INSERT INTO outbox_jobs (lead_id, channel, recipient, subject, body, status, scheduled_for, created_at)
            VALUES (?, ?, ?, ?, ?, 'pending', ?, ?)
            """,
            (lead_id, channel.strip(), recipient.strip(), subject.strip(), body.strip(), sched, ts),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM outbox_jobs WHERE id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def list_outbox_jobs(status: str = "") -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        if status.strip():
            rows = conn.execute(
                "SELECT * FROM outbox_jobs WHERE status = ? ORDER BY scheduled_for ASC, id DESC",
                (status.strip(),),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM outbox_jobs ORDER BY id DESC LIMIT 100"
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def update_outbox_job(job_id: int, status: str, error_msg: str = "") -> None:
    conn = get_connection()
    try:
        sent_at = now_iso() if status == "sent" else ""
        conn.execute(
            "UPDATE outbox_jobs SET status = ?, sent_at = ?, error_msg = ? WHERE id = ?",
            (status, sent_at, error_msg[:400], job_id),
        )
        conn.commit()
    finally:
        conn.close()

