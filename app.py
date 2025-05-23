import asyncio
import os

import streamlit as st

from fizbuzz.agents.finance_agent import FinanceAgent
from fizbuzz.utils import get_default_ollama_llm


async def main():
    llm = get_default_ollama_llm(temperature=0.0)

    st.set_page_config(
        page_title="FizBuzz",
        page_icon="📈",
        layout="centered",
        initial_sidebar_state="auto",
    )

    st.title("FizBuzz")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I am finance agent. How can I help you?",
            }
        ]

    agent = await FinanceAgent.create(mcp_url=os.getenv("FINANCE_MCP_URL"), llm=llm)

    if prompt := st.chat_input("Ask me anything about stock!"):
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        with st.chat_message(name=message["role"]):
            st.write(message["content"])

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = await agent.handle_user_request(prompt)

            st.write(response)

            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    asyncio.run(main=main())
