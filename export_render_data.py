import requests
import json

# Export data from Render via API
def export_render_data():
    base_url = "https://portfolio-backend-latest-1.onrender.com"
    
    # Get auth token first
    login_data = {
        "username": "dengjohn200@gmail.com",
        "password": "John@Alustudent1"
    }
    
    try:
        # Login
        response = requests.post(f"{base_url}/api/login", json=login_data)
        if response.status_code != 200:
            print("Login failed")
            return
        
        token = response.json()['token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Export data
        endpoints = ['messages', 'subscribers', 'admin/articles', 'admin/poems']
        data = {}
        
        for endpoint in endpoints:
            response = requests.get(f"{base_url}/api/{endpoint}", headers=headers)
            if response.status_code == 200:
                table_name = endpoint.split('/')[-1]  # Get last part
                data[table_name] = response.json()
                print(f"Exported {len(data[table_name])} {table_name}")
            else:
                print(f"Failed to export {endpoint}: {response.status_code}")
        
        # Save to file
        with open('render_data.json', 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print("Data exported to render_data.json")
        
    except Exception as e:
        print(f"Export error: {e}")

if __name__ == "__main__":
    export_render_data()