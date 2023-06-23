from modulos import *


#Criando a classe de menu em forma de árvore
class TreeMenu(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.tree = Treeview(self, columns=('Valor',))
        self.tree.heading('#0',text="Variável")
        self.tree.heading('Valor', text='Valor')
        self.tree.column('Valor',stretch=False,minwidth=50, width=100)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.pack(fill=BOTH, expand=True)
        self.nodes={}
    
    #Adicionando um nó
    def add_node(self, parent,id, name, value):
        if not self.tree:
            return
        node_id = self.tree.insert(parent,"end", text=name,values=(value,))
        self.nodes[node_id] = value
        return node_id
    
    def att_node_id(self,id, value):
        self.tree.set(id,'Valor',value)
        self.nodes[id] = value
        self.tree.item(id,tags=())
    
    #Evento de duplo clique:
    def on_double_click(self, event):
        editable_items = ['Câmera USB Path','Imagem Path','Vídeo Path','Modo de Uso','Cor','Cor Principal T1', 'Cor Principal T2','T1_robo 1','T1_robo 2','T1_robo 3','T2_robo 1','T2_robo 2','T2_robo 3','Debug','Borda da janela','offSet da Erosão','Debug do Algorítmo','Binarização Threshold','Dim. Matriz TOPHAT']
        item = self.tree.focus()
        if item:
            if self.tree.item(item, 'text') in editable_items:
                self.tree.item(item, tags=('edit',))
                entry = simpledialog.askstring("Editar variável", "Adicione o novo valor da variável")
                if entry is not None:
                    self.tree.set(item,'Valor',entry)
                    self.nodes[item] = entry
                self.tree.item(item,tags=())
            
    #Adquirindo os dados com o get_tree_data, é uma função recursiva
    def get_tree_data(self, node_id=''):
        if node_id == '':
            children = self.tree.get_children()
        else:
            children = self.tree.get_children(node_id)

        data = {}
        for child in children:
            item_id = child
            name = self.tree.item(child, 'text')
            value = self.tree.item(child, 'values')
            data[item_id] = {"name": name, "value": value, "children": self.get_tree_data(child)}
        
        return data
    
    #Função para salvar o arquivo em json
    def save_to_json(self, filename):
        data = self.get_tree_data()
        with open(filename + '.json', "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

    # Método para carregar a TreeView a partir de um arquivo JSON
    def load_from_json(self, node):
        name = node.get('name')
        value = node.get('value')
        children = node.get('children')

        item_id = self.tree.insert('', 'end', text=name, values=value)
        if children:
            for child in children.values():
                self.load_from_json_recursive(item_id, child)

    def load_from_json_recursive(self, parent_id, node):
        name = node.get('name')
        value = node.get('value')
        children = node.get('children')

        item_id = self.tree.insert(parent_id, 'end', text=name, values=value)

        if children:
            for child in children.values():
                self.load_from_json_recursive(item_id, child)

    def load_from_json_file(self, filename):
        with open(filename, 'r',encoding='utf-8') as file:
            data = json.load(file)

        root_node = data.get('I001')
        self.load_from_json(root_node)

    def clear_tree(self):
        self.tree.destroy()
        self.tree = Treeview(self, columns=('Valor',))
        self.tree.heading('#0',text="Variável")
        self.tree.heading('Valor', text='Valor')
        self.tree.column('Valor',stretch=False,minwidth=50, width=100)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.pack(fill=BOTH, expand=True)
        self.nodes={}


if __name__ == "__main__":
    print("Módulo sendo executado como funcao principal")

