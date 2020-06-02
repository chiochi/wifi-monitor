from flask import Flask,render_template,request,redirect,url_for
from flask import * 
from pysnmp.hlapi import *
import pyrebase
import datetime
import time
from collections import OrderedDict


config = {
    'apiKey': "AIzaSyBNadP2zErsdPyF68FVy00EmfNY9iB_XV4",
    'authDomain': "test1-593bb.firebaseapp.com",
    'databaseURL': "https://test1-593bb.firebaseio.com",
    'projectId': "test1-593bb",
    'storageBucket': "test1-593bb.appspot.com",
    'messagingSenderId': "457630935702",
    'appId': "1:457630935702:web:b489bc53a51c19a5"
    }
firebase = pyrebase.initialize_app(config)
db = firebase.database()
date = datetime.date.today()
date = str(date)
time = time.strftime("%H"+":"+"%M"+":"+"%S")
time = str(time)
print('Sent to database .....')
communityName = 'public' # SNMP Community RO / RW
ipaddress1 = '10.64.1.10'
ipaddress2 = '10.64.1.13'

result_client = []
dataclient_mac = []
dataclient_ip = []
dataclient_radio = []
dataclient_user = []
dataclient_ssid = []

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]
wlc1dl = [] 

#newname = input("Enter Newname : ") 
def snmpget_wlc1(oid):
    from pysnmp.entity.rfc3413.oneliner import cmdgen
    errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
        CommunityData(communityName),
        UdpTransportTarget((ipaddress1, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
        ) 
    )
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1] or '?'))
        else:
            for name, val in varBinds:
                #print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                return val.prettyPrint()
def snmpget_wlc2(oid):
    from pysnmp.entity.rfc3413.oneliner import cmdgen
    errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
        CommunityData(communityName),
        UdpTransportTarget((ipaddress2, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
        ) 
    )
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1] or '?'))
        else:
            for name, val in varBinds:
                #print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                return val.prettyPrint()
def get_data_client_wlc1(oid) :
    c = online_user1*7
    i = 1 
    count = 1
    while i < c+1 :
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        errorIndication, errorStatus, errorIndex, varBinds = next(
            nextCmd(SnmpEngine(),
                CommunityData(communityName),
                UdpTransportTarget((ipaddress1, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
                ) 
        )
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1] or '?'))
            else:
                for name, val in varBinds:
                    #print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                    #print('Number %d: ' % i,val)
                    n = name.prettyPrint()
                    n = str(n)
                    r = val.prettyPrint()
                    r = str(r)
                    count = str(count)
                    n1 = n[38]

                    if online_user1 == 0 : 
                        #data = {"Client": "No client"}
                        #db.child("Client").child(date).child("WLC1").child("cl_"+count).update(data)
                        dataclient = r 
                        print ("dataclient ",i,": ",r)
                        #return dataclient
                    elif n1 == '1' :
                        #data = {"Mac_Address": r}
                        #db.child("Client").child(date).child("WLC1").child("cl_"+count).update(data)
                        dataclient = r
                        dataclient_mac.append(dataclient) 
                        print ("dataclient ",i,": ",r)
                        result_client.append({"mac":[dataclient_mac]})
                        #return dataclient
                    elif n1 == '2' :
                        #data = {"Ip_Address": r}
                        #db.child("Client").child(date).child("WLC1").child("cl_"+count).update(data)
                        dataclient = r
                        dataclient_ip.append(dataclient) 
                        print ("dataclient ",i,": ",r)
                        result_client.append({"ip":[dataclient_ip]})
                        #return dataclient
                    elif n1 == '3' :
                        if r == "" : r = "Unknow"  
                        #data = {"Username": r}
                        #db.child("Client").child(date).child("WLC1").child("cl_"+count).update(data)
                        dataclient = r
                        dataclient_user.append(dataclient) 
                        print ("dataclient ",i,": ",r)
                        result_client.append({"user":[dataclient_user]})
                        #return dataclient
                    elif n1 == '4' : 
                        #data = {"Radio_AP_Connect": r}
                        #db.child("Client").child(date).child("WLC1").child("cl_"+count).update(data)
                        dataclient = r
                        dataclient_radio.append(dataclient) 
                        print ("dataclient ",i,": ",r)
                        result_client.append({"radio":[dataclient_radio]})
                        #return dataclient
                    elif n1 == '7' : 
                        #data = {"SSID_Connect": r}
                        #db.child("Client").child(date).child("WLC1").child("cl_"+count).update(data)
                        dataclient = r
                        dataclient_ssid.append(dataclient) 
                        print ("dataclient ",i,": ",r)
                        result_client.append({"ssid":[dataclient_ssid]})
                        #return dataclient
                    count = int(count)
                    count += 1
                    if count > online_user1 : count = 1 
                    if i == online_user1*7 : 
                        result_client.extend(dataclient_mac)
                        print("result_client : ",dataclient_mac,dataclient_ip,dataclient_user,dataclient_radio,dataclient_ssid)
                        return result_client
                            
                    oid = name
                    i += 1
