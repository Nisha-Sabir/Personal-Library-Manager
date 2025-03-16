import streamlit as st
import json

LIBRARY_FILE = "library.json"

def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(title, author, year, genre, read):
    library.append({"Title": title, "Author": author, "Year": year, "Genre": genre, "Read": read})
    save_library(library)

def remove_book(title):
    global library
    library = [book for book in library if book["Title"].lower() != title.lower()]
    save_library(library)

def search_books(query):
    return [book for book in library if query.lower() in book["Title"].lower() or query.lower() in book["Author"].lower()]

def library_stats():
    total_books = len(library)
    read_books = sum(1 for book in library if book["Read"])
    return total_books, (read_books / total_books * 100) if total_books > 0 else 0

st.title("📚 Personal Library Manager")

library = load_library()

menu = st.sidebar.selectbox("Menu", ["Add Book", "Remove Book", "Search Book", "View Library", "Statistics"])

if menu == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1800, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read = st.checkbox("Mark as Read")
    
    if st.button("Add Book"):
        add_book(title, author, year, genre, read)
        st.success("Book added successfully!")

elif menu == "Remove Book":
    st.subheader("Remove a Book")
    remove_title = st.text_input("Enter book title to remove")
    if st.button("Remove"):
        remove_book(remove_title)
        st.success("Book removed successfully!")

elif menu == "Search Book":
    st.subheader("Search for a Book")
    query = st.text_input("Enter title or author")
    if st.button("Search"):
        results = search_books(query)
        if results:
            for book in results:
                st.write(book)
        else:
            st.warning("No matching books found.")

elif menu == "View Library":
    st.subheader("Your Book Collection")
    if library:
        for book in library:
            st.write(book)
    else:
        st.warning("Your library is empty.")

elif menu == "Statistics":
    st.subheader("Library Statistics")
    total, read_percentage = library_stats()
    st.write(f"Total Books: {total}")
    st.write(f"Read Percentage: {read_percentage:.2f}%")
