"""Seed the Kronos database with realistic sample data matching the PDF spec."""

from datetime import date, datetime, timedelta

from app import app
from models import (
    AssetChangeLog,
    DigitalTracker,
    LegalException,
    PriorAudit,
    System,
    UseCase,
    Vendor,
    db,
)


def seed():
    with app.app_context():
        if Vendor.query.count() > 0:
            print("Database already seeded. Skipping.")
            return

        # --- Vendors ---
        vendors = [
            Vendor(asset_id="VND-ADOBE", name="Adobe", vendor_type="SaaS", vendor_category="analytics",
                   description="Analytics, audience management, and ad-serving platform", owner="Marketing",
                   risk_rating="high", dpa_in_place=True, contract_expiry=date(2027, 6, 30),
                   data_shared="Page views, user events, device data", region="Global", status="active"),
            Vendor(asset_id="VND-GOOGLE", name="Google", vendor_type="SaaS", vendor_category="advertising",
                   description="Search, advertising, and analytics services", owner="Marketing",
                   risk_rating="high", dpa_in_place=True, contract_expiry=date(2026, 12, 31),
                   data_shared="Ad impressions, conversions, audience segments", region="Global", status="active"),
            Vendor(asset_id="VND-ONETRUST", name="OneTrust", vendor_type="SaaS", vendor_category="privacy",
                   description="Privacy management and consent orchestration", owner="Privacy",
                   risk_rating="medium", dpa_in_place=True, contract_expiry=date(2027, 3, 15),
                   data_shared="Consent records, privacy preferences", region="Global", status="active"),
            Vendor(asset_id="VND-SNOWFLK", name="Snowflake", vendor_type="SaaS", vendor_category="cloud",
                   description="Cloud data warehouse and analytics platform", owner="Data Engineering",
                   risk_rating="medium", dpa_in_place=True, contract_expiry=date(2027, 9, 30),
                   data_shared="All data warehouse data", region="Global", status="active"),
            Vendor(asset_id="VND-AWS", name="Amazon Web Services", vendor_type="IaaS", vendor_category="cloud",
                   description="Infrastructure, storage, and compute services", owner="Infrastructure",
                   risk_rating="medium", dpa_in_place=True, contract_expiry=date(2028, 1, 1),
                   data_shared="All cloud-hosted data", region="Global", status="active"),
            Vendor(asset_id="VND-BRAZE", name="Braze", vendor_type="SaaS", vendor_category="marketing",
                   description="Customer engagement and messaging platform", owner="Lifecycle",
                   risk_rating="medium", dpa_in_place=True, contract_expiry=date(2026, 9, 30),
                   data_shared="User profiles, campaign data, push tokens", region="US", status="active"),
            Vendor(asset_id="VND-ADJUST", name="Adjust", vendor_type="SaaS", vendor_category="attribution",
                   description="Mobile attribution and analytics", owner="Marketing",
                   risk_rating="medium", dpa_in_place=True, contract_expiry=date(2026, 8, 31),
                   data_shared="Install attribution, in-app events", region="Global", status="active"),
            Vendor(asset_id="VND-CONVIVA", name="Conviva", vendor_type="SaaS", vendor_category="analytics",
                   description="Streaming quality analytics and optimization", owner="Product & Tech Analytics",
                   risk_rating="low", dpa_in_place=True, contract_expiry=date(2027, 4, 15),
                   data_shared="Playback telemetry, buffering events", region="Global", status="active"),
            Vendor(asset_id="VND-NEWRELC", name="New Relic", vendor_type="SaaS", vendor_category="monitoring",
                   description="Application performance monitoring", owner="Engineering",
                   risk_rating="low", dpa_in_place=True, contract_expiry=date(2026, 11, 30),
                   data_shared="APM traces, error logs", region="US", status="active"),
            Vendor(asset_id="VND-LEGACYX", name="LegacyTrack Corp", vendor_type="SaaS", vendor_category="analytics",
                   description="Legacy tracking vendor — pending migration", owner="Marketing",
                   risk_rating="critical", dpa_in_place=False, contract_expiry=date(2025, 12, 31),
                   data_shared="User behavior, device IDs", region="US", status="under_review"),
        ]
        db.session.add_all(vendors)
        db.session.flush()

        vendor_map = {v.asset_id: v for v in vendors}

        # --- Systems ---
        systems = [
            System(asset_id="SYS-DPLUS", name="Disney+ Platform", system_type="application",
                   description="Primary streaming platform serving Disney+ content", business_unit="Disney+",
                   data_classification="confidential", hosting="cloud", pii_processed=True,
                   owner="Disney+ Engineering", vendor_id=vendor_map["VND-AWS"].id, region="Global", status="active"),
            System(asset_id="SYS-HULU", name="Hulu Platform", system_type="application",
                   description="Hulu streaming service with live TV and on-demand", business_unit="Hulu",
                   data_classification="confidential", hosting="cloud", pii_processed=True,
                   owner="Hulu Engineering", vendor_id=vendor_map["VND-AWS"].id, region="US", status="active"),
            System(asset_id="SYS-ESPN", name="ESPN Digital", system_type="application",
                   description="ESPN web and mobile applications", business_unit="ESPN",
                   data_classification="confidential", hosting="cloud", pii_processed=True,
                   owner="ESPN Engineering", vendor_id=vendor_map["VND-AWS"].id, region="US", status="active"),
            System(asset_id="SYS-CDP", name="Customer Data Platform", system_type="database",
                   description="Unified customer profiles for audience activation", business_unit="Unified Audience Data",
                   data_classification="restricted", hosting="cloud", pii_processed=True,
                   owner="Unified Audience Data", vendor_id=vendor_map["VND-SNOWFLK"].id, region="Global", status="active"),
            System(asset_id="SYS-SFWH", name="Snowflake Data Warehouse", system_type="warehouse",
                   description="Central analytical data warehouse (54 PB, 170K tables)", business_unit="Data Engineering",
                   data_classification="confidential", hosting="cloud", pii_processed=True,
                   owner="Data Engineering", vendor_id=vendor_map["VND-SNOWFLK"].id, region="Global", status="active"),
            System(asset_id="SYS-S3DL", name="AWS S3 Data Lake", system_type="database",
                   description="Primary data lake (1.4 EB across 130K buckets)", business_unit="Data Engineering",
                   data_classification="confidential", hosting="cloud", pii_processed=True,
                   owner="Infrastructure", vendor_id=vendor_map["VND-AWS"].id, region="Global", status="active"),
            System(asset_id="SYS-OTRUST", name="OneTrust Consent Manager", system_type="application",
                   description="Consent collection and preference management", business_unit="Privacy",
                   data_classification="restricted", hosting="cloud", pii_processed=True,
                   owner="Privacy", vendor_id=vendor_map["VND-ONETRUST"].id, region="Global", status="active"),
            System(asset_id="SYS-IDGRPH", name="Identity Graph", system_type="database",
                   description="Cross-device identity resolution service", business_unit="Identity",
                   data_classification="restricted", hosting="cloud", pii_processed=True,
                   owner="Identity", region="Global", status="active"),
            System(asset_id="SYS-RECENG", name="Recommendation Engine", system_type="application",
                   description="Content recommendation ML pipeline", business_unit="Science",
                   data_classification="internal", hosting="cloud", pii_processed=True,
                   owner="Science", region="Global", status="active"),
            System(asset_id="SYS-PAYMT", name="Payment Processing System", system_type="application",
                   description="Handles subscription billing and payment methods", business_unit="Commerce",
                   data_classification="restricted", hosting="cloud", pii_processed=True,
                   certifications="PCI-DSS", owner="Commerce Data Solutions", region="Global", status="active"),
        ]
        db.session.add_all(systems)
        db.session.flush()

        system_map = {s.asset_id: s for s in systems}

        # --- Digital Trackers ---
        trackers = [
            DigitalTracker(asset_id="TRK-ADOBEA", name="Adobe Analytics Tag", tracker_type="tag",
                           purpose="Site and app analytics including page views, events, and user flows",
                           domain_or_platform="disneyplus.com, hulu.com, espn.com",
                           data_collected="Page URL, events, device type, user ID", placement="website",
                           consent_required=True, owner="Marketing", vendor_id=vendor_map["VND-ADOBE"].id,
                           region="Global", status="active"),
            DigitalTracker(asset_id="TRK-ADOBET", name="Adobe Target Pixel", tracker_type="pixel",
                           purpose="A/B testing and personalization",
                           domain_or_platform="disneyplus.com",
                           data_collected="Variant assignments, conversion events", placement="website",
                           consent_required=True, owner="Product & Tech Analytics", vendor_id=vendor_map["VND-ADOBE"].id,
                           region="US", status="active"),
            DigitalTracker(asset_id="TRK-GTAG", name="Google Analytics 4 Tag", tracker_type="tag",
                           purpose="Traffic analytics and conversion measurement",
                           domain_or_platform="disneyplus.com, espn.com",
                           data_collected="Page views, scroll depth, events", placement="website",
                           consent_required=True, owner="Marketing", vendor_id=vendor_map["VND-GOOGLE"].id,
                           region="Global", status="active"),
            DigitalTracker(asset_id="TRK-GADS", name="Google Ads Conversion Pixel", tracker_type="pixel",
                           purpose="Track ad campaign conversions",
                           domain_or_platform="disneyplus.com, hulu.com",
                           data_collected="Conversion events, transaction values", placement="website",
                           consent_required=True, owner="Marketing", vendor_id=vendor_map["VND-GOOGLE"].id,
                           region="US", status="active"),
            DigitalTracker(asset_id="TRK-ADJUST", name="Adjust SDK", tracker_type="SDK",
                           purpose="Mobile install attribution and in-app analytics",
                           domain_or_platform="Disney+ iOS, Disney+ Android, Hulu iOS",
                           data_collected="Install source, in-app events, device ID", placement="app",
                           consent_required=True, owner="Marketing", vendor_id=vendor_map["VND-ADJUST"].id,
                           region="Global", status="active"),
            DigitalTracker(asset_id="TRK-BRAZEP", name="Braze Push SDK", tracker_type="SDK",
                           purpose="Push notification delivery and engagement tracking",
                           domain_or_platform="Disney+ iOS, Disney+ Android, Hulu iOS",
                           data_collected="Push token, notification events, open rates", placement="app",
                           consent_required=True, owner="Lifecycle", vendor_id=vendor_map["VND-BRAZE"].id,
                           region="US", status="active"),
            DigitalTracker(asset_id="TRK-CONVIV", name="Conviva Streaming Sensor", tracker_type="SDK",
                           purpose="Video quality of experience monitoring",
                           domain_or_platform="Disney+, Hulu, ESPN",
                           data_collected="Buffering, bitrate, playback failures", placement="app",
                           consent_required=False, owner="Product & Tech Analytics",
                           vendor_id=vendor_map["VND-CONVIVA"].id, region="Global", status="active"),
            DigitalTracker(asset_id="TRK-OTCMP", name="OneTrust Consent Banner", tracker_type="script",
                           purpose="Cookie consent collection and preference management",
                           domain_or_platform="disneyplus.com, hulu.com, espn.com",
                           data_collected="Consent preferences, opt-in/out status", placement="website",
                           consent_required=False, owner="Privacy", vendor_id=vendor_map["VND-ONETRUST"].id,
                           region="Global", status="active"),
            DigitalTracker(asset_id="TRK-LEGACY", name="LegacyTrack Pixel", tracker_type="pixel",
                           purpose="Legacy behavioral tracking — pending removal",
                           domain_or_platform="legacy.disneyplus.com",
                           data_collected="User behavior, click events, device fingerprint", placement="website",
                           consent_required=True, owner="Marketing", vendor_id=vendor_map["VND-LEGACYX"].id,
                           region="US", status="deprecated"),
        ]
        db.session.add_all(trackers)
        db.session.flush()

        tracker_map = {t.asset_id: t for t in trackers}

        # --- Business Use Cases ---
        use_cases = [
            UseCase(asset_id="UC-ADSATTR", name="Advertising Attribution",
                    category="Audience Measurement", subcategory="Ad Attribution",
                    description="Measure effectiveness of ad campaigns across platforms",
                    legal_basis="consent", owner="Marketing", region="Global", status="active"),
            UseCase(asset_id="UC-PERSNLZ", name="Content Personalization",
                    category="Product Experience", subcategory="Recommendations",
                    description="Personalize content recommendations based on viewing history",
                    legal_basis="legitimate interest", owner="Science", region="Global", status="active"),
            UseCase(asset_id="UC-PURCHPR", name="Purchase Propensity Modeling",
                    category="Audience Measurement", subcategory="Purchase Propensity",
                    description="Predict likelihood of subscription upgrade or churn",
                    legal_basis="legitimate interest", owner="Science", region="US", status="active"),
            UseCase(asset_id="UC-ABTEST", name="A/B Testing & Experimentation",
                    category="Product Experience", subcategory="Experimentation",
                    description="Run controlled experiments on UI, pricing, and features",
                    legal_basis="legitimate interest", owner="Product & Tech Analytics",
                    region="Global", status="active"),
            UseCase(asset_id="UC-EMAILC", name="Lifecycle Email Campaigns",
                    category="Marketing", subcategory="Email & Push",
                    description="Targeted email campaigns for engagement and retention",
                    legal_basis="consent", owner="Lifecycle", region="US", status="active"),
            UseCase(asset_id="UC-STRQOE", name="Streaming Quality of Experience",
                    category="Operations", subcategory="QoE Monitoring",
                    description="Monitor and optimize video playback quality metrics",
                    legal_basis="legitimate interest", owner="Product & Tech Analytics",
                    region="Global", status="active"),
            UseCase(asset_id="UC-IDRESO", name="Cross-Device Identity Resolution",
                    category="Identity", subcategory="Device Graph",
                    description="Link user sessions across devices for unified experience",
                    legal_basis="consent", cross_border=True, owner="Identity", region="Global", status="active"),
            UseCase(asset_id="UC-CONMGM", name="Consent Management",
                    category="Privacy & Compliance", subcategory="Consent Orchestration",
                    description="Collect, store, and enforce user consent preferences",
                    legal_basis="legal obligation", owner="Privacy", region="Global", status="active"),
            UseCase(asset_id="UC-SUBSBI", name="Subscription Billing Analytics",
                    category="Commerce", subcategory="Revenue Analytics",
                    description="Analyze subscription revenue, churn, and payment patterns",
                    legal_basis="contract", owner="Commerce Data Solutions", region="Global", status="active"),
        ]
        db.session.add_all(use_cases)
        db.session.flush()

        uc_map = {u.asset_id: u for u in use_cases}

        # --- M:M Relationships ---
        # Ad Attribution → Google, Adobe, trackers, systems
        uc_map["UC-ADSATTR"].vendors.extend([vendor_map["VND-GOOGLE"], vendor_map["VND-ADOBE"], vendor_map["VND-ADJUST"]])
        uc_map["UC-ADSATTR"].trackers.extend([tracker_map["TRK-GTAG"], tracker_map["TRK-GADS"],
                                               tracker_map["TRK-ADOBEA"], tracker_map["TRK-ADJUST"]])
        uc_map["UC-ADSATTR"].systems.extend([system_map["SYS-DPLUS"], system_map["SYS-HULU"], system_map["SYS-ESPN"]])

        # Content Personalization
        uc_map["UC-PERSNLZ"].vendors.extend([vendor_map["VND-SNOWFLK"]])
        uc_map["UC-PERSNLZ"].trackers.extend([tracker_map["TRK-ADOBEA"]])
        uc_map["UC-PERSNLZ"].systems.extend([system_map["SYS-RECENG"], system_map["SYS-CDP"], system_map["SYS-SFWH"]])

        # Purchase Propensity
        uc_map["UC-PURCHPR"].vendors.extend([vendor_map["VND-SNOWFLK"]])
        uc_map["UC-PURCHPR"].systems.extend([system_map["SYS-CDP"], system_map["SYS-SFWH"]])
        uc_map["UC-PURCHPR"].trackers.extend([tracker_map["TRK-ADOBEA"]])

        # A/B Testing
        uc_map["UC-ABTEST"].vendors.extend([vendor_map["VND-ADOBE"]])
        uc_map["UC-ABTEST"].trackers.extend([tracker_map["TRK-ADOBET"], tracker_map["TRK-ADOBEA"]])
        uc_map["UC-ABTEST"].systems.extend([system_map["SYS-DPLUS"]])

        # Email Campaigns
        uc_map["UC-EMAILC"].vendors.extend([vendor_map["VND-BRAZE"]])
        uc_map["UC-EMAILC"].trackers.extend([tracker_map["TRK-BRAZEP"]])
        uc_map["UC-EMAILC"].systems.extend([system_map["SYS-CDP"]])

        # Streaming QoE
        uc_map["UC-STRQOE"].vendors.extend([vendor_map["VND-CONVIVA"]])
        uc_map["UC-STRQOE"].trackers.extend([tracker_map["TRK-CONVIV"]])
        uc_map["UC-STRQOE"].systems.extend([system_map["SYS-DPLUS"], system_map["SYS-HULU"], system_map["SYS-ESPN"]])

        # Identity Resolution
        uc_map["UC-IDRESO"].systems.extend([system_map["SYS-IDGRPH"], system_map["SYS-CDP"]])

        # Consent Management
        uc_map["UC-CONMGM"].vendors.extend([vendor_map["VND-ONETRUST"]])
        uc_map["UC-CONMGM"].trackers.extend([tracker_map["TRK-OTCMP"]])
        uc_map["UC-CONMGM"].systems.extend([system_map["SYS-OTRUST"]])

        # Subscription Billing
        uc_map["UC-SUBSBI"].systems.extend([system_map["SYS-PAYMT"], system_map["SYS-SFWH"]])

        # --- Legal Exceptions ---
        exceptions = [
            LegalException(asset_id="LEX-001", name="Legacy Tracker Retention Waiver",
                           exception_type="policy waiver", related_assets="TRK-LEGACY, VND-LEGACYX",
                           expiry_date=date(2026, 6, 30), approval_date=date(2025, 12, 1),
                           approved_by="Legal Counsel", policy_or_standard="Data Retention Standard",
                           justification="Migration to Adobe in progress; legacy pixel remains until cutover",
                           owner="Privacy", status="active"),
            LegalException(asset_id="LEX-002", name="Payment Data Indefinite Retention",
                           exception_type="regulatory exception", related_assets="SYS-PAYMT",
                           expiry_date=date(2026, 9, 30), approval_date=date(2025, 6, 15),
                           approved_by="Legal Counsel", policy_or_standard="SOX Compliance",
                           justification="Financial reporting data must be retained per SOX; defining formal retention period",
                           owner="Legal", status="active"),
            LegalException(asset_id="LEX-003", name="COPPA Minor Data Extended Hold",
                           exception_type="legal hold", related_assets="SYS-IDGRPH, SYS-CDP",
                           expiry_date=date(2026, 12, 31), approval_date=date(2026, 1, 10),
                           approved_by="Privacy Legal", policy_or_standard="COPPA Compliance",
                           justification="Pending audit of minor deletion signal enforcement across all systems",
                           owner="Privacy", status="active"),
        ]
        db.session.add_all(exceptions)

        # --- Prior Audits ---
        audits = [
            PriorAudit(asset_id="AUD-2025Q3", name="Q3 2025 Tracker Compliance Audit",
                       audit_type="internal", audit_date=date(2025, 9, 15),
                       auditor="Data Governance", scope="All digital trackers and consent mechanisms",
                       findings_count=7, critical_findings=1,
                       remediation_due=date(2025, 12, 31), status="closed",
                       owner="Data Governance"),
            PriorAudit(asset_id="AUD-2025Q4", name="Q4 2025 Vendor Risk Assessment",
                       audit_type="internal", audit_date=date(2025, 12, 1),
                       auditor="Privacy Team", scope="All active vendors with high/critical risk",
                       findings_count=4, critical_findings=2,
                       remediation_due=date(2026, 3, 31), status="in_progress",
                       owner="Privacy"),
            PriorAudit(asset_id="AUD-2026Q1", name="Q1 2026 RIM Signal Enforcement Review",
                       audit_type="compliance", audit_date=date(2026, 2, 15),
                       auditor="Data Governance + Legal", scope="RIM/GIS delete signal flow to all downstream systems",
                       findings_count=12, critical_findings=3,
                       remediation_due=date(2026, 6, 30), status="open",
                       owner="Data Governance"),
            PriorAudit(asset_id="AUD-EY2024", name="E&Y External Privacy Audit 2024",
                       audit_type="external", audit_date=date(2024, 8, 20),
                       auditor="Ernst & Young", scope="Enterprise-wide privacy program review",
                       findings_count=15, critical_findings=2,
                       remediation_due=date(2025, 2, 28), status="closed",
                       owner="Privacy"),
        ]
        db.session.add_all(audits)

        # --- Change log entries ---
        now = datetime.utcnow()
        logs = []
        for i, v in enumerate(vendors):
            logs.append(AssetChangeLog(asset_type="vendor", asset_id=v.asset_id, action="created",
                                       changed_by="Data Governance", change_summary=f"Initial seed: {v.name}",
                                       timestamp=now - timedelta(days=30 - i)))
        for i, s in enumerate(systems):
            logs.append(AssetChangeLog(asset_type="system", asset_id=s.asset_id, action="created",
                                       changed_by="Data Governance", change_summary=f"Initial seed: {s.name}",
                                       timestamp=now - timedelta(days=28 - i)))
        for i, t in enumerate(trackers):
            logs.append(AssetChangeLog(asset_type="tracker", asset_id=t.asset_id, action="created",
                                       changed_by="Data Governance", change_summary=f"Initial seed: {t.name}",
                                       timestamp=now - timedelta(days=25 - i)))
        for i, u in enumerate(use_cases):
            logs.append(AssetChangeLog(asset_type="use_case", asset_id=u.asset_id, action="created",
                                       changed_by="Data Governance", change_summary=f"Initial seed: {u.name}",
                                       timestamp=now - timedelta(days=20 - i)))

        logs.append(AssetChangeLog(asset_type="tracker", asset_id="TRK-LEGACY", action="updated",
                                    changed_by="Privacy Team", change_summary="Marked as deprecated — pending removal",
                                    timestamp=now - timedelta(days=5)))
        logs.append(AssetChangeLog(asset_type="vendor", asset_id="VND-LEGACYX", action="updated",
                                    changed_by="Privacy Team", change_summary="Flagged for review — no DPA, expired contract",
                                    timestamp=now - timedelta(days=3)))

        db.session.add_all(logs)
        db.session.commit()

        print(f"Seeded: {len(vendors)} vendors, {len(systems)} systems, "
              f"{len(trackers)} trackers, {len(use_cases)} use cases, "
              f"{len(exceptions)} legal exceptions, {len(audits)} audits, "
              f"{len(logs)} change log entries.")


