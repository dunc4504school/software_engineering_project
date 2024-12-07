import streamlit as st
import psycopg2
import pandas as pd
import sql_queries as sq
import base64
import os
from datetime import date

# Set page configuration
st.set_page_config(page_title="Movie System", page_icon="🎥")

# Initialize session state for page navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "welcome"

if "selected_movie_id" not in st.session_state:
    st.session_state["selected_movie_id"] = None


# Database connection function
def get_connection():
    return psycopg2.connect(
        host="localhost",       # Your database host
        database="cp317_db",    # Your database name
        user="postgres",       # Your database username
        password="password" # Your database password
    )

# Create connection and cursor for DB
conn = get_connection()
cur = conn.cursor()

def get_symbol(val):
    if val > 0:
        return "✅"
    else:
        return "❗"
def scroll():
    st.markdown("""
    <script>
        window.scrollTo(0, 0);
    </script>
    """, unsafe_allow_html=True)

# Function to encode the image as base64
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Ensure the image path is correct
def add_background(background):
    background = "background.png"
    if not os.path.exists(background):
        st.error("Image file not found! Ensure the file path is correct.")
    else:
        img = get_img_as_base64(background)

        # Apply CSS for background image
        page_bg_img = f"""
                <style>
                [data-testid="stAppViewContainer"] {{
                    background-image: url("data:image/jpeg;base64,{img}");
                    background-position: center; 
                    background-repeat: no-repeat;
                    background-size: cover;
                    background-attachment: fixed;
                    image-rendering: crisp-edges; 
                    -webkit-backface-visibility: hidden;
                }}

                [data-testid="stHeader"] {{
                    background: rgba(0,0,0,0);
                }}

                [data-testid="stToolbar"] {{
                    right: 2rem;
                }}
                </style>
            """
        st.markdown(page_bg_img, unsafe_allow_html=True)

def welcome_page():
    add_background("background.png")
    #Photo
    st.image("logo.png", caption=None, width=600, use_container_width=False)
    col1, col2, col3 = st.columns([1, 1, 2]) 

    #Sign Up
    with col2: 
        if st.button("Sign Up", key="signup"):
            st.session_state["current_page"] = "signup"

    #Login
    with col3:
        if st.button("Login", key="login"):
            st.session_state["current_page"] = "login"
    
