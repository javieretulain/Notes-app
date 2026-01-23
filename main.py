#imports
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

Window.size = (300, 500)

class MainScreen(Screen):
    pass

class Notes(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

class NoteCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.height = 120
        self.padding = 10

        with self.canvas.before:
            Color(1, 1, 1, 1)  # blanco
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)

        label = Label(
            text="Note",
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)
        )
        label.bind(size=label.setter("text_size"))

        self.add_widget(label)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

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
                App.get_running_app().root.current = "add_note"

class AddNoteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        title = Label(
            text="Add Note",
            font_size="22sp",
            size_hint_y=None,
            height=40
        )

        note_input = TextInput(
            hint_text="Write your note here...",
            multiline=True
        )

        back_button = Button(
            text="Back",
            size_hint_y=None,
            height=40
        )
        back_button.bind(on_press=self.go_back)

        layout.add_widget(title)
        layout.add_widget(note_input)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "main"

class NotesApp(App):
    def on_edit_button_press(self, instance):
        edit_panel = EditPanel()
        edit_panel.open()
    
    def on_add_note_button_press(self, instance):
        pass
        
    def build(self):
        self.title = "Notes App"
        
        sm = ScreenManager()

        main_screen = MainScreen(name="main")
        add_note_screen = AddNoteScreen(name="add_note")
        
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
        
        notes_grid = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None
        )
        notes_grid.bind(minimum_height=notes_grid.setter("height"))
        
        spacer = Widget()
        
        with open ("notes.json", "r") as file:
            notes = file.readlines()
            for note in notes:
                notes_grid.add_widget(NoteCard())

        scroll = ScrollView()
        scroll.add_widget(notes_grid)

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

        sm.add_widget(main_screen)
        sm.add_widget(add_note_screen)

        return sm   
   
if __name__ == "__main__":
    NotesApp().run() 