def export_json():
    """Export all database contents as a JSON blob suitable for embedding in index.html."""
    import json

    with app.app_context():
        def _date(d):
            return d.strftime("%Y-%m-%d") if d else None

        def _dt(d):
            return d.strftime("%Y-%m-%d") if d else None

        vendors = [{
            "asset_id": v.asset_id, "name": v.name, "vendor_type": v.vendor_type,
            "vendor_category": v.vendor_category, "description": v.description,
            "owner": v.owner, "risk_rating": v.risk_rating,
            "dpa_in_place": v.dpa_in_place, "contract_expiry": _date(v.contract_expiry),
            "data_shared": v.data_shared, "region": v.region, "status": v.status,
        } for v in Vendor.query.order_by(Vendor.name).all()]

        trackers = [{
            "asset_id": t.asset_id, "name": t.name, "tracker_type": t.tracker_type,
            "purpose": t.purpose, "domain_or_platform": t.domain_or_platform,
            "data_collected": t.data_collected, "placement": t.placement,
            "consent_required": t.consent_required, "owner": t.owner,
            "vendor_id": t.vendor.asset_id if t.vendor else None,
            "region": t.region, "status": t.status,
        } for t in DigitalTracker.query.order_by(DigitalTracker.name).all()]

        systems = [{
            "asset_id": s.asset_id, "name": s.name, "system_type": s.system_type,
            "description": s.description, "business_unit": s.business_unit,
            "data_classification": s.data_classification, "hosting": s.hosting,
            "pii_processed": s.pii_processed, "certifications": s.certifications,
            "owner": s.owner, "vendor_id": s.vendor.asset_id if s.vendor else None,
            "region": s.region, "status": s.status,
        } for s in System.query.order_by(System.name).all()]

        use_cases = [{
            "asset_id": u.asset_id, "name": u.name, "category": u.category,
            "subcategory": u.subcategory, "description": u.description,
            "legal_basis": u.legal_basis, "owner": u.owner, "region": u.region,
            "status": u.status, "cross_border": u.cross_border,
            "vendors": [v.asset_id for v in u.vendors],
            "trackers": [t.asset_id for t in u.trackers],
            "systems": [s.asset_id for s in u.systems],
        } for u in UseCase.query.order_by(UseCase.name).all()]

        legal_exceptions = [{
            "asset_id": e.asset_id, "name": e.name, "exception_type": e.exception_type,
            "related_assets": e.related_assets, "expiry_date": _date(e.expiry_date),
            "approval_date": _date(e.approval_date), "approved_by": e.approved_by,
            "policy_or_standard": e.policy_or_standard, "justification": e.justification,
            "owner": e.owner, "status": e.status,
        } for e in LegalException.query.order_by(LegalException.expiry_date.desc()).all()]

        prior_audits = [{
            "asset_id": a.asset_id, "name": a.name, "audit_type": a.audit_type,
            "audit_date": _date(a.audit_date), "auditor": a.auditor,
            "scope": a.scope, "findings_count": a.findings_count,
            "critical_findings": a.critical_findings,
            "remediation_due": _date(a.remediation_due),
            "status": a.status, "owner": a.owner,
        } for a in PriorAudit.query.order_by(PriorAudit.audit_date.desc()).all()]

        change_log = [{
            "asset_type": l.asset_type, "asset_id": l.asset_id,
            "action": l.action, "changed_by": l.changed_by,
            "change_summary": l.change_summary,
            "timestamp": _dt(l.timestamp),
        } for l in AssetChangeLog.query.order_by(AssetChangeLog.timestamp.desc()).all()]

        blob = {
            "vendors": vendors, "trackers": trackers, "systems": systems,
            "use_cases": use_cases, "legal_exceptions": legal_exceptions,
            "prior_audits": prior_audits, "change_log": change_log,
        }

        out = json.dumps(blob, indent=2)
        with open("kronos_data.json", "w") as f:
            f.write(out)

        print(f"Exported {len(vendors)} vendors, {len(trackers)} trackers, "
              f"{len(systems)} systems, {len(use_cases)} use cases to kronos_data.json")
        print("Paste the contents of kronos_data.json into the DATA variable in index.html to update.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--export-json":
        export_json()
    else:
        seed()
