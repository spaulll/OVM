import sqlite3
import os
import base64
from dotenv import load_dotenv

load_dotenv()

def is_wallet_address_present_in_db(address):
    with sqlite3.connect('backend/db/voter_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM voters WHERE wallet_address = ?', (address,))
        count = cursor.fetchone()[0]
        return count > 0

# Function to fetch candidate details from the database based on the wallet address
def get_candidates_from_db(address):
    # Retrieve the area from the database
    with sqlite3.connect('backend/db/voter_data.db') as conn:
        cursor = conn.cursor()

        # Query to find the area corresponding to the address
        cursor.execute('SELECT area FROM voters WHERE wallet_address = ?', (address,))
        area = cursor.fetchone()
        
    # If no area is found, return None
    if area is None:
        return None
    
    #Retrieve candidate details from the database
    with sqlite3.connect('backend/db/candidates.db') as conn:
        cursor = conn.cursor()

        # Query to find candidate details for the specified area
        cursor.execute('SELECT * FROM candidates WHERE area = ?', (area[0],))
        results = cursor.fetchall()

    # If no candidates are found, return None
    if not results:
        return None

    # Convert the results to a list of dictionaries
    candidates = []
    for candidate in results:
        candidates.append({
            'candidate_id': candidate[0],
            'name': candidate[1],
            'area': candidate[2],
            'party': candidate[3],
            'photo': base64.b64encode(candidate[4]).decode('utf-8')
        })

    return candidates

def get_all_candidates():
    with sqlite3.connect('backend/db/candidates.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM candidates')
        results = cursor.fetchall()

    candidates = []
    for candidate in results:
        candidates.append({
            'candidate_id': candidate[0],
            'name': candidate[1],
            'area': candidate[2],
            'party': candidate[3],
            'photo': base64.b64encode(candidate[4]).decode('utf-8')
        })
        
    return candidates