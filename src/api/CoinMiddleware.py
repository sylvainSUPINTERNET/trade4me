from os import stat
from aiohttp import web
import json 
from src.db.models.Focus import Focus
from datetime import datetime
from src.db.Configuration import Configuration as dbConfiguration
from dotenv import dotenv_values



"""
Add or Update existing focus
"""
async def add_focus_coin(request):
    try:
        payload = await request.json()

        db = dbConfiguration(dotenv_values(".env"))
        focusCollection = db.get_collection("focus")

        focusExist = focusCollection.find_one({
            "coinUse": payload["coinUse"],
            "coinTarget": payload["coinTarget"]
        })


        if focusExist is None:
            newFocus = Focus(
            allocatedBudget=payload["allocatedBudget"],
            coinUse=payload["coinUse"],
            coinTarget=payload["coinTarget"])
            
            newFocus.createdAt= datetime.now().isoformat()
            newFocus.updatedAt = datetime.now().isoformat()
            newFocus.budgetSpend = 0.00
            to_json = json.loads(json.dumps(newFocus.__dict__))

            focusCollection.insert_one(newFocus.__dict__)
            
            return web.json_response(to_json, status=200)
        else:
            
            if "allocatedBudget" in payload:
                focusExist["allocatedBudget"] = payload["allocatedBudget"]
                
            if "coinTarget" in payload:
                focusExist["coinTarget"] = payload["coinTarget"]

            if "coinUse" in payload:
                focusExist["coinUse"] = payload["coinUse"]

            focusExist["updatedAt"] = datetime.now().isoformat()

            focusExist["budgetSpend"] = 0.00
            
            focusExist["_id"] = str(focusExist["_id"])

            return web.json_response(focusExist, status=200)
    except Exception as e:
        error = json.loads(json.dumps({"error": str(e)}))
        return web.json_response(error, status=400)

