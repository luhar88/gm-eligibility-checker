# gm-eligibility-checker
Application to verify an employee's eligibility

## Build and run steps
`docker-compose build`

`docker-compose up`

## API
Server runs on localhost:8000
Below are the supported url's

| Method | Route | Description |
|---|---|---|
| GET | `/v1/ping` | Returns a 200 with "pong" as response |
| GET | `/v1/PARTNER_ID/config` | Returns the accepted employee query schema for the partner |
| POST | `/v1/PARTNER_ID/check` | Takes in a schema as part of the post body, and returns a json response if the employee's eligibility |

### Partner Currently Supported
**Acme**         
Acme supplies GM with a tsv file, listing eligible employees metadata.
Verification is performed based on employee_id.

**E.g.**            
_Accepted partner_id = 12345_ (details in eligibiity_checker_service/web/sample_data/partner_metadata.json)          
_Accepted employee_id's for '12345' partner_id are [1111,2222,3333,4444,5555,6666,7777,8888,9999,1]_ (details in eligibiity_checker_service/web/sample_data/acme_data.tsv)           

**Sample api calls**            
`curl -X GET http://localhost:8000/v1/ping`          
`curl -X GET http://localhost:8000/v1/12345/config`            
`curl -X POST http://localhost:8000/v1/12345/check -H 'Content-Type: application/json' -d '{"employee_id": 1111}'`                

## Next Steps
- Mechanism to refresh employee details file
- Add production nginx container
- Add unit, functional, load tests
- Setup db container to store schema's, employee data, also setup cache 
- Setup documentation container for swagger
