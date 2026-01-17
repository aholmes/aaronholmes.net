.. meta::
    :date: 2025-12-15

Interview Coding Take-Homes: Part 3
===================================

|pagedate|

.. tags:: Programming, Software, Interviewing

UCLA Health - Population Analysis
----------------------------------

This take-home was about the data ingestion and cleaning population data.
The goal was to take messy JSON from an API and turn it
into a clean CSV, so the analysis and visualization could focus on the real
questions without getting bogged down in data cleanup.

Goals
-----

- Produce a CSV with a fixed header order and stable types.
- Keep each transformation small and unit-testable.
- Fail fast on missing required fields and log useful diagnostics.

Why this approach
-----------------

Even though the dataset was small and straightforward, it had all the typical
real-world issues: keys with spaces, inconsistent casing, and numbers as
strings. Instead of using heavy tools, I focused on keeping things clear,
with predictable output and a simple flow I could easily follow.

Repository
----------

The implementation is in the `population-analysis` repo
under the `Analysis/` directory. See the source and examples at:

`population-analysis (Analysis) <https://github.com/aholmes/population-analysis/tree/aba1e5330fabbd1df162d00770b853b4838f1cae/Analysis>`_

Process overview
----------------

1. Load JSON from the API or from the cached sample used in tests.
2. Rename and normalize keys so everything aligns with the internal schema.
3. Coerce types (strings -> ints/dates) and fail if required data is missing.
4. Emit two CSVs: one raw mapping for auditing and one cleaned file for analysis.

Key implementation details
--------------------------

Handling messy JSON keys
^^^^^^^^^^^^^^^^^^^^^^^^

The prompt demanded a tight mapping between API fields and output columns.
Because the API returns keys with spaces and wobbly casing, the data model
leans on ``[JsonPropertyName]`` attributes to translate them into clean C#
properties:

.. scrollable::

    .. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_3/Analysis/APIModels/PopulationEntry.cs
        :language: csharp
        :linenos:
        :lines: 15-23
        :dedent:
        :caption: :download:`PopulationEntry.cs <../_static/files/2025/interview_coding_take_homes_part_3/Analysis/APIModels/PopulationEntry.cs>`

This keeps the mapping explicit and makes it obvious which API field feeds
each column.

Fetching and caching the data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The application calls the public census API, but I do not re-fetch on every
test run. Instead the client caches the payload locally so the API stays quiet
while I iterate:

.. scrollable::

    .. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_3/Analysis/Api.cs
        :language: csharp
        :linenos:
        :lines: 76-81
        :dedent:
        :caption: :download:`Api.cs <../_static/files/2025/interview_coding_take_homes_part_3/Analysis/Api.cs>`

On a fresh pull, the JSON hits disk before deserialization. That keeps the
workflow testable and reinforces a clean separation of concerns:

.. scrollable::

    .. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_3/Analysis/Api.cs
        :language: csharp
        :linenos:
        :lines: 85-97
        :dedent:
        :caption: :download:`Api.cs <../_static/files/2025/interview_coding_take_homes_part_3/Analysis/Api.cs>`

Example input (trimmed)
-----------------------

This is an example of the API shape-keys with spaces, mixed casing, and numeric
types that arrive as JSON numbers.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_3/Analysis/sample_input.json
    :language: json
    :linenos:
    :caption: :download:`sample_input.json <../_static/files/2025/interview_coding_take_homes_part_3/Analysis/sample_input.json>`

The ingest pipeline renames those columns to ``id``, ``state``, ``slug``, etc.,
and asserts that the types stay stable before writing the normalized CSV.

Normalized CSV (representative rows)
------------------------------------

The cleaned CSV fixes the header order and uses explicit types. Representative
rows:

.. code-block:: text

    id,state,slug,year,population
    04000US01,Alabama,alabama,2023,5054253
    04000US02,Alaska,alaska,2023,733971

Notes on implementation
-----------------------

