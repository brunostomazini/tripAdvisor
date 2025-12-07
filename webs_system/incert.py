# Este script foi projetado para ser executado DENTRO do Django Shell:
# python manage.py shell < scripts/create_categories_script.py

import os
import django
from django.db import models # Necessário para TextChoices no mock
from django.core.validators import MinLengthValidator # Necessário para o mock
from django.apps import apps # Necessário para verificar se o app existe

# ----------------------------------------------------------------------
# Configuração inicial (garante que o ambiente Django está carregado)
# NOTE: Pode ser necessário ajustar se o script não for executado via pipe (<)
# if not django.setup():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')
#     django.setup()
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# MOCK DE DEPENDÊNCIAS (REFLETINDO O NOVO ENUM CLASSFICACAO)
# ----------------------------------------------------------------------

# Definição do seu Enum Classificacao (usado no modelo Categoria)
class Classificacao(models.TextChoices):
    """Definição real (mockada) do Enum Classificacao."""
    GENERAL = "Geral", "Para todos os públicos"
    FAMILIES = "Famílias", "Adequado para famílias com crianças"
    COUPLES = "Casais", "Experiências românticas ou para dois"
    SOLO = "Solo", "Aventura ou tranquilidade para viajantes individuais"
    BUSINESS = "Negócios", "Focado em eventos corporativos ou trabalho"
    ADULT = "Adulto", "Conteúdo restrito ou maior de idade"

# Assumindo a definição do BaseModel
class BaseModel:
    """Mock para a classe BaseModel."""
    # O método save deve estar em Categoria no caso de mock
    pass 

# ----------------------------------------------------------------------
# IMPORTAÇÃO DO MODELO (AJUSTE ESTA LINHA!)
# ----------------------------------------------------------------------

# Definição de uma flag para rastrear se usamos o mock
use_mock = False

try:
    # Tenta importar o modelo real (AJUSTE O CAMINHO!)
    # Exemplo CORRETO: from tripAdvisor.models import Categoria 
    from seu_app.models import Categoria 
    
except (ImportError, LookupError, RuntimeError):
    # Se falhar a importação (ModuleNotFoundError) ou se o modelo não estiver pronto (RuntimeError/LookupError)
    use_mock = True
    print("AVISO: Usando a definição MOCK da classe Categoria.")
    
    # ----------------------------------------------------------------------
    # DEFINIÇÃO DO MOCK DA CATEGORIA (CORRIGIDO)
    # ----------------------------------------------------------------------
    # O mock é definido aqui dentro do bloco except, garantindo a sua definição
    class Categoria(models.Model):
        nome = models.CharField(max_length=50, validators=[MinLengthValidator(5)])
        # Importante: Classificacao.choices é o atributo usado pelo campo models.CharField
        classificacao = models.CharField(max_length=20, choices=Classificacao.choices) 
        descricao = models.TextField()

        # O BaseModel provavelmente define métodos como save(), mas para o shell
        # e para evitar o erro de 'RuntimeError: Model class builtins.Categoria doesn't declare an explicit app_label'
        # garantimos que ele se comporte como um modelo Django.
        
        def __str__(self):
            return f"Categoria:{self.nome} Classificação:{self.classificacao}"
        
        # ESSENCIAL para modelos mockados no shell se comportarem como modelos reais
        class Meta:
            app_label = 'seu_app_mock' # Usamos um nome diferente para evitar conflito com apps reais
            # O Django exige que modelos tenham uma conexão com um app.
            
    # Adicionando o método objects, necessário para Categoria.objects.filter/bulk_create
    # Se você está no shell, isso pode ser desnecessário, mas o mock completo exige.
    try:
        if Categoria.objects is None:
            from django.db.models import Manager
            Categoria.objects = Manager()
    except AttributeError:
        from django.db.models import Manager
        Categoria.objects = Manager()
        
    # NOTA: O mock ainda pode falhar se o ambiente Django não estiver 
    # totalmente carregado (o que é improvável ao usar `manage.py shell < script.py`).


# ----------------------------------------------------------------------
# DADOS PARA CRIAÇÃO EM MASSA (AJUSTADOS PARA O NOVO ENUM)
# ----------------------------------------------------------------------

