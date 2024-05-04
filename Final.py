# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 20:55:32 2024

@author: rbooa
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from time import sleep
import pandas as pd
from unidecode import unidecode

# 1 Iniciamos la sesión y se accede a la página web.
# 1.1 Driver.
driver = webdriver.Firefox()

# 1.2 Acceso a página web.
url = 'https://www.pisos.com'
driver.get(url)

# 2 Establecemos la búsqueda que queremos realizar, en nuestro caso: Comprar, Casas y Pisos, Madrid Capital.
# 2.1 Primero de todo, se aceptan las cookies.
element_msg_cookies = (By.XPATH, "//span[contains(text(),'Aceptar y cerrar')]/parent::button")
msg_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_cookies))
msg_cookies.send_keys(Keys.ENTER)

# Se cierra el banner de incio de sesión de Google y se vuelve a la pagina original. 
try: 
    # Se localiza el banner de inicio de sesion de google.
    element_msg_iframe = (By.XPATH, "//iframe[contains(@src, 'accounts.google.com')]")
    msg_iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(element_msg_iframe))
    # Se clica la x de cerrar el banner.
    element_login_google = (By.XPATH, "//div[@aria-label = 'Cerrar']")
    login_google = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_login_google))
    login_google.click()
    # Se vuelve al contenido original.
    driver.switch_to.default_content()
except: 
    print("No hay banner de inicio de sesión de Google")

# Se espera a que desaparezca el banner de inicio de sesión para que no obstaculice al resto de elementos. 
try:
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(element_msg_iframe))
except TimeoutException:
    print("El banner de inicio de sesión de Google no desapareció")

# 2.2 Selección de la acción (Comprar): No es necesario porque el valor predeterminado es Comprar.

# 2.3 Selección de los edificios (Casas y pisos): No es necesario porque el valor predeterminado es Casas y pisos.  

# 2.4 Selección de la región (Madrid Capital).
element_msg_region = (By.XPATH, "//input[@placeholder = 'Busca por municipio, barrio, distrito...']")  
msg_region = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_region))
msg_region.send_keys('Madrid Capital')

# 2.5 Se busca la selección realizada.
element_msg_pulsar_seleccion = (By.XPATH, "//div[@class = 'suggest__item']")  
msg_pulsar_seleccion = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_pulsar_seleccion))
msg_pulsar_seleccion.click()

# 2.6 Se selecciona Ver resultados.
element_msg_ver = (By.XPATH, "//a[contains(text(),'Ver')]")
msg_ver = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(element_msg_ver))
msg_ver.click()

# 3 Una vez en la página necesitamos establecer una serie de filtros sobre el tipo de vivienda.
# 3.1 Se selecciona casas y chalets.
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
element_msg_casas_chalets = (By.XPATH, "//input[@id = 'ckF002S022']/parent::div")
msg_casas_chalets = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_casas_chalets))
msg_casas_chalets.click()

# 3.2 Se selecciona pisos y apartamentos.
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
element_msg_pisos_apartamentos = (By.XPATH, "//input[@id = 'ckF002S021']/parent::div")
msg_pisos_apartamentos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_pisos_apartamentos))
msg_pisos_apartamentos.click()

# 3.3 Se selecciona aticos.
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
element_msg_aticos = (By.XPATH, "//input[@id = 'ckF002S024T015']/parent::div")
msg_aticos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_aticos))
msg_aticos.click()

# 3.4 Se selecciona duplex.
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
element_msg_duplex = (By.XPATH, "//input[@id = 'ckF002S024T010']/parent::div")
msg_duplex = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_duplex))
msg_duplex.click()

# 3.5 Se selecciona "Ver resultados" para aplicar los filtros.
element_msg_resultados = (By.XPATH, "//button[contains(text(),'Ver')]")
msg_resultados = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_resultados))
msg_resultados.click()

# 3.6 Se clica la x del banner que nos pide el email.
try: 
    element_msg_email = (By.XPATH, "//button[@class = 'modal__close']")
    msg_email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_email))
    msg_email.click()
except: 
    print("No hay banner de email")
    
# 3.7 Se accede a la lista de ordenacion.
element_msg_lista_ordenacion = (By.XPATH, "//select[@id = 'sortResults']")
msg_lista_ordenacion = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_lista_ordenacion))
msg_lista_ordenacion.click()

# 3.8 Se selecciona 'Mas recientes'.
element_msg_mas_recientes = (By.XPATH, "//option[contains(text(),'Más recientes')]")
msg_mas_recientes = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_mas_recientes))
msg_mas_recientes.click()

