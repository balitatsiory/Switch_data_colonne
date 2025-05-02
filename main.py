import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog
from ttkbootstrap.tableview import Tableview
from tkinter import messagebox

root = tb.Window(themename="superhero")
root.title("Programme Recitale")
root.geometry('1000x900')

alltabs = tb.Notebook(root, bootstyle="dark")
alltabs.pack(pady=10)

tab1 = tb.Frame(alltabs)
tab2 = tb.Frame(alltabs)

alltabs.add(tab1, text="Importation")
alltabs.add(tab2, text="Exportation")

global column_headers

column_headers = [
      {"text": "Odre", "anchor": "center"},
      {"text": "Nom Colonne", "anchor": "center"}
   ]



# Dictionnaire "affichage" => "valeur réelle"
global separator_options
separator_options = {
   "Tabulation": "\t",
   "Point-virgule ;": ";",
   "Virgule ,": ",",
   "Espace": " ",
   "Point .": "."
}

global format_options
format_options = {
   "Excel": ".xlsx",
   ".txt": ".txt",
   ".csv": ".csv",
}



global dictionnaire
dictionnaire = dict()
global combobox_var_format



# def tableviewcolonnes(container,root,nom_colonnes):
   # column_headers = [
   #                 {"text": " Name"            , "stretch": True, "anchor": "center"},
   #                 {"text": " Age"             , "stretch": True, "anchor": "center"},
   #                 {"text": " Email"           , "stretch": True, "anchor": "center"},
   # ]
   # colors = root.style.colors
   # data_table  = Tableview(
   #                      master     = container,
   #                      coldata    = column_headers,
   #                      rowdata    = nom_colonnes,
   #                      pagesize   = 10,
   #                      height     = 10,
   #                      autofit    = True,
   #                      paginated  = True,
   #                      searchable = True,
   #                      bootstyle  = SUCCESS,
                        
   #                      stripecolor = (colors.light, None),
   #                     )
   # return data_table

def afficher_message_error(message):
   messagebox.showerror(title="Message d'erreur",message=message)
   return

def afficher_message_success(path):
    messagebox.showinfo("Succès", "Fichier exporter vers "+path+" avec succès.")



def on_file_select():
   file_path = filedialog.askopenfilename(
      filetypes=[("Fichiers texte", "*.txt *.csv"), ("Tous les fichiers", "*.*")]
   )
   if file_path:
     readonly_entry_var.set(file_path)
   #   print(file_path)
     lecture_file(file_path)
   return

def on_config_file_select():
   global nb_lignes_data_import

   file_path = filedialog.askopenfilename(
      filetypes=[("Fichiers texte", "*.txt *.csv"), ("Tous les fichiers", "*.*")]
   )
   if file_path:
      readonly_entry_var_tab2.set(file_path)
      if len(dictionnaire) == 0 :
         afficher_message_error("Aucun donnees importer")
         return

      lecture_configfile(file_path,nb_lignes_data_import)
   return

def on_export_file_select():
   global repository_path_export
   repository_path_export=filedialog.askdirectory()
   if repository_path_export:
      readonly_entry_var_2_tab2.set(repository_path_export)
   return
   

def lecture_configfile(file_path,nb_lignes_data_import):
   
   with open(file_path, "r", encoding="utf-8") as f:
      # file_colonnes = f.readline().strip().split(';')
      file_colonnes = f.read().split('\n')
      new_colums = []
      data_preview_cols = []
      
      file_colonnes = [x.strip() for x in file_colonnes if x != ""]
      
      

      for i in range (len(file_colonnes)):
         if file_colonnes[i] == "":
            file_colonnes.pop(i)
            continue
         
         trim_file_colonnes_i = str(file_colonnes[i]).strip()
         split_trim_file_colonnes_i = trim_file_colonnes_i.split("==")
         if len(split_trim_file_colonnes_i) >=2 :
            
            new_colums.append(
               (str(i) , split_trim_file_colonnes_i[0].strip() +'',split_trim_file_colonnes_i[1].strip())
            )
            data_preview_cols.append(
            { "text":split_trim_file_colonnes_i[1].strip() ,"anchor": "center" }
            )
            file_colonnes[i]=split_trim_file_colonnes_i[0].strip()
         else:
            new_colums.append(
               (str(i) , trim_file_colonnes_i +'')
            )
            data_preview_cols.append(
            { "text":trim_file_colonnes_i ,"anchor": "center" }
            )


         

      headers_table_colonnes = column_headers
      headers_table_colonnes.append(
         {"text": "Renommage", "anchor": "center"}
      )

      data_export_col.build_table_data(coldata=headers_table_colonnes,rowdata=new_colums)
      
      data_export.build_table_data(coldata=data_preview_cols,rowdata=build_datafinals(file_colonnes,dictionnaire,nb_lignes_data_import))
      return
   
