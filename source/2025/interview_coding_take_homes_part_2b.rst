.. meta::
    :date: 2025-08-28

Interview Coding Take-Homes: Part 2.b
=====================================

|pagedate|

.. tags:: Programming, Software, Interviewing

UCLA Health - Terraform Module
------------------------------

This take-home was for a Senior Cloud DevOps Engineer position in a key IT organization at UCLA Health.

This is part **b** of a two-part take-home. Read the first part, :ref:`Interview Coding Take-Homes: Part 2.a`.

Prompt
------

.. pull-quote::

    You are a terraform developer building a new module to help with naming
    resources deployed within the cloud environment. You will have two inputs
    to this module identifying a "base_name" and "resource_type" with which
    you will have to evaluate and generate a "resource_name" as an output.
    The "resource_name" that you generate should follow these rules:

    1. You should setup the "resource_type" to only allow the values of
       "virtual_machine", "key_vault", and "storage_account"
    2. If the resource_type is "virtual_machine" you should take the
       "base_name" and append "vm-" to the front of it and "-00" to the back.
       If the base name and and values you're appending are greater than 15
       characters you should truncate the "base_name" only in order to be 15
       characters when combined with your additional characters. Note that the
       base_name can be greater than 15 characters.
    3. If the resource_type is "key_vault" you should append "kv-" to the
       front of "base_name" and then set all characters to lower case.
    4. If the resource_type is "storage_account" you should append "sa" to the
       front of "base_name and then remove all "-" from the name and then set
       all characters to lower case.
    5. You should also build a secondary module that calls your naming module.
       This parent module should intake a map which has the "base_name" as the
       key and the "resource_type" as the value. It should present each
       key/value pair in this map to your naming module.
    6. The Parent Module should reflect all the outputs of the child module
       and allow for additional outputs if the child module outputs are
       expanded in the future without further modification to the parent.
    7. Please write these modules as you would for a production environment
       following best practices and structure that makes it easy to share
       with other team members and allows them to use it quickly after
       receiving it.
    8. You can reference the naming module either through a local path or a
       github URL as long as the entire package can be run from a computer
       with public internet access.


My Approach
-----------

Whew - that's a lot to read.

Although I knew what Terraform is, my experience with it is very limited.
So first and foremost, I read the `Get Started - AWS <https://developer.hashicorp.com/terraform/tutorials/aws-get-started>`__
tutorial. To avoid unintentionally incurring costs, I used `LocalStack <https://github.com/localstack/localstack>`__
instead of AWS for my testing.

After completing the tutorial, I relied heavily on the `Terraform documentation <https://developer.hashicorp.com/terraform/language>`__
to complete the prompt.

Here is the project structure I ended up with.

.. uml::

   @startfiles
   /main.tf
   /batch/
   /batch/main.tf
   /batch/variables.tf
   /batch/outputs.tf
   /naming/
   /naming/main.tf
   /naming/variables.tf
   /naming/locals.tf
   /naming/outputs.tf
   /outputs.tf
   /versions.tf
   /terraform.tf
   /tests/batch.tftest.hcl
   /tests/naming.tftest.hcl
   @endfiles
   
The specifics of these files is documented in :ref:`Resource Name Mapper`.

``resource_type`` Constraints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. pull-quote::

    1. You should setup the "resource_type" to only allow the values of
       "virtual_machine", "key_vault", and "storage_account"

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2b/naming/variables.tf
   :language: tf
   :linenos:
   :lineno-match:
   :lines: 6 - 14
   :caption: :download:`naming/variables.tf <../_static/files/2025/interview_coding_take_homes_part_2b/naming/variables.tf>`

This requirement uses an `input variable <https://developer.hashicorp.com/terraform/language/values/variables>`__
block that contains a `validation <https://developer.hashicorp.com/terraform/language/values/variables#custom-validation-rules>`__
block. The `contains(list, value) <https://developer.hashicorp.com/terraform/language/functions/contains>`__
function is used to constrain the input variable to the three acceptable values.

``base_name`` and ``resource_name`` Alterations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. pull-quote::

    2. If the resource_type is "virtual_machine" you should take the
       "base_name" and append "vm-" to the front of it and "-00" to the back.
       If the base name and and values you're appending are greater than 15
       characters you should truncate the "base_name" only in order to be 15
       characters when combined with your additional characters. Note that the
       base_name can be greater than 15 characters.
    3. If the resource_type is "key_vault" you should append "kv-" to the
       front of "base_name" and then set all characters to lower case.
    4. If the resource_type is "storage_account" you should append "sa" to the
       front of "base_name and then remove all "-" from the name and then set
       all characters to lower case.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2b/naming/locals.tf
   :language: tf
   :linenos:
   :lineno-match:
   :lines: 2 - 6
   :caption: :download:`naming/locals.tf <../_static/files/2025/interview_coding_take_homes_part_2b/naming/locals.tf>`

