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

from langchain.schema import HumanMessage

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        print(f"Received query: {query.question}")

        graph = GraphBuilder(model_provider="groq")()

        messages = {"messages": [HumanMessage(content=query.query)]}
        print("Messages sent to graph:", messages)

        output = graph.invoke(messages)
        print("Graph raw output:", output)

        # SAFE GUARD
        if (
            isinstance(output, dict)
            and "messages" in output
            and output["messages"]
        ):
            last_msg = output["messages"][-1]
            final_output = getattr(last_msg, "content", str(last_msg))
        else:
            final_output = "⚠️ Bot did not return any messages."

        return {"answer": final_output}

    except Exception as e:
        import traceback
        print("Error:", traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e)})



