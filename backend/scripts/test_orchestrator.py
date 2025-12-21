from app.providers.orchestrator import ProviderOrchestrator

credentials = [
    {
        "provider": "solis",
        "company_id": "company-uuid-1",
        "credentials": {
            "username": "...",
            "password": "...",
        },
    },
    {
        "provider": "solarman",
        "company_id": "company-uuid-2",
        "credentials": {
            "api_key": "...",
        },
    },
]

orch = ProviderOrchestrator(credentials)
metrics = orch.run()

print(f"Fetched {len(metrics)} metrics")
