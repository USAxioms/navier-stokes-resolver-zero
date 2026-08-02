from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from resolver import NavierStokesResolverR3

app = FastAPI(
    title="NavierStokes Axiomatic Solution API",
    version="1.0.0"
)

class FlowEvaluationRequest(BaseModel):
    external_time: int = Field(..., description="External time t (WAD-scaled or integer base)")
    velocity: int = Field(..., description="Fluid velocity magnitude v (WAD-scaled)")
    viscosity: int = Field(10**16, description="Kinematic viscosity nu (WAD-scaled)")

@app.get("/health")
def health_check():
    return {
        "status": "operational",
        "contract": "0x2B70A9B420bd3ff30F04592D1EF4578cC0aF33ab",
        "axiom_set": {
            "WAD": 10**18,
            "VORTICITY_THRESHOLD": 10**18,
            "REGULARITY_THRESHOLD": 75 * 10**16,
            "DEFAULT_VISCOSITY": 10**16
        }
    }

@app.post("/resolve-flow")
def resolve_flow(payload: FlowEvaluationRequest):
    try:
        resolver = NavierStokesResolverR3(
            external_time=payload.external_time,
            velocity=payload.velocity,
            viscosity=payload.viscosity
        )
        result = resolver.evaluate()
        return {
            "evaluation_parameters": {
                "external_time": payload.external_time,
                "velocity": payload.velocity,
                "viscosity": payload.viscosity
            },
            "evaluation_result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