This requirement is handled by a lengthy `conditional expression <https://developer.hashicorp.com/terraform/language/expressions/conditionals#conditional-expressions>`__.

Line 3 is specific to ``virtual_machine``'s ``base_name``. As the requirements
state, we truncate the ``base_name`` to 15 characters, minus the length of
the ``vm-`` prefix and ``-00`` suffix we add to the ``resource_name``.

Both ``key_vault`` and ``storage_account`` are handled here as well.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2b/naming/locals.tf
   :language: tf
   :linenos:
   :lineno-match:
   :lines: 8 - 12
   :caption: :download:`naming/locals.tf <../_static/files/2025/interview_coding_take_homes_part_2b/naming/locals.tf>`

And here we use another conditional expression to add the prefix and suffix to
the resource names.

Secondary Module
^^^^^^^^^^^^^^^^

    5. You should also build a secondary module that calls your naming module.
       This parent module should intake a map which has the "base_name" as the
       key and the "resource_type" as the value. It should present each
       key/value pair in this map to your naming module.

I've named this module ``batch`` because it processes a "batch" of resources together.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2b/batch/variables.tf
   :language: tf
   :linenos:
   :caption: :download:`batch/variables.tf <../_static/files/2025/interview_coding_take_homes_part_2b/batch/variables.tf>`

The module takes the input ``resources`` as a ``string`` `map <https://developer.hashicorp.com/terraform/language/functions/map>`__.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2b/batch/main.tf
   :language: tf
   :linenos:
   :caption: :download:`batch/main.tf <../_static/files/2025/interview_coding_take_homes_part_2b/batch/main.tf>`

The ``batch`` module uses the ``naming`` module. From the ``resources``
input variable, ``base_name`` is set to its key, and ``resource_type``
is set to its value.

.. pull-quote::

    6. The Parent Module should reflect all the outputs of the child module
       and allow for additional outputs if the child module outputs are
       expanded in the future without further modification to the parent.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2b/batch/outputs.tf
   :language: tf
   :linenos:
   :lineno-match:
   :lines: 1 - 4
   :caption: :download:`batch/outputs.tf <../_static/files/2025/interview_coding_take_homes_part_2b/batch/outputs.tf>`
   
The module sets the ``resource_names`` `output <https://developer.hashicorp.com/terraform/language/values/outputs>`__
variable as an `object <https://developer.hashicorp.com/terraform/language/expressions/for#result-types>`_
that reflects the outputs from the ``naming`` module.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2b/batch/outputs.tf
   :language: tf
   :linenos:
   :lineno-match:
   :lines: 6 - 8
   :caption: :download:`batch/outputs.tf <../_static/files/2025/interview_coding_take_homes_part_2b/batch/outputs.tf>`

The requirement for "future" outputs wasn't completely clear to me, so I
opted to just return all possible outputs from the ``naming`` module.
This way, any new outputs added to that module will also output in the
``batch`` module as the ``all_naming_outputs`` output variable.

Production Quality
^^^^^^^^^^^^^^^^^^

.. pull-quote::

    7. Please write these modules as you would for a production environment
       following best practices and structure that makes it easy to share
       with other team members and allows them to use it quickly after
       receiving it.

To the best of my knowledge, I followed Terraform's best practices when
writing these modules, and the structure (the names of the files and their
contents) reflects what I found in their `documentation <https://developer.hashicorp.com/terraform/language/modules/develop/structure>`__.

Tests
~~~~~

Of course, any production system needs tests. I added several tests for both modules.

Their contents are truncated here, but you can download the files to see each test.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2b/tests/batch.tftest.hcl
   :language: hcl
   :linenos:
   :lineno-match:
   :lines: 1 - 17
   :caption: :download:`tests/batch.tf <../_static/files/2025/interview_coding_take_homes_part_2b/tests/batch.tftest.hcl>`

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2b/tests/naming.tftest.hcl
   :language: hcl
   :linenos:
   :lineno-match:
   :lines: 1 - 17
   :caption: :download:`tests/naming.tf <../_static/files/2025/interview_coding_take_homes_part_2b/tests/naming.tftest.hcl>`

|cta|
|disqus|