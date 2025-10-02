import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP Client - Command Sender")
        self.root.geometry("500x450")

        standard_font = ("Arial", 12)
        
        # Connection status
        self.status_label = tk.Label(root, text="Status: Disconnected", font=standard_font, fg="red")
        self.status_label.pack(pady=10)
        
        # Connection controls
        conn_frame = tk.Frame(root)
        conn_frame.pack(pady=5)
        
        tk.Label(conn_frame, text="Server IP:", font=standard_font).grid(row=0, column=0, padx=5)
        self.ip_entry = tk.Entry(conn_frame, width=15, font=standard_font)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(conn_frame, text="Port:", font=standard_font).grid(row=0, column=2, padx=5)
        self.port_entry = tk.Entry(conn_frame, width=8, font=standard_font)
        self.port_entry.insert(0, "5555")
        self.port_entry.grid(row=0, column=3, padx=5)
        
        self.connect_btn = tk.Button(conn_frame, text="Connect", command=self.connect_to_server, bg="green", fg="black", font=standard_font)
        self.connect_btn.grid(row=0, column=4, padx=5)
        
        self.disconnect_btn = tk.Button(conn_frame, text="Disconnect", command=self.disconnect_from_server, bg="red", fg="black", font=standard_font, state=tk.DISABLED)
        self.disconnect_btn.grid(row=0, column=5, padx=5)
        
        tk.Label(root, text="Send Commands:", font=standard_font).pack(pady=10)
        
        cmd_frame = tk.Frame(root)
        cmd_frame.pack(pady=5)
        
        commands = [
            ("HELLO", "blue"),
            ("TIME", "purple"),
            ("STATUS", "green"),
            ("DATA", "orange"),
            ("SHUTDOWN", "red")
        ]
        
        for i, (cmd, color) in enumerate(commands):
            btn = tk.Button(cmd_frame, text=cmd, width=12, height=2, command=lambda c=cmd: self.send_command(c), bg=color, fg="black", font=standard_font, state=tk.DISABLED)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            setattr(self, f"cmd_btn_{i}", btn)
        
        # Response display area
        tk.Label(root, text="Server Responses:", font=standard_font).pack(pady=5)
        self.response_area = scrolledtext.ScrolledText(root, width=60, height=10, font=standard_font)
        self.response_area.pack(pady=10, padx=10)
        
        tk.Button(root, text="Clear Responses", command=self.clear_responses, font=standard_font).pack(pady=5)
        
        # Socket connection
        self.client_socket = None
        self.connected = False
    
    def connect_to_server(self):
        try:
            host = self.ip_entry.get()
            port = int(self.port_entry.get())
            
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.connected = True
            
            self.status_label.config(text=f"Status: Connected to {host}:{port}", fg="green")
            self.connect_btn.config(state=tk.DISABLED)
            self.disconnect_btn.config(state=tk.NORMAL)
            self.ip_entry.config(state=tk.DISABLED)
            self.port_entry.config(state=tk.DISABLED)
            
            # Enable command buttons
            for i in range(5):
                getattr(self, f"cmd_btn_{i}").config(state=tk.NORMAL)
            
            self.display_response(f"Connected to server at {host}:{port}\n\n")
            
        except Exception as e:
            self.display_response(f"Connection error: {e}\n\n")
            self.status_label.config(text="Status: Connection Failed", fg="red")
    
    def disconnect_from_server(self):
        self.connected = False
        if self.client_socket:
            self.client_socket.close()
        
        self.status_label.config(text="Status: Disconnected", fg="red")
        self.connect_btn.config(state=tk.NORMAL)
        self.disconnect_btn.config(state=tk.DISABLED)
        self.ip_entry.config(state=tk.NORMAL)
        self.port_entry.config(state=tk.NORMAL)
        
        # Disable command buttons
        for i in range(5):
            getattr(self, f"cmd_btn_{i}").config(state=tk.DISABLED)
        
        self.display_response("Disconnected from server\n\n")
    
    def send_command(self, command):
        if not self.connected:
            self.display_response("Error: Not connected to server\n\n")
            return
        
        try:
            self.client_socket.send(command.encode('utf-8'))
            self.display_response(f"Sent: {command}\n")
            
            threading.Thread(target=self.receive_response, daemon=True).start()
            
        except Exception as e:
            self.display_response(f"Error sending command: {e}\n\n")
            self.disconnect_from_server()
    
    def receive_response(self):
        try:
            response = self.client_socket.recv(1024).decode('utf-8')
            self.display_response(f"Response: {response}\n\n")
        except Exception as e:
            self.display_response(f"Error receiving response: {e}\n\n")
    
    def display_response(self, message):
        self.response_area.insert(tk.END, message)
        self.response_area.see(tk.END)
    
    def clear_responses(self):
        self.response_area.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()

    app = ClientGUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.disconnect_from_server(), root.destroy()))
    
    root.mainloop()