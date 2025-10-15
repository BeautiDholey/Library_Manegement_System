import sqlite3
from tkinter import *
from tkinter import ttk, messagebox as mb

root = Tk()
root.title("Library Management System")
root.state("zoomed")  # Full screen

# ---------- Database Setup ----------
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS Library')
cursor.execute('''
    CREATE TABLE Library (
        BK_ID TEXT PRIMARY KEY,
        BK_NAME TEXT,
        AUTHOR_NAME TEXT
    )
''')

books_data = [
    ("BK001", "To Kill a Mockingbird", "Harper Lee"),
    ("BK002", "1984", "George Orwell"),
    ("BK003", "Pride and Prejudice", "Jane Austen"),
    ("BK004", "The Great Gatsby", "F. Scott Fitzgerald"),
    ("BK005", "Moby Dick", "Herman Melville"),
    ("BK006", "War and Peace", "Leo Tolstoy"),
    ("BK007", "Crime and Punishment", "Fyodor Dostoevsky"),
    ("BK008", "The Catcher in the Rye", "J.D. Salinger"),
    ("BK009", "The Lord of the Rings", "J.R.R. Tolkien"),
    ("BK010", "Harry Potter and the Philosopher’s Stone", "J.K. Rowling"),
    ("BK011", "The Hobbit", "J.R.R. Tolkien"),
    ("BK012", "The Alchemist", "Paulo Coelho"),
    ("BK013", "Animal Farm", "George Orwell"),
    ("BK014", "Jane Eyre", "Charlotte Brontë"),
    ("BK015", "Brave New World", "Aldous Huxley"),
    ("BK016", "The Kite Runner", "Khaled Hosseini"),
    ("BK017", "Wuthering Heights", "Emily Brontë"),
    ("BK018", "Les Misérables", "Victor Hugo"),
    ("BK019", "A Tale of Two Cities", "Charles Dickens"),
    ("BK020", "Don Quixote", "Miguel de Cervantes"),
    ("BK021", "The Da Vinci Code", "Dan Brown"),
    ("BK022", "Angels and Demons", "Dan Brown"),
    ("BK023", "Inferno", "Dan Brown"),
    ("BK024", "Digital Fortress", "Dan Brown"),
    ("BK025", "Deception Point", "Dan Brown"),
    ("BK026", "The Fault in Our Stars", "John Green"),
    ("BK027", "Looking for Alaska", "John Green"),
    ("BK028", "Paper Towns", "John Green"),
    ("BK029", "The Silent Patient", "Alex Michaelides"),
    ("BK030", "It Ends With Us", "Colleen Hoover"),
    ("BK031", "Verity", "Colleen Hoover"),
    ("BK032", "Atomic Habits", "James Clear"),
    ("BK033", "Rich Dad Poor Dad", "Robert Kiyosaki"),
    ("BK034", "The Psychology of Money", "Morgan Housel"),
    ("BK035", "The Subtle Art of Not Giving a F*ck", "Mark Manson"),
    ("BK036", "Deep Work", "Cal Newport"),
    ("BK037", "Clean Code", "Robert C. Martin"),
    ("BK038", "The Pragmatic Programmer", "Andrew Hunt"),
    ("BK039", "Design Patterns", "Erich Gamma"),
    ("BK040", "Introduction to Algorithms", "Thomas H. Cormen"),
    ("BK041", "Artificial Intelligence: A Modern Approach", "Stuart Russell"),
    ("BK042", "Python Crash Course", "Eric Matthes"),
    ("BK043", "Fluent Python", "Luciano Ramalho"),
    ("BK044", "Machine Learning Yearning", "Andrew Ng"),
    ("BK045", "Hands-On Machine Learning", "Aurélien Géron"),
    ("BK046", "Data Science from Scratch", "Joel Grus"),
    ("BK047", "Computer Networks", "Andrew S. Tanenbaum"),
    ("BK048", "Operating System Concepts", "Abraham Silberschatz"),
    ("BK049", "Database System Concepts", "Abraham Silberschatz"),
    ("BK050", "Modern Operating Systems", "Andrew S. Tanenbaum"),
]

for book in books_data:
    cursor.execute('INSERT OR IGNORE INTO Library VALUES (?, ?, ?)', (book[0], book[1], book[2]))
conn.commit()

# ---------- Functions ----------
def clear_data():
    book_id_entry.delete(0, END)
    book_name_entry.delete(0, END)
    author_name_entry.delete(0, END)

def add_book():
    bid = book_id_entry.get().strip()
    bname = book_name_entry.get().strip()
    aname = author_name_entry.get().strip()
    if not (bid and bname and aname):
        mb.showerror("Error", "All fields are required.")
        return
    try:
        cursor.execute('INSERT INTO Library VALUES (?, ?, ?)', (bid, bname, aname))
        conn.commit()
        mb.showinfo("Success", "Book added successfully!")
        clear_and_display()
    except sqlite3.IntegrityError:
        mb.showerror("Error", "Book ID already exists!")

