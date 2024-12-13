# Inventory Manager

The Inventory Manager is a command-line program written in Python that allows you to load, search, summarize, and display inventory data from CSV files.

## Prerequisites

Before installing and using the program, make sure you have Python installed on your machine. The program also requires a few dependencies.

### Dependencies

- Python 3.x
- pandas
- colorama

## Installation

### 1. Clone or download the repository

If you haven't already, clone the repository using Git or download it manually.

```bash
git clone https://github.com/NicoHoed/script-inventaire.git
cd inventory-manager
```

### 2. Install the dependencies

Install the required modules using `pip`.

```bash
pip install -r requirements.txt
```

## Usage

The program runs through the command-line interface. Here are the steps to use it.

### 1. Run the program

Start the Python script using the following command:

```bash
python main.py
```

This will launch the Inventory Manager command-line interface.

### 2. Load CSV files

To load CSV files into the inventory, use the `load` command and specify the folder containing the CSV files.

```bash
load /path/to/folder
```

The program will load all CSV files in the specified folder and combine them into a single database.

### 3. Search for a product or category

Use the `search` command to search for a specific product or category in the inventory.

```bash
search category=Electronics
search product_name=Laptop
```

### 4. Display a summary of the data

To generate a summary of the inventory by category (total quantity and average price), use the `summary` command.

```bash
summary
```

You can also specify a filename to save the summary as a CSV:

```bash
summary /path/to/file.csv
```

### 5. Display the first few rows of the inventory

Use the `show` command to display the first few rows of the inventory (default is 5 rows).

```bash
show 10  # Displays the first 10 rows
```

### 6. Exit the program

To exit the application, use the `exit` command:

```bash
exit
```

## Example CSV

Here is an example of a CSV file for an inventory of electronic products:

```csv
product_name,quantity,unit_price,category
Laptop,10,800.0,Electronics
Smartphone,15,500.0,Electronics
Wireless Mouse,8,25.0,Electronics
```
