import time
from typing import Literal, Callable, Any

import pandas as pd

from .constants import OPENTARGETS_GRAPHQL_API
from .utils import set_up_logger, wrap_cols_func, graphql_query, json_list_to_df

logger = set_up_logger()


def opentargets(
    ensembl_id: str,
    resource: Literal["diseases", "drugs", "tractability", "pharmacogenetics", "expression"] = "diseases",
    limit: int | None = None,
    verbose: bool = True,
    wrap_text: bool = False,
) -> pd.DataFrame:
    """
    Query OpenTargets for data associated with a given Ensembl gene ID.

    Args:

    - ensembl_id    Ensembl gene ID to be queried (str), e.g. "ENSG00000169194".
    - resource      Defines type of information to be returned.
                    "diseases":         Returns diseases associated with the gene (default).
                    "drugs":            Returns drugs associated with the gene.
                    "tractability":     Returns tractability data for the gene.
                    "pharmacogenetics": Returns pharmacogenetics data for the gene.
                    "expression":       Returns gene expression data (by tissues, organs, and anatomical systems).
    - limit         Limit the number of results returned (default: No limit).
    - verbose       Print progress messages (default: True).
    - wrap_text     If True, displays data frame with wrapped text for easy reading. Default: False.

    Returns requested information in DataFrame format.
    """

    # check if resource argument is valid
    if resource not in _RESOURCES:
        raise ValueError(
            f"'resource' argument specified as {resource}. Expected one of: {', '.join(_RESOURCES)}"
        )

    return _RESOURCES[resource](
        ensembl_id, limit=limit, verbose=verbose, wrap_text=wrap_text
    )


def _limit_pagination() -> tuple[str, str, callable]:
    """
    Limit is expressed as (page: {"index": 0, "size": limit}).
    """
    def f(limit: int | None, is_rows_based_query: bool):
        if limit is None:
            # special case because `None` is used to probe the total count
            if is_rows_based_query:
                limit = 1
            else:
                return None
        return {"index": 0, "size": limit}
    return "page", "Pagination", f


def _limit_size() -> tuple[str, str, callable]:
    """
    Limit is expressed as (size: limit).
    """
    def f(limit: int | None, is_rows_based_query: bool):
        # special case because `None` is used to probe the total count
        if limit is None and is_rows_based_query:
            limit = 1
        return limit
    return "size", "Int", f


def _limit_not_supported() -> tuple[None, None, callable]:
    """
    Limit is not supported for this resource (it has no GraphQL-support, and it is meaningless).
    """
    def f(limit: int | None, _is_rows_based_query: bool):
        if limit is not None:
            raise ValueError("Limit is not supported for this resource.")
        return None

    return None, None, f


def _limit_deferred() -> tuple[None, None, callable]:
    """
    Limit is handled after fetching the data (it is not supported by the GraphQL query, but does have meaning).
    """
    def f(_limit: int | None, _is_rows_based_query: bool):
        return None

    return None, None, f


def _tractability_converter(row: dict[str, ...]):
    _modality_map = {
        "SM": "Small molecule",
        "AB": "Antibody",
        "PR": "PROTAC",
        "OC": "Other",
    }
    row["modality"] = _modality_map.get(row["modality"], row["modality"])


def _pharmacogenetics_converter(row: dict[str, ...]):
    # need to modify the drugs field to parse it into a dataframe
    drugs = row["drugs"]
    drugs_df = json_list_to_df(drugs, [("id", "drugId"), ("name", "drugFromSource")])
    row["drugs"] = drugs_df


