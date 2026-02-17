
import customtkinter as ctk
import threading
import assistant_pro as core

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("600x500")
app.title("Nova AI Assistant")

chatbox = ctk.CTkTextbox(app,width=520,height=300,font=("Arial",14))
chatbox.pack(pady=15)
chatbox.insert("end","System: Say 'Nova' to wake me up...\n")
chatbox.configure(state="disabled")

def log(msg):
    chatbox.configure(state="normal")
    chatbox.insert("end",msg+"\n")
    chatbox.see("end")
    chatbox.configure(state="disabled")

def start():
    log("System: Wake mode active")
    threading.Thread(target=core.listen_for_wake,args=(log,),daemon=True).start()

title = ctk.CTkLabel(app,text="NOVA Voice Assistant",font=("Arial",26,"bold"))
title.pack(pady=10)

btn = ctk.CTkButton(app,text="Start Wake Mode",height=45,font=("Arial",16,"bold"),command=start)
btn.pack(pady=10)

exitb = ctk.CTkButton(app,text="Exit",fg_color="red",command=app.destroy)
exitb.pack(pady=10)

app.mainloop()
