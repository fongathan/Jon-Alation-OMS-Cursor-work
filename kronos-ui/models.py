from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ---------------------------------------------------------------------------
# Junction / M:M association tables
# ---------------------------------------------------------------------------

usecase_systems = db.Table(
    "usecase_systems",
    db.Column("use_case_id", db.Integer, db.ForeignKey("use_cases.id"), primary_key=True),
    db.Column("system_id", db.Integer, db.ForeignKey("systems.id"), primary_key=True),
)

usecase_trackers = db.Table(
    "usecase_trackers",
    db.Column("use_case_id", db.Integer, db.ForeignKey("use_cases.id"), primary_key=True),
    db.Column("tracker_id", db.Integer, db.ForeignKey("digital_trackers.id"), primary_key=True),
)

usecase_vendors = db.Table(
    "usecase_vendors",
    db.Column("use_case_id", db.Integer, db.ForeignKey("use_cases.id"), primary_key=True),
    db.Column("vendor_id", db.Integer, db.ForeignKey("vendors.id"), primary_key=True),
)


# ---------------------------------------------------------------------------
# Core asset models
# ---------------------------------------------------------------------------

class Vendor(db.Model):
    __tablename__ = "vendors"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    vendor_type = db.Column(db.String(128))
    vendor_category = db.Column(db.String(128))
    description = db.Column(db.Text)
    owner = db.Column(db.String(128))
    contract_expiry = db.Column(db.Date)
    data_shared = db.Column(db.Text)
    dpa_in_place = db.Column(db.Boolean, default=False)
    subprocessors = db.Column(db.Text)
    risk_rating = db.Column(db.String(32))
    status = db.Column(db.String(32), default="active")
    region = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)

    trackers = db.relationship("DigitalTracker", backref="vendor", lazy="dynamic")
    systems = db.relationship("System", backref="vendor", lazy="dynamic")
    use_cases = db.relationship("UseCase", secondary=usecase_vendors, back_populates="vendors")


class DigitalTracker(db.Model):
    __tablename__ = "digital_trackers"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    tracker_type = db.Column(db.String(64))
    purpose = db.Column(db.Text)
    domain_or_platform = db.Column(db.String(256))
    data_collected = db.Column(db.Text)
    placement = db.Column(db.String(128))
    consent_required = db.Column(db.Boolean, default=True)
    retention_period = db.Column(db.String(128))
    privacy_policy_url = db.Column(db.String(512))
    owner = db.Column(db.String(128))
    status = db.Column(db.String(32), default="active")
    region = db.Column(db.String(64))
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)

    use_cases = db.relationship("UseCase", secondary=usecase_trackers, back_populates="trackers")


class System(db.Model):
    __tablename__ = "systems"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    system_type = db.Column(db.String(64))
    description = db.Column(db.Text)
    business_unit = db.Column(db.String(128))
    data_classification = db.Column(db.String(32))
    hosting = db.Column(db.String(64))
    integrations = db.Column(db.Text)
    pii_processed = db.Column(db.Boolean, default=False)
    certifications = db.Column(db.String(256))
    owner = db.Column(db.String(128))
    status = db.Column(db.String(32), default="active")
    region = db.Column(db.String(64))
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)

    use_cases = db.relationship("UseCase", secondary=usecase_systems, back_populates="systems")


class UseCase(db.Model):
    __tablename__ = "use_cases"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(128))
    subcategory = db.Column(db.String(128))
    description = db.Column(db.Text)
    data_flow = db.Column(db.Text)
    legal_basis = db.Column(db.String(128))
    retention = db.Column(db.String(128))
    cross_border = db.Column(db.Boolean, default=False)
    owner = db.Column(db.String(128))
    status = db.Column(db.String(32), default="active")
    region = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)

    vendors = db.relationship("Vendor", secondary=usecase_vendors, back_populates="use_cases")
    trackers = db.relationship("DigitalTracker", secondary=usecase_trackers, back_populates="use_cases")
    systems = db.relationship("System", secondary=usecase_systems, back_populates="use_cases")


class LegalException(db.Model):
    __tablename__ = "legal_exceptions"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    exception_type = db.Column(db.String(128))
    related_assets = db.Column(db.Text)
    expiry_date = db.Column(db.Date)
    approval_date = db.Column(db.Date)
    approved_by = db.Column(db.String(128))
    policy_or_standard = db.Column(db.String(256))
    justification = db.Column(db.Text)
    owner = db.Column(db.String(128))
    status = db.Column(db.String(32), default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)


class PriorAudit(db.Model):
    __tablename__ = "prior_audits"

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    audit_type = db.Column(db.String(64))
    audit_date = db.Column(db.Date)
    auditor = db.Column(db.String(128))
    scope = db.Column(db.Text)
    findings_count = db.Column(db.Integer, default=0)
    critical_findings = db.Column(db.Integer, default=0)
    remediation_due = db.Column(db.Date)
    report_link = db.Column(db.String(512))
    owner = db.Column(db.String(128))
    status = db.Column(db.String(32), default="closed")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)


class AssetChangeLog(db.Model):
    """Tracks every registration, update, and deboarding action for audit trail."""
    __tablename__ = "asset_change_log"

    id = db.Column(db.Integer, primary_key=True)
    asset_type = db.Column(db.String(64), nullable=False)
    asset_id = db.Column(db.String(32), nullable=False)
    action = db.Column(db.String(32), nullable=False)  # created, updated, deboarded
    changed_by = db.Column(db.String(128))
    change_summary = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