# 3.9 Se localizan todas las viviendas de la pagina. 
element_msg_info = (By.XPATH, "//div[contains(@class,'has-desc')]")
msg_info_inicial = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(element_msg_info))

# 4 Funciones utilizadas.
# 4.1 Funcion para tratar con las excepciones para las características binarias.
def excepciones_binarias(xpath, elemento):
    elem = 'no'
    try:
        WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, xpath))).text
        elem = 'si'
    except TimeoutException:
        a = 0
    return(elem)
  
# 4.2 Funcion para tratar con las excepciones para el resto características.
def excepciones(xpath, elemento):
    elem = 'null'
    try:
        elem = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, xpath))).text
    except TimeoutException:
        a = 0
    return(elem)

# 4.3 Funcion para guardar las caracteristicas de la vivienda.
caracteristicas = []
def guardar_caracteristicas(): 
    # Se verifica si hay direccion.
    element_msg_direccion = "//h1"
    direccion = excepciones(element_msg_direccion,'direccion')

    # Se verifica si hay barrio.
    element_msg_barrio = "//p"
    barrio = excepciones(element_msg_barrio,'barrio')

    # Se verifica si hay precio.
    element_msg_precio = "//div[@class = 'price__value jsPriceValue']"
    precio = excepciones(element_msg_precio,'precio')
    precio = precio.replace('€','euros')

    # Se verifica si hay piscina.
    element_msg_piscina = "//span[@class = 'features__label' and contains(text(),'Piscina')]"
    piscina = excepciones_binarias(element_msg_piscina, "piscina")

    # Se verifica si hay terraza. 
    element_msg_terraza = "//span[@class = 'features__label' and (contains(text(),'Terraza') or contains(text(),'Balcón'))]"
    terraza = excepciones_binarias(element_msg_terraza, "terraza")

    # Se verifica si hay jardín.
    element_msg_jardin = "//span[@class = 'features__label' and contains(text(),'Jardín')]"
    jardin = excepciones_binarias(element_msg_jardin, "jardin")

    # Se verifica si hay garaje.
    element_msg_garaje = "//span[@class = 'features__label' and contains(text(),'Garaje')]"
    garaje = excepciones_binarias(element_msg_garaje, "garaje")

    # Se verifica si hay trastero.
    element_msg_trastero = "//span[@class = 'features__label' and contains(text(),'Trastero')]"
    trastero = excepciones_binarias(element_msg_trastero, "trastero")

    # Se verifica si hay calefacción.
    element_msg_calefacción = "//span[@class = 'features__label' and contains(text(),'Calefacción')]/parent::div"
    calefaccion = excepciones_binarias(element_msg_calefacción, "calefacción")

    # Se verifica si hay aire acondicionado.
    element_msg_aire_acondicionado = "//span[@class = 'features__label' and contains(text(),'Aire')]"
    aire_acondicionado = excepciones_binarias(element_msg_aire_acondicionado, "aire acondicionado")

    # Se verifica si hay ascensor.
    element_msg_ascensor = "//span[@class = 'features__label' and contains(text(),'Ascensor')]"
    ascensor = excepciones_binarias(element_msg_ascensor, "ascensor")

    # Se verifica si hay superficie construida.
    element_msg_superficie_construida = "//span[contains(text(),'Superficie construida')]/following-sibling::span[@class = 'features__value']"
    superficie_construida = excepciones(element_msg_superficie_construida,'superficie construida')
    superficie_construida = superficie_construida.replace('m²','metros cuadrados')

    # Se verifica si hay habitaciones.
    element_msg_habitaciones = "//span[contains(text(),'Habitaciones')]/following-sibling::span[@class = 'features__value']"
    habitaciones = excepciones(element_msg_habitaciones ,'habitaciones ')

    # Se verifica si hay baños.
    element_msg_baños = "//span[contains(text(),'Baños')]/following-sibling::span[@class = 'features__value']"
    baños = excepciones(element_msg_baños,'baños')

    # Se verifica si hay planta.
    element_msg_planta = "//span[contains(text(),'Planta')]/following-sibling::span[contains(@class,'features__value')]"
    planta = excepciones(element_msg_planta,'planta')
    
    # Se verfica si hay inmobiliaria
    element_msg_inmobiliaria = "//p[contains(@class, 'owner-info')]"
    inmobiliaria = excepciones(element_msg_inmobiliaria, "inmobiliaria")
    
    # Se guardan las caracteristicas en una lista.
    lista = [direccion, barrio, precio, piscina, terraza, jardin, garaje, trastero, calefaccion,
             aire_acondicionado, ascensor, superficie_construida, habitaciones, baños, planta, inmobiliaria]
    lista = list(map(unidecode,lista))
    caracteristicas.append(lista)
    return(caracteristicas)

