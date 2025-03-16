import streamlit as st # type: ignore
import json
import os

# File to store library data
LIBRARY_FILE = "library.json"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize library
library = load_library()

# Streamlit UI
st.title("📚 Personal Library Manager")

# Sidebar Menu
menu = st.sidebar.radio("Select an Option:", ["Add Book", "Remove Book", "Search Book", "Display Books", "Statistics"])

# 1️⃣ Add a Book
if menu == "Add Book":
    st.header("📖 Add a New Book")
    title = st.text_input("Enter Book Title")
    author = st.text_input("Enter Author Name")
    year = st.text_input("Enter Publication Year")
    genre = st.text_input("Enter Genre")
    read_status = st.checkbox("Mark as Read")

    if st.button("Add Book"):
        if title and author and year.isdigit():
            book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status}
            library.append(book)
            save_library(library)
            st.success(f"✅ '{title}' added successfully!")
        else:
            st.error("⚠ Please enter valid details.")

# 2️⃣ Remove a Book
elif menu == "Remove Book":
    st.header("🗑 Remove a Book")
    book_titles = [book["title"] for book in library]
    book_to_remove = st.selectbox("Select a Book to Remove", ["Select"] + book_titles)

    if st.button("Remove Book"):
        if book_to_remove != "Select":
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success(f"✅ '{book_to_remove}' removed successfully!")
        else:
            st.error("⚠ Please select a book.")

# 3️⃣ Search for a Book
elif menu == "Search Book":
    st.header("🔍 Search for a Book")
    search_query = st.text_input("Enter Book Title or Author")

    if st.button("Search"):
        results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            for book in results:
                read_status = "✅ Read" if book["read"] else "❌ Unread"
                st.write(f"📖 *{book['title']}* by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
        else:
            st.warning("⚠ No matching books found.")

# 4️⃣ Display All Books
elif menu == "Display Books":
    st.header("📚 Your Library Collection")
    if not library:
        st.info("📭 Your library is empty!")
    else:
        for book in library:
            read_status = "✅ Read" if book["read"] else "❌ Unread"
            st.write(f"📖 *{book['title']}* by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")

# 5️⃣ Display Statistics
elif menu == "Statistics":
    st.header("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books) * 100 if total_books else 0

    st.write(f"📚 *Total Books:* {total_books}")
    st.write(f"✅ *Read Books:* {read_books}")
    st.write(f"📈 *Percentage Read:* {percentage_read:.1f}%")

    # save changes on exit
    save_library(library)