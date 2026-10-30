
import os

base_template = "templates/base.html"
if os.path.exists(base_template):
    with open(base_template, "r", encoding="utf-8") as f:
        content = f.read()

    # Inject timeout script before closing body tag if not already present
    timeout_script = """
    <!-- Session Inactivity Timeout (15 Minutes) -->
    <div id="idle-warning" style="display:none; position:fixed; top:20px; right:20px; background:#1a1a1a; color:#cfa76e; padding:15px 20px; border-radius:6px; box-shadow:0 4px 12px rgba(0,0,0,0.3); z-index:9999; font-size:14px; border:1px solid #cfa76e;">
        <strong>Security Notice:</strong> Inactivity timeout in <span id="countdown-timer" style="font-weight:bold; color:#fff;">15:00</span>.
    </div>
    <script>
        let idleSeconds = 0;
        const maxIdleTime = 900; // 15 minutes in seconds
        
        function resetTimer() {
            idleSeconds = 0;
            document.getElementById("idle-warning").style.display = "none";
        }

        // Listen for user activity
        window.onload = resetTimer;
        window.onmousemove = resetTimer;
        window.onkeypress = resetTimer;
        window.onclick = resetTimer;
        window.onscroll = resetTimer;

        setInterval(() => {
            idleSeconds++;
            let timeLeft = maxIdleTime - idleSeconds;
            
            if (timeLeft <= 60 && timeLeft > 0) {
                let mins = Math.floor(timeLeft / 60);
                let secs = timeLeft % 60;
                document.getElementById("countdown-timer").innerText = mins + ":" + (secs < 10 ? "0" : "") + secs;
                document.getElementById("idle-warning").style.display = "block";
            }
            
            if (timeLeft <= 0) {
                alert("Session expired due to inactivity for your security.");
                window.location.href = "/accounts/logout/";
            }
        }, 1000);
    </script>
    """

    if "idle-warning" not in content:
        content = content.replace("</body>", timeout_script + "\n</body>")
        with open(base_template, "w", encoding="utf-8") as f:
            f.write(content)
        print("Session timeout script successfully added to base template!")
else:
    print("Base template not found.")

