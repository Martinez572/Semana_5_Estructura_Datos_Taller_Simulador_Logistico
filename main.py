import tkinter as tk
from collections import deque


class SmartLogisticsApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Smart Logistics Hub")
        self.root.geometry("1200x600")

        # 🔵 Cola de pedidos (FIFO)
        self.order_queue = deque()

        # 🟡 Pedidos procesados listos para envío
        self.ready_orders = []

        # 🔴 Pila del camión (LIFO)
        self.truck_stack = []

        # 🟢 Array fijo del inventario
        self.inventory = [
            "Electrónica",
            "Ropa",
            "Hogar",
            "Deportes",
            "Alimentos"
        ]

        # Contador automático de pedidos
        self.order_id_counter = 1

        # Crear interfaz
        self.create_interface()

    # =============================
    # CREAR INTERFAZ
    # =============================
    def create_interface(self):

        title = tk.Label(
            self.root,
            text="SMART LOGISTICS HUB",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        # ----------- PEDIDOS (COLA) -----------
        orders_frame = tk.LabelFrame(
            self.root,
            text="Pedidos Entrantes (Cola FIFO)",
            padx=10,
            pady=10
        )
        orders_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.order_entry = tk.Entry(orders_frame, width=30)
        self.order_entry.pack(pady=5)

        add_button = tk.Button(
            orders_frame,
            text="Agregar pedido",
            command=self.add_order
        )
        add_button.pack(pady=5)

        process_button = tk.Button(
            orders_frame,
            text="Procesar pedido",
            command=self.process_order
        )
        process_button.pack(pady=5)

        self.order_listbox = tk.Listbox(orders_frame, width=35, height=15)
        self.order_listbox.pack(pady=10)

        # ----------- LISTOS PARA ENVÍO -----------
        ready_frame = tk.LabelFrame(
            self.root,
            text="Pedidos Listos para Envío",
            padx=10,
            pady=10
        )
        ready_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        load_button = tk.Button(
            ready_frame,
            text="Cargar al camión",
            command=self.load_to_truck
        )
        load_button.pack(pady=5)

        self.ready_listbox = tk.Listbox(ready_frame, width=35, height=15)
        self.ready_listbox.pack(pady=10)

        # ----------- CAMIÓN (PILA) -----------
        truck_frame = tk.LabelFrame(
            self.root,
            text="Camión de Reparto (Pila LIFO)",
            padx=10,
            pady=10
        )
        truck_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        deliver_button = tk.Button(
            truck_frame,
            text="Entregar paquete",
            command=self.deliver_package
        )
        deliver_button.pack(pady=5)

        self.truck_listbox = tk.Listbox(truck_frame, width=35, height=15)
        self.truck_listbox.pack(pady=10)

        self.top_label = tk.Label(truck_frame, text="Paquete en la cima: Ninguno")
        self.top_label.pack(pady=5)

        # ----------- INVENTARIO (ARRAY) -----------
        inventory_frame = tk.LabelFrame(
            self.root,
            text="Inventario del Almacén (Array Fijo)",
            padx=10,
            pady=10
        )
        inventory_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.inventory_listbox = tk.Listbox(inventory_frame, width=35, height=15)
        self.inventory_listbox.pack(pady=10)

        self.update_inventory_list()

    # =============================
    # FUNCIONES COLA (FIFO)
    # =============================
    def add_order(self):
        order_name = self.order_entry.get()

        if order_name != "":
            order_id = f"Pedido-{self.order_id_counter}: {order_name}"
            self.order_queue.append(order_id)
            self.order_id_counter += 1

            self.update_order_list()
            self.order_entry.delete(0, tk.END)

    def process_order(self):
        if len(self.order_queue) > 0:
            order = self.order_queue.popleft()
            self.ready_orders.append(order)

            self.update_order_list()
            self.update_ready_list()

    def update_order_list(self):
        self.order_listbox.delete(0, tk.END)

        for order in self.order_queue:
            self.order_listbox.insert(tk.END, order)

    # =============================
    # FUNCIONES LISTOS
    # =============================
    def update_ready_list(self):
        self.ready_listbox.delete(0, tk.END)

        for order in self.ready_orders:
            self.ready_listbox.insert(tk.END, order)

    # =============================
    # FUNCIONES PILA (LIFO)
    # =============================
    def load_to_truck(self):
        if len(self.ready_orders) > 0:
            order = self.ready_orders.pop(0)
            self.truck_stack.append(order)

            self.update_ready_list()
            self.update_truck_list()

    def deliver_package(self):
        if len(self.truck_stack) > 0:
            self.truck_stack.pop()
            self.update_truck_list()

    def update_truck_list(self):
        self.truck_listbox.delete(0, tk.END)

        for package in self.truck_stack:
            self.truck_listbox.insert(tk.END, package)

        if len(self.truck_stack) > 0:
            top_package = self.truck_stack[-1]
            self.top_label.config(text=f"Paquete en la cima: {top_package}")
        else:
            self.top_label.config(text="Paquete en la cima: Ninguno")

    # =============================
    # FUNCIONES ARRAY (INVENTARIO)
    # =============================
    def update_inventory_list(self):
        self.inventory_listbox.delete(0, tk.END)

        for index, category in enumerate(self.inventory):
            item_text = f"Pasillo {index} → {category}"
            self.inventory_listbox.insert(tk.END, item_text)


# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartLogisticsApp(root)
    root.mainloop()