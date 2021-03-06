import mqttConnect
import subprocess
import pwdCrypt.crypt as crypt

def handle_cmd(cmd):
    process = subprocess.Popen(cmd, shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
    out, err = process.communicate()

    if (err.decode().strip() == ""): # No error message
        if ("0" in out.decode().strip()): # output is display_power=0
            return "OFF"
        else:
            return "ON"
    else:
        # TODO: Handle error
        return "OFF"

def on_action():
    """
    When the request is ON, turn on the display
    """
    cmd = "vcgencmd display_power 1"
    return(handle_cmd(cmd))

def off_action():
    """
    When the request is OFF, turn off the display
    """
    cmd = "vcgencmd display_power 0"
    return(handle_cmd(cmd))

def get_status():
    """
    Get status, used at startup
    """
    cmd = "vcgencmd display_power"
    return(handle_cmd(cmd))

if __name__ == "__main__":
    # Get info from config.json
    crypt = crypt.pwdCrypt()
    userData = crypt.get_user_info()

    # Add actions definition
    userData["onAction"] = on_action
    userData["offAction"] = off_action
    userData["getStatus"] = get_status

    # Call MAIN of mqttConnect
    mqttConnect.main(userData)