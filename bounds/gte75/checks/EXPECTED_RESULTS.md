# Expected results of `run_all.sh`

Recorded on 2026-10-01 (Python 3.12, one core). The suite prints the last six lines of each script; the full
JSON outputs are written next to the scripts (`finite_facts.json`, `CHECK72.json`, `CHECK73.json`,
`DARK_SOURCE_VERIFIED.json`, `VERIFIED74.json`, `INDEPENDENT74.json`, `VERIFIED75.json`, `INDEPENDENT75.json`,
`stress.json`, `lp_regen_74.json`). What to look for:

| script | the line that matters |
|---|---|
| finite_facts.py | `ALL FINITE PREMISES RECOMPUTED AND MATCH` (every assertion in the script is a number of the proof note) |
| check72.py | `"minimum_two_step_increment": 3` and positive increments for G = 69, 70, 71 (file CHECK72.json) |
| check73.py | the unique non-positive-drift case a = b = 24, Y = Z = 0, and `"rank": 28` |
| check_dark_source.py | `"rank_R10": 29`, `"complete_nonzero_quotient_word_count": 736`, `"all_checks_passed": true` |
| certify74.py / independent74.py | `"all_checks_passed": true`; 262 states, 524 claims, 484 certificates, largest right side -1 |
| certify75.py / independent75.py | `"all_checks_passed": true`; 1,102 states, 2,204 claims, 4,057 certificates, 9,604 references, 927 direct, largest right side -1 |
| stress.py | `"failures": []` for the 9 circuits in `evidence/circuits/` (stress.json) |
| lp_regen.py | `survivors 0`, `claims identical 2204`, `certified keys that my LP finds feasible (must be 0): 0` |

A failed assertion in any script, or a `"failures"` list that is not empty, means a discrepancy with the note
and should be reported.

## Transcript

```
=== finite_facts.py
[   16.5s] Mt: no active six-form label has a two/four form: OK
[   16.5s] Mt: active labels meeting repeated-helper pairs: 632 max pairs per label: 1
[   31.4s] M (u,Mu) nine-part search: words 360 nodes 1485213 leaves 62112 splits found 0
[   32.6s] Mt (u,M^T u) nine-part search: words 308 nodes 91485 leaves 720 splits found 0
[   32.6s] eight-part partition exists (bit families fixed by M): OK
[   32.6s] ALL FINITE PREMISES RECOMPUTED AND MATCH
=== check72.py
          "increment": 5
        }
      ]
    }
  ]
}
=== check73.py
    "triples": 41664,
    "weight_six_relations": 84,
    "rank": 28,
    "zero_missing_zero_helper_edges_implies_y_at_least": 4
  }
}
=== check_dark_source.py
  },
  "rank_R10": 29,
  "complete_nonzero_quotient_word_count": 736,
  "inherited_source_exactly_matches": true,
  "all_checks_passed": true
}
=== certify74.py
    "missing pairs <=",
    "reverse EE budget <=",
    "weighted label capacity <="
  ],
  "all_checks_passed": true
}
=== independent74.py
  "independently_checked_coefficients": 13819,
  "largest_right_side": -1,
  "certificate_references": 1456,
  "distinct_referenced_certificates": 383,
  "all_checks_passed": true
}
=== certify75.py
    "six color packing <=",
    "unanchored required <=",
    "weighted label capacity <="
  ],
  "all_checks_passed": true
}
=== independent75.py
  "largest_right_side": -1,
  "certificate_references": 9604,
  "distinct_referenced_certificates": 3481,
  "direct_geometric_references": 927,
  "all_checks_passed": true
}
=== stress.py
    0
   ],
   1
  ]
 ]
}
=== lp_regen.py
G=74: scalar states 1102, oriented claims 2204, survivors 0, LP keys 9371, unknown 0, 4s
claims identical 2204 mine stronger/different 0 mine below certified (must be 0 unless the certified side was not reached): 0
certified keys that my LP finds feasible (must be 0): 0 []
```
