import requests
from bs4 import BeautifulSoup

def obtener_info_good(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        # Realizar una solicitud GET a la página
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

        # Parsear el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Obtener el título (modifica el selector según sea necesario)
        title_element = soup.find("h1", {"data-testid": "bookTitle"})
        title = title_element.get_text(strip=True).capitalize() if title_element else None

        # Obtener el autor (modifica el selector según sea necesario)
        autor_element = soup.find_all("span", class_="ContributorLink__name")
        autor = autor_element[0].get_text(strip=True) if autor_element else None

        # Obtener la URL de la imagen (modifica el selector según sea necesario)
        imagen_element = soup.find("img", class_="ResponsiveImage")
        imagen = imagen_element["src"] if imagen_element else None

    except Exception as e:
        print(f"Error al obtener información: {e}")
        title, autor, imagen = None, None, None

    return title, autor, imagen

def obtener_info_casa(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title_element = soup.find("span", class_="titleProducto")
        title = title_element.get_text(strip=True).capitalize() if title_element else None

        # Extract author
        autor_element = soup.select_one("div.autores p a.inheritColor")
        autor = autor_element.get_text(strip=True) if autor_element else None

        # Extract image URL
        imagen_element = soup.select_one("div.portada img[loading='eager']")
        imagen = imagen_element["src"] if imagen_element else None

    except Exception as e:
        print(f"Error al obtener información: {e}")
        title, autor, imagen = None, None, None

    return title, autor, imagen

def obtener_info(url):
    if "goodreads.com" in url:
        # Usar Selenium para obtener información de Casa del Libro
        return obtener_info_good(url)
    elif "casadellibro.com" in url:
        # Usar requests para obtener información de Goodreads
        return obtener_info_casa(url)
    else:
        print("URL no soportada.")
        return None, None, None