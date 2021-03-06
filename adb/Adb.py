# Author: Chema Garcia (aka sch3m4)
# Contact: chema@safetybits.net | @sch3m4 | http://safetybits.net/contact 
# Homepage: http://safetybits.net
# Project Site: http://github.com/sch3m4/pyadb

import sys
import os
import traceback
import subprocess

PYADB_VERSION = "1.1.0"


class ADB(object):

    __adb_path = None
    __output = None
    __error = None
    __return = 0
    __devices = []
    __target = None

    # reboot modes
    REBOOT_RECOVERY = 1
    REBOOT_BOOTLOADER = 2
    
    # default TCP/IP port
    DEFAULT_TCP_PORT = 5555
    # default TCP/IP host
    DEFAULT_TCP_HOST = "localhost"
    
    def pyadb_version(self):
        return PYADB_VERSION

    def __init__(self, adb_path=None):
        self.__adb_path = adb_path

    def __clean(self):
        self.__output = None
        self.__error = None
        self.__return = 0

    def __parse_output__(self,outstr):
        ret = None

        if(len(outstr) > 0):
            ret = outstr.splitlines()

        return ret

    def __build_command__(self,cmd):
        ret = None

        if self.__devices is not None and len(self.__devices) > 1 and self.__target is None:
            self.__error = "Must set target device first"
            self.__return = 1
            return ret

        # Modified function to directly return command set for Popen
        #
        # Unfortunately, there is something odd going on and the argument list is not being properly
        # converted to a string on the windows 7 test systems.  To accomodate, this block explitely
        # detects windows vs. non-windows and builds the OS dependent command output
        #
        # Command in 'list' format: Thanks to Gil Rozenberg for reporting the issue
        #
        if sys.platform.startswith('win'):
            ret = self.__adb_path + " "
            if( self.__target is not None ):
                ret += "-s " + self.__target + " "
            if type(cmd) == type([]):
                ret += ' '.join(cmd)
            else:
                ret += cmd
        else:
            ret = [self.__adb_path]
            if( self.__target is not None ):
                ret += ["-s", self.__target]
                
            if type(cmd) == type([]):
                for i in cmd:
                    ret.append(i)
            else:
                ret += [cmd]

        return ret
    
    def get_output(self):
        return self.__output
    
    def get_error(self):
        return self.__error

    def get_return_code(self):
        return self.__return

    def lastFailed(self):
        """
        Did the last command fail?
        """
        if self.__output is None and self.__error is not None and self.__return:
            return True
        return False

    def run_cmd(self,cmd):
        """
        Runs a command by using adb tool ($ adb <cmd>)
        """
        self.__clean()

        if self.__adb_path is None:
            self.__error = "ADB path not set"
            self.__return = 1
            return
        
        # For compat of windows
        cmd_list = self.__build_command__(cmd)

        try:
            adb_proc = subprocess.Popen(cmd_list, stdin = subprocess.PIPE, \
                                  stdout = subprocess.PIPE, \
                                  stderr = subprocess.PIPE, shell = False)
            (self.__output, self.__error) = adb_proc.communicate()
            self.__return = adb_proc.returncode

            if( len(self.__output) == 0 ):
                self.__output = ''

            if( len(self.__error) == 0 ):
                self.__error = ''

        except:
            print(traceback.format_exc())

        return

    def get_version(self):
        """
        Returns ADB tool version
        adb version
        """
        self.run_cmd("version")
        try:
            ret = self.__output.split()[-1:][0]
        except:
            ret = None
        return ret

    def check_path(self):
        """
        Intuitive way to verify the ADB path
        """
        if self.get_version() is None:
            return False
        return True

    def set_adb_path(self,adb_path):
        """
        Sets ADB tool absolute path
        """
        if os.path.isfile(adb_path) is False:
            return False
        self.__adb_path = adb_path
        return True

    def get_adb_path(self):
        """
        Returns ADB tool path
        """
        return self.__adb_path

    def start_server(self):
        """
        Starts ADB server
        adb start-server
        """
        self.__clean()
        self.run_cmd('start-server')
        return self.__output

    def kill_server(self):
        """
        Kills ADB server
        adb kill-server
        """
        self.__clean()
        self.run_cmd('kill-server')

    def test_wifi_state(self):
        """
        Test Wifi State
        """
        self.__clean()
        self.shell_command('cat sys/class/net/wlan0/address')
        if self.__output is not None and len(self.__output) > 0:
            return self.__output
        return 2

    def test_power(self):
        """
        Test Power State
        """
        self.__clean()
        self.shell_command('cat /sys/devices/soc0/tps65185_sensor.22/temp_input')
        value = self.__output
        if len(self.__error) == 0 and len(value) > 0:
            value = int(value.strip())
            if value < 50 and value > 0:
                self.shell_command('cat /sys/class/power_supply/battery/voltage_now')
                if len(self.__error) == 0:
                    value = int(self.__output.strip())
                    if value > 3500 and value < 4250:
                        return 1
                    else:
                        return 2
            else:
                return 2
        else:
            return 2

    def test_back_light(self):
        """
        Test BackLight State
        """
        self.__clean()
        self.shell_command('echo 140 > /sys/class/backlight/pwm-backlight.0/brightness')
        self.shell_command('cat /sys/class/backlight/pwm-backlight.0/actual_brightness')
        if self.__output is not None and len(self.__output) > 0:
            if self.__output == '140\r\n':
                return 1
        return 2

    def test_audio(self):
        """
        Test Audio State
        """
        self.__clean()
        self.shell_command('cat /sys/class/sound/pcmC0D0c/device/id')
        self.shell_command('cat /sys/class/sound/pcmC0D0p/device/id')
        if self.__output is not None and len(self.__output) > 0:
            return 1
        return 2

    def test_sensor(self):
        self.__clean()
        self.shell_command('cat sys/bus/iio/devices/iio:device0/in_illuminance0_input')
        if self.__output is not None and len(self.__output) > 0:
            return 1
        return 2

    def test_record(self):
        """
        Test Record State
        """
        self.__clean()
        self.run_cmd('remount')
        self.push_local_file('adb/record', '/system/bin/')
        self.shell_command('record')
        if self.__output is not None and len(self.__output) > 0:
            if self.__output == '100\r\n':
                return 1
        return 2

    def store_sn_data(self, sn_number):
        self.__clean()
        self.shell_command('echo "' +  str(sn_number) + '" > /data/sn_number')
        if self.__error is None:
            return 1
        return 2

    def restart_server(self):
        """
        Restarts ADB server
        """
        self.kill_server()
        return self.start_server()

    def restore_file(self,file_name):
        """
        Restore device contents from the <file> backup archive
        adb restore <file>
        """
        self.__clean()
        self.run_cmd(['restore' , file_name ])
        return self.__output

    def wait_for_device(self):
        """
        Blocks until device is online
        adb wait-for-device
        """
        self.__clean()
        self.run_cmd('wait-for-device')
        return self.__output

    def get_help(self):
        """
        Returns ADB help
        adb help
        """
        self.__clean()
        self.run_cmd('help')
        return self.__output

    def get_devices(self):
        """
        Returns a list of connected devices
        adb devices
        """
        error = 0
        self.run_cmd("devices")
        if self.__error is not None:
            return ''
        try:
            self.__devices = self.__output.partition('\n')[2].replace('device','').split()

            if self.__devices[1:] == ['no','permissions']:
                error = 2
                self.__devices = []
        except:
            self.__devices = []
            error = 1

        return (error,self.__devices)

    def set_target_device(self, device):
        """
        Select the device to work with
        """
        self.__clean()
        if device is None or not device in self.__devices:
            self.__error = 'Must get device list first'
            self.__return = 1
            return False
        self.__target = device
        return True

    def get_target_device(self):
        """
        Returns the selected device to work with
        """
        return self.__target

    def get_state(self):
        """
        Get ADB state
        adb get-state
        """
        self.__clean()
        self.run_cmd('get-state')
        return self.__output

    def get_serialno(self):
        """
        Get serialno from target device
        adb get-serialno
        """
        self.__clean()
        self.run_cmd('get-serialno')
        return self.__output

    def reboot_device(self,mode):
        """
        Reboot the target device
        adb reboot recovery/bootloader
        """
        self.__clean()
        if not mode in (self.REBOOT_RECOVERY,self.REBOOT_BOOTLOADER):
            self.__error = "mode must be REBOOT_RECOVERY/REBOOT_BOOTLOADER"
            self.__return = 1
            return self.__output
        self.run_cmd(["reboot", "%s" % "recovery" if mode == self.REBOOT_RECOVERY else "bootloader"])
        return self.__output

    def set_adb_root(self):
        """
        restarts the adbd daemon with root permissions
        adb root
        """
        self.__clean()
        self.run_cmd('root')
        return self.__output

    def set_system_rw(self):
        """
        Mounts /system as rw
        adb remount
        """
        self.__clean()
        self.run_cmd("remount")
        return self.__output

    def get_remote_file(self,remote,local):
        """
        Pulls a remote file
        adb pull remote local
        """
        self.__clean()
        self.run_cmd(['pull',remote , local] )

        if self.__error is not None and "bytes in" in self.__error:
            self.__output = self.__error
            self.__error = None

        return self.__output

    def push_local_file(self,local,remote):
        """
        Push a local file
        adb push local remote
        """
        self.__clean()
        self.run_cmd(['push',local,remote] )
        return self.__output

    def shell_command(self,cmd):
        """
        Executes a shell command
        adb shell <cmd>
        """
        self.__clean()
        self.run_cmd(['shell',cmd])
        return self.__output

    def listen_usb(self):
        """
        Restarts the adbd daemon listening on USB
        adb usb
        """
        self.__clean()
        self.run_cmd("usb")
        return self.__output

    def listen_tcp(self,port=DEFAULT_TCP_PORT):
        """
        Restarts the adbd daemon listening on the specified port
        adb tcpip <port>
        """
        self.__clean()
        self.run_cmd(['tcpip',port])
        return self.__output

    def get_bugreport(self):
        """
        Return all information from the device that should be included in a bug report
        adb bugreport
        """
        self.__clean()
        self.run_cmd("bugreport")
        return self.__output

    def get_jdwp(self):
        """
        List PIDs of processes hosting a JDWP transport
        adb jdwp
        """
        self.__clean()
        self.run_cmd("jdwp")
        return self.__output

    def get_logcat(self,lcfilter=""):
        """
        View device log
        adb logcat <filter>
        """
        self.__clean()
        self.run_cmd(['logcat',lcfilter])
        return self.__output

    def run_emulator(self,cmd=""):
        """
        Run emulator console command
        """
        self.__clean()
        self.run_cmd(['emu',cmd])
        return self.__output
    
    def connect_remote (self,host=DEFAULT_TCP_HOST,port=DEFAULT_TCP_PORT):
        """
        Connect to a device via TCP/IP
        adb connect host:port
        """
        self.__clean()
        self.run_cmd(['connect',"%s:%s" % ( host , port ) ] )
        return self.__output
    
    def disconnect_remote (self , host=DEFAULT_TCP_HOST , port=DEFAULT_TCP_PORT):
        """
        Disconnect from a TCP/IP device
        adb disconnect host:port
        """
        self.__clean()
        self.run_cmd(['disconnect',"%s:%s" % ( host , port ) ] )
        return self.__output
    
    def ppp_over_usb(self,tty=None,params=""):
        """
        Run PPP over USB
        adb ppp <tty> <params>
        """
        self.__clean()
        if tty is None:
            return self.__output
        
        cmd = ["ppp",tty]
        if params != "":
            cmd += params
            
        self.run_cmd(cmd)
        return self.__output

    def sync_directory(self,directory=""):
        """
        Copy host->device only if changed (-l means list but don't copy)
        adb sync <dir>
        """
        self.__clean()
        self.run_cmd(['sync',directory])
        return self.__output
    
    def forward_socket(self,local=None,remote=None):
        """
        Forward socket connections
        adb forward <local> <remote>
        """
        self.__clean()
        if local is None or remote is None:
            return self.__output
        self.run_cmd(['forward',local,remote])
        return self.__output


    def uninstall(self,package=None,keepdata=False):
        """
        Remove this app package from the device
        adb uninstall [-k] package
        """
        self.__clean()
        if package is None:
            return self.__output

        cmd = 'uninstall '
        if keepdata:
            cmd += '-k '
        cmd += package
        self.run_cmd(cmd.split())
        return self.__output

    def install(self,fwdlock=False,reinstall=False,sdcard=False,pkgapp=None):
        """
        Push this package file to the device and install it
        adb install [-l] [-r] [-s] <file>
        -l -> forward-lock the app
        -r -> reinstall the app, keeping its data
        -s -> install on sdcard instead of internal storage
        """

        self.__clean()
        if pkgapp is None:
            return self.__output
        
        cmd = "install "
        if fwdlock is True:
            cmd += "-l "
        if reinstall is True:
            cmd += "-r "
        if sdcard is True:
            cmd += "-s "
 
        cmd += pkgapp
        self.run_cmd(cmd.split())
        return self.__output

    def find_binary(self,name=None):
        """
        Look for a binary file on the device
        """
        
        self.shell_command(['which',name])
        
        if self.__output is None: # not found
            self.__error = "'%s' was not found" % name
        elif self.__output.strip() == "which: not found": # 'which' binary not available
            self.__output = None
            self.__error = "which binary not found"
        else:
            self.__output = self.__output.strip()

        return self.__output
