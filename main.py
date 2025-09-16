from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain.schema import HumanMessage

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")

async def query_travel_agent(query: QueryRequest):
    """
    Handle a travel query, build a graph, and return an AI-generated response.
    """
    try:
        print(query)
        graph = GraphBuilder(model_provider="groq")
        react_app=graph()


        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        messages={"messages": HumanMessage(content=query.question)}
        output = react_app.invoke(messages)


        if (
            isinstance(output, dict)
            and "messages" in output
            and output["messages"]
            ):
                
                last_msg = output["messages"][-1]
    # check if last_msg has attribute 'content'
                final_output = getattr(last_msg, "content", str(last_msg))
        else:
            final_output = "No response from bot."
        
        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