# SignUp Page (*)
def signup_page():
    if st.button("⬅️ Back to Welcome Page"):
        st.session_state["current_page"] = "welcome"

    add_background("background.png")
    st.title("📝 Sign Up")
    
    # Collect user input
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    age = st.number_input("Age", min_value=1, max_value=150, value=18, step=1)
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    
    #Attempt To Create
    if st.button("Create Account"):
        if not name or not username or not email or not phone or not password:
            st.error("Please fill out all fields.")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()

            # Check if username already exists
            cur.execute("SELECT COUNT(*) FROM account WHERE username = %s", (username,))
            if cur.fetchone()[0] > 0:
                st.error("Username already exists. Please choose a different one.")
                return

            # Generate new ID and get today's date
            cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM account")
            index = cur.fetchone()[0]
            today = date.today()

            # Insert new account
            cur.execute(
                """
                INSERT INTO account (id, name, username, date_created, email, phone, password, age)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (index, name, username, today, email, phone, password, age)
            )
            conn.commit()

            if cur.rowcount > 0:
                st.success("Account created successfully! Redirecting to login...")
                st.session_state["new_id"] = index
                st.session_state["current_page"] = "login"
                st.rerun()
            else:
                st.error("Failed to create account. Please try again.")

        except Exception as e:
            st.error(f"Database error: {e}")

# Login Page (*)
def login_page():

    add_background("background.png")
    st.title("Login Page")

    if st.button("⬅️ Back to Welcome Page"):
        st.session_state["current_page"] = "welcome"

    # User Input Fields
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Login")

    # Attempt To Login
    if login_button:
        #If Both Filled Out
        if username and password:

            #Check Database
            cur.execute(sq.attempt_login(), (username, password))
            user_id = cur.fetchone()

            #If Returns Valid Account
            if user_id:
                st.success("Login successful! Redirecting to homepage...")
                st.session_state["user_id"] = user_id
                st.session_state["username"] = username

                st.session_state["current_page"] = "homepage"
            #Fails
            else:
                st.error("Invalid username or password. Please try again.")
        else:
            st.warning("Please enter both username and password.")

def fetch_account_id():
    account_id =  st.session_state.get("user_id")
    if account_id is None:
        st.warning("You need to log in to access the account page.")
        return account_id

# Homepage
def homepage():

    add_background("background.png")
    account_id = st.session_state.get("user_id")
    # Add an image banner
    st.image(
        "banner.png",
        width=2000,
        use_container_width=True
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rock+Salt&display=swap');
    </style>
    <div style="text-align: center;">
        <p style="font-family: 'Rock Salt', cursive; font-size: 1.6rem; color: black;">
            Explore, discover and share a world of movies
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Display the four options as buttons in a grid layout
    col1, col2, col3 = st.columns([1, 0.8,0.65])

    with col1:
        if st.button("👤 Manage Account", help="Manage your account settings and preferences."):
            st.session_state["current_page"] = "account"

        if st.button("🎥 Make Reviews", help="Check out reviews of movies and TV shows."):
            st.session_state["current_page"] = "reviews"
        

    with col2:
        if st.button("🤝 Social", help="See Peer Activity"):
            st.session_state["current_page"] = "social"
        if st.button("🔍 Search", help="Search For Media"):
            st.session_state["current_page"] = "search"

    with col3:
        if st.button("✍️ Reccomendations", help="Get Reccomendations"):
            st.session_state["current_page"] = "reccomendations"
        if st.button("❌ Logout"):
            del st.session_state["user_id"]
            st.session_state["current_page"] = "welcome"
            st.success("You have been logged out.")

    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rock+Salt&display=swap');
    </style>
    <div style="text-align: center;">
        <p style="font-family: 'Rock Salt', cursive; font-size: 1.6rem; color: black;">
            What's Trending?
        </p>
    </div>
    """, unsafe_allow_html=True)
    top_rated = fetch_most_reviewed()
    display_movies_horizontally(top_rated)


#Reviews Page
def reviews_page():
    add_background("background.png")

    # Ensure account_id is retrieved from session state
    account_id = st.session_state.get("user_id")

    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    # Check if the user is logged in
    if account_id is None:
        st.warning("You need to log in to access the reviews page.")
        return

    st.title("🎥 Reviews")
    st.subheader("Explore Movie and TV Show Reviews")
    st.write("Here, you can browse through reviews or add your own.")

    # Media selection list
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM media ORDER BY name;")
    media_list = [row[0] for row in cur.fetchall()]
    conn.close()

    # Dropdown for movie name
    selected_movie_name = st.selectbox("Select a Movie/TV Show", media_list)

    # User input for review
    rating = st.slider("Rating", min_value=0.0, max_value=10.0, step=0.1)
    # Submit button logic
    if st.button("Submit Review"):
        if selected_movie_name:
            try:
                # Insert the review into the database
                conn = get_connection()
                cur = conn.cursor()
                sql = sq.add_review_frontend()
                cur.execute(sql, (account_id, selected_movie_name, rating, "None"))
                conn.commit()
                cur.close()
                conn.close()
                st.success("Review submitted successfully!")
                #st.session_state["current_page"] = "account"
                return
            except Exception as e:
                st.error(f"An error occurred while submitting your review: {e}")
        else:
            st.warning("Please fill in all fields.")
        

