from pathlib import Path
import shutil
import subprocess

PREFIX = {
    "fan-dev": "fan",
    "gyy": "gyy",
    "haoze": "haoze",
    "jl_dev": "jl",
    "junteng_dev": "junteng",
    "junxian_dev": "junxian",
    "lueyang-dev": "lueyang",
    "lv": "lv",
    "ruige": "ruige",
    "wenshuo-dev": "wenshuo",
    "xiaochen_dev": "xiaochen",
    "yuxuan-dev": "yuxuan",
    "yuzhen-dev": "yuzhen",
    "zhaochen": "zhaochen",
}

TASKS = {
    "fan-dev": ["coupon-manager", "discount-calculator", "loyalty-program", "price-tracker"],
    "gyy": ["blog-engine", "cms-builder", "content-scheduler", "robots-handler", "social-publisher", "tag-manager"],
    "haoze": ["media-organizer", "streaming-service", "subtitle-generator", "video-trimmer"],
    "jl_dev": ["canvas-grade-automation", "customer-feedback-processor", "email-classification-system", "inventory-management", "pdf-report-generator"],
    "junteng_dev": ["booking-system", "calendar-sync", "contact-manager", "help-desk", "order-processor", "product-catalog", "reminder-service", "shipment-tracker"],
    "junxian_dev": ["qr-generator", "social-connector", "translation-api"],
    "lueyang-dev": ["activity-logger", "client-portal", "crm-system", "deal-manager", "email-campaign", "follow-up-reminder", "sales-pipeline", "territory-manager"],
    "lv": ["analytics-dashboard", "chat-bot", "feedback-collector", "personalization-service", "sentiment-analyzer", "survey-builder", "voice-processor"],
    "ruige": ["canvas-automation", "data-analytics", "expense-tracker", "file-manager", "log-analyzer", "web-crawler"],
    "wenshuo-dev": ["cache-optimizer", "image-processor", "scheduler", "search-engine"],
    "xiaochen_dev": ["backup-utility", "deployment-tool", "error-tracker", "health-monitor", "monitoring-agent", "security-scanner", "status-checker"],
    "yuxuan-dev": ["asset-optimizer", "content-manager", "network-analyzer", "sync-service", "task-scheduler"],
    "yuzhen-dev": ["alert-system", "data-validator", "form-builder", "invoice-generator", "payment-processor", "permission-manager"],
    "zhaochen": ["certificate-manager", "load-balancer", "storage-manager", "template-engine"],
}

def run(*args):
    subprocess.run(args, check=True)

root = Path("tasks/finalpool")
if root.exists():
    shutil.rmtree(root)
root.mkdir(parents=True)
files = 0
for branch, names in TASKS.items():
    run("git", "fetch", "--depth", "1", "origin", branch)
    for name in names:
        source = f"tasks/{PREFIX[branch]}/{name}"
        listing = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", "FETCH_HEAD", source], text=True
        ).splitlines()
        if not listing:
            raise SystemExit(f"Missing source task: {branch}:{source}")
        for path in listing:
            data = subprocess.check_output(["git", "show", f"FETCH_HEAD:{path}"])
            target = root / name / Path(path).relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            files += 1
print(f"Copied 77 tasks and {files} files into tasks/finalpool")
