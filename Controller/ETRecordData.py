#------------------------------------------------------------------------------
#   File: ETRecordData.py
#   Desc: Defines the entry point for the Python Eye Tracker Sample Application - 
#         Send TCP Command to Eye Tracker to record data.
#	Change History:
#      09/28/2020: Created.
#
#  Copyright © 2016 - 2022 Argus Science, LLC.  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without modification,
#  are permitted provided that the following conditions are met:
#
#  •	Redistributions of source code must retain the above copyright notice,
#		this list of conditions and the following disclaimer.
#  •	Redistributions in binary form must reproduce the above copyright notice,
#		this list of conditions and the following disclaimer in the documentation
#		and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
#  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
#  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#  OF THE POSSIBILITY OF SUCH DAMAGE.
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Import
#------------------------------------------------------------------------------
import sys
import msvcrt
import socket


#------------------------------------------------------------------------------
# Definitions
#------------------------------------------------------------------------------
# Command
CMD_START_DATAFILE_RECORDING			=   0x0001
CMD_STOP_DATAFILE_RECORDING				=   0x0002
CMD_OPEN_DATAFILE						=   0x0003
CMD_CLOSE_DATAFILE						=   0x0004
CMD_SET_XDAT                            =   0x0005
CMD_SET_DATAFILE_NAME					=   0x0006


#------------------------------------------------------------------------------
# CalCheckSum:  Calculate Check Sum of Buffer
#    Buf		-	Buffer array
#    BufSize	-	Buffer Size
#    Return		-	Check sum of buffer
#------------------------------------------------------------------------------
def CalCheckSum(Buf, BufSize):
    # Initialize Check Sum    
    CheckSum = 0

	# Calculate Sum of Buffer
    for i in range(0, BufSize):
        CheckSum += Buf[i]

    # Calculate Check Sum in Byte
    CheckSum = (~CheckSum + 1) & 0xFF 

    # Return result
    return CheckSum


#------------------------------------------------------------------------------
# SendETCmd:    Send Command to Eye Tracker
#    CSocket    -   Command Socket connected to Eye Tracker
#    Cmd		-	Command
#    Arg		-	Command Argument
#    Return		-	True if succeeded, False if failed
#------------------------------------------------------------------------------
def SendETCmd(CSocket, Cmd, Arg):
    # Convert Command to byte array in little endian
    CmdArr = Cmd.to_bytes(4, "little")

    # Convert Argument to byte array in little endian
    ArgArr = Arg.to_bytes(4, "little")

    # Set up Command Structure, please check details with Argus Network Protocol
    CmdStruc = [0x53, 0x47, 0x41, 0x20, 20, 0, 0, 0, CmdArr[0], CmdArr[1], CmdArr[2], CmdArr[3], 0, 0, 0, 0, ArgArr[0], ArgArr[1], ArgArr[2], ArgArr[3]]

    # Calculate Check Sum of Command Structure
    CSum = CalCheckSum(bytearray(CmdStruc), 20)
    
    # Convert Check Sum to byte array
    CSumArr = CSum.to_bytes(4, "little")
    
    # Updat command structure checksum
    CmdStruc[12] = CSumArr[0]

    # Try to send command
    try:
        CSocket.send(bytearray(CmdStruc))
    except Exception as e:
        # Return False if failed
        return False

    # Return True if succeeded
    return True


