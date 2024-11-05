from random import choice

class Collision(MazeSolveAlgo):
    """Um rato que navega pelo labirinto usando backtracking. Ele armazena as bifurcações
    e volta para a última caso encontre um caminho sem saída."""

    def _solve(self):
        """Resolve o labirinto por tentativa e erro, com backtracking até encontrar a saída.
        
        Returns:
            list: solução para o labirinto
        """
        caminho = []
        bifurcacoes = {}

        atual = self.start
        caminho.append(atual)
        
        while atual != self.end:
            vizinhos = self._find_unblocked_neighbors(atual)
            
            if len(caminho) > 1:
                ultimo = caminho[-2]
                if ultimo in vizinhos:
                    vizinhos.remove(ultimo)

            # guarda bifurcação
            if len(vizinhos) > 1:
                bifurcacoes[atual] = vizinhos

            if vizinhos:
                proximo = choice(vizinhos)
                caminho.append(proximo)
                atual = proximo
            else:
                # Se beco sem saída, volta
                while caminho and (atual not in bifurcacoes or not bifurcacoes[atual]):
                    caminho.pop()
                    if caminho:
                        atual = caminho[-1]

                if atual in bifurcacoes:
                    proximo = bifurcacoes[atual].pop()
                    caminho.append(proximo)
                    atual = proximo

        return caminho
