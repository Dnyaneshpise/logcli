import requests
import time
from logcli.utils.config import BASE_URL, save_token, clear_token


def show_progress_bar(duration=10):
    """Displays a simple progress bar for a given duration (seconds)."""
    print("\n🔄 Authenticating", end="")
    for _ in range(duration):
        time.sleep(1)
        print(".", end="", flush=True)
    print("\n")

def login(email, password):
    url = f"{BASE_URL}/api/users/login"  # API Endpoint

    print(r"""
    ╔════════════════════════════════════════════╗
    ║  🔐 AUTHENTICATING... PLEASE WAIT...       ║
    ║  📡 Connecting to Flight Data Logger...    ║
    ╚════════════════════════════════════════════╝
    """)

    show_progress_bar()  # Show progress bar effect

    response = requests.post(url, json={"email": email, "password": password})

    if response.status_code == 200:
        token = response.cookies.get("token")  # Extract token

        if token:
            save_token(token)  # Save token
            print(rf"""
            ╔════════════════════════════════════════════════╗
            ║  🎉 LOGIN SUCCESSFUL!                          ║
            ║  🚀 Welcome back, Pilot!                       ║
            ║  🔑 Secure session established.                ║
            ╠════════════════════════════════════════════════╣
            ║  🆔 Token Stored: 🔒 [SECURED]                 ║
            ║  🌍 Ready to access flight logs!              ║
            ╚════════════════════════════════════════════════╝
            """)
        else:
            print(r"""
            ╔══════════════════════════════════════╗
            ║  ❌ LOGIN FAILED!                     ║
            ║  🔍 No authentication token found!   ║
            ║  🛑 Please try again.                ║
            ╚══════════════════════════════════════╝
            """)
    else:
        print(rf"""
        ╔══════════════════════════════════════════════╗
        ║  ❌ LOGIN ERROR!                              ║
        ║  🔥 Status Code: {response.status_code}              ║
        ║  📝 Error: {response.text}  ║
        ║  🚀 Try again with correct credentials!      ║
        ╚══════════════════════════════════════════════╝
        """)


def logout():
    url = f"{BASE_URL}/api/users/logout"
    response = requests.post(url)

    if response.status_code == 200:
        print(r"""
        ╔════════════════════════════════════════╗
        ║  🔒 LOGGED OUT SUCCESSFULLY!           ║
        ╠════════════════════════════════════════╣
        ║  🚀 Safe travels, pilot!               ║
        ║  🛸 Session terminated.                ║
        ║  🔑 Authentication token removed.      ║
        ╚════════════════════════════════════════╝"
        """)
        clear_token()
    else:
        print(f"❌ Logout failed: {response.json().get('message', 'Unknown error')}")
        print(r"""
        ╔══════════════════════════════════════╗
        ║  ⚠️ No active session found!          ║
        ║  🔍 You were already logged out.      ║
        ╚══════════════════════════════════════╝
        """)
