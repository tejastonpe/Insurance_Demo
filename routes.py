from fastapi import FastAPI,status,HTTPException,Depends,Security
from fastapi.security import APIKeyHeader
from schemas import BaseResponseModel,AdminSchema, EmployeeSchema, CustomerSchema, InsuranceAgentSchema,LoginRoles,LoginSchema,AdminRegistrationSchema,EmployeeRegistrationSchema,CustomerRegistrationSchema,InsuranceAgentRegistrationSchema, GetAllAgentResponseSchema, AgentSchema,FetchEmployeeSchema,GetAllEmployeeResponseSchema,FetchCustomerSchema,GetallCustomerResponseSchema, ReadAgentIdSchema, ReadAgentSchema,ReadCustomerIdSchema, ReadCustomerSchema, ReadEmployeeIdSchema, ReadEmployeeSchema,SchemeCreationResponseModel,SchemeCreationSchema,SchemeResponseModel,GetAllSchemes, InsuarancePlanRegistrationSchema, InsuarancePlanResponseSchema, ShowAllInsurancePlanSchema, GetAllInsurancePlanSchema,AllSchemeResponseModel, PolicyRegisterSchema, PolicyResponseSchema, GetAllPolicySchema, ShowAllPolicySchema
from sqlalchemy.orm import Session
from models import get_db_session,Admin, Employee, Customer, InsuranceAgent,Customer,InsuranceAgent, InsurancePlan,InsurancePlan,Scheme,EmployeeScheme, Policy
from utils import EmailUtils,PasswordUtils,JWTUtils
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from datetime import datetime

app=FastAPI()


@app.post("/admin_register", status_code=status.HTTP_201_CREATED, response_model=AdminRegistrationSchema,response_model_exclude={"data": ["Password"]})
def register_admin(admin: AdminSchema, db: Session = Depends(get_db_session)):
    try:
        admin_exists = db.query(Admin).filter(Admin.Username == admin.Username).first()
        if admin_exists:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        new_admin = Admin(**admin.model_dump())
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        
        EmailUtils.send_email(to_email=admin.Email,Subject=f"Credential Details for E-Insuarance App",body=f'''Welcome to the Application... 
                              \n Dear {[admin.FullName]}, \n 
                              We are pleased to inform you that your e-Insurance account has been successfully created. 
                              Below you will find your login credentials and instructions for accessing your account. 
                              \n User Name: {admin.Username} \n Password: {admin.Password}''')
        return {"message": "Admin registered successfully", "status": 201,"data":new_admin}
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error - {e}")
  