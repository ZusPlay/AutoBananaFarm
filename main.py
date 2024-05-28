import pyautogui
import time
import subprocess
import os
import psutil
import requests

steam_path = r'C:\Program Files (x86)\Steam\Steam.exe'  # Specify path to Steam.exe
game_id = '2923300'
game_executable = 'Banana.exe'
steamId = ''  # Your Steam ID (steamID64 (Dec))


def get_inventory():
    url = f'https://steamcommunity.com/inventory/{steamId}/{game_id}/2'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('descriptions', [])
    else:
        print('Failed to retrieve inventory')
        return None


def check_new_items(old_inventory):
    new_inventory = get_inventory()
    if not new_inventory:
        return None

    old_items = {item['classid'] for item in old_inventory}
    new_items = {item['classid'] for item in new_inventory}
    new_item_ids = new_items - old_items

    new_item_names = [item['name'] for item in new_inventory if item['classid'] in new_item_ids]
    return new_item_names


def start_game():
    subprocess.Popen([steam_path, '-applaunch', game_id])  # Launch the game via Steam

    # print('Waiting for the game to start...')  # Waiting for the game to start by checking for a window
    game_is_started = False
    while not game_is_started:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == game_executable:
                time.sleep(5)
                game_is_started = True
                break
        time.sleep(1)
    # print('The game is up and running!')


def click_center():
    screen_width, screen_height = pyautogui.size()  # Get the screen size
    pyautogui.click(screen_width // 2, screen_height // 2)  # Click in the center of the screen


def close_game():
    os.system(f'taskkill /F /IM {game_executable} > nul 2>&1')  # Close the game via taskkill (for Windows)
    time.sleep(3)  # Wait 3 seconds for all processes to complete


def main():
    old_inventory = get_inventory()
    while True:
        start_game()
        click_center()
        time.sleep(3)  # Wait a little while after clicking
        close_game()

        new_items = check_new_items(old_inventory)
        if new_items:
            print('New items in inventory:', ', '.join(new_items))
            old_inventory = get_inventory()

        time.sleep((3 * 60 * 60) + 60)  # Wait 3 hours and 1 minute for the next startup


if __name__ == '__main__':
    main()
