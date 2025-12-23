def bulk_preview(users, external_creds):
    users = users or []
    external_creds = external_creds or []
    return {
        "users_count": len(users),
        "external_credentials_count": len(external_creds),
        "providers": sorted({str(c.provider) for c in external_creds}),
    }