#------------------------------------------------------------------------------
# SendETCmdStr:     Send Command with String as Argument to Eye Tracker
#    CSocket    -   Command Socket connected to Eye Tracker
#    Cmd		-	Command
#    ArgStr	    -	Command String Argument
#    Return		-	True if succeeded, False if failed
#------------------------------------------------------------------------------
def SendETCmdStr(CSocket, Cmd, ArgStr):
    # Convert Command to byte array in little endian
    CmdArr = Cmd.to_bytes(4, "little")

    # Convert Argument String to bytearray
    ArgArr = bytearray(ArgStr, 'utf-8') + bytearray(1)

    # Calculate Command Message Size
    MsgSize = len(ArgArr) + 16

    # Initial Checksum
    CSum = 0

    # Set up Command Structure, please check details with Argus Network Protocol
    # Byte  0 -  3: Argus Signature
    # Byte  4 -  7: Command Structure Size
    # Byte  8 - 11: Command
    # Byte 12 - 15: Checksum
    # Byte 16 -   : Argument String
    CmdStrucArr = (0x20414753).to_bytes(4, "little") + MsgSize.to_bytes(4, "little") + CmdArr + CSum.to_bytes(4, "little") + ArgArr

    # Calculate Check Sum of Command Structure
    CSum = CalCheckSum(CmdStrucArr, len(CmdStrucArr))
    
    # Updat command structure checksum
    CmdStrucArr = (0x20414753).to_bytes(4, "little") + MsgSize.to_bytes(4, "little") + CmdArr + CSum.to_bytes(4, "little") + ArgArr

    # Try to send command
    try:
        CSocket.send(CmdStrucArr)
    except Exception as e:
        # Return False if failed
        return False

    # Return True if succeeded
    return True


#------------------------------------------------------------------------------
# Main entry point for the Eye Tracker Sample Application
#    argv[1]    -   Eye Tracker Host IP Address
#    argv[2]    -   Eye Tracker Host IP Port Number
#    argv[3]	-	Data File Name
#    Return		-	None
#------------------------------------------------------------------------------
# Get number of arguments
# NumArg = len(sys.argv)

# # Check whether it's correct
# if NumArg != 4:
#     # Show instruction message if number of arguments is not right
#     print("Please use command: py ETRecordData.py IPAddress IPPort FileName\n")

#     # Quit
#     sys.exit()

# Get Eye Tracker Host IP Address to connect
# HostIPAddr = sys.argv[1]
HostIPAddr = '146.186.228.86'
# Get Eye Trackt Port Number to connect
# HostPortNum = int(sys.argv[2])
HostPortNum = 51000
# Get Data File Name String
# FNameStr = sys.argv[3]
FNameStr = 'eye.eyd'

# Create TCP socket to connect to host
CmdSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set TCP_NODELAY
CmdSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

# Set time out to 10 seconds
CmdSocket.settimeout(10.0)

# Initialize Network Connected Flag
FlagConnected = True

# Try to connect to Eye Tracker Host
try:
    # Connect to host
    CmdSocket.connect((HostIPAddr, HostPortNum))

# Failed
except Exception as e:
    # Change Connection Flag to False if failed
    FlagConnected = False

# Send command to Set Data File Name if connected
if (FlagConnected):
    FlagConnected = SendETCmdStr(CmdSocket, CMD_SET_DATAFILE_NAME, FNameStr)

# Send command to Open Data File if connected
if (FlagConnected):
    FlagConnected = SendETCmd(CmdSocket, CMD_OPEN_DATAFILE, 0)

# Send command to Start Data File Recording if connected
if (FlagConnected):
    FlagConnected = SendETCmd(CmdSocket, CMD_START_DATAFILE_RECORDING, 0)

# Check result
if (FlagConnected):
    # Show message
    print(f"Start to record Host({HostIPAddr}:{HostPortNum}) eye data into file: {FNameStr}... (Press 'Esc' to stop recording and quit!)\n")
# Quit if failed to build the connection
if (FlagConnected == False):
    # Show message
    print(f"Failed to connect {HostIPAddr} at port {HostPortNum}!")
    print("Please double check the IP Address and Port Number that Eye Tracker is listening!\n")
    
    # Quit
    sys.exit()

while (FlagConnected):

    # Quit if ESC Key is pressed
    if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():
        # Send command to Stop Data File Recording if connected
        if (FlagConnected):
            FlagConnected = SendETCmd(CmdSocket, CMD_STOP_DATAFILE_RECORDING, 0)

        # Send command to Close Data File if connected
        if (FlagConnected):
            FlagConnected = SendETCmd(CmdSocket, CMD_CLOSE_DATAFILE, 0)
        
        # Change Flag to quit
        FlagConnected = False
    
# Show message
print(f"Record Host({HostIPAddr}:{HostPortNum}) eye data into file: {FNameStr} successfully\n")

# Quit
sys.exit()