def build_datafinals(new_colums_tab, dictionnaire,nb_lignes_data_import):
   if len(dictionnaire) == 0 :
      afficher_message_error("Aucun donnees importer")
      return

   
   # print(dictionnaire)
   global final_data_export

   data_lc=[]
   
   for c in range (nb_lignes_data_import):
      one_line_none=[]
      for k in range (len(new_colums_tab)):
         one_line_none.append(None)
      data_lc.append(one_line_none)
   
   for c in range (len(new_colums_tab)):
      if new_colums_tab[c] in dictionnaire:
         for i in range(nb_lignes_data_import):
            data_lc[i][c]=str(dictionnaire.get(new_colums_tab[c])[i]).strip()
      else:
         for i in range(nb_lignes_data_import):
            data_lc[i][c]=None

   final_data_export=data_lc
   final_data_export.insert(0,new_colums_tab)

   return data_lc
   

def lecture_file(file_path):
   global nb_lignes_data_import
   
   with open(file_path, "r", encoding="utf-8") as f:
      first_line = f.readline().strip()

      sep = separator_options[combobox_var.get()]
      
      columns = first_line.split(sep)      
      # print(columns)
      new_colums = []
      new_colums_name = []
      data_preview_cols = []

      for i in range (len(columns)):
         if columns[i] in new_colums_name:
            position = i+1
            afficher_message_error("la colonne '"+columns[i]+"' est doublons, en position "+str(position))
            return
         
         trim_file_colonnes_i = str(columns[i]).strip()
         new_colums.append((str(i) , trim_file_colonnes_i+'',))
         new_colums_name.append(trim_file_colonnes_i)
         data_preview_cols.append(
            { "text": trim_file_colonnes_i ,"anchor": "center" }
         )
         
      # lit lignes et enleve ligne vide
      lignes = [ligne for ligne in f.read().split('\n') if ligne.strip() != '']      
                  
      nb_lignes_data_import = len(lignes)
      row_data_preview = []
      
      
      for ligne in lignes:
         # print(ligne.split(sep)) 
         
         # mi ingnorer columns tsisy entete
         row_data_preview.append(
            ligne.split(sep)[0:len(columns)-1]
         )
         

      data_table.build_table_data(coldata=column_headers,rowdata=new_colums)
      
      data_preview.build_table_data(coldata=data_preview_cols,rowdata=row_data_preview)
                  
      for i in range(len(columns)):
         dict_one_ligne =[]
         for j in range(len(lignes)):
            dict_one_ligne.append(str(lignes[j].split(sep)[i]).strip())
         
         dictionnaire[str(columns[i]).strip()] = dict_one_ligne
      
      # print('dictionnaire')
      # print(dictionnaire)
   
      return
      
def on_combobox_change(event):
   selected_value = combobox_var.get()
   print(f"Option sélectionnée : {selected_value}")
    
def on_combobox_export_change(event):
   selected_value = combobox_var_2.get()
   print(f"Option sélectionnée : {selected_value}")

    
def exporter_final():
   global final_data_export
   global readonly_entry_var_2_tab2
   global nommage

   name_file_export = nommage.get().strip()

   if readonly_entry_var_2_tab2.get() == "":
      afficher_message_error("veillez selectionner un repertoire a ou placer les donnees exporter")
      return
   
   if name_file_export == "":
      afficher_message_error("veillez remplir le nom du fichier a exporter")
      return
      
   try: 
      final_data_export
   except NameError:
      afficher_message_error("les donnees a exporter ne sont pas valides")
      return
   
   fichier_export=readonly_entry_var_2_tab2.get()+"/"+name_file_export+format_options[combobox_var_2.get()]
   
   with open(fichier_export, "w", encoding="utf-8") as f:
      for ligne in final_data_export:
         for elemt in ligne:
            if elemt :
               f.write(elemt + ";")
            else:
               f.write(";")
         f.write("\n")
   afficher_message_success(fichier_export)
   return
        
    