def _make_query_fun(
    top_level_key: str,
    inner_query: str,
    human_readable_tlk: str,
    df_schema: list[tuple[str, str]],
    wrap_columns: list[str],
    limit_func: callable,
    is_rows_based_query: bool = True,
    sorter: Callable[[dict[str, ...]], Any] | None = None,
    sort_reverse: bool = False,
    filter_: Callable[[dict[str, ...]], bool] = lambda x: True,
    converter: Callable[[dict[str, ...]], None] = lambda x: None,
) -> callable:
    """
    Make a query function for OpenTargets API.

    Args:

    - top_level_key         Top level key in the GraphQL query response, e.g. "associatedDiseases".
    - inner_query           Query string for the row data, e.g. "score disease{id name description}".
    - human_readable_tlk    Human readable version of the top level key, e.g. "associated diseases".
    - df_schema             Schema for the DataFrame, e.g. [("id", "disease.id"), ("name", "disease.name")].
    - wrap_columns          Columns to wrap text for easy reading, e.g. ["description"].
    - limit_func            Function to convert a limit into a pagination variable.
    - is_rows_based_query   If True, the query is wrapped inside `count rows{query}`.
    - sorter                Function to sort the raw data before it is limited, filtered, or converted.
                            Note: you may want to use `_limit_deferred`, otherwise the limit will be
                            applied through GraphQL before sorting.
    - sort_reverse          If True, sort in reverse order.
    - filter_               Function to filter the raw data (return False to skip value).
                            Note: applied after limit but before converter.
    - converter             Function to optionally manipulate the raw data IN PLACE before it is converted to a DataFrame.

    Returns a function that queries the OpenTargets API and returns the data in DataFrame format.
    """

    limit_key, limit_type, limit_func = limit_func()

    def fun(
        ensembl_id: str,
        limit: int | None = None,
        verbose: bool = True,
        wrap_text: bool = False,
    ) -> pd.DataFrame:
        if limit_key is None:
            query_string = """
            query target($ensemblId: String!) {
                target(ensemblId: $ensemblId) {
                    <TOP_LEVEL_KEY>{
                        <ROW_QUERY>
                    }
                }
            }
            """.replace(
                "<TOP_LEVEL_KEY>", top_level_key
            ).replace(
                "<ROW_QUERY>", inner_query
            )
        else:
            if is_rows_based_query:
                query_tmp = """
                count
                rows{
                    <INNER_QUERY>
                }""".replace("<INNER_QUERY>", inner_query)
            else:
                query_tmp = inner_query
            query_string = """
            query target($ensemblId: String!, $pagination: <LIMIT_TYPE>) {
                target(ensemblId: $ensemblId) {
                    <TOP_LEVEL_KEY>(<LIMIT_KEY>: $pagination){
                        <QUERY>
                    }
                }
            }
            """.replace(
                "<TOP_LEVEL_KEY>", top_level_key
            ).replace(
                "<LIMIT_TYPE>", limit_type
            ).replace(
                "<LIMIT_KEY>", limit_key
            ).replace(
                "<QUERY>", query_tmp
            )

        pagination = limit_func(limit, is_rows_based_query)
        variables = {"ensemblId": ensembl_id, "pagination": pagination}

        if limit_key is None:
            del variables["pagination"]

        results = graphql_query(OPENTARGETS_GRAPHQL_API, query_string, variables)
        target: dict[str, ...] = results["data"]["target"]
        if target is None:
            raise ValueError(
                f"No data found for Ensembl ID: {ensembl_id}. Please double-check the ID and try again."
            )
        data: dict[str, ...] = target[top_level_key]

        if is_rows_based_query:
            total_count: int = data["count"]
            rows: list[dict[str, ...]] = data["rows"]
        else:
            # noinspection PyTypeChecker
            rows: list[dict[str, ...]] = data
            total_count = len(data)

        if verbose:
            explanation = ""
            if limit is None and limit_key is not None and is_rows_based_query:
                explanation = " (Querying count, will fetch all results next.)"
            logger.info(
                f"Retrieved {len(rows)}/{total_count} {human_readable_tlk}.{explanation}"
            )

        if limit is None and limit_key is not None and is_rows_based_query:
            # wait 1 second as a courtesy
            time.sleep(1)
            variables["pagination"] = limit_func(total_count, is_rows_based_query)

            new_results = graphql_query(
                OPENTARGETS_GRAPHQL_API, query_string, variables
            )
            new_data: dict[str, ...] = new_results["data"]["target"][top_level_key]
            new_rows: list[dict[str, ...]] = new_data["rows"]
            # we re-fetched the original 1, so we need to replace them
            rows = new_rows
            if verbose:
                logger.info(
                    f"Retrieved {len(rows)}/{total_count} {human_readable_tlk}."
                )

        if sorter is not None:
            rows.sort(key=sorter, reverse=sort_reverse)

        if limit is not None:
            rows = rows[:limit]

        rows = [row for row in rows if filter_(row)]
        for row in rows:
            converter(row)

        df = json_list_to_df(
            rows,
            df_schema,
        )

        if wrap_text:
            df_wrapped = df.copy()
            wrap_cols_func(df_wrapped, wrap_columns)

        return df

    return fun