def delete_book():
    bid = book_id_entry.get().strip()
    if not bid:
        mb.showerror("Error", "Enter Book ID to delete.")
        return
    cursor.execute('DELETE FROM Library WHERE BK_ID = ?', (bid,))
    conn.commit()
    mb.showinfo("Success", "Book deleted successfully!")
    clear_and_display()

def update_book():
    bid = book_id_entry.get().strip()
    bname = book_name_entry.get().strip()
    aname = author_name_entry.get().strip()
    if not (bid and bname and aname):
        mb.showerror("Error", "All fields required for update.")
        return
    cursor.execute('UPDATE Library SET BK_NAME=?, AUTHOR_NAME=? WHERE BK_ID=?', (bname, aname, bid))
    conn.commit()
    mb.showinfo("Success", "Book updated successfully!")
    clear_and_display()

def clear_and_display():
    tree.delete(*tree.get_children())
    cursor.execute('SELECT * FROM Library')
    for row in cursor.fetchall():
        tree.insert('', END, values=row)

def search_record():
    search_value = search_entry.get().strip()
    field = search_by.get()
    if not search_value:
        mb.showerror("Input Error", "Please enter something to search.")
        return
    field_map = {"Book Name": "BK_NAME", "Book ID": "BK_ID", "Author": "AUTHOR_NAME"}
    query = f"SELECT * FROM Library WHERE {field_map[field]} LIKE ?"
    cursor.execute(query, ('%' + search_value + '%',))
    results = cursor.fetchall()
    tree.delete(*tree.get_children())
    for record in results:
        tree.insert('', END, values=record)

# ---------- GUI ----------
# Colors
bg_color = "#f0f0f0"
frame_color = "#e6e6e6"
button_color = "#607d8b"
button_hover = "#455a64"
title_color = "#37474f"
tree_color = "#eceff1"

root.configure(bg=bg_color)

Label(root, text="Library Management System", font=('Arial', 28, 'bold'), bg=title_color, fg="white").pack(side=TOP, fill=X)

frame = Frame(root, bg=frame_color)
frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

# Left section - inputs
left_frame = Frame(frame, bg=frame_color)
left_frame.pack(side=LEFT, fill=Y, padx=20, pady=10)

Label(left_frame, text="Book ID:", font=('Arial', 14), bg=frame_color).grid(row=0, column=0, sticky=W, pady=5)
book_id_entry = Entry(left_frame, font=('Arial', 14))
book_id_entry.grid(row=0, column=1, pady=5)

Label(left_frame, text="Book Name:", font=('Arial', 14), bg=frame_color).grid(row=1, column=0, sticky=W, pady=5)
book_name_entry = Entry(left_frame, font=('Arial', 14))
book_name_entry.grid(row=1, column=1, pady=5)

Label(left_frame, text="Author Name:", font=('Arial', 14), bg=frame_color).grid(row=2, column=0, sticky=W, pady=5)
author_name_entry = Entry(left_frame, font=('Arial', 14))
author_name_entry.grid(row=2, column=1, pady=5)

Button(left_frame, text="Add", font=('Arial', 12), bg=button_color, fg="white", command=add_book).grid(row=3, column=0, pady=10)
Button(left_frame, text="Update", font=('Arial', 12), bg=button_color, fg="white", command=update_book).grid(row=3, column=1, pady=10)
Button(left_frame, text="Delete", font=('Arial', 12), bg=button_color, fg="white", command=delete_book).grid(row=4, column=0, pady=10)
Button(left_frame, text="Clear", font=('Arial', 12), bg=button_color, fg="white", command=clear_data).grid(row=4, column=1, pady=10)

# Right section - table and search
right_frame = Frame(frame, bg=frame_color)
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

Label(right_frame, text="Search by:", font=('Arial', 14), bg=frame_color).place(x=10, y=10)
search_by = StringVar(value="Book ID")
OptionMenu(right_frame, search_by, "Book ID", "Book Name", "Author").place(x=120, y=5)
search_entry = Entry(right_frame, font=('Arial', 14))
search_entry.place(x=260, y=10)
Button(right_frame, text="Search", font=('Arial', 12), bg=button_color, fg="white", command=search_record).place(x=460, y=8)
Button(right_frame, text="Show All", font=('Arial', 12), bg=button_color, fg="white", command=clear_and_display).place(x=550, y=8)

# Table
tree = ttk.Treeview(right_frame, columns=('BK_ID', 'BK_NAME', 'AUTHOR_NAME'), show='headings')
tree.heading('BK_ID', text='Book ID')
tree.heading('BK_NAME', text='Book Name')
tree.heading('AUTHOR_NAME', text='Author Name')
tree.column('BK_ID', width=100)
tree.column('BK_NAME', width=350)
tree.column('AUTHOR_NAME', width=200)
tree.place(x=10, y=50, width=750, height=500)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background=tree_color, foreground="black", rowheight=25, fieldbackground=tree_color)
style.map('Treeview', background=[('selected', '#90a4ae')])

clear_and_display()
root.mainloop()
