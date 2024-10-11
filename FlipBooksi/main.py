import flet as ft
import sqlite3 



# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('FlipbooksiDatabase.db')
cursor = conn.cursor()

# Criar tabela para armazenar palavras e traduções
cursor.execute('''
CREATE TABLE IF NOT EXISTS palavras_respostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    palavra TEXT NOT NULL,
    resposta TEXT NOT NULL
)
''')

# Salvar as mudanças e fechar a conexão
conn.commit()
conn.close()


def main(page: ft.Page):
    page.title = 'FlipBooksi.App'
    page.bgcolor = ft.colors.BLACK
    page.window.max_width = 1000
    page.window.max_height = 700
    page.window.resizable = False
    


    #Parte das Funções

    #Função que preenche e atualiza as lista que serão usadas para exibir as palavras e respostas
    def atualiza_listas():
        conn = sqlite3.connect('FlipbooksiDatabase.db')
        cursor = conn.cursor()
        cursor.execute('SELECT palavra, resposta FROM palavras_respostas')
        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            conn = sqlite3.connect('FlipbooksiDatabase.db')
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO palavras_respostas (palavra, resposta)
            VALUES ("As palavras e frases vão aqui","E aqui as Respostas !")
            ''')
            conn.commit()
            conn.close()

        return resultados
        
        

    #Classe que contém as variaveis que serão usadas pelas funções
    class VariaveisApp:
        def __init__(self):
            self.indice = 0
            self.palavras_respostas = []
            

        def carregar_listas(self):
            self.palavras_respostas = atualiza_listas()
        


    #Função que passa para a próxima palavra
    def proxima_palavra(e, app):
        try:
            if app.indice < len(app.palavras_respostas):
                app.indice += 1
                palavraMostrada.value = app.palavras_respostas[app.indice][0].capitalize()
                respostaMostrada.value = app.palavras_respostas[app.indice][1].capitalize()
                respostaMostrada.visible = False

            elif app == len(app.palavras):
                palavraMostrada.value = 'Você já viu todas as palavras salvas!!'
                respostaMostrada.value = ''

        except IndexError:
            palavraMostrada.value = 'Você já viu todas as palavras salvas!!'
            respostaMostrada.value = 'Parabéns !!'
            respostaMostrada.visible = True
            app.indice = 0
            page.update()


        page.update()

    app = VariaveisApp()
    app.carregar_listas()

    #Função que cadastra as palavras e suas traduções
    def cadastra_palavras(e, input_palavra, input_resposta):
        palavra = input_palavra.value
        resposta = input_resposta.value

        if palavra:
            conn = sqlite3.connect('FlipbooksiDatabase.db')
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO palavras_respostas (palavra, resposta)
            VALUES (?, ?)
            ''', (palavra, resposta))
            conn.commit()
            conn.close()

        input_palavra.value = ''
        input_resposta.value = ''    
        page.update()


    def revela_resposta(e, respostaMostrada):
        respostaMostrada.visible = True
        page.update()



    #Parte do Front End/Interface Gráfica do App usando a biblioteca Flet
    palavraLogo = ft.Text(
        value='FlipBooksi',
        size=195,
        weight=ft.FontWeight.BOLD,
        style=ft.TextStyle(
            foreground=ft.Paint(
                gradient=ft.PaintLinearGradient(
                    begin=ft.Offset(x=0, y=0),
                    end=ft.Offset(x=600, y=0),
                    colors=[ft.colors.CYAN, ft.colors.PURPLE, ft.colors.PINK],
                    color_stops=[0, 0.8, 1],
                )
            )
        )
    )

    input_palavra = ft.TextField(hint_text='Digite aqui uma palavra, frase ou pergunta que deseja estudar', text_size=20, bgcolor=ft.colors.SURFACE_VARIANT, border_radius=ft.border_radius.all(15), multiline=True, max_lines=4)
    input_resposta = ft.TextField(hint_text='Digite aqui a tradução/resposta do que foi escrito acima', text_size=20, bgcolor=ft.colors.SURFACE_VARIANT, border_radius=ft.border_radius.all(15), multiline=True, max_lines=4, )
    palavraMostrada = ft.Text(value= atualiza_listas()[app.indice][0].capitalize(), size=40, color=ft.colors.PINK_ACCENT_100, weight=ft.FontWeight.BOLD)
    respostaMostrada =ft.Text(value= atualiza_listas()[app.indice][1].capitalize(), size=50, color=ft.colors.PINK_ACCENT_100, weight=ft.FontWeight.BOLD, visible= False)


    #View da Página Inicial
    st = ft.Stack(
        controls=[
            ft.Container(
                palavraLogo,
                left=7,
                top=45
            ),
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        text='Começar Estudo',
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        color=ft.colors.PINK_100,
                        on_click=lambda _: page.go("/comecar"),
                        height=40,
                        width=200
                    )
                ],
                left=400,
                top=350
            ),
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        text='Adicionar Palavras',
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        color=ft.colors.PINK_100,
                        on_click=lambda _: page.go("/adicionarpalavras"),
                        height=40,
                        width=200
                    )
                ],
                top=430,
                left=400
            ),
        ],
        expand=True,
    )

    #View da página onde se inicia o estudo
    st2 = ft.Stack(
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        content=palavraMostrada,
                        width=975,
                        height=250,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=ft.border_radius.all(10),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=respostaMostrada,
                        height=375,
                        width=975,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        on_click= lambda e: revela_resposta(e,respostaMostrada),
                        border_radius=ft.border_radius.all(10),
                        alignment=ft.alignment.center
                    ),
                ]
            ),
            ft.Container(
                ft.FloatingActionButton(
                    icon=ft.icons.ARROW_BACK,
                    foreground_color=ft.colors.PINK_100,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    on_click=lambda _: page.go('/'),
                    height=40,
                    width=40,
                ),
                bottom=25,
                left=25
            ),
            ft.Container(
                ft.FloatingActionButton(
                    icon=ft.icons.ARROW_FORWARD,
                    foreground_color=ft.colors.PINK_100,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    on_click= lambda e: proxima_palavra(e,app),
                    height=40,
                    width=40,
                ),
                bottom=25,
                right=25
            )
        ],
        expand=True,
    )

    #View da página de cadastro das palavras que serão estudadas
    st3= ft.Stack(
        controls=[
            ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        ft.Text(value='Aqui você poderá cadastrar palavras, frases ou perguntas que esteja estudando para te ajudar a fixar na memória os conteúdos estudados.', size=20, color=ft.colors.PINK_100, weight=ft.FontWeight.BOLD, text_align=ft.alignment.center),
                        height=150,
                        padding=ft.padding.all(15),
                        alignment=ft.alignment.center

                    ),
                    ft.Container(
                        input_palavra,
                        height=250,
                        padding=ft.padding.only(top=50)
                    ),
                    ft.Container(
                        input_resposta,
                        height=300
                    ),
                ]
            ),
            ft.Container(
                     ft.FloatingActionButton(
                         text='Salvar',
                         height=40,
                         width=80,
                         bgcolor=ft.colors.SURFACE_VARIANT,
                         foreground_color=ft.colors.PINK_100,
                         on_click= lambda e: cadastra_palavras(e,input_palavra, input_resposta)
                     ),
                bottom=25,
                left=440
            ),
            ft.Container(
                ft.FloatingActionButton(
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    foreground_color=ft.colors.PINK_100,
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: page.go('/'),
                    height=40,
                    width=40
                ),
                bottom=25,
                left=25
            )
        ],
        expand=True,
    )


    def mudaPagina(route):
        troute = ft.TemplateRoute(page.route)

        if troute.match("/"):
            page.clean()
            page.add(st)
            app.indice = 0
            app.carregar_listas()



        elif troute.match("/comecar"):
            page.clean()
            page.add(st2)


        elif troute.match("/adicionarpalavras"):
            page.clean()
            page.add(st3)



    page.add(st)
    page.on_route_change = mudaPagina
    page.update()


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')