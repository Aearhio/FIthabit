from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from datetime import datetime, timedelta
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Line
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase
from kivy.graphics import Color
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, Rectangle
from kivy.storage.jsonstore import JsonStore
import random


# Initialize storage
store = JsonStore('habit_data.json')

# Set the window size to a typical mobile resolution for testing
Window.size = (360, 640)


class CircleWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 0, 1, 1)
            self.circle = Ellipse(size=(10, 10))

    def update_position(self, x, y):
        self.circle.pos = (x, y)


class StartUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set the background color or image
        with self.canvas:
            self.bg_color = Color(1.0, 0.71, 0.76, 1)  # RGB color (light blue)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_bg, pos=self.update_bg)

        layout = BoxLayout(orientation='vertical', padding=20)

        # Add a title label with a custom font
        img = Image(source='FitHabit.png', size_hint=(1, .1))

        # Add an image


        # Add a start button
        start_button = Button(
            text="Start",
            font_size=24,
            font_name="font.ttf",
            size_hint=(1
                       , 0.02),

            background_color=(1.0, 0.71, 0.76, 1),
            on_press=self.start_app
        )

        layout.add_widget(img)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def update_bg(self, *args):
        """Update the background rectangle size and position."""
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def start_app(self, instance):
        app = App.get_running_app()
        app.root.current = "loading_screen"
        Clock.schedule_once(self.show_loading_screen, 1)

    def show_loading_screen(self, dt):
        app = App.get_running_app()
        app.root.current = "main_screen"


class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set background color or image
        with self.canvas.before:
            Color(1.0, 0.71, 0.76, 1)  # Set your background color (Blue here)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_bg, pos=self.update_bg)

        # Optionally, add an image as background:
        # background_image = Image(source="background_image.jpg", allow_stretch=True, size_hint=(1, 1))
        # self.add_widget(background_image)

        layout = BoxLayout(orientation='vertical', padding=50)

        # Add the loading label with a custom font
        label = Label(
            text="Loading...",
            font_size=30,
            size_hint=(1, 0.2),
            font_name="font.ttf"  # Set custom font here
        )
        layout.add_widget(label)

        self.add_widget(layout)

    def update_bg(self, *args):
        """Update the background rectangle size and position."""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_enter(self):
        # Add animation (fade-in effect)
        self.opacity = 0
        anim = Animation(opacity=1, duration=2)  # Fade in over 2 seconds
        anim.start(self)

        # After animation ends, switch to the main screen
        anim.bind(on_complete=self.switch_to_main_screen)

    def switch_to_main_screen(self, *args):
        app = App.get_running_app()
        app.root.current = "main_screen"


    LabelBase.register(name="CustomFont", fn_regular="font.ttf")


