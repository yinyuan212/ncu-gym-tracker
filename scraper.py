import requests
from bs4 import BeautifulSoup
import csv
import re
import time
from datetime import datetime
import os

# Using the specific sheet URL from your screenshot
URL = "https://docs.google.com/spreadsheets/u/0/d/e/2PACX-1vTi7PeVb_4bE22ioWlIMlYwoaDbOQiq7fdn3VRAmS_5V60_9cmTh3P8e97jfvT5X867teqRsMoGY_Ou/pubhtml/sheet?headers=false&gid=0&range=A1:B10"

def crawl():
    try:
        response = requests.get(URL, timeout=30)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # We find the cell that contains the text '重訓室'
        gym_label_cell = soup.find('td', string=re.compile('重訓室'))
        
        if gym_label_cell:
            # According to your screenshot, the number 70 is in the next <td>
            gym_value_cell = gym_label_cell.find_next_sibling('td')
            
            if gym_value_cell:
                gym_count = gym_value_cell.get_text(strip=True)
                
                # Double-check it's a number
                if gym_count.isdigit():
                    now = datetime.now().strftime("%Y-%m-%d %H:%M")
                    file_path = 'data.csv'
                    file_exists = os.path.isfile(file_path)
                    
                    # Enhanced saving logic to prevent merged lines
                    with open(file_path, 'a+', newline='', encoding='utf-8') as f:
                        # Move to the end of the file and check the last character
                        f.seek(0, 2) 
                        if f.tell() > 0:
                            f.seek(f.tell() - 1)
                            if f.read(1) != '\n':
                                f.write('\n')
                        
                        writer = csv.writer(f)
                        if f.tell() == 0: # If file was totally empty, add header
                            writer.writerow(['timestamp', 'gym_count'])
                        writer.writerow([now, gym_count])
                    
                    print(f"Success! Recorded: {now} | Count: {gym_count}")
                    return

        print("Failed to find the '70' in the gym cell. Checking structure...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    crawl()