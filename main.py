#scrapping info
from bs4 import BeautifulSoup
import requests
#gui
import tkinter as tk
from tkinter import messagebox
#preview
from jinja2 import Environment, FileSystemLoader
import webview


root = tk.Tk()
root.title("Summarizer")
tk.Label(root, text="Summarizer", font=("Aerial", 20)).grid(row=0,column=0)
tk.Label(root, text="Enter your book title:  ").grid(row=1,column=0)
title_entry = tk.Entry(root, width=20)
title_entry.grid(row=1, column=1)

def summarize():
    title = title_entry.get().replace(" ", "-").replace("'", "").lower()
    try:
        response = requests.get(f"https://sobrief.com/books/{title}")
        soup = BeautifulSoup(response.content, "lxml")

        author = soup.find("div", class_="book-author").contents[2].get_text()
        summary = soup.find("div", class_="chapter-summary")
        if summary.get_text(strip=True) == "":
            summary = "<h2 style='color: red'>unavailable</h2>"
        rating_tag = soup.find("div", class_="rating-value")
        rating = float(rating_tag.get_text(strip=True))
        image_tag = str(soup.find("img", class_="cover"))

        stars = "⭐" * round(rating)
        while len(stars) != 5:
            stars += "☆"

        data = {
            "title": title.replace("-", " ").title(),
            "summary": str(summary),
            "author": author,
            "rating": rating,
            "stars": stars,
            "image_tag": image_tag
        }

        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("template.html")
        html = template.render(data)
        def download():
            with open(f"{title}-summary.html", "w", encoding="utf-8") as file:
                file.write(html)
            messagebox.showinfo("Success", "File downloaded")
        tk.Button(root, text="Download as HTML", command= download).grid(row=4, column=1)
        webview.create_window("Summary", html=html)
        webview.start()

        
    except Exception as e:
        messagebox.showerror("Error", f"Book not found\n\n{str(e)}")

tk.Button(root, text="Generate Summary", command= summarize).grid(row=3, column=1)
tk.Label(root).grid(row=2, column=0)


root.mainloop()
