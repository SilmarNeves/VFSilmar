from carteira.models import Carteira
from movimentacao.models import Movimentacao

def obter_historico_papeis():
    # Papeis da carteira atual
    papeis_atuais = Carteira.objects.values_list('papel', flat=True).distinct()
    
    # Papeis históricos via movimentações
    papeis_historicos = Movimentacao.objects.values_list('papel', flat=True).distinct()
    
    # Combina os dois conjuntos sem duplicatas
    todos_papeis = set(list(papeis_atuais) + list(papeis_historicos))
    return list(todos_papeis)
