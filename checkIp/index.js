const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");

const app = express();
const PORT = 4000;

app.use(cors());
app.use(express.json());

function setStaticIP(ip, subnet = "255.255.255.0", gateway = "") {
  return new Promise((resolve, reject) => {
    const interfaceName = "Ethernet"; // أو "Wi-Fi" حسب جهازك
    const command = `wmic nicconfig where Description='Realtek PCIe GBE Family Controller' call EnableStatic ("192.168.40.254"), ("255.255.255.0")`;
    exec(command, { windowsHide: true }, (error, stdout, stderr) => {
      if (error) return reject(stderr);
      resolve(stdout);
    });
  });
}

app.post("/check-ips", async (req, res) => {
  const ips = req.body.ips || [];
  if (ips.length === 0) return res.status(400).json({ error: "No IPs provided" });

  // استخرج أول IP وحدد الشبكة
  try {
    // 1. تغيير IP الجهاز
    await setStaticIP(newDeviceIP);

    // 2. فحص IPات
    const checkIp = (ip) =>
      new Promise((resolve) => {
        exec(`ping -n 1 -w 200 ${ip}`, (error, stdout) => {
          const alive = stdout.includes("TTL=");
          resolve({ ip, alive });
        });
      });

    const results = await Promise.all(ips.map(checkIp));
    const deadIps = results.filter(r => !r.alive).map(r => r.ip);
    res.json({ deadIps });
  } catch (error) {
    res.status(500).json({ error: "Failed to change IP or check connectivity", details: error.toString() });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
