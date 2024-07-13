import tkinter as tk
from tkinter import messagebox
import database as db
import yfinance as yf

class PortfolioTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        
        db.init_db()  # Initialize the database
        self.create_widgets()
    
    def create_widgets(self):
        # Add stock widgets
        self.add_stock_label = tk.Label(self.root, text="Add Stock")
        self.add_stock_label.grid(row=0, column=0, pady=10)
        
        self.symbol_label = tk.Label(self.root, text="Symbol:")
        self.symbol_label.grid(row=1, column=0)
        self.symbol_entry = tk.Entry(self.root)
        self.symbol_entry.grid(row=1, column=1)
        
        self.quantity_label = tk.Label(self.root, text="Quantity:")
        self.quantity_label.grid(row=2, column=0)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=2, column=1)
        
        self.price_label = tk.Label(self.root, text="Price:")
        self.price_label.grid(row=3, column=0)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.grid(row=3, column=1)
        
        self.add_button = tk.Button(self.root, text="Add", command=self.add_stock)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Remove stock widgets
        self.remove_stock_label = tk.Label(self.root, text="Remove Stock")
        self.remove_stock_label.grid(row=5, column=0, pady=10)
        
        self.remove_symbol_label = tk.Label(self.root, text="Symbol:")
        self.remove_symbol_label.grid(row=6, column=0)
        self.remove_symbol_entry = tk.Entry(self.root)
        self.remove_symbol_entry.grid(row=6, column=1)
        
        self.remove_button = tk.Button(self.root, text="Remove", command=self.remove_stock)
        self.remove_button.grid(row=7, column=0, columnspan=2, pady=10)
        
        # View portfolio button
        self.view_button = tk.Button(self.root, text="View Portfolio", command=self.view_portfolio)
        self.view_button.grid(row=8, column=0, columnspan=2, pady=10)
        
        # Calculate performance button
        self.calculate_button = tk.Button(self.root, text="Calculate Performance", command=self.calculate_performance)
        self.calculate_button.grid(row=9, column=0, columnspan=2, pady=10)
    
    def fetch_stock_data(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data for {symbol}: {e}")
            return None
    
    def add_stock(self):
        symbol = self.symbol_entry.get().upper()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        
        if not symbol or not quantity or not price:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and price must be a float.")
            return
        
        db.add_stock(symbol, quantity, price)
        messagebox.showinfo("Success", f"Added {quantity} shares of {symbol} at ${price} each to the portfolio.")
    
    def remove_stock(self):
        symbol = self.remove_symbol_entry.get().upper()
        
        if not symbol:
            messagebox.showerror("Error", "Please enter a stock symbol.")
            return
        
        db.remove_stock(symbol)
        messagebox.showinfo("Success", f"Removed {symbol} from the portfolio.")
    
    def view_portfolio(self):
        portfolio = db.get_portfolio()
        if portfolio:
            portfolio_message = "\n".join([f"{row[1]}: {row[2]} shares at ${row[3]} each" for row in portfolio])
            messagebox.showinfo("Portfolio", portfolio_message)
        else:
            messagebox.showinfo("Portfolio", "Portfolio is empty.")
    
    def calculate_performance(self):
        portfolio = db.get_portfolio()
        if portfolio:
            total_value = 0
            performance_message = ""
            for row in portfolio:
                stock_data = self.fetch_stock_data(row[1])
                if stock_data is not None and not stock_data.empty:
                    latest_close = stock_data['Close'].iloc[-1]
                    stock_value = latest_close * row[2]
                    total_value += stock_value
                    performance_message += f"{row[1]}: {row[2]} shares at ${latest_close} each, Value: ${stock_value}\n"
            
            performance_message += f"Total portfolio value: ${total_value}"
            messagebox.showinfo("Performance", performance_message)
        else:
            messagebox.showinfo("Performance", "Portfolio is empty.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioTracker(root)
    root.mainloop()
