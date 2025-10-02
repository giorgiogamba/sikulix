import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP Server - Receiver")
        self.root.geometry("500x400")

        standard_font = ("Arial", 12)
        
        # Server status
        self.status_label = tk.Label(root, text="Server Status: Stopped", fg="red")
        self.status_label.pack(pady=10)
        
        # Display area for received messages
        tk.Label( root, text="Received Commands:", font=standard_font).pack()
        self.display_area = scrolledtext.ScrolledText(root, width=60, height=15, font=standard_font)
        self.display_area.pack(pady=10, padx=10)
    
        # General button frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        # Start button
        self.start_btn = tk.Button(button_frame, text="Start Server", command=self.start_server, bg="green", fg="black", font=standard_font, width=20)
        self.start_btn.grid(row=0, column=0, padx=5)
    
        # Stop button 
        self.stop_btn = tk.Button(button_frame, text="Stop Server", command=self.stop_server, bg="red", fg="black", font=standard_font, width=20, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Clear button
        self.clear_btn = tk.Button(button_frame, text="Clear Display", command=self.clear_display, font=standard_font, width=12)
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        # Server configuration
        self.host = '127.0.0.1'
        self.port = 5555
        self.server_socket = None
        self.running = False
        
    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            self.status_label.config(text=f"Server Status: Running on {self.host}:{self.port}", fg="green")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.display_message(f"Server started on {self.host}:{self.port}\n")
            
            # Start accepting connections in a separate thread
            threading.Thread(target=self.accept_connections, daemon=True).start()
            
        except Exception as e:
            self.display_message(f"Error starting server: {e}\n")
    
    def accept_connections(self):
        while self.running:
            try:
                self.server_socket.settimeout(1.0)
                client_socket, address = self.server_socket.accept()
                self.display_message(f"Connection from {address}\n")
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    self.display_message(f"Error accepting connection: {e}\n")
                break
    
    def handle_client(self, client_socket):
        try:
            while self.running:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                self.process_command(data)
                
                # Send ack
                response = f"Command '{data}' received and processed"
                client_socket.send(response.encode('utf-8'))
                
        except Exception as e:
            self.display_message(f"Error handling client: {e}\n")
        finally:
            client_socket.close()
    
    def process_command(self, command):
        # Process different commands and display results
        results = {
            "HELLO": "[Server] Hello!",
            "TIME": "[Server] Processing time request...",
            "STATUS": "[Server] System is operational.",
            "DATA": "[Server] Data retrieval in progress...",
            "SHUTDOWN": "[Server] Shutdown command received."
        }
        
        result = results.get(command, f"[Server] Unknown command '{command}'")
        self.display_message(f">>> Command: {command}\n")
        self.display_message(f"    Result: {result}\n\n")
    
    def display_message(self, message):
        self.display_area.insert(tk.END, message)
        self.display_area.see(tk.END)
    
    def stop_server(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        
        self.status_label.config(text="[Server] Stopped", fg="red")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.display_message("Server stopped\n")
    
    def clear_display(self):
        self.display_area.delete(1.0, tk.END)

if __name__ == "__main__":
    
    root = tk.Tk()
    app = ServerGUI(root)

    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop_server(), root.destroy()))
    
    root.mainloop()