#Account Page (Our)
def account_page():
    add_background("background.png")
    scroll()
    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    st.title("👤 Account Page")
    st.subheader("Manage Your Account and Preferences")

    account_id =  st.session_state.get("user_id")
    if account_id is None:
        st.warning("You need to log in to access the account page.")
        return

    # Database connection
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Fetch account details
        cur.execute(sq.get_self_summary(), (account_id,))
        user_details = cur.fetchone()

        if not user_details:
            st.error("Could not fetch account details.")
            return    

        # Update Profile Section
        st.markdown("### Your Profile/Info")
        with st.form(key="update_profile_form"):
            new_name = st.text_input("Full Name(shown)", value=user_details[1])
            new_username = st.text_input("Username(shown)", value=user_details[2])
            new_phone = st.text_input("Phone Number(not shown)", value=user_details[3])
            new_email = st.text_input("Email(not shown)", value=user_details[4])
            new_age = st.text_input("Age(not shown)", value=user_details[11])
            st.write(f"**Total Reviews:** {user_details[5]}")
            st.write(f"**Followers:** {user_details[6]}")
            st.write(f"**Following:** {user_details[7]}")
            st.write(f"**Created:** {user_details[8]}")
            st.write(f"**Reviews:** {round(user_details[9],1)} ({round(user_details[10],1)}{get_symbol(user_details[10])})")
            submit_update = st.form_submit_button("Save Changes")

        #Commit Update
        if submit_update:
            try:
                cur.execute(""" UPDATE account 
                        SET name = %s, username = %s, phone = %s, email = %s, age = %s
                        WHERE id = %s
                    """,
                    (new_name, new_username, new_phone, new_email, new_age, account_id),
                )
                conn.commit()
                st.success("Profile updated successfully!")
            except Exception as e:
                st.error(f"Error updating profile: {e}")

        # Account Reviews Section
        st.markdown("### Your Reviews (expand)")
        cur.execute(sq.get_account_review(), (account_id,))
        print_account_reviews(cur.fetchall())

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

#Prints List Of Reviews For Account
def print_account_reviews(reviews):
    if reviews:
        with st.expander(f"Date, Name, Rating, (Difference From Global)"):
            for review in reviews:
                if st.button(f"🎬{review[7]} - **{review[0]}**({review[4]}) - Rated {review[1]}/10 ({round(review[2],1)}{get_symbol(review[2])})"):
                    st.session_state["current_page"] = "movie_profile"
                    st.session_state["selected_movie_id"] = review[6]
    else:
            st.write("No reviews yet.")

