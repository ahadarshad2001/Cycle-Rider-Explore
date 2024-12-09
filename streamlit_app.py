import streamlit as st
import requests
import datetime

# Strava API Configuration
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
CLIENT_ID = "your_client_id"  # Replace with your actual Client ID
CLIENT_SECRET = "your_client_secret"  # Replace with your actual Client Secret
REDIRECT_URI = "http://localhost:8501"  # Ensure this matches the redirect URI in Strava App Settings

# OAuth2 Authorization URL
def get_authorization_url():
    auth_url = (
        f"{STRAVA_AUTH_URL}?client_id={CLIENT_ID}&response_type=code"
        f"&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=read,activity:read"
    )
    return auth_url

# Exchange Authorization Code for Access Token
def get_access_token(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
    }
    response = requests.post(STRAVA_TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        st.error(f"Error: {response.json().get('message', 'Unable to fetch access token')}")
        return None

# Fetch Recent Cycling Activities
def get_cycling_activities(access_token):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.json().get('message', 'Unable to fetch activities')}")
        return []

# Mock Nearby Events Data
def get_nearby_events(location):
    events = [
        {"name": "Bike Ride Meetup", "location": "Park A", "time": "2:00 PM"},
        {"name": "Cycling Championship", "location": "Downtown", "time": "3:30 PM"},
    ]
    return events

# Main Streamlit App
def main():
    st.title("Cycle Ride Event Explorer 🚴")

    # Authentication Step
    if "access_token" not in st.session_state:
        st.write("Log in with Strava to explore your cycling activities and nearby events.")
        auth_url = get_authorization_url()
        st.markdown(f"[Log in with Strava]({auth_url})")

        # Get Authorization Code from User
        code = st.text_input("Enter the authorization code:")
        if code:
            access_token = get_access_token(code)
            if access_token:
                st.session_state.access_token = access_token
                st.success("Logged in successfully! 🎉")
    else:
        access_token = st.session_state.access_token

        # Fetch Cycling Activities
        activities = get_cycling_activities(access_token)
        if activities:
            st.subheader("Your Recent Cycling Activities:")
            for activity in activities[:5]:  # Display the top 5 activities
                st.write(f"**Activity:** {activity['name']}")
                st.write(f"**Date:** {activity['start_date']}")
                st.write(f"**Distance:** {activity['distance'] / 1000:.2f} km")
                st.write(f"**Duration:** {str(datetime.timedelta(seconds=activity['elapsed_time']))}")
                st.markdown("---")

            # Display Nearby Events
            location = "Current Location"  # Mock location
            st.subheader("Nearby Events:")
            events = get_nearby_events(location)
            if events:
                for event in events:
                    st.write(f"**Event:** {event['name']}")
                    st.write(f"**Location:** {event['location']}")
                    st.write(f"**Time:** {event['time']}")
                    st.markdown("---")
            else:
                st.write("No events found nearby.")
        else:
            st.write("No cycling activities found.")

if __name__ == "__main__":
    main()
