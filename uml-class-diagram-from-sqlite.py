import sqlite3
from tkinter import Tk, filedialog
from graphviz import Digraph

"""WD: 
     Get the structure of the specified database into a dictionary
      - This function retrieves the list of tables, columns, and foreign key relationships 
      from the SQLite database, organizing the data into a dictionary.
"""
def get_db_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema = {}
    
    for table_name in tables:
        table_name = table_name[0]
        
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        schema[table_name] = {
            "columns": columns,
            "foreign_keys": []
        }
        
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys = cursor.fetchall()
        
        for fk in foreign_keys:
            schema[table_name]["foreign_keys"].append({
                "table": fk[2],
                "from": fk[3],
                "to": fk[4]
            })
    
    conn.close()
    return schema

"""WD: 
    Generate a UML diagram from the schema dictionary
    - This function uses Graphviz to generate and render a UML diagram based on the table 
      structures and foreign key relationships obtained from the schema.
"""
def generate_uml(schema):
    uml = Digraph("UML Diagram", filename="uml_diagram", format="png")
    uml.attr(rankdir="BT")
    
    for table_name, details in schema.items():
        columns = details["columns"]    
        table_label = f"{table_name}\n" + "-" * len(table_name) + "\n"
        for column in columns:
            table_label += f"+ {column[1]} : {column[2]}\n"
        
        uml.node(table_name, table_label)
    
    for table_name, details in schema.items():
        for fk in details["foreign_keys"]:
            uml.edge(table_name, fk["table"], label=f"{table_name}.{fk['from']} -> {fk['table']}.{fk['to']}")
    
    uml.render()
    print("Diagramme UML généré sous 'uml_diagram.png'.")

"""WD: 
    Main function to handle user input and initiate schema retrieval and UML generation
    - This function opens a file dialog to let the user select a SQLite database file. 
      If a file is selected, it retrieves the schema and generates a UML diagram.
"""
def main():
    root = Tk()
    root.withdraw()
    db_path = filedialog.askopenfilename(
        title="Sélectionner une base de données SQLite",
        filetypes=[("SQLite Database", "*.sqlite *.db")]
    )
    
    if db_path:
        schema = get_db_schema(db_path)
        generate_uml(schema)
    else:
        print("Aucune base de données sélectionnée.")

"""WD: 
    Entry point of the script to ensure the main function is called when the script is executed
    - This block ensures that the `main()` function runs when the script is executed directly (not when imported as a module).
"""
if __name__ == "__main__":
    main()
