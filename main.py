from selenium import webdriver
from time import sleep
from enviarEmail import EmailBot
import os
import pandas as pd

email_inicio_do_processo = EmailBot('douglas.bot.rh.vagas@gmail.com',
                                    '<H3>Robô iniciou o processo</H3>',
                                    'Robô RH-001-Vagas')
email_inicio_do_processo.enviar()

contador = 0
while contador < 5:

    try:

        # Finaliza navegador
        os.system("taskkill /f /im firefox.exe")
        sleep(3)

        # Iniciando a navegação
        browser = webdriver.Firefox(executable_path=r"selenium/geckodriver.exe")
        browser.get("https://cadmus.com.br/vagas-tecnologia/")
        browser.implicitly_wait(60)

        # Auxilia no carregamento da página
        browser.execute_script("window.scrollTo({top: 1000, left: 100, behavior: 'smooth'});")
        sleep(2)

        tabela_de_elementos_das_vagas = browser.find_element_by_id('pfolio')

        # Popula as vagas na lista
        lista_de_vagas = []
        elementos = tabela_de_elementos_das_vagas.find_elements_by_class_name('box')
        for elemento in elementos:

            nome_da_vaga = elemento.find_element_by_tag_name('h3').text
            localidade_da_vaga = elemento.find_element_by_tag_name('p').text

            if len(nome_da_vaga) > 0 and len(localidade_da_vaga) > 0:
                lista_de_vagas.append([nome_da_vaga, localidade_da_vaga])
            else:
                break

        if lista_de_vagas:

            # Insere a descrição das vagas na lista
            for posicao, lista_aux_vagas in enumerate(lista_de_vagas):
                xpath_botao_da_descricao = '/html/body/section[2]/div/div[2]/div/div/div[' + str(
                    posicao + 1) + ']/div/p[2]/a'
                botao_descricao_da_vaga = browser.find_element_by_xpath(xpath_botao_da_descricao)
                browser.execute_script("arguments[0].click();", botao_descricao_da_vaga)
                sleep(4)
                descricao_da_vaga = browser.find_element_by_xpath('/html/body/section/div/div[2]/div[1]/div[1]/p')
                lista_de_vagas[posicao].insert(3, descricao_da_vaga.text)
                sleep(1)
                browser.back()
                sleep(2)

            # Cria a tabela vagas
            df_tabela_das_vagas = pd.DataFrame(lista_de_vagas, columns=['nome', 'local', 'descrição'])

            # Cria o arquivo excel com as vagas
            df_tabela_das_vagas.to_excel(r'files\rh_vagas.xlsx', index=False, header=True)

            browser.quit()

            email_sucesso = EmailBot('douglas.bot.rh.vagas@gmail.com',
                                     '<H2>Processo Finalizado com sucesso!</H2>',
                                     'Robô RH-001-Vagas',
                                     'files', 'rh_vagas.xlsx')
            email_sucesso.enviar()

            break

    except Exception as err:
        print(err)
        email_erro = EmailBot('douglas.bot.rh.vagas@gmail.com',
                              f'<H3>Erro no robô, descrição do erro:  {err} </H3>',
                              'Robô RH-001-Vagas')
        email_erro.enviar()

    contador = contador + 1
else:
    email_limite_tentativas = EmailBot('douglas.bot.rh.vagas@gmail.com',
                                       '<H3>Limite de tentativas foi atingido!</H3>',
                                       'Robô RH-001-Vagas')
    email_limite_tentativas.enviar()

    # Finaliza navegador
    os.system("taskkill /f /im firefox.exe")
