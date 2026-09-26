import streamlit as st
from agent import run_agent



st.set_page_config(
    page_title="Self-Improving Test Agent",
    page_icon="🧪",
    layout="wide"
)


# Title
st.title("🧪 Self-Improving Test Generation Agent")

st.write(
    "Upload your source code and let the AI generate, "
    "execute, analyze, and improve tests automatically."
)


# Language Selection
language = st.selectbox(
    "Select Programming Language",
    ["Python", "JavaScript", "Java"]
)


# File Upload
uploaded_file = st.file_uploader(
    "Upload your source code",
    type=["py", "js", "java"]
)


# If file is uploaded
if uploaded_file:

    code = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Uploaded Code")

    st.code(
        code,
        language=language.lower()
    )


    # Generate and Test
    if st.button("🚀 Generate & Test"):

        with st.spinner(
            "AI is analyzing your code and generating tests..."
        ):

            try:

                # Run Agent
                result = run_agent(
                    code,
                    language
                )


                # Workflow completed
                st.success(
                    "✅ Agent workflow completed!"
                )


                # Code Analysis
                st.subheader("🧠 Code Analysis")

                st.write(
                    result.get(
                        "analysis",
                        "No analysis available."
                    )
                )


                # Generated Tests
                st.subheader(
                    "🧪 Generated / Improved Tests"
                )

                test_code = result.get(
                    "test_code",
                    ""
                )

                display_language = {
                    "Python": "python",
                    "JavaScript": "javascript",
                    "Java": "java"
                }

                st.code(
                    test_code,
                    language=display_language[language]
                )


                # Test Execution Result
                st.subheader(
                    "📊 Test Execution Result"
                )

                test_result = result.get(
                    "test_result",
                    ""
                )


                if result.get("success"):

                    st.success(
                        "✅ Tests passed successfully!"
                    )

                else:

                    st.error(
                        "❌ Tests did not pass within "
                        "the retry limit."
                    )


                st.code(
                    test_result,
                    language="text"
                )


                # Error Analysis
                error_analysis = result.get(
                    "error_analysis",
                    ""
                )

                if error_analysis:

                    st.subheader(
                        "🔍 Error Analysis"
                    )

                    st.write(
                        error_analysis
                    )


                # Self-Healing Attempts
                st.subheader(
                    "🔄 Self-Healing Attempts"
                )

                st.metric(
                    "Attempts",
                    result.get(
                        "attempts",
                        0
                    )
                )


            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )