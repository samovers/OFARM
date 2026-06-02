#!/usr/bin/env python3
import json
import hashlib
import itertools
from pathlib import Path

PATH_ALIASES = {
  "core-v1": {
    "lot.claimBasis": "Lot.claimBasis",
    "crop.seasonYear": "CropCycle.seasonYear",
    "field.zoneType": "Zone.zoneType",
    "op.kind": "OperationEvent.kind",
    "evidence.docType": "EvidenceRecord.documentType",
    "lot.sourceLot": "Lot.producedFromLot",
    "lot.assuranceScheme": "Lot.assuranceScheme",
    "lot.farmId": "Lot.farmId",
    "op.performedBy": "OperationEvent.performedBy",
    "event.observedAt": "Event.observedAt"
  },
  "core-v2": {
    "lot.claimBasis": "Lot.claimBasis",
    "crop.growingYear": "CropCycle.seasonYear",
    "zone.kind": "Zone.zoneType",
    "operation.kind": "OperationEvent.kind",
    "evidence.type": "EvidenceRecord.documentType",
    "lot.originLot": "Lot.producedFromLot",
    "lot.scheme": "Lot.assuranceScheme",
    "lot.farmIdentifier": "Lot.farmId",
    "operation.actor": "OperationEvent.performedBy",
    "event.timestamp": "Event.observedAt",
    "lot.originFarm": "Lot.originFarm"
  }
}

RELATION_ALIASES = {
  "core-v1": {
    "lot.cropCycle": "Lot.cropCycle",
    "lot.zone": "Lot.zone",
    "lot.operation": "Lot.operation",
    "op.evidence": "OperationEvent.evidence",
    "lot.sourceLot": "Lot.producedFromLot"
  },
  "core-v2": {
    "lot.crop": "Lot.cropCycle",
    "lot.fieldZone": "Lot.zone",
    "lot.performedOperation": "Lot.operation",
    "operation.evidence": "OperationEvent.evidence",
    "lot.originLot": "Lot.producedFromLot"
  }
}

