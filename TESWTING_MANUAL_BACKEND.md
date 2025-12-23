# 🧪 HELIOSIGHT – FULL MANUAL TEST PLAN (CLI / PowerShell)

This document defines a **clean, deterministic, end-to-end manual test plan** to validate everything built so far in HelioSight **without touching the frontend**.

It validates:
- Authentication
- Role hierarchy
- Multi-tenancy
- User profiles & hardware mapping
- Bulk upload (users + external credentials)

---

## 🎯 GOAL

1. Create Super Admin (DB bootstrap)
2. Create Company (EPC)
3. Create Company Admin
4. Create End User (manual signup)
5. Bulk upload users + external credentials
6. Verify database state
7. Verify bulk users can log in

---

## ⚙️ PRE-REQUISITES

Start backend:

```powershell
docker compose up -d

curl http://localhost:8000/health

Expected:

{ "status": "ok" }

STEP 0️⃣ – CREATE SUPER ADMIN (DB-LEVEL, ONE TIME)

Super admin is bootstrap-only, not created via signup.

INSERT INTO users (
  username,
  email,
  password_hash,
  role,
  is_active
)
VALUES (
  'superadmin',
  'superadmin@heliosight.ai',
  '$2b$12$/FlOzbvMDyBRWMBZqxixo.jtxq4rP/jjRByQVgFFwHzcRq1VEdAWC',
  'super_admin',
  TRUE
);


🔐 Use the same bcrypt utility already used in backend (hash_password()).

STEP 1️⃣ – LOGIN AS SUPER ADMIN
curl http://localhost:8000/auth/login `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{
    "email": "superadmin@heliosight.ai",
    "password": "SuperAdminPassword"
  }'


Save token:

$SUPER_ADMIN_TOKEN="PASTE_TOKEN_HERE"

STEP 2️⃣ – CREATE COMPANY (EPC)
curl http://localhost:8000/companies `
  -Method POST `
  -Headers @{
    "Authorization" = "Bearer $SUPER_ADMIN_TOKEN"
    "Content-Type" = "application/json"
  } `
  -Body '{
    "name": "Test EPC Pvt Ltd",
    "description": "Solar EPC Test Company"
  }'


Save company ID:

$COMPANY_ID="UUID_FROM_RESPONSE"

STEP 3️⃣ – CREATE COMPANY ADMIN (SIGNUP)

Company admin is a normal signup, but backend forces role internally.

PS C:\Users\priya\Documents\GitHub\HelioSight_V1> curl http://localhost:8000/auth/signup `
>>   -Method POST `
>>   -Headers @{ "Content-Type" = "application/json" } `
>>   -Body '{
>>     "user": {                                                                                                                       >>       "email": "admin@testepc.com",                                                                                                 >>       "username": "testepc_admin",                                                                                                  >>       "fullname": "Test EPC Admin",                                                                                                 
>>       "password": "Admin@123",
>>       "confirm_password": "Admin@123"
>>     },
>>     "address": "EPC Head Office, Mumbai, MH, India - 400001",
>>     "company": {
>>       "name": "Test EPC Pvt Ltd",
>>       "description": "Solar EPC Test Company"
>>     }
>>   }'


STEP 4️⃣ – LOGIN AS COMPANY ADMIN
 $COMPANY_ADMIN_TOKEN = (
>>   curl http://localhost:8000/auth/login `
>>     -Method POST `
>>     -Headers @{ "Content-Type" = "application/json" } `
>>     -Body '{
>>       "email": "admin@testepc.com",
>>       "password": "Admin@123"
>>     }'
>> ).Content | ConvertFrom-Json | Select -ExpandProperty access_token


 

STEP 5️⃣ – CREATE ONE END USER (MANUAL SIGNUP)

Validates:

User profile table

Hardware profile table

Role assignment

curl http://localhost:8000/auth/signup `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{
    "user": {
      "email": "user1@test.com",
      "username": "user1",
      "fullname": "User One",
      "password": "Password@123",
      "confirm_password": "Password@123"
    },
    "whatsapp_number": "+919999999999",
    "address": "Bangalore, KA",
    "panelBrand": "Adani",
    "panelCapacity": "5",
    "panelType": "Mono",
    "inverterBrand": "Solis",
    "inverterCapacity": "5"
  }'

STEP 6️⃣ – VERIFY USER CREATED (DB)
SELECT
  u.username,
  u.role,
  p.whatsapp_number,
  h.panel_brand
FROM users u
LEFT JOIN user_profiles p ON p.user_id = u.id
LEFT JOIN user_hardware_profiles h ON h.user_id = u.id
WHERE u.username = 'user1';


✅ Expected:

Exactly 1 row

All joined fields populated

STEP 7️⃣ – BULK UPLOAD USERS (COMPANY ADMIN)
📄 CSV: users.csv
username,email,full_name,provider,provider_username,provider_password
user2,user2@test.com,User Two,solis,solis_u2,solis_pw2
user3,user3@test.com,User Three,solarman,solarman_u3,solarman_pw3

⬆️ Upload
curl http://localhost:8000/bulk-upload/users `
  -Method POST `
  -Headers @{
    "Authorization" = "Bearer $COMPANY_ADMIN_TOKEN"
  } `
  -Form @{
    file = Get-Item "./users.csv"
  }

STEP 8️⃣ – VERIFY BULK USERS (DB)
SELECT
  username,
  email,
  role,
  company_id
FROM users
WHERE username IN ('user2', 'user3');


✅ Expected:

role = end_user

company_id = Test EPC

STEP 9️⃣ – VERIFY EXTERNAL CREDENTIALS
SELECT *
FROM user_external_credentials;


✅ Must contain:

provider = solis / solarman

Correct user_id

Encrypted credentials

STEP 🔟 – LOGIN AS BULK USER (CRITICAL)

Bulk users must authenticate normally.

curl http://localhost:8000/auth/login `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{
    "email": "user2@test.com",
    "password": "solis_pw2"
  }'


✅ If this succeeds → bulk upload + auth pipeline is correct

🧠 WHAT THIS TEST GUARANTEES

✔ Role hierarchy works
✔ Tenancy isolation works
✔ Profiles & hardware separation works
✔ External credentials mapping works
✔ Bulk upload creates real HelioSight users
✔ Future ingestion pipelines can safely use external creds




$SUPER_ADMIN_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjMDk2OTNiMi1mZWIyLTQ5MGItOGZkMi00MTFjODgwNGIwNzEiLCJyb2xlIjoic3VwZXJfYWRtaW4iLCJjb21wYW55X2lkIjpudWxsLCJleHAiOjE3NjY1MDg2ODV9.ZZ3riHUk41K_PQ0urGUszsPg2PS2e4LjE1cU1UVOjJM"

curl http://localhost:8000/companies `
  -Method POST `
  -Headers @{
    "Authorization" = "Bearer $SUPER_ADMIN_TOKEN"
    "Content-Type" = "application/json"
  } `
  -Body '{
    "name": "Test EPC Pvt Ltd",
    "description": "Solar EPC Test Company"
  }'

