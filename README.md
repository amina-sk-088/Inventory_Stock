# 📦 Inventory and Stock Management System

A menu-driven Python console application for managing product inventory. It lets you add products, track stock, record sales, restock items, get low-stock alerts, calculate total inventory value, and view charts. All data is saved automatically to a JSON file.

## 📖 Overview

Small shops often track stock on paper or in scattered spreadsheets, which leads to stockouts, mistakes, and no clear picture of inventory value. This project provides a simple, lightweight tool that keeps all stock information in one place, warns you when items run low, and shows the data visually.

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Add Product** | Add a product with ID, name, price, quantity, and low-stock limit. Duplicate IDs are rejected. |
| 2 | **View Products** | Display all products with their details and the total product count. |
| 3 | **Sell Product** | Reduce stock after a sale. Prevents selling more than what is available and shows the sale value. |
| 4 | **Restock Product** | Add new units to an existing product. |
| 5 | **Low Stock Alerts** | Flags items as `LOW STOCK` or `OUT OF STOCK` based on each product's limit. |
| 6 | **Total Inventory Value** | Shows value per product (price × quantity) and the overall total in Rs. |
| 7 | **View Charts** | Dashboard with four charts: available stock, inventory value, stock distribution, and stock vs low-stock limit. |
| 8 | **Exit** | Closes the program safely. |

### Extra highlights
- 💾 **Automatic saving** to `inventory.json` after every change
- ✅ **Input validation** for numbers, empty fields, and negative values
- 🔄 **Rollback on save failure**, so memory and file stay consistent
- 🛡️ **Safe file loading** that skips corrupted or invalid records
- 🧹 **Clean interface** that clears the screen between actions
- 📊 **Optional charts**: the program still works if Matplotlib is not installed

## 🛠️ Tech Stack

- **Language:** Python 3
- **Data storage:** JSON file (`inventory.json`)
- **Libraries:**
  - `json`, `os` (built-in)
  - `matplotlib` (optional, only for the charts feature)

## 📁 Project Structure

```
Inventory_Stock/
├── main.py           # Main program
├── inventory.json    # Product data (created/updated automatically)
└── README.md         # Project documentation
```

## 🚀 Setup and Run

### 1. Prerequisites
Install **Python 3.8 or higher** from [python.org](https://www.python.org/downloads/).

### 2. Clone the repository
```bash
git clone https://github.com/amina-sk-088/Inventory_Stock.git
cd Inventory_Stock
```

### 3. (Optional) Install Matplotlib for charts
```bash
python -m pip install matplotlib
```

### 4. Run the program
```bash
python main.py
```

## 🖥️ Usage

When the program starts, you will see this menu:

```
===================================
 INVENTORY AND STOCK MANAGEMENT
===================================
1. Add Product
2. View Products
3. Sell Product
4. Restock Product
5. Low Stock Alerts
6. Total Inventory Value
7. View Charts
8. Exit
===================================
Enter your choice (1-8):
```

Type a number from 1 to 8 and follow the prompts. After each action, press **Enter** to return to the menu.

## 🗄️ Data Storage

Data is stored in `inventory.json` in the same folder as `main.py`. The file is created automatically when you add your first product. Each product has this structure:

```json
{
    "101": {
        "name": "Notebook",
        "price": 45.0,
        "quantity": 100,
        "low_limit": 10
    }
}
```

| Field | Meaning |
|-------|---------|
| Key (`"101"`) | Unique product ID |
| `name` | Product name |
| `price` | Price per unit in Rs. |
| `quantity` | Units currently in stock |
| `low_limit` | Stock level at or below which a low-stock alert appears |

## ⚙️ Environment Variables and APIs

- **Environment variables:** none required
- **External APIs:** none used
- **Database:** none. A local JSON file is used instead.

## 🔮 Future Improvements

- Search and filter products
- Edit and delete products
- Sales history and reports
- Export data to CSV or Excel
- GUI or web version
- Switch from JSON to a database such as SQLite

## 👤 Team Contributions

| Member | Contribution |
|--------|--------------|
| **Amina Shaik** | Designed and developed the complete application: inventory logic, JSON storage, input validation, alerts, and chart dashboard |

## 📄 License

This project is for educational purposes.