# 4.4 Funcion para pasar de vivienda en vivienda recogiendo las caracteristicas mas importantes.
def bucle_casas(x,y):
    # Inicializamos un bucle que nos permita pasar de pagina en pagina hasta que no se encuentren mas. 
    iteraciones = 1
    siguiente = "verdadero"
    while siguiente == "verdadero":
        # Creamos un bucle para acceder a cada vivienda.
        for i in range(len(x)):
            # Encontramos todas las viviendas cada vez que actualizamos la pagina para evitar StaleElementReferenceException.
            msg_info = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(y))    
            # Verificamos que no se produzca ningun error de List out of range. 
            try: 
                if i < len(x):
                   hipoteca = "si"
                   desactivacion = "si"
                   # Accedemos a cada vivienda.
                   msg_info[i].click()
                   # Se verifica si se abre el cálculo de la hipoteca en vez de la vivienda.
                   try: 
                       element_msg_hipoteca = (By.XPATH, "//button[@class = 'modal__close']")
                       msg_hipoteca = WebDriverWait(driver, 1).until(EC.element_to_be_clickable(element_msg_hipoteca))
                       msg_hipoteca.click()
                   except TimeoutException:
                       hipoteca = "no"
                   # Se verifica si la vivienda se ha desactivado y no podemos acceder a ella.
                   try:
                       element_msg_desactivacion = (By.XPATH, "//p[contains(text(),'desactivado')]")
                       msg_desactivacion = WebDriverWait(driver, 1).until(EC.presence_of_element_located(element_msg_desactivacion))
                       driver.back()
                       sleep(1)
                   except TimeoutException:
                       desactivacion = "no"
                   # Si no se abre el cálculo de la hipoteca y la vivienda está activa, se guarda la info de la vivienda.
                   if hipoteca == "no" and desactivacion == "no": 
                       # Llamamos a la funcion que guarda las caracteristicas de la vivienda. 
                       lista_caracteristicas = guardar_caracteristicas()
                       sleep(1)       
                       # Volvemos al listado de viviendas.
                       driver.back()
                       sleep(1)
                   # Vemos a que vivienda estamos accediendo. 
                   print(i)
            # Si se produce un error de List out of range, salimos del bucle porque el robot esta considerando 
            # que hay casas de mas, entonces trata de acceder a la casa k cuando el rango es k - 1. 
            except IndexError: 
                print("Índice fuera de rango, pasamos a la siguiente página.")
                break
        # Mostramos un mensaje de guardar caracteristicas. 
        print(f"Guardando caracteristicas en el archivo {iteraciones}.")
        # Guardamos las caracteristicas en un dataframe.
        datos = pd.DataFrame(lista_caracteristicas)
        columnas = ('direccion', 'barrio', 'precio', 'piscina', 'terraza', 'jardin', 'garaje', 'trastero', 'calefaccion',
                    'aire_acondicionado', 'ascensor', 'superficie_construida', 'habitaciones', 'baños', 'planta', 'inmobiliaria')
        datos.columns = columnas
        # Guardamos los datos en un archivo csv.
        nombre_archivo = f"datos_scraping_{iteraciones}.csv"
        datos.to_csv(nombre_archivo, index = False, encoding = "utf-8-sig", sep = ";")
        # Pasamos a la siguiente página.
        try: 
            element_msg_siguiente_pagina = (By.XPATH, "//div[contains(@class,'pagination__next')]")
            msg_siguiente_pagina = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_siguiente_pagina))
            msg_siguiente_pagina.click()
            iteraciones += 1
        except: 
            print("No hay mas paginas")
            siguiente = "falso"
        # Se busca el banner del email.
        try: 
             element_msg_email = (By.XPATH, "//button[@class = 'modal__close']")
             msg_email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_msg_email))
             msg_email.click()
        except: 
             print("No hay banner de email")
    # Se devuelve el dataframe con las caracteristicas de las viviendas.
    return(datos)

# Llamada a la función.
caracteristicas_viviendas = bucle_casas(msg_info_inicial, element_msg_info)

# Cerramos la sesión.
driver.quit()

