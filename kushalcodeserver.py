try:
    tunnelName = "kushalcodeserver"
    # importing packages
    import subprocess
    import requests
    import time
    from datetime import datetime
    from dateutil.tz import gettz


    def CheckWebsiteUp(websiteName):
        try:
            statusCode = requests.get(websiteName).status_code
            if statusCode == 200: return("Up")
            else: return("Down")   
        except Exception:
            return("Down")


    while True:
        dtobj = datetime.now(tz=gettz('Asia/Kolkata'))
        print(f'''
Date: {dtobj.day}/{dtobj.month}/{dtobj.year}
Time: {dtobj.strftime("%r")}
 
CHECKING IF WEBSITES ARE UP....''')


        codeserverStatus = CheckWebsiteUp("http://localhost:8080")
        print("Code Server is ", codeserverStatus)

        tunnelStatus = CheckWebsiteUp(f"https://{tunnelName}.loca.lt")
        print("Tunnel is ", tunnelStatus, "\n\n")


        while codeserverStatus == "Down":
            print("Starting code-server...")
            subprocess.Popen("cd ~/code-server-3.10.2-linux-arm64/ && export PASSWORD='Kushal#07' && ./code-server", shell= True)
            time.sleep(40)
            codeserverStatus = CheckWebsiteUp("http://localhost:8080")
            print("Code Server is ", codeserverStatus)


        while tunnelStatus == "Down":
            print("Starting tunnel ...")
            subprocess.Popen(f"lt --port 8080 --subdomain {tunnelName}", shell= True)
            time.sleep(40)
            tunnelStatus = CheckWebsiteUp(f"https://{tunnelName}.loca.lt")
            print("Tunnel is ", tunnelStatus, "\n\n")

        time.sleep(120)

except KeyboardInterrupt:
    print(f"\nThank you for using {tunnelName} status checker")