SCENARIOS = [
  {
    "scenarioId": "GPE_EQ_01",
    "family": "variable-renaming-and-predicate-reorder",
    "expected": "EQUIVALENT",
    "notes": "Variable symbols and predicate order differ, but anchor, edges, and resolved predicates are the same.",
    "queryA": {
      "queryId": "q_eq_01_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "crop",
          "type": "CropCycle"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "crop",
          "relation": "lot.cropCycle",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "lot",
          "path": "lot.claimBasis",
          "op": "EQ",
          "value": "ORGANIC"
        },
        {
          "var": "crop",
          "path": "crop.seasonYear",
          "op": "EQ",
          "value": 2026
        }
      ]
    },
    "queryB": {
      "queryId": "q_eq_01_b",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "l0",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "l0",
          "type": "Lot"
        },
        {
          "var": "c0",
          "type": "CropCycle"
        }
      ],
      "edges": [
        {
          "from": "l0",
          "to": "c0",
          "relation": "lot.cropCycle",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "c0",
          "path": "crop.seasonYear",
          "op": "EQ",
          "value": 2026
        },
        {
          "var": "l0",
          "path": "lot.claimBasis",
          "op": "EQ",
          "value": "ORGANIC"
        }
      ]
    }
  },
  {
    "scenarioId": "GPE_EQ_02",
    "family": "alias-version-path-equivalence",
    "expected": "EQUIVALENT",
    "notes": "Path aliases differ across alias versions but resolve to the same canonical property paths.",
    "queryA": {
      "queryId": "q_eq_02_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "crop",
          "type": "CropCycle"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "crop",
          "relation": "lot.cropCycle",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "lot",
          "path": "lot.assuranceScheme",
          "op": "EQ",
          "value": "EU_ORGANIC"
        },
        {
          "var": "crop",
          "path": "crop.seasonYear",
          "op": "EQ",
          "value": 2026
        }
      ]
    },
    "queryB": {
      "queryId": "q_eq_02_b",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v2",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "crop",
          "type": "CropCycle"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "crop",
          "relation": "lot.crop",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "crop",
          "path": "crop.growingYear",
          "op": "EQ",
          "value": 2026
        },
        {
          "var": "lot",
          "path": "lot.scheme",
          "op": "EQ",
          "value": "EU_ORGANIC"
        }
      ]
    }
  },
  {
    "scenarioId": "GPE_EQ_03",
    "family": "branch-reordering",
    "expected": "EQUIVALENT",
    "notes": "Two required branches from the same anchor are expressed in opposite order.",
    "queryA": {
      "queryId": "q_eq_03_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "crop",
          "type": "CropCycle"
        },
        {
          "var": "zone",
          "type": "Zone"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "crop",
          "relation": "lot.cropCycle",
          "mode": "REQUIRED"
        },
        {
          "from": "lot",
          "to": "zone",
          "relation": "lot.zone",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "crop",
          "path": "crop.seasonYear",
          "op": "EQ",
          "value": 2026
        },
        {
          "var": "zone",
          "path": "field.zoneType",
          "op": "EQ",
          "value": "FIELD"
        }
      ]
    },
    "queryB": {
      "queryId": "q_eq_03_b",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v2",
      "anchors": [
        {
          "var": "l",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "l",
          "type": "Lot"
        },
        {
          "var": "z",
          "type": "Zone"
        },
        {
          "var": "c",
          "type": "CropCycle"
        }
      ],
      "edges": [
        {
          "from": "l",
          "to": "z",
          "relation": "lot.fieldZone",
          "mode": "REQUIRED"
        },
        {
          "from": "l",
          "to": "c",
          "relation": "lot.crop",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "z",
          "path": "zone.kind",
          "op": "EQ",
          "value": "FIELD"
        },
        {
          "var": "c",
          "path": "crop.growingYear",
          "op": "EQ",
          "value": 2026
        }
      ]
    }
  },
  {
    "scenarioId": "GPE_EQ_04",
    "family": "lineage-branch-equivalence",
    "expected": "EQUIVALENT",
    "notes": "Source-lot lineage is queried through different alias-version labels but the same canonical relation is used.",
    "queryA": {
      "queryId": "q_eq_04_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "src",
          "type": "Lot"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "src",
          "relation": "lot.sourceLot",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "src",
          "path": "lot.claimBasis",
          "op": "EQ",
          "value": "ORGANIC"
        }
      ]
    },
    "queryB": {
      "queryId": "q_eq_04_b",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v2",
      "anchors": [
        {
          "var": "l",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "l",
          "type": "Lot"
        },
        {
          "var": "origin",
          "type": "Lot"
        }
      ],
      "edges": [
        {
          "from": "l",
          "to": "origin",
          "relation": "lot.originLot",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "origin",
          "path": "lot.claimBasis",
          "op": "EQ",
          "value": "ORGANIC"
        }
      ]
    }
  },
  {
    "scenarioId": "GPE_EQ_05",
    "family": "operation-evidence-branch-equivalence",
    "expected": "EQUIVALENT",
    "notes": "Equivalent operation/evidence branch with renamed variables and v1/v2 alias differences.",
    "queryA": {
      "queryId": "q_eq_05_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "op",
          "type": "OperationEvent"
        },
        {
          "var": "ev",
          "type": "EvidenceRecord"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "op",
          "relation": "lot.operation",
          "mode": "REQUIRED"
        },
        {
          "from": "op",
          "to": "ev",
          "relation": "op.evidence",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "op",
          "path": "op.kind",
          "op": "EQ",
          "value": "HARVEST"
        },
        {
          "var": "ev",
          "path": "evidence.docType",
          "op": "EQ",
          "value": "WEIGH_TICKET"
        }
      ]
    },
    "queryB": {
      "queryId": "q_eq_05_b",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v2",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "operation",
          "type": "OperationEvent"
        },
        {
          "var": "evidence",
          "type": "EvidenceRecord"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "operation",
          "relation": "lot.performedOperation",
          "mode": "REQUIRED"
        },
        {
          "from": "operation",
          "to": "evidence",
          "relation": "operation.evidence",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "evidence",
          "path": "evidence.type",
          "op": "EQ",
          "value": "WEIGH_TICKET"
        },
        {
          "var": "operation",
          "path": "operation.kind",
          "op": "EQ",
          "value": "HARVEST"
        }
      ]
    }
  },
  {
    "scenarioId": "GPE_EQ_06",
    "family": "alias-version-identifier-equivalence",
    "expected": "EQUIVALENT",
    "notes": "Farm identifier aliases differ across versions but resolve to the same canonical path.",
    "queryA": {
      "queryId": "q_eq_06_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        }
      ],
      "edges": [],
      "predicates": [
        {
          "var": "lot",
          "path": "lot.farmId",
          "op": "EQ",
          "value": "farm-001"
        }
      ]
    },
    "queryB": {
      "queryId": "q_eq_06_b",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v2",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        }
      ],
      "edges": [],
      "predicates": [
        {
          "var": "lot",
          "path": "lot.farmIdentifier",
          "op": "EQ",
          "value": "farm-001"
        }
      ]
    }
  },
  {
    "scenarioId": "GPE_NEQ_01",
    "family": "optional-versus-required-edge",
    "expected": "NON_EQUIVALENT",
    "notes": "Optional edge cannot be collapsed into required edge without changing match semantics.",
    "queryA": {
      "queryId": "q_neq_01_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "crop",
          "type": "CropCycle"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "crop",
          "relation": "lot.cropCycle",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "crop",
          "path": "crop.seasonYear",
          "op": "EQ",
          "value": 2026
        }
      ]
    },
    "queryB": {
      "queryId": "q_neq_01_b",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "crop",
          "type": "CropCycle"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "crop",
          "relation": "lot.cropCycle",
          "mode": "OPTIONAL"
        }
      ],
      "predicates": [
        {
          "var": "crop",
          "path": "crop.seasonYear",
          "op": "EQ",
          "value": 2026
        }
      ]
    }
  },
  {
    "scenarioId": "GPE_NEQ_02",
    "family": "anchor-shift",
    "expected": "NON_EQUIVALENT",
    "notes": "Changing the anchor from Lot to CropCycle changes the result identity set.",
    "queryA": {
      "queryId": "q_neq_02_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "crop",
          "type": "CropCycle"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "crop",
          "relation": "lot.cropCycle",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "crop",
          "path": "crop.seasonYear",
          "op": "EQ",
          "value": 2026
        }
      ]
    },
    "queryB": {
      "queryId": "q_neq_02_b",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "crop",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "crop",
          "type": "CropCycle"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "crop",
          "relation": "lot.cropCycle",
          "mode": "REQUIRED"
        }
      ],
      "predicates": [
        {
          "var": "crop",
          "path": "crop.seasonYear",
          "op": "EQ",
          "value": 2026
        }
      ]
    }
  },
  {
    "scenarioId": "GPE_NEQ_03",
    "family": "twin-posture-shift",
    "expected": "NON_EQUIVALENT",
    "notes": "ComplianceTwin versus AdvisoryTwin is a semantic change in governed query posture.",
    "queryA": {
      "queryId": "q_neq_03_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        }
      ],
      "edges": [],
      "predicates": [
        {
          "var": "lot",
          "path": "lot.claimBasis",
          "op": "EQ",
          "value": "ORGANIC"
        }
      ]
    },
    "queryB": {
      "queryId": "q_neq_03_b",
      "twin": "AdvisoryTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        }
      ],
      "edges": [],
      "predicates": [
        {
          "var": "lot",
          "path": "lot.claimBasis",
          "op": "EQ",
          "value": "ORGANIC"
        }
      ]
    }
  },
  {
    "scenarioId": "GPE_NEQ_04",
    "family": "temporal-posture-shift",
    "expected": "NON_EQUIVALENT",
    "notes": "Current-state query posture is not equivalent to an as-observed temporal slice.",
    "queryA": {
      "queryId": "q_neq_04_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        }
      ],
      "edges": [],
      "predicates": [
        {
          "var": "lot",
          "path": "lot.claimBasis",
          "op": "EQ",
          "value": "ORGANIC"
        }
      ]
    },
    "queryB": {
      "queryId": "q_neq_04_b",
      "twin": "ComplianceTwin",
      "temporalFrame": "AS_OBSERVED_AT:2026-04-01T12:00:00Z",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        }
      ],
      "edges": [],
      "predicates": [
        {
          "var": "lot",
          "path": "lot.claimBasis",
          "op": "EQ",
          "value": "ORGANIC"
        }
      ]
    }
  },
  {
    "scenarioId": "GPE_NEQ_05",
    "family": "alias-path-drift",
    "expected": "NON_EQUIVALENT",
    "notes": "Origin farm and farm identifier are not interchangeable canonical paths.",
    "queryA": {
      "queryId": "q_neq_05_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v2",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        }
      ],
      "edges": [],
      "predicates": [
        {
          "var": "lot",
          "path": "lot.farmIdentifier",
          "op": "EQ",
          "value": "farm-001"
        }
      ]
    },
    "queryB": {
      "queryId": "q_neq_05_b",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v2",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        }
      ],
      "edges": [],
      "predicates": [
        {
          "var": "lot",
          "path": "lot.originFarm",
          "op": "EQ",
          "value": "farm-001"
        }
      ]
    }
  },
  {
    "scenarioId": "GPE_NEQ_06",
    "family": "relation-change",
    "expected": "NON_EQUIVALENT",
    "notes": "Produced-from-lot lineage is not equivalent to crop-cycle membership.",
    "queryA": {
      "queryId": "q_neq_06_a",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "src",
          "type": "Lot"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "src",
          "relation": "lot.sourceLot",
          "mode": "REQUIRED"
        }
      ],
      "predicates": []
    },
    "queryB": {
      "queryId": "q_neq_06_b",
      "twin": "ComplianceTwin",
      "temporalFrame": "CURRENT_STATE",
      "aliasVersionRef": "core-v1",
      "anchors": [
        {
          "var": "lot",
          "role": "PRIMARY"
        }
      ],
      "nodes": [
        {
          "var": "lot",
          "type": "Lot"
        },
        {
          "var": "crop",
          "type": "CropCycle"
        }
      ],
      "edges": [
        {
          "from": "lot",
          "to": "crop",
          "relation": "lot.cropCycle",
          "mode": "REQUIRED"
        }
      ],
      "predicates": []
    }
  }
]

