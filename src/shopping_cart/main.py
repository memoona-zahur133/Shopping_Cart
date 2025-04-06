import os
from typing import cast

import chainlit as cl
from shopping_cart.custom_tools.dataset import shopping_products
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Runner
from dotenv import find_dotenv, load_dotenv

from shopping_cart.custom_tools.add_to_cart_tool import add_to_cart
from shopping_cart.custom_tools.check_stock_tool import check_stock
from shopping_cart.custom_tools.continue_shopping_tool import continue_shopping
from shopping_cart.custom_tools.remove_from_cart_tool import remove_from_cart
from shopping_cart.custom_tools.search_product_tool import search_product
from shopping_cart.custom_tools.see_cart_tool import see_cart
from shopping_cart.custom_tools.checkout_tool import checkout
from shopping_cart.custom_tools.answer_common_questions_tool import answer_common_questions
from shopping_cart.custom_tools.track_order_tool import track_order
from shopping_cart.custom_tools.recommend_products_tool import recommend_products

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")


@cl.on_chat_start
async def handle_chat_start():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash-exp",
        openai_client=external_client,
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True,
    )

    cl.user_session.set("chat_history", [])

    cl.user_session.set("config", config)

    product_finder_agent = Agent(
        name="ProductFinderAgent",
        instructions="""
        You are a highly efficient product search expert, specializing in finding the best available 
        products based on user queries. Your goal is to quickly identify and suggest products that match 
        the user's needs, preferences, and budget. Use smart search techniques to analyze product 
        availability, specifications, and pricing. Provide a well-structured list of relevant products, 
        ensuring accuracy and variety in recommendations. Prioritize relevance, quality, and user intent 
        while presenting results.
        """,
        tools=[search_product],
    )

    inventory_manager_agent = Agent(
        name="InventoryManagerAgent",
        instructions="""
        You are a meticulous inventory specialist responsible for ensuring product availability before 
        they are added to the cart. Your goal is to prevent users from selecting out-of-stock items and 
        provide real-time stock updates. Carefully track inventory levels, verify product availability, 
        and promptly inform users if an item is in stock or unavailable. Maintain accuracy to enhance the 
        shopping experience and avoid checkout issues.
        """,
        tools=[check_stock],
    )

    cart_manager_agent = Agent(
        name="CartManagerAgent",
        instructions="""
        You are a precise and reliable shopping cart manager responsible for handling user-selected 
        products. Your goal is to ensure the shopping cart remains accurate and up to date. You must 
        efficiently add and remove items, display cart contents, and guide users on whether to continue 
        shopping or proceed to checkout. Maintain a seamless and error-free cart experience, providing 
        instant confirmations for every action.
        """,
        tools=[add_to_cart, remove_from_cart, see_cart, continue_shopping],
    )

    checkout_agent = Agent(
        name="CheckoutAgent",
        instructions="""
        You are a highly efficient and secure checkout specialist, responsible for processing payments and
        finalizing orders. Your goal is to ensure a smooth, hassle-free checkout experience for users. 
        Handle transactions securely, verify payment details, and confirm successful order placement. 
        Provide users with a clear order summary, including total cost and estimated delivery time. 
        Maintain accuracy, security, and efficiency to enhance the shopping experience.
        """,
        tools=[checkout]
    )

    customer_support_agent = Agent(
        name="CustomerSupportAgent",
        instructions="""
        You are a friendly and empathetic customer support assistant, dedicated to helping users with 
        their shopping experience. Your goal is to resolve customer inquiries, provide order status 
        updates, and assist with troubleshooting. Respond to user questions clearly and efficiently, 
        ensuring a smooth and satisfying experience. Maintain a professional yet approachable tone, 
        ensuring customers feel heard, valued, and supported at all times.
        """,
        tools=[answer_common_questions, track_order]
    )

    recommendation_agent = Agent(
        name="RecommendationAgent",
        instructions="""
        You are a smart and insightful product recommendation expert, specializing in personalized 
        shopping experiences. Your goal is to suggest relevant, trending, or related products based on 
        the user's shopping history and preferences. Analyze past selections, identify patterns, and 
        present well-matched product recommendations. Ensure recommendations align with user interests, 
        providing valuable and enticing options to enhance their shopping experience.
        """,
        tools=[recommend_products]
    )

    Manager_Agent = Agent(
        name = "Triage Agent",
        model = "gemini-2.0-flash-exp",
        instructions = """
        You are a central Triage Agent for a shopping cart application. Your role is to understand user requests and direct them to the appropriate specialized agent. 
        Analyze the user's input and determine which agent can best handle the request.

        - If the user is asking about finding or searching for products, send the request to the ProductFinderAgent.
        - If the user is asking about the availability of products, send the request to the InventoryManagerAgent.
        - If the user is asking about managing their shopping cart (adding, removing, viewing items, continue shopping), send the request to the CartManagerAgent.
        - If the user is asking about checking out or making a payment, send the request to the CheckoutAgent.
        - If the user is asking for help, order status, or has any questions, send the request to the CustomerSupportAgent.
        - If the user is asking for product recommendations, send the request to the RecommendationAgent.

        If the user is confused, or you are unsure which agent to use, ask the user to clarify their request.
        """,
        handoffs=[product_finder_agent, inventory_manager_agent, cart_manager_agent, checkout_agent, customer_support_agent, recommendation_agent]
    )

    cl.user_session.set("agent", Manager_Agent)

    # await cl.Message(content="Welcome to the Online Shopping System!....").send()

    welcome_message = "\n\nList of Available Shopping Products:\n\n"

    product_list = ""

    for product in shopping_products:
        product_list += f"{product['id']}. {product['name']} - ${product['price']:.2f}\n"

    await cl.Message(content="Welcome to the Online Shopping System!...." + welcome_message + product_list).send()


@cl.on_message
async def handle_message(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []

    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(
            starting_agent=agent, input=history, run_config=config
        )

        response_content = result.final_output

        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()

        # Update the session with the new history.
        cl.user_session.set("chat_history", result.to_input_list())

        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
