import streamlit as st
import requests
import datetime

# Strava API Authentication URL
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
CLIENT_ID = "your_client_id"  # Replace with your client ID
CLIENT_SECRET = "your_client_secret"  # Replace with your client secret
REDIRECT_URI = "http://localhost:8501"  # Change to your redirect URI

# Step 1: Strava OAuth2 authentication
def get_authorization_url():
    auth_url = f"{STRAVA_AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=read"
    return auth_url

# Step 2: Fetch the access token
def get_access_token(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(STRAVA_TOKEN_URL, data=data)
    return response.json().get('access_token')

# Step 3: Get the recent cycling activities
def get_cycling_activities(access_token):
    url = f"https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Step 4: Display nearby events (using a mock event API or location)
def get_nearby_events(location):
    # Example: Replace with an actual event API or database for events.
    events = [
        {"name": "Bike Ride Meetup", "location": "Park A", "time": "2:00 PM"},
        {"name": "Cycling Championship", "location": "Downtown", "time": "3:30 PM"}
    ]
    # Filter events based on the user's location or preferences
    return events

# Streamlit Interface
def main():
    st.title("Cycle Ride Event Explorer")

    # Authentication step
    if "access_token" not in st.session_state:
        st.write("Please log in with Strava to get started.")
        auth_url = get_authorization_url()
        st.markdown(f"[Log in with Strava]({auth_url})")
        
        # Redirect to Strava authorization page
        code = st.text_input("Enter the authorization code:")
        if code:
            access_token = get_access_token(code)
            st.session_state.access_token = access_token
            st.success("Logged in successfully!")
    else:
        access_token = st.session_state.access_token

        # Fetch cycling activities
        activities = get_cycling_activities(access_token)
        
        if activities:
            st.write("Your Recent Cycling Activities:")
            for activity in activities[:5]:  # Display the top 5 activities
                st.write(f"Activity: {activity['name']}")
                st.write(f"Date: {activity['start_date']}")
                st.write(f"Distance: {activity['distance'] / 1000} km")
                st.write(f"Duration: {str(datetime.timedelta(seconds=activity['elapsed_time']))}")
                st.write("-" * 50)

            # Get nearby events (using a mock location or GPS data)
            location = "Current Location"  # Replace with actual GPS data or user input
            events = get_nearby_events(location)
            
            if events:
                st.write("Nearby Events:")
                for event in events:
                    st.write(f"Event: {event['name']}")
                    st.write(f"Location: {event['location']}")
                    st.write(f"Time: {event['time']}")
                    st.write("-" * 50)
            else:
                st.write("No events found nearby.")
        else:
            st.write("No cycling activities found.")

if __name__ == "__main__":
    main()
