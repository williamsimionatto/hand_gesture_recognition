import tkinter as tk
from tkinter import ttk

class SliderApp:
    def __init__(self, queue):
        self.queue = queue

        self.root = tk.Tk()
        self.root.geometry('300x200')
        self.root.resizable(False, False)
        self.root.title('Slider')

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)

        self.current_value = tk.DoubleVar()
        self.current_value.set(0)

        self.create_widgets()

        self.update_slider_value()

    def create_widgets(self):
        # label for the slider
        slider_label = ttk.Label(
            self.root,
            text='Slider:'
        )
        slider_label.grid(
            column=0,
            row=0,
            sticky='w'
        )

        # slider
        self.slider = ttk.Scale(
            self.root,
            from_=0,
            to=100,
            orient='horizontal',
            variable=self.current_value,
            command=self.slider_changed
        )
        self.slider.grid(
            column=1,
            row=0,
            sticky='we'
        )

        # current value label
        current_value_label = ttk.Label(
            self.root,
            text='Current Value:'
        )
        current_value_label.grid(
            row=1,
            columnspan=2,
            sticky='n',
            ipadx=10,
            ipady=10
        )

        # value label
        self.value_label = ttk.Label(
            self.root,
            text=self.get_current_value()
        )
        self.value_label.grid(
            row=2,
            columnspan=2,
            sticky='n'
        )

    def get_current_value(self):
        return '{: .2f}'.format(self.current_value.get())

    def slider_changed(self, event):
        self.value_label.configure(text=self.get_current_value())

    def update_slider_value(self):
        while True:
            if not self.queue.empty():
                value = self.queue.get()
                self.current_value.set(value)
                self.value_label.configure(text=self.get_current_value())
            self.root.update()

    def run(self):
        self.root.mainloop()