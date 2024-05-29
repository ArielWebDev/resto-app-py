import mysql.connector
from prettytable import PrettyTable
from getpass import getpass

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restaurant"
)
cursor = db.cursor()

def register():
    name = input("Masukkan nama Anda: ")
    email = input("Masukkan email Anda: ")
    password = getpass("Masukkan kata sandi Anda: ")
    try:
        cursor.execute("INSERT INTO Customers (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        db.commit()
        print("Registrasi berhasil!")
    except mysql.connector.Error as err:
        print(f"Registrasi gagal: {err}")

def login(role):
    if role == "customer":
        email = input("Masukkan email Anda: ")
        password = getpass("Masukkan kata sandi Anda: ")
        cursor.execute("SELECT * FROM Customers WHERE email = %s AND password = %s", (email, password))
        return cursor.fetchone()
    elif role == "admin":
        email = input("Masukkan email Anda: ")
        password = getpass("Masukkan kata sandi Anda: ")
        cursor.execute("SELECT * FROM Admins WHERE email = %s AND password = %s", (email, password))
        return cursor.fetchone()

def display_menu():
    cursor.execute("SELECT * FROM MenuItems")
    menu_items = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["ID", "Nama", "Deskripsi", "Harga", "Kategori"]
    for item in menu_items:
        table.add_row(item)
    print(table)


def place_order(customer_id):
    display_menu()
    item_id = int(input("Masukkan ID item yang ingin dipesan: "))
    quantity = int(input("Masukkan jumlah: "))
    cursor.execute("INSERT INTO Orders (customer_id) VALUES (%s)", (customer_id,))
    order_id = cursor.lastrowid
    cursor.execute("INSERT INTO OrderItems (order_id, item_id, quantity) VALUES (%s, %s, %s)", (order_id, item_id, quantity))
    db.commit()
    print("Pesanan berhasil ditempatkan!")

def view_orders(customer_id):
    cursor.execute("SELECT * FROM Orders WHERE customer_id = %s", (customer_id,))
    orders = cursor.fetchall()
    for order in orders:
        print(order)

def view_all_orders():
    cursor.execute("SELECT * FROM Orders")
    orders = cursor.fetchall()
    for order in orders:
        print(order)

def update_order_status(order_id, status):
    cursor.execute("UPDATE Orders SET status = %s WHERE order_id = %s", (status, order_id))
    db.commit()
    print(f"Status pesanan {order_id} berhasil diubah menjadi {status}")

def admin_add_menu_item():
    name = input("Masukkan nama item menu baru: ")
    description = input("Masukkan deskripsi: ")
    price = float(input("Masukkan harga: "))
    category = input("Masukkan kategori: ")
    cursor.execute("INSERT INTO MenuItems (name, description, price, category) VALUES (%s, %s, %s, %s)", (name, description, price, category))
    db.commit()
    print("Item menu berhasil ditambahkan!")

# Main program
while True:
    print("\nSelamat datang di Sistem Pemesanan Restoran Online Indonesia")
    print("1. Masuk")
    print("2. Daftar")
    print("3. Keluar")
    choice = input("Masukkan pilihan Anda: ")

    if choice == "1":
        print("\nMasuk sebagai:")
        print("1. Pelanggan")
        print("2. Admin")
        role_choice = input("Masukkan peran Anda: ")
        if role_choice == "1":
            customer = login("customer")
            if customer:
                print("Login berhasil!")
                while True:
                    print("\nMenu Pelanggan:")
                    print("1. Tampilkan Menu")
                    print("2. Pesan")
                    print("3. Lihat Pesanan")
                    print("4. Batalkan Pesanan")
                    print("5. Logout")
                    customer_choice = input("Masukkan pilihan Anda: ")
                    if customer_choice == "1":
                        display_menu()
                    elif customer_choice == "2":
                        place_order(customer[0])
                    elif customer_choice == "3":
                        view_orders(customer[0])
                    elif customer_choice == "4":
                        pass  # Implementasi pembatalan pesanan
                    elif customer_choice == "5":
                        break
                    else:
                        print("Pilihan tidak valid. Silakan coba lagi.")
            else:
                print("Login gagal. Silakan coba lagi.")
        elif role_choice == "2":
            admin = login("admin")
            if admin:
                print("Login berhasil!")
                while True:
                    print("\nMenu Admin:")
                    print("1. Lihat Pesanan")
                    print("2. Ubah Status Pesanan")
                    print("3. Tambah Item Menu")
                    print("4. Logout")
                    admin_choice = input("Masukkan pilihan Anda: ")
                    if admin_choice == "1":
                        view_all_orders()
                    elif admin_choice == "2":
                        order_id = int(input("Masukkan ID pesanan: "))
                        status = input("Masukkan status baru (pending, completed, cancelled): ")
                        update_order_status(order_id, status)
                    elif admin_choice == "3":
                        admin_add_menu_item()
                    elif admin_choice == "4":
                        break
                    else:
                        print("Pilihan tidak valid. Silakan coba lagi.")
            else:
                print("Login gagal. Silakan coba lagi.")
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
    elif choice == "2":
        register()
    elif choice == "3":
        break
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")


cursor.close()
db.close()