#Account Page (Other)
def other_account_page():
    add_background("background.png")
    scroll()

    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    if st.button("⬅️ Back to Social"):
        st.session_state["current_page"] = "social"
        st.rerun()

    st.title("👤 View User Profile")

    # Fetch and display profile details
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(sq.get_account_summary(), (st.session_state["selected_account_id"],))
        profile = cur.fetchone()

        if profile:
            user_id, name, username, total_reviews, total_followers, total_following, avg_rating, delta, datec = profile
            st.markdown("### Profile/Info")
            # Display profile information
            st.markdown(f"- **Name:** {name}")
            st.markdown(f"- **Username:** {username}")
            st.markdown(f"- **Total Reviews:** {total_reviews}")
            st.markdown(f"- **Followers:** {total_followers}")
            st.markdown(f"- **Following:** {total_following}")
            st.markdown(f"- **Created:** {datec}")
            if avg_rating: 
                st.markdown(f"- **Average Rating:** {avg_rating:.1f} ({round(delta,1)}{get_symbol(delta)})")
            else: st.markdown(f"- **Average Rating:** N/A")
            
            # Fetch and display reviews
            st.markdown("### Reviews (expand)")
            cur.execute(sq.get_account_review(), (st.session_state["selected_account_id"],))
            print_account_reviews(cur.fetchall())
            
        else:
            st.error("User not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

#Media Page
def media_page():
    add_background("background.png")
    scroll()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(sq.get_media_genre_names(), (st.session_state["selected_movie_id"],))
    result = cur.fetchone()

    # Back to Search Button
    if st.button("⬅️ Back to Search"):
        st.session_state["current_page"] = "homepage"
        st.rerun()

    # Display Movie Details
    if st.session_state["selected_movie_id"]:  # Ensure movie is not None
        
        #Obtain The Age Of This User
        cur.execute("SELECT age from account where id = %s", (st.session_state["user_id"]))
        age = cur.fetchone()[0]
        #If Age Is Less Then 14 and Adult
        if age <= 14 and result[14]:
            st.write("SORRY THIS MEDIA NOT AVAILABLE FOR YOUTH ACCOUNT")

        else:
            # Display other movie details
            st.markdown(f"<h1 style='font-weight: bold;'>{result[1]}</h1>", unsafe_allow_html=True)
            st.write(f"🎥 **Type**: {result[2]}")
            st.write(f"🎭 **Genres**: {', '.join([str(result[i]) for i in range(3, 6) if result[i]])}")
            st.write(f"📅 **Release Date**: {pd.to_datetime(result[6]).strftime('%B %d, %Y')}")
            st.write(f"⭐ **Average Rating**: {result[7]}")
            st.write(f"👥 **Total Reviews**: {result[8]}")
            st.write(f"🎬 **Studio**: {result[9]}")
            st.write(f"🎞️ **Producer**: {result[10]}")
            st.write(f"🧑‍🧑‍🧒 **Popularity**: {result[12]}")
            st.write(f"🛂 **Language**: {result[13]}")
            st.write(f"🎲 **Adult**: {result[14]}")
            st.write(f"⏩ **Description**: {result[11]}")

            # Write a Review Button
            if st.button("✍️ Write a Review"):
                st.session_state["current_page"] = "reviews"  # Redirect to review page
                st.session_state["selected_media_name"] = movie['Name']            
                st.rerun()

            # Fetch and Display Recent Reviews
            st.subheader("📝 Recent Reviews By Following (expand)")
            try:
                conn = get_connection()  # Establish database connection
                cur = conn.cursor()

                cur.execute(sq.get_media_reviews(), (st.session_state["selected_movie_id"],st.session_state["user_id"]))
                print_media_reviews(cur.fetchall())

                cur.close()
                conn.close()
            except Exception as e:
                st.error(f"An error occurred while fetching reviews: {e}")
    else:
        st.error(f"Movie details not found.")

    cur.close()
    conn.close()

#Prints List Of Media Reviews (From Following)
def print_media_reviews(reviews):
    if reviews:
         with st.expander(f"Date, Account, Rating, (Difference From Global)"):
            for review in reviews:
                if st.button(f"🧑‍🧒 {review[1]} - {review[2]} - Rated {review[0]}/10 ({round(review[3],1)}{get_symbol(review[3])})"):
                    st.session_state["current_page"] = "account_profile"
                    st.session_state["selected_account_id"] = review[4]

def print_following(following, name, f):
    with st.expander(f"{name} ({len(following)})"):
        for foll in following:
            col11, col22 = st.columns([2, 1])

            with col11:
                if st.button(f"{foll[1]} ({foll[2]}) - {foll[3]}", key=f"{f}{foll[0]}"):
                    st.session_state["current_page"] = "account_profile"
                    st.session_state["selected_account_id"] = foll[0]
            with col22:
                if st.button(f"Remove:", key=f"{f}{foll[0]}R"):
                    if name == "Following":
                        cur.execute(sq.delete_following(), (st.session_state["user_id"], foll[0]))
                    else:
                        cur.execute(sq.delete_following(), (foll[0], st.session_state["user_id"]))
                    conn.commit()
                    st.session_state["current_page"] = "social"


#SOCIAL PAGE
def social_page():
    add_background("background.png")
    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"

    # Check navigation state
    if st.session_state.get("view_profile", False):
        # If viewing a profile, call view_profile_page
        user_id = st.session_state.get("selected_user_id")
        if st.button("⬅️ Back to Social Page"):
            st.session_state["view_profile"] = False
            st.rerun()
        view_profile_page(user_id)
        return

    st.title("🤝 Social Page")
    st.subheader("Stay Connected and Discover Movies")

    account_id =  st.session_state.get("user_id")
    if account_id is None:
        st.warning("You need to log in to access the social page.")
        return


    conn = get_connection()
    cur = conn.cursor()

    st.write("## Discover Accounts")
    query = st.text_input("Search Account:")
    if query:
        cur.execute(sq.get_searched_account(), (st.session_state["user_id"], f"%{query.lower()}%"))
        
        matchs = cur.fetchall()
        if not matchs:
            st.write("No results found.")
        else:
            with st.expander(f"Matchs"):
                for row in matchs:
                    col11, col22 = st.columns([2, 1])

                    with col11:
                        if st.button(f"{row[1]} ({row[2]})"):
                            st.session_state["current_page"] = "account_profile"
                            st.session_state["selected_account_id"] = row[0]
                    
                    with col22:
                        if row[3] == 1 :
                            st.write("Already Followed")
                        else:
                            if st.button(f" Follow: {row[2]}"):
                                cur.execute(sq.add_following(), (st.session_state["user_id"], row[0]))
                                conn.commit()
                                st.rerun()
                        
                            
    
    st.write("## Your Following")
    cur.execute(sq.get_account_following(), (account_id,))
    print_following(cur.fetchall(), "Following", "F")
    
    cur.execute(sq.get_account_follows(), (account_id,))
    print_following(cur.fetchall(), "Followers", "f")



    st.write("## Recent Follower Activity")
    cur.execute(sq.get_account_recent(), (st.session_state["user_id"],))
    events = cur.fetchall()

    events = sorted(events, key= lambda row: row[9], reverse=True)

    if not events:
        st.write("No Recent Activity")
    else:
        for event in events:
            st.write(f"On _**{event[9]}**_ _**{event[5]}**_ Reviewed _**{event[4]}**_ A _**{event[6]}** (**{event[7]}{get_symbol(event[7])}**)_ ")

#SEARCH PAGE
def search_page():
    add_background("background.png")
    st.title("🔍 Search for Movies")

    if st.button("Back to Homepage"):
        st.session_state["current_page"] = "homepage"
        st.rerun()

    account_id =  st.session_state.get("user_id")
    if account_id is None:
        st.warning("You need to log in to access the account page.")
        return
    
    # Search bar
    query = st.text_input("Search Movies:")
    if query:
        movies = search_movies(query)
        if movies.empty:
            st.write("No results found.")
        else:
            
            for _, row in movies.iterrows():
                if st.button(f"{row['Name']} ({row['Type']})  -  -  -  {row['Genres']}"):
                    st.session_state["selected_movie_id"] = row["ID"]
                    st.session_state["current_page"] = "movie_profile"
                    st.rerun()


def search_movies(query):
    sql = sq.search_movies_by_attributes()
    search_term = f"%{query.lower()}%"
    conn = get_connection()  # Ensure a valid DB connection
    cur = conn.cursor()
    cur.execute(sql, (search_term, search_term, search_term, search_term, search_term, search_term))
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    if not results:
        return pd.DataFrame()
    
    return pd.DataFrame(results, columns=["ID", "Name", "Type", "Genres", "Release"])
 

# Function to fetch movie details
def get_movie_details(movie_id):
    try:
        
         
        if result:
            
            return {
                "ID": movie,
                "Name": movie_name,
                "Type": movie_type,
                "Genres": movie_genres,
                "Release": release_date,
                "Average Rating": avg_rating,
                "Total Reviews": total_reviews,
                "Studio": studio,
                "Producer": producer,
                "Description": description,
                "Popularity": popularity,
                "Language": language
            }
        return None
    except Exception as e:
        st.error(f"Error fetching movie details: {e}")
        return None


# Function to fetch recommended movies based on user preferences
def fetch_user_reccomendations(account_id):

    account_id =  st.session_state.get("user_id")
    if account_id is None:
        st.warning("You need to log in to access the account page.")
        return

    query = sq.recommend_movies_user(account_id)
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(query, (account_id, account_id))
            results = cur.fetchall()
        return results
    finally:
        conn.close()

# Function to fetch recommended movies based on followed accounts
def fetch_following_reccomendations(account_id):

    account_id =  st.session_state.get("user_id")
    if account_id is None:
        st.warning("You need to log in to access the account page.")
        return

    query = sq.recommend_movies_followed(account_id,)
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (account_id))
            results = cur.fetchall()
        return results
    finally:
        conn.close()

