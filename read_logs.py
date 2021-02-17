import os
import json 

class tenant_unique_users():
  def __init__(self):
    self.count = {}
    self.month_userlist = {}

def parse_file():
  try:
    data = {}
    print ("Identifying all the files")

    for file in os.listdir("/root"):
      if file.endswith(".log"):
        my_file = os.path.join("/root", file)
        fp = open(my_file, "r")
        for line in fp.readlines():
          # These are activities by the synthetic monitors and should not counted as login acitivity
          if "WebUI " in line:
            continue
          else:
            #print (line)
            date_obj = line.split(" UTC ")
            month = date_obj[0].split("-")[1]
            #print (month)

            json_data = date_obj[1]
            event_dict = json.loads(json_data)
            if event_dict["eventType"] == "LOGIN":
              tenantId = event_dict["tenantId"]
              userId = event_dict["userId"]
              #print (tenantId)
              try:
                user_list = data[tenantId].month_userlist[month]
                if userId in user_list:
                   continue
                else:
                    data[tenantId].month_userlist[month].append(userId)
                    data[tenantId].count[month] = data[tenantId].count[month] + 1
                    print("Count " + tenantId + " " + str(month) + " " + str(data[tenantId].count[month]))
                    print(data[tenantId].month_userlist[month])

              except KeyError:
                    print("Month: " + tenantId + " " + str(month))
                    var = tenant_unique_users()
                    var.count[month] = 1 
                    var.month_userlist[month] = []
                    var.month_userlist[month].append(userId)
                    data[tenantId] = var
    print("PRINTINGGGGG")
    for tenant in data.keys():
       print(data.keys())
       print(tenant)
       my_struct = data[tenant]
       countdict = my_struct.count
       print(countdict.keys())
       for key in countdict.keys():
          print(countdict[key])
          print(key)
      
  except Exception as e:
    print ("Ecountered an exception", str(e))

if __name__ == "__main__":
  parse_file()
