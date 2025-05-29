import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import random

class EWatchApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.initialize_systems()
        self.setup_ui()
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("eWatch Connect Lite")
        self.root.geometry("800x600")
        self.root.configure(bg='#121212')
        
    def initialize_systems(self):
        """Initialize all subsystems"""
        # User System
        self.current_user = {
            "name": "User",
            "storage": "500TB",
            "balance": 1000  # UGX
        }
        
        # Sample movie database
        self.movies = [
            {"title": "Action Movie", "price": 200, "image": None},
            {"title": "Comedy Film", "price": 150, "image": None},
            {"title": "Drama Story", "price": 180, "image": None},
            {"title": "Sci-Fi Adventure", "price": 250, "image": None},
        ]
        
        # Generate thumbnails
        for movie in self.movies:
            movie["image"] = self.generate_thumbnail(movie["title"])
    
    def generate_thumbnail(self, text):
        """Create simple thumbnail image"""
        img = Image.new('RGB', (150, 200), color=(random.randint(0, 100), 
                        random.randint(0, 100), random.randint(100, 255)))
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), text, fill=(255, 255, 255))
        return ImageTk.PhotoImage(img)
        
    def setup_ui(self):
        """Build user interface"""
        # Main notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        
        # Add tabs - pass self.root as master instead of self
        self.tabs = {
            "home": HomeTab(self.root, self),
            "movies": MovieTab(self.root, self),
            "account": AccountTab(self.root, self)
        }
        
        for name, tab in self.tabs.items():
            self.notebook.add(tab, text=name.capitalize())
            
        self.notebook.pack(fill='both', expand=True)
        
        # Status bar
        self.status_bar = ttk.Frame(self.root)
        ttk.Label(self.status_bar, 
                 text=f"User: {self.current_user['name']} | Balance: {self.current_user['balance']} UGX").pack(side='left')
        self.status_bar.pack(fill='x', side='bottom')

class HomeTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        ttk.Label(self, text="Welcome to eWatch Lite", font=('Helvetica', 16)).pack(pady=20)
        
        # Featured movies
        ttk.Label(self, text="Featured Movies").pack()
        
        featured_frame = ttk.Frame(self)
        for i, movie in enumerate(self.app.movies[:3]):
            btn = ttk.Button(featured_frame, image=movie["image"], 
                            command=lambda m=movie: self.watch_movie(m))
            btn.grid(row=0, column=i, padx=10)
        featured_frame.pack()

    def watch_movie(self, movie):
        """Handle movie purchase"""
        if self.app.current_user["balance"] >= movie["price"]:
            self.app.current_user["balance"] -= movie["price"]
            messagebox.showinfo("Success", f"Now playing: {movie['title']}")
            self.app.status_bar.children['!label'].config(
                text=f"User: {self.app.current_user['name']} | Balance: {self.app.current_user['balance']} UGX")
        else:
            messagebox.showerror("Error", "Insufficient balance")

class MovieTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        """Movie library interface"""
        # Search bar
        search_frame = ttk.Frame(self)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', expand=True, fill='x')
        
        ttk.Button(search_frame, text="Search", 
                  command=self.search_movies).pack(side='left')
        search_frame.pack(fill='x', pady=10)
        
        # Movie grid
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.movie_frame = ttk.Frame(self.canvas)
        
        self.movie_frame.bind(
    "<Configure>",
    lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
)  # This line was incorrectly indented before.configure(scrollregion=self.canvas.bbox("all"))
        
        self.canvas.create_window((0, 0), window=self.movie_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')
        
        # Load movies
        self.load_movies()
        
    def load_movies(self):
        """Load movie thumbnails"""
        for i, movie in enumerate(self.app.movies):
            frame = ttk.Frame(self.movie_frame)
            
            # Movie poster
            ttk.Label(frame, image=movie["image"]).pack()
            
            # Movie info
            ttk.Label(frame, text=movie["title"]).pack()
            ttk.Button(frame, text=f"Watch ({movie['price']} UGX)", 
                      command=lambda m=movie: self.watch_movie(m)).pack()
            
            frame.grid(row=i//2, column=i%2, padx=10, pady=10)
    
    def watch_movie(self, movie):
        """Handle movie purchase"""
        if self.app.current_user["balance"] >= movie["price"]:
            self.app.current_user["balance"] -= movie["price"]
            messagebox.showinfo("Success", f"Now playing: {movie['title']}")
            self.app.status_bar.children['!label'].config(
                text=f"User: {self.app.current_user['name']} | Balance: {self.app.current_user['balance']} UGX")
        else:
            messagebox.showerror("Error", "Insufficient balance")
    
    def search_movies(self):
        """Filter movies based on search"""
        query = self.search_entry.get().lower()
        
        for widget in self.movie_frame.winfo_children():
            widget.destroy()
            
        for i, movie in enumerate([m for m in self.app.movies if query in m["title"].lower()]):
            frame = ttk.Frame(self.movie_frame)
            ttk.Label(frame, image=movie["image"]).pack()
            ttk.Label(frame, text=movie["title"]).pack()
            ttk.Button(frame, text=f"Watch ({movie['price']} UGX)", 
                       command=lambda m=movie: self.watch_movie(m)).pack()
            frame.grid(row=i//2, column=i%2, padx=10, pady=10)

class AccountTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        """User account management"""
        ttk.Label(self, text="Account Details", font=('Helvetica', 14)).pack(pady=10)
        
        # User info
        info_frame = ttk.Frame(self)
        ttk.Label(info_frame, text="Name:").grid(row=0, column=0, sticky='e')
        ttk.Label(info_frame, text=self.app.current_user["name"]).grid(row=0, column=1, sticky='w')
        
        ttk.Label(info_frame, text="Balance:").grid(row=1, column=0, sticky='e')
        ttk.Label(info_frame, text=f"{self.app.current_user['balance']} UGX").grid(row=1, column=1, sticky='w')
        
        info_frame.pack()
        
        # Top up balance
        ttk.Button(self, text="Add 1000 UGX", 
                  command=self.add_balance).pack(pady=20)
        
    def add_balance(self):
        """Add virtual money to account"""
        self.app.current_user["balance"] += 1000
        messagebox.showinfo("Success", "1000 UGX added to your account")
        self.app.status_bar.children['!label'].config(
            text=f"User: {self.app.current_user['name']} | Balance: {self.app.current_user['balance']} UGX")

if __name__ == "__main__":
    root = tk.Tk()
    app = EWatchApp(root)
    root.mainloop()