def resolve_path(alias_version, path):
    return PATH_ALIASES.get(alias_version, {}).get(path, path)

def resolve_relation(alias_version, relation):
    return RELATION_ALIASES.get(alias_version, {}).get(relation, relation)

def normalize_value(value):
    if isinstance(value, list):
        return [normalize_value(v) for v in sorted(value, key=lambda x: json.dumps(x, sort_keys=True))]
    if isinstance(value, dict):
        return {k: normalize_value(value[k]) for k in sorted(value)}
    return value

def canonicalize_query(query):
    nodes = {n["var"]: n["type"] for n in query["nodes"]}
    type_groups = {}
    for var, typ in nodes.items():
        type_groups.setdefault(typ, []).append(var)
    type_order = sorted(type_groups)
    perm_iters = [list(itertools.permutations(sorted(type_groups[t]))) for t in type_order]

    best_txt = None
    best_payload = None
    for combo in itertools.product(*perm_iters):
        mapping = {}
        for typ, perm in zip(type_order, combo):
            for idx, var in enumerate(perm, start=1):
                mapping[var] = f"{typ}#{idx}"

        anchors = sorted((mapping[a["var"]], a.get("role", "PRIMARY")) for a in query["anchors"])
        edges = sorted(
            (
                mapping[e["from"]],
                resolve_relation(query["aliasVersionRef"], e["relation"]),
                mapping[e["to"]],
                e.get("mode", "REQUIRED"),
            )
            for e in query["edges"]
        )
        predicates = sorted(
            (
                mapping[p["var"]],
                resolve_path(query["aliasVersionRef"], p["path"]),
                p["op"],
                normalize_value(p["value"]),
            )
            for p in query["predicates"]
        )

        payload = {
            "twin": query["twin"],
            "temporalFrame": query["temporalFrame"],
            "anchors": anchors,
            "edges": edges,
            "predicates": predicates,
        }
        txt = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        if best_txt is None or txt < best_txt:
            best_txt = txt
            best_payload = payload

    signature = hashlib.sha256(best_txt.encode("utf-8")).hexdigest()[:16]
    return signature, best_payload

