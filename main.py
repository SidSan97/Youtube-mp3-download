import tkinter as tk
from tkinter import filedialog, messagebox, Label, Entry
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube
import subprocess
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytube.exceptions import VideoUnavailable, PytubeError

def excluir_video(caminho_arquivo):
    try:
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
            print(f"Arquivo '{caminho_arquivo}' excluído com sucesso.")

            messagebox.showinfo(title='Sucesso!', icon='info', message='Processo concluído com sucesso')
        else:
            print(f"Arquivo '{caminho_arquivo}' não encontrado.")
            messagebox.showinfo(title='Alerta!', icon='info', message='Processo concluído com exito.')
    except Exception as e:
        print(f"Erro ao excluir o arquivo: {e}")
        messagebox.showinfo(title='Alerta!', icon='info', message='Processo concluído com exito.')

def extrair_audio(video_path, audio_path):
    print("****************************** Extraindo audio ************************")
    print(f"video: {video_path}")
    try:
        video = VideoFileClip(video_path)
        print(video)

        audio = video.audio
        audio.write_audiofile(audio_path)
        print("Áudio salvo com sucesso!")

    except FileNotFoundError:
        messagebox.showerror("Arquivo não encontrado", "O vídeo não foi localizado.")
    except Exception as e:
        messagebox.showerror("Erro inesperado", f"Ocorreu um erro: {e}")
    finally:
        try:
            video.close()
        except:
            pass

    excluir_video(video_path)

def baixar_video(videoUrl, caminho_destino='Downloads'):
    try:
        yt = YouTube(videoUrl, on_progress_callback=on_progress)
        print(f"Título do vídeo: {yt.title}")

        if not os.path.exists(caminho_destino):
            os.makedirs(caminho_destino)

        ys = yt.streams.get_highest_resolution()
        ys.download(caminho_destino)
        print("Download concluído com sucesso!")

        video_path = os.path.join(caminho_destino, yt.title + '.mp4')
        audio_path = os.path.join(caminho_destino, yt.title + '.mp3')

        extrair_audio(video_path, audio_path)
    except VideoUnavailable:
        messagebox.showerror("Vídeo indisponível", "O vídeo solicitado não está disponível.")
    except PytubeError as e:
        messagebox.showerror("Erro do YouTube", f"Ocorreu um erro com a biblioteca Pytube: {e}")
    except Exception as e:
        messagebox.showerror("Erro inesperado", f"Ocorreu um erro inesperado: {e}")

def colar_dados():
    try:
        dados = root.clipboard_get()  # pega texto da área de transferência
        url.delete(0, tk.END)         # limpa o campo
        url.insert(0, dados)          # cola os dados
    except tk.TclError:
        messagebox.showerror("Erro", "A área de transferência está vazia ou não contém texto.")

def abrir_pasta():
    diretorio_atual = os.getcwd()
    pasta_docs = os.path.join(diretorio_atual, "Downloads")
    
    # Verifica se a pasta 'docs' existe dentro do diretório atual
    if os.path.exists(pasta_docs) and os.path.isdir(pasta_docs):
        diretorio_para_abrir = pasta_docs
    else:
        diretorio_para_abrir = diretorio_atual
    
    subprocess.Popen(f'explorer {os.path.realpath(diretorio_para_abrir)}')

root = tk.Tk()
root.title("Youtube MP3 download | By: Sidnei Santiago")
root.geometry("500x200+300+150")
root.resizable(height=False, width=False)

lbl1 = Label(root, text='Insira a URL do video', anchor='center')
lbl1.place(x=10, y=40)
url = Entry(justify='left', width=52)
url.place(x=135, y=40)

botao_url = tk.Button(root, text="Executar", command=lambda: baixar_video(url.get()))
botao_url.pack(pady=20)
botao_url.place(x=135, y=67)

# Botão de colar
botao_colar = tk.Button(root, text="Colar", command=colar_dados)
botao_colar.pack()
botao_colar.place(x=400, y=67)

botao_abrir_pasta = tk.Button(root, text="Abrir Pasta", command=abrir_pasta)
botao_abrir_pasta.pack(pady=20)
botao_abrir_pasta.place(x=205, y=150)


root.mainloop()