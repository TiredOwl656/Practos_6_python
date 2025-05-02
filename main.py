import asyncio
import aiohttp

IP_API_KEY = "k1qe45zy8uuc428x"
WEATHER_API_KEY = "ymJsdGXbNlob+4md81vlxQ==ljWcYxmHBsy0OecZ"
JOKE_API_KEY = WEATHER_API_KEY

async def fetch(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            raise Exception(f"Ошибка запроса: {response.status}")
        return await response.json()

async def get_coordinates(ip):
    url = f"https://api.2ip.io/{ip}?token={IP_API_KEY}"
    async with aiohttp.ClientSession() as session:
        data = await fetch(session, url)
        return data["lat"], data["lon"], data.get("city", "неизвестно")

async def get_weather(lat, lon):
    url = f"https://api.api-ninjas.com/v1/weather?lat={lat}&lon={lon}"
    headers = {"X-Api-Key": WEATHER_API_KEY}
    async with aiohttp.ClientSession() as session:
        return await fetch(session, url, headers)

async def get_joke():
    url = "https://api.api-ninjas.com/v1/jokes"
    headers = {"X-Api-Key": JOKE_API_KEY}
    async with aiohttp.ClientSession() as session:
        jokes = await fetch(session, url, headers)
        return jokes[0]["joke"] if jokes else "Не удалось получить шутку"

async def main():
    try:
        ip = input("Введите IP-адрес: ")
        
        coordinates_task = asyncio.create_task(get_coordinates(ip))
        joke_task = asyncio.create_task(get_joke())
        
        lat, lon, city = await coordinates_task
        joke = await joke_task
        
        print(f"\n📍 Местоположение: {city}")
        print(f"🌐 Координаты: {lat}, {lon}")
        
        print("\n😄 Случайная шутка:")
        print(joke)
        
        weather = await get_weather(lat, lon)
        
        print("\n🌤 Погода:")
        print(f"🌡 Температура: {weather['temp']}°C (ощущается как {weather['feels_like']}°C)")
        print(f"📶 Влажность: {weather['humidity']}%")
        print(f"☁ Облачность: {weather['cloud_pct']}%")
        print(f"💨 Ветер: {weather['wind_speed']} м/с, направление {weather['wind_degrees']}°")
        print(f"📊 Диапазон температур: от {weather['min_temp']}°C до {weather['max_temp']}°C")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())