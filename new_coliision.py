from random import choice

class Collision(MazeSolveAlgo):
    """Um rato que navega pelo labirinto usando backtracking. Ele armazena as bifurcações
    e volta para a última caso encontre um caminho sem saída."""

    def _solve(self):
        """Resolve o labirinto por tentativa e erro, com backtracking até encontrar a saída.
        
        Returns:
            list: solução para o labirinto
        """
        caminho = []  # Guarda o caminho percorrido até o momento
        bifurcacoes = {}  # Guarda as bifurcações e direções inexploradas

        # Começa na posição inicial
        atual = self.start
        caminho.append(atual)
        
        while atual != self.end:
            # Encontrar vizinhos não bloqueados
            vizinhos = self._find_unblocked_neighbors(atual)
            
            # Remove a célula de onde o rato veio, se possível
            if len(caminho) > 1:
                ultimo = caminho[-2]
                if ultimo in vizinhos:
                    vizinhos.remove(ultimo)

            # Se estiver em uma bifurcação com várias direções, armazena-a
            if len(vizinhos) > 1:
                bifurcacoes[atual] = vizinhos

            # Se houver vizinhos disponíveis, escolhe um e avança
            if vizinhos:
                proximo = choice(vizinhos)  # Escolhe aleatoriamente entre as opções
                caminho.append(proximo)
                atual = proximo  # Atualiza a posição do rato
            else:
                # Se não houver vizinhos (beco sem saída), faz o backtrack
                while caminho and (atual not in bifurcacoes or not bifurcacoes[atual]):
                    caminho.pop()  # Remove o atual do caminho
                    if caminho:
                        atual = caminho[-1]  # Volta para a última posição com opções

                # Recupera as direções inexploradas na última bifurcação
                if atual in bifurcacoes:
                    proximo = bifurcacoes[atual].pop()  # Escolhe uma direção inexplorada
                    caminho.append(proximo)
                    atual = proximo

        return caminho  # Retorna o caminho até o ponto final
