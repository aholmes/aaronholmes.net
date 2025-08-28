:orphan:

Resource Name Mapper
====================

There are two modules:

* ``naming``
* ``batch``

The root module
---------------

The root module only demonstrates the use of ``naming`` and ``batch``. These examples are in `main.tf <../_static/files/2025/interview_coding_take_homes_part_2b/main.tf>`__.

naming
^^^^^^

The module ``naming`` accepts a ``base_name`` and ``resource_type`` input.

* ``base_name`` can be any ``string``.
* ``resource_type`` is a ``string`` and must be one of ``virtual_machine``, ``key_vault``, or ``storage_account``.

An output, ``resource_name`` is returned. Its value is the reformatted ``base_name`` based on its ``resource_type``.

The following transformations are applied to ``base_name`` based on ``resource_type``:

* ``virtual_machine`` prepends ``vm-`` and appends ``-00``. ``base_name`` is limited to 15 characters.
* ``key_vault`` prepends ``kv-``. ``base_name`` characters are lower-cased.
* ``storage_account`` prepends ``sa``. ``base_name`` removes hyphens, and is lower-cased.

Here are examples of this module's output for the ``resource_name``.

.. list-table::
   :header-rows: 1
   :align: left

   * - ``base_name``
     - ``resource_type``
     - ``resource_name``
   * - ``VERY-long-virtual-machine-name``
     - ``virtual_machine``
     - ``vm-VERY-long-00``
   * - ``CrAzY-Kv-NaMe``
     - ``key_vault``
     - ``kv-crazy-kv-name``
   * - ``CrAzY-Sa-NaMe``
     - ``storage_account``
     - ``sacrazysaname``

batch
^^^^^

The module ``batch`` accepts an input ``resources`` that is a map of ``{ "base_name" = "resource_type" }``. This allows the creation of several ``resource_name``s without invoking the ``naming`` module directly.

In the map, the key is ``base_name`` and the value is ``resource_type``. The inputs follow the same rules as the ``naming`` module.

* ``base_name`` can be any ``string``.
* ``resource_type`` is a ``string`` and must be one of ``virtual_machine``, ``key_vault``, or ``storage_account``.

An output, ``resource_names`` is returned. Its value is a map of ``{ "base_name" = "resource_name" }`` where ``resource_name`` is the transformed ``base_name`` value from the ``naming`` module.

Here are examples of this module's output for the ``resource_names``.

.. list-table::
   :header-rows: 1
   :align: left

   * - ``resources``
     - ``resource_names``
   * - ``{"VERY-long-virtual-machine-name" = "virtual_machine"}``
     - ``{"VERY-long-virtual-machine-name" = "vm-VERY-long-00"}``
   * - ``{"CrAzY-Kv-NaMe" = "key_vault"}``
     - ``{"CrAzY-Kv-NaMe" = "kv-crazy-kv-name"}``
   * - ``{"CrAzY-Sa-NaMe" = "storage_account"}``
     - ``{"CrAzY-Sa-NaMe" = "sacrazysaname"}``

Tests
-----

Run ``terraform test`` to execute automated tests for these modules.