- API keys such as ``"ID State"`` and ``"Slug State"`` map to canonical names
  (``id``, ``slug``) so downstream code never reasons about the raw schema.
- Validation is blunt by design: missing required fields fail the run; weird
  values get logged for inspection instead of disappearing quietly.
- Every time a new API field appeared, I did the same ritual: dump a single
  response to disk, diff it against the schema, and verify the mapping by
  regenerating the CSV. That quick loop kept regressions visible without a
  ton of ceremony.

Testing and verification
------------------------

Testing the pipeline
^^^^^^^^^^^^^^^^^^^^

Before trusting the CSV, I walk through the same routine I use on most
take-homes: run the automated suite, then spot-check the binary output.

.. code-block:: console

    $ cd population-analysis
    $ dotnet test

The tests live in ``population-analysis/Test`` and use xUnit + Moq. They verify
that the ingestion pipeline does what I expect even when the API or filesystem
behaves badly.

What the tests cover
^^^^^^^^^^^^^^^^^^^^

- :download:`Test/AnalysisApi.cs <../_static/files/2025/interview_coding_take_homes_part_3/Test/AnalysisApi.cs>` drives the API client through both code paths. It
  ensures cached payloads short-circuit HTTP calls, verifies that cache files
  are written before parsing, and checks that failures log meaningful errors.
- :download:`Test/AnalysisReport.cs <../_static/files/2025/interview_coding_take_homes_part_3/Test/AnalysisReport.cs>` exercises the aggregation layer. It confirms that
  populations group by state/year, headers stay deterministic, sorted tables
  behave, and the factor column lines up with each year.
- :download:`Test/AnalysisReport.cs <../_static/files/2025/interview_coding_take_homes_part_3/Test/AnalysisReport.cs>` also reflection-loads the ``Report`` helpers so I
  can assert on the tables without spinning up the CLI.

Manual sanity checks
^^^^^^^^^^^^^^^^^^^^

Automated tests catch regressions, but I still run a quick end-to-end pass to
see the CSV with my own eyes:

.. code-block:: console

   $ cd population-analysis
   $ dotnet run --project Analysis/Analysis.csproj
   Enter a path to write the CSV file to:

I point it at :download:`population.csv <../_static/files/2025/interview_coding_take_homes_part_3/report/population.csv>`,
inspect the generated CSV/raw pair, and spot-check a few rows against the
original JSON. When a slug or population looks wrong, I can walk back through
the normalization rules immediately.

Running with Docker
^^^^^^^^^^^^^^^^^^^

If you prefer not to set up .NET locally, the application also runs in a
Docker container. The image is multi-arch and supports both AMD64 and ARM64,
so it should work on most systems.

Pull and run it like this:

.. code-block:: console

    $ docker run \
    >    -u $(id -u):$(id -g) \
    >    -v /path/to/output/directory:/csv_destination \
    >    --rm -it \
    >    aholmes0/population-analysis:latest

This mounts a local directory to ``/csv_destination`` inside the container,
where the CSV files get written. The ``-u`` flag runs as your user ID to avoid
permission issues with the output files.

Tradeoffs
---------

- The pipeline favors clarity and observability over extreme throughput. It
  assumes the dataset fits on one machine without drama.
- Formal schema enforcement (JSON Schema, etc.) would help for larger teams,
  but I skipped it here to keep iteration fast.

Analysis and findings
---------------------

With the cleaned CSV ready, I shifted into exploration mode. The dataset spans
multiple years across every U.S. state and territory, so it is a natural fit
for trend comparisons. The headline question people kept asking was:
**Are Californians moving to Texas?** Rather than lean on anecdotes, I ran the
numbers.

Key steps:

- Compute year-over-year population changes per state.
- Normalize growth rates with z-scores and compare peers head-to-head.
- Flag periods where migration signals diverged.
- Plot each view so the story is obvious without reading code.

