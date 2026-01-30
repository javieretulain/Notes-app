#imports
import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior

def load_notes():
    if not os.path.exists("notes.json"):
        return []

    with open("notes.json", "r") as f:
        data = json.load(f)

        if isinstance(data, dict):
            return data.get("notes", [])

        return data

def save_notes(notes):
    with open("notes.json", "w") as f:
        json.dump(notes, f, indent=4)

Window.size = (300, 500)

class MainScreen(Screen):
    pass

class Notes(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

class EditPanel(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (0.8, None)
        self.height = 200
        self.auto_dismiss = True  # se cierra tocando afuera

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        with layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.bg = RoundedRectangle(
                pos=layout.pos,
                size=layout.size,
                radius=[15]
            )

        layout.bind(
            pos=lambda *_: setattr(self.bg, "pos", layout.pos),
            size=lambda *_: setattr(self.bg, "size", layout.size)
        )
        
        btn_edit = Button(text="Edit")
        btn_add = Button(text="Add notes")
        
        layout.add_widget(btn_edit)
        layout.add_widget(btn_add)
        btn_add.bind(on_press=self.go_to_add_note)

        self.add_widget(layout)

    def go_to_add_note(self, instance):
                self.dismiss()
                App.get_running_app().open_new_note()

class NotesApp(App):
    def open_new_note(self):
        self.current_note_index = None
        self.screen_manager.current = "edit_note"

    def open_note(self, index):
        self.current_note_index = index
        self.screen_manager.current = "edit_note"

    def on_edit_button_press(self, instance):
        edit_panel = EditPanel()
        edit_panel.open()
    
    def refresh_notes(self):
        self.notes_grid.clear_widgets()

        notes = load_notes()
        for index, note in enumerate(notes):
            self.notes_grid.add_widget(
                NoteCard(note_index=index, title=note.get("title", "Sin título"))
            )

       
    def build(self):
        self.title = "Notes App"
        
        self.notes_grid = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None
        )
        self.notes_grid.bind(minimum_height=self.notes_grid.setter("height"))

        self.screen_manager = ScreenManager()

        main_screen = MainScreen(name="main")
        
        main_layout = Notes()
        
        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.20,
            padding=10,
            spacing=10
        )

        sub_header = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.1,
            padding=5,
            spacing=5
        )

        body = BoxLayout(
            orientation="vertical",
            size_hint_y=0.7,
            padding=10,
            spacing=10
        )
        
        menu_button = Button(
            size_hint=(None, None),
            size=(35, 35),
            background_normal="images/menu.png",
            background_down="images/menu.png",
            text="",
            padding=0,
            border=(0, 0, 0, 0)
        )

        edit_button = Button(
            size_hint=(None, None),
            size=(35, 35),
            background_normal="images/edit.png",
            background_down="images/edit.png",
            text="",
            padding=0,
            border=(0, 0, 0, 0),
            on_press=self.on_edit_button_press
        )
        
        search_button = Button(
            size_hint=(None, None),
            size=(35, 35),
            background_normal="images/search.png",
            background_down="images/search.png",
            text="",
            padding=0,
            border=(0, 0, 0, 0)
        )

        title = Label(
            text="My Notes",
            font_size="22sp",
            halign="left",
            valign="middle"
        )
        
        self.notes_grid.bind(minimum_height=self.notes_grid.setter("height"))
        
        spacer = Widget()

        scroll = ScrollView()
        scroll.add_widget(self.notes_grid)

        body.add_widget(scroll)
        
        sub_header.add_widget(menu_button)
        sub_header.add_widget(spacer)
        sub_header.add_widget(search_button)
        sub_header.add_widget(edit_button)
        header.add_widget(title)

        main_layout.add_widget(header)
        main_layout.add_widget(sub_header)
        main_layout.add_widget(body)
        
        main_screen.add_widget(main_layout)
        
        self.screen_manager.add_widget(main_screen)
        self.screen_manager.add_widget(EditNoteScreen(name="edit_note"))

        self.refresh_notes()
        
        return self.screen_manager   

class EditNoteScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        notes = load_notes()

        self.note_index = app.current_note_index

        if self.note_index is None:
            self.title_input.text = ""
            self.body_input.text = ""
            return

        note = notes[self.note_index]
        self.title_input.text = note.get("title", "")
        self.body_input.text = note.get("text", "")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.title_input = TextInput(
            hint_text="Title",
            multiline=False,
            font_size="22sp",
            size_hint_y=None,
            height=40
        )

        self.body_input = TextInput(
            multiline=True,
            hint_text="Write your note here...",
            font_size="16sp"
        )

        back_btn = Button(text="Back", size_hint_y=None, height=40)
        back_btn.bind(on_press=self.save_and_back)

        layout.add_widget(self.title_input)
        layout.add_widget(self.body_input)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def save_and_back(self, instance):
        notes = load_notes()

        if self.note_index is None:
            notes.append({
                "title": self.title_input.text,
                "text": self.body_input.text
            })
        else:
            notes[self.note_index]["title"] = self.title_input.text
            notes[self.note_index]["text"] = self.body_input.text

        save_notes(notes)

        App.get_running_app().screen_manager.current = "main"
        App.get_running_app().refresh_notes()

class NoteCard(ButtonBehavior, BoxLayout):
    def __init__(self, note_index, title, **kwargs):
        super().__init__(**kwargs)

        self.note_index = note_index
        self.size_hint_y = None
        self.height = 120
        self.padding = 10

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)

        self.label = Label(
            text=title,
            bold=True,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)
        )
        self.label.bind(size=self.label.setter("text_size"))
        self.add_widget(self.label)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_press(self):
        App.get_running_app().open_note(self.note_index)

if __name__ == "__main__":
    NotesApp().run() 
    
