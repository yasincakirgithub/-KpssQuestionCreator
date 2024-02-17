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
 
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo_16k_0613,
            
            messages=[{
                "role": "user",
                "content": """
                    KPSS lisans genel kültür coğrafya veya tarih sorusu oluşturur musun?
                    Sorunun içeriği 19.yüzyıl Osmanlı Devleti Islahatlarla ilgili sorular olsun.
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

            secenek1.config(text=choices.get("A"))
            secenek2.config(text=choices.get("B"))
            secenek3.config(text=choices.get("C"))
            secenek4.config(text=choices.get("D"))
            secenek5.config(text=choices.get("E"))

            break

def check_answer_is_true():

    secim = selected_answer.get()
    dogru_cevap = question_answer.get()

    if secim == dogru_cevap:
        sonucLabel.config(text="Doğru Tebrikler",fg="green")
    else:
        sonucLabel.config(text=f"Yanlış Doğru Cevap {dogru_cevap}",fg="red")


pencere = tk.Tk()
pencere.geometry("1000x800")
pencere.title("KPSS SORU OLUŞTURUCU")

question_answer = tk.StringVar()


#SORUNUN METNİ

sorutag = tk.Label(pencere, text="Soru:")
sorutag.grid(row=1, column=1, padx=40)
sorutextarea = tk.Text(pencere, height=20, width=50,padx=40,pady=20,font=font.Font(family="Arial", size=15, weight="bold"))
sorutextarea.grid(row=2, column=1, padx=40)


# SEÇENEKLERİN GETİRİLMESİ
panel = tk.Frame(pencere, height=20, width=50, padx=40)
panel.grid(row=3, column=1, padx=40)

selected_answer = tk.StringVar()
secenek1=tk.Radiobutton(panel, text="A", variable=selected_answer, value="A",wraplength=100,font=font.Font(family="Arial", size=13, weight="bold"))
secenek1.grid(row=1, column=1, sticky="w")
secenek2=tk.Radiobutton(panel, text="B", variable=selected_answer, value="B",wraplength=100,font=font.Font(family="Arial", size=13, weight="bold"))
secenek2.grid(row=1, column=2, sticky="w")
secenek3=tk.Radiobutton(panel, text="C", variable=selected_answer, value="C",wraplength=100,font=font.Font(family="Arial", size=13, weight="bold"))
secenek3.grid(row=1, column=3, sticky="w")
secenek4=tk.Radiobutton(panel, text="D", variable=selected_answer, value="D",wraplength=100,font=font.Font(family="Arial", size=13, weight="bold"))
secenek4.grid(row=1, column=4, sticky="w")
secenek5=tk.Radiobutton(panel, text="E", variable=selected_answer, value="E",wraplength=100,font=font.Font(family="Arial", size=13, weight="bold"))
secenek5.grid(row=1, column=5, sticky="w")

sonucLabel = tk.Label(panel,text="")
sonucLabel.grid(row=1, column=6, padx=20)


#AKSİYONLAR
cevabigonderbutton = tk.Button(pencere, text="Sonucu Göster", command=check_answer_is_true,font=font.Font(family="Arial", size=15, weight="bold"))
cevabigonderbutton.grid(row=8, column=1, padx=40)

yenisorubutton = tk.Button(pencere, text="Yeni Soru", command=get_new_question,font=font.Font(family="Arial", size=15, weight="bold"))
yenisorubutton.grid(row=9, column=1, padx=40)

# Pencereyi başlat
pencere.mainloop()
