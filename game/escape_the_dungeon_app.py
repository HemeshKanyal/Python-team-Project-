import tkinter as tk
from queue import Queue
import threading
import escape_the_dungeon

class TextAdventureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Adventure Game")

        self.text_display = tk.Text(root, wrap="word", state="disabled", width=80, height=20)
        self.text_display.pack()

        self.entry = tk.Entry(root)
        self.entry.bind("<Return>", self.process_input)
        self.entry.pack()

        self.input_queue = Queue()

        escape_the_dungeon.input = self.get_input
        escape_the_dungeon.print = self.display_text

        self.game_thread = threading.Thread(target=self.run_game)
        self.game_thread.start()

        self.root.after(100, self.check_game_thread)

    def get_input(self, prompt=""):
        """Custom input function to get input from GUI."""
        self.display_text(prompt)
        return self.input_queue.get()

    def process_input(self, event):
        """Handle user input from entry widget."""
        user_input = self.entry.get()
        self.input_queue.put(user_input)
        self.entry.delete(0, tk.END)

    def display_text(self, text):
        """Display text in the text widget."""
        self.text_display.config(state="normal")
        self.text_display.insert(tk.END, text + "\n")
        self.text_display.config(state="disabled")
        self.text_display.see(tk.END)

    def run_game(self):
        """Run the game in a separate thread."""
        try:
            escape_the_dungeon.main()
        except Exception as e:
            self.display_text(f"An error occurred: {e}")

    def check_game_thread(self):
        """Check if the game thread is still running and handle cleanup if it stops."""
        if not self.game_thread.is_alive():
            self.display_text("Game has ended.")
        else:
            self.root.after(100, self.check_game_thread)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextAdventureApp(root)
    root.mainloop()
