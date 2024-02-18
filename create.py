import g4f
import os
import tkinter as tk
from tkinter import font
import re
import json

g4f.debug.logging = True  # Enable debug logging
g4f.debug.version_check = False  # Disable automatic version checking

base_dir = os.getcwd()

def get_response_json(response):

    if response:
        try:
            response_json = json.loads(response)
            question = response_json.get("question",None)
            choices = response_json.get("choices",None)
            answer = response_json.get("answer",None)
            return question,choices,answer
        except:
            pass
    return None,None,None

def get_new_question():
    sonucLabel.config(text=f"")
    while True:
        
        subject = subjecttextarea.get("1.0",tk.END).strip()
  
        if subject == "" or subject is None:
            subject = "Genel kültür coğrafya veya tarih"
        
        print("Subject",subject,type(subject))
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo_16k_0613,
            
            messages=[{
                "role": "user",
                "content": """
                    KPSS lisans sınavı için """+ subject +""" konusunda sorusu oluşturmanı istiyorum.
                    Kısa uzunlukta soru olmasın.
                    5 şıklı,şıklar A,B,C,D ve E olacak.
                    Sonucu question,choices ve answer keyleri içerek json olarak yazdır.
                    Örneğin { "question": "example question","choices":{"A": "cevap1","B": "cevap2","C": "cevap3","D": "cevap4","E": "cevap5"} , "answer":"C" } gibi. 
                """
                }
            ],
        )

        question,choices,answer= get_response_json(response)
        if answer is None or question is None or choices is None:
            continue
        else:

            #Sorulayu Yazdır
            sorutextarea.delete(1.0, tk.END)
            sorutextarea.insert(tk.END, question + "\n")

            question_answer.set(answer)

            secenek1.config(text="A) " + choices.get("A"))
            secenek2.config(text="B) " + choices.get("B"))
            secenek3.config(text="C) " + choices.get("C"))
            secenek4.config(text="D) " + choices.get("D"))
            secenek5.config(text="E) " + choices.get("E"))

            break

def check_answer_is_true():

    secim = selected_answer.get()
    dogru_cevap = question_answer.get()

    if secim == dogru_cevap:
        sonucLabel.config(text="Doğru Tebrikler",fg="green")
    else:
        sonucLabel.config(text=f"Yanlış Doğru Cevap {dogru_cevap}",fg="red")


pencere = tk.Tk()
pencere.config(padx=40,pady=20)
pencere.geometry("1000x800")
pencere.title("KPSS SORU OLUŞTURUCU")

question_answer = tk.StringVar()
selected_answer = tk.StringVar()
subject = tk.StringVar()


#KONU METNİ
subject_panel = tk.Frame(pencere)
subject_panel.grid(row=1, column=1)

subjectLabel = tk.Label(subject_panel,text="Konu")
subjectLabel.grid(row=1, column=1)

subjecttextarea = tk.Text(subject_panel, height=1, width=40,font=font.Font(size=15),padx=10,pady=10)
subjecttextarea.grid(row=1, column=2)


#SORUNUN METNİ
question_panel = tk.Frame(pencere,bg="green")
question_panel.grid(row=2, column=1)

sorutextarea = tk.Text(question_panel, height=10, width=50,font=font.Font(size=15),padx=10,pady=10)
sorutextarea.grid(row=1, column=1)


# SEÇENEKLERİN GETİRİLMESİ
answer_panel = tk.Frame(pencere)
answer_panel.grid(row=3, column=1,pady=20)

secenek1=tk.Radiobutton(answer_panel, variable=selected_answer, value="A",wraplength=100,font=font.Font(size=10))
secenek1.grid(row=1, column=1)
secenek2=tk.Radiobutton(answer_panel, variable=selected_answer, value="B",wraplength=100,font=font.Font(size=10))
secenek2.grid(row=1, column=2)
secenek3=tk.Radiobutton(answer_panel, variable=selected_answer, value="C",wraplength=100,font=font.Font(size=10))
secenek3.grid(row=1, column=3)
secenek4=tk.Radiobutton(answer_panel, variable=selected_answer, value="D",wraplength=100,font=font.Font(size=10))
secenek4.grid(row=1, column=4)
secenek5=tk.Radiobutton(answer_panel, variable=selected_answer, value="E",wraplength=100,font=font.Font(size=10))
secenek5.grid(row=1, column=5)

cevabigonderbutton = tk.Button(answer_panel, text="Sonucu Göster", command=check_answer_is_true,font=font.Font(size=12))
cevabigonderbutton.grid(row=1, column=6)

sonucLabel = tk.Label(answer_panel,text="")
sonucLabel.grid(row=1, column=7, padx=20)


#AKSİYONLAR
yenisorubutton = tk.Button(pencere, text="Yeni Soru", command=get_new_question,font=font.Font(size=12))
yenisorubutton.grid(row=4, column=1)

# Pencereyi başlat
get_new_question()
pencere.mainloop()
