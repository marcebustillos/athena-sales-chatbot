import streamlit as st
import pandas as pd

# Function to determine the recommended Athena program based on responses
def recommend_program(data):
    role = data.get("role")
    challenges = data.get("challenges", [])
    career_goals = data.get("career_goals", [])
    top_goal = data.get("top_goal")
    board_journey = data.get("board_journey", None)
    resume_ready = data.get("resume_ready", None)
    financial_assistance = data.get("financial_assistance", False)
    major_corporation = data.get("major_corporation", False)
    major_hub = data.get("major_hub", False)
    location = data.get("location", "")
    function = data.get("function", "")
    
    recommendation = []
    
    # Identify if coaching is needed
    if any(challenges):
        recommendation.append("Coaching")
    
    # Role-based programs
    if function == "Go-to-market":
        recommendation.append("Executive Elevate Program")
    elif function == "Product Leadership":
        recommendation.append("Executive Edge Program")
    
    # Location-based recommendations
    if major_hub:
        recommendation.append("Cohort-Based Learning")
    else:
        recommendation.append("Peer Group Experience")
    
    if location == "Florida":
        recommendation.append("Diamond Florida Membership")
    
    # Career Goal Recommendations
    if "Secure a board seat" in career_goals:
        if board_journey in ["Just starting", "Somewhat positioned"]:
            recommendation.append("Board Coaching Program (BCP)")
        if board_journey in ["Actively looking", "Had board conversations"]:
            recommendation.append("Board Readiness Course")
    
    if "Transition into a new executive role" in career_goals:
        if data.get("clarity") in ["Need clarity", "Completely lost"]:
            recommendation.append("Architect Your Next Chapter Course + Coaching")
    
    if "Rise to the C-suite" in career_goals:
        recommendation.append("Unleash Your Impact Course")
    
    if "Start a company" in career_goals:
        recommendation.append("Coaching for Founders")
    
    if "Invest in private markets" in career_goals:
        recommendation.append("Become an Investor Course")
    
    # Financial assistance recommendations
    if financial_assistance:
        if major_corporation:
            recommendation.append("Company Sponsorship Guide")
        else:
            recommendation.append("Klarna Installment Plan")
    
    return recommendation

# Streamlit UI
st.title("Athena Sales Recommendation Chatbot")

# Collect user input
name = st.text_input("Prospect Name")
email = st.text_input("Prospect Email")
role = st.selectbox("Prospect Role", ["Sr. Director or VP", "C-suite Executive", "CEO", "Experienced Board Director", "Leader in Transition", "Retired (but still engaged)"])
function = st.selectbox("Primary Function", ["Go-to-market", "Product Leadership", "Other"])
location = st.selectbox("Location", ["New York", "San Francisco", "Washington DC", "Seattle", "Miami", "Other"])
major_hub = location in ["New York", "San Francisco", "Washington DC", "Seattle", "Miami"]
career_goals = st.multiselect("What are their career priorities?", ["Secure a board seat", "Transition into a new executive role", "Explore new career paths", "Rise to the C-suite", "Start a company", "Invest in private markets", "Expand professional network", "Continue learning & give back"])
financial_assistance = st.checkbox("Do they need assistance with the membership fee?")
major_corporation = st.checkbox("Do they work for a major corporation?")

# Store responses in dictionary
data = {
    "name": name,
    "email": email,
    "role": role,
    "function": function,
    "location": location,
    "major_hub": major_hub,
    "career_goals": career_goals,
    "financial_assistance": financial_assistance,
    "major_corporation": major_corporation,
}

# Generate recommendation if data is entered
if st.button("Get Recommendation"):
    recommendation = recommend_program(data)
    st.write("### Recommended Athena Programs:")
    st.write("\n".join(recommendation))

    # Convert data to DataFrame for CSV export
    df = pd.DataFrame([data])
    df["Recommended Programs"] = ", ".join(recommendation)
    df.to_csv("athena_recommendations.csv", index=False)
    st.download_button("Download Recommendation as CSV", "athena_recommendations.csv")
