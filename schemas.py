from pydantic import BaseModel, Field,EmailStr,field_validator
import re
from datetime import datetime,date
from enum import Enum
from typing import List

class RoleEnum(str, Enum):
    SchemaManager = "SchemaManager"

class LoginRoles(str,Enum):
    admin="Admin"
    employee="Employee"
    customer="Customer"
    agent="Agent"

class LoginSchema(BaseModel):
    email: EmailStr = Field(default=" ")
    password: str = Field(default=" ")
    role : LoginRoles

class BaseResponseModel(BaseModel):
    message: str
    status: int

class AdminRegistrationSchema(BaseResponseModel):
    data: "AdminSchema"

class EmployeeRegistrationSchema(BaseResponseModel):
    data:"EmployeeSchema"

class CustomerRegistrationSchema(BaseResponseModel):
    data:"CustomerSchema"

class InsuranceAgentRegistrationSchema(BaseResponseModel):
    data:"InsuranceAgentSchema"

class GetAllSchemes(BaseResponseModel):
    data:"List[AllSchemeResponseModel]"

class AllSchemeResponseModel(BaseModel):
    SchemeID: int
    SchemeName: str
    SchemeDetails: str
    SchemeAmount : int
    SchemeCover : int
    SchemeTenure : int
    PlanID: int
    CreatedAt: datetime

    class Config:
        from_attributes = True

class EmployeeLoginSchema(BaseModel):
    Email: str
    Password: str
    Role: RoleEnum

class LoginResponseSchema(BaseModel):
    message: str
    status: int
    access_token: str = None

class AgentSchema(BaseModel):
    AgentID : int
    FullName :str

    class Config:
        from_attributes = True

class GetAllAgentResponseSchema(BaseResponseModel):
    data: List[AgentSchema]

    class Config:
        orm_mode = True

class FetchEmployeeSchema(BaseModel):
    EmployeeID: int
    Username: str
    Email: str
    FullName:str
    Role: str

    class Config:
        from_attributes = True

class GetAllEmployeeResponseSchema(BaseResponseModel):
    data: List[FetchEmployeeSchema]

    class Config:
        orm_mode = True

class FetchCustomerSchema(BaseModel):
    FullName : str
    Email: str
    Username : str
    Phone: int
    DateOfBirth : date

    class Config:
        from_attributes = True

class GetallCustomerResponseSchema(BaseResponseModel):
    data:List[FetchCustomerSchema]

    class Config:
        orm_mode =True

class ReadAgentSchema(BaseModel):
    Username : str 
    Password : str 
    Email : str
    FullName : str

    class Config:
        from_attributes = True

class ReadAgentIdSchema(BaseResponseModel):
    data: ReadAgentSchema

    class Config:
        orm_mode = True

class ReadCustomerSchema(BaseModel):
    FullName : str 
    Email: str
    Username : str 
    Password : str 
    Phone: int  
    DateOfBirth : str
    AgentID: int

    class Config:
        from_attributes = True

class ReadCustomerIdSchema(BaseResponseModel):
    data: ReadCustomerSchema

    class Config:
        orm_mode = True

class ReadEmployeeSchema(BaseModel):
    Username: str
    Password: str
    Email:str
    FullName:str
    Role: str

    class config:
        from_attributes = True

class ReadEmployeeIdSchema(BaseResponseModel):
    data: ReadEmployeeSchema

    class config:
        orm_mode = True

class SchemeCreationSchema(BaseModel):
    SchemeName : str
    SchemeDetails : str
    SchemeAmount : int
    SchemeCover : int
    SchemeTenure : int
    PlanID : int 

class SchemeCreationResponseModel(BaseResponseModel):
    data:SchemeCreationSchema

class SchemeResponseModel(BaseModel):
    SchemeID: int
    SchemeName: str
    SchemeDetails: str
    PlanID: int
    CreatedAt: datetime

    class Config:
        orm_mode = True

class AdminSchema(BaseModel):
    Username: str =Field(max_length=10)
    Password: str =Field()
    Email:EmailStr
    FullName:str=Field()

    @field_validator('Password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[@$!%*?&]', value):
            raise ValueError("Password must contain at least one special character (@$!%*?&).")
        return value
    
    @field_validator("Username")
    def validate_user_name(cls, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise ValueError("Username must contain only letters, numbers, and @/./+/-/_ characters.")
        return value

class EmployeeSchema(BaseModel):
    Username: str=Field(max_length=15)
    Password: str=Field()
    Email:EmailStr
    FullName:str=Field()
    Role: RoleEnum = Field(..., description="Role of the employee")

    @field_validator('Password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[@$!%*?&]', value):
            raise ValueError("Password must contain at least one special character (@$!%*?&).")
        return value
    
    @field_validator("Username")
    def validate_user_name(cls, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise ValueError("Username must contain only letters, numbers, and @/./+/-/_ characters.")
        return value

class loginSchema(BaseModel):
    Username : str = Field()
    Password : str = Field()
    Role : str = Field(max_length=20)

    @field_validator('Password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[@$!%*?&]', value):
            raise ValueError("Password must contain at least one special character (@$!%*?&).")
        return value
    
    @field_validator("Username")
    def validate_user_name(cls, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise ValueError("Username must contain only letters, numbers, and @/./+/-/_ characters.")
        return value

class CustomerSchema(BaseModel):
    FullName : str = Field(max_length=20)
    Email: EmailStr
    Username : str = Field()
    Password : str = Field()
    Phone: int = Field()
    DateOfBirth : date
    AgentID: int

    @field_validator('Password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[@$!%*?&]', value):
            raise ValueError("Password must contain at least one special character (@$!%*?&).")
        return value
    
    @field_validator("Username")
    def validate_user_name(cls, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise ValueError("Username must contain only letters, numbers, and @/./+/-/_ characters.")
        return value
        
class InsuranceAgentSchema(BaseModel):     
    Username : str = Field()
    Password : str =Field()
    Email : EmailStr
    FullName : str = Field(max_length=20)

    @field_validator('Password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[@$!%*?&]', value):
            raise ValueError("Password must contain at least one special character (@$!%*?&).")
        return value
    
    @field_validator("Username")
    def validate_user_name(cls, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise ValueError("Username must contain only letters, numbers, and @/./+/-/_ characters.")
        return value 

class InsuarancePlanRegistrationSchema(BaseModel):        
    PlanName :str = Field(max_length=50)
    PlanDetails : str = Field(max_length=500)

class InsuarancePlanResponseSchema(BaseResponseModel):
    data : InsuarancePlanRegistrationSchema

class ShowAllInsurancePlanSchema(BaseModel):
    PlanID: int
    PlanName: str
    PlanDetails: str
    CreatedAt : datetime

    class Config:
        from_attributes= True   

class GetAllInsurancePlanSchema(BaseResponseModel):
    data: List[ShowAllInsurancePlanSchema]

    class Config:
        orm_mode = True

class PolicyRegisterSchema(BaseModel):
    SchemeID : int
    PolicyDetails : str
    Premium : int
    MaturityPeriod : int
    PolicyLapseDate : date

class PolicyResponseSchema(BaseResponseModel):
    data: PolicyRegisterSchema

class ShowAllPolicySchema(BaseModel):
    PolicyID : int
    CustomerID : int
    SchemeID : int
    PolicyDetails : str
    Premium : int
    DateIssued : date
    MaturityPeriod : int
    PolicyLapseDate : date

    class Config:
        from_attributes= True   

class GetAllPolicySchema(BaseResponseModel):
    data: List[ShowAllPolicySchema]

    class Config:
        orm_mode = True



