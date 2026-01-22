#imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget

Window.size = (300, 500)

class Notes(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
    
class NotesApp(App):
    def build(self):
        self.title = "Notes App"
        
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

        menu_button = Button(
            size_hint=(None, None),
            size=(35, 35),
            background_normal="images/menu.png",
            background_down="",
            text="",
            padding=0,
            border=(0, 0, 0, 0)
        )

        edit_button = Button(
            size_hint=(None, None),
            size=(35, 35),
            background_normal="images/edit.png",
            background_down="",
            text="",
            padding=0,
            border=(0, 0, 0, 0)
        )
        
        search_button = Button(
            size_hint=(None, None),
            size=(35, 35),
            background_normal="images/search.png",
            background_down="",
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
        
        spacer = Widget()
        
        sub_header.add_widget(menu_button)
        sub_header.add_widget(spacer)
        sub_header.add_widget(search_button)
        sub_header.add_widget(edit_button)
        header.add_widget(title)

        main_layout.add_widget(header)
        main_layout.add_widget(sub_header)
        
        self.text_input = TextInput(hint_text="Enter your notes here...", size_hint_y=0.9)
        main_layout.add_widget(self.text_input)
        
        button_layout = GridLayout(cols=2, size_hint_y=0.1)
        
        save_button = Button(text="Save Note")
        #save_button.bind(on_press=self.save_note)
        button_layout.add_widget(save_button)
        
        clear_button = Button(text="Clear Note")
        #clear_button.bind(on_press=self.clear_note)
        button_layout.add_widget(clear_button)
        
        main_layout.add_widget(button_layout)
        
        return main_layout     
   
if __name__ == "__main__":
    NotesApp().run() 