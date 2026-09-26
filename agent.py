import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

from prompts import (
    CODE_ANALYZER_PROMPT,
    TEST_GENERATOR_PROMPT,
    ERROR_ANALYZER_PROMPT,
    SELF_HEALER_PROMPT,
)

from test_runner import run_tests


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

class AgentState(TypedDict):
    code: str
    language: str
    analysis: str
    test_code: str
    test_result: str
    error_analysis: str
    success: bool
    attempts: int



# 1. Analyze Code


def analyze_code(state: AgentState):

    prompt = CODE_ANALYZER_PROMPT.format(
        code=state["code"]
    )

    response = llm.invoke(prompt)

    return {
        "analysis": response.content
    }




def generate_tests(state: AgentState):

    prompt = TEST_GENERATOR_PROMPT.format(
        code=state["code"],
        analysis=state["analysis"]
    )

    response = llm.invoke(prompt)

    test_code = response.content

    test_code = test_code.replace("```python", "")
    test_code = test_code.replace("```javascript", "")
    test_code = test_code.replace("```java", "")
    test_code = test_code.replace("```", "")

    test_code = test_code.strip()

    return {
        "test_code": test_code,
        "attempts": 1
    }


# --------------------------------
# 3. Execute Tests
# --------------------------------

def execute_tests(state: AgentState):

    result = run_tests(
        state["code"],
        state["test_code"],
        state["language"]
    )

    return {
        "test_result": result["output"],
        "success": result["success"]
    }



# 4. Analyze Error


def analyze_error(state: AgentState):

    prompt = ERROR_ANALYZER_PROMPT.format(
        code=state["code"],
        test_code=state["test_code"],
        test_result=state["test_result"]
    )

    response = llm.invoke(prompt)

    return {
        "error_analysis": response.content
    }


# --------------------------------
# 5. Self Healing
# --------------------------------

def self_heal(state: AgentState):

    prompt = SELF_HEALER_PROMPT.format(
        code=state["code"],
        test_code=state["test_code"],
        error_analysis=state["error_analysis"]
    )

    response = llm.invoke(prompt)

    improved_test = response.content

    improved_test = improved_test.replace(
        "```python", ""
    )

    improved_test = improved_test.replace(
        "```javascript", ""
    )

    improved_test = improved_test.replace(
        "```java", ""
    )

    improved_test = improved_test.replace(
        "```", ""
    )

    improved_test = improved_test.strip()

    return {
        "test_code": improved_test,
        "attempts": state["attempts"] + 1
    }


# --------------------------------
# 6. Check Result
# --------------------------------

def check_result(state: AgentState):

    if state["success"]:
        return "success"

    if state["attempts"] >= 3:
        return "stop"

    return "heal"


# --------------------------------
# Build LangGraph
# --------------------------------

workflow = StateGraph(AgentState)

workflow.add_node(
    "analyze_code",
    analyze_code
)

workflow.add_node(
    "generate_tests",
    generate_tests
)

workflow.add_node(
    "execute_tests",
    execute_tests
)

workflow.add_node(
    "analyze_error",
    analyze_error
)

workflow.add_node(
    "self_heal",
    self_heal
)


workflow.set_entry_point(
    "analyze_code"
)


workflow.add_edge(
    "analyze_code",
    "generate_tests"
)

workflow.add_edge(
    "generate_tests",
    "execute_tests"
)


workflow.add_conditional_edges(
    "execute_tests",
    check_result,
    {
        "success": END,
        "heal": "analyze_error",
        "stop": END
    }
)


workflow.add_edge(
    "analyze_error",
    "self_heal"
)

workflow.add_edge(
    "self_heal",
    "execute_tests"
)


app = workflow.compile()


# --------------------------------
# Main Agent Function
# --------------------------------

def run_agent(code: str, language: str):

    initial_state = {
        "code": code,
        "language": language,
        "analysis": "",
        "test_code": "",
        "test_result": "",
        "error_analysis": "",
        "success": False,
        "attempts": 0
    }

    result = app.invoke(
        initial_state
    )

    return result