def fetch_most_reviewed():
    query = sq.most_reviewed()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()
        return results
    finally:
        conn.close()

def reccomendations_page():
    add_background("background.png")
    if st.button("⬅️ Back to Homepage"):
        st.session_state["current_page"] = "homepage"
    
    account_id = st.session_state.get("user_id")
    if account_id is None:
        st.warning("You need to log in to access the account page.")
        return
    
    st.title("🎥 Movie Recommendation System")

    # Recommendations based on reviews
    user_recommendations = fetch_user_reccomendations(account_id)
    if user_recommendations:
        st.subheader("Movies Recommended for You:")
        display_movies_horizontally(user_recommendations)
    else:
        st.write("No recommendations found for your reviews.")

    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")

    # Recommendations based on followed accounts
    followed_recommendations = fetch_following_reccomendations(account_id)
    if followed_recommendations:
        st.subheader("Movies Recommended Based on Followed Accounts:")
        display_movies_horizontally(followed_recommendations)
    else:
        st.write("No recommendations found based on followed accounts.")

def display_movies_horizontally(movies):
    num_columns = 3  # Number of movies per row
    for i in range(0, len(movies), num_columns):
        cols = st.columns(num_columns)
        for col, movie in zip(cols, movies[i:i + num_columns]):
            with col:
                display_movie_card(movie)

