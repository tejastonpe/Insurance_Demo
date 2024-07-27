from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey,Text,DECIMAL,create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker,backref
from settings import settings
from utils import PasswordUtils
from datetime import datetime
from sqlalchemy.orm import relationship

engine = create_engine(settings.DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass

class Admin(Base):
    __tablename__ = 'admin'
    AdminID = Column(Integer, primary_key=True, index=True,autoincrement=True)
    Username = Column(String(50), nullable=False)
    Password = Column(String(255), nullable=False)
    Email = Column(String(100), nullable=False)
    FullName = Column(String(100), nullable=False)
    CreatedAt = Column(DateTime, nullable=False,default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Password = PasswordUtils.hash_password(self.Password)

class Employee(Base):
    __tablename__ = 'employee'
    EmployeeID = Column(Integer, primary_key=True, index=True,autoincrement=True)
    Username = Column(String(50), nullable=False)
    Password = Column(String(255), nullable=False)
    Email = Column(String(100), nullable=False)
    FullName = Column(String(100), nullable=False)
    Role = Column(String(50), nullable=False)
    CreatedAt = Column(DateTime, nullable=False,default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Password = PasswordUtils.hash_password(self.Password)

class Customer(Base):
    __tablename__ = 'customer'
    CustomerID = Column(Integer, primary_key=True, index=True,autoincrement=True)
    FullName = Column(String(100), nullable=False)
    Email = Column(String(100), nullable=False)
    Username = Column(String(50), nullable=False)
    Password = Column(String(255), nullable=False)
    Phone = Column(String(15), nullable=False)
    DateOfBirth = Column(Date, nullable=False)
    AgentID = Column(Integer, ForeignKey('insuranceagent.AgentID'), nullable=False)
    CreatedAt = Column(DateTime, nullable=False,default=datetime.utcnow)
    agent = relationship("InsuranceAgent", back_populates="customers")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Password = PasswordUtils.hash_password(self.Password)

class InsuranceAgent(Base):
    __tablename__ = 'insuranceagent'
    AgentID = Column(Integer, primary_key=True, index=True,autoincrement=True)
    Username = Column(String(50), nullable=False)
    Password = Column(String(255), nullable=False)
    Email = Column(String(100), nullable=False)
    FullName = Column(String(100), nullable=False)
    CreatedAt = Column(DateTime, nullable=False,default=datetime.utcnow)
    customers = relationship("Customer", back_populates="agent")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Password = PasswordUtils.hash_password(self.Password)

class InsurancePlan(Base):
    __tablename__ = 'insuranceplan'
    PlanID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    PlanName = Column(String(100), nullable=False)
    PlanDetails = Column(Text, nullable=False)
    CreatedAt = Column(DateTime, nullable=False, default=datetime.utcnow)

class Scheme(Base):
    __tablename__ = 'scheme'
    SchemeID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    SchemeName = Column(String(100), nullable=False)
    SchemeDetails = Column(Text, nullable=False)
    SchemeAmount = Column(Integer,nullable=False)
    SchemeCover = Column(Integer,nullable=False)
    SchemeTenure = Column(Integer,nullable=False)
    PlanID = Column(Integer, ForeignKey('insuranceplan.PlanID'), nullable=False)
    CreatedAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    plan = relationship("InsurancePlan", backref=backref("schemes", cascade="all, delete-orphan"))

class Policy(Base):
    __tablename__ = 'policy'
    PolicyID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey('customer.CustomerID'), nullable=False)
    SchemeID = Column(Integer, ForeignKey('scheme.SchemeID'), nullable=False)
    PolicyDetails = Column(Text, nullable=False)
    Premium = Column(DECIMAL(10, 2), nullable=False)
    DateIssued = Column(Date, nullable=False)
    MaturityPeriod = Column(Integer, nullable=False)
    PolicyLapseDate = Column(Date, nullable=False)
    CreatedAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    customer = relationship("Customer", backref=backref("policies", cascade="all, delete-orphan"))
    scheme = relationship("Scheme", backref=backref("policies", cascade="all, delete-orphan"))

class Payment(Base):
    __tablename__ = 'payment'
    PaymentID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey('customer.CustomerID'), nullable=False)
    PolicyID = Column(Integer, ForeignKey('policy.PolicyID'), nullable=False)
    Amount = Column(DECIMAL(10, 2), nullable=False)
    PaymentDate = Column(Date, nullable=False)
    CreatedAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    customer = relationship("Customer", backref=backref("payments", cascade="all, delete-orphan"))
    policy = relationship("Policy", backref=backref("payments", cascade="all, delete-orphan"))

class Commission(Base):
    __tablename__ = 'commission'
    CommissionID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    AgentID = Column(Integer, ForeignKey('insuranceagent.AgentID'), nullable=False)
    PolicyID = Column(Integer, ForeignKey('policy.PolicyID'), nullable=False)
    CommissionAmount = Column(DECIMAL(10, 2), nullable=False)
    CreatedAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    agent = relationship("InsuranceAgent", backref=backref("commissions", cascade="all, delete-orphan"))
    policy = relationship("Policy", backref=backref("commissions", cascade="all, delete-orphan"))

class EmployeeScheme(Base):
    __tablename__ = 'employeescheme'
    EmployeeSchemeID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    EmployeeID = Column(Integer, ForeignKey('employee.EmployeeID'), nullable=False)
    SchemeID = Column(Integer, ForeignKey('scheme.SchemeID'), nullable=False)
    employee = relationship("Employee", backref=backref("employee_schemes", cascade="all, delete-orphan"))
    scheme = relationship("Scheme", backref=backref("employee_schemes", cascade="all, delete-orphan"))