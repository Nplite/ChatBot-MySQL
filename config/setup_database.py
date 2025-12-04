import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

load_dotenv()

# Get database credentials
host = os.getenv('MYSQL_HOST', 'localhost')
port = os.getenv('MYSQL_PORT', '3306')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DATABASE')

# URL encode password
encoded_password = quote_plus(password)

connection_string = (
    f"mysql+pymysql://{user}:{encoded_password}@"
    f"{host}:{port}/{database}"
)

engine = create_engine(connection_string)

def create_tables():
    """Create only project + knowledge base tables"""
    tables = [
        """
        CREATE TABLE IF NOT EXISTS knowledgebase (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            category ENUM('docs', 'faq', 'sop') NOT NULL,
            tags VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_category (category)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            project_name VARCHAR(255) NOT NULL,
            description TEXT,
            tech_stack TEXT,
            status ENUM('active', 'completed', 'on-hold') DEFAULT 'active',
            start_date DATE,
            metadata JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]
    
    with engine.connect() as conn:
        for table_sql in tables:
            conn.execute(text(table_sql))
            conn.commit()

def insert_sample_data():
    """Insert sample data (ONLY knowledge base + projects)"""
    

    # -----------------------------
    # Knowledgebase
    # -----------------------------
    kb_entries = [
        # Original entries...
        (
            "Milagro Offer Engine – Dynamic Rules",
            "Milagro's Offer Engine allows restaurants to create dynamic promotions using spend thresholds, visit frequency, and customer segments. "
            "Rules support auto-apply coupons, BOGO promotions, and scheduled offer campaigns.",
            "docs",
            "milagro,offers,promotions"
        ),
        (
            "Utiliko CRM Lead Pipeline Setup",
            "To configure lead pipelines: create stages (New → Qualified → In Progress → Won/Lost), assign team access levels, enable notifications, "
            "and define automation triggers for stage transitions.",
            "sop",
            "utiliko,crm,leads"
        ),
        (
            "Vivant Sensor Calibration SOP",
            "Calibration steps: open device dashboard → select sensor → apply calibration offset → save and reboot device. "
            "Recommended for temperature, humidity, and CO2 sensors every 6 months.",
            "docs",
            "vivant,iot,calibration"
        ),
        (
            "Milagro Campaign Delivery Failures",
            "Email/SMS campaign failures usually occur due to invalid contact details, provider throttling, DNS (SPF/DKIM) misconfiguration, "
            "or blocked opt-in status. Check provider logs and contact validity.",
            "faq",
            "milagro,campaigns,errors"
        ),
        (
            "Utiliko API Authentication Guidelines",
            "Utiliko APIs use token-based authentication. Steps: generate API token → store securely → include in Authorization header → "
            "regenerate tokens every 90 days. Rate limits apply per account.",
            "docs",
            "utiliko,api,auth"
        ),
        (
            "Vivant Alert Escalation Rules",
            "Alert escalations support multi-level routing: Level 1 (Technician) → Level 2 (Supervisor) → Level 3 (Admin). "
            "Escalations trigger when no acknowledgment is received within defined SLA time intervals.",
            "sop",
            "vivant,iot,alerts"
        ),
        (
            "Milagro Kiosk Connectivity Issues",
            "Kiosk offline issues often stem from WiFi drops, captive gateway restrictions, incorrect store mapping, or blocked WebSocket ports. "
            "Check network stability and kiosk diagnostics logs.",
            "faq",
            "milagro,kiosk,connectivity"
        ),
        (
            "Utiliko Timesheet Approval Workflow",
            "Timesheets follow this workflow: Employee submits → Manager review → HR validation → Auto sync to payroll. "
            "Rules can include overtime flags, missing entry alerts, and work-hour thresholds.",
            "sop",
            "utiliko,timesheet,workflow"
        ),
        (
            "Vivant Edge Device Firmware Upgrade",
            "Firmware update steps: download latest firmware package → upload via dashboard or USB → reboot device → verify version. "
            "Supports rollback in case of failed update.",
            "docs",
            "iot,vivant,firmware"
        ),
        (
            "Milagro Guest Segmentation Best Practices",
            "Guidelines for segmenting guests based on frequency, spend, and preferences to personalize offers and campaigns.",
            "docs",
            "milagro,crm,segmentation"
        ),
        (
            "Milagro POS Refund Process SOP",
            "Steps to process refunds via POS including validation, authorization, and customer notification.",
            "sop",
            "milagro,pos,refunds"
        ),
        (
            "Milagro Campaign Reporting Errors",
            "Common reporting discrepancies include duplicate entries, timezone misalignment, and missing transaction logs.",
            "faq",
            "milagro,campaigns,reporting"
        ),
        (
            "Milagro Customer Feedback Collection Guidelines",
            "Defines methods to collect and store customer feedback from app, kiosk, and in-store surveys.",
            "docs",
            "milagro,crm,feedback"
        ),
        (
            "Milagro Menu Update Workflow",
            "Workflow for updating menu items, prices, and availability on POS and mobile platforms with approval steps.",
            "sop",
            "milagro,menu,workflow"
        ),
        (
            "Milagro Loyalty Points Expiry FAQ",
            "Explains how loyalty points expire, how to adjust expiry settings, and troubleshoot points not applying.",
            "faq",
            "milagro,loyalty,points"
        ),
        (
            "Milagro API Webhook Setup",
            "Instructions to configure webhooks for real-time event notifications such as orders, loyalty updates, and refunds.",
            "docs",
            "milagro,api,webhooks"
        ),
        (
            "Milagro Offline POS Order Handling SOP",
            "Steps for managing offline orders, syncing data, and resolving conflicts when POS reconnects.",
            "sop",
            "milagro,pos,offline"
        ),
        (
            "Milagro Push Notification Delivery Issues",
            "Troubleshooting delivery failures including invalid tokens, app version mismatches, and provider throttling.",
            "faq",
            "milagro,notifications,issues"
        ),
        (
            "Milagro Gift Card Management",
            "Instructions to create, activate, and redeem gift cards via POS and mobile app.",
            "docs",
            "milagro,giftcards,management"
        ),
        (
            "Utiliko Project Template Configuration",
            "Create project templates with pre-defined tasks, milestones, and workflows to accelerate project setup.",
            "docs",
            "utiliko,project,templates"
        ),
        (
            "Utiliko SLA Escalation Rules SOP",
            "Define SLA thresholds, alert notifications, and escalation steps for overdue tasks or tickets.",
            "sop",
            "utiliko,sla,workflow"
        ),
        (
            "Utiliko API Throttling FAQ",
            "Common causes for API throttling, best practices for retries, and monitoring API limits.",
            "faq",
            "utiliko,api,throttling"
        ),
        (
            "Utiliko Lead Assignment Rules",
            "Rules to auto-assign leads based on territory, team, or priority, including conflict resolution settings.",
            "docs",
            "utiliko,crm,leads"
        ),
        (
            "Utiliko Timesheet Error Handling SOP",
            "Handling missing entries, overtime discrepancies, and approval conflicts with step-by-step resolution.",
            "sop",
            "utiliko,timesheet,errors"
        ),
        (
            "Utiliko Data Export Issues FAQ",
            "Troubleshooting CSV and Excel export failures, including permission issues and data validation errors.",
            "faq",
            "utiliko,data,export"
        ),
        (
            "Utiliko Workflow Automation Best Practices",
            "Guidelines for creating efficient workflows, avoiding loops, and testing conditions before deployment.",
            "docs",
            "utiliko,workflow,best-practices"
        ),
        (
            "Utiliko User Permissions Configuration SOP",
            "Step-by-step guide to assign roles, adjust permissions, and review access logs.",
            "sop",
            "utiliko,users,permissions"
        ),
        (
            "Utiliko Notification Delivery FAQ",
            "Troubleshooting email, in-app, and SMS notification failures with stepwise verification.",
            "faq",
            "utiliko,notifications,issues"
        ),
        (
            "Utiliko Project Dashboard Setup",
            "Instructions to configure dashboards with widgets, filters, and key metrics for project monitoring.",
            "docs",
            "utiliko,dashboard,projects"
        ),
        (
            "Vivant Sensor Network Configuration",
            "Setup and configure Vivant sensors with network credentials, device groups, and reporting intervals.",
            "docs",
            "vivant,iot,network"
        ),
        (
            "Vivant Alert Escalation SOP",
            "Define alert thresholds, multi-level escalation, and notification channels for critical events.",
            "sop",
            "vivant,alerts,escalation"
        ),
        (
            "Vivant Device Offline Troubleshooting FAQ",
            "Common reasons for devices going offline and steps to restore connectivity.",
            "faq",
            "vivant,iot,connectivity"
        ),
        (
            "Vivant Energy Meter Calibration",
            "Procedure to calibrate energy meters for accurate readings, including validation steps.",
            "docs",
            "vivant,energy,calibration"
        ),
        (
            "Vivant Edge Firmware Update SOP",
            "Update firmware using dashboard or USB, with rollback steps in case of failure.",
            "sop",
            "vivant,firmware,update"
        ),
        (
            "Vivant Motion Sensor Configuration FAQ",
            "Adjust sensitivity, detection zones, and reporting intervals for optimal performance.",
            "faq",
            "vivant,iot,motion"
        ),
        (
            "Vivant IoT Device Grouping Best Practices",
            "Organize devices into logical groups for reporting, alerts, and maintenance scheduling.",
            "docs",
            "vivant,iot,grouping"
        ),
        (
            "Vivant Predictive Maintenance Setup SOP",
            "Configure AI models to monitor sensor trends and trigger preventive maintenance alerts.",
            "sop",
            "vivant,maintenance,predictive"
        ),
        (
            "Vivant Dashboard Widget Configuration FAQ",
            "Troubleshoot missing or misaligned widgets, refresh intervals, and data sources.",
            "faq",
            "vivant,dashboard,widgets"
        ),
        (
            "Vivant Security Patch Management",
            "Guidelines to apply security patches, schedule updates, and verify device compliance.",
            "docs",
            "vivant,security,patches"
        ),
        (
            "Milagro Cross-Sell Campaign Guidelines",
            "Steps to configure cross-sell campaigns using AI-driven recommendations and historical data analysis.",
            "docs",
            "milagro,campaigns,cross-sell"
        ),
        (
            "Milagro Kiosk Payment Gateway Troubleshooting",
            "Common payment failures including network issues, gateway timeouts, and configuration errors.",
            "faq",
            "milagro,kiosk,payments"
        ),
        (
            "Milagro Menu Price Update SOP",
            "Workflow to update item prices on POS and mobile apps, including approval and rollback steps.",
            "sop",
            "milagro,menu,pricing"
        ),
        (
            "Milagro Loyalty Tier Upgrade FAQ",
            "Explains tier upgrade conditions, automatic reward assignment, and troubleshooting points.",
            "faq",
            "milagro,loyalty,tiers"
        ),
        (
            "Milagro API Integration Checklist",
            "Checklist to validate API keys, endpoints, request/response formats, and error handling.",
            "docs",
            "milagro,api,integration"
        ),
        (
            "Milagro Offer Expiration Rules SOP",
            "Configures offer expiration logic, notifications to users, and handling of pending redemptions.",
            "sop",
            "milagro,offers,expiration"
        ),
        (
            "Milagro Customer Data Sync FAQ",
            "Troubleshoot failures in syncing guest data across POS, mobile, and loyalty systems.",
            "faq",
            "milagro,crm,sync"
        ),
        (
            "Milagro Email Campaign Template Guidelines",
            "Create consistent templates for email campaigns including personalization, media assets, and testing steps.",
            "docs",
            "milagro,campaigns,email"
        ),
        (
            "Milagro Store Opening Checklist SOP",
            "Checklist for new store setup including POS, loyalty, inventory, and staff onboarding.",
            "sop",
            "milagro,store,setup"
        ),
        (
            "Milagro Push Notification Best Practices FAQ",
            "Troubleshoot low delivery or engagement rates with device tokens, opt-ins, and campaign configuration.",
            "faq",
            "milagro,notifications,best-practices"
        ),
        # NEW ENTRIES for better coverage
        (
            "Common Database Connection Pool Exhaustion",
            "When connection pool is exhausted: 1) Check for unclosed connections in code, 2) Review pool size configuration, 3) Monitor connection lifecycle, 4) Implement connection timeout settings, 5) Use connection pooling best practices.",
            "faq",
            "database,performance,all-products"
        ),
        (
            "Redis Cache Invalidation Strategy",
            "Best practices for cache invalidation: 1) Use TTL-based expiration, 2) Implement event-driven invalidation, 3) Version cache keys, 4) Monitor cache hit rates, 5) Handle cache stampede scenarios.",
            "docs",
            "redis,caching,all-products"
        ),
        (
            "API Rate Limiting Troubleshooting",
            "When facing rate limit errors: 1) Check current request rate, 2) Implement exponential backoff, 3) Use request queuing, 4) Monitor rate limit headers, 5) Contact support for limit increase if needed.",
            "faq",
            "api,performance,all-products"
        ),
    ]


    # -----------------------------
    # Projects
    # -----------------------------

    projects = [
    # Milagro Projects
    (
        "Milagro Customer Analytics Portal",
        "Provides advanced analytics on customer behavior, campaign effectiveness, and sales trends with interactive dashboards.",
        "React, Node.js, PostgreSQL, D3.js, Redis",
        "active",
        "2024-02-28"
    ),
    (
        "Milagro POS Cloud Sync",
        "Cloud-based POS synchronization service ensuring real-time data consistency across multiple outlets with automated conflict resolution.",
        "Node.js, Express, MongoDB, Redis, Docker",
        "active",
        "2024-03-01"
    ),
    (
        "Milagro Restaurant Operations Dashboard",
        "Dashboard for restaurant managers to monitor daily sales, inventory, staff performance, and customer feedback in real-time.",
        "Node.js, React, PostgreSQL, Redis, Docker",
        "completed",
        "2023-09-15"
    ),
    (
        "Milagro Offer Engine Automation",
        "Automates creation and delivery of promotions, BOGO campaigns, and targeted customer offers based on AI-driven segmentation.",
        "Python, Flask, PostgreSQL, Redis, Celery",
        "active",
        "2024-05-10"
    ),
    (
        "Milagro Kiosk Analytics",
        "Monitors self-service kiosk usage, error logs, and transaction patterns for multiple restaurant locations.",
        "Flutter, Firebase, Node.js, MongoDB",
        "active",
        "2024-07-01"
    ),
    (
        "Milagro Mobile Ordering App",
        "Enables customers to place orders via mobile app, integrates with POS, loyalty, and personalized recommendations.",
        "React Native, Node.js, PostgreSQL, Redis",
        "active",
        "2024-06-15"
    ),
    (
        "Milagro Campaign Management System",
        "Manages email, SMS, and push campaigns with scheduling, analytics, and A/B testing support.",
        "Python, Django, PostgreSQL, Celery, Redis",
        "active",
        "2024-04-20"
    ),
    (
        "Milagro Loyalty Points Engine",
        "Tracks and manages customer loyalty points, redemptions, and tier progression in real-time across POS and mobile apps.",
        "Node.js, MongoDB, Redis, Express",
        "active",
        "2024-03-15"
    ),

    # Utiliko Projects
    (
        "Utiliko Compliance & Audit Tracker",
        "Tracks compliance across multiple projects, logs changes, and automates audit report generation with role-based access.",
        "Python, FastAPI, PostgreSQL, Celery, Vue.js",
        "active",
        "2024-01-15"
    ),
    (
        "Utiliko Intelligent Ticket Routing",
        "Automatically routes tickets to the right teams based on SLA, priority, and agent availability.",
        "Python, FastAPI, PostgreSQL, Celery, Vue.js",
        "active",
        "2024-03-20"
    ),
    (
        "Utiliko API Integration Hub",
        "Central hub to integrate third-party APIs with Utiliko workflows and automate data sync across systems.",
        "Python, Django, PostgreSQL, Celery, Vue.js",
        "active",
        "2024-02-25"
    ),
    (
        "Utiliko Project Performance Dashboard",
        "Visualizes project progress, task completion, and resource utilization with real-time reporting.",
        "Python, FastAPI, PostgreSQL, Vue.js, Plotly",
        "active",
        "2024-04-01"
    ),
    (
        "Utiliko Timesheet Automation",
        "Automates timesheet approvals, overtime detection, and integration with payroll systems.",
        "Python, FastAPI, PostgreSQL, Celery, Vue.js",
        "active",
        "2024-03-05"
    ),
    (
        "Utiliko Knowledge Base AI Search",
        "Enables intelligent search and recommendations for SOPs, FAQs, and workflow documentation.",
        "Python, Django, Elasticsearch, Vue.js",
        "active",
        "2024-06-01"
    ),
    (
        "Utiliko Employee Performance Analytics",
        "Tracks KPIs, timesheet compliance, and task completion rates with AI-driven insights for optimization.",
        "Python, FastAPI, PostgreSQL, Vue.js, Pandas",
        "active",
        "2024-04-05"
    ),
    (
        "Utiliko CRM Workflow Upgrade",
        "Enhances CRM workflows with automated approvals, reminders, and SLA notifications.",
        "Python, Django, PostgreSQL, Vue.js",
        "active",
        "2024-05-20"
    ),
    (
        "Utiliko Startup Consulting Project",
        "Strategic consultation for optimizing Utiliko setup for fast-growing startups, including process automation and best practices.",
        "Python, FastAPI, PostgreSQL, Vue.js",
        "completed",
        "2024-06-15"
    ),
    (
        "Utiliko Enterprise Billing Integration",
        "Automates billing, invoicing, and subscription management within Utiliko CRM for enterprise clients.",
        "Python, Django, PostgreSQL, Celery, Vue.js",
        "active",
        "2024-07-01"
    ),

    # Vivant Projects
    (
        "Vivant Facility IoT Gateway Upgrade",
        "Next-gen gateway system for edge devices, supporting BACnet, Modbus, and MQTT protocols with secure OTA firmware updates.",
        "Go, MQTT, Docker, Kubernetes, React",
        "active",
        "2024-09-10"
    ),
    (
        "Vivant Energy Management Dashboard",
        "Centralized dashboard for real-time monitoring of energy consumption, predictive maintenance, and anomaly detection.",
        "Go, React, InfluxDB, Grafana, MQTT",
        "on-hold",
        "2024-05-20"
    ),
    (
        "Vivant Predictive Maintenance Platform",
        "AI-powered predictive maintenance platform for HVAC, lighting, and industrial sensors to reduce downtime and optimize efficiency.",
        "Python, TensorFlow, MQTT, PostgreSQL, Kubernetes",
        "active",
        "2024-08-01"
    ),
    (
        "Vivant Smart Security Integration",
        "Integrates CCTV, access control, and motion sensors into a unified dashboard with AI-based anomaly detection.",
        "Python, OpenCV, MQTT, React, PostgreSQL",
        "active",
        "2024-06-20"
    ),
    (
        "Vivant Environmental Monitoring System",
        "Monitors air quality, temperature, humidity, and CO2 levels in real-time across multiple facilities with alerting.",
        "Go, InfluxDB, MQTT, React, Grafana",
        "active",
        "2024-08-15"
    ),
    (
        "Vivant Network Security Expansion",
        "Deploys enterprise-grade secure network with firewalls, VPNs, and monitoring across multiple locations.",
        "Go, Kubernetes, Terraform, Grafana, Prometheus",
        "active",
        "2024-07-10"
    ),
    (
        "Vivant SD-WAN Implementation",
        "SD-WAN deployment across multiple locations with centralized management and redundancy for warehouse facilities.",
        "Go, MQTT, React, Kubernetes",
        "on-hold",
        "2024-10-15"
    ),
    (
        "Vivant VoIP System Deployment",
        "Deploy VoIP system for multiple offices with mobile client integration and cloud PBX management.",
        "Python, React, MQTT, PostgreSQL",
        "on-hold",
        "2024-11-01"
    ),
    (
        "Vivant IoT Sensor Expansion",
        "Adds new IoT sensors to existing Vivant monitoring platform for predictive analytics and energy optimization.",
        "Go, MQTT, InfluxDB, React, Docker",
        "completed",
        "2025-01-10"
    ),
    (
        "Vivant Industrial Automation Analytics",
        "Provides real-time analytics and predictive insights for industrial machinery using IoT sensor data.",
        "Python, TensorFlow, MQTT, PostgreSQL, React",
        "active",
        "2024-09-20"
    ),
      (
        "Milagro Virtual Event Ordering Platform",
        "Allows restaurants to host virtual events with integrated ordering, loyalty rewards, and real-time analytics.",
        "Node.js, React, Firebase, MongoDB, Redis",
        "completed",
        "2025-01-10"
    ),
    (
        "Milagro Voice-Activated Ordering System",
        "Enables customers to place orders using voice commands with POS integration and personalized recommendations.",
        "Python, TensorFlow, Flask, PostgreSQL, Docker",
        "completed",
        "2025-02-01"
    ),
    (
        "Milagro AI Menu Optimization",
        "Analyzes sales and customer behavior to recommend menu changes, dynamic pricing, and promotional items.",
        "Python, PyTorch, Django, PostgreSQL, Redis",
        "active",
        "2024-12-15"
    ),

    # Utiliko Projects
    (
        "Utiliko AI Contract Analyzer",
        "Uses NLP to review contracts, detect risks, and summarize key clauses for legal teams.",
        "Python, FastAPI, SpaCy, PostgreSQL, Vue.js",
        "completed",
        "2025-01-15"
    ),
    (
        "Utiliko Remote Workforce Tracker",
        "Monitors employee tasks, attendance, and productivity in real-time for remote teams with analytics dashboards.",
        "Python, Django, PostgreSQL, Vue.js, Celery",
        "active",
        "2024-12-20"
    ),
    (
        "Utiliko Automated Compliance Reporter",
        "Generates regulatory and internal compliance reports automatically based on workflow data and audit logs.",
        "Python, FastAPI, PostgreSQL, Pandas, Vue.js",
        "active",
        "2024-11-30"
    ),

    # Vivant Projects
    (
        "Vivant Smart Parking Management",
        "Monitors parking lot occupancy, controls access, and provides real-time availability data via mobile app.",
        "Go, MQTT, React, PostgreSQL, Kubernetes",
        "completed",
        "2025-01-05"
    ),
    (
        "Vivant AI Energy Consumption Optimizer",
        "AI-powered platform to reduce energy consumption in industrial facilities based on real-time sensor data and predictive modeling.",
        "Python, TensorFlow, MQTT, PostgreSQL, Grafana",
        "active",
        "2024-12-10"
    ),
    (
        "Vivant Fleet IoT Tracking",
        "Tracks vehicles in real-time using IoT sensors, monitors fuel usage, and optimizes routes with predictive analytics.",
        "Go, MQTT, InfluxDB, React, Docker",
        "completed",
        "2025-02-01"
    ),
    (
        "Vivant Smart HVAC Scheduling",
        "Automatically schedules HVAC operations based on occupancy, weather forecast, and energy pricing data.",
        "Python, Flask, MQTT, PostgreSQL, React",
        "active",
        "2024-12-01"
    )
]





    with engine.connect() as conn:
        # Insert knowledge base
        for title, content, category, tags in kb_entries:
            conn.execute(
                text("""
                    INSERT INTO knowledgebase (title, content, category, tags) 
                    VALUES (:title, :content, :category, :tags)
                """),
                {"title": title, "content": content, "category": category, "tags": tags}
            )
            conn.commit()
        
        # Insert projects
        for name, desc, tech, status, start_date in projects:
            conn.execute(
                text("""
                    INSERT INTO projects (project_name, description, tech_stack, status, start_date) 
                    VALUES (:name, :desc, :tech, :status, :start_date)
                """),
                {"name": name, "desc": desc, "tech": tech, "status": status, "start_date": start_date}
            )
            conn.commit()

def verify_data():
    """Verify only project + KB data"""
    with engine.connect() as conn:
        kb_count = conn.execute(text("SELECT COUNT(*) FROM knowledgebase")).scalar()
        proj_count = conn.execute(text("SELECT COUNT(*) FROM projects")).scalar()
        
        print("\n" + "="*60)
        print("Verification:")
        print("="*60)
        print(f"Knowledge Base entries: {kb_count}")
        print(f"Projects: {proj_count}")
        
        return kb_count > 0 and proj_count > 0

def setup_database():
    """Main setup function"""
    print("="*60)
    print("Database Setup Script")
    print("="*60)
    print(f"\nConnecting to database: {database}")
    
    try:
        # Check if KB already has data
        with engine.connect() as conn:
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM knowledgebase"))
                count = result.scalar()
                
                if count > 0:
                    print(f"\n⚠️  Database already contains {count} knowledge base entries")
                    response = input("Do you want to clear and reload data? (y/n): ").lower()
                    if response == 'y':
                        print("\nClearing existing data...")
                        conn.execute(text("DELETE FROM projects"))
                        conn.execute(text("DELETE FROM knowledgebase"))
                        conn.commit()
                        print("✓ Data cleared")
                    else:
                        print("Setup cancelled")
                        return
            except:
                pass  # Tables not created yet
        
        # Create tables
        print("\n[1/2] Creating tables...")
        create_tables()
        print("✓ Tables created successfully")
        
        # Insert sample data
        print("\n[2/2] Inserting sample data...")
        insert_sample_data()
        print("✓ Sample data inserted successfully")
        
        # Verify
        if verify_data():
            print("\n✓ Database setup completed successfully!")
        else:
            print("\n⚠️  Warning: Some data may not have been inserted correctly")
            
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_database()
