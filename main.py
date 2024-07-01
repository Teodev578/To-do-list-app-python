import tkinter as tk
from tkinter import Scrollbar, simpledialog, messagebox, filedialog, ttk
from datetime import datetime, timedelta
import threading
import time
import json

class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.geometry("1200x600")
        self.title("Liste de tâches")
        self.configure(background="#46494C")

        # Initialisation des tâches et des catégories
        self.tasks = []
        self.categories = ["Tout"]

        # Création des widgets de l'interface utilisateur
        self.create_widgets()

        # Chargement des catégories depuis le fichier
        self.load_categories()

        # Lancement du thread pour les rappels de tâches
        self.reminders_thread()

    def create_widgets(self):
        # Création du cadre de recherche
        self.search_frame = tk.Frame(self, bg="#46494C")
        self.search_frame.pack(pady=10)

        # Champ de saisie pour la recherche
        self.search_entry = tk.Entry(self.search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        # Bouton de recherche
        self.search_button = tk.Button(self.search_frame, text="Rechercher", command=self.search_task)
        self.search_button.pack(side=tk.LEFT, padx=5)

        # Bouton de tri par date limite
        self.sort_button = tk.Button(self.search_frame, text="Trier par date limite", command=self.sort_tasks)
        self.sort_button.pack(side=tk.LEFT, padx=5)

        # Création du cadre des catégories
        self.category_frame = tk.Frame(self, bg="#46494C")
        self.category_frame.pack(pady=10)

        # Étiquette pour les catégories
        self.category_label = tk.Label(self.category_frame, text="Catégories", bg="#46494C", fg="white")
        self.category_label.pack()

        # Liste des catégories
        self.category_Listbox = tk.Listbox(self.category_frame, selectmode=tk.SINGLE, height=6, width=20)
        self.category_Listbox.pack(side=tk.LEFT, padx=5)
        self.category_Listbox.bind("<<ListboxSelect>>", self.filter_tasks_by_category)

        # Cadre pour les boutons des catégories
        self.category_button_frame = tk.Frame(self.category_frame, bg="#46494C")
        self.category_button_frame.pack(side=tk.LEFT, padx=5)

        # Bouton pour ajouter une catégorie
        self.add_category_button = tk.Button(self.category_button_frame, text="Ajouter une catégorie", command=self.add_category)
        self.add_category_button.pack(pady=5)

        # Bouton pour supprimer une catégorie
        self.delete_category_button = tk.Button(self.category_button_frame, text="Supprimer une catégorie", command=self.delete_category)
        self.delete_category_button.pack(pady=5)

        # Liste des tâches avec barres de défilement
        self.tasks_frame = tk.Frame(self)
        self.tasks_frame.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Barre de défilement verticale
        self.task_scrollbar_y = Scrollbar(self.tasks_frame, orient=tk.VERTICAL)
        self.task_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Barre de défilement horizontale
        self.task_scrollbar_x = Scrollbar(self.tasks_frame, orient=tk.HORIZONTAL)
        self.task_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Modifier la taille du Treeview pour qu'il s'adapte à la taille du cadre
        self.tasks_Treeview = ttk.Treeview(self.tasks_frame, columns=("Titre", "Description", "Date Limite", "Statut", "Catégorie"), show="headings", yscrollcommand=self.task_scrollbar_y.set, xscrollcommand=self.task_scrollbar_x.set)

        self.tasks_Treeview.pack(expand=True, fill="both")

        # Configuration des barres de défilement pour agir sur la liste des tâches
        self.task_scrollbar_y.config(command=self.tasks_Treeview.yview)
        self.task_scrollbar_x.config(command=self.tasks_Treeview.xview)

        # Définition des en-têtes de colonnes
        self.tasks_Treeview.heading("Titre", text="Titre")
        self.tasks_Treeview.heading("Description", text="Description")
        self.tasks_Treeview.heading("Date Limite", text="Date Limite")
        self.tasks_Treeview.heading("Statut", text="Statut")
        self.tasks_Treeview.heading("Catégorie", text="Catégorie")

        # Définition de la largeur des colonnes
        self.tasks_Treeview.column("Titre", width=200)  # Modifiez cette valeur selon vos besoins
        self.tasks_Treeview.column("Description", width=300)  # Modifiez cette valeur selon vos besoins
        self.tasks_Treeview.column("Date Limite", width=100)  # Modifiez cette valeur selon vos besoins
        self.tasks_Treeview.column("Statut", width=100)  # Modifiez cette valeur selon vos besoins
        self.tasks_Treeview.column("Catégorie", width=100)  # Modifiez cette valeur selon vos besoins

        # Cadre pour les boutons des tâches
        self.button_frame = tk.Frame(self, bg="#46494C")
        self.button_frame.pack(pady=5)

        # Bouton pour ajouter une tâche
        self.add_task_button = tk.Button(self.button_frame, text="Ajouter une tâche", command=self.add_task)
        self.add_task_button.grid(row=0, column=0, padx=5)

        # Bouton pour éditer une tâche
        self.edit_task_button = tk.Button(self.button_frame, text="Éditer une tâche", command=self.edit_task)
        self.edit_task_button.grid(row=0, column=1, padx=5)

        # Bouton pour supprimer une tâche
        self.delete_task_button = tk.Button(self.button_frame, text="Supprimer une tâche", command=self.delete_task)
        self.delete_task_button.grid(row=0, column=2, padx=5)

        # Bouton pour marquer une tâche comme terminée
        self.mark_done_button = tk.Button(self.button_frame, text="Marquer comme terminée", command=self.mark_done)
        self.mark_done_button.grid(row=0, column=3, padx=5)

        # Bouton pour sauvegarder les tâches
        self.save_button = tk.Button(self.button_frame, text="Sauvegarder", command=self.save_tasks)
        self.save_button.grid(row=0, column=4, padx=5)

        # Bouton pour charger les tâches
        self.load_button = tk.Button(self.button_frame, text="Charger", command=self.load_tasks)
        self.load_button.grid(row=0, column=5, padx=5)

        # Bouton pour supprimer les tâches terminées
        self.delete_done_tasks_button = tk.Button(self.button_frame, text="Supprimer les tâches terminées", command=self.delete_done_tasks)
        self.delete_done_tasks_button.grid(row=0, column=6, padx=5)

        # Mise à jour de la liste des catégories
        self.update_category_listbox()


    def add_task(self):
        # Création d'une fenêtre de dialogue pour l'ajout de tâche
        add_task_dialog = tk.Toplevel(self)
        add_task_dialog.title("Ajouter une tâche")

        tk.Label(add_task_dialog, text="Titre:").grid(row=0, column=0, padx=10, pady=5)
        title_entry = tk.Entry(add_task_dialog)
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_task_dialog, text="Description:").grid(row=1, column=0, padx=10, pady=5)
        description_entry = tk.Entry(add_task_dialog)
        description_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_task_dialog, text="Date limite (AAAA-MM-JJ):").grid(row=2, column=0, padx=10, pady=5)
        deadline_entry = tk.Entry(add_task_dialog)
        deadline_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(add_task_dialog, text="Catégorie:").grid(row=3, column=0, padx=10, pady=5)
        category_combobox = ttk.Combobox(add_task_dialog, values=self.categories[1:])  # Exclure "Tout"
        category_combobox.grid(row=3, column=1, padx=10, pady=5)

        def save_task():
            title = title_entry.get()
            description = description_entry.get()
            deadline = deadline_entry.get()
            category = category_combobox.get()

            if not title:
                messagebox.showerror("Erreur", "Le titre de la tâche est obligatoire.")
                return

            if deadline:
                try:
                    datetime.strptime(deadline, '%Y-%m-%d')
                except ValueError:
                    messagebox.showerror("Date invalide", "Veuillez entrer une date valide au format AAAA-MM-JJ.")
                    return

            if not category:
                messagebox.showerror("Erreur", "La catégorie de la tâche est obligatoire.")
                return

            # Ajout de la tâche à la liste des tâches
            task = {"title": title, "description": description, "deadline": deadline, "status": "En cours", "category": category}
            self.tasks.append(task)
            self.update_task_listbox()
            add_task_dialog.destroy()

        tk.Button(add_task_dialog, text="Ajouter", command=save_task).grid(row=4, column=0, columnspan=2, pady=10)

    def edit_task(self):
        # Sélection de la tâche à éditer
        selected_item = self.tasks_Treeview.selection()
        if selected_item:
            task_index = self.tasks_Treeview.index(selected_item[0])
            task = self.tasks[task_index]

            # Création d'une fenêtre de dialogue pour l'édition de tâche
            edit_task_dialog = tk.Toplevel(self)
            edit_task_dialog.title("Éditer une tâche")

            tk.Label(edit_task_dialog, text="Titre:").grid(row=0, column=0, padx=10, pady=5)
            title_entry = tk.Entry(edit_task_dialog)
            title_entry.insert(0, task["title"])
            title_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(edit_task_dialog, text="Description:").grid(row=1, column=0, padx=10, pady=5)
            description_entry = tk.Entry(edit_task_dialog)
            description_entry.insert(0, task["description"])
            description_entry.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(edit_task_dialog, text="Date limite (AAAA-MM-JJ):").grid(row=2, column=0, padx=10, pady=5)
            deadline_entry = tk.Entry(edit_task_dialog)
            deadline_entry.insert(0, task["deadline"])
            deadline_entry.grid(row=2, column=1, padx=10, pady=5)

            tk.Label(edit_task_dialog, text="Catégorie:").grid(row=3, column=0, padx=10, pady=5)
            category_combobox = ttk.Combobox(edit_task_dialog, values=self.categories[1:])  # Exclure "Tout"
            category_combobox.set(task["category"])
            category_combobox.grid(row=3, column=1, padx=10, pady=5)

            def save_task():
                title = title_entry.get()
                description = description_entry.get()
                deadline = deadline_entry.get()
                category = category_combobox.get()

                if not title:
                    messagebox.showerror("Erreur", "Le titre de la tâche est obligatoire.")
                    return

                if deadline:
                    try:
                        datetime.strptime(deadline, '%Y-%m-%d')
                    except ValueError:
                        messagebox.showerror("Date invalide", "Veuillez entrer une date valide au format AAAA-MM-JJ.")
                        return

                if not category:
                    messagebox.showerror("Erreur", "La catégorie de la tâche est obligatoire.")
                    return

                # Mise à jour de la tâche
                self.tasks[task_index] = {"title": title, "description": description, "deadline": deadline, "status": task["status"], "category": category}
                self.update_task_listbox()
                edit_task_dialog.destroy()

            tk.Button(edit_task_dialog, text="Enregistrer", command=save_task).grid(row=4, column=0, columnspan=2, pady=10)

    def delete_task(self):
        # Suppression de la tâche sélectionnée
        selected_item = self.tasks_Treeview.selection()
        if selected_item:
            task_index = self.tasks_Treeview.index(selected_item[0])
            del self.tasks[task_index]
            self.update_task_listbox()

    def mark_done(self):
        # Marquage de la tâche sélectionnée comme terminée
        selected_item = self.tasks_Treeview.selection()
        if selected_item:
            task_index = self.tasks_Treeview.index(selected_item[0])
            self.tasks[task_index]["status"] = "Terminée"
            self.update_task_listbox()

    def delete_done_tasks(self):
        # Suppression des tâches terminées
        self.tasks = [task for task in self.tasks if task["status"] != "Terminée"]
        self.update_task_listbox()

    def search_task(self):
        # Recherche des tâches contenant le terme de recherche dans le titre
        search_term = self.search_entry.get()
        if search_term:
            results = [task for task in self.tasks if search_term.lower() in task["title"].lower()]
            self.update_task_listbox(results)

    def sort_tasks(self):
        # Tri des tâches par date limite
        self.tasks.sort(key=lambda x: datetime.strptime(x["deadline"], '%Y-%m-%d'))
        self.update_task_listbox()

    def add_category(self):
        # Ajout d'une nouvelle catégorie
        category = simpledialog.askstring("Catégorie", "Entrez une nouvelle catégorie:")
        if category and category not in self.categories:
            self.categories.append(category)
            self.update_category_listbox()

    def delete_category(self):
        # Suppression de la catégorie sélectionnée
        selected_category_index = self.category_Listbox.curselection()
        if selected_category_index and selected_category_index[0] != 0:  # Empêche la suppression de la catégorie "Tout"
            category = self.categories[selected_category_index[0]]
            self.categories.remove(category)
            self.tasks = [task for task in self.tasks if task["category"] != category]
            self.update_category_listbox()
            self.update_task_listbox()

    def get_selected_category(self):
        # Obtention de la catégorie sélectionnée
        selected_category_index = self.category_Listbox.curselection()
        if selected_category_index:
            return self.categories[selected_category_index[0]]
        return "Tout"

    def filter_tasks_by_category(self, event):
        # Filtrage des tâches par catégorie
        category = self.get_selected_category()
        if category == "Tout":
            self.update_task_listbox()
        else:
            filtered_tasks = [task for task in self.tasks if task["category"] == category]
            self.update_task_listbox(filtered_tasks)

    def save_tasks(self):
        # Sauvegarde des tâches dans un fichier
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for task in self.tasks:
                    task_data = f'{task["title"]} | {task["description"]} | {task["deadline"]} | {task["status"]} | {task["category"]}\n'
                    file.write(task_data)
            self.save_categories()  # Sauvegarde des catégories

    def load_tasks(self):
        # Chargement des tâches à partir d'un fichier
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.tasks = []
                for line in file:
                    title, description, deadline, status, category = line.strip().split(" | ")
                    self.tasks.append({"title": title, "description": description, "deadline": deadline, "status": status, "category": category})
                self.update_task_listbox()
                self.update_category_listbox()

    def save_categories(self):
        # Sauvegarde des catégories dans un fichier JSON
        with open("categories.json", "w") as file:
            json.dump(self.categories, file)

    def load_categories(self):
        # Chargement des catégories à partir d'un fichier JSON
        try:
            with open("categories.json", "r") as file:
                self.categories = json.load(file)
        except FileNotFoundError:
            self.categories = ["Tout"]
        self.update_category_listbox()

    def update_task_listbox(self, tasks=None):
        # Mise à jour de la liste des tâches affichées
        for item in self.tasks_Treeview.get_children():
            self.tasks_Treeview.delete(item)
        tasks = tasks if tasks is not None else self.tasks
        for task in tasks:
            self.tasks_Treeview.insert("", "end", values=(task["title"], task["description"], task["deadline"], task["status"], task["category"]))

    def update_category_listbox(self):
        # Mise à jour de la liste des catégories affichées
        self.category_Listbox.delete(0, tk.END)
        for category in self.categories:
            self.category_Listbox.insert(tk.END, category)

    def reminders_thread(self):
        # Démarrage du thread pour les rappels
        threading.Thread(target=self.check_reminders, daemon=True).start()

    def check_reminders(self):
        # Vérification des rappels de tâches toutes les minutes
        while True:
            now = datetime.now()
            for task in self.tasks:
                task_deadline = datetime.strptime(task["deadline"], '%Y-%m-%d')
                if task["status"] == "En cours" and now >= task_deadline - timedelta(minutes=30):
                    messagebox.showinfo("Rappel", f'La tâche "{task["title"]}" est arrivée à terme!')
            time.sleep(60)

if __name__ == "__main__":
    app = TodoListApp()
    app.mainloop()