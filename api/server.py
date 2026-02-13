# api/server.py
# Externe API-Schicht der AI-Chain
# Darf NICHTS initialisieren, NICHTS erzeugen, NICHTS laden.
# Darf NUR über vm.VC -> interne API kommunizieren.

from fastapi import FastAPI
from vm import get_vm_vc

app = FastAPI()

# VM/VC-Instanz abrufen (NICHT neu erzeugen!)
vm_vc = get_vm_vc()


# ---------------------------
# EXTERNE ENDPOINTS
# ---------------------------

@app.get("/blocks")
def get_blocks():
    # Viewer ist intern -> über interne API "portfolio" oder eigenen viewer-call
    return vm_vc.vm.viewer.get_blocks()


@app.post("/register")
def register(username: str, password: str, phrase: str):
    # Extern -> Intern
    return vm_vc.call_internal(
        "register",
        username=username,
        password=password,
        phrase=phrase
    )


@app.post("/login")
def login(username: str, password: str):
    return vm_vc.call_internal(
        "login",
        username=username,
        password=password
    )


@app.post("/logout")
def logout(username: str):
    return vm_vc.call_internal(
        "logout",
        username=username
    )


@app.get("/portfolio/{address}")
def portfolio(address: str):
    return vm_vc.call_internal("portfolio", address)


@app.post("/deposit")
def deposit(address: str, amount: float):
    return vm_vc.call_internal(
        "deposit",
        address=address,
        amount=amount
    )


@app.post("/withdraw")
def withdraw(address: str, amount: float):
    return vm_vc.call_internal(
        "withdraw",
        address=address,
        amount=amount
    )


@app.get("/marketprice")
def marketprice():
    return vm_vc.call_internal("marketprice")


@app.post("/sync")
def sync():
    return vm_vc.call_internal("sync")
  