def main():
    here = Path(__file__).resolve().parent

    equivalence_records = []
    non_equivalence_records = []
    canonical_forms = []
    telemetry = []

    for scenario in SCENARIOS:
        sig_a, canon_a = canonicalize_query(scenario["queryA"])
        sig_b, canon_b = canonicalize_query(scenario["queryB"])

        observed = "EQUIVALENT" if sig_a == sig_b else "NON_EQUIVALENT"
        status = "PASS" if observed == scenario["expected"] else "FAIL"

        telemetry.extend([
            {
                "eventId": f"telemetry-{len(telemetry)+1:03d}",
                "kind": "ALIAS_RESOLUTION_APPLIED",
                "scenarioId": scenario["scenarioId"],
                "queryId": scenario["queryA"]["queryId"],
                "aliasVersionRef": scenario["queryA"]["aliasVersionRef"],
            },
            {
                "eventId": f"telemetry-{len(telemetry)+2:03d}",
                "kind": "GRAPH_CANONICALIZED",
                "scenarioId": scenario["scenarioId"],
                "queryId": scenario["queryA"]["queryId"],
                "canonicalSignature": sig_a,
            },
            {
                "eventId": f"telemetry-{len(telemetry)+3:03d}",
                "kind": "ALIAS_RESOLUTION_APPLIED",
                "scenarioId": scenario["scenarioId"],
                "queryId": scenario["queryB"]["queryId"],
                "aliasVersionRef": scenario["queryB"]["aliasVersionRef"],
            },
            {
                "eventId": f"telemetry-{len(telemetry)+4:03d}",
                "kind": "GRAPH_CANONICALIZED",
                "scenarioId": scenario["scenarioId"],
                "queryId": scenario["queryB"]["queryId"],
                "canonicalSignature": sig_b,
            },
            {
                "eventId": f"telemetry-{len(telemetry)+5:03d}",
                "kind": "GRAPH_PATTERN_EQUIVALENCE_EVALUATED",
                "scenarioId": scenario["scenarioId"],
                "expected": scenario["expected"],
                "observed": observed,
                "status": status,
            },
        ])

        canonical_forms.extend([
            {
                "scenarioId": scenario["scenarioId"],
                "queryId": scenario["queryA"]["queryId"],
                "canonicalSignature": sig_a,
                "canonicalForm": canon_a,
            },
            {
                "scenarioId": scenario["scenarioId"],
                "queryId": scenario["queryB"]["queryId"],
                "canonicalSignature": sig_b,
                "canonicalForm": canon_b,
            },
        ])

        record = {
            "scenarioId": scenario["scenarioId"],
            "family": scenario["family"],
            "expected": scenario["expected"],
            "observed": observed,
            "status": status,
            "notes": scenario["notes"],
            "queryAId": scenario["queryA"]["queryId"],
            "queryBId": scenario["queryB"]["queryId"],
            "canonicalSignatureA": sig_a,
            "canonicalSignatureB": sig_b,
            "canonicalFormA": canon_a,
            "canonicalFormB": canon_b,
        }
        if observed == "EQUIVALENT":
            record["sharedCanonicalForm"] = canon_a

        if scenario["expected"] == "EQUIVALENT":
            equivalence_records.append(record)
        else:
            non_equivalence_records.append(record)

    overall = "PASS_WITH_LIMITATIONS" if all(r["status"] == "PASS" for r in equivalence_records + non_equivalence_records) else "FAIL"

    results = {
        "wave": 22,
        "title": "OFARM runtime graph-pattern equivalence results v0.1",
        "overallStatus": overall,
        "pairScenariosChecked": len(SCENARIOS),
        "equivalencePairs": len(equivalence_records),
        "nonEquivalencePairs": len(non_equivalence_records),
        "queryVariantsNormalized": len(canonical_forms),
        "canonicalFormsEmitted": len(canonical_forms),
        "telemetryEvents": len(telemetry),
        "familiesCovered": sorted({scenario["family"] for scenario in SCENARIOS}),
        "limitations": [
            "The suite works over a package-local normalized internal query-fragment subset rather than full QuerySpecification executor integration.",
            "This wave closes graph-pattern equivalence, not execution-target equivalence; target-plan semantic-equivalence remains a separate row.",
            "Alias resolution here is bounded to package-local fixture catalogs and does not yet prove deployment-produced alias telemetry or saved-query regression.",
        ],
    }

    (here / "OFARM_runtime_graph_pattern_equivalence_records_v0_1.json").write_text(json.dumps(equivalence_records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (here / "OFARM_runtime_graph_pattern_non_equivalence_records_v0_1.json").write_text(json.dumps(non_equivalence_records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (here / "OFARM_runtime_graph_pattern_canonical_forms_v0_1.json").write_text(json.dumps(canonical_forms, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (here / "OFARM_runtime_graph_pattern_equivalence_telemetry_v0_1.json").write_text(json.dumps(telemetry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (here / "OFARM_runtime_graph_pattern_equivalence_results_v0_1.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
