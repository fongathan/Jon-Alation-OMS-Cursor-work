"""
Kronos — Sustainable Inventory Management UI
Supports PostgreSQL (SISU), Snowflake, or SQLite (dev).
"""

import csv
import io
import uuid
from collections import Counter
from datetime import date, datetime

from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from config import Config
from models import (
    AssetChangeLog,
    DigitalTracker,
    LegalException,
    PriorAudit,
    System,
    UseCase,
    Vendor,
    db,
    usecase_systems,
    usecase_trackers,
    usecase_vendors,
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


# ---------------------------------------------------------------------------
# Template globals
# ---------------------------------------------------------------------------

@app.context_processor
def inject_globals():
    return dict(
        db_backend=Config.DB_BACKEND,
        today=date.today(),
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MODEL_MAP = {
    "vendors": Vendor,
    "vendor": Vendor,
    "trackers": DigitalTracker,
    "tracker": DigitalTracker,
    "systems": System,
    "system": System,
    "use_cases": UseCase,
    "use_case": UseCase,
}

TYPE_LABELS = {
    "vendors": "Vendors",
    "trackers": "Digital Trackers",
    "systems": "Systems",
    "use_cases": "Business Use Cases",
}

SINGULAR_MAP = {
    "vendors": "vendor",
    "trackers": "tracker",
    "systems": "system",
    "use_cases": "use_case",
}

PREFIX_MAP = {
    "vendor": "VND",
    "tracker": "TRK",
    "system": "SYS",
    "use_case": "UC",
}


def generate_asset_id(asset_type: str) -> str:
    prefix = PREFIX_MAP.get(asset_type, "AST")
    short = uuid.uuid4().hex[:6].upper()
    return f"{prefix}-{short}"


def log_change(asset_type, asset_id, action, changed_by="Data Governance", summary=None):
    entry = AssetChangeLog(
        asset_type=asset_type,
        asset_id=asset_id,
        action=action,
        changed_by=changed_by,
        change_summary=summary,
    )
    db.session.add(entry)
    db.session.commit()


def get_related_assets(asset):
    """Return list of dicts describing related assets for any asset type."""
    related = []

    if isinstance(asset, UseCase):
        for v in asset.vendors:
            related.append(dict(type="vendor", asset_id=v.asset_id, name=v.name, status=v.status, owner=v.owner))
        for s in asset.systems:
            related.append(dict(type="system", asset_id=s.asset_id, name=s.name, status=s.status, owner=s.owner))
        for t in asset.trackers:
            related.append(dict(type="tracker", asset_id=t.asset_id, name=t.name, status=t.status, owner=t.owner))
    elif isinstance(asset, Vendor):
        for uc in asset.use_cases:
            related.append(dict(type="use_case", asset_id=uc.asset_id, name=uc.name, status=uc.status, owner=uc.owner))
        for t in asset.trackers.all():
            related.append(dict(type="tracker", asset_id=t.asset_id, name=t.name, status=t.status, owner=t.owner))
        for s in asset.systems.all():
            related.append(dict(type="system", asset_id=s.asset_id, name=s.name, status=s.status, owner=s.owner))
    elif isinstance(asset, System):
        for uc in asset.use_cases:
            related.append(dict(type="use_case", asset_id=uc.asset_id, name=uc.name, status=uc.status, owner=uc.owner))
        if asset.vendor:
            v = asset.vendor
            related.append(dict(type="vendor", asset_id=v.asset_id, name=v.name, status=v.status, owner=v.owner))
    elif isinstance(asset, DigitalTracker):
        for uc in asset.use_cases:
            related.append(dict(type="use_case", asset_id=uc.asset_id, name=uc.name, status=uc.status, owner=uc.owner))
        if asset.vendor:
            v = asset.vendor
            related.append(dict(type="vendor", asset_id=v.asset_id, name=v.name, status=v.status, owner=v.owner))

    return related


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def dashboard():
    counts = dict(
        vendors=Vendor.query.count(),
        vendors_active=Vendor.query.filter_by(status="active").count(),
        trackers=DigitalTracker.query.count(),
        trackers_active=DigitalTracker.query.filter_by(status="active").count(),
        systems=System.query.count(),
        systems_active=System.query.filter_by(status="active").count(),
        use_cases=UseCase.query.count(),
        use_cases_active=UseCase.query.filter_by(status="active").count(),
        legal_exceptions=LegalException.query.count(),
        legal_exceptions_active=LegalException.query.filter_by(status="active").count(),
        audits=PriorAudit.query.count(),
        audits_open=PriorAudit.query.filter(PriorAudit.status.in_(["open", "in_progress"])).count(),
        relationships=(
            db.session.query(usecase_vendors).count()
            + db.session.query(usecase_systems).count()
            + db.session.query(usecase_trackers).count()
        ),
    )

    # Status breakdown across all asset types
    all_statuses = []
    for model in [Vendor, DigitalTracker, System, UseCase]:
        for row in db.session.query(model.status).all():
            all_statuses.append(row[0] or "active")
    status_breakdown = dict(Counter(all_statuses))
    total_assets = len(all_statuses)

    recent_logs = AssetChangeLog.query.order_by(AssetChangeLog.timestamp.desc()).limit(10).all()
    high_risk_vendors = Vendor.query.filter(Vendor.risk_rating.in_(["high", "critical"])).all()

    return render_template(
        "dashboard.html",
        active_page="dashboard",
        counts=counts,
        status_breakdown=status_breakdown,
        total_assets=total_assets,
        recent_logs=recent_logs,
        high_risk_vendors=high_risk_vendors,
    )


@app.route("/inventory/<asset_type>")
def inventory(asset_type):
    model = MODEL_MAP.get(asset_type)
    if not model:
        return "Unknown asset type", 404

    query = model.query
    status_filter = request.args.get("status")
    if status_filter:
        query = query.filter_by(status=status_filter)
    owner_filter = request.args.get("owner")
    if owner_filter:
        query = query.filter_by(owner=owner_filter)
    if asset_type == "vendors":
        risk_filter = request.args.get("risk")
        if risk_filter:
            query = query.filter_by(risk_rating=risk_filter)

    items = query.order_by(model.name).all()
    owners = sorted({a.owner for a in model.query.with_entities(model.owner).distinct().all() if a.owner})

    return render_template(
        "inventory.html",
        active_page=asset_type,
        asset_type=asset_type,
        asset_type_singular=SINGULAR_MAP.get(asset_type, asset_type),
        type_label=TYPE_LABELS.get(asset_type, asset_type),
        items=items,
        owners=owners,
    )


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    selected_types = request.args.getlist("types")
    results = []

    example_queries = [
        "Which platforms use Adobe's systems & trackers?",
        "Trackers used for purchase propensity",
        "Vendors with high risk rating",
        "Systems that store subscriber data",
        "EMEA region use cases",
        "Consent-required trackers on Disney+",
    ]

    if query:
        search_term = f"%{query}%"

        if not selected_types or "vendor" in selected_types:
            for v in Vendor.query.filter(
                db.or_(Vendor.name.ilike(search_term), Vendor.description.ilike(search_term),
                       Vendor.vendor_category.ilike(search_term), Vendor.vendor_type.ilike(search_term))
            ).all():
                rels = len(v.use_cases) + v.trackers.count() + v.systems.count()
                results.append(dict(type="vendor", asset_id=v.asset_id, name=v.name,
                                    description=v.description, detail=v.vendor_category,
                                    status=v.status, owner=v.owner, relationships=rels))

        if not selected_types or "tracker" in selected_types:
            for t in DigitalTracker.query.filter(
                db.or_(DigitalTracker.name.ilike(search_term), DigitalTracker.purpose.ilike(search_term),
                       DigitalTracker.domain_or_platform.ilike(search_term))
            ).all():
                rels = len(t.use_cases) + (1 if t.vendor else 0)
                results.append(dict(type="tracker", asset_id=t.asset_id, name=t.name,
                                    description=t.purpose, detail=t.domain_or_platform,
                                    status=t.status, owner=t.owner, relationships=rels))

        if not selected_types or "system" in selected_types:
            for s in System.query.filter(
                db.or_(System.name.ilike(search_term), System.description.ilike(search_term),
                       System.business_unit.ilike(search_term), System.system_type.ilike(search_term))
            ).all():
                rels = len(s.use_cases) + (1 if s.vendor else 0)
                results.append(dict(type="system", asset_id=s.asset_id, name=s.name,
                                    description=s.description, detail=s.business_unit,
                                    status=s.status, owner=s.owner, relationships=rels))

        if not selected_types or "use_case" in selected_types:
            for uc in UseCase.query.filter(
                db.or_(UseCase.name.ilike(search_term), UseCase.description.ilike(search_term),
                       UseCase.category.ilike(search_term), UseCase.subcategory.ilike(search_term))
            ).all():
                rels = len(uc.vendors) + len(uc.systems) + len(uc.trackers)
                results.append(dict(type="use_case", asset_id=uc.asset_id, name=uc.name,
                                    description=uc.description, detail=uc.category,
                                    status=uc.status, owner=uc.owner, relationships=rels))

    return render_template(
        "search.html",
        active_page="search",
        query=query,
        results=results,
        selected_types=selected_types,
        example_queries=example_queries,
    )


@app.route("/asset/<asset_type>/<asset_id>")
def asset_detail(asset_type, asset_id):
    model = MODEL_MAP.get(asset_type)
    if not model:
        return "Unknown asset type", 404
    asset = model.query.filter_by(asset_id=asset_id).first_or_404()

    properties = []
    if isinstance(asset, Vendor):
        back_url = url_for("inventory", asset_type="vendors")
        properties = [
            ("Vendor Type", asset.vendor_type),
            ("Category", asset.vendor_category),
            ("Risk Rating", asset.risk_rating),
            ("DPA In Place", "Yes" if asset.dpa_in_place else "No"),
            ("Contract Expiry", asset.contract_expiry.strftime("%Y-%m-%d") if asset.contract_expiry else None),
            ("Data Shared", asset.data_shared),
            ("Subprocessors", asset.subprocessors),
        ]
    elif isinstance(asset, DigitalTracker):
        back_url = url_for("inventory", asset_type="trackers")
        properties = [
            ("Tracker Type", asset.tracker_type),
            ("Platform", asset.domain_or_platform),
            ("Purpose", asset.purpose),
            ("Data Collected", asset.data_collected),
            ("Placement", asset.placement),
            ("Consent Required", "Yes" if asset.consent_required else "No"),
            ("Retention Period", asset.retention_period),
            ("Vendor", asset.vendor.name if asset.vendor else None),
        ]
    elif isinstance(asset, System):
        back_url = url_for("inventory", asset_type="systems")
        properties = [
            ("System Type", asset.system_type),
            ("Business Unit", asset.business_unit),
            ("Data Classification", asset.data_classification),
            ("Hosting", asset.hosting),
            ("PII Processed", "Yes" if asset.pii_processed else "No"),
            ("Certifications", asset.certifications),
            ("Integrations", asset.integrations),
            ("Vendor", asset.vendor.name if asset.vendor else None),
        ]
    elif isinstance(asset, UseCase):
        back_url = url_for("inventory", asset_type="use_cases")
        properties = [
            ("Category", asset.category),
            ("Subcategory", asset.subcategory),
            ("Legal Basis", asset.legal_basis),
            ("Data Flow", asset.data_flow),
            ("Retention", asset.retention),
            ("Cross-Border", "Yes" if asset.cross_border else "No"),
        ]
    else:
        back_url = url_for("dashboard")

    related_assets = get_related_assets(asset)
    change_log = AssetChangeLog.query.filter_by(
        asset_type=asset_type, asset_id=asset_id
    ).order_by(AssetChangeLog.timestamp.desc()).limit(20).all()

    return render_template(
        "asset_detail.html",
        active_page="",
        asset=asset,
        asset_type=asset_type,
        properties=properties,
        related_assets=related_assets,
        change_log=change_log,
        back_url=back_url,
    )


@app.route("/asset/<asset_type>/<asset_id>/edit", methods=["GET", "POST"])
def edit_asset(asset_type, asset_id):
    model = MODEL_MAP.get(asset_type)
    if not model:
        return "Unknown asset type", 404
    asset = model.query.filter_by(asset_id=asset_id).first_or_404()

    if request.method == "POST":
        asset.name = request.form.get("name", asset.name)
        asset.description = request.form.get("description", asset.description)
        asset.owner = request.form.get("owner", asset.owner)
        asset.status = request.form.get("status", asset.status)
        asset.region = request.form.get("region", asset.region)
        asset.notes = request.form.get("notes", asset.notes)
        db.session.commit()
        log_change(asset_type, asset_id, "updated", summary=f"Updated fields via edit form")
        return redirect(url_for("asset_detail", asset_type=asset_type, asset_id=asset_id))

    return render_template(
        "edit_asset.html",
        active_page="",
        asset=asset,
        asset_type=asset_type,
    )


@app.route("/asset/<asset_type>/<asset_id>/deboard", methods=["POST"])
def deboard_asset(asset_type, asset_id):
    model = MODEL_MAP.get(asset_type)
    if not model:
        return "Unknown asset type", 404
    asset = model.query.filter_by(asset_id=asset_id).first_or_404()
    asset.status = "deprecated"
    db.session.commit()
    log_change(asset_type, asset_id, "deboarded", summary="Asset deboarded via portal")

    plural = {v: k for k, v in SINGULAR_MAP.items()}.get(asset_type, asset_type + "s")
    return redirect(url_for("inventory", asset_type=plural))


@app.route("/onboard", methods=["GET", "POST"])
def onboard():
    vendors = Vendor.query.order_by(Vendor.name).all()
    systems_list = System.query.order_by(System.name).all()
    trackers_list = DigitalTracker.query.order_by(DigitalTracker.name).all()
    success = None

    if request.method == "POST":
        asset_type = request.form.get("asset_type", "vendor")
        name = request.form.get("name", "").strip()
        if not name:
            flash("Name is required.", "error")
            return redirect(url_for("onboard"))

        aid = generate_asset_id(asset_type)
        common = dict(
            asset_id=aid,
            name=name,
            description=request.form.get("description", "").strip() or None,
            owner=request.form.get("owner", "").strip() or None,
            status=request.form.get("status", "active"),
            region=request.form.get("region", "").strip() or None,
            notes=request.form.get("notes", "").strip() or None,
        )

        if asset_type == "vendor":
            obj = Vendor(
                **common,
                vendor_type=request.form.get("vendor_type") or None,
                vendor_category=request.form.get("vendor_category") or None,
                risk_rating=request.form.get("risk_rating") or None,
                contract_expiry=_parse_date(request.form.get("contract_expiry")),
                dpa_in_place="dpa_in_place" in request.form,
            )
        elif asset_type == "tracker":
            obj = DigitalTracker(
                **common,
                tracker_type=request.form.get("tracker_type") or None,
                domain_or_platform=request.form.get("domain_or_platform") or None,
                purpose=request.form.get("purpose") or None,
                placement=request.form.get("placement") or None,
                consent_required="consent_required" in request.form,
                vendor_id=int(request.form["vendor_id"]) if request.form.get("vendor_id") else None,
            )
        elif asset_type == "system":
            obj = System(
                **common,
                system_type=request.form.get("system_type") or None,
                business_unit=request.form.get("business_unit") or None,
                data_classification=request.form.get("data_classification") or None,
                hosting=request.form.get("hosting") or None,
                pii_processed="pii_processed" in request.form,
                vendor_id=int(request.form["vendor_id"]) if request.form.get("vendor_id") else None,
            )
        elif asset_type == "use_case":
            obj = UseCase(
                **common,
                category=request.form.get("category") or None,
                subcategory=request.form.get("subcategory") or None,
                legal_basis=request.form.get("legal_basis") or None,
                cross_border="cross_border" in request.form,
            )
            db.session.add(obj)
            db.session.flush()

            for vid in request.form.getlist("related_vendors"):
                v = Vendor.query.get(int(vid))
                if v:
                    obj.vendors.append(v)
            for sid in request.form.getlist("related_systems"):
                s = System.query.get(int(sid))
                if s:
                    obj.systems.append(s)
            for tid in request.form.getlist("related_trackers"):
                t = DigitalTracker.query.get(int(tid))
                if t:
                    obj.trackers.append(t)
        else:
            return "Unknown asset type", 400

        if asset_type != "use_case":
            db.session.add(obj)

        db.session.commit()
        log_change(asset_type, aid, "created", summary=f"Registered via portal: {name}")
        success = f"Asset '{name}' registered as {aid}."

    return render_template(
        "onboard.html",
        active_page="onboard",
        vendors=vendors,
        systems_list=systems_list,
        trackers_list=trackers_list,
        success=success,
    )


@app.route("/relationships")
def relationships():
    sel_type = request.args.get("type", "use_case")
    sel_id = request.args.get("id", "")
    model = MODEL_MAP.get(sel_type)

    asset_options = model.query.order_by(model.name).all() if model else []

    selected_asset = None
    relationship_groups = {}
    all_relationships = []
    any_relationships = False

    if sel_id and model:
        selected_asset = model.query.filter_by(asset_id=sel_id).first()
        if selected_asset:
            all_relationships = get_related_assets(selected_asset)
            any_relationships = bool(all_relationships)
            for rel in all_relationships:
                rtype = rel["type"]
                relationship_groups.setdefault(rtype, []).append(
                    type("Obj", (), rel)()
                )

    rel_counts = dict(
        uc_vendors=db.session.query(usecase_vendors).count(),
        uc_systems=db.session.query(usecase_systems).count(),
        uc_trackers=db.session.query(usecase_trackers).count(),
    )

    return render_template(
        "relationships.html",
        active_page="relationships",
        sel_type=sel_type,
        sel_id=sel_id,
        asset_options=asset_options,
        selected_asset=selected_asset,
        relationship_groups=relationship_groups,
        all_relationships=[type("Obj", (), r)() for r in all_relationships],
        any_relationships=any_relationships,
        rel_counts=rel_counts,
    )


@app.route("/reports")
def reports():
    audits = PriorAudit.query.order_by(PriorAudit.audit_date.desc()).all()
    change_logs = AssetChangeLog.query.order_by(AssetChangeLog.timestamp.desc()).limit(50).all()
    return render_template(
        "reports.html",
        active_page="reports",
        audits=audits,
        change_logs=change_logs,
    )


@app.route("/legal-exceptions")
def legal_exceptions_view():
    exceptions = LegalException.query.order_by(LegalException.expiry_date.desc()).all()
    return render_template(
        "legal_exceptions.html",
        active_page="legal_exceptions",
        exceptions=exceptions,
    )


@app.route("/export/<asset_type>.csv")
def export_csv(asset_type):
    si = io.StringIO()
    writer = csv.writer(si)

    if asset_type == "vendors":
        writer.writerow(["ID", "Name", "Type", "Category", "Risk", "DPA", "Owner", "Status", "Contract Expiry"])
        for v in Vendor.query.order_by(Vendor.name).all():
            writer.writerow([v.asset_id, v.name, v.vendor_type, v.vendor_category,
                             v.risk_rating, v.dpa_in_place, v.owner, v.status,
                             v.contract_expiry])
    elif asset_type == "trackers":
        writer.writerow(["ID", "Name", "Type", "Platform", "Purpose", "Vendor", "Consent", "Owner", "Status"])
        for t in DigitalTracker.query.order_by(DigitalTracker.name).all():
            writer.writerow([t.asset_id, t.name, t.tracker_type, t.domain_or_platform,
                             t.purpose, t.vendor.name if t.vendor else "", t.consent_required,
                             t.owner, t.status])
    elif asset_type == "systems":
        writer.writerow(["ID", "Name", "Type", "Business Unit", "Classification", "PII", "Owner", "Status"])
        for s in System.query.order_by(System.name).all():
            writer.writerow([s.asset_id, s.name, s.system_type, s.business_unit,
                             s.data_classification, s.pii_processed, s.owner, s.status])
    elif asset_type == "use_cases":
        writer.writerow(["ID", "Name", "Category", "Subcategory", "Legal Basis", "Cross-Border", "Owner", "Status"])
        for uc in UseCase.query.order_by(UseCase.name).all():
            writer.writerow([uc.asset_id, uc.name, uc.category, uc.subcategory,
                             uc.legal_basis, uc.cross_border, uc.owner, uc.status])
    elif asset_type == "all":
        writer.writerow(["Asset Type", "ID", "Name", "Owner", "Status", "Updated"])
        for model, label in [(Vendor, "Vendor"), (DigitalTracker, "Tracker"),
                             (System, "System"), (UseCase, "UseCase")]:
            for a in model.query.all():
                writer.writerow([label, a.asset_id, a.name, a.owner, a.status, a.updated_at])
    else:
        return "Unknown asset type", 404

    output = make_response(si.getvalue())
    output.headers["Content-Type"] = "text/csv"
    output.headers["Content-Disposition"] = f"attachment; filename=kronos_{asset_type}_{date.today()}.csv"
    return output


# ---------------------------------------------------------------------------
# Edit form (simple)
# ---------------------------------------------------------------------------

@app.route("/edit/<asset_type>/<asset_id>", methods=["GET"])
def edit_asset_form(asset_type, asset_id):
    return edit_asset(asset_type, asset_id)


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Edit template (inline, simple)
# ---------------------------------------------------------------------------

@app.route("/edit-form/<asset_type>/<asset_id>", methods=["GET", "POST"])
def edit_form(asset_type, asset_id):
    return edit_asset(asset_type, asset_id)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