class FITHABIT(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.habits = ['images/sleep.png', 'images/study.png', 'images/eat.png', 'images/physic.png']
        self.entries = {}
        self.weekdays =  [
    'days/day1.png',
    'days/day2.png',
    'days/day3.png',
    'days/day4.png',
    'days/day5.png',
    'days/day6.png',
    'days/day7.png'
]
        self.week_data = {day: {habit: [] for habit in self.habits} for day in self.weekdays}
        self.selected_day = None
        self.last_saved_day = None
        self.current_streak = 0
        self.selected_month = datetime.now().month

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Set background image for the calendar layout
        with self.canvas.before:
            Color(0.9, 0.8, 1.0, 1.0)  # Background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_bg, pos=self.update_bg)

        # Add Year Calendar Layout
        year_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), padding=10, spacing=10)

        # Month navigation buttons with images
        nav_buttons = BoxLayout(orientation='horizontal', size_hint=(1, .03))
        prev_button = Button(
            background_normal='prev.png',  # Replace with your image
            background_down='prev.png',  # Replace with your image
            size_hint=(0.2, 1),
            on_press=self.show_previous_month
        )
        next_button = Button(
            background_normal='next.png',  # Replace with your image
            background_down='next.png',  # Replace with your image
            size_hint=(0.2, 1),
            on_press=self.show_next_month
        )
        nav_buttons.add_widget(prev_button)
        nav_buttons.add_widget(next_button)
        year_layout.add_widget(nav_buttons)

        # Display the month name with custom font and color
        self.month_label = Label(
            text="",
            size_hint=(1, 0.1),
            font_size=24,
            font_name="font.ttf",  # Custom font
            color=(0.8, 0.2, 0.4, 1.0)  # Change to green text
        )
        year_layout.add_widget(self.month_label)

        # Scrollable calendar layout
        self.month_layout = BoxLayout(orientation='vertical', size_hint_y=5)
        self.month_layout.bind(minimum_height=self.month_layout.setter('height'))

        self.update_calendar()

        year_fixed_view = BoxLayout(orientation='vertical', size_hint=(1, 0.3), padding=(0, 1000, 0, 0))
        year_fixed_view.add_widget(self.month_layout)
        year_layout.add_widget(year_fixed_view)
        layout.add_widget(year_layout)

        # Add Week Progress Section
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=(0, 1100, 0, 0))
        self.week_label = Label(
            text="Week Progress",
            size_hint=(0.8, 1),
            padding=(0, 100, 0, 0),
            font_name="font.ttf",  # Custom font
            font_size=22,  # Change font size
            color=(0.8, 0.2, 0.4, 1.0)  # Change text color to blue
                                        )
        header.add_widget(self.week_label)
        layout.add_widget(header)

        self.calendar_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), padding=(0, 63, 0, 0))
        self.day_labels = {}
        self.day_circles = {}

        for i, day in enumerate(self.weekdays):
            day_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1))

            # Create an Image widget for each weekday
            day_image = Image(
                source=day,  # Use the day PNG images like 'days/day1.png'
                size_hint=(1, 1.3),
                allow_stretch=True,
                keep_ratio=True
            )
            day_layout.add_widget(day_image)

            # Create a circle widget to match your design
            circle = CircleWidget()
            self.day_circles[day] = circle
            day_layout.add_widget(circle)

            # Bind the click event to select the day
            day_image.day = day
            day_image.bind(on_touch_down=self.on_day_label_click)  # Bind the click event here

            self.day_labels[day] = day_image  # Store image as a reference to the day
            self.calendar_box.add_widget(day_layout)

        layout.add_widget(self.calendar_box)
        # Habits section with custom font and color
        self.input_box = BoxLayout(orientation='vertical', size_hint=(1, .5), padding=10, spacing=2)
        for habit in self.habits:
            habit_box = BoxLayout(orientation='horizontal', size_hint=(1, .5) ,  padding=33,spacing=5)


            imagelabel = Image(
                source=habit,
                size_hint=(1, 20),  # Disable size hint to use fixed size
                size=(6, 15),
                # Set the width and height explicitly
                allow_stretch=True,  # Allow stretching if necessary
                keep_ratio=True  # Maintain aspect ratio
            )
            input_field = TextInput(
                multiline=False,
                input_filter='int' if habit == 'images/eat.png' else 'float',
                size_hint=(1, 20),
                height=50
            )
            habit_box.add_widget(imagelabel)
            habit_box.add_widget(input_field)
            self.entries[habit] = input_field
            self.input_box.add_widget(habit_box)

        layout.add_widget(self.input_box)



        # Save and View Report buttons with custom images
        button_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

        save_button = Button(
            background_normal='save.png',  # Replace with your PNG
            background_down='save.png',  # Replace with your PNG
            size_hint=(0.45, 1.3), on_press=self.save_data
        )
        view_button = Button(
            background_normal='report.png',  # Replace with your PNG
            background_down='report.png',  # Replace with your PNG
            size_hint=(0.45, 1.3), on_press=self.view_report
        )

        button_box.add_widget(save_button)
        button_box.add_widget(view_button)
        layout.add_widget(button_box)

        self.add_widget(layout)

    def update_bg(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


    # Method to handle click on weekday
    def on_day_label_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print(f"Day clicked: {instance.source}")

    # Method to handle click on habit
    def on_habit_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print(f"Habit clicked: {instance.source}")

    def update_bg(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def show_previous_month(self, instance):
        print("Previous month")

    def show_next_month(self, instance):
        print("Next month")

    def update_calendar(self):
        pass  # Your calendar update logic

    def save_data(self, instance):
        print("Data saved")

    def view_report(self, instance):
        print("Viewing report")

    # Method to handle click on weekday
    def on_day_label_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print(f"Day clicked: {instance.source}")

    # Method to handle click on habit
    def on_habit_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print(f"Habit clicked: {instance.source}")

    def update_bg(self, *args):
        """Update the background rectangle size and position."""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_calendar(self):
        self.month_layout.clear_widgets()
        month_name = datetime(2025, self.selected_month, 1).strftime('%B')
        self.month_label.text = month_name

        # Get the number of days in the selected month and the starting weekday
        first_day = datetime(2025, self.selected_month, 1)
        last_day = (first_day.replace(month=self.selected_month % 12 + 1) - timedelta(days=1)).day
        start_weekday = first_day.weekday()  # 0 is Monday, 6 is Sunday

        # Create an empty grid for the calendar
        days_grid = BoxLayout(orientation='vertical', size_hint_y=None, height=60 * 6)  # 6 weeks for all months

        # Get today's date to highlight the current day
        today = datetime.today()

        # Create rows for each week
        for week in range(6):  # 6 weeks in a month grid to accommodate all possible month configurations
            week_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, padding=(0, 2000, 0, 0))

            # Add day cells to the week row
            for day_in_week in range(7):  # 7 days in a week
                day_number = week * 7 + day_in_week - start_weekday + 1
                if 1 <= day_number <= last_day:
                    # Determine color based on day of the week or if it is today's date
                    if (start_weekday + day_in_week) % 7 in [5, 6]:  # 5 = Saturday, 6 = Sunday
                        day_color = [0.7, 0.62, 0.71, 1]  # Red for weekends
                    elif day_number == today.day and self.selected_month == today.month and today.year == 2025:
                        day_color = [0, 1, 0, 1]  # Green for today's date
                    else:
                        day_color = [0.7, 0.62, 0.71, 1]  # Black for regular days

                    # Create label with dynamic color and font
                    day_label = Label(
                        text=str(day_number),
                        size_hint=(1, 1),
                        font_size=16,
                        padding=(0, 240, 0, 0),
                        color=day_color
                    )

                    # Set custom font (ensure you have the font file available)
                    day_label.font_name = "font.ttf"  # Replace with actual path to the font file
                    day_label.font_size = 18  # You can adjust the size as well
                else:
                    day_label = Label()  # Empty label for days outside the current month
                week_layout.add_widget(day_label)

            days_grid.add_widget(week_layout)

        self.month_layout.add_widget(days_grid)

    def on_day_label_click(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):
            self.selected_day = instance.day
            self.update_day_color(instance)  # Change the label color
            self.update_input_for_selected_day()

    def update_day_color(self, instance):
        # Change the background color of the clicked day label
        instance.color = (0.53, 0.81, 0.98, 1)

    def on_day_button_click(self, button):
        """Handle the event when a day button is clicked."""
        self.selected_day = button.day  # Get the day associated with the clicked button
        self.update_input_for_selected_day()  # Update input fields for the selected day
        self.show_popup("Day Selected", f"You selected {self.selected_day}.")

    def update_input_for_selected_day(self):
        if self.selected_day:
            for habit, input_field in self.entries.items():
                habit_data = self.week_data[self.selected_day].get(habit, [])
                input_field.text = str(habit_data[-1]) if habit_data else ''

    def save_data(self, _):
        if not self.selected_day:
            self.show_popup("No Day Selected", "Please select a day to enter data.")
            return

        today = datetime.now().strftime('%Y-%m-%d')
        daily_data = {}

        for habit, input_field in self.entries.items():
            try:
                input_value = input_field.text.strip()
                value = int(input_value) if habit == 'Eating' else float(input_value) if input_value else 0
                daily_data[habit] = value
                self.week_data[self.selected_day][habit].append(value)
            except ValueError:
                self.show_popup("Invalid Input", f"Please enter a valid number for {habit}.")
                return

        store.put(today, **daily_data)
        self.update_calendar_after_save(today)
        self.show_popup("Success", "Data saved successfully!")

    def update_calendar_after_save(self, today):
        if not self.last_saved_day or (
                datetime.strptime(today, '%Y-%m-%d') - datetime.strptime(self.last_saved_day, '%Y-%m-%d')).days > 1:
            self.current_streak = 0
        self.current_streak += 1
        self.last_saved_day = today

        for i in range(self.current_streak):
            day = self.weekdays[i]
            self.day_circles[day].update_position(self.day_labels[day].x + self.day_labels[day].width / 2 - 5,
                                                  self.day_labels[day].y - 10)

        if self.current_streak == 7:
            self.check_average_and_show_quote()

    def add_circle_to_day(self, day):
        # Add a circle under the selected day label once data is saved
        circle = self.day_circles[day]
        circle.update_position(10, 50)  # Adjust the position of the circle as needed

    def show_previous_month(self, instance):
        if self.selected_month == 1:
            self.selected_month = 12
        else:
            self.selected_month -= 1
        self.update_calendar()

    def show_next_month(self, instance):
        if self.selected_month == 12:
            self.selected_month = 1
        else:
            self.selected_month += 1
        self.update_calendar()

    def check_average_and_show_quote(self):
        averages = {}
        for habit in self.habits:
            total = sum(self.week_data[day][habit][-1] for day in self.weekdays if self.week_data[day][habit])
            averages[habit] = total / 7

        is_adequate = all(averages[habit] >= (1 if habit == 'Eating' else 6) for habit in self.habits)
        quote = random.choice(["Keep up!", "Great job!"]) if is_adequate else random.choice(["Oh no!", "Try harder!"])
        self.show_popup("Weekly Summary", quote)

    def show_popup(self, title, message):
        # Create a layout for the popup
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Custom label with a new font and color
        label = Label(
            text=message,
            font_name="font.ttf",  # Replace with your desired font file
            font_size=18,
            color=(0.5, 0.2, 0.7, 1),  # Light purple text
            size_hint=(1, 0.7)
        )

        # Add a custom background color to the popup
        with layout.canvas.before:
            Color(0.9, 0.8, 1.0, 1.0)  # Lightest purple background
            layout.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self.update_rect, pos=self.update_rect)

        # Add the label to the layout
        layout.add_widget(label)

        # Add a close button
        close_button = Button(
            text="Close",
            size_hint=(0.5, 0.3),
            font_name="font.ttf",
            font_size=16,
            background_color=(0.6, 0.3, 0.8, 1)  # Darker purple button
        )
        close_button.bind(on_release=lambda _: popup.dismiss())
        layout.add_widget(close_button)

        # Create and display the popup
        popup = Popup(
            title=title,
            title_color=(0.4, 0.1, 0.5, 1),  # Purple title
            title_size=22,
            content=layout,
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def update_rect(self, instance, value):
        # Update the rectangle size and position when layout changes
        instance.rect.size = instance.size
        instance.rect.pos = instance.pos

    def view_report(self, _):
        app = App.get_running_app()
        app.root.current = "report_screen"

class ReportScreen(Screen):
    def __init__(self, store=None, **kwargs):
        super().__init__(**kwargs)
        self.store = store or JsonStore('default_store.json')

        # Background color
        with self.canvas.before:
            Color(0.7, 0.62, 0.71, 1)  # Background color
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_background, pos=self.update_background)

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=20)

        # Scrollable report area
        self.report_scroll = ScrollView(size_hint=(1.1, 3), height=self.height * 0.75)
        self.report_box = BoxLayout(orientation='vertical', size_hint_y=None, height=self.height * 7)

        # Report text
        self.report_label = Label(
            text="",
            size_hint_y=.8,
            height=self.height * 0.1,
            font_name="font.ttf",
            color=(1, 1, 1, 1),
            text_size=(self.width * 0.9, None),
            halign="left",
            valign="top",
            padding=(0, 20),
        )

        self.report_label.bind(width=self.update_text_width)
        self.report_box.add_widget(self.report_label)
        self.report_scroll.add_widget(self.report_box)

        # Back button
        back_button = Button(
            text="Back to Main",
            size_hint=(1, 0.5),
            font_name="font.ttf",
            background_color=(1.0, 0.71, 0.76, 1),
            on_press=self.go_back,
        )

        layout.add_widget(self.report_scroll)
        layout.add_widget(back_button)
        self.add_widget(layout)

        self.load_and_display_data()

    def load_and_display_data(self):
        # Example: Mapping from filenames to human-readable labels
        activity_map = {
            "images/sleep.png": "Sleeping",
            "images/eat.png": "Eating",
            "images/physic.png": "Exercising",
            "images/study.png": "Studying",
        }

        # Fetch data from the JsonStore
        if self.store.exists("habits"):
            habits = self.store.get("habits")
            formatted_data = []
            for key, value in habits.items():
                label = activity_map.get(key, key)
                formatted_data.append(f"{label}: {value} hrs")

            self.report_label.text = "\n".join(formatted_data)
        else:
            self.report_label.text = "No activity data available."

    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def update_text_width(self, *args):
        self.report_label.text_size = (self.report_scroll.width * 0.9, None)

    def go_back(self, instance):
        self.manager.current = "main_screen"



    def update_border(self, *args):
        """Update the border to match the size of the ScrollView."""
        self.border_rect.size = self.report_scroll.size
        self.border_rect.pos = self.report_scroll.pos
        self.border_line.rectangle = (self.report_scroll.x, self.report_scroll.y, self.report_scroll.width, self.report_scroll.height)



    def on_enter(self):
        """Refresh the report when the screen is displayed."""
        self.generate_report()

    def generate_report(self):
        """Generate the report text."""
        report_text = "Habit Report:\n\n"
        for date in store:
            habits = store.get(date)  # Get the value (likely a dictionary or list) associated with the key
            report_text += f"{date}:\n"
            for habit, value in habits.items():
                unit = "times" if habit == "Eating" else "hours"
                report_text += f"  {habit}: {value} {unit}\n"
            report_text += "\n"
        self.report_label.text = report_text


class FITHABITApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(StartUpScreen(name="start_screen"))
        screen_manager.add_widget(LoadingScreen(name="loading_screen"))
        screen_manager.add_widget(FITHABIT(name="main_screen"))
        screen_manager.add_widget(ReportScreen(name="report_screen"))
        return screen_manager


if __name__ == "__main__":
    FITHABITApp().run()
