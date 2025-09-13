# pip install PyQt6
import sys
import sqlite3
import calendar
from datetime import date, datetime, timedelta

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit, QCheckBox,
    QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QGroupBox,
    QHeaderView, QSplitter
)
from PyQt6.QtCore import Qt, QDate, QTimer, QSettings
from PyQt6.QtGui import QFont, QColor, QBrush, QPalette


# --- Helpers -----------------------------------------------------------------
def today_iso():
    return date.today().isoformat()


def now_iso():
    return datetime.now().replace(microsecond=0).isoformat()


def fmt_date_readable(iso: str | None) -> str:
    if not iso:
        return ""
    y, m, d = map(int, iso.split("-"))
    return f"{d:02d}.{m:02d}.{y:04d}"


def add_months_iso(iso_str: str | None, months: int = 1) -> str | None:
    if not iso_str:
        return None
    y, m, d = map(int, iso_str.split("-"))
    m_new = m - 1 + months
    y_new = y + m_new // 12
    m_new = m_new % 12 + 1
    day = min(d, calendar.monthrange(y_new, m_new)[1])
    return f"{y_new:04d}-{m_new:02d}-{day:02d}"


def qdate_to_iso(qd: QDate) -> str:
    return qd.toString("yyyy-MM-dd")


# --- Theme manager -----------------------------------------------------------
class ThemeManager:
    LIGHT = "light"
    DARK = "dark"

    COLORS_LIGHT = {
        "window": "#ffffff",
        "panel": "#f3f4f6",
        "text": "#111827",
        "muted": "#6b7280",
        "input_bg": "#ffffff",
        "input_border": "#cfcfcf",
        "alt_base": "#f9fafb",
        "focus": "#6aa9ff",
        "btn_bg": "#3b82f6",
        "btn_hover": "#2563eb",
        "btn_disabled": "#9aa5b1",
        "header_bg": "#f3f4f6",
        "header_border": "#e5e7eb",
        "group_border": "#e5e7eb",
        "gridline": "#e5e7eb",
        "row_overdue": "#fde2e2",
        "row_soon": "#fff6cc",
        "row_done": "#e7f7e7",
        "select_bg": "#3b82f6",
        "select_text": "#ffffff",
        "link": "#2563eb",
    }

    COLORS_DARK = {
        "window": "#0f172a",  # slate-900
        "panel": "#111827",  # slate-800
        "text": "#e5e7eb",
        "muted": "#9ca3af",
        "input_bg": "#0b1220",
        "input_border": "#374151",
        "alt_base": "#0e1a2b",
        "focus": "#60a5fa",
        "btn_bg": "#2563eb",
        "btn_hover": "#1d4ed8",
        "btn_disabled": "#4b5563",
        "header_bg": "#111827",
        "header_border": "#374151",
        "group_border": "#374151",
        "gridline": "#334155",
        "row_overdue": "#3b1a1a",
        "row_soon": "#3b2f06",
        "row_done": "#10361f",
        "select_bg": "#2563eb",
        "select_text": "#ffffff",
        "link": "#93c5fd",
    }

    def __init__(self):
        self.settings = QSettings("TaskMaster", "TaskMasterApp")

    def load(self) -> str:
        # По умолчанию тёмная — как просили
        return self.settings.value("ui/theme", self.DARK)

    def save(self, theme: str):
        self.settings.setValue("ui/theme", theme)

    def apply(self, theme: str) -> dict:
        app = QApplication.instance()
        if app is None:
            return {}

        colors = self.COLORS_DARK if theme == self.DARK else self.COLORS_LIGHT

        # Palette
        if theme == self.DARK:
            pal = QPalette()
            pal.setColor(QPalette.ColorRole.Window, QColor(colors["window"]))
            pal.setColor(QPalette.ColorRole.WindowText, QColor(colors["text"]))
            pal.setColor(QPalette.ColorRole.Base, QColor(colors["input_bg"]))
            pal.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["alt_base"]))
            pal.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["panel"]))
            pal.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text"]))
            pal.setColor(QPalette.ColorRole.Text, QColor(colors["text"]))
            pal.setColor(QPalette.ColorRole.Button, QColor(colors["panel"]))
            pal.setColor(QPalette.ColorRole.ButtonText, QColor(colors["text"]))
            pal.setColor(QPalette.ColorRole.BrightText, QColor("#ff0000"))
            pal.setColor(QPalette.ColorRole.Link, QColor(colors["link"]))
            pal.setColor(QPalette.ColorRole.Highlight, QColor(colors["select_bg"]))
            pal.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["select_text"]))
            pal.setColor(QPalette.ColorRole.PlaceholderText, QColor(colors["muted"]))
        else:
            pal = app.style().standardPalette()
            pal.setColor(QPalette.ColorRole.Highlight, QColor(colors["select_bg"]))
            pal.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["select_text"]))
            pal.setColor(QPalette.ColorRole.Link, QColor(colors["link"]))
            pal.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["alt_base"]))
            pal.setColor(QPalette.ColorRole.PlaceholderText, QColor(colors["muted"]))

        app.setPalette(pal)

        # Stylesheet (общий)
        style = f"""
            QWidget {{
                font-size: 11pt;
                color: {colors['text']};
                background: {colors['window']};
            }}
            QLineEdit, QTextEdit, QComboBox, QDateEdit {{
                padding: 6px; border: 1px solid {colors['input_border']}; border-radius: 6px;
                background: {colors['input_bg']};
                color: {colors['text']};
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {{
                border: 1px solid {colors['focus']};
            }}
            QPushButton {{
                padding: 8px 12px; border: 1px solid {colors['btn_bg']};
                background: {colors['btn_bg']}; color: white; border-radius: 6px;
            }}
            QPushButton:hover {{ background: {colors['btn_hover']}; }}
            QPushButton:disabled {{ background: {colors['btn_disabled']}; border-color: {colors['btn_disabled']}; }}

            QHeaderView::section {{
                background: {colors['header_bg']}; padding: 6px; border: 1px solid {colors['header_border']};
                font-weight: 600; color: {colors['text']};
            }}
            QGroupBox {{
                border: 1px solid {colors['group_border']}; border-radius: 8px; margin-top: 10px; padding-top: 14px;
            }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 4px; }}
            QTableView {{ gridline-color: {colors['gridline']}; }}
        """
        app.setStyleSheet(style)
        return colors


