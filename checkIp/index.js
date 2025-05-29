const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");

const app = express();
const PORT = 4000;

app.use(cors());
app.use(express.json());

function setStaticIP(ip, subnet = "255.255.255.0", gateway = "") {
  return new Promise((resolve, reject) => {
    const interfaceAlias = "Ethernet"; // أو "Wi-Fi" حسب جهازك

    // إعداد جزء البوابة إن وُجد
    const gatewayPart = gateway ? `-DefaultGateway ${gateway}` : "";

    const command = `powershell -Command "New-NetIPAddress -InterfaceAlias '${interfaceAlias}' -IPAddress '${ip}' -PrefixLength 24 ${gatewayPart} -ErrorAction Stop"`;

    exec(command, { windowsHide: true }, (error, stdout, stderr) => {
      if (error) return reject(stderr || error.message);
      resolve("تم تعيين IP ثابت بنجاح");
    });
  });
}


app.post("/check-raqaa", async (req, res) => {
  const ips = req.body.ips || [];

  if (ips.length === 0) {
    return res.status(400).json({ error: "No IPs provided" });
  }

  try {
    // تعيين IP ثابت
    await setStaticIP("192.166.168.254");

    // اختبار الاتصال بكل IP
    const results = await Promise.all(
      ips.map(
        (ip) =>
          new Promise((resolve) => {
            exec(`ping -n 1 -w 200 ${ip}`, (error, stdout) => {
              const alive = stdout.includes("TTL=");
              resolve({ ip, alive });
            });
          })
      )
    );

    // تصفية الإيبيهات المعطّلة فقط
    const inactiveIPs = results.filter(result => !result.alive);

    res.json({ inactive: inactiveIPs });
  } catch (err) {
    res.status(500).json({ error: "حدث خطأ أثناء التحقق", details: err });
  }
});
app.post("/check-kobani", async (req, res) => {
  const ips = req.body.ips || [];

  if (ips.length === 0) {
    return res.status(400).json({ error: "No IPs provided" });
  }

  try {
    // تعيين IP ثابت
    await setStaticIP("192.166.163.254");

    // اختبار الاتصال بكل IP
    const results = await Promise.all(
      ips.map(
        (ip) =>
          new Promise((resolve) => {
            exec(`ping -n 1 -w 200 ${ip}`, (error, stdout) => {
              const alive = stdout.includes("TTL=");
              resolve({ ip, alive });
            });
          })
      )
    );

    // تصفية الإيبيهات المعطّلة فقط
    const inactiveIPs = results.filter(result => !result.alive);

    res.json({ inactive: inactiveIPs });
  } catch (err) {
    res.status(500).json({ error: "حدث خطأ أثناء التحقق", details: err });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