def get_cl_username_wlc1(oid) :
    c = online_user1
    i = 1
    count = 1 
    while i <= c :
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        errorIndication, errorStatus, errorIndex, varBinds = next(
            nextCmd(SnmpEngine(),
                CommunityData(communityName),
                UdpTransportTarget((ipaddress1, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
                ) 
        )
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1] or '?'))
            else:
                for name, val in varBinds:
                    r = val.prettyPrint()
                    r = str(r)
                    count = str(count)
                    #print(count,name, r)
                    if r == "" : r = "Unknow"  
                    #data = {"Username": r}
                    #db.child("Client").child(date).child("WLC1").child("cl_"+count).update(data)
                    count = int(count)
                    count += 1
                    oid = name
                    i += 1
def set_data(oid,newname):
    g = setCmd(SnmpEngine(),
        CommunityData('private'),
        UdpTransportTarget((ipaddress1, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid), newname)
    )
    next(g)

app = Flask(__name__)
@app.route('/')
@app.route('/dashboard')
def dash():
    K1 = []
    D1 = []
    U1 = []
    D2 = []
    U2 = [] 
    
    wlc1_ap_join = db.child("WLC").child(date).child("WLC1_AP_Join").get()
    wlc1_online_user = db.child("WLC").child(date).child("WLC1_Online_User").get()
    wlc1_download = db.child("WLC").child(date).child("WLC1_Download").get()
    wlc1_upload = db.child("WLC").child(date).child("WLC1_Upload").get()
    #wlc1_uptime = db.child("WLC").child(date).child("WLC1_Uptime").get()

    wlc2_ap_join = db.child("WLC").child(date).child("WLC2_AP_Join").get()
    wlc2_online_user = db.child("WLC").child(date).child("WLC2_Online_User").get()
    wlc2_download = db.child("WLC").child(date).child("WLC2_Download").get()
    wlc2_upload = db.child("WLC").child(date).child("WLC2_Upload").get()
    #wlc2_uptime = db.child("WLC").child(date).child("WLC2_Uptime").get()

    all_wlc = db.child("WLC").get()
    for data in all_wlc.each():
        wlc1_download = db.child("WLC").child(data.key()).child("WLC1_Download").get()
        
        wlc1_upload = db.child("WLC").child(data.key()).child("WLC1_Upload").get()

        wlc2_download = db.child("WLC").child(data.key()).child("WLC2_Download").get()
        wlc2_upload = db.child("WLC").child(data.key()).child("WLC2_Upload").get()

        D1.append(wlc1_download.val())
        U1.append(wlc1_upload.val())
        D2.append(wlc2_download.val())
        U2.append(wlc2_upload.val())
        K1.append(data.key())
    date1 = K1
    download1 = D1
    upload1 = U1
    download2 = D2
    upload2 = U2
    
    max1 = 100
    #if int(wlc2_download) >= 100 : max1 = 1000 

    return render_template('dashboard.html',
    wlc1_ap_join=str(wlc1_ap_join.val()),
    wlc1_online_user=str(wlc1_online_user.val()),
    wlc1_download=str(wlc1_download.val()),
    wlc1_upload=str(wlc1_upload.val()),
    #wlc1_uptime=str(wlc1_uptime.val()),

    wlc2_ap_join=str(wlc2_ap_join.val()),
    wlc2_online_user=str(wlc2_online_user.val()),
    wlc2_download=str(wlc2_download.val()),
    wlc2_upload=str(wlc2_upload.val()),
    #wlc2_uptime=str(wlc2_uptime.val())
    max=1000,max1=max1,labels=date1,
    download1=download1, upload1=upload1,
    download2=download2, upload2=upload2)

@app.route('/show')
def show():
    K = []
    D = [] 
    all_wlc = db.child("WLC").get()
    for data in all_wlc.each():
        wlc1_download = db.child("WLC").child(data.key()).child("WLC1_Download").limit_to_first(5).get()
        D.append(wlc1_download.val())
        K.append(data.key())
        
    print("K : ", K)
    print("D : ", D)

    line_labels = K
    line_values = D
    return render_template('show.html', max=1000, labels=line_labels, values=line_values,data=D)
    #return render_template('show.html',data=D)

@app.route('/client')
def client():
    cl_name = db.child("Client").child(date).child("WLC1").get()
    K = []
    cl_name1 = [] 
    cl_mac1 = []
    cl_ip1 = []
    cl_user1 = []
    online_user1
    for data in cl_name.each():
        wlc1_cl_Mac = db.child("Client").child(date).child("WLC1").child(data.key()).child("Mac_Address").get()
        wlc1_cl_Ip = db.child("Client").child(date).child("WLC1").child(data.key()).child("Ip_Address").get()
        wlc1_cl_User = db.child("Client").child(date).child("WLC1").child(data.key()).child("Username").get()
        cl_mac1.append(wlc1_cl_Mac.val())
        cl_ip1.append(wlc1_cl_Ip.val())
        cl_user1.append(wlc1_cl_User.val())
        

        K.append(data.key())
    print("K : ", K)
    print("cl_name1 : ", cl_name1)
    print("online user :", online_user1)
    return render_template('client.html',K=K,wlc1_cl_Mac=cl_mac1,wlc1_cl_Ip=cl_ip1,wlc1_cl_User=cl_user1)

