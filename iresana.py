import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# database
client_ids = {}
agent_ids = {}
property_ids = {}


def get_conn():
    return sqlite3.connect("rent.db")

def create_tables():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        personal_code TEXT,
        email TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        deals_count INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        area REAL,
        type TEXT,
        price INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        agent_id INTEGER,
        property_id INTEGER,
        deal_type TEXT,
        deal_price INTEGER
    )
    """)

    conn.commit()
    conn.close()



def fetch_clients():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, first_name || ' ' || last_name FROM clients")
    data = cur.fetchall()
    conn.close()
    return data

def fetch_agents():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, first_name || ' ' || last_name FROM agents")
    data = cur.fetchall()
    conn.close()
    return data

def fetch_properties():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, address FROM properties")
    data = cur.fetchall()
    conn.close()
    return data


def add_client():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clients (first_name, last_name, personal_code, email)
        VALUES (?, ?, ?, ?)
    """, (c_fn.get(), c_ln.get(), c_code.get(), c_email.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("OK", "Klients pievienots")

def add_agent():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO agents (first_name, last_name, email)
        VALUES (?, ?, ?)
    """, (a_fn.get(), a_ln.get(), a_email.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("OK", "Aģents pievienots")

def add_property():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO properties (address, area, type, price)
        VALUES (?, ?, ?, ?)
    """, (p_addr.get(), p_area.get(), p_type.get(), p_price.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("OK", "Īpašums pievienots")

def refresh_deal_lists():
    global client_ids, agent_ids, property_ids

    clients = fetch_clients()
    agents = fetch_agents()
    props = fetch_properties()

    deal_client["values"] = [c[1] for c in clients]
    deal_agent["values"] = [a[1] for a in agents]
    deal_property["values"] = [p[1] for p in props]

    client_ids = {c[1]: c[0] for c in clients}
    agent_ids = {a[1]: a[0] for a in agents}
    property_ids = {p[1]: p[0] for p in props}


def add_deal():
    if not deal_client.get() or not deal_agent.get() or not deal_property.get():
        messagebox.showerror("Kļūda", "Izvēlies klientu, aģentu un īpašumu")
        return

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO deals (client_id, agent_id, property_id, deal_type, deal_price)
        VALUES (?, ?, ?, ?, ?)
    """, (
        client_ids[deal_client.get()],
        agent_ids[deal_agent.get()],
        property_ids[deal_property.get()],
        deal_type.get(),
        deal_price.get()
    ))

    cur.execute("""
        UPDATE agents
        SET deals_count = deals_count + 1
        WHERE id = ?
    """, (agent_ids[deal_agent.get()],))

    conn.commit()
    conn.close()
    messagebox.showinfo("OK", "Darījums pievienots")



root = tk.Tk()
root.title("Nekustamā īpašuma sistēma")
root.geometry("500x400")

create_tables()

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# klienti
tab_client = ttk.Frame(notebook)
notebook.add(tab_client, text="Klienti")

c_fn = ttk.Entry(tab_client); c_ln = ttk.Entry(tab_client)
c_code = ttk.Entry(tab_client); c_email = ttk.Entry(tab_client)

for lbl, ent in [
    ("Vārds", c_fn),
    ("Uzvārds", c_ln),
    ("Personas kods", c_code),
    ("E-pasts", c_email)
]:
    ttk.Label(tab_client, text=lbl).pack()
    ent.pack()

ttk.Button(tab_client, text="Pievienot klientu", command=add_client).pack(pady=5)

# agenti
tab_agent = ttk.Frame(notebook)
notebook.add(tab_agent, text="Aģenti")

a_fn = ttk.Entry(tab_agent); a_ln = ttk.Entry(tab_agent); a_email = ttk.Entry(tab_agent)

for lbl, ent in [
    ("Vārds", a_fn),
    ("Uzvārds", a_ln),
    ("E-pasts", a_email)
]:
    ttk.Label(tab_agent, text=lbl).pack()
    ent.pack()

ttk.Button(tab_agent, text="Pievienot aģentu", command=add_agent).pack(pady=5)

tab_prop = ttk.Frame(notebook)
notebook.add(tab_prop, text="Īpašumi")

p_addr = ttk.Entry(tab_prop)
p_area = ttk.Entry(tab_prop)
p_type = ttk.Entry(tab_prop)
p_price = ttk.Entry(tab_prop)

for lbl, ent in [
    ("Adrese", p_addr),
    ("Platība m2", p_area),
    ("Tips", p_type),
    ("Cena", p_price)
]:
    ttk.Label(tab_prop, text=lbl).pack()
    ent.pack()

ttk.Button(tab_prop, text="Pievienot īpašumu", command=add_property).pack(pady=5)

#darijums
tab_deal = ttk.Frame(notebook)
notebook.add(tab_deal, text="Darījumi")

deal_client = ttk.Combobox(tab_deal, state="readonly")
deal_agent = ttk.Combobox(tab_deal, state="readonly")
deal_property = ttk.Combobox(tab_deal, state="readonly")
deal_type = ttk.Entry(tab_deal)
deal_price = ttk.Entry(tab_deal)

for lbl, ent in [
    ("Klients", deal_client),
    ("Aģents", deal_agent),
    ("Īpašums", deal_property),
    ("Darījuma veids", deal_type),
    ("Cena", deal_price)
]:
    ttk.Label(tab_deal, text=lbl).pack()
    ent.pack()

ttk.Button(tab_deal, text="Atjaunot sarakstus", command=refresh_deal_lists).pack(pady=3)
ttk.Button(tab_deal, text="Pievienot darījumu", command=add_deal).pack(pady=5)

root.mainloop()
