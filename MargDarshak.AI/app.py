import streamlit as st
from features.auth import authentication
from features.functions import load_lottie_file
import streamlit_lottie as st_lottie



st.set_page_config(page_title="MargDarshak.AI",
            page_icon="🧑🏻‍🎓",
            layout="wide",
            initial_sidebar_state="expanded")

if 'register' not in st.session_state:
    st.session_state['register'] = False
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

def intro():
    st.header("MargDarshak.AI: AI-Powered Course Advisor 🧑🏻‍🎓", divider='rainbow')

    with st.container(border=True):
        left_col, right_col = st.columns(2)
        with left_col:
                st.subheader("About MargDarshak.AI", divider='rainbow')
                intro = '''
                        For students, choosing the right skills and courses can be overwhelming with so many
                        options available. Without proper guidance, they often struggle to find the most relevant
                        learning resources, wasting valuable time on courses that don’t align with their career goals.
                        This app serves as a personal AI learning companion, helping students make informed decisions by
                        recommending the best courses, study plans, and project ideas tailored to their interests and future
                        aspirations.

                        **MargDarshak.AI** An AI-powered personalized learning assistant that helps students choose the right courses, skills, and projects based on their career goals.
                        Using Generative AI, the platform provides personalized study plans, AI-generated notes, resume-building tools, and project ideas, ensuring students focus on learning
                        what truly matters. With an interactive and smart AI-driven approach, this app eliminates confusion, enhances skill development, and helps students confidently navigate their learning journey.
                '''
                st.markdown(intro)


        with right_col:
                robot_assist = load_lottie_file("animations/Animation - 1740647666211.json")
                st_lottie.st_lottie(robot_assist, loop=True, width=500, height=500)

    with st.container(border=True):
            left_col, right_col = st.columns(2)
            with right_col:
                st.subheader("Features of MargDarshak.AI ℹ️", divider='rainbow')
                features = [
                            "**AI Mentor:** AI Mentor is a Personalized Learning Assistant that helps students with their learning journey.",
                            "**Roadmap Generator:** Roadmap Generator provides a personalized learning path for students based on their career goals.",
                            "**Career Guidance:** Career Guidance feature helps students explore various career options and their growth prospects.",
                            "**Feedback:** Feedback feature allows students to share their experience and suggestions for improvement."
                ]

                for feature in features:
                    st.markdown(f"🔹 {feature}")
                st.write("*Explore the features from the sidebar navigation.*")

            with left_col:
                feature_animation = load_lottie_file("animations/Animation - 1740647732574.json")
                st_lottie.st_lottie(feature_animation, loop=True, width=500, height=400)

    with st.container(border=True):
            st.subheader("Why Margdarshak.AI? 🚀", divider='rainbow')
            left_col, right_col = st.columns(2)
            with left_col:
                    benefits = [
                                "Personalized Learning Experience: AI-driven recommendations tailored to your interests and career goals.",
                                "Skill Development: Develop in-demand skills with curated courses, study plans, and project ideas.",
                                "Career Guidance: Explore various career options and growth prospects to make informed decisions.",
                                "Resume Building: Create professional resumes with AI-generated content and project highlights.",
                                "Feedback Mechanism: Share your experience and suggestions to help us improve the platform."
                    ]

                    for benefit in benefits:
                        st.markdown(f"🔹 {benefit}")

            with right_col:
                benefits_animation = load_lottie_file("animations/Animation - 1736172774697.json")
                st_lottie.st_lottie(benefits_animation, loop=True, width=500, height=300)

    with st.container(border=True):
            st.subheader("FAQs❓", divider='rainbow')

            # FAQ 1
            with st.expander("What is MargDarshak.AI?"):
                st.write("MargDarshak.AI is an AI-powered learning assistant that helps students choose the right courses, develop skills, and build career-focused projects. It offers personalized recommendations and study plans based on your interests and career goals.")

            # FAQ 2
            with st.expander("What are the features of MargDarshak.AI?"):
                st.write("It offers AI-driven course recommendations, study material generation, resume building, coding assistance, and personalized study plans. The platform also provides career guidance and project ideas to help students make informed decisions.")

            # FAQ 3
            with st.expander("How MargDarshak.AI will help you?"):
                st.write("It simplifies learning by providing smart recommendations, AI-generated resources, and career guidance tailored to your goals. The platform ensures you focus on relevant skills, courses, and projects, enhancing your learning experience.")

            # FAQ 4
            with st.expander("How to use MargDarshak.AI?"):
                st.write("Simply enter your interests, career goals, or learning preferences, and the AI will provide customized recommendations and resources. You can explore various features like AI Mentor, Roadmap Generator, Career Guidance, and Feedback to enhance your learning journey.")

            # FAQ 5
            with st.expander("How to contact Team MargDarshak?"):
                st.write("You can contact us from the Feedback feature in the sidebar navigation. Share your experience, suggestions, or queries, and our team will get back to you promptly.")


authentication()

if st.session_state["authentication_status"]:
     pg = st.navigation([
        st.Page(intro, title="Home", icon="🏠"),
        st.Page("features/0-AI-Mentor.py", title="CareerBot AI", icon="🧑🏻‍🏫"),
        st.Page("features/1-Skill-Assessment.py", title="SkillLens", icon="📊"),
        st.Page("features/2-Roadmap.py", title="PathFinder", icon="📚"),
        st.Page("features/RAG.py", title="LearnWise", icon="🎓"),
        st.Page("features/2-Career-Guidance.py", title="CareerNavigator", icon="🚀"),
        st.Page("features/Mock-Interview.py", title="InterviewPro", icon="🎙️"),
        st.Page("features/Feedback.py", title="Feedback", icon="📝"),
    ])
     pg.run()