@app.route('/manage')
def manage():
    wlcname = snmpget_wlc1('.1.3.6.1.4.1.14179.2.1.4.1.9.136.247.191.76.121.19')
    wlcname = str(wlcname)

    #username = get_cl_username_wlc1('1.3.6.1.4.1.14179.2.1.4.1.3')
    

    return render_template('manage.html',wlcname=wlcname)

@app.route('/edit',methods=['POST'])
def edit():
    if request.method=="POST":
        newname = request.form['newname']
        #set_data('.1.3.6.1.2.1.1.5.0',newname)
        newname = int(newname)
        print("newname : ", newname, type(newname))
        set_data('.1.3.6.1.4.1.14179.2.1.4.1.9.136.247.191.76.121.19',newname)
        
        return redirect(url_for('manage'))

@app.route('/location')
def location():
    """K = []
    D = []
    all_ap = db.child("AccessPoint").get()
    for data in all_ap.each():

        count = 1
        count = str(count)
        wlc1_ap_Name = db.child("AccessPoint").child(data.key()).child("WLC1").child("ap_"+count).child("Name").get()
        D.append(wlc1_ap_Name.val())
        K.append(data.key())
        #print("KEY : ", data.key())
        #print("wcl1_download : ", wcl1_download.val())
        count = int(count)
        count += 1
    all_ap_name = db.child("AccessPoint").child(date).child("WLC1").get()
    K = []
    Name1 = [] 
    for data in all_ap_name.each():
        wlc1_ap_Name = db.child("AccessPoint").child(date).child("WLC1").child(data.key()).child("Name").get()
        Name1.append(wlc1_ap_Name.val())
        K.append(data.key())
    #print("K : ", K)
    #print("D : ", Name1)
    return render_template('location.html',wlc1_ap_name=Name1)"""
    return render_template('location.html')

#@app.route('/ap')
#def ap():
 #   all_ap_name = db.child("AccessPoint").child(date).child("WLC1").get()
  #  K = []
   # Name1 = [] 
    #for data in all_ap_name.each():
     #   wlc1_ap_Name = db.child("AccessPoint").child(date).child("WLC1").child(data.key()).child("Name").get()
      #  Name1.append(wlc1_ap_Name.val())
       # K.append(data.key())
       
    #print("K : ", K)
    #print("D : ", Name1)
    #return render_template('ap.html',wlc1_ap_name=Name1)

@app.route('/accesspoint',methods=['POST'])
def accesspoint():
    K1 = []
    RX1 = []
    
    if request.method=="POST" : 
        key = request.form['key']
        print("KEY = ", key)
        wlc1_ap_Name = db.child("AccessPoint").child(date).child("WLC1").child(key).child("Name").get().val()
        wlc1_ap_Ip = db.child("AccessPoint").child(date).child("WLC1").child(key).child("Ip_Address").get().val()
        wlc1_ap_Mac = db.child("AccessPoint").child(date).child("WLC1").child(key).child("Mac_Address").get().val()

        wlc1_ap_interface1 = db.child("AccessPoint").child(date).child("WLC1").child(key).child("Interface1").child("Name").get().val()

        all_ap = db.child("AccessPoint").get()
        for data in all_ap.each():
            wlc1_ap_Rx1 = db.child("AccessPoint").child(data.key()).child("WLC1").child(key).child("Interface1").child("rx").get()
            
            #wlc1_upload = db.child("WLC").child(data.key()).child("WLC1_Upload").get()

            RX1.append(wlc1_ap_Rx1.val())
            #U1.append(wlc1_upload.val())
            K1.append(data.key())
        date1 = K1
        rx1 = RX1
        print(rx1)
        print(date1)
        #upload1 = U1
        #download2 = D2
        #upload2 = U2

    return render_template('accesspoint.html',
    wlc1_ap_Name=wlc1_ap_Name,
    wlc1_ap_Ip=wlc1_ap_Ip,
    wlc1_ap_Mac=wlc1_ap_Mac,
    wlc1_ap_interface1=wlc1_ap_interface1,
    max=10,date1=date1,
    rx1=rx1)
def ap1():
    
    return render_template('ap/ap1.html')

online_user1 = snmpget_wlc1('1.3.6.1.4.1.9.9.618.1.8.12.0')
online_user1 = int(online_user1)
#get_data_client_wlc1('.1.3.6.1.4.1.14179.2.1.1.1.100.6')

if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0', port=8000)