_RESOURCES = {
    "diseases": _make_query_fun(
        "associatedDiseases",
        """
        score
        disease{
            id
            name
            description
        }""",
        "associated diseases",
        [
            ("id", "disease.id"),
            ("name", "disease.name"),
            ("description", "disease.description"),
            ("score", "score"),
        ],
        ["description"],
        _limit_pagination,
    ),

    "drugs": _make_query_fun(
        "knownDrugs",
        """
        # Basic drug data
        drugId
        prefName
        drugType
        mechanismOfAction
        # Disease data
        disease{
            id
            name
        }
        # Clinical trial data
        phase
        status
        ctIds
        # More drug data
        drug{
            synonyms
            tradeNames
            description
            isApproved
        }
        """,
        "known drugs",
        [
            # Drug data
            ("id", "drugId"),
            ("name", "prefName"),
            ("type", "drugType"),
            ("action_mechanism", "mechanismOfAction"),
            ("description", "drug.description"),
            ("synonyms", "drug.synonyms"),
            ("trade_names", "drug.tradeNames"),
            # Disease data
            ("disease_id", "disease.id"),
            ("disease_name", "disease.name"),
            # Trial data
            ("trial_phase", "phase"),
            ("trial_status", "status"),
            ("trial_ids", "ctIds"),
            ("approved", "drug.isApproved"),
        ],
        ["description", "synonyms", "trade_names", "trial_ids"],
        _limit_size,
    ),

    "tractability": _make_query_fun(
        "tractability",
        """
        label
        modality
        value
        """,
        "tractability states",
        [
            ("label", "label"),
            ("modality", "modality"),
        ],
        [],
        _limit_not_supported,
        filter_=lambda x: x["value"],
        converter=_tractability_converter,
        is_rows_based_query=False
    ),
    "pharmacogenetics": _make_query_fun(
        "pharmacogenomics",
        """
        variantRsId
        
        genotypeId
        genotype
        
        variantFunctionalConsequence{
            id
            label
        }
        
        drugs{
            drugId
            drugFromSource
        }
        phenotypeText
        genotypeAnnotationText
        
        pgxCategory
        isDirectTarget
        
        evidenceLevel
        
        datasourceId
        literature
        """,
        "pharmacogenetic responses",
        [
            ("rs_id", "variantRsId"),

            ("genotype_id", "genotypeId"),
            ("genotype", "genotype"),

            ("variant_consequence_id", "variantFunctionalConsequence.id"),
            ("variant_consequence_label", "variantFunctionalConsequence.label"),

            ("drugs", "drugs"), # this is processed into a DataFrame by the converter

            ("phenotype", "phenotypeText"),
            ("genotype_annotation", "genotypeAnnotationText"),

            ("response_category", "pgxCategory"),
            ("direct_target", "isDirectTarget"),

            ("evidence_level", "evidenceLevel"),

            ("source", "datasourceId"),
            ("literature", "literature"),
        ],
        ["phenotype", "genotype_annotation"],
        _limit_pagination,
        is_rows_based_query=False,
        converter=_pharmacogenetics_converter,
    ),

    "expression": _make_query_fun(
        "expressions",
        """
        tissue{
            id
            label
            anatomicalSystems
            organs
        }
        rna{
            zscore
            value
            unit
            level
        }
        """,
        "baseline expressions",
        [
            ("tissue_id", "tissue.id"),
            ("tissue_name", "tissue.label"),
            ("rna_zscore", "rna.zscore"),
            ("rna_value", "rna.value"),
            ("rna_unit", "rna.unit"),
            ("rna_level", "rna.level"),
            ("anatomical_systems", "tissue.anatomicalSystems"),
            ("organs", "tissue.organs"),
        ],
        ["tissue_name", "anatomical_systems", "organs"],
        _limit_deferred,
        is_rows_based_query=False,
        sorter=lambda x: (x["rna"]["value"], x["rna"]["zscore"]),
        sort_reverse=True,
    )
}

OPENTARGETS_RESOURCES = list(_RESOURCES.keys())
