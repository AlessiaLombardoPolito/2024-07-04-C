import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        anno = self._view.ddyear.value
        forma = self._view.ddshape.value
        if anno == None or forma == None:
            self._view.txt_result1.controls.append(ft.Text("Selezionare un anno e una forma dal menù"))
            self._view.update_page()
            return
        else :
            self._model.buildGraph(anno,forma)

        numNodi, numArchi= self._model.dettagliGrafo()
        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha {numNodi} nodi e {numArchi} archi"))
        ordinati = self._model.get_top_edges()
        for edge in ordinati:
            self._view.txt_result1.controls.append(
                ft.Text(f"{edge[0].id} -> {edge[1].id} | weight = {edge[2]['weight']}"))

        self._view.update_page()

    def handle_path(self, e):
        pass



    def popolaTendina(self):
        anni = self._model.getAnni()
        for anno in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(anno))
        self._view.update_page()


    def popolaTendina2(self,e):
        anno = self._view.ddyear.value
        if anno == None:
            self._view.txt_result1.controls.append(ft.Text("Selezionare un anno dal menù"))
            self._view.update_page()
        else :
            forme = self._model.getShapes(anno)

        for forma in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(forma))
        self._view.update_page()