# Mapeamento para usar as KEYs do enum (ex: 'Geral')
CLASSIFICACAO_MAP = {
    key: value for key, value in Classificacao.choices
}

CATEGORIAS_DADOS = [
    {
        'nome': 'Museus e História',
        # Usamos o valor real que será armazenado no DB, conforme definido pelo TextChoices
        'classificacao': Classificacao.GENERAL, 
        'descricao': 'Locais educativos e de interesse histórico, adequados para todos os públicos.',
    },
    {
        'nome': 'Parques Temáticos',
        'classificacao': Classificacao.FAMILIES,
        'descricao': 'Atrações com foco em entretenimento para todas as idades, especialmente crianças.',
    },
    {
        'nome': 'Pousadas Românticas',
        'classificacao': Classificacao.COUPLES,
        'descricao': 'Acomodações e experiências projetadas para casais e luas de mel.',
    },
    {
        'nome': 'Hostels e Mochilão',
        'classificacao': Classificacao.SOLO,
        'descricao': 'Opções de hospedagem e atividades para viajantes individuais e orçamentos limitados.',
    },
    {
        'nome': 'Salas de Conferência',
        'classificacao': Classificacao.BUSINESS,
        'descricao': 'Locais e serviços focados em eventos corporativos, reuniões e conferências.',
    },
    {
        'nome': 'Bares e Clubes',
        'classificacao': Classificacao.ADULT,
        'descricao': 'Estabelecimentos noturnos com restrição de idade (maiores de 18 anos).',
    },
    {
        'nome': 'Restaurantes Típicos',
        'classificacao': Classificacao.GENERAL,
        'descricao': 'Gastronomia local e culinária regional para todos os visitantes.',
    },
]

# ----------------------------------------------------------------------
# LÓGICA DE CRIAÇÃO
# ----------------------------------------------------------------------

def criar_categorias():
    """Cria as instâncias do modelo Categoria usando bulk_create."""
    print("--- Iniciando a criação de categorias em massa ---")
    
    # Esta verificação só é necessária se o mock estiver ativo e o ambiente não estiver pronto
    if use_mock:
        print("ALERTA: O modo de mock está ativo. A criação real no DB pode não ocorrer.")
    
    # Cria uma lista de objetos Categoria
    novas_categorias = [
        Categoria(**dados) for dados in CATEGORIAS_DADOS
    ]
    
    try:
        # Obtém apenas os nomes das categorias que já existem no banco
        # Acessar .objects falhará se a classe não for um modelo Django carregado
        nomes_existentes = set(Categoria.objects.filter(
            nome__in=[c['nome'] for c in CATEGORIAS_DADOS]
        ).values_list('nome', flat=True))
    except Exception as e:
        print(f"AVISO: Falha ao consultar o banco de dados (provavelmente por causa do mock/ambiente): {e}. Prosseguindo com a criação completa.")
        nomes_existentes = set()
    
    # Filtra os objetos para criar apenas aqueles que não existem
    categorias_a_criar = [
        cat for cat in novas_categorias if cat.nome not in nomes_existentes
    ]

    if not categorias_a_criar:
        print("Nenhuma nova categoria para criar. Todas já existem.")
        return

    try:
        # Usa bulk_create para eficiência
        Categoria.objects.bulk_create(categorias_a_criar)
        
        nomes_criados = [cat.nome for cat in categorias_a_criar]
        print(f"\n✅ {len(nomes_criados)} Categorias criadas com sucesso:")
        for nome in nomes_criados:
            print(f"- {nome}")
            
    except Exception as e:
        # Usamos uma string genérica para evitar o erro de codificação UnicodeEncodeError
        print(f"\n[ERRO] Falha na criação em massa. Detalhes: {e}")
        print("Verifique se as dependências (BaseModel, Classificacao) e as validações (MinLengthValidator) estão corretas.")

# Executa a função
criar_categorias()

# Limpando variáveis globais criadas pelo script
del CATEGORIAS_DADOS, CLASSIFICACAO_MAP, novas_categorias, categorias_a_criar, criar_categorias

# A limpeza do mock agora é opcional, pois o script está terminando
if use_mock:
    del Categoria, Classificacao, BaseModel, apps, use_mock
else:
    del apps

print("\n--- Script de população finalizado ---")