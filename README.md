# Real inflection points of perturbations of concurrent lines

**Oleksiy Babanskyy** · [ORCID](https://orcid.org/0009-0001-6176-6208)

An explicit criterion for counting all real inflection points in small
perturbations of a prescribed arrangement of distinct concurrent real
lines, with constructions that control the topology of the resulting curve.

Read the [paper](paper/real_inflections_concurrent_lines.pdf)
or its [LaTeX source](paper/real_inflections_concurrent_lines.tex).

## Main results

Let n >= 3, let P be a product of n distinct real concurrent lines, and
let V be a homogeneous degree-n perturbation, nonzero at their common point.
If the real zeros of V_zz on each limiting line are simple, then every
sufficiently small nonzero real parameter gives a complex nonsingular
curve P + mu V = 0. Its ordinary real flexes correspond exactly to those
polar zeros, including projective limit points at infinity. A uniform
estimate excludes additional real flexes near the common point.

For every fixed arrangement, explicit perturbations realize:

| Degree | Attainable real flex totals |
| --- | --- |
| n even | 0, 2, ..., n(n-2) |
| n odd | n, n+2, ..., n(n-2) |

The constructions can be chosen in one rigid-isotopy class. The article
also classifies the fourteen attainable marked quartic line-count vectors,
assigns flexes to individual ovals, recovers radial and Stern families,
and gives two quartics with the same second polar but six and eight
ordinary real flexes when the simplicity condition fails.

Global existence of admissible flex totals and the complex specialization
formalism have earlier sources. The contribution developed here is the
exhaustive criterion for a fixed perturbation and its explicit constructive
use. The bibliography includes the model comparison with Breiding, Kohn
and Sturmfels and the global quartic distributions of Brugalle and Lopez
de Medrano.

## Repository layout

| Directory | Contents |
| --- | --- |
| `paper/` | The PDF, LaTeX source and bibliography, directly accessible. |
| `examples/` | Exact verification programs and their recorded results. |
| `scripts/` | The manuscript build helper. |

Temporary TeX products are kept in the ignored root-level `build/` directory.

## Read and reproduce

A short reading route is Theorems 1.1 and 1.2, Proposition 3.1, Corollary 4.2
and Section 6.3. The decisive exhaustion argument is in Section 2.

The two example checkers use exact arithmetic. With Python 3.10 or later:

    python -m pip install -r requirements.txt
    python -X utf8 examples/check_quartic.py
    python -X utf8 examples/check_extensions.py

They exit unsuccessfully if a check fails and write result JSON beside
the scripts. Expected outcomes are 9 checks for the first six-flex quartic,
5 symbolic identities, and 10 checks each for the same-polar six/eight
examples. All three fixed quartics use mu = 1/1000. Checks do not rely on
Python assertions. Timings may differ on replay.

[REPRODUCTION_RECORD.json](REPRODUCTION_RECORD.json) records the environment,
commands and result-file hashes. These finite computations supplement the
proofs; they do not certify an entire isotopy path at mu = 1/1000.

## Build the paper

Install a local TeX Live or MiKTeX distribution with pdflatex, bibtex,
lmodern, amsmath, amssymb, amsthm, mathtools, geometry, booktabs, array,
microtype, natbib, hyperref and the plainnat bibliography style. Then run:

    python -X utf8 scripts/build_manuscript.py

The helper requests no package installation. The PDF is written to
`paper/real_inflections_concurrent_lines.pdf`; logs and a source/output
digest receipt are in the ignored `build/manuscript/` directory. Python packages are needed only for the example checkers,
not for the mathematical proofs or TeX itself.

## Scope

The odd lower endpoint describes this transverse perturbation family,
not the full rigid-isotopy class. The line-count vectors cannot generally
be chosen independently. The paper gives neither a general numerical
threshold for the small parameter nor uniformity when limiting lines
collide. The four-flex-per-oval bound for quartics concerns this family,
not the global classification of quartics.

## Citation and rights

Citation metadata is in [CITATION.cff](CITATION.cff).
Original companion code and repository documentation are under
[MIT](LICENSE). The manuscript, its sources and bibliography, and the PDF
are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
as specified in [LICENSE_SCOPE.md](LICENSE_SCOPE.md).
The paper discloses substantial OpenAI Codex assistance in mathematics,
code and writing. The author reports using the most capable GPT model
available to him in Codex at the time; exact historical model-version
identifiers are not documented. AI review and finite computations do not
constitute independent specialist review or formal verification.
Third-party publications are cited and are not redistributed.
