from licenseware.report_components import TableAttrs, SummaryAttrs, StyleAttrs


# pytest -s -v tests/test_report_attrs_styles.py


def test_table_attrs():

    table = TableAttrs().attr("some_column")

    print(table.metadata)

    assert "columns" in table.metadata


def test_summary_attrs():

    summary = (
        SummaryAttrs()
        .attr(
            value_key="missing_parent_details",
            value_description="Missing parent details",
            icon="Icons.FEATURES",
        )
        .attr(value_key="unknown_types")
    )

    print(summary.metadata)

    assert "series" in summary.metadata


def test_styles():

    styles = StyleAttrs().width_full

    print(styles.metadata)

    assert "width" in styles.metadata
