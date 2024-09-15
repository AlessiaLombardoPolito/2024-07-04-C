from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._allYears = DAO.get_all_Years()
        self._grafo = nx.DiGraph()
        self._idMap = {}



    def getAnni(self):
        return self._allYears

    def getShapes(self, anno):
        forme = DAO.get_all_shapes(anno)
        return forme

    def buildGraph(self, anno, forma):
        self._grafo.clear()
        nodi = DAO.getNodes(anno,forma)
        for nodo in nodi:
            self._grafo.add_node(nodo)

        for a in list(self._grafo.nodes):
            self._idMap[a.id] = a

        for i in range(0, len(nodi) - 1):
            for j in range(i + 1, len(nodi)):
                if nodi[i].state == nodi[j].state and nodi[i].longitude < nodi[j].longitude:
                    weight = nodi[j].longitude - nodi[i].longitude
                    self._grafo.add_edge(nodi[i], nodi[j], weight=weight)
                elif nodi[i].state == nodi[j].state and nodi[i].longitude > nodi[
                    j].longitude:
                    weight = nodi[i].longitude - nodi[j].longitude
                    self._grafo.add_edge(nodi[j], nodi[i], weight=weight)

    """Due cicli annidati:

Il primo ciclo for i in range(0, len(nodi) - 1) itera su tutti i nodi della lista nodi, tranne l'ultimo.
Il secondo ciclo annidato for j in range(i + 1, len(nodi)) inizia dall'indice successivo rispetto al ciclo esterno 
(i.e., i + 1) e scorre fino alla fine della lista. Questo serve per confrontare ogni nodo con i successivi, evitando 
confronti ridondanti e autoconfronti.
Condizioni sui nodi:

Viene controllato se i nodi nodi[i] e nodi[j] appartengono allo stesso stato attraverso nodi[i].state == nodi[j].state. 
Se appartengono allo stesso stato, si procede con ulteriori controlli.
Calcolo del peso dell'arco:

Se la longitudine del nodo nodi[i] è minore di quella del nodo nodi[j], si calcola il peso dell'arco come la differenza 
tra le longitudini: weight = nodi[j].longitude - nodi[i].longitude.
Si aggiunge poi un arco al grafo da nodi[i] a nodi[j] con il peso calcolato tramite il metodo 
self._grafo.add_edge(nodi[i], nodi[j], weight=weight).
Se invece la longitudine di nodi[i] è maggiore di quella di nodi[j], si calcola nuovamente la differenza, ma si aggiunge
l'arco al grafo nell'ordine inverso, ovvero da nodi[j] a nodi[i]."""

    def get_top_edges(self):
            sorted_edges = sorted(self._grafo.edges(data=True), key=lambda edge: edge[2].get('weight'), reverse=True)
            return sorted_edges[0:5]

    def dettagliGrafo(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

