import logging
logger = logging.getLogger(__name__)

import tkinter as tk
from tkinter import ttk
from typing import Callable


class GameUI:
    # Handles all UI components and layout for the 20 Questions game
    
    def __init__(self, on_start_game_callback: Callable, on_yes_callback: Callable, 
                 on_no_callback: Callable, on_start_over_callback: Callable):
        self.on_start_game_callback = on_start_game_callback
        self.on_yes_callback = on_yes_callback
        self.on_no_callback = on_no_callback
        self.on_start_over_callback = on_start_over_callback
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("20 Questions Game")
        self.root.geometry("800x600")
        self.root.minsize(400, 600)
        
        # Configure responsive grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Bind resize event for responsiveness
        self.root.bind('<Configure>', self.on_window_resize)
        
        # UI state
        self.current_screen = "start"
        self.current_question = 1
        
    def create_start_screen(self):
        # Create the start game screen
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        self.current_screen = "start"
        
        # Configure grid weights for responsive layout
        for i in range(7):
            self.main_frame.grid_rowconfigure(i, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title label
        self.title_label = ttk.Label(
            self.main_frame,
            text="20 Questions Game",
            font=("Arial", self.get_responsive_font_size(32), "bold"),
            anchor="center"
        )
        self.title_label.grid(row=0, column=0, pady=20, sticky="ew")
        
        # Instruction label
        self.instruction_label = ttk.Label(
            self.main_frame,
            text="Think of an object, animal, or concept.\nI'll try to guess it in 20 questions!",
            font=("Arial", self.get_responsive_font_size(18)),
            anchor="center",
            justify="center"
        )
        self.instruction_label.grid(row=1, column=0, pady=10, sticky="ew")
        
        # Input label
        self.input_label = ttk.Label(
            self.main_frame,
            text="What are you thinking of?",
            font=("Arial", self.get_responsive_font_size(16)),
            anchor="center"
        )
        self.input_label.grid(row=2, column=0, pady=(20, 5), sticky="ew")
        
        # Text entry
        self.text_entry = ttk.Entry(
            self.main_frame,
            font=("Arial", self.get_responsive_font_size(16)),
            justify="center"
        )
        self.text_entry.grid(row=3, column=0, pady=5, padx=50, sticky="ew")
        self.text_entry.bind("<FocusIn>", self.on_text_focus)
        self.text_entry.bind("<Return>", lambda e: self.on_start_game_callback())
        
        # Start button frame for centering
        responsive_padding = self.get_responsive_padding(100)
        start_button_container = ttk.Frame(self.main_frame)
        start_button_container.grid(row=4, column=0, pady=20, padx=responsive_padding, sticky="ew")
        start_button_container.grid_columnconfigure(0, weight=1)
        
        # Start button using same style as yes/no buttons
        self.start_button_frame = tk.Frame(start_button_container, bg="#007bff", relief="raised", bd=2)
        self.start_button_frame.grid(row=0, column=0)
        
        self.start_button = tk.Label(
            self.start_button_frame,
            text="Start Game",
            font=("Arial", self.get_responsive_font_size(14), "bold"),
            bg="#007bff",
            fg="white",
            padx=30,
            pady=12,
            cursor="hand2"
        )
        self.start_button.pack()
        self.start_button.bind("<Button-1>", lambda e: self.on_start_game_callback())
        self.start_button.bind("<Enter>", lambda e: self.start_button.configure(bg="#0056b3"))
        self.start_button.bind("<Leave>", lambda e: self.start_button.configure(bg="#007bff"))
        
        # Bottom label for feedback
        self.bottom_label = ttk.Label(
            self.main_frame,
            text="Enter the name of an object, animal, or concept you want me to guess.",
            font=("Arial", self.get_responsive_font_size(12)),
            anchor="center",
            foreground="gray",
            wraplength=500
        )
        self.bottom_label.grid(row=6, column=0, pady=10, sticky="ew")
        
        # Ensure fonts are properly sized for current window after creation
        self.root.after(10, self.update_start_screen_fonts)
    
    def create_game_screen(self, question_text: str, show_buttons: bool = True):
        # Create the in-game screen
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        self.current_screen = "game"
        
        # Configure grid weights for responsive layout (now with reasoning row)
        for i in range(6):
            self.main_frame.grid_rowconfigure(i, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Top header frame for question counter and start over button
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(10, 20))
        header_frame.grid_columnconfigure(1, weight=1)  # Middle column expands
        
        # Question counter (top left)
        self.question_counter_label = ttk.Label(
            header_frame,
            text=f"Question {self.current_question} of 20",
            font=("Arial", self.get_responsive_font_size(16))
        )
        self.question_counter_label.grid(row=0, column=0, sticky="w")
        
        # Start over button (top right)
        self.start_over_button = ttk.Button(
            header_frame,
            text="Start Over",
            command=self.on_start_over_callback
        )
        self.start_over_button.grid(row=0, column=2, sticky="e")
        
        # Spacer for vertical centering
        spacer_top = ttk.Frame(self.main_frame)
        spacer_top.grid(row=1, column=0, sticky="ew")
        
        # Question label (center of screen)
        self.question_label = ttk.Label(
            self.main_frame,
            text=question_text,
            font=("Arial", self.get_responsive_font_size(20)),
            anchor="center",
            wraplength=500
        )
        self.question_label.grid(row=2, column=0, pady=20, sticky="ew")
        
        # Buttons frame for yes/no buttons (only show if needed)
        if show_buttons:
            self.create_yes_no_buttons()
        
        # Reasoning text area below buttons
        self.reasoning_label = ttk.Label(
            self.main_frame,
            text="",
            font=("Arial", self.get_responsive_font_size(14)),
            anchor="center",
            wraplength=500,
            foreground="gray"
        )
        self.reasoning_label.grid(row=4, column=0, pady=(10, 20), sticky="ew")
        
        # Spacer at bottom for vertical centering
        spacer_bottom = ttk.Frame(self.main_frame)
        spacer_bottom.grid(row=5, column=0, sticky="ew")
        
        # Ensure fonts are properly sized for current window after creation
        self.root.after(10, self.update_game_screen_fonts)
    
    def create_yes_no_buttons(self):
        # Create the Yes/No buttons
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.grid(row=3, column=0, pady=20, sticky="ew")
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=0)
        self.buttons_frame.grid_columnconfigure(2, weight=0)
        self.buttons_frame.grid_columnconfigure(3, weight=1)
        
        # Yes button (green) - Using Canvas for reliable colors on macOS
        self.yes_button_frame = tk.Frame(self.buttons_frame, bg="#28a745", relief="raised", bd=2)
        self.yes_button_frame.grid(row=0, column=1, padx=10)
        
        self.yes_button = tk.Label(
            self.yes_button_frame,
            text="Yes",
            font=("Arial", self.get_responsive_font_size(16), "bold"),
            bg="#28a745",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.yes_button.pack()
        self.yes_button.bind("<Button-1>", lambda e: self.on_yes_callback())
        self.yes_button.bind("<Enter>", lambda e: self.yes_button.configure(bg="#218838"))
        self.yes_button.bind("<Leave>", lambda e: self.yes_button.configure(bg="#28a745"))
        
        # No button (red) - Using Canvas for reliable colors on macOS
        self.no_button_frame = tk.Frame(self.buttons_frame, bg="#dc3545", relief="raised", bd=2)
        self.no_button_frame.grid(row=0, column=2, padx=10)
        
        self.no_button = tk.Label(
            self.no_button_frame,
            text="No",
            font=("Arial", self.get_responsive_font_size(16), "bold"),
            bg="#dc3545",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.no_button.pack()
        self.no_button.bind("<Button-1>", lambda e: self.on_no_callback())
        self.no_button.bind("<Enter>", lambda e: self.no_button.configure(bg="#c82333"))
        self.no_button.bind("<Leave>", lambda e: self.no_button.configure(bg="#dc3545"))
    
    def get_responsive_font_size(self, base_size: int) -> int:
        # Calculate responsive font size based on window size
        try:
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            # If window hasn't been drawn yet, use default
            if window_width <= 1 or window_height <= 1:
                return base_size
            
            # Scale font based on window size
            scale_factor = min(window_width / 600, window_height / 700)
            font_size = max(8, int(base_size * scale_factor))
            return font_size
        except Exception:
            return base_size
    
    def get_responsive_padding(self, base_padding: int) -> int:
        # Calculate responsive padding based on window size
        try:
            window_width = self.root.winfo_width()
            
            # If window hasn't been drawn yet, use default
            if window_width <= 1:
                return base_padding
            
            # Scale padding based on window width
            scale_factor = window_width / 600
            responsive_padding = max(20, int(base_padding * scale_factor))
            return responsive_padding
        except Exception:
            return base_padding
    
    def on_window_resize(self, event):
        # Handle window resize events for responsive design
        if event.widget == self.root:
            logger.info(f"Window resized to: {self.root.winfo_width()}x{self.root.winfo_height()}")
            
            # Update font sizes for current screen
            if self.current_screen == "start":
                self.root.after(10, self.update_start_screen_fonts)
            elif self.current_screen == "game":
                self.root.after(10, self.update_game_screen_fonts)
    
    def update_start_screen_fonts(self):
        # Update all start screen fonts for current window size
        try:
            if hasattr(self, 'title_label'):
                self.title_label.configure(font=("Arial", self.get_responsive_font_size(32), "bold"))
            if hasattr(self, 'instruction_label'):
                self.instruction_label.configure(font=("Arial", self.get_responsive_font_size(18)))
            if hasattr(self, 'input_label'):
                self.input_label.configure(font=("Arial", self.get_responsive_font_size(16)))
            if hasattr(self, 'text_entry'):
                self.text_entry.configure(font=("Arial", self.get_responsive_font_size(16)))
            if hasattr(self, 'start_button'):
                # Update button font directly like yes/no buttons
                self.start_button.configure(font=("Arial", self.get_responsive_font_size(14), "bold"))
                # Update button padding responsively
                responsive_padding = self.get_responsive_padding(100)
                if hasattr(self, 'start_button_frame'):
                    # The container needs to be re-gridded with new padding
                    start_button_container = self.start_button_frame.master
                    start_button_container.grid(row=4, column=0, pady=20, padx=responsive_padding, sticky="ew")
            if hasattr(self, 'bottom_label'):
                self.bottom_label.configure(font=("Arial", self.get_responsive_font_size(12)))
        except Exception as e:
            logger.error(f"Error updating start screen fonts: {e}")
    
    def update_game_screen_fonts(self):
        # Update all game screen fonts for current window size
        try:
            if hasattr(self, 'question_counter_label'):
                self.question_counter_label.configure(font=("Arial", self.get_responsive_font_size(16)))
            if hasattr(self, 'question_label'):
                self.question_label.configure(font=("Arial", self.get_responsive_font_size(20)))
            if hasattr(self, 'yes_button'):
                self.yes_button.configure(font=("Arial", self.get_responsive_font_size(16), "bold"))
            if hasattr(self, 'no_button'):
                self.no_button.configure(font=("Arial", self.get_responsive_font_size(16), "bold"))
            if hasattr(self, 'reasoning_label'):
                self.reasoning_label.configure(font=("Arial", self.get_responsive_font_size(14)))
        except Exception as e:
            logger.error(f"Error updating game screen fonts: {e}")
    
    def on_text_focus(self, event):
        # Handle text entry focus - clear placeholder text
        pass  # Placeholder for any focus handling logic
    
    def update_question_text(self, text: str):
        # Update the question label text
        if hasattr(self, 'question_label'):
            self.question_label.configure(text=text)
    
    def update_question_counter(self, question_num: int):
        # Update the question counter
        self.current_question = question_num
        if hasattr(self, 'question_counter_label'):
            self.question_counter_label.configure(text=f"Question {question_num} of 20")
    
    def update_reasoning_text(self, reasoning: str = ""):
        # Update the reasoning text below the buttons
        if hasattr(self, 'reasoning_label'):
            if reasoning:
                display_text = f"AI's reasoning: {reasoning}"
            else:
                display_text = ""
            self.reasoning_label.configure(text=display_text)
    
    def get_user_input(self) -> str:
        # Get the text from the input field
        if hasattr(self, 'text_entry'):
            return self.text_entry.get().strip()
        return ""
    
    def show_feedback_message(self, message: str, color: str = "gray"):
        # Show feedback message in the bottom label
        if hasattr(self, 'bottom_label'):
            self.bottom_label.configure(text=message, foreground=color)
    
    def run(self):
        # Start the UI main loop
        self.root.mainloop()