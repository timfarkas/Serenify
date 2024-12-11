"""Custom calendar interface to manage appointments"""
from tkinter import ttk
import calendar
from datetime import datetime, date, timedelta


class Calendar(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)

        # Initialise variables
        self._mindate = kwargs.get('mindate', None)
        self._maxdate = kwargs.get('maxdate', None)
        self._pattern = kwargs.get('date_pattern', 'yyyy-mm-dd')
        self._selected_date = datetime.now().date()
        self._current_month = self._selected_date

        # Month and year navigation
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', expand=True, pady=5)

        ttk.Button(header_frame, text="◀", width=5, command=self._prev_month).pack(side='left', padx=5)
        self.header_label = ttk.Label(header_frame, text="", font=('Arial', 10, 'bold'))
        self.header_label.pack(side='left', expand=True)
        ttk.Button(header_frame, text="▶", width=5, command=self._next_month).pack(side='right', padx=5)

        # Days of week header
        days_frame = ttk.Frame(self)
        days_frame.pack(fill='x', expand=True)
        for i, day in enumerate(('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')):
            ttk.Label(
                days_frame,
                text=day,
                anchor='center',
                width=8
            ).grid(row=0, column=i, sticky='nsew', padx=1, pady=1)

        # Configure grid columns to be equal width
        for i in range(7):
            days_frame.grid_columnconfigure(i, weight=1)

        # Calendar grid
        self.cal_frame = ttk.Frame(self)
        self.cal_frame.pack(fill='both', expand=True)

        # Create grid
        self._update_calendar()

    def _update_calendar(self):
        # Clear existing calendar
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        # Update header
        self.header_label.config(text=self._current_month.strftime('%B %Y'))

        # Get calendar for current month
        cal = calendar.monthcalendar(self._current_month.year, self._current_month.month)

        # Create calendar grid
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    date_obj = date(self._current_month.year, self._current_month.month, day)
                    disabled = self._is_date_disabled(date_obj)

                    btn = ttk.Button(
                        self.cal_frame,
                        text=str(day),
                        command=lambda d=date_obj: self._on_date_selected(d)
                    )

                    if disabled:
                        btn.state(['disabled'])
                    if self._selected_date and date_obj == self._selected_date:
                        btn.state(['pressed'])

                    btn.grid(row=week_num, column=day_num, padx=1, pady=1, sticky='nsew')

        # Configure grid weights
        for i in range(7):
            self.cal_frame.grid_columnconfigure(i, weight=1)

    def _is_date_disabled(self, date_obj):
        now = datetime.now()
        today = now.date()

        
        if date_obj < today:
            return True
        elif date_obj == today:
            current_hour = now.hour
            return True if current_hour >= 16 else False
        ## block weekends
        if date_obj.weekday() in (5, 6):
            return True
        ## block major UK holidays
        if (date_obj.month == 12 and date_obj.day in (24, 25, 26, 31)) or \
           (date_obj.month == 1 and date_obj.day == 1):
           #(date_obj.month == 4 and date_obj.day in (GoodFriday, EasterMonday)) or \
           #(date_obj.month == 5 and date_obj.day in (EarlyMayBankHoliday, SpringBankHoliday)) or \
           #(date_obj.month == 8 and date_obj.day == SummerBankHoliday):
            return True
        if self._mindate and date_obj < self._mindate.date():
            return True
        if self._maxdate and date_obj > self._maxdate.date():
            return True
        return False

    def _on_date_selected(self, selected_date):
        if not self._is_date_disabled(selected_date):
            self._selected_date = selected_date
            self._update_calendar()
            self.event_generate('<<CalendarSelected>>')

    def _prev_month(self):
        first_day = date(self._current_month.year, self._current_month.month, 1)
        prev_month = (first_day - timedelta(days=1)).replace(day=1)

        # Don't allow navigation if prev month is before current month
        if prev_month < datetime.now().date().replace(day=1):
            return

        self._current_month = prev_month
        self._update_calendar()

    def _next_month(self):
        days_in_month = calendar.monthrange(self._current_month.year, self._current_month.month)[1]
        last_day = date(self._current_month.year, self._current_month.month, days_in_month)
        self._current_month = (last_day + timedelta(days=1)).replace(day=1)
        self._update_calendar()

    def get_date(self):
        """Returns selected date in yyyy-mm-dd format - maintains compatibility with tkcalendar"""
        return self._selected_date.strftime('%Y-%m-%d')

    def selection_get(self):
        """Alternative getter - maintains compatibility with tkcalendar"""
        return self._selected_date

    def selection_set(self, date_obj):
        """Sets the selected date - maintains compatibility with tkcalendar"""
        if isinstance(date_obj, str):
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
        self._selected_date = date_obj
        self._update_calendar()