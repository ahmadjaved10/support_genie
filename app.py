import streamlit as st
from openai import OpenAI

# Set up the page
st.set_page_config(page_title="SupportGenie MVP", page_icon="🤖")
st.title("🤖 SupportGenie MVP")
st.caption("AI Customer Support Agent with RAG + Tool Calling")

# Initialize OpenAI client using Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Dummy Knowledge Base (acts as your Vector DB for MVP) ---
KB = """
Refund Policy: Refunds are processed within 30 days of purchase.
Shipping Info: Standard shipping takes 3-5 business days.
Contact: For urgent issues, email support@example.com.
"""

# --- Dummy Order Data (acts as your Tool/API for MVP) ---
ORDERS = {
    "12345": {"status": "Shipped", "eta": "Oct 5"},
    "67890": {"status": "Processing", "eta": "Oct 7"},
    "11111": {"status": "Delivered", "eta": "Delivered on Sep 30"},
}

# --- Sidebar for Dummy Login (to show you thought about auth) ---
st.sidebar.header("🔐 Demo Login")
username = st.sidebar.text_input("Username", value="demo")
password = st.sidebar.text_input("Password", type="password", value="demo123")

if username != "demo" or password != "demo123":
    st.warning("Please use the dummy credentials: demo / demo123")
    st.stop()

# --- Main Chat Interface ---
st.divider()
user_input = st.text_input("Ask SupportGenie a question:", placeholder="e.g., Where is my order 12345?")

if user_input:
    with st.spinner("Thinking..."):
        # Simple Intent Detection & Tool Calling Logic
        # (This is a simplified version of what you'd do with LangChain)
        if "order" in user_input.lower():
            # Extract order ID
            order_id = "".join(filter(str.isdigit, user_input))
            
            if order_id in ORDERS:
                order_info = ORDERS[order_id]
                st.success(f"**Order {order_id}:** Status is **{order_info['status']}**. ETA: {order_info['eta']}")
            else:
                st.error("I couldn't find that order ID. Please check and try again.")
        
        elif "refund" in user_input.lower():
            st.info("I can help with refunds. Please provide your order ID to check eligibility.")
        
        else:
            # RAG-like fallback: Send the Knowledge Base to the LLM
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a helpful support agent. Answer using ONLY this knowledge base:\n{KB}"},
                    {"role": "user", "content": user_input}
                ]
            )
            st.write(response.choices[0].message.content)
    
    # Simulate Confidence Check / Escalation
    st.divider()
    st.caption("🛡️ Confidence Guardrail: If the AI is unsure, it will escalate to a human.")