def display_movie_card(movie):
    movie_name, genre, popularity, rating, language, total_reviews, studio, friend_reviews = (movie + (None,) * 8)[:8]

    # Define the card style
    card_style = """
    <style>
        .movie-card {
            background-color: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Add shadow for depth */
        }
        .movie-card h1 {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .movie-card p {
            margin: 5px 0;
        }
    </style>
    """

    # Inject CSS
    st.markdown(card_style, unsafe_allow_html=True)

    # Create the card content
    card_content = f"""
    <div class="movie-card">
        <h1>{movie_name}</h1>
        <p><strong>Genre:</strong> {genre}</p>
        <p><strong>Popularity:</strong> {popularity}</p>
        <p><strong>Rating:</strong> {rating}</p>
        <p><strong>Language:</strong> {language}</p>
        <p><strong>Total Reviews:</strong> {total_reviews}</p>
        <p><strong>Studio:</strong> {studio}</p>

    </div>
    """

    # Render the card
    st.markdown(card_content, unsafe_allow_html=True)



# Add custom CSS for background and buttons
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        color: #444;
    }
    button {
        background-color: orange;
        color: orange;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    button:hover {
        background-color: grey;
    }
    </style>
    """, unsafe_allow_html=True)

#Welcome Page
if st.session_state["current_page"] == "welcome":
    welcome_page()

#Login Page
elif st.session_state["current_page"] == "login":
    login_page()

#Sign Up Page
elif st.session_state["current_page"] == "signup":
    signup_page()

#Create Account Page
elif st.session_state["current_page"] == "create_account":
    create_account_page()

#HomePage
elif st.session_state["current_page"] == "homepage":
    homepage()

#Add Review
elif st.session_state["current_page"] == "reviews":
    reviews_page()

#Account Details
elif st.session_state["current_page"] == "account":
    account_page()

#Reccomendations
elif st.session_state["current_page"] == "reccomendations":
    reccomendations_page()

#Social
elif st.session_state["current_page"] == "social":
    social_page()

#Search
elif st.session_state["current_page"] == "search":
    search_page()

#Movie Profile
elif st.session_state["current_page"] == "movie_profile":
    media_page()

#Other Account
elif st.session_state["current_page"] == "account_profile":
    other_account_page()