Result: both California and Texas keep growing, and their growth curves tend
to move in tandem. That implies broader economic or demographic drivers
rather than a one-way California -> Texas pipeline.

Testing the idea
^^^^^^^^^^^^^^^^

I do not accept charts at face value, so I poked at the data from a few angles:

- **Cross-check the raw counts.** Before normalizing, I spot-checked California
  and Texas populations against the Census CSV to ensure the ingest layer did
  not mangle digits. Having the raw CSV beside the formatted one made this
  painless.
- **Validate the story with multiple transforms.** The z-score plot highlights
  divergences, but I also built the rank-change visualization to confirm the
  same periods popped out. If two independent views disagree, the notebook
  gets deleted.
- **Interrogate the edges.** Whenever a state's growth looked extreme, I
  tracked it back to the underlying rows to see if the spike came from a real
  trend or a data glitch. That habit kept the write-up grounded in facts, not
  vibes.

Output and visualization
^^^^^^^^^^^^^^^^^^^^^^^^

The cleaned population data:

.. scrollable::

    .. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_3/report/population.csv
        :language: text
        :linenos:
        :lines: 1-10
        :caption: :download:`population.csv (first 10 rows) <../_static/files/2025/interview_coding_take_homes_part_3/report/population.csv>`



Key analysis code blocks and observations:

Helper Functions for Analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before diving into visualizations, I defined helper classes and functions to
handle the data transformations consistently across plots.

.. scrollable::

    .. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_3/report/notebook_block_03.py
        :language: python
        :linenos:
        :lines: 1-62
        :caption: FillData class and zscore helper functions

Year-over-Year Change Analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first visualization examines year-over-year population changes, normalized
by z-scores to compare states on the same scale. The plot highlights periods
where California and Texas growth rates diverged significantly, using filled
areas and arrows to mark those intervals.

.. scrollable::

    .. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_3/report/notebook_block_04.py
        :language: python
        :linenos:
        :lines: 1-15
        :caption: YoY change calculation and plotting

.. image:: /_static/images/2025/interview_coding_take_homes_part_3/yoy_plot.svg
   :alt: Year-over-year population change plot with z-score normalization
   :align: center

Rank Change Visualization
^^^^^^^^^^^^^^^^^^^^^^^^^

This plot shows how states' population ranks shifted from 2013 to 2022, with
bars representing 2022 populations and curved arrows indicating rank changes.
States that moved up or down in ranking are highlighted with colored bars and
connecting arcs.

.. scrollable::

    .. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_3/report/notebook_block_05.py
        :language: python
        :linenos:
        :lines: 1-45
        :caption: Rank change plotting with custom legend handler

.. image:: /_static/images/2025/interview_coding_take_homes_part_3/rank_change_plot.svg
   :alt: Population rank change visualization with arrows
   :align: center

Average Annual Growth Rate Map
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The final visualization maps average annual growth rates across all states
using a color gradient, with vertical markers for California and Texas. The
horizontal color bar provides context for the growth spectrum from highest
growth to population loss.

.. scrollable::

    .. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_3/report/notebook_block_06.py
        :language: python
        :linenos:
        :lines: 1-32
        :caption: Gradient colormap visualization

.. image:: /_static/images/2025/interview_coding_take_homes_part_3/gradient_plot.svg
   :alt: Average annual growth rate gradient map
   :align: center

The full analysis including charts and findings is available in the Jupyter notebook:

:download:`PopulationAnalysis.ipynb <../_static/files/2025/interview_coding_take_homes_part_3/report/PopulationAnalysis.ipynb>`

Conclusion
----------

In the end, this take-home took raw JSON and turned it into a clean CSV by
breaking it down into small, clear steps. That makes it simple to test and
audit, and gets you ready for the analysis. The practical approach-caching to
skip repeated API calls, clear key mappings, and straightforward validation-
shows good thinking and communication, not unnecessary complexity.

|cta|
|disqus|