def main():
   global combobox_var
   global combobox_var_2
   
   nb_lignes_data_import=0
   final_data_export=0
   
   
   container = tb.Frame(tab1)
   container.pack(fill=BOTH, expand=True, padx=10, pady=10)
   container_tab2 = tb.Frame(tab2)
   container_tab2.pack_propagate(False)
   container_tab2.pack(padx=10, pady=10)
   

   # Label + Combobox
   tb.Label(container, text="Choisir une option :").grid(row=0, column=1, sticky="w", padx=5, pady=(5, 0))

   # Liste des clés pour l'affichage
   display_options = list(separator_options.keys())
   
   combobox_var = tb.StringVar(value=display_options[1])
   combobox = tb.Combobox(container, textvariable=combobox_var, values=display_options, state="readonly",)
   combobox.grid(row=1, column=0, padx=5, pady=5)
   combobox.bind("<<ComboboxSelected>>", on_combobox_change)


   # Label + Entry (readonly)
   tb.Label(container, text="Choisir fichier à importer :").grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))
   global readonly_entry_var
   readonly_entry_var = tb.StringVar()
   readonly_entry = tb.Entry(container, textvariable=readonly_entry_var, state='readonly', width=40)
   readonly_entry.grid(row=1, column=1, padx=5, pady=5)
   
   # Bouton pour sélectionner un fichier
   select_file_btn = tb.Button(container, text="Sélectionner un fichier", command=on_file_select)
   select_file_btn.grid(row=2, column=1, padx=5, pady=10)

   # Exportation : 
   tb.Label(container_tab2, text="Choisir fichier ordre colonnes à appliquer :").grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))
   global readonly_entry_var_tab2
   readonly_entry_var_tab2 = tb.StringVar()
   readonly_entry_tab2 = tb.Entry(container_tab2, textvariable=readonly_entry_var_tab2, state='readonly', width=40)
   readonly_entry_tab2.grid(row=1, column=0, padx=5, pady=5)
   select_file_btn_tab2 = tb.Button(container_tab2, text="Sélectionner un fichier", command=on_config_file_select)
   select_file_btn_tab2.grid(row=2, column=0, padx=5, pady=10)


   global data_table
   global data_preview
   global data_export_col
   global data_export
   
   data_table = Tableview(
        master=container,
        height=6,
        paginated=True,
        searchable=True,
        bootstyle=SUCCESS,
    )

   data_table.grid(row=3,column=0,padx=10)
   
   data_preview= Tableview(
        master=container,
        height=6,
        paginated=True,
        searchable=True,
        bootstyle=SUCCESS,
    )

   data_preview.grid(row=3,column=1)
   
   tb.Label(container_tab2, text="Ordre colonnes à appliquer :").grid(row=3, column=0, sticky="w", padx=5, pady=(5, 0))
   data_export_col= Tableview(
      master=container_tab2,
      paginated=True,
      searchable=True,
      bootstyle=SUCCESS,
   )
   data_export_col.grid(row=4,column=0,padx=5)
   
   tb.Label(container_tab2, text="Donnees exporter :").grid(row=3, column=1, sticky="w", padx=5, pady=(5, 0))
   data_export= Tableview(
      master=container_tab2,
      paginated=True,
      searchable=True,
      bootstyle=SUCCESS,
   )
   data_export.grid(row=4,column=1,padx=5)
   
   
   tb.Label(container_tab2, text="Choisir emplacement exportation :").grid(row=5, column=0, sticky="w", padx=5, pady=(5, 0))
   global readonly_entry_var_2_tab2
   readonly_entry_var_2_tab2 = tb.StringVar()
   readonly_entry_tab2 = tb.Entry(container_tab2, textvariable=readonly_entry_var_2_tab2, state='readonly', width=40)
   readonly_entry_tab2.grid(row=6, column=0, padx=5, pady=5)
   select_repo_btn_tab2 = tb.Button(container_tab2, text="Sélectionner un fichier", command=on_export_file_select)
   select_repo_btn_tab2.grid(row=7, column=0, padx=5, pady=10)

   tb.Label(container_tab2, text="Choisir nom fichier : ").grid(row=5, column=1, sticky="w", padx=5, pady=(5, 0))
   # Variable pour récupérer le texte
   global nommage
   nommage = tb.StringVar()
   input_texte = tb.Entry(container_tab2, textvariable=nommage, width=40).grid(row=6,column=1)
   
   
   tb.Label(container_tab2, text="Choisir fomat exportation : ").grid(row=7, column=1, sticky="w", padx=5, pady=(5, 0))
   display_options = list(format_options.keys())
   combobox_var_2 = tb.StringVar(value=display_options[1])
   combobox_2 = tb.Combobox(container_tab2, textvariable=combobox_var_2, values=display_options, state="readonly")
   combobox_2.grid(row=8, column=1, padx=5, pady=5)
   combobox_2.bind("<<ComboboxSelected>>", on_combobox_export_change)
   

   tb.Button(container_tab2, text="Exporter" , command=exporter_final).grid(row=9, column=1, padx=5, pady=10)


   # Équilibrer les colonnes
   container.columnconfigure(0, weight=1, uniform="half")  # Première colonne 50%
   container.columnconfigure(1, weight=1, uniform="half")  # Deuxième colonne 50%
   container.columnconfigure(2, weight=1)
   
   container_tab2.columnconfigure(0,weight=1, uniform="half")
   container_tab2.columnconfigure(1,weight=1, uniform="half")
   container_tab2.columnconfigure(2,weight=1, uniform="half")
   
   
   data_table.bind("<Button-3>", lambda e: "break")
   data_preview.bind("<Button-3>", lambda e: "break")
   data_export_col.bind("<Button-3>", lambda e: "break")
   data_export.bind("<Button-3>", lambda e: "break")


   root.mainloop()


if __name__ == "__main__":
   main()
