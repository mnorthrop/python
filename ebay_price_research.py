import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import messagebox
import numpy as np
import sys

def fetch_ebay_data(search_query, exclude_words):
    url = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}&_ipg=100&LH_Sold=1&LH_Complete=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('.s-item')
    
    listings = []
    for item in items:
        title_elem = item.select_one('.s-item__title')
        price_elem = item.select_one('.s-item__price')
        
        if title_elem and price_elem and 'Shop on eBay' not in title_elem.text:
            title = title_elem.text
            price = price_elem.text
            if not any(word.lower() in title.lower() for word in exclude_words):
                listings.append({
                    'title': title,
                    'price': price
                })
    
    return listings

def extract_price(price_str):
    prices = re.findall(r'\d+\.\d+', price_str)
    
    if prices:
        return float(prices[0])
    else:
        return 0.0

def search_and_display(event=None):
    search_query = search_entry.get()
    exclude_query = exclude_entry.get()
    exclude_words = exclude_query.split()
    listings = fetch_ebay_data(search_query, exclude_words)
    for listing in listings:
        listing['numeric_price'] = extract_price(listing['price'])
    
    # Sort listings by numeric price in descending order
    listings.sort(key=lambda x: x['numeric_price'], reverse=True)
    prices = [listing['numeric_price'] for listing in listings if listing['numeric_price'] > 0]

    count = len(prices)
    average_price = sum(prices) / count if count else 0
    median_price = np.median(prices) if count else 0
    q1 = np.percentile(prices, 25) if count else 0
    q3 = np.percentile(prices, 75) if count else 0
    min_price = min(prices) if count else 0
    max_price = max(prices) if count else 0
    
    results_text.delete('1.0', tk.END)
    results_text.insert(tk.END, f"Total Listings Found: {count}\n")
    results_text.insert(tk.END, f"Average Price: ${average_price:.2f}\n")
    results_text.insert(tk.END, f"Median Price: ${median_price:.2f}\n")
    results_text.insert(tk.END, f"Quartile 1 Price: ${q1:.2f}\n")
    results_text.insert(tk.END, f"Quartile 3 Price: ${q3:.2f}\n")
    results_text.insert(tk.END, f"Min Price: ${min_price:.2f}\n")
    results_text.insert(tk.END, f"Max Price: ${max_price:.2f}\n")
    results_text.insert(tk.END, f"Price Range: ${min_price:.2f} - ${max_price:.2f}\n\n")
    for listing in listings:
        results_text.insert(tk.END, f"{listing['title']} - {listing['price']}\n")

def clear_fields():
    search_entry.delete(0, tk.END)
    exclude_entry.delete(0, tk.END)
    results_text.delete('1.0', tk.END)
    for widget in graph_frame.winfo_children():
        widget.destroy()

def on_closing():
    root.destroy()
    sys.exit()

# Set up the main application window
root = tk.Tk()
root.title("eBay Price Research Tool")
root.geometry("1400x800")

# Create frames for layout
text_frame = tk.Frame(root)
graph_frame = tk.Frame(root)
text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create and place the search input field with a larger font for the label
search_label = tk.Label(text_frame, text="Enter your search query (all words will be searched together):", font=('Arial', 16))
search_label.pack()

# Modify the search entry box to be larger and easier to read
search_entry = tk.Entry(text_frame, width=80, font=('Arial', 16))
search_entry.pack()

# Label and input field for excluded words
exclude_label = tk.Label(text_frame, text="Enter words to exclude from titles (separated by spaces):", font=('Arial', 16))
exclude_label.pack()
exclude_entry = tk.Entry(text_frame, width=80, font=('Arial', 16))
exclude_entry.pack()

# Bind the Enter key to the search_and_display function
search_entry.bind('<Return>', search_and_display)
exclude_entry.bind('<Return>', search_and_display)

# Modify the search button to be larger and easier to read
search_button = tk.Button(text_frame, text="Search", command=search_and_display, font=('Arial', 14), width=10, height=2)
search_button.pack()

# Add a Clear button to reset the fields
clear_button = tk.Button(text_frame, text="Clear", command=clear_fields, font=('Arial', 14), width=10, height=2)
clear_button.pack()

# Create and place the results text widget with larger font
results_text = tk.Text(text_frame, wrap='word', font=('Arial', 14), width=80, height=20)
results_text.pack()

# Handle the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

print("Starting application...")
root.mainloop()
print("Application started successfully")
