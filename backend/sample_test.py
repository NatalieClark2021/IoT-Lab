import pytest
from serverSide import add_deviceSQL, delete_deviceSQL, get_devicesSQL, delALL, device_by_id



#============================================================


# def add_deviceSQL(device_id, name, ip, description, device_type):
#     cnx= mysql.connector.connect(host='localhost', user='root',password='pass13', database='iotdatabase') 
#     cursor = cnx.cursor()

#     query = ("INSERT INTO devicest (DeviceID, DeviceName, DeviceIP, DeviceDescription, deviceType)"
#     "VALUES (%s, %s, %s, %s, %s);")
#     cursor.execute(query, (device_id, name, ip, description, device_type))
#     cnx.commit()
#     cursor.close()
#     cnx.close()

#     return {"success SQL add"}

def test_add_sql(): #success test
    output =  add_deviceSQL(998,"test","test","test","test") 
    delete_deviceSQL(998) 
    assert output == "success SQL add"  
    
def test_add_sql_one():    #fail test
    output =  add_deviceSQL("test","test","test","test","test") 
    
    assert output == "failure to add"  
    

def test_add_sql_three():    #fail test

    add_deviceSQL(7,"test","test","test","test") 
    output =  add_deviceSQL(7,"test","test","test","test") 
    delete_deviceSQL(7) 
    assert output == "failure to add"  
    
    
    #delete tests
    
def test_delete_sql():    #success test
   
    add_deviceSQL(7,"test","test","test","test") 
    output =  delete_deviceSQL(7) 
    
    assert output == "success"  
    
def test_delete_sql_one():    #fail test
   
    output =  delete_deviceSQL("test") 
    
    assert output == "failure"  
    


#get tests




def test_get_all():    #empty test
   
    delALL()
    output = get_devicesSQL() 
    
    assert len(output["devices"])== 0 
    
def test_get_all_one():    #full test
   
    delALL()
    add_deviceSQL(998,"test","test","test","test") 
    output = get_devicesSQL() 
    delALL()
    assert len(output["devices"]) > 0 
    
    

#get by id

def test_by_id(): #Assert != None when device does exist
    delALL()
    
    add_deviceSQL(7,"test","test","test","test") 
    
    output = device_by_id(7)
    
    assert output != None
    
def test_by_id_two(): #assert NONE device when device not found
    delALL()
    
    output = device_by_id(7)
    
    delALL()
    assert output == None
    


   
    
    
    