# --- Repository (SQLite) -----------------------------------------------------
class TaskRepository:
    def __init__(self, db_path: str = "tasks.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                priority TEXT CHECK(priority IN ('Low','Medium','High')) NOT NULL DEFAULT 'Medium',
                due_date TEXT,
                status TEXT CHECK(status IN ('Todo','In Progress','Done')) NOT NULL DEFAULT 'Todo',
                repeat_monthly INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due ON tasks(due_date)")
        self.conn.commit()

    def add_task(self, name, description, priority, due_date_iso, status, repeat_monthly: bool) -> int:
        cur = self.conn.cursor()
        now = now_iso()
        cur.execute("""
            INSERT INTO tasks (name, description, priority, due_date, status, repeat_monthly, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, description, priority, due_date_iso, status, int(repeat_monthly), now, now))
        self.conn.commit()
        return cur.lastrowid

    def update_task(self, task_id: int, name, description, priority, due_date_iso, status, repeat_monthly: bool):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE tasks
            SET name=?, description=?, priority=?, due_date=?, status=?, repeat_monthly=?, updated_at=?
            WHERE id=?
        """, (name, description, priority, due_date_iso, status, int(repeat_monthly), now_iso(), task_id))
        self.conn.commit()

    def delete_task(self, task_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    def get_task(self, task_id: int) -> sqlite3.Row | None:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        return cur.fetchone()

    def mark_done(self, task_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        row = cur.fetchone()
        if not row:
            return False
        cur.execute("UPDATE tasks SET status='Done', updated_at=? WHERE id=?", (now_iso(), task_id))
        if row["repeat_monthly"]:
            next_due = add_months_iso(row["due_date"]) if row["due_date"] else None
            cur.execute("""
                INSERT INTO tasks (name, description, priority, due_date, status, repeat_monthly, created_at, updated_at)
                VALUES (?, ?, ?, ?, 'Todo', ?, ?, ?)
            """, (row["name"], row["description"], row["priority"], next_due, row["repeat_monthly"], now_iso(),
                  now_iso()))
        self.conn.commit()
        return True

    def list_tasks(self, search: str | None, status: str | None, priority: str | None,
                   overdue_only: bool, only_this_month: bool):
        sql = "SELECT * FROM tasks WHERE 1=1"
        params: list = []

        if search:
            sql += " AND (name LIKE ? OR description LIKE ?)"
            like = f"%{search}%"
            params += [like, like]
        if status and status != "Все":
            sql += " AND status=?"
            params.append(status)
        if priority and priority != "Все":
            sql += " AND priority=?"
            params.append(priority)
        if overdue_only:
            sql += " AND status!='Done' AND due_date IS NOT NULL AND date(due_date) < date('now','localtime')"
        if only_this_month:
            sql += " AND due_date IS NOT NULL AND strftime('%Y-%m', due_date) = strftime('%Y-%m','now','localtime')"

        sql += " ORDER BY CASE status WHEN 'Done' THEN 1 ELSE 0 END, COALESCE(due_date, '9999-12-31')"

        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()


# --- Main UI -----------------------------------------------------------------
class TaskMaster(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TaskMaster")
        self.resize(1100, 700)

        self.repo = TaskRepository()
        self.current_id: int | None = None

        # Theme
        self.theme_manager = ThemeManager()
        self.current_theme = self.theme_manager.load()
        self.theme_colors: dict = {}

        self._build_ui()
        self._connect_signals()
        self._apply_theme()  # применяем текущую тему

        self._reload_table()

    # UI construction
    def _build_ui(self):
        root = QVBoxLayout(self)

        # Title
        title = QLabel("TaskMaster")
        f = QFont()
        f.setPointSize(18)
        f.setBold(True)
        title.setFont(f)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        root.addWidget(title)

        # Filters/search bar
        filters = QHBoxLayout()
        filters.addWidget(QLabel("Поиск:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Название или описание…")
        filters.addWidget(self.search_edit, 2)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Все", "Todo", "In Progress", "Done"])
        filters.addWidget(QLabel("Статус:"))
        filters.addWidget(self.status_filter)

        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["Все", "Low", "Medium", "High"])
        filters.addWidget(QLabel("Приоритет:"))
        filters.addWidget(self.priority_filter)

        self.chk_overdue = QCheckBox("Только просроченные")
        filters.addWidget(self.chk_overdue)

        self.chk_this_month = QCheckBox("Этот месяц")
        filters.addWidget(self.chk_this_month)

        self.btn_reset_filters = QPushButton("Сброс фильтров")
        filters.addWidget(self.btn_reset_filters)

        # Theme selector
        filters.addStretch(1)
        filters.addWidget(QLabel("Тема:"))
        self.theme_box = QComboBox()
        self.theme_box.addItems(["Тёмная", "Светлая"])
        filters.addWidget(self.theme_box)

        root.addLayout(filters)

        # Splitter: table | form
        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Horizontal)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Название", "Описание", "Приоритет", "Срок", "Статус", "Ежемесячно", "Создано"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        self.table.hideColumn(0)  # скрываем ID
        splitter.addWidget(self.table)

        # Form (right)
        form_box = QGroupBox("Карточка задачи")
        form = QGridLayout(form_box)

        row = 0
        form.addWidget(QLabel("Название:"), row, 0)
        self.ed_name = QLineEdit()
        self.ed_name.setPlaceholderText("Например: Купить молоко")
        form.addWidget(self.ed_name, row, 1, 1, 3)

        row += 1
        form.addWidget(QLabel("Описание:"), row, 0, Qt.AlignmentFlag.AlignTop)
        self.ed_desc = QTextEdit()
        self.ed_desc.setPlaceholderText("Детали задачи…")
        self.ed_desc.setFixedHeight(100)
        form.addWidget(self.ed_desc, row, 1, 1, 3)

        row += 1
        form.addWidget(QLabel("Приоритет:"), row, 0)
        self.cmb_priority = QComboBox()
        self.cmb_priority.addItems(["Low", "Medium", "High"])
        self.cmb_priority.setCurrentText("Medium")
        form.addWidget(self.cmb_priority, row, 1)

        form.addWidget(QLabel("Статус:"), row, 2)
        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["Todo", "In Progress", "Done"])
        self.cmb_status.setCurrentText("Todo")
        form.addWidget(self.cmb_status, row, 3)

        row += 1
        form.addWidget(QLabel("Срок (дата):"), row, 0)
        self.date_due = QDateEdit()
        self.date_due.setCalendarPopup(True)
        self.date_due.setDisplayFormat("dd.MM.yyyy")
        self.date_due.setDate(QDate.currentDate().addDays(7))
        form.addWidget(self.date_due, row, 1)

        self.chk_no_due = QCheckBox("Без срока")
        form.addWidget(self.chk_no_due, row, 2)

        self.chk_monthly = QCheckBox("Ежемесячно")
        form.addWidget(self.chk_monthly, row, 3)

        row += 1
        btns = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_save = QPushButton("Сохранить изменения")
        self.btn_delete = QPushButton("Удалить")
        self.btn_mark_done = QPushButton("Отметить выполненной")
        self.btn_clear = QPushButton("Очистить форму")
        btns.addWidget(self.btn_add)
        btns.addWidget(self.btn_save)
        btns.addWidget(self.btn_mark_done)
        btns.addWidget(self.btn_delete)
        btns.addStretch(1)
        btns.addWidget(self.btn_clear)

        form.addLayout(btns, row, 0, 1, 4)

        splitter.addWidget(form_box)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        root.addWidget(splitter)

        # debounce timer for search
        self._search_timer = QTimer(self)
        self._search_timer.setSingleShot(True)
        self._search_timer.setInterval(300)

        # init buttons state
        self._update_buttons_enabled()

        # Set theme selector initial value
        self.theme_box.setCurrentIndex(0 if self.current_theme == ThemeManager.DARK else 1)

    def _connect_signals(self):
        self.btn_add.clicked.connect(self._on_add)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_mark_done.clicked.connect(self._on_mark_done)
        self.btn_clear.clicked.connect(self._clear_form)

        self.btn_reset_filters.clicked.connect(self._reset_filters)

        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.cellDoubleClicked.connect(self._on_cell_double_clicked)

        self.chk_no_due.toggled.connect(self._on_no_due_toggled)

        # Filters / Search
        self.search_edit.textChanged.connect(lambda: self._search_timer.start())
        self._search_timer.timeout.connect(self._reload_table)
        self.status_filter.currentIndexChanged.connect(self._reload_table)
        self.priority_filter.currentIndexChanged.connect(self._reload_table)
        self.chk_overdue.toggled.connect(self._reload_table)
        self.chk_this_month.toggled.connect(self._reload_table)

        # Theme
        self.theme_box.currentIndexChanged.connect(self._on_theme_changed)

    def _apply_theme(self):
        self.theme_colors = self.theme_manager.apply(self.current_theme)
        self._reload_table()

    # Logic
    def _get_filters(self):
        return {
            "search": self.search_edit.text().strip(),
            "status": self.status_filter.currentText(),
            "priority": self.priority_filter.currentText(),
            "overdue_only": self.chk_overdue.isChecked(),
            "only_this_month": self.chk_this_month.isChecked(),
        }

    def _reload_table(self, preserve_id: int | None = None):
        filters = self._get_filters()
        rows = self.repo.list_tasks(
            search=filters["search"] or None,
            status=filters["status"],
            priority=filters["priority"],
            overdue_only=filters["overdue_only"],
            only_this_month=filters["only_this_month"]
        )

        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        for r, row in enumerate(rows):
            self.table.insertRow(r)

            id_item = QTableWidgetItem(str(row["id"]))
            id_item.setData(Qt.ItemDataRole.UserRole, row["id"])
            self.table.setItem(r, 0, id_item)

            self.table.setItem(r, 1, QTableWidgetItem(row["name"] or ""))
            self.table.setItem(r, 2, QTableWidgetItem(row["description"] or ""))
            self.table.setItem(r, 3, QTableWidgetItem(row["priority"] or ""))
            self.table.setItem(r, 4, QTableWidgetItem(fmt_date_readable(row["due_date"])))
            self.table.setItem(r, 5, QTableWidgetItem(row["status"] or ""))
            self.table.setItem(r, 6, QTableWidgetItem("Да" if row["repeat_monthly"] else "Нет"))
            created_disp = (row["created_at"] or "").replace("T", " ")
            self.table.setItem(r, 7, QTableWidgetItem(created_disp))

            self._style_row(r, row)

        self.table.setSortingEnabled(True)

        if preserve_id is not None:
            self._select_row_by_id(preserve_id)

        self._update_buttons_enabled()

    def _style_row(self, row_index: int, row: sqlite3.Row):
        due = row["due_date"]
        status = row["status"] or "Todo"

        color: QColor | None = None
        if status == "Done":
            color = QColor(self.theme_colors.get("row_done", "#e7f7e7"))
        else:
            if due:
                try:
                    d = date.fromisoformat(due)
                    if d < date.today():
                        color = QColor(self.theme_colors.get("row_overdue", "#fde2e2"))
                    elif d <= date.today() + timedelta(days=2):
                        color = QColor(self.theme_colors.get("row_soon", "#fff6cc"))
                except ValueError:
                    pass

        if color:
            for c in range(self.table.columnCount()):
                item = self.table.item(row_index, c)
                if item:
                    item.setBackground(QBrush(color))

    def _select_row_by_id(self, task_id: int):
        for r in range(self.table.rowCount()):
            id_item = self.table.item(r, 0)
            if id_item and int(id_item.text()) == task_id:
                self.table.selectRow(r)
                self.table.scrollToItem(id_item, QTableWidget.ScrollHint.PositionAtCenter)
                return

    def _on_selection_changed(self):
        items = self.table.selectedItems()
        if not items:
            self.current_id = None
            self._update_buttons_enabled()
            return
        row = self.table.currentRow()
        id_item = self.table.item(row, 0)
        if not id_item:
            return
        self.current_id = int(id_item.text())
        self._fill_form_from_row(row)
        self._update_buttons_enabled()

    def _fill_form_from_row(self, table_row: int):
        self.ed_name.setText(self.table.item(table_row, 1).text())
        self.ed_desc.setPlainText(self.table.item(table_row, 2).text())
        self.cmb_priority.setCurrentText(self.table.item(table_row, 3).text())

        due_text = self.table.item(table_row, 4).text().strip()
        if not due_text:
            self.chk_no_due.setChecked(True)
        else:
            self.chk_no_due.setChecked(False)
            d, m, y = map(int, due_text.split("."))
            self.date_due.setDate(QDate(y, m, d))

        self.cmb_status.setCurrentText(self.table.item(table_row, 5).text())
        self.chk_monthly.setChecked(self.table.item(table_row, 6).text() == "Да")

    def _on_cell_double_clicked(self, row: int, col: int):
        pass

    def _update_buttons_enabled(self):
        has_selection = self.current_id is not None
        self.btn_save.setEnabled(has_selection)
        self.btn_delete.setEnabled(has_selection)
        self.btn_mark_done.setEnabled(has_selection)

    def _on_no_due_toggled(self, checked: bool):
        self.date_due.setEnabled(not checked)

    def _clear_form(self):
        self.current_id = None
        self.ed_name.clear()
        self.ed_desc.clear()
        self.cmb_priority.setCurrentText("Medium")
        self.cmb_status.setCurrentText("Todo")
        self.chk_monthly.setChecked(False)
        self.chk_no_due.setChecked(False)
        self.date_due.setDate(QDate.currentDate().addDays(7))
        self._update_buttons_enabled()
        self.table.clearSelection()

    def _validate_form(self) -> tuple[bool, str]:
        name = self.ed_name.text().strip()
        if not name:
            return False, "Название не может быть пустым."
        return True, ""

    def _collect_form(self):
        name = self.ed_name.text().strip()
        desc = self.ed_desc.toPlainText().strip()
        priority = self.cmb_priority.currentText()
        status = self.cmb_status.currentText()
        repeat_monthly = self.chk_monthly.isChecked()
        due_iso = None if self.chk_no_due.isChecked() else qdate_to_iso(self.date_due.date())
        return name, desc, priority, due_iso, status, repeat_monthly

    def _on_add(self):
        ok, err = self._validate_form()
        if not ok:
            QMessageBox.warning(self, "Проверка", err)
            return
        name, desc, prio, due_iso, status, repeat_monthly = self._collect_form()
        new_id = self.repo.add_task(name, desc, prio, due_iso, status, repeat_monthly)
        self._reload_table(preserve_id=new_id)
        self._clear_form()

    def _on_save(self):
        if self.current_id is None:
            QMessageBox.information(self, "Инфо", "Выберите задачу для сохранения изменений.")
            return
        ok, err = self._validate_form()
        if not ok:
            QMessageBox.warning(self, "Проверка", err)
            return
        name, desc, prio, due_iso, status, repeat_monthly = self._collect_form()
        self.repo.update_task(self.current_id, name, desc, prio, due_iso, status, repeat_monthly)
        self._reload_table(preserve_id=self.current_id)

    def _on_delete(self):
        if self.current_id is None:
            QMessageBox.information(self, "Инфо", "Выберите задачу для удаления.")
            return
        row_name = self.ed_name.text().strip() or f"#{self.current_id}"
        if QMessageBox.question(self, "Подтверждение",
                                f"Удалить задачу «{row_name}»?",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.repo.delete_task(self.current_id)
            self.current_id = None
            self._reload_table()
            self._clear_form()

    def _on_mark_done(self):
        if self.current_id is None:
            QMessageBox.information(self, "Инфо", "Выберите задачу.")
            return
        if self.repo.mark_done(self.current_id):
            self._reload_table(preserve_id=self.current_id)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить задачу.")

    def _reset_filters(self):
        self.search_edit.clear()
        self.status_filter.setCurrentIndex(0)  # Все
        self.priority_filter.setCurrentIndex(0)  # Все
        self.chk_overdue.setChecked(False)
        self.chk_this_month.setChecked(False)
        self._reload_table()

    def _on_theme_changed(self, idx: int):
        text = self.theme_box.currentText()
        theme = ThemeManager.DARK if "Тём" in text else ThemeManager.LIGHT
        if theme != self.current_theme:
            self.current_theme = theme
            self.theme_manager.save(theme)
            self._apply_theme()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # база для аккуратной тёмной темы
    w = TaskMaster()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
