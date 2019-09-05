import adbutils
import io

import time

class AdbClient():
    def __init__(self, proto_path, adb_host, adb_port, adb_address):
        self.adb = adbutils.AdbClient(host=adb_host, port=adb_port)
        if adb_address is not "":
            if ":" in adb_address:
                print(self.adb.connect(adb_address))
                time.sleep(3)
                self.device = self.adb.device() 
            else:
                self.device = self.adb.device(serial=adb_address)
        else:
            self.device = self.adb.device()
        self.proto_path = proto_path
        
    def pull_proto(self):
        print(self.device.shell(["ps", "-A", "|", "grep", "com.google.android.apps.chromecast.app", "|", "awk", "{print \$2}", "|", "su", "-c", "xargs kill"]))
        print(self.device.shell(["monkey", "--pct-syskeys", "0", "-p", "com.google.android.apps.chromecast.app", "-c", "android.intent.category.LAUNCHER", "1"]))
        print("Sleeping...")
        time.sleep(30)
        print(self.device.shell(["su", "-c", "cp /data/data/com.google.android.apps.chromecast.app/files/home_graph*.proto /sdcard/home_graph.proto"]))
        self.device.sync.pull("/sdcard/home_graph.proto", self.proto_path)
        return io.FileIO(self.proto_path)

if __name__ == "__main__":
    client = AdbClient("home_graph.proto")
    print(client.pull_proto().readall())
