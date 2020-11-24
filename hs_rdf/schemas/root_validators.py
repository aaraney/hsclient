from hs_rdf.schemas.enums import CoverageType, SpatialReferenceType, DateType
from hs_rdf.schemas.fields import SpatialReferenceInRDF
from hs_rdf.utils import to_coverage_value_string


def parse_coverages(cls, values):
    if "coverages" in values:
        return values
    if "spatial_coverage" in values or "period_coverage" in values:
        assert "coverages" not in values
        values["coverages"] = []
    if "spatial_coverage" in values:
        sc = values["spatial_coverage"]
        del values["spatial_coverage"]
        if sc:
            value = to_coverage_value_string(sc)
            cov_type = CoverageType[sc["type"]]
            values["coverages"].append({"type": cov_type, "value": value})
    if "period_coverage" in values:
        pc = values["period_coverage"]
        del values["period_coverage"]
        if pc:
            value = to_coverage_value_string(pc)
            cov_type = CoverageType.period
            values["coverages"].append({"type": cov_type, "value": value})
    return values

def parse_rdf_spatial_reference(cls, values):
    assert "spatial_reference" in values
    if isinstance(values["spatial_reference"], SpatialReferenceInRDF):
        return values
    sr = values["spatial_reference"]
    value = to_coverage_value_string(sr)
    cov_type = SpatialReferenceType[sr["type"]]
    values["spatial_reference"] = {"type": cov_type, "value": value}
    return values

def parse_rdf_dates(cls, values):
    if "dates" in values:
        return values

    dates = []
    assert "created" in values
    assert values["created"]
    dates.append({"type": DateType.created, "value": values["created"]})
    del values["created"]

    assert "modified" in values
    assert values["modified"]
    dates.append({"type": DateType.modified, "value": values["modified"]})
    del values["modified"]

    if "published" in values and values["published"]:
        dates.append({"type": DateType.published, "value": values["published"]})
        del values["published"]

    values["dates"] = dates
    return values

def parse_rdf_sources(cls, values):
    if "derived_from" in values:
        values["sources"] = [{"is_derived_from": v} for v in values["derived_from"]]
        del values["derived_from"]
    return values

def parse_rdf_extended_metadata(cls, values):
    if "additional_metadata" in values:
        em = values["additional_metadata"]
        assert isinstance(em, dict)
        values["extended_metadata"] = []
        del values["additional_metadata"]
        for key, value in em.items():
            values["extended_metadata"].append({"key": key, "value": value})
    return values

def rdf_parse_formats(cls, values):
    if "file_formats" in values:
        values["formats"] = [{"value": v} for v in values["file_formats"]]
        del values["file_formats"]
    return values

def rdf_parse_description(cls, values):
    if "abstract" in values:
        values["description"] = {"abstract": values["abstract"]}
        del values["abstract"